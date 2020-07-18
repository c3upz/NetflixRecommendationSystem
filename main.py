from import_data import *
from predict_ratings import predictRatingsForActiveUsers, predictRatingsPearCoor
from separate_au_data import *
from write_results import writeRatingsToFile, writePearsonRatingsToFile, writeRatingsToFile2
from user_similarity_calcs import calcBasicCFSimilarity, calcPearsonCoorSimilarity
from item_based import predict
from os import system
import sys


number = 20
#print(number)
#main.py
outfilename = "Results" + str(number) + "COMBOFINAL.txt"
infilename = "data/test" + str(number) + ".txt"
#print(infilename, outfilename)


def controller(infilename, outfilename):
  system('clear')
  user_filtering = 0 
  iuf = 0
  case_amplification = 0
  print("Please pick one of the following:")
  print("1) use basic user-based CF")
  print("2) use pearsons correlation")
  print("3) use item-based CF")
  print("4) Combo (custom)")
  user_filtering = int(input())
  if user_filtering < 4:
    if user_filtering <= 2:
      system('clear')
      print("Would you like to add IUF")
      print("1) yes")
      print("2) no")
      iuf = int(input())
    system('clear')
    print("Would you like to add case amplification")
    print("1) yes")
    print("2) no")
    case_amplification = int(input())
    system('clear')
    print("Would you like add extra training data?")
    print("1) yes")
    print("2) no")
    extra_data = int(input())
    if user_filtering == 1:
      system('clear')
      print("Would you like add discounted similarity?")
      print("1) yes")
      print("2) no")
      discounted_sim = int(input())

  if user_filtering == 1:
    BasicUserCF(iuf, case_amplification, infilename, outfilename, number, extra_data, discounted_sim,0)
  elif user_filtering == 2:
    PearsonsCorrelation(iuf, case_amplification, infilename, outfilename, number, extra_data, 0)
  elif user_filtering == 3:
    #print("insert custom algorithm here")
    ItemBasedCS(case_amplification, infilename, outfilename, extra_data, 0)
  elif user_filtering == 4:
    Combo(1, 1, infilename, outfilename, number, 1)
  else:
    print("not a valid option")

def BasicUserCF(iuf, case_amplification, infilename, outfilename, number, extra_data, discounted_sim,combo):
  # MAE1 = 0.99975373501888 
  # MAE2 = 0.815013955015597 , fixed -100 issue, issue occured bc for loop went out of bounds in filter_tu_ratings
  # I think MAE2 points to the fact that I am implementing basic user CF... 
  print("iuf = ", iuf, " ", "case_amplification = ", case_amplification) # iuf&case_amp = yes(1),no(2)
  #user_filtering = 0, execute functions below
  training_data = importTrainingData(number, extra_data)
  #print(training_data)
  # training data = {0: [rating(item0)...rating(total_item_count - 1)], 1:... 199:}
  # more genereally, training_data = {item#: [ratings for each item],}
  #print(training_data.get(0)[0]) # prints 5 which is the 0th elements rating of the 0th movie
  print("imported and formatted all training data...")

  #now importing and formatting active user data
  active_user_data = importActiveUserData(infilename)
  #print(active_user_data.keys()) # prints 201 - 300, this is correct for test5.txt
  print("imported and formatted all active user data...")
  #print(active_user_data)
  #sys.exit(0)

  active_user_rated_dict = separateAuRatings(active_user_data)
  #print(active_user_rated_dict)
  #sys.exit(0)

  active_users_unknown_ratings = separateAuUnknownRatings(active_user_data)
  # after this point the tests data should be separated into two dictionaries
  #   1. active_user_rated_list will contain all the elements with known ratings for users in the test files.
  #   2. active_user_unknown_ratings will contain all the elements with unknown ratings
  #print(active_users_unknown_ratings)
  #sys.exit(0)

  neighbors_for_each_activeuser = calcBasicCFSimilarity(active_user_rated_dict, training_data, iuf, discounted_sim,number) #using cosine similarity here to find neighbors
  #print(neighbors_for_each_activeuser)
  #sys.exit(0)
  #print("rating is: ",training_data.get(47)[205])

  predicted_ratings = predictRatingsForActiveUsers(neighbors_for_each_activeuser, active_users_unknown_ratings, training_data, active_user_rated_dict,case_amplification, number)
  #print(predicted_ratings)
  #sys.exit("main yeye")
  if combo == 1:
    return predicted_ratings
  else:
    writeRatingsToFile(predicted_ratings, outfilename)


