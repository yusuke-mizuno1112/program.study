# -*- coding: utf-8 -*-
"""
Created on Thu Aug 12 18:22:58 2021
@author: mkamono
"""

import numpy as np
import os
import math
import scipy.io
import time
from matplotlib import pyplot as plt
np.set_printoptions(suppress=True)
"""
import glob2
from PIL import Image
import sys


def make_gray_data(filepath):#一つの画像を読み込んでベクトルにする作業
    img = Image.open(filepath)
    gray_img = img.convert('L')
    width, height = gray_img.size
    gray_img_array = np.empty((height, width), dtype='int')  #make empty array having the size of image data
    for y in range(height):
        for x in range(width):
            gray_img_array[y][x] = gray_img.getpixel((x,y))
    data = gray_img_array.reshape(-1).T  #reshape array into vector
    return data

def make_data_array(num_images, files):#複数の画像のベクトルを行列にする
    #linux
    #windows
    #files = glob2.glob('C:/Users/trash/Google ドライブ/python/spyder/script_file/B2programing/pokemon.json-master/images/*')
    print()
    data_list = [make_gray_data(files[0])]
    for j in range(len(data_list)):
        data_list[0][j] = 1
    for i in range(0,num_images):
        data_list.append(make_gray_data(files[i]))#以下はだいたいコンソールの表示に関することなので流し読みで結構
        name = os.path.basename(files[i]) #ファイル名を取得　https://note.nkmk.me/python-os-basename-dirname-split-splitext/
        sys.stdout.write("\033[2K\033[G")
        sys.stdout.flush()    #行をクリア　http://www.mm2d.net/main/prog/c/console-02.html
        print('Now processing \033[32m %s \033[0m (%d/%d)'% (name, i+1, num_images),end='',flush=True) #\033[ は色つけただけ
        #https://note.nkmk.me/python-print-basic/   %の使い方に関して
        #https://dot-blog.jp/news/python-print-overwrite-output/　endオプションに関して
        #https://qiita.com/mmsstt/items/469a9346ce545709f53c flushオプションに関して
    sys.stdout.write("\033[2K\033[G")
    sys.stdout.flush()
    print("\r\033[34mProcess Completed (%d/%d)\033[0m" % (num_images, num_images))
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
    return data
"""

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
                answer[row][column] =1.0/(1.0 + math.exp((-1) * array[row][column]))
    return answer

def addBias(vector):
    vector = np.insert(vector, [0], 1)
    vector = vector[:, np.newaxis] #次元数が0しかないので追加 https://www.kamishima.net/mlmpyja/nbayes2/shape.html
    return vector
 
def calculate_D(theta,DELTA,lam,m):
    D = np.zeros((theta.shape))
    for i in range(theta.shape[0]):
        if i == 0:
            D[0] = (1/m) * DELTA[0]
        else:
            D[i] = (1/m) * (DELTA[i] + (lam * theta[i]))
    return D

def CostFunction(x,y,theta,lam):
    num_data_list = x.shape[0]
    Cost = 0 
    for m in range(num_data_list):
        y_m = (y[m])[:,np.newaxis]
        log1 = np.log(Predict(x[m],theta)[1])
        log2 = np.log(1-(Predict(x[m],theta)[1]))
        Cost += np.sum((-1)*y_m*log1)+np.sum((-1)*(1-y_m)*log2)
    Cost += (1/2)*lam*(np.sum(theta[0][:, : 400]**2) + np.sum(theta[1][:, : 25]**2))
    return Cost/num_data_list

