#output_results.py
import sys
# ROUNDING HAPPENS IN THIS FILE
def writeRatingsToFile(ratings, output_filename):
  output_file = open(output_filename, "w")

  for key, item in ratings.items():
    i=0
    for i in range(len(item)):
      # print(key, round(item[i][0]), round(item[i][1]))
      output_file.write("%i %i %i\n" % (key, round(item[i][0]), round(item[i][1])))

def writeRatingsToFile2(bcf, ib, pc, output_filename, number,combo_type):
  output_file = open(output_filename, "w")

  for user in bcf:
    i=0
    user_num = user
    for i in range(len(bcf.get(user))):
      # print(key, round(item[i][0]), round(item[i][1]))
      doc_num = bcf.get(user)[i][0]
      if number == 5:
        rating1 = ((bcf.get(user)[i][1])*2.3) #here numbers are weighting #2, 1.5
        rating2 = ((ib.get(user)[i][1])*1.7) #1.5,1.2
        rating3 = ((pc.get(user)[i][1])*1)   #1
        #denom = (2 + 1.5 + 1) #v4
        denom = (2.3 + 1.7 + 1) #v5 better version for test5 only
        #denom = (2.5 + 1.8 + 1) #v6
      elif number == 10:
        rating1 = ((bcf.get(user)[i][1])*1.8) #here numbers are weighting #2.4(badv5) ,1.8(best), 1.5
        rating2 = ((ib.get(user)[i][1])*1.3) #1.75(badv5),1.3(best),1.2
        rating3 = ((pc.get(user)[i][1])*1)   #1
        denom = (1.8 + 1.3 + 1) #v4
        #denom = (2.4 + 1.75 + 1) #v5
        #denom = (1.95 + 1.5 + 1) #v6


      elif number == 20:
        rating1 = ((bcf.get(user)[i][1])*2) # 2.3(badv5), 2(v4), 1.5..here numbers are weighting #1.5
        rating2 = ((ib.get(user)[i][1])*1) #1,1.2
        rating3 = ((pc.get(user)[i][1])*1.3)   #,1.4(badv5),1.3(v4),1
        denom = (2 + 1 + 1.3) #v4
        #denom = (2.3 + 1 + 1.4) #v5
        #denom = (1.8 + 1 + 1.3) #v6
      else:
        sys.exit("WRONG NUMBER WRITE RESULTS")


      if(combo_type == 2):
        avg_r = (rating1 + rating2) / 2.7
      elif(combo_type == 3):
        avg_r = (rating1 + rating2 + rating3) / denom #3.7
      if(avg_r > 5):
        avg_r = 5
      if(avg_r < 1):
        avg_r = 1

      output_file.write("%i %i %i\n" % (user_num, doc_num, round(avg_r)))

def writePearsonRatingsToFile(ratings, output_filename):
  output_file = open(output_filename, "w")

  for key, item in ratings.items():
    i=0
    for i in range(len(item)):
      # print(key, round(item[i][0]), round(item[i][1]))
      doc_number = round(item[i][0])
      rating = round(item[i][1])
      if rating > 5:
        rating = 5
      elif rating < 1:
        rating = 1

      output_file.write("%i %i %i\n" % (key, doc_number, rating))