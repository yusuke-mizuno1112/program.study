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

def make_data_array(images):#画像のベクトルを行列にする
    for i in range(0,images+1): #とりあえず10個にしてるよ
        filenumber = str(i).zfill(3)   #1→001とかに変換
        if i == 0: #バイアスユニットの生成
            data_list = [make_gray_data("001")]
            for j in range(len(data_list)):
                data_list[0][j] = 1
        else:
            data_list.append(make_gray_data(filenumber))
            print('Now loading   ' + str(filenumber) + '   image...')

    temp = tuple(data_list)
    all_data = np.stack(temp)
    return all_data

def sigmoid(array):
    (hight, width) = array.shape
    answer = np.empty((hight, width))
    for row in range(hight):
        for column in range(width):
            if array[row][column] >500: #expがバグるので大きめのところで切ってる
                answer[row][column] = 1
            elif array[row][column] < -500:
                answer[row][column] = 0
            else:
                answer[row][column] =1.0/(1.0 + math.exp(array[row][column]))
    return answer

def h_theta(x, theta):
    z = np.dot(x,theta)
    h_theta = sigmoid(z)
    return h_theta

#def CostFunction(x,y,theta,lam):

#def Backpropagation():

#def Refresh_theta(J_theta):

#def Predict():

data_list = make_data_array(3) #読み込む画像の枚数 マックス890枚くらい
theta_1 = np.zeros((160000,1))
theta_1 += 1   #これはなんとなく
print("\ndate_list_shape = ", data_list.shape)
print("theta_1_shape = ", theta_1.shape)
print("h_theta_1 = \n", h_theta(data_list, theta_1)) # \nは正規表現で言う改行だよ