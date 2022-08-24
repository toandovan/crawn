import requests
import json
import os
import multiprocessing
from multiprocessing import Pool, freeze_support
import shutil
f = open('data.json')
data = json.load(f)
def zoom(layer, URL, data):
    try:
        os.mkdir("./"+str(layer['name'])+"/"+str(data['z']))
    except FileExistsError:
        pass
    pool = multiprocessing.Pool(8)
    processes=[pool.apply_async(x_function, args=(layer, URL, data, x)) for x in range(data['xmin'],data['xmax'])]
    result = [p.get() for p in processes]

def x_function(layer, URL, data, x ):
    try:
        os.mkdir("./"+str(layer['name'])+"/"+str(data["z"])+"/"+str(x))
    except FileExistsError:
        pass
    for y in range(data['ymin'],data['ymax']):
        y_function(layer, URL, data, x, y)

def y_function(layer, URL, data, x, y):
    URL_format = URL.format(data['z'],x,y)
    response = requests.get(URL_format)
    if len(response.content)!=0:
        open("./"+str(layer['name'])+"/"+str(data['z'])+"/"+str(x)+"/"+str(y)+".png", "wb").write(response.content)
if __name__ == '__main__':
    freeze_support()
    for layer in data['layer']:
        URL = layer['URL']
        try:
            os.mkdir(str(layer['name']))
        except FileExistsError:
            pass
        for i in data['data']:
            multiprocessing.Process(target=zoom, args=(layer,URL,i)).start()