import glob2
from PIL import Image
import numpy as np
import os

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
        print('\rNow processing %s (%d/%d)'% (name, i+1, num_images) ,end='')
        #https://note.nkmk.me/python-print-basic/   %の使い方に関して
        #https://dot-blog.jp/news/python-print-overwrite-output/　\r,endオプションに関して
    print("\rCompleted (%d/%d)                                        " % (num_images, num_images))