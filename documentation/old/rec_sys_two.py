# python3 rec_sys_two.py
# MAE = 1.03
import math
import random
from random import randrange

def importTrainingData():
  trainingfile = open('../data/train.txt', 'r')
  unfiltered_user_list = {} # will store whole user list here
  i = 0 # starting i at 0 means that training users will have id#s 0-199

  for singleline_content in trainingfile:
    singleline_content = [l.strip('\n') for l in singleline_content.split()]
    singleline_content = list(map(int, singleline_content))
    unfiltered_user_list[i] = singleline_content 
    i+=1

  #print(i) # this results in 200 which is correct because there are 200 users in training data
  return unfiltered_user_list

def importActiveUserData(filename):
  testfile = open(filename, 'r')
  active_users = {}
  i = 0
  for singleline_content in testfile:
    singleline_content = [l.strip('\n') for l in singleline_content.split()]
    singleline_content = list(map(int, singleline_content))
    if singleline_content[0] not in active_users: # just making sure not dup users
      active_users[singleline_content[0]] = [] # creating an array for each active user#, the array will contain the item# followed by the rating
    
    active_users[singleline_content[0]].append((singleline_content[1] , singleline_content[2]))
    i+=1
  
  #print(i) # prints '8497' which is correct for test5.txt
  return active_users

def output_results(prediction_results):
  #print(len(prediction_results))
  output_file = open("results5.1.txt", "w")
  
  i = 0
  for i in range(len(prediction_results)):
      output_file.write("{} \n".format(prediction_results[i]))
      i += 1
      
    
def separateAuRatings(data):
  filtered_data = data
  new_data = {}
  #print(filtered_data.get(201)[0][1]) #returns 'key' inside the 0th element inside key 201
  #print(len(filtered_data.get(201))) #returns length of a key
  # x = list(filtered_data.get(201))
  # x.append((0,0))
  # print(x)
  for key, value in filtered_data.items():
    #print(key, value)
    temp = []
    for i in range(len(value)):
      #print(value[i])
      if value[i][1] > 0:
        #print(value[i][1], "is not zero")
        temp.append(value[i])
      else:
        #print(value[i][1], "is zero")
        continue
        
    new_data.update({key: temp})
    #print(new_data)
    #break
    
  return new_data


def separateAuUnknownRatings(data):
  filtered_data = data
  new_data = {}
  for key, value in filtered_data.items():
    #print(key, value)
    temp = []
    for i in range(len(value)):
      #print(value[i])
      if value[i][1] == 0:
        #print(value[i][1], "is not zero")
        temp.append(value[i])
      else:
        #print(value[i][1], "is zero")
        continue
        
    new_data.update({key: temp})
    #print(new_data)
     
  return new_data

def calcSimilarity(active_users, training_users):
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
    #print(active_users.get(key))
    #break
    temp_training_users = training_users.copy()
    filter1_training_users = filterUnrelatedUsers(active_users.get(key), temp_training_users)
    #print(filter1_training_users)
    # now all the training users with less than 1 match with given active user are deleted
    temp_sim_holder = []
    temp_sim_holder = getSimilarity(active_users.get(key), filter1_training_users) #temp_sim_holder should return 
    #print(temp_sim_holder[0][0]) # prints 6 when array is sorted for test5.txt
    similarity_dict.update({key: (temp_sim_holder)})
    #print(similarity_dict)
    #break # for some reason removing/commentingout this break will literally break the program
  return similarity_dict


