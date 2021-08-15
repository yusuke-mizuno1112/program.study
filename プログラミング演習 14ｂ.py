import tkinter as tk
import random
import time  # タイマー

####################
# グローバル変数
#status = "" #ブロック状態：移動中"avtive"、固定"fix"、次"next"、ゲーム停止"stop"

#        "shape"種類  "fill"色  "outline"枠の色 
block = {"W":{"fill":"gray30", "outline":"black"},  #"W"壁・天井・床
         "B":{"fill":"white",  "outline":"gray80"}, #"B"背景(ブロック移動可能範囲)
         "A":{"fill":"gray60", "outline":"gray40"}, #"A"お邪魔
         "Z":{"fill":"red3",   "outline":"red1"},   #"Z"ブロック（赤）
         "T":{"fill":"magenta3", "outline":"magenta1"},
         "I":{"fill":"cyan3",    "outline":"cyan1"},
         "O":{"fill":"yellow3",  "outline":"yellow1"},
         "S":{"fill":"green3",   "outline":"green1"},
         "J":{"fill":"blue3",    "outline":"blue1"},
         "L":{"fill":"orange3",  "outline":"orange1"},
         }

# "shape"種類:基準ブロック0,0と相対座標リスト
mino = {"Z":[{"dx":0, "dy":0}, {"dx":-1, "dy":-1}, {"dx":0, "dy":-1}, {"dx":1, "dy":0}],
        "T":[{"dx":0, "dy":0}, {"dx":-1, "dy":0 }, {"dx":+1,"dy":0 }, {"dx":0, "dy":+1}],
        "I":[{"dx":0, "dy":0}, {"dx":0, "dy":-1}, {"dx":0, "dy":+1}, {"dx":0, "dy":+2}],
        "O":[{"dx":0, "dy":0}, {"dx":+1, "dy":0}, {"dx":+1, "dy":+1}, {"dx":0, "dy":+1}],
        "S":[{"dx":0, "dy":0}, {"dx":-1, "dy":0}, {"dx":0, "dy":-1}, {"dx":+1, "dy":-1}],
        "J":[{"dx":0, "dy":0}, {"dx":+1, "dy":-1}, {"dx":0, "dy":+1}, {"dx":0, "dy":-1}],
        "L":[{"dx":0, "dy":0}, {"dx":+1, "dy":+1}, {"dx":0, "dy":-1}, {"dx":0, "dy":+1}],
        
        
              # 提出問題14a
        }

key_move = {"Right":{"mx":1, "my":0},  # キーに対する移動量
            "Left":{"mx":-1, "my":0},
            "Down":{"mx":0, "my":1}}

new_x = 5
new_y = 5

####################
# 関数定義
def display_active_info():   # グローバル変数active_listの表示
    s_list = []
    for active in active_list:
        s_list.append(str(active))
    s = "\n".join(s_list)    # リストを改行で連結
    label.configure(text=s)

def create_block(x, y, shape, reverse=False):  # ブロックの生成
    s = BLOCK_SIZE
    margin = 2  # 2画素小さめ
    x1 = x*s + margin
    y1 = y*s + margin
    x2 = (x+1)*s - margin
    y2 = (y+1)*s - margin
    fill_color = block[shape]["fill"]
    outline_color = block[shape]["outline"]
    if reverse:  # 固定ブロック：fillとoutlineの色を入れ替え
        fill_color, outline_color = outline_color, fill_color
    block_id = canvas.create_rectangle(x1, y1, x2, y2,
                                       fill=fill_color,
                                       outline=outline_color,
                                       width=3) #枠3画素
    return block_id  # 返り値：図形のid

def is_completed_line(): # 固定ブロックが揃ったか（背景"B"以外か）
    global completed_y_list
    completed_y_list = []
    for y in y_list:
        completed = True
        for x in range(1, FIELD_WIDTH-1):
            if field[y][x] == "B":
                completed = False
                break
        if completed:
            completed_y_list.append(y)
    if len(completed_y_list) == 0:
        return False
    return True

def delete_line(): # 段消し
    #completed_y_list
    for y in completed_y_list:
        for x in range(1, FIELD_WIDTH-1): #　壁以外のブロックを白枠に変更（アニメーション効果）
            canvas.itemconfig(fix_id[y][x], outline="white")
    window.update()  # 画面更新
    time.sleep(0.5)

    for y in completed_y_list:
        for x in range(1, FIELD_WIDTH-1): # 段消し：壁以外のブロック削除
            canvas.delete(fix_id[y][x])   # 図形を削除
            fix_id[y][x] = None
            field[y][x] = "B"  # 背景に変更
    window.update()
    print("delete")

