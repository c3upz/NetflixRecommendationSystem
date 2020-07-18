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