def Backpropagation(x,y,theta,lam):
    plt_J = []
    plt_acc = []
    iter_num = []
    
    num_data_list = x.shape[0]
    m = num_data_list
    iter = 1
    while True:
        try:
            DELTA_1 = []
            DELTA_2 = [] #初期化
            for M in range(num_data_list):
                x_m = x[M]
                y_m = y[M][:, np.newaxis]
                a1 = addBias(x_m)
                (a2, a3) = Predict(x_m,theta)

                delta_2 = []
                delta_3 = []
                
                delta_3 = a3 - y_m
                delta_2 = (np.dot(theta[1].T, delta_3))*((a2)*(1-a2))
                delta_2 = np.delete(delta_2,0,0) #delta[0]を除去
                if M == 0:
                    DELTA_2 = np.dot(delta_3,a2.T)
                    DELTA_1 = np.dot(delta_2,a1.T)
                else:
                    DELTA_2 += np.dot(delta_3,a2.T)
                    DELTA_1 += np.dot(delta_2,a1.T)
            D_1 = calculate_D(theta[0],DELTA_1,lam,m)
            D_2 = calculate_D(theta[1],DELTA_2,lam,m)
            Refresh_theta(theta, D_1, D_2)
            
            J = CostFunction(x, y, theta, lam)
            acc = accuracy(X, y, theta_list)
            
            plt_J.append(J)
            plt_acc.append(acc)
            iter_num.append(iter)
            
            plt.plot(iter_num, plt_acc)
            plt.show()
            
            print(f"{iter} th Cost = ", J)
            if iter % 10 == 0:
                print("accuracy = ", acc, "%")
                end = time.time()
                print("経過時間 = ", round((end-start), 2), "秒")
            iter += 1
        except KeyboardInterrupt:
            break
    return(CostFunction(x, y, theta, lam))

def Refresh_theta(theta,D1,D2):
    theta[0] = theta[0] - D1
    theta[1] = theta[1] - D2
    return

def Predict(data_list, theta):
    data_list = addBias(data_list) #バイアス追加
    a2 = sigmoid(addBias(np.dot(theta[0], data_list)))
    a3 = sigmoid(np.dot(theta[1], a2))
    return a2, a3

def make_theta(outputs):
    theta_list = []
    a = np.random.rand(25, 401) - 0.5
    theta_list.append(a*0.24)
    b = np.random.rand(outputs, 26) - 0.5
    theta_list.append(b*0.24)
    return theta_list

def make_y_array(y_label, y):
    for i in range(y_label.shape[0]):
        j = int(y_label[i])
        y[i][j] = 1

def accuracy(x, y, theta):
    correct_number = 0
    num_data_list = x.shape[0]
    m = num_data_list
    for i in range(m):
        pred = Predict(x[i], theta)[1]
        answer = y[i]
        if np.argmax(pred) == np.argmax(answer):
            correct_number += 1
    oomakanumber = round((correct_number/m)*100, 4)
    return oomakanumber

outputs = 10 #アウトプット

if "theta_list" in globals():
    theta_list = theta_list
else:
    theta_list = make_theta(outputs) #theta 初期化


#以下matファイルを使った作業
#参考　https://www.delftstack.com/ja/howto/python/read-mat-files-python/#python-%25E3%2581%25A7-numpy-%25E3%2583%25A2%25E3%2582%25B8%25E3%2583%25A5%25E3%2583%25BC%25E3%2583%25AB%25E3%2582%2592%25E4%25BD%25BF%25E7%2594%25A8%25E3%2581%2597%25E3%2581%25A6mat-%25E3%2583%2595%25E3%2582%25A1%25E3%2582%25A4%25E3%2583%25AB%25E3%2582%2592%25E8%25AA%25AD%25E3%2581%25BF%25E5%258F%2596%25E3%2582%258A%25E3%2581%25BE%25E3%2581%2599

dir_path = os.path.dirname(__file__)
mat_path = os.path.join(dir_path, "ex4data1.mat")
print(mat_path)

X = scipy.io.loadmat(mat_path)["X"]
y_label = scipy.io.loadmat(mat_path)["y"]

y = np.zeros((y_label.shape[0], outputs))
y_label[np.where(y_label == 10)] = 0
make_y_array(y_label, y)

lam = 0.1
J = CostFunction(X, y, theta_list, lam)

print("X-shape = ", X.shape)
print("y-shape = ", y_label.shape)
for i in range(2):
    print("theta_%s-shape = " % i, theta_list[i].shape)

print("Initial Cost = ", J)
print("initial accuracy = ", accuracy(X, y, theta_list), "%")

print("\nctrl + C を押した段階で学習を終了するよ!\n")

start = time.time()

Backpropagation(X, y, theta_list, lam)


print("\nlast accuracy = ", accuracy(X, y, theta_list), "%")