def down_line():  # 段差げ：下から上に順に、1段ずつ下げる
    s = BLOCK_SIZE
    y = completed_y_list[0]
    down_n = 1
    for yy in range(y-1, 0, -1):      #down_n段ずつ下げる
        if yy in completed_y_list:
            down_n += 1
            continue
        for xx in range(1, FIELD_WIDTH-1):
            if field[yy][xx] != "B":
                field[yy + down_n][xx] = field[yy][xx]
                field[yy][xx] = "B"
                fix_id[yy + down_n][xx] = fix_id[yy][xx]
                fix_id[yy][xx] = None
                canvas.move(fix_id[yy + down_n][xx], 0, s*down_n)
    window.update()
    print("down")

def fix_block():  # 移動ブロックactiveを固定ブロックとして保存
    global y_list # 固定したyリスト
    y_list = []
    for active in active_list:
        x = active["x"]
        y = active["y"]
        fix_id[y][x] = active["id"]    # fix_id: 固定ブロックのid
        field[y][x] = active["shape"]  # field:  固定ブロックのshape
        canvas.itemconfig(active["id"], outline="black") #固定ブロックを黒枠に変更
        if y not in y_list:
            y_list.append(y)
    y_list.sort(reverse=True)    #大きい順に並べ替え
    window.update()  # 画面更新
    print("fix")

next_mino_list = []
def next_mino(): # 次のミノの種類を返す：7回に1回は、必ず選ばれるように
    global next_mino_list
    if next_mino_list == []:
        next_mino_list = list(mino)    # ["Z", "T", "I", "O", "S", "J", "L"]
        random.shuffle(next_mino_list) # リストのランダムシャッフル
    return next_mino_list.pop(0)       # リストの先頭要素を取り出す（リストから削除）

def can_new_block():    # 新しいブロックを作れるか
    for active in active_list:
        x = active["x"]
        y = active["y"]
        if field[y][x] != "B":  # 背景以外なら作成できないFalse
            return False
    return True

def create_new_block(x=new_x, y=new_y):  # 新しいブロックの作成
    global status, active_list
    shape = next_mino()
    active_list = []
    for dxdy in mino[shape]:  # 基準ブロックx,yに対する相対座標
        active = {"x":None, "y":None, "id":None, "shape":None}
        active["x"] = x + dxdy["dx"]
        active["y"] = y + dxdy["dy"]
        active["shape"] = shape
        active_list.append(active)
    if can_new_block():  # 新しいブロックを作れるか
        is_center = True  # 基準ブロック（回転中心）の色を反転
        for active in active_list:
            x = active["x"]
            y = active["y"]        
            active["id"] = create_block(x, y, shape, reverse=is_center)
            is_center = False
        status = "active"
        print("active")
        display_active_info()
    else:
        status = "stop"
        print("game_over")

def can_move(mx, my):  # active_listのブロックがmx, my移動可能か
    for active in active_list:  #Z-minoの場合は4個
        x = active["x"] + mx
        y = active["y"] + my
        if field[y][x] != "B":  # 背景"B"以外なら移動不可
            return False        # 1つでも移動不可ならFalse、for中断
    return True  # 4つとも移動可能ならTrue

def actual_move(mx, my):
    s = BLOCK_SIZE
    for active in active_list:
        active["x"] += mx
        active["y"] += my
        canvas.move(active["id"], mx*s, my*s)  #図形idを実際に移動

def move_block(event):  # キーを押したときの関数定義
    global status
    #ブロック状態：移動中avtive、固定fix、次"next"、ゲーム停止stop
    if status == "stop" or status == "fix":
        return
    if status == "next":
        create_new_block()
        return
    key = event.keysym  # 押したキー：event.keysym
    mx = key_move[key]["mx"]  # キーに対する移動量
    my = key_move[key]["my"]
    if can_move(mx, my):  # 移動可能なら
        actual_move(mx, my)  # 実際に移動
    elif key == "Down":   # 下に移動できない（移動不可かつ下矢印）
        status = "fix"
        fix_block()       # ブロック固定
        time.sleep(0.5)   # 0.5秒待ち
        if is_completed_line(): # 固定ブロックが揃ったら
            delete_line() # 段消し
            time.sleep(0.5)
            down_line()   # 段差げ
            time.sleep(0.5)
        status = "next"
    display_active_info()

def can_rotate_block():
    
    return False  # 回転不可

def rotate_block(event):
    s = BLOCK_SIZE
    if status != "active":
        return
    
    center = active_list[0]
    cx = center["x"]
    cy = center["y"]
    for active in active_list[0:]:
        x = active["x"]
        y = active["y"]
        active["x"] = -(y-cy)+cx
        active["y"] = (x-cx)+cx
        mx = active["x"] - x
        my = active["y"] - y
        canvas.move(active["id"], mx*s, my*s)
            
            
            
            
        
    window.update()

