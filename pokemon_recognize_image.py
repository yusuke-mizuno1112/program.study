# -*- coding: utf-8 -*-
"""
Created on Thu Aug 12 18:22:58 2021
@author: mkamono
"""

from PIL import Image
import numpy as np
import math

def make_gray_data(filenumber):#一つの画像を読み込んでベクトルにする作業
    #linux
    file_path = '/mnt/chromeos/GoogleDrive/MyDrive/python/spyder/script_file/B2programing/pokemon.json-master/images/' + filenumber + '.png' #make file path
    #windows
    #file_path = 'C:/Users/trash/Google ドライブ/python/spyder/script_file/B2programing/pokemon.json-master/images/' + filenumber + '.png'
    img = Image.open(file_path)
    gray_img = img.convert('L')
    width, height = gray_img.size
    gray_img_array = np.empty((height, width), dtype='int')  #make empty array having the size of image data
    for y in range(height):
        for x in range(width):
            gray_img_array[y][x] = gray_img.getpixel((x,y))
    data = gray_img_array.reshape(-1).T  #reshape array into vector
    return data

def make_data_array():#画像のベクトルを行列にする
    for i in range(1,11): #とりあえず10個にしてるよ
        filenumber = str(i).zfill(3)   #1→001とかに変換
        if i == 1:
            data_list = [make_gray_data(filenumber)]
        else:
            data_list.append(make_gray_data(filenumber))
        print('Now loading   ' + str(filenumber) + '   image...')

    temp = tuple(data_list)
    all_data = np.stack(temp)
    return all_data

data_list = make_data_array()

def sigmoid(array):
    (hight, width) = array.shape
    answer = np.empty((hight, width))
    print(array.shape, answer.shape)
    for row in range(hight):
        for column in range(width):
            answer[row][column] = 1 #1.0/(1.0 + math.exp(array[row][column]))
            print(array[row][column])
            if array[row][column] >710:
                answer[row][column] = 1
            else:
                answer[row][column] =0
    print(answer)
    return answer

def h_theta(x, theta):
    z = np.dot(x,theta)
    print(z)

    h_theta = sigmoid(z)
    return h_theta


#def CostFunction(x,y,theta,lam):


theta = np.zeros((160000,1))
theta += 1
h_theta(data_list, theta)
#print(h_theta)