def getSimilarity(activeuser, training_users):
  # here I am calculating the CosSim between given user 'activeuser' and the users in 'training_users'
  top = 0 # numerator
  bot = 0 # denominator
  bot2 = 0 # second part of denom
  temp_num = 0
  ret_arr = []
  #print(activeuser[0][1])
  #print(training_users.get(0)[306])
  #print(len(training_users))
  for testuser in training_users:
    #print(testuser)
    #break
    for i in range(len(activeuser)):
      if training_users.get(testuser)[activeuser[i][0]] > 0:
        #print(training_users.get(testuser)[activeuser[i][0]])
        #print(activeuser[i][1])
        top += ((training_users.get(testuser)[activeuser[i][0]])*(activeuser[i][1]))
        #print(top)
        bot += ((training_users.get(testuser)[activeuser[i][0]])*(training_users.get(testuser)[activeuser[i][0]]))
        bot2 += ((activeuser[i][1])*(activeuser[i][1]))

    botf = 0
    sim_result = 0.0
    botf = ((math.sqrt(bot)) * (math.sqrt(bot2)))
    sim_result = (top / botf)
    # print("testuser#:", testuser,"  sim =", sim_result)
    ret_arr.append((testuser, sim_result))
    
  ret_arr1 = sorted(ret_arr, key=lambda x: x[1], reverse=True) #NOTE THIS IS HOW WE SORT BE SECOND ELEMENT!!!
  #print(ret_arr1)
  return ret_arr1


def filterUnrelatedUsers(activeuser, training_users):
  #print(activeuser[0][0])
  #print(len(activeuser))
  #print(len(training_users.get(0))) # should print 1000
  #print(training_users.get(0)[0])
  #print(training_users.get(1)[306], "yeyeyey")
  training_users1 = training_users.copy()
  y=0
  #print(len(training_users), '= # of training users given')
  #print(len(activeuser))

  for y in range(len(training_users1)):
    #print("training_user#: ",y)  
    count = 0 # increase as we gain matches
    for i in range(len(activeuser)):
      #print(training_users1.get(y)[activeuser[i][0]], "testtters")
      if training_users1.get(y)[activeuser[i][0]] > 0:
        #print(activeuser[i][0])
        #print("das a match")
        count +=1
     

    if count <= 1:
      del training_users1[y]
      #print("deleted element ", y, "from training users")
  #print('finished')
  return training_users1

def predictRatingsForActiveUsers(active_user_sim_dict, active_users_unknown, training_users):
  #for each unrated movie(i) for an active user
    # filter NU that have not rated movie(i)
    # calc predicted rating with weighted average of K users
  #print(active_users_unknown)
  final_predicted_ratings = {}
  k = 5 # number of neighbors from neighborhood that we will use to predict rating... will just use maximum possible users I think... some only have one user that can help them
  #print(len(active_users_unknown.get(201))) # gives the number of unrated items for user 201
  #print()
  
  for activeuser, value in active_users_unknown.items():
    #print(activeuser, active_user_sim_dict.get(activeuser), training_users[72][361])
    #print(" ")
    active_user_predicted_ratings = []
    sim_dict = active_user_sim_dict.get(activeuser).copy()
    # print(sim_dict)
    #print(" ")
    #print(activeuser)
    for i in range(len(value)):
      filter2_training_dict = []
      filter2_training_dict = filter_tu_norating(value[i][0], training_users, sim_dict)
      #print(value[i][0])
      #I think filter_tu_norating may need to have an edge case where there there are no trainingusers that have rated a particular movie
      # YES ^ is true... the possible user count is = 0
      #print(filter2_training_dict)
      if(filter2_training_dict) != []:
        pred_rating = 0
        pred_rating = preditRatingForItem(filter2_training_dict)
        #print(pred_rating)
        #print(value[i][0])
        #print(activeuser)
        active_user_predicted_ratings.append((value[i][0],pred_rating))
        #print(active_user_predicted_ratings)
      else:
        active_user_predicted_ratings.append((value[i][0], 1)) # change '1' back to '-1' to see which movies, for specific user, do not have similar user ratings
      #break #one item
    #break #one user, all items
    final_predicted_ratings.update({activeuser: (active_user_predicted_ratings)})
  return final_predicted_ratings

def preditRatingForItem(weights_and_ratings):
  #print(weights_and_ratings)
  #print(len(weights_and_ratings))
  top = 0 
  bot = 0
  for item in weights_and_ratings:
    temp = 0
    #print(item[0])
    top += (item[0]*item[1])
    bot += (item[0])

  final_res = 0
  final_res = (top / bot)
  #print(top, "/", bot, "=", final_res)
  #print(final_res)
  return final_res

