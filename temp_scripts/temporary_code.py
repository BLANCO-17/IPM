# import requests

# hodl = [300, 540, 900, 1030, 750, 520, 570, 650, 850, 890, 900, 750]
# invst = [10, 50, 20, 15, 100, 10, 30, 5, 5, 7, 5, 5]
# gain = [100, 400, 600, 670, 400, 300, 320, 350, 475, 490, 600, 630]

# # for x in range(0, 12):
# #     requests.get("http://127.0.0.1:5000/toapp/setMonthData?item=btc&cur=usd&month="+str(x+1)+"&hodl="+str(hodl[x])+"&investment="+str(invst[x])+"&netgain="+str(gain[x]))

# print("done")

# import os, shutil
# path = r"D:\\Development Environment\\IPM\\backend\\icons\\"#r"C:\\Users\\saini\\Desktop\\3D-Cryptocurrency-Icons\\3D Crypto Icons ( PNGS+Source)\\"

# files = []

# print(os.listdir(path))

# for x in os.listdir(path):
#-> rename files
#     os.rename(path+x, path+x.lower())
#     print("renamed", x, " -> ", x.lower())

#-> to get files
#     if "_F" in x:
#         files.append(x)
#         shutil.copy(path+x, 'D:\\Development Environment\\IPM\\backend\\icons\\')
#         print(x, "copied to icon dir.")
        
# print(files)
import requests
import json
from datetime import date

class Fear_Greed:
    '''class to Read from bitcoin fear and greed index'''
    def __init__(self, name, time, value, classification):
        
        
        self.name = name
        self.time = time
        self.value = value
        self.classification = classification
        
    def print_info():
        '''Method to print the data from  Fear and greed index for bitcoin'''
        uri = 'https://api.alternative.me/fng/?limit=2'
        today = date.today()
        d1 = today.strftime("%m/%d/%Y")

        r = requests.get(uri) 
        data = r.json()
        #def find_actors(self, movies):
        with open('output.json', 'w') as file:
            file.write(f"{data}")
        name = data['name']
        time = data['data'][0]['timestamp']
        value = data['data'][0]['value']
        classification = data['data'][0]['value_classification']
        endline = "\n-----------------------------\n"
        print(f"{name}\n\n\tFear level: {value}\n\tRating: {classification}\n\tTimestamp: {time}\n\tDate: {d1}\n{endline}")
print(Fear_Greed.print_info())