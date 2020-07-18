#user_similarity_calcs.py
import math
import sys
from random import randrange

#--------------------------------------------------------------------
# -------------------------BASIC CF-------------------------------
#--------------------------------------------------------------------
def calcBasicCFSimilarity(active_users, training_users, iuf, discounted_sim,number):
  #for each active users
    # get rid of TU w/ 1 or less ratings in common with AU
    # calculate CosSim for remaining TU (!note: not sorting the list here)
  # return dictionary where the keys are represent all the active_users, and there values are the trainingusersID and cooresponding similarity
  similarity_dict = {}
  #del active_users[300] #this deletes the 300th key and its values
  #print(active_users)
  #temp_training_users = training_users.copy()
  # print(temp_training_user, "# in training users before call")
  for key in active_users:
    #print(key)
    #sys.exit("key")
    #print(active_users.get(key))
    #break
    temp_training_users = training_users.copy()
    #print("active user = ",key)
    filter1_training_users = filterUnrelatedUsers(active_users.get(key), temp_training_users)
    #print(filter1_training_users.keys())
    
    # now all the training users with less than 1 match with given active user are deleted
    temp_sim_holder = []
    temp_sim_holder = getSimilarity(active_users.get(key), filter1_training_users, key, iuf, training_users, active_users, discounted_sim,number) #temp_sim_holder should return 
    #print(temp_sim_holder)
    #sys.exit("BF SIM")
    #print(temp_sim_holder[0][0]) # prints 6 when array is sorted for test5.txt
    similarity_dict.update({key: (temp_sim_holder)})
    #print(similarity_dict)
    #break # for some reason removing/commentingout this break will literally break the program
  return similarity_dict

def getSimilarity(activeuser, training_users, activeuserID, iuf, full_tu_dict, full_au_dict, discounted_sim, number): #activeuser = active user rating list, activeuserID = specific active user 
  #here I am calculating the CosSim between given user 'activeuser' and the users in 'training_users'
  #activeuser = [(movie#, rating)...]
  # top = 0 # numerator
  # bot = 0 # denominator
  # bot2 = 0 # second part of denom
  ret_arr = []

  for testuser in training_users:
    top = 0 # numerator
    bot = 0 # denominator
    bot2 = 0 # second part of denom
    # can play with beta values to try to fine tune MAE 
    if number == 5:
      beta = 3
    elif number == 10:
      beta = 5
    elif number == 20:
      beta = 7
    else:
      sys.exit("INVALID NUMBER IN SIM CALCS")
   # print(testuser)
    #print(activeuser)
    counter = 0
    for i in range(len(activeuser)):
      if training_users.get(testuser)[activeuser[i][0] - 1] > 0: # if program goes into this if statement that should mean that both AU and TU have rated the item
        #calc IUF
        # print("in IUF BCF")
        # sys.exit("IN IUF BCF")
        #print("movie# ", activeuser[i][0],"has iuf weight = ",iuf_factor)
        ra = (activeuser[i][1])
        rt = (training_users.get(testuser)[activeuser[i][0]-1])
        counter +=1
        #print("AU rating = ", ra, "TU rating = ", rt)
        if iuf == 1:
          iuf_factor = getIUF(activeuser[i][0], full_tu_dict, full_au_dict) # activeuser[i][0] = movie #
          top += (ra*rt*iuf_factor)
          bot += ((rt*rt)*iuf_factor)
          bot2 += ((ra*ra)*iuf_factor)
        else:       
          top += (ra*rt)
          bot += (rt*rt)
          bot2 += (ra*ra)
      
       
    #print(counter)
    botf = 0
    sim_result = 0.0
    botf = ((math.sqrt(bot)) * (math.sqrt(bot2)))
    sim_result = (top / botf)
    # print("testuser#:", testuser,"  sim =", sim_result)
    if (discounted_sim == 1) and ((number != 20) or (number != 10)):
      sim_result = (sim_result * ((min(counter, beta))/beta))

    if sim_result > 1:
      sim_result = 1.0
    ret_arr.append((testuser, sim_result))
    
  ret_arr1 = sorted(ret_arr, key=lambda x: x[1], reverse=True) #NOTE THIS IS HOW WE SORT BE SECOND ELEMENT!!!
  #print(ret_arr1)
  return ret_arr1


#--------------------------------------------------------------------
# -------------------------Pearson-------------------------------
#--------------------------------------------------------------------
def calcPearsonCoorSimilarity(active_users, training_users, au_avg_rating_dict, tu_avg_rating_dict, iuf):
  #NOTE active_users = dictionary of active users and rated movies
  #for each active users
    # get rid of TU w/ 1 or less ratings in common with AU
    # calculate CosSim for remaining TU (!note: not sorting the list here)
  # return dictionary where the keys are represent all the active_users, and there values are the trainingusersID and cooresponding similarity
  similarity_dict = {}
  abs_sim_dict = {}
  for key in active_users:
    #print("AU# = ", key)
    temp_training_users = training_users.copy()
    filter1_training_users = filterUnrelatedUsers(active_users.get(key), temp_training_users) #deleting all TU w/ less than 1 movie rating in common w/ AU
    # now all the training users with less than 1 match with given active user are deleted
    temp_sim_holder = []
    temp_sim_holder, abs_sim_holder = getPearsonSimilarity(active_users.get(key), filter1_training_users, au_avg_rating_dict, tu_avg_rating_dict, key, iuf, 
    training_users, active_users) #temp_sim_holder should return 
    # print(temp_sim_holder)
    # sys.exit("PEARSIM")
    #print(temp_sim_holder)
    #break
    similarity_dict.update({key: (temp_sim_holder)})
    abs_sim_dict.update({key: (abs_sim_holder)})    
  return similarity_dict, abs_sim_dict
  #return 0

