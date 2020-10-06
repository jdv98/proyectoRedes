import json
import datetime
import random
import time
#d= datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")

if __name__ == '__main__':
    while(True):
        time.sleep(random.randint(1, 10))
        d= datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        data={}
        data['last_time']=d
        with open('last9.json', 'w+') as json_file:
            json.dump(data, json_file)