def filter_tu_norating(item_number, tu_dict, au_sim):
  au_sim_tu = au_sim.copy()
  #print(au_sim_tu)
  weight_rating_list = [] # weight_rating_list will contain the [(weight of TU1, TU1 rating), (weight of TU2, TU2 rating)......]
  #print(len(au_sim_tu))
  #print(au_sim_tu)
  i = 0
  possible_neighbor_count = 0
  #print(item_number) !
  #print(len(au_sim_tu))
  for i in range(len(au_sim_tu)): #user = user we are checking to make sure they have rated movie 'item_number'
    #print(tu_dict[au_sim_tu[i][0]])
    # print("traininguser#:", au_sim_tu[i][0])
    # print(tu_dict[au_sim_tu[i][0]][item_number])
    try:
      if tu_dict[au_sim_tu[i][0]][item_number] > 0:
        possible_neighbor_count +=1
        #print("#",possible_neighbor_count)
        #print(au_sim_tu[i][1], tu_dict[au_sim_tu[i][0]][item_number])
        rounded = (tu_dict[au_sim_tu[i][0]][item_number]) #took out rounding here it was not doing anything
        weight_rating_list.append((au_sim_tu[i][1], rounded))
        #print(tu_dict.get(user[0])[item_number])
      # else:
      #   print("cant use TU#=", au_sim_tu[i][0])
    except:
        #print(item_number, au_sim_tu[i][0])
        weight_rating_list.append((au_sim_tu[i][1], -100))
             
  #print(weight_rating_list)
  #print("#",possible_neighbor_count) !

  return weight_rating_list


def writeRatingsToFile(ratings):
  output_file = open("resultsTEST20.txt", "w")

  for key, item in ratings.items():
    i=0
    for i in range(len(item)):
      # print(key, round(item[i][0]), round(item[i][1]))
      output_file.write("%i %i %i\n" % (key, round(item[i][0]), round(item[i][1])))



# execute functions below
training_data = importTrainingData()
# training data = {0: [rating(item0)...rating(total_item_count - 1)], 1:... 199:}
# more genereally, training_data = {item#: [ratings for each item],}
#print("imported and formatted all training data...")
#print(training_data.get(0)[0]) # prints 5 which is the 0th elements rating of the 0th movie

#now importing and formatting active user data
active_user_data = importActiveUserData("test20.txt")
#print("imported and formatted all active user data...")
#print(active_user_data.keys()) # prints 201 - 300, this is correct
#print(active_user_data)

active_user_rated_dict = separateAuRatings(active_user_data)
#print(active_user_rated_dict)

active_users_unknown_ratings = separateAuUnknownRatings(active_user_data)
#print(active_users_unknown_ratings)
# after this point the tests data should be separated into two dictionaries
#   1. active_user_rated_list will contain all the elements with known ratings for users in the test files.
#   2. active_user_unknown_ratings will contain all the elements with unknown ratings

neighbors_for_each_activeuser = calcSimilarity(active_user_rated_dict, training_data) #using cosine similarity here to find neighbors
#print(neighbors_for_each_activeuser.get(205))
#print("rating is: ",training_data.get(47)[205])

predicted_ratings = predictRatingsForActiveUsers(neighbors_for_each_activeuser, active_users_unknown_ratings, training_data)

#print(predicted_ratings)

writeRatingsToFile(predicted_ratings)

# def replace_zeros_with_rand(active_users):
#   # we should create a new array here that removes all the elements that have non-zero rating
#   rand_results = {}
#   singleline_result = []

#   for key in active_users:
#     i = 0
#     y = 0
#     for i in range(len(active_users[key])):
#       if active_users[key][i][1] == 0:
#         rand_results[y] = list(active_users[key][i])
#         rand_results[y][1] = randrange(5) + 1
#         str = "{} {} {}".format(key, rand_results[y][0], rand_results[y][1])
#         singleline_result.append(str)
#         y += 1
#         i += 1
#       else:
#         i += 1

#   return singleline_result