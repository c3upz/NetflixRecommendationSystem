#import_data.py
import sys
from separate_au_data import separateAuRatings
def importTrainingData(number, extra_data):
  trainingfile = open('data/train.txt', 'r')
  unfiltered_user_list = {} # will store whole user list here
  i = 0 # starting i at 0 means that training users will have id#s 0-199

  for singleline_content in trainingfile:
    singleline_content = [l.strip('\n') for l in singleline_content.split()]
    #print(singleline_content)
    singleline_content = list(map(int, singleline_content))
    #print(singleline_content)
    #sys.exit(0)
    unfiltered_user_list[i] = singleline_content 
    i+=1

  if(extra_data == 1):
    if(number == 5):
      filelist = [("data/test10.txt", 10),("data/test20.txt", 20)]
      for filename in filelist:
        #singleline_content needs to be in form [301, 1, 3]
        file = importActiveUserData(filename[0])
        au_r_data = separateAuRatings(file)
        for user, item in au_r_data.items():
          count = 0 
          new_user_arr = []
          y = 0
          for count in range(1000):
            if y < int(filename[1]):
              #print(item[y][0]-1)
              #print(count)
              if (item[y][0]-1) == count:
                new_user_arr.append(item[y][1])
                y += 1
              else:
                new_user_arr.append(0)
            else:
              new_user_arr.append(0) 
            #print(count)

          #arr = list(map(int, new_user_arr))
          unfiltered_user_list[i] = new_user_arr
          i += 1
      


    elif(number == 10):
      filelist = [("data/test5.txt", 5),("data/test20.txt", 20)]
      for filename in filelist:
        #singleline_content needs to be in form [301, 1, 3]
        file = importActiveUserData(filename[0])
        au_r_data = separateAuRatings(file)
        for user, item in au_r_data.items():
          count = 0 
          new_user_arr = []
          y = 0
          for count in range(1000):
            if y < filename[1]:
              if (item[y][0]-1) == count:
                new_user_arr.append(item[y][1])
                y += 1
              else:
                new_user_arr.append(0)                
            else:
              new_user_arr.append(0) 

          unfiltered_user_list[i] = new_user_arr
          i += 1
     
    elif(number == 20):
      filelist = [("data/test5.txt", 5),("data/test10.txt", 10)]
      for filename in filelist:
        #singleline_content needs to be in form [301, 1, 3]
        file = importActiveUserData(filename[0])
        au_r_data = separateAuRatings(file)
        for user, item in au_r_data.items():
          count = 0 
          new_user_arr = []
          y = 0
          for count in range(1000):
            if y < filename[1]:
              if (item[y][0]-1) == count:
                new_user_arr.append(item[y][1])
                y += 1
              else:
                new_user_arr.append(0)
            else:
              new_user_arr.append(0) 

          unfiltered_user_list[i] = new_user_arr
          i += 1
     
    else:
      sys.exit("INVALID NUMBER (in import_data.py)")
  #print(i) # this results in 200 which is correct because there are 200 users in training data
  #print(unfiltered_user_list)
  #print(i)

  #sys.exit(0)
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