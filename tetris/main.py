import pygame
from random import randint
import time
from math import pow

pygame.init()

screen=pygame.display.set_mode((700,1000))

pygame.display.set_caption('tetris')

icon=pygame.image.load('png/tetris.png')
pygame.display.set_icon(icon)

block=pygame.image.load('png/blok.png')
plansza=pygame.image.load('png/plansza.png')

piesR=pygame.image.load('png/piesR.png')
piesL=pygame.image.load('png/piesL.png')
pieselR=pygame.image.load('png/pieselR.png')
pieselL=pygame.image.load('png/pieselL.png')
psy1=(pieselR,pieselL)
psy2=(piesR,piesL)


def blok(x,y):
    screen.blit(block,(x,y))


# DANE STARTOWE #
wynik=0
x=300
y=100
speed=0.5
klocki=[[] for _ in range(7)]
tablica=[[0]*12 for _ in range(16)]
tablica.append([1]*12)
c=0
run=True
zycie=1
#piesel
xp=0
yp=0
sx=2
sy=2
###########
def k(klocki):
    klocki[0].append([[1]*2 for _ in range(2)])

    klocki[1].append([[1,1,1,1],[0,0,0,0]])
    klocki[1].append([[1] for _ in range(4)])

    t=[ [0,1],
        [1,1],
        [0,1]]
    klocki[2].append(t)
    t=[ [1,0],
        [1,1],
        [1,0]]
    klocki[2].append(t)
    t=[ [0,1,0],
        [1,1,1]]
    klocki[2].append(t)
    t=[ [1,1,1],
        [0,1,0]]
    klocki[2].append(t)

    t=[ [0,1],
        [0,1],
        [1,1]]
    klocki[3].append(t)
    t=[ [1,1],
        [1,0],
        [1,0]]
    klocki[3].append(t)
    t=[ [1,0,0],
        [1,1,1]]
    klocki[3].append(t)
    t=[ [1,1,1],
        [0,0,1]]
    klocki[3].append(t)

    t=[ [1,1],
        [0,1],
        [0,1]]
    klocki[4].append(t)
    t=[ [1,0],
        [1,0],
        [1,1]]
    klocki[4].append(t)
    t=[ [0,0,1],
        [1,1,1]]
    klocki[4].append(t)
    t=[ [1,1,1],
        [1,0,0]]
    klocki[4].append(t)

    t=[ [1,0],
        [1,1],
        [0,1]]
    klocki[5].append(t)
    t=[ [0,1,1],
        [1,1,0]]
    klocki[5].append(t)

    t=[ [0,1],
        [1,1],
        [1,0]]
    klocki[6].append(t)
    t=[ [1,1,0],
        [0,1,1]]
    klocki[6].append(t)
k(klocki)
###########

def sapce(tab,t,x,y):
    a=len(t)
    b=len(t[0])
    for i in range(b):
        j=a
        while t[j-1][i]!=1 and j>=0:
            j-=1
        if tab[j+int(y/50)-2][i+int(x/50)-1]==1: return False
    return True

def built(tab,t,x,y):
    a=len(t)
    b=len(t[0])
    for j in range(a):
        for i in range(b):
            if t[j][i]==1:
                tab[j+int(y/50)-2][i+int(x/50)-1]=1

def repair(tab,s):
    q=0
    for i in range(16):
        if sum(tab[i])==12:
            if s>0.3: s-=0.01
            q+=1
            tab.pop(i)
            t=[[0]*12]
            tab=t+tab
    return tab,s,q


czas=time.perf_counter()
rand=randint(0, 6)
while run:
    if zycie==1: screen.fill((50,50,50))
    else: screen.fill((250,0,0))

    screen.blit(plansza, (50, 100))

    if tablica[0][5]==1 or tablica[0][6]==1:
        if wynik>=100: psy=psy2
        else:   psy=psy1
        zycie=0


    #wyswietlanie planszy
    for i in range(12):
        for j in range(16):
            if tablica[j][i]==1: blok(i*50+50,j*50+100)


    #spadanie klocka
    if time.perf_counter()-czas>=speed and zycie==1:
        czas=time.perf_counter()
        if sapce(tablica,klocki[rand][c],x,y): y+=50
        else:
            built(tablica,klocki[rand][c],x,y)
            tablica,speed,mnoznik=repair(tablica,speed)
            wynik+=int(pow(10,mnoznik))
            print("Wynik: ",wynik)
            rand=randint(0, 6)
            c=0
            y=100
            x=300



    #printowanie spadajacego klocka
    if zycie==1:
        a=len(klocki[rand][c])
        b=len(klocki[rand][c][0])
        for i in range(a):
            for j in range(b):
                if klocki[rand][c][i][j]==1: blok(j*50+x,i*50+y)
    else:#pieseł
        if sx>0: screen.blit(psy[0], (xp, yp))
        else: screen.blit(psy[1], (xp, yp))

        xp+=sx
        yp+=sy

        if xp>600: xp=600; sx*=-1
        if xp<0: xp=0; sx*=-1
        if yp>880: yp=880; sy*=-1
        if yp<0: yp=0; sy*=-1



    #main
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            run=False
            print("Wynik koncowy: ", wynik)
            print('Nała')


        if event.type==pygame.KEYDOWN:
            if event.key==pygame.K_LEFT:
                if x>50 and sapce(tablica,klocki[rand][c],x-50,y): x-=50
            if event.key==pygame.K_RIGHT:
                if x<650-(b)*50 and sapce(tablica,klocki[rand][c],x+50,y): x+=50
            if event.key==pygame.K_DOWN:
                m=0
                while sapce(tablica,klocki[rand][c],x,y+m*50): m+=1
                y+=m*50
            if event.key==pygame.K_c:
                c=(c+1)%len(klocki[rand])
                b=len(klocki[rand][c][0])
                if x>650-(b)*50: x=650-(b)*50






    pygame.display.update()