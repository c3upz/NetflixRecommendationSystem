import sys
def predictRatingsPearCoor(simm_dict, active_users_unknown_ratings, training_data, active_user_rated_dict, au_avg_dict, tu_avg_dict, case_amplification, number):
  #print(simm_dict.get(201))
  final_predicted_ratings = {}
  #predicted rating = AU rating for
  #print(simm_dict)
  #exit(0)
  for activeuser,value in active_users_unknown_ratings.items():
   # print(user,value)
    active_user_predicted_ratings = []
    au_avg = au_avg_dict.get(activeuser)
    sim_dict = simm_dict.get(activeuser).copy()
    #print(user_avg)
    for i in range(len(value)):
      #print(value[i][1]) # all 0s
      filter2_training_dict = filter_tu_norating(value[i][0], training_data, sim_dict, 1)
      #print(filter2_training_dict) #PRINTS OUT CORRECTLY LEFT OFF HERE !
      #exit(0) 
   #  break
   # break
    
 #sometimes filter2_training_dict will be empty bc there are no similar users to AU that have rated target item i
      #if it is not empty we proceed as normal.. if it is empty I append a the users average rating for all movies
      if(filter2_training_dict) != []:
        pred_rating = 0
        #print(activeuser)
        pred_rating = preditRatingForItemPear(filter2_training_dict, au_avg, tu_avg_dict, case_amplification, number)
        #print(pred_rating)
        active_user_predicted_ratings.append((value[i][0],pred_rating))
      else: 
        # print(activeuser)
        #avg_movie_rating = getAvgMovieRating(value[i][0], training_users, activeuser, active_user_ratings)
        #au_avg_rating will be set equal to this particular active users average rating of all 5 movies
        #au_avg_rating = getActiveUserAverageRating(activeuser, active_user_ratings)
        #averg = ((int(avg_movie_rating)+int(au_avg_rating))/2)
        print("using avg")
        active_user_predicted_ratings.append((value[i][0], au_avg)) # putting in user avg if no users to base rating prediction off
      #break #one item
    #break #one user, all items
    final_predicted_ratings.update({activeuser: (active_user_predicted_ratings)})
    #print(final_predicted_ratings)
    #break
  return final_predicted_ratings
  #return 0

def preditRatingForItemPear(data, au_avg, tu_avg_dict, case_amplification, number):
  #data = [(tu#, weight, rating @ item i).....]
  #print(data)
  #print(case_amplification)
  rating = 0
  top_sum = 0
  bot_sum = 0
  ra = au_avg
  counter = 0
  for item in data:
    #print(item)
    #sys.exit("PREDICTPEAR")
    #break
    if(case_amplification == 1): #using Case Amp
      #calc new weight
      weight = (item[1] * ((abs(item[1]))**(1.5))) #calc new weight using case amp w/ p = .25
      #print("new weight= ", weight)
    else:
      #print("old weight=", item[1])
      weight = item[1]

    if(weight != 0.0):
      top1 = 0
      top2 = 0
      # could put if statements to change used weights / ratings by doc here
      if number == 5:
      # if abs(weight) > .6: #or (counter < 15 and abs(weight) > .55): 
        #if abs(weight) > .7:
        top1 = weight
        top2 = (item[2] - tu_avg_dict[item[0]])
        top_sum += (top1 * top2)
        bot_sum += abs(weight)
        counter += 1
      elif number == 10:
        #if abs(weight) > .6: #or (counter < 25 and abs(weight) > .55): 
        top1 = weight
        top2 = (item[2] - tu_avg_dict[item[0]])
        top_sum += (top1 * top2)
        bot_sum += abs(weight)
        counter += 1
      elif number == 20:
        #print("weight==",abs(weight))
      # if abs(weight) > .55: #or (counter < 35 and abs(weight) > .40):
        #if counter <  
        top1 = weight
        top2 = (item[2] - tu_avg_dict[item[0]])
        top_sum += (top1 * top2)
        bot_sum += abs(weight)
        counter += 1
      else:
        print("invalid number")
    else:
      print("weight=", weight)
    
  
  #print(counter)
  if counter == 0:
    #print("counter = 0")
    rating = au_avg
  else:
    #print(counter)
    if bot_sum == 0:
      fraction_part = 0  
    else:
      fraction_part = (top_sum / bot_sum) 
    
    rating = ra + (fraction_part)

  #print(rating)
  return rating # NOTE: we round rating when we are writing results to the file
