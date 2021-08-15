# じゃんけん
import sys     #プログラムを終了する関数exit()
#https://docs.python.org/ja/3/library/sys.html#sys.exit
import random  #乱数
#https://docs.python.org/ja/3/library/random.html

# あなたの手
print("0:グー")
print("1:チョキ")
print("2:パー")
x = int(input("あなたの手> "))

if not(x==0 or x==1 or x==2): #0,1,2以外は入力エラーで終了
    print("入力エラー")
    sys.exit()

# コンピュータの手：
random.seed() #システム時刻で乱数の種seedを初期化
y = random.choice([0, 1, 2]) #0,1,2からランダム選択
print("コンピュータの手>", y)

#その１：
#入力の組み合わせ(0,1,2)x(0,1,2)=9通りの場合分け
#ifの入れ子で、条件を一つずつ
if x==0:
    if y==0:
        print("あいこ")
    elif y==1:
        print("勝ち")
    else: #y==2
        print("負け")
elif x==1:
    if y==0:
        print("負け")
    elif y==1:
        print("あいこ")
    else: #y==2
        print("勝ち")
else: #x==2
    if y==0:
        print("勝ち")
    elif y==1:
        print("負け")
    else: #y==2
        print("あいこ")

#その２：
#判定3つの場合分け（あいこ、勝ち、負け）
#ifの入れ子を使用しない場合
if x==y:
    print("あいこ")
elif (   (x==0 and y==1) #グー　　対 チョキ
      or (x==1 and y==2) #チョキ　対 パー
      or (x==2 and y==0) #パー 　対 グー
      ):
    print("勝ち")
else:
    print("負け")


#add comment