import os
from random import randint
import sys
import pygame as pg



WIDTH, HEIGHT = 1100, 650
os.chdir(os.path.dirname(os.path.abspath(__file__)))


def check_bound(rct: pg.Rect) -> tuple[bool, bool]:
    """
    引数で与えられたRectが画面の中か外かを判定する
    引数：こうかとんRect,爆弾Rect
    画面内ならTrue、画面外ならFalseを返す
    """
    w, h = True, True
    if rct.left < 0 or WIDTH < rct.right:
        w = False
    if rct.top < 0 or HEIGHT < rct.bottom:
        h = False
    return w, h


def main():
    pg.display.set_caption("逃げろ！こうかとん")
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    bg_img = pg.image.load("fig/pg_bg.jpg")    
    kk_img = pg.transform.rotozoom(pg.image.load("fig/3.png"), 0, 0.9)
    kk_rct = kk_img.get_rect()
    kk_rct.center = 300, 200
    
    bb_img = pg.Surface((20,20)) #爆弾用の空Surface
    pg.draw.circle(bb_img, (255, 0, 0), (10, 10), 10) #bb_imgに半径10の赤い円を描画
    bb_img.set_colorkey((0, 0, 0)) #四隅の黒を透過する
    bb_rct = bb_img.get_rect()
    bb_rct.center = randint(0,WIDTH), randint(0,HEIGHT)
    vx, vy = +5, +5 #爆弾速度ベクトル
    clock = pg.time.Clock()
    tmr = 0
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT: 
                return
        screen.blit(bg_img, [0, 0]) 

        key_lst = pg.key.get_pressed()
        sum_mv = [0, 0]       
        DELTA = {
            pg.K_UP:(0,-5), 
            pg.K_DOWN:(0,5), 
            pg.K_LEFT:(-5,0), 
            pg.K_RIGHT:(5,0),
            }
        for key, tpl in DELTA.items():
            if key_lst[key]:
                sum_mv[0] += tpl[0]
                sum_mv[1] += tpl[1]   
        
        kk_rct.move_ip(sum_mv)
        #こうかとんが画面外なら元の場所にどす
        if check_bound(kk_rct) != (True,True):
            kk_rct.move_ip(-sum_mv[0], -sum_mv[1])
        bb_rct.move_ip(vx, vy)
        #爆弾が画面外なら反対方向に移動させる
        if check_bound(bb_rct)[0] != True:
            vx *= -1
        elif check_bound(bb_rct)[1] != True:
            vy *= -1
        bb_rct.move_ip(vx, vy)
        screen.blit(kk_img, kk_rct)
        screen.blit(bb_img, bb_rct)
        pg.display.update()
        tmr += 1
        clock.tick(50)


if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()