#------------------------------------------------------------------------------------------------------------
#---------------------------ACTIVE USER PREDICTION------------------------------------------------------
#------------------------------------------------------------------------------------------------------------

def predictRatingsForActiveUsers(active_user_sim_dict, active_users_unknown, training_users, active_user_ratings, case_amplification, number):
  #for each unrated movie(i) for an active user
    # filter NU that have not rated movie(i)
    # calc predicted rating with weighted average of K users
  #print(active_users_unknown)
  final_predicted_ratings = {}
  #k = 5 # number of neighbors from neighborhood that we will use to predict rating... will just use maximum possible users I think... some only have one user that can help them
  #print(len(active_users_unknown.get(201))) # gives the number of unrated items for user 201
  #print()
  
  for activeuser, value in active_users_unknown.items():
    #print(activeuser, active_user_sim_dict.get(activeuser), training_users[72][361])
    #print(" ")
    active_user_predicted_ratings = []
    sim_dict = active_user_sim_dict.get(activeuser).copy()
    # print(sim_dict)
    #print(activeuser)
    for i in range(len(value)):
      filter2_training_dict = []
      #filter2_training_dict returns a list of values in the format "[(similarity1, rating1),(similarity2, rating2),...(similarityN, ratingN)]"
      #filter2_training_dict should have all the TU that have rated item #value[i][0]
      #print
      filter2_training_dict = filter_tu_norating(value[i][0], training_users, sim_dict, 0)
     # print(filter2_training_dict) # HERHE#HREHREHREHRH
      #break
      #sometimes filter2_training_dict will be empty bc there are no similar users to AU that have rated target item i
      #if it is not empty we proceed as normal.. if it is empty I append a the users average rating for all movies
      if(filter2_training_dict) != []:
        pred_rating = 0
        pred_rating = preditRatingForItem(filter2_training_dict, case_amplification, number)
        # print(pred_rating)
        # break
        if pred_rating == 0:
          print("using active users average")
          au_avg_rating = getActiveUserAverageRating(activeuser, active_user_ratings)
          active_user_predicted_ratings.append((value[i][0], au_avg_rating))
        else:
          #print("rating=", pred_rating)
          active_user_predicted_ratings.append((value[i][0],pred_rating))
      else: 
        # print(activeuser)
        #avg_movie_rating = getAvgMovieRating(value[i][0], training_users, activeuser, active_user_ratings)
        #au_avg_rating will be set equal to this particular active users average rating of all 5 movies
        print("using active user avg rating v2")
        au_avg_rating = getActiveUserAverageRating(activeuser, active_user_ratings)
        #averg = ((int(avg_movie_rating)+int(au_avg_rating))/2)
        #print(au_avg_rating)
        active_user_predicted_ratings.append((value[i][0], au_avg_rating)) 
      #break #one item
    #break #one user, all items
    final_predicted_ratings.update({activeuser: (active_user_predicted_ratings)})
  return final_predicted_ratings
  #return 0 #WAS CHECKING FILTER2_TRAINING_DICT BEFORE I LEFT FOR WALK

def preditRatingForItem(weights_and_ratings, case_amplification, number):
  #item[0] = weight, item[1] = rating
  top = 0 
  bot = 0
  weight = 0
  counter = 0
  # print(weights_and_ratings)
  #sys.exit(0)
  for item in weights_and_ratings:
    #    print("item",item)
   # #print("old weight = ", item[0], ((abs(item[0]))**.25))
    if case_amplification == 1: # then we case amp
      weight = (item[0] * ((abs(item[0]))**1.5))
     # print("new weight = ", weight)
      #sys.exit("IN CA")
    else:
     # print("old weight = ", item[0])
      weight = item[0]
    if(weight != 0):
      top += (weight*item[1])
      bot += (weight)
      counter +=1
    else:
      print("weight=", weight)
    # if number  == 5:
    #   if abs(weight) > .9: # threshold
    #     top += (weight * item[1])
    #     bot += (weight)
    #     counter +=1
    # elif number == 10:
    #   if abs(weight) > .9: # threshold
    #  # print("rating = ", weight, "*", item[1], " = ", (weight*item[1]))
    #     top += (weight*item[1])
    #     bot += (weight)
    #     counter +=1
    # elif number == 20:
    #   if abs(weight) > .9: # threshold
    # # print("rating = ", weight, "*", item[1], " = ", (weight*item[1]))
    #     top += (weight*item[1])
    #     bot += (weight)
    #     counter +=1
    # else:
    #   sys.exit("invalid number")
   
    
  #print("counter = ",counter)
  if counter > 0:
    if abs(top) > 0:
      final_res = (top / bot)
    else:
      final_res = -100
    #print("       FINAL RESULT = ", final_res)
    #print("inside counter: ",counter)
    return final_res
  #print("using active users average", )
  return 0
  #here I am just returning the avg rating of a particular item

