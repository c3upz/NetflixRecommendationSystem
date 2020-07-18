import math
import sys
from user_similarity_calcs import getIUF
from main import getTUAverageRating, getActiveUserAverageRating # used for adjusted cos
def predict(training_data, active_items_known_ratings, active_items_unknown_ratings, case_amplification, mean_centered):
  #print(active_items_unknown_ratings)
  final_pred_ratings = {}
  for user, movies in active_items_unknown_ratings.items():
    predicted_rating = []
    for i in range(len(movies)):
      active_item = movies[i][0]
      #print(active_item)
      item_and_sim = []
      for item in active_items_known_ratings.get(user):
        #print(item[y][0])
        train_item = item[0]
        sim_rating_list = getAllUsersWhoRated(active_item, train_item, training_data, mean_centered)
        #sim_rating_list= [(item[0](active movie rating), item[1](trainmovie rating))...]
       # print(sim_rating_list)
        #sys.exit("PREDICT MEAN")
        if(sim_rating_list != []):
          similarity = calcSim(sim_rating_list)
          trainrating = item[1]
          if similarity == -100:
            continue
          else:
            item_and_sim.append((train_item, similarity, trainrating))
        else:
          #print("no users who have rated both trainingitem and active item")
          continue
        #print(item_and_sim)
      if(item_and_sim != []):
        pr = predictRating(item_and_sim, case_amplification)
        if pr < 1:
          pr = 3#getMovieAvgRating(active_item, training_data)
  
        predicted_rating.append((active_item, pr))
      else:
        predicted_rating.append((active_item, 3)) # pred rating = activeitems avg if cant item w/ similarity
        # active_item_avg = getMovieAvgRating(active_item, training_data)
        # if(active_item_avg != 100):
        #   predicted_rating.append((active_item, 3)) # pred rating = activeitems avg if cant item w/ similarity
        # else:
        #   predicted_rating.append((active_item, 3)) # pred rating = activeitems avg if cant item w/ similarity
    
    final_pred_ratings.update({user: (predicted_rating)})
    #print(final_pred_ratings)
    #sys.exit("Results for 201")
    
  #print(final_pred_ratings)
  #want to find items that are similar to item i
  return final_pred_ratings

def predictRating(item_sim_dict, case_amplification):
  #item_sim_dict = {trainitem#: (docID#,similarity, rating)....}
  # print(item_sim_dict)
  # sys.exit("predict")
  #print(item_sim_dict)
  #sys.exit(0)
  top = 0
  bot = 0
  for item in item_sim_dict:
    if case_amplification == 1:
      sim_weight = item[1]*((abs(item[1])**1.5))
    else:
      sim_weight = item[1]
    
    if(abs(sim_weight) > 0):
      trainrating = item[2]
      top += (sim_weight * trainrating)
      bot += (abs(sim_weight))
      
  #print("")
  #print(top)
  #print(bot)
  #if((top != 0) and (bot != 0)):
  if(abs(bot) > 0):
    predicted_rating = (top / bot)
  else:
    predicted_rating = -200
  #print(predicted_rating)
  #sys.exit("rating")
  return predicted_rating

def getAllUsersWhoRated(activemovieID, trainmovieID, training_data, mean_centered):
  #print(movieid)
  sim_rating_list = []
  if mean_centered == 1:
    active_movie_avg = 2.5#getMovieAvgRating(activemovieID, training_data) # could try '2.5' instead of items average rating
    train_movie_avg = 2.5#getMovieAvgRating(trainmovieID, training_data)
  for user in training_data:
      #print(user)
      #print(training_data.get(user)[activemovieID-1])
      if ((training_data.get(user)[activemovieID-1] > 0) and (training_data.get(user)[trainmovieID-1] > 0)):

        # print("user#",user, " rated item activemovie#",activemovieID, "@ score", (training_data.get(user)[activemovieID-1]))
        # print("user#",user, " rated item trainemovie#",trainmovieID, "@ score", (training_data.get(user)[trainmovieID-1]))
        #training_data.get(user)
        if mean_centered == 1:
          adjusted_active_rating = ((training_data.get(user)[activemovieID-1])-active_movie_avg)
          adjusted_train_rating = ((training_data.get(user)[trainmovieID-1])-train_movie_avg)
          #if((active_movie_avg != 100) and (train_movie_avg != 100)):
          sim_rating_list.append((adjusted_active_rating, adjusted_train_rating))
        else:
          sim_rating_list.append((training_data.get(user)[activemovieID-1], training_data.get(user)[trainmovieID-1]))

  return list(sim_rating_list)

def getMovieAvgRating(movieid, training_data):
  sum_rating = 0
  counter = 0
  for user in training_data:
    if (training_data.get(user)[movieid-1] > 0):
      sum_rating += training_data.get(user)[movieid-1]
      counter += 1
    else:
      continue

  if counter > 0:
    movie_avg_rating = (sum_rating/counter)
    if((movie_avg_rating > 5) or (movie_avg_rating < 1)):
      sys.exit("AVG MOVIE RATING OUT OF RANGE")
    else:
      return movie_avg_rating
  else:
    print("NO USERS HAVE RATED MOVIE #ID= ", movieid)
    return 100

def calcSim(sim_data):
  #sim_data[item][0] = active movie rating, sim_data[item][1] = trainmovie rating 
  #sim_data = list(simm_data.copy())
  #print(type(sim_data))
  #sys.exit(0)
  #iuf: m = total number of movies, mj = total # of users
  # for iuf it would be the total number of docs / of the number of
  #print(sim_data)
  top = 0.0
  bot1 = 0.0
  bot2 = 0.0
  ra = 0.0
  rt = 0.0
  for items in sim_data:
 #   print(items[0])
    ra = (items[0])
    rt = (items[1])
    top += (ra*rt)
    bot1 += (ra*ra)
    bot2 += (rt*rt)

  botf = 0.0
  botf = ((math.sqrt(bot1))*(math.sqrt(bot2)))
  if(botf == 0.0):
    print("failed to get sim") # problem is not here
    answer = -100
  else:
    answer = (top / botf)

  return answer