def PearsonsCorrelation(iuf, case_amplification, infilename, outfilename, number, extra_data, combo):
  print("iuf = ", iuf, " ", "case_amplification = ", case_amplification) # iuf&case_amp = yes(1),no(2)
  training_data = importTrainingData(number, extra_data)
  print("imported and formatted all training data...")
  active_user_data = importActiveUserData(infilename)
  print("imported and formatted all active user data...")

  # have imported all data I need..


  active_user_rated_dict = separateAuRatings(active_user_data)

  active_users_unknown_ratings = separateAuUnknownRatings(active_user_data)
  # after this point the tests data should be separated into two dictionaries
  #   1. active_user_rated_list will contain all the elements with known ratings for users in the test files.
  #   2. active_user_unknown_ratings will contain all the elements with unknown ratings
  #print(active_users_unknown_ratings)
  
  au_avg_rating_dict = {}
  for activeuser in active_user_rated_dict:
    avg_rating = 0
    avg_rating = getActiveUserAverageRating(activeuser, active_user_rated_dict)
    au_avg_rating_dict.update({activeuser: (avg_rating)})
  #print(au_avg_rating_dict)

  tu_avg_rating_dict = {}
  for traininguser in training_data:
    avg_rating = 0
    avg_rating = getTUAverageRating(traininguser, training_data)
    tu_avg_rating_dict.update({traininguser: (avg_rating)})
  #print(tu_avg_rating_dict)
  #sys.exit("AVG RATINGS")
  pear_sim, pear_abs_sim = calcPearsonCoorSimilarity(active_user_rated_dict, training_data, au_avg_rating_dict, tu_avg_rating_dict, iuf)
  #pearsons_coor = {AU#: [(TU#, sim), (TU#,sim)...]} this list should be sorted
  #print(pearsons_coor)
  #print(" ")
  #print(pearsons_coor)
  #print(pear_abs_sim)
  #print(pear_sim)
  #exit(0)
  
  #filtered_sim = filterlow_sim(pearsons_coor)
  predicted_ratings = predictRatingsPearCoor(pear_sim, active_users_unknown_ratings, training_data, active_user_rated_dict, au_avg_rating_dict, tu_avg_rating_dict, case_amplification, number)
  #print(predicted_ratings)
  #writePearsonRatingsToFile(predicted_ratings, outfilename)
  #sys.exit("PEAR")
  if combo == 1:
    return predicted_ratings
  else:
    writePearsonRatingsToFile(predicted_ratings, outfilename)

def ItemBasedCS(case_amplification, infilename, outfilename, extra_data, combo):
  if combo == 1:
    mean_centered = 2
  else:
    system('clear')
    print("Would you like to mean centered ratings?")
    print("1) yes")
    print("2) no")
    mean_centered = int(input())

  print("iuf = N/A", " ", "case_amplification = ", case_amplification, "mean centering=", mean_centered, "extra data= ", extra_data) # iuf&case_amp = yes(1),no(2)
  training_data = importTrainingData(number, extra_data)
  #print(len(training_data.get(302)))
  #sys.exit("TRDATA")
  print("imported and formatted all training data...")
  active_user_data = importActiveUserData(infilename)
  print("imported and formatted all active user data...")

  active_items_known_ratings = separateAuRatings(active_user_data)
  #print(active_items_known_ratings)
  #sys.exit(0)

  active_items_unknown_ratings = separateAuUnknownRatings(active_user_data)

  predicted_ratings = predict(training_data, active_items_known_ratings, active_items_unknown_ratings, case_amplification, mean_centered)
  #print(predicted_ratings.get(201))
  #sys.exit("ITEMB")
  if combo == 1:
    return predicted_ratings
  else:
    writeRatingsToFile(predicted_ratings, outfilename)

def Combo(iuf, case_amplification, infilename, outfilename, number, extra_data):
  bcf = BasicUserCF(iuf, case_amplification, infilename, outfilename, number, extra_data, 1,1) # 1(discounted_sim), 1(combo)
  #sys.exit("COUNTER test") # 5 = ~3, 10 = ~5, 20 = ~7
  ib = ItemBasedCS(case_amplification, infilename, outfilename, extra_data, 1)
  pc = PearsonsCorrelation(iuf, case_amplification, infilename, outfilename, number, extra_data, 1)
  writeRatingsToFile2(bcf, ib, pc,outfilename, number,3) # 2 = bcf + ib, 3 = bcf + ib + pc


#----------------------------------------------------------------------------------------


def getActiveUserAverageRating(activeuser_number, active_user_ratings):
  #print(active_user_ratings)
  rating_sum = 0 
  count = 0
  for i in range(len(active_user_ratings.get(activeuser_number))):
    #print(active_user_ratings.get(activeuser_number)[i][1]);
    rating_sum += active_user_ratings.get(activeuser_number)[i][1]
    count += 1

    

  avg = rating_sum / count
  return avg


def getTUAverageRating(specific_user, training_users):
  rating_sum = 0
  temp = training_users.get(specific_user)
  count = 0
  for i in range(len(temp)):
    if(temp[i] > 0):
      rating_sum += temp[i]
      count += 1 
    else:
      continue
  avg = rating_sum / count
  return avg

#filtering out 'not that similar users' from the list of possible similar users
def filterlow_sim(data):
  new_sim_list = {}
  for key,value in data.items():
    temp = []
    for i in range(len(value)):
      #print(key,value[i][1])
      if value[i][1] > .7:
        temp.append((value[i][0], value[i][1]))
    new_sim_list.update({key: (temp)})

  #print(new_sim_list)
  return 0

controller(infilename, outfilename)