def getAvgMovieRating(movie_number, training_users, activeuser_number, active_user_ratings):
  #print(movie_number)
  #print(training_users.get(0)[movie_number])
  #for i in range(len(training_users.get(i)))
  summ = 0
  avgg = 0
  count = 0
  for i in range(len(training_users)):
    #print(training_users.get(user)[movie_number])
    if int(training_users.get(i)[movie_number - 1]) > 0:
      summ += int(training_users.get(i)[movie_number - 1])
      count += 1
    # print(len(training_users))
  if(count > 0):
    avgg = (summ / count)
    #print(avgg)
    return avgg
  return 0
  #here I am just returning the avg rating given by a an active user
def getActiveUserAverageRating(activeuser_number, active_user_ratings):
  #print(activeuser_number)
  # print(active_user_ratings)
  temp = active_user_ratings.get(activeuser_number)
  rating_sum = 0 
  for i in range(len(temp)):
    #print(temp[i][1]) # prints the activeusers ratings
    rating_sum += temp[i][1]

  avg = rating_sum / len(temp)
  return avg

def filter_tu_norating(item_number, tu_dict, au_sim, pearson):
  #print(au_sim)
  #sys.exit("filtertu")
  au_sim_tu = au_sim.copy()
  #print(au_sim_tu)
  weight_rating_list = [] # weight_rating_list will contain the [(weight of TU1, TU1 rating), (weight of TU2, TU2 rating)......]
  #print(len(au_sim_tu))
  #print(au_sim_tu)
  i = 0
  possible_neighbor_count = 0
  #print(item_number) !
  #print((au_sim_tu))
  for i in range(len(au_sim_tu)): #user = user we are checking to make sure they have rated movie 'item_number'
    #print(tu_dict[au_sim_tu[i][0]][item_number])
    # print("traininguser#:", au_sim_tu[i][0])
    #print(tu_dict[au_sim_tu[i][0]][1000])
    #sys.exit("1000")
    try:
      if tu_dict[au_sim_tu[i][0]][item_number -1] > 0:
        #print(tu_dict[au_sim_tu[i][0]][1000])
        #print(au_sim_tu)
        #print(len(tu_dict[au_sim_tu[i][0]]))
        possible_neighbor_count +=1
        #print("#",possible_neighbor_count)
        #print(au_sim_tu[i][1], tu_dict[au_sim_tu[i][0]][item_number])
        rounded = (tu_dict[au_sim_tu[i][0]][item_number-1]) #took out rounding here it was not doing anything
        if(pearson == 0):
          weight_rating_list.append((au_sim_tu[i][1], rounded))
        elif(pearson == 1):
          weight_rating_list.append((au_sim_tu[i][0],au_sim_tu[i][1], rounded))
        else:
          print("not using basic user CF or Pearson????")
    except:
        print("error within 'fitler_tu_norating', length: ",len(tu_dict[au_sim_tu[i][0]]))
        if(pearson == 0):
          weight_rating_list.append((au_sim_tu[i][1], -100))
        elif(pearson == 1):
          weight_rating_list.append((au_sim_tu[i][0],au_sim_tu[i][1], -100))
        else:
          print("not using basic user CF or Pearson???? in except")
             
  #print(weight_rating_list)
  #print("#",possible_neighbor_count) !

  return weight_rating_list