# python3 rec_sys_one.py
import math
import random
from random import randrange


predicted_ratings = []

def importTrainingData():
  trainingfile = open('train.txt', 'r')
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
  
  #print(i) # prints '8497' which is correct
  return active_users

def replace_zeros_with_rand(active_users):
  # we should create a new array here that removes all the elements that have non-zero rating
  rand_results = {}
  singleline_result = []

  for key in active_users:
    i = 0
    y = 0
    for i in range(len(active_users[key])):
      if active_users[key][i][1] == 0:
        rand_results[y] = list(active_users[key][i])
        rand_results[y][1] = randrange(5) + 1
        str = "{} {} {}".format(key, rand_results[y][0], rand_results[y][1])
        singleline_result.append(str)
        y += 1
        i += 1
      else:
        i += 1

  return singleline_result


def output_results(prediction_results):
  print(len(prediction_results))
  output_file = open("results5.1.txt", "w")
  
  i = 0
  for i in range(len(prediction_results)):
      output_file.write("{} \n".format(prediction_results[i]))
      i += 1
      
    


# execute functions below
training_data = importTrainingData()
# training data = {0: [rating(item0)...rating(total_item_count - 1)], 1:... 199:}
# more genereally, training_data = {item#: [ratings for each item],}
print("imported and formatted all training data...")

#now importing and formatting active user data
active_user_data = importActiveUserData("test5.txt")
print("imported and formatted all active user data...")
print(active_user_data)

#RAND FILLER
#-------------------------------------------------------------------------
# since i have very little time I am just going to assign a random rating to all of the active_user_data
active_user_predicted = replace_zeros_with_rand(active_user_data)
#-------------------------------------------------------------------------

# now I need to transfer the results of 'active_user_predicted' into a file
output_results(active_user_predicted)
