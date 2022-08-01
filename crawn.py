import requests
import json
import os
import multiprocessing
from multiprocessing import Pool
import shutil
f = open('data.json')
data = json.load(f)
def zoom(layer, URL, data):
    try:
        os.mkdir("./"+str(layer['name'])+"/"+str(data['z']))
    except FileExistsError:
        # directory already exists
        pass
    pool = multiprocessing.Pool(3)
    processes=[pool.apply_async(x_function, args=(layer, URL, data, x)) for x in range(data['xmin'],data['xmax'])]
    result = [p.get() for p in processes]

def x_function(layer, URL, data, x ):
    try:
        os.mkdir("./"+str(layer['name'])+"/"+str(data["z"])+"/"+str(x))
    except FileExistsError:
        # directory already exists
        pass
    for y in range(data['ymin'],data['ymax']):
        y_function(layer, URL, data, x, y)
        # multiprocessing.Process(target=y_function, args=(layer, URL, data, x, y)).start()

def y_function(layer, URL, data, x, y):
    URL_format = URL.format(data['z'],x,y)
    response = requests.get(URL_format)
    if len(response.content)!=0:
        open("./"+str(layer['name'])+"/"+str(data['z'])+"/"+str(x)+"/"+str(y)+".png", "wb").write(response.content)

for layer in data['layer']:
    URL = layer['URL']
    try:
        os.mkdir(str(layer['name']))
    except FileExistsError:
        # directory already exists
        pass
    for i in data['data']:
        multiprocessing.Process(target=zoom, args=(layer,URL,i)).start()