def create_field():
    global field
    w = FIELD_WIDTH   #10+2
    h = FIELD_HEIGHT  #20+2
    
    field = [None]*h  #行数分の空リスト
    
    #field[0] = ["W","W","W","W","W","W","W","W","W","W","W","W"]
    for y in range(0, h-1):                     # 天井なし
        field[y] = ["W"] + ["B"]*(w-2) + ["W"]  # 壁"W", 背景"B"*10個, 壁"W"
    field[FIELD_HEIGHT-1] = ["W"]*w             # 床"W"*12個
    
    for y in range(0, h):                       # w*hのブロック（壁、背景）の図形を描く
        for x in range(0, w):
            if y == new_y and x == new_x:
                create_block(x, y, field[y][x], reverse=True)
            else:
                create_block(x, y, field[y][x])   #返り値（図形id）は使わないので、未代入

def create_ojama(n=3, ojama_w=9): # お邪魔ブロックの段数n=3、1段あたりの個数9
    w = FIELD_WIDTH-2           # 壁以外のフィールド幅
    y_max = FIELD_HEIGHT-2      # フィールドの最下段（床上）
    
    for y in range(y_max, y_max-n, -1):   # 床上からn段
        ojama_line = ["A"] * ojama_w + ["B"]  * (w - ojama_w)  # お邪魔"A"、背景"B"
        random.shuffle(ojama_line)        # "B"の位置をランダムシャッフル
        field[y] = ["W"] + ojama_line + ["W"]  # y段目：左壁"W"+お邪魔+右壁"W"
        for x in range(1, w+1):
            if field[y][x] == "A":  # お邪魔ブロックの作成
                fix_id[y][x] = create_block(x, y, field[y][x])  # 固定ブロックの一種

def init_fix_id():  #固定ブロックidの二次元リストの作成
    global fix_id
    fix_id = [None]*FIELD_HEIGHT  # 初期値None
    for y in range(FIELD_HEIGHT):
        fix_id[y] = [None]*FIELD_WIDTH

def window_quit(event):  # qを押したときの関数定義
    print("quit")
    window.after_cancel(after_id)
    window.destroy()     # ウィンドウを破棄

def click_button():
    new_game()
    create_new_block()

def new_game():
    global status
    canvas.delete("all") # 全ての図形を示すタグ"all"
    create_field()       # フィールドの作成
    init_fix_id()        # 固定ブロックidの2次元リスト
    create_ojama()
    status = "stop"

####################
# メイン処理：ここから
BLOCK_SIZE = 40       #ブロックサイズ：40*40画素の正方形
FIELD_WIDTH = 10 +2   #フィールド幅：10ブロック  ＋ 左壁・右壁：+2ブロック
FIELD_HEIGHT = 20 +2  #フィールド高さ：20ブロック ＋ 天井・床：+2ブロック

window = tk.Tk()        #ウインドウの作成
window.title('tetris')  #ウインドウのタイトル

#フィールド用のcanvas
canvas_w = FIELD_WIDTH*BLOCK_SIZE +1    #右端の輪郭分：+1
canvas_h = FIELD_HEIGHT*BLOCK_SIZE +1   #下端の輪郭分：+1
canvas = tk.Canvas(window, width=canvas_w, height=canvas_h, highlightthickness=0) #キャンバス:描画エリア
canvas.pack(padx=10, pady=10, side="left")  #canvasを左寄せ：余白padding:10画素

FONT=("Consolas", 16)   #表示用フォント
#グローバル変数active表示用のlabel
label = tk.Label(window, width=50, height=4,    #50文字分、4行
                 font=FONT, bg="white",
                 borderwidth=1, relief="solid") #枠の種類relief：実線solid
label.pack(padx=10, pady=10, side="top")  #labelを左寄せ：余白padding:10画素

#startボタン
button = tk.Button(window, text="start", command=click_button, font=FONT)
button.pack(padx=10, pady=10, side="top")

window.bind("<Right>", move_block)  #右矢印キーを押したときの関数move_block()登録
window.bind("<Left>", move_block)   #左矢印キーを押したときの関数move_block()登録
window.bind("<Down>", move_block)   #下矢印キーを押したときの関数move_block()登録
window.bind("<Up>", rotate_block)   #上矢印キーを押したときの関数rotate_block()登録
window.bind("q", window_quit)       #qを押したときの関数window_quit()登録

new_game()

def down_block():
    global after_id
    window.event_generate("<Down>")  #下矢印キーのイベント生成
    after_id = window.after(500, down_block)

window.after(500, down_block)  #500ms後に、強制的に落下
window.mainloop() #イベントループ（描画、キー入力）