def getPearsonSimilarity(activeuser, training_users, au_avg_rating_dict, tu_avg_rating_dict, activeuserID, iuf, full_tu_dict, full_au_dict): #activeuser = active user rating list, activeuserID = specific active user 
  #activeuser = [(movie#, rating)...]
  # here I am calculating the CosSim between given user 'activeuser' and the users in 'training_users'
  # top = 0 # numerator
  # bot = 0 # denominator
  # bot2 = 0 # second part of denom
  ret_arr = []
  abs_ret_arr = []
  #print(activeuserID)
  # print(activeuser)
  # print(au_avg_rating_dict.get(activeuserID))
  for testuser in training_users:
    #print(au_avg_rating_dict[activeuserID])
    #print(tu_avg_rating_dict[testuser])
    #print("TU#=",testuser)
    top = 0 # numerator
    bot = 0 # denominator
    bot2 = 0 # second part of denom
    for i in range(len(activeuser)):
      if training_users.get(testuser)[activeuser[i][0]-1] > 0: # if program goes into this if statement that should mean that both AU and TU have rated the item
        #print("traininguser", testuser, "rated movie #",activeuser[i][0],#"@ score =", training_users.get(testuser)[activeuser[i][0]-1])
       # print("traininguser average:",tu_avg_rating_dict[testuser])
        #print("active average:",au_avg_rating_dict[activeuserID])
        
        # SUBTRACTING AVG RATING of AU & TU from their rating of a particular movie (particular movie = activeuser[i][0])
        ra = ((activeuser[i][1]) - au_avg_rating_dict[activeuserID])
        rt = ((training_users.get(testuser)[activeuser[i][0]-1]) - tu_avg_rating_dict[testuser])
        #print(ra)
        #print(rt)
        if iuf == 1: # if using IUF
          iuf_factor = getIUF(activeuser[i][0], full_tu_dict, full_au_dict) # activeuser[i][0] = movie #
         # print("iuf weight =",iuf_factor)
          top += (iuf_factor*ra*rt)
          #print("top=",top)
          bot += (iuf_factor*(ra*ra))
         # print("bot=",bot)
          bot2 += (iuf_factor*(rt*rt))
          #print("bot2=",bot2)
        else:
          top += (ra*rt)
          bot += (ra*ra)
          bot2 += (rt*rt)
      # else:
      #   print("trainginuser", testuser, "did NOT rate", activeuser[i][0])

    #print("sim = ", top, "/", math.sqrt(bot), "+", math.sqrt(bot2))
    botf = 0
    sim_result = 0.0
    botf = ((math.sqrt(bot)) * (math.sqrt(bot2)))
    #print(top, "/", botf)
    if(abs(botf) > 0.0):
      sim_result = (top / botf)
    if(sim_result > 1):
      sim_result = 1.0
      
    #print("trainguser#", testuser, "has similarity =", sim_result)
    #print(" ")
    # print("testuser#:", testuser,"  sim =", sim_result)
    ret_arr.append((testuser, sim_result))
    abs_ret_arr.append((testuser, abs(sim_result)))
    
  ret_arr1 = sorted(ret_arr, key=lambda x: abs(x[1]), reverse=True) #NOTE THIS IS HOW TOs SORT BE SECOND ELEMENT!!!
  #print(ret_arr1)
  #ret_arr1 = ret_arr
  abs_ret_arr1 = abs_ret_arr
  return ret_arr1, abs_ret_arr1


#---------------------------------------------
#----------------HELPERS----------------------
#---------------------------------------------
def filterUnrelatedUsers(activeuser, training_users):
  #activeuser = the movies that a specific AU has rated
  training_users1 = training_users.copy()
  poss_neighbor = {}
  #y=0
  #print(len(training_users), '= # of training users given')
  unused_count = 0
  #for y in range(len(training_users1)): # should be same as "for user in training_users1:"... here user = y
  for user in training_users1:
    #print("training_user#: ",y)  
    count = 0 # increase as we gain matches
    for i in range(len(activeuser)):
      #print(training_users1.get(user)[activeuser[i][1000]])
      if training_users1.get(user)[activeuser[i][0]-1] > 0:
        #print("das a match")
        count +=1
    #print("TU#", user,"has", count, "ratings in common")
           
    if count > 1:
      # deleteing a lot of users here ... hmmmm
      #print("possible neighbor has ", count, "ratings in common with active user")
      poss_neighbor.update({user: (training_users1.get(user))})
    else:
      #del training_users1[user]
      #print("not using user# ", user)
      unused_count += 1 

  #print("for AU? not using ", unused_count, " out of ",len(training_users1))  
  return poss_neighbor


def getIUF(movie_num, all_training_users, all_active_users):
  iuf = 0
  number_of_ratings = 0 # number of ratings for specific movie
  #print(all_training_users)
  #print(all_active_users)
  total_num_users = 0
  for trainuser in all_training_users:
    #print(all_training_users.get(trainuser)[1000]) # movies# are between 0 - 999
    if all_training_users.get(trainuser)[movie_num - 1] > 0:
      number_of_ratings += 1
  
  for activeuser, item in all_active_users.items():  
    #print(item[0])
    for i in range(len(item)):
      if item[i][0] == movie_num:
        if item[i][1] > 0:
          number_of_ratings += 1
  

    
  total_num_users = len(all_training_users) + len(all_active_users)
  #print("log ", total_num_users, "/", number_of_ratings)
  iuf = math.log((total_num_users / number_of_ratings),2)
  #print(total_num_users)
  #print("=", iuf)
  #sys.exit(0)
  #print(training_user)
  #sys.exit("IUFBB")
  return iuf