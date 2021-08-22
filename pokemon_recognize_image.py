# -*- coding: utf-8 -*-
"""
Created on Thu Aug 12 18:22:58 2021
@author: mkamono
"""

import glob2
from PIL import Image
import numpy as np
import os
import math
import sys

def make_gray_data(filepath):#一つの画像を読み込んでベクトルにする作業
    #linux
    #windows
    #file_path = 'C:/Users/trash/Google ドライブ/python/spyder/script_file/B2programing/pokemon.json-master/images/' + filenumber + '.png'
    img = Image.open(filepath)
    gray_img = img.convert('L')
    width, height = gray_img.size
    gray_img_array = np.empty((height, width), dtype='int')  #make empty array having the size of image data
    for y in range(height):
        for x in range(width):
            gray_img_array[y][x] = gray_img.getpixel((x,y))
    data = gray_img_array.reshape(-1).T  #reshape array into vector
    return data

def make_data_array(num_images):#複数の画像のベクトルを行列にする
    #linux
    files = glob2.glob('/mnt/chromeos/GoogleDrive/MyDrive/python/spyder/script_file/B2programing/pokemon.json-master/images/*.png')
    #windows
    #files = glob2.glob('C:/Users/trash/Google ドライブ/python/spyder/script_file/B2programing/pokemon.json-master/images/*')
    print()
    data_list = [make_gray_data(files[0])]
    for j in range(len(data_list)):
        data_list[0][j] = 1
    for i in range(0,num_images):
        data_list.append(make_gray_data(files[i]))
        name = os.path.basename(files[i])
        sys.stdout.write("\033[2K\033[G")
        sys.stdout.flush()    #行をクリア　http://www.mm2d.net/main/prog/c/console-02.html
        print('Now processing \033[32m %s \033[0m (%d/%d)'% (name, i+1, num_images),end='',flush=True) #\033[ は色つけただけ
        #https://note.nkmk.me/python-print-basic/   %の使い方に関して
        #https://dot-blog.jp/news/python-print-overwrite-output/　endオプションに関して
        #https://qiita.com/mmsstt/items/469a9346ce545709f53c flushオプションに関して
    sys.stdout.write("\033[2K\033[G")
    sys.stdout.flush()
    print("\r\033[34mCompleted (%d/%d)\033[0m" % (num_images, num_images))
    temp = tuple(data_list)
    all_data = np.stack(temp)
    return all_data

def load_data(file_path):
    img = Image.open(file_path)
    gray_img = img.convert('L')
    width, height = gray_img.size
    gray_img_array = np.empty((height, width), dtype='int')  #make empty array having the size of image data
    for y in range(height):
        for x in range(width):
            gray_img_array[y][x] = gray_img.getpixel((x,y))
    data = gray_img_array.reshape(-1)  #reshape array into vector
    data = addBias(data) #バイアス追加
    return data

def sigmoid(array):
    (hight, width) = array.shape
    answer = np.empty((hight, width))
    for row in range(hight):
        for column in range(width):
            if array[row][column] >500: #expがバグるので大きめのところで切ってる
                answer[row][column] = 1
            elif array[row][column] < -500: #速度向上のため
                answer[row][column] = 0
            else:
                answer[row][column] =1.0/(1.0 + math.exp(array[row][column]))
    return answer

def h_theta(z):
    h_theta = sigmoid(z)
    return h_theta

def addBias(vector):
    vector = np.insert(vector, [0], 1)
    vector = vector[:, np.newaxis] #次元数が0しかないので追加 https://www.kamishima.net/mlmpyja/nbayes2/shape.html
    return vector

#def CostFunction(x,y,theta,lam):

#def Backpropagation():

#def Refresh_theta(J_theta):

def Predict(data_list, theta_1, theta_2, theta_3):
    a1 = addBias(np.dot(theta_1, data_list))
    a2 = np.dot(theta_2, a1)
    z = a2 * theta_3.T
    h_theta_x = sigmoid(z)
    return h_theta_x

def PrintResult(data_list,theta_1,theta_2,theta_3,loaded_data):
    print("\ndata_list_shape = ", data_list.shape)
    print("theta_1_shape = ", theta_1.shape)
    print("theta_2_shape = ", theta_2.shape)
    print("theta_3_shape = ", theta_3.shape)
    print("loaded_data_shape = ", loaded_data.shape)
    print()
    print("predict_result =")
    print(Predict(loaded_data, theta_1, theta_2, theta_3))

def make_theta(num_pokemon):
    theta_list = []
    theta_list.append(np.zeros((25, 160001)))
    theta_list.append(np.zeros((num_pokemon, 26))) #想定しているのはinput,output含め四層構造
    theta_list.append(np.zeros((1, num_pokemon)))
    return theta_list

num_pokemon = 3 #判別するポケモンの種類の数、アウトプット
data_list = make_data_array(10) #読み込む画像の枚数 マックス890枚くらい
loaded_data = load_data('/mnt/chromeos/GoogleDrive/MyDrive/python/spyder/script_file/B2programing/pokemon.json-master/images/001.png')
#とりあえず最初の写真読み込んでるだけ　本来はデータセットにない未知のデータ

theta_list = make_theta(num_pokemon)

PrintResult(data_list,theta_list[0],theta_list[1],theta_list[2],loaded_data)

print("\nlog(hx) = \n",np.log(Predict(loaded_data,theta_list[0],theta_list[1],theta_list[2])))