import turtle
import winsound
import time
#이미지 지정, 변수 지정
imagename = ["Block.gif","BuffaloUnit.gif","DogUnit.gif","HunterUnit.gif","InteractiveBlock.gif","SeaBlock.gif"]
NumberImageName=["-five.gif","-four.gif","-three.gif","-two.gif","-one.gif","zero.gif","one.gif","two.gif","three.gif","four.gif","five.gif"]

s = turtle.Screen()
for i in range(0,11):
    if i < 6: s.addshape(imagename[i])
    s.addshape(NumberImageName[i])

BlueBuffalos =[0,0,0,0,0,0,0,0,0,0,0]
RedUnit=[0,0,0,0,0]#0은 사냥꾼, 1~4는 개

TurnName =["red","blue"]; TurnNumber=1 #turnNumber0 블루,1 레드

GameOver = 0 #0==false,1==true
Start ="false"
#버팔로, 헌터, 강아지, 판그리기 함수제작
  # 게임 시작시 블럭 설치 
def PlateDefinition(x,y,Image) : 
    t= turtle.Turtle()
    t.penup()
    t.speed(10)
    t.goto(x,y)
    t.shape(Image)
    return t

def InstallationFunction(): # 맵 설치 반복 함수 
    print("설치 시작")
    
    for j in range(-5,6): # 타일 설치
        for i in range (-3,4):
            if i ==-3 or i==3 :PlateDefinition(j*100,i*100,imagename[5]);
            else :PlateDefinition(j*100,i*100,imagename[0])
    # 번호 타일 설치
    P =0; K =0          
    for x in range(-5,6):#버팔로 설치
        BlueBuffalos[P]=PlateDefinition(x*100,-300,imagename[1])
        PlateDefinition(x*100,350,NumberImageName[P])
        P =P+1
    for y in range(-3,4):
        PlateDefinition(-550,y*100,NumberImageName[K+2])
        K +=1
        
    #레드팀 사냥꾼과 사냥개 설치
    RedUnit[0]=PlateDefinition(0,200,imagename[3])
    RedUnit[1]=PlateDefinition(-200,200,imagename[2])
    RedUnit[2]=PlateDefinition(-100,200,imagename[2])
    RedUnit[3]=PlateDefinition(100,200,imagename[2])
    RedUnit[4]=PlateDefinition(200,200,imagename[2])
    Targeting(TurnNumber)


def HunterPositionDetector(target,x,y):#red팀 hunter 말특석상 움직임이 복잡함 움직임 담당 함수(중요☆)
    movelist=[[x,y+1],[x+1,y+1],[x+1,y],[x+1,y-1],[x,y-1],[x-1,y-1],[x-1,y],[x-1,y+1]];# 주변 8칸
    cangoing = 0
    # 같은 팀의 겹치는칸 확인, 걸러내기
    for i in range(1,5):
        for j in range(0,8):
            PL =[RedUnit[i].xcor()/100,RedUnit[i].ycor()/100]
            if movelist[j]!="이동불가" and(PL == movelist[j] or  movelist[j][1]==-3 or  movelist[j][1]==3 or movelist[j][0]<-5 or movelist[j][1]>5):
                movelist[j]="이동불가"
    for b in range(0,8): #출력,이동가능칸 확인
        if movelist[b] !="이동불가":
            print("움직일 수 있는 칸 ",movelist[b])
            cangoing +=1
            
        if b==7 and movelist[b] !="이동불가" and cangoing ==0:
            print("움직일 수 있는 칸이 없습니다. 선택지로 이동합니다. ");Targeting(0);
    cangoing=0
    print("현재 유닛의 이동할 좌표 입력:")
    tx =int(input("X좌표"))
    ty =int(input("Y좌표"))
    PL =[tx,ty]
                                
    for b in range(0,8):# 입력값 확인
        if PL == movelist[b]:
            print(PL,"좌표로 이동할까요? (네,아니요)")
            A = str(input())
            
            if A =="네":
                winsound.PlaySound("walk.wav",winsound.SND_FILENAME)
                target.goto(tx*100,ty*100);
                for i in range(0,11):# 버팔로와 이동 칸 겹치는지 확인하기
                    if target.xcor() == BlueBuffalos[i].xcor() and target.ycor() ==BlueBuffalos[i].ycor():
                        BlueBuffalos[i].ht();winsound.PlaySound("gun.wav",winsound.SND_FILENAME);
                        print("버팔로 사냥!");GameReferee(0)# 한마리 잡을때마다 검사
                TurnNumber=1
                Targeting(TurnNumber)# 이동, 블루팀으로 턴 넘기
                
            else:
                Targeting(0)# 다시 선택창으로 이동
                b=0
        elif b==7 and PL !=movelist[b]:
            print("이동 불가능한 좌표를 입력했습니다."); HunterPositionDetector(target,x,y);

def DogPositionDetector(target,x,y):#red팀 dog 말특석상 움직임이 복잡함 움직임 담당 함수(중요☆)
    fdmovelist = [[x,y-1],[x,y-2],[x,y-3],[x,y-4]]; bdmovelist = [[x,y+1],[x,y+2],[x,y+3],[x,y+4]]
    rigtsidelist = [[x+1,y],[x+2,y],[x+3,y],[x+4,y],[x+5,y]];leftsidelist = [[x-1,y],[x-2,y],[x-3,y],[x-4,y],[x-5,y]];
    frightdiagonal=[[x+1,y-1],[x+2,y-2],[x+3,y-3],[x+4,y-4]]; brightdiagonal =[[x+1,y+1],[x+2,y+2],[x+3,y+3],[x+4,y+4]]
    fleftdiagonal=[[x-1,y-1],[x-2,y-2],[x-3,y-3],[x-4,y-4]]; bletfdiagoal = [[x-1,y+1],[x-2,y+2],[x-3,y+3],[x-4,y+4]]
    cangoing =0
     # 같은 팀의 겹치는칸 확인, 걸러내기
    for j in range(0,5):
        for i in range(0,5):
            PL =[RedUnit[i].xcor()/100,RedUnit[i].ycor()/100]
            if j<4 and fdmovelist[j] !="이동불가" and (PL ==fdmovelist[j] or fdmovelist[j][1] <=-3 or (j >0 and fdmovelist[j-1]=="이동불가")) :
                fdmovelist[j]="이동불가"
            if j<4 and bdmovelist[j]!="이동불가" and(PL ==bdmovelist[j] or bdmovelist[j][1] >=3 or (j >0 and bdmovelist[j-1]=="이동불가")):
                bdmovelist[j]="이동불가"
            if j<4 and frightdiagonal[j]!="이동불가" and(PL ==frightdiagonal[j]or frightdiagonal[j][1] <=-3 or frightdiagonal[j][0] >5 or (j >0 and frightdiagonal[j-1]=="이동불가")):
                frightdiagonal[j] ="이동불가"
            if j<4 and brightdiagonal[j]!="이동불가" and (PL ==brightdiagonal[j]or brightdiagonal[j][1] >=3 or brightdiagonal[j][0] >5 or (j >0 and brightdiagonal[j-1]=="이동불가")):
                brightdiagonal[j] ="이동불가"
            if j<4 and fleftdiagonal[j]!="이동불가" and(PL ==fleftdiagonal[j]or fleftdiagonal[j][1] <=-3 or fleftdiagonal[j][0] <-5 or (j >0 and fleftdiagonal[j-1]=="이동불가")):    
                fleftdiagonal[j]="이동불가"
            if j<4 and bletfdiagoal[j]!="이동불가" and (PL ==bletfdiagoal[j]or bletfdiagoal[j][1] >=3 or bletfdiagoal[j][0] <-5 or (j >0 and bletfdiagoal[j-1]=="이동불가")):    
                bletfdiagoal[j] ="이동불가"
            if rigtsidelist[j]!="이동불가" and (PL ==rigtsidelist[j]or rigtsidelist[j][0]>5 or (j >0 and rigtsidelist[j-1]=="이동불가")):        
                rigtsidelist[j]="이동불가"                
            if leftsidelist[j]!="이동불가" and (PL ==leftsidelist[j]or leftsidelist[j][0]<-5 or (j >0 and leftsidelist[j-1]=="이동불가")):
                leftsidelist[j]="이동불가"
        for i in range(0,11):
            PL =[BlueBuffalos[i].xcor()/100,BlueBuffalos[i].ycor()/100]
            if j<4 and fdmovelist[j] !="이동불가" and (PL ==fdmovelist[j] or fdmovelist[j][1] <=-3 or (j >0 and fdmovelist[j-1]=="이동불가")) :
                fdmovelist[j]="이동불가"
            if j<4 and bdmovelist[j]!="이동불가" and(PL ==bdmovelist[j] or bdmovelist[j][1] >=3 or (j >0 and bdmovelist[j-1]=="이동불가")):
                bdmovelist[j]="이동불가"
            if j<4 and frightdiagonal[j]!="이동불가" and(PL ==frightdiagonal[j]or frightdiagonal[j][1] <=-3 or frightdiagonal[j][0] >5 or (j >0 and frightdiagonal[j-1]=="이동불가")):
                frightdiagonal[j] ="이동불가"
            if j<4 and brightdiagonal[j]!="이동불가" and (PL ==brightdiagonal[j]or brightdiagonal[j][1] >=3 or brightdiagonal[j][0] >5 or (j >0 and brightdiagonal[j-1]=="이동불가")):
                brightdiagonal[j] ="이동불가"
            if j<4 and fleftdiagonal[j]!="이동불가" and(PL ==fleftdiagonal[j]or fleftdiagonal[j][1] <=-3 or fleftdiagonal[j][0] <-5 or (j >0 and fleftdiagonal[j-1]=="이동불가")):    
                fleftdiagonal[j]="이동불가"
            if j<4 and bletfdiagoal[j]!="이동불가" and (PL ==bletfdiagoal[j]or bletfdiagoal[j][1] >=3 or bletfdiagoal[j][0] <-5 or (j >0 and bletfdiagoal[j-1]=="이동불가")):    
                bletfdiagoal[j] ="이동불가"
            if rigtsidelist[j]!="이동불가" and (PL ==rigtsidelist[j]or rigtsidelist[j][0]>5 or (j >0 and rigtsidelist[j-1]=="이동불가")):        
                rigtsidelist[j]="이동불가"                
            if leftsidelist[j]!="이동불가" and (PL ==leftsidelist[j]or leftsidelist[j][0]<-5 or (j >0 and leftsidelist[j-1]=="이동불가")):
                leftsidelist[j]="이동불가"

    for j in range(0,5): #출력,이동가능칸 확인
        if j<4:
            if fdmovelist[j] !="이동불가":
                print("움직일 수 있는 칸",fdmovelist[j])
                cangoing +=1
            if bdmovelist[j]!="이동불가":
                print("움직일 수 있는 칸",bdmovelist[j])
                cangoing +=1
            if frightdiagonal[j]!="이동불가":
                print("움직일 수 있는 칸",frightdiagonal[j])
                cangoing +=1
            if brightdiagonal[j]!="이동불가":
                print("움직일 수 있는 칸",brightdiagonal[j])
                cangoing +=1
            if fleftdiagonal[j]!="이동불가":
                print("움직일 수 있는 칸",fleftdiagonal[j])
                cangoing +=1
            if bletfdiagoal[j]!="이동불가":
                print("움직일 수 있는 칸",bletfdiagoal[j])
                cangoing +=1
        if rigtsidelist[j]!="이동불가":
            print("움직일 수 있는 칸",rigtsidelist[j])
            cangoing +=1
        if leftsidelist[j]!="이동불가":
            print("움직일 수 있는 칸",leftsidelist[j])
            cangoing +=1
        if j==4 and cangoing==0:
            print("움직일 수 있는 칸이 없습니다. 선택지로 이동합니다. ");Targeting(0);

    cangoing=0
    print("현재 유닛의 이동할 좌표 입력:")
    tx =int(input("X좌표"))
    ty =int(input("Y좌표"))
    PL =[tx,ty]
                                
    for b in range(0,5):# 입력값 확인
        if (b <4 and fdmovelist[b]==PL) or (b <4 and bdmovelist[b]==PL)or (b <4 and frightdiagonal[b]==PL)or (b <4 and brightdiagonal[b]==PL)or (b <4 and fleftdiagonal[b]==PL)or (b <4 and bletfdiagoal[b]==PL)or rigtsidelist[b]==PL or leftsidelist[b]==PL:
            print(PL,"좌표로 이동할까요? (네,아니요)") 
            A = str(input())
            
            if A =="네":
                winsound.PlaySound("walk.wav",winsound.SND_FILENAME)
                winsound.PlaySound("dog.wav",winsound.SND_FILENAME)
                target.goto(tx*100,ty*100);
                TurnNumber=1;
                Targeting(TurnNumber)# 이동, 블루팀으로 턴 넘기
            else :
                b=0; Targeting(0)# 다시 선택창으로 이동
        else:
            if b==4:
                print("이동 불가능한 좌표를 입력했습니다.");
                DogPositionDetector(target,x,y)
           
def UnitMovementRules(target,x,y,TN): #맵 배치후 게임시작 (중요☆)
    answer=""
    if TurnName[TN] =="blue":
        #첫번째 규칙 버팔로는 앞으로 한칸씩만 움직인다. 단 개가 버팔로 앞에 없을시에만
        for i in range(0,5):
            if RedUnit[i].ycor()/100 ==y+1 and RedUnit[i].xcor()/100 ==target.xcor()/100:
                print("현재 버팔로 앞에 다른 유닛이 있어 움직이지 못합니다.다시 선택지로 돌아갑니다."); i=0;Targeting(1);
                
            elif RedUnit[i].ycor()/100 !=target.ycor()+1 and RedUnit[i].xcor()/100 !=target.xcor()/100 and i==4 :
                print("현재 버팔로가 움직일 수 있는 칸좌표:",x,y+1,"움직일까요? (네,아니요)");answer =str(input())
                if answer=="네":
                    winsound.PlaySound("buffalo.wav",winsound.SND_FILENAME)
                    target.goto(x*100,(y+1)*100);GameReferee(1); TurnNumber=0;Targeting(TurnNumber);
                elif answer =="아니요":
                    i=0;Targeting(1);
    elif TurnName[TN] =="red":
        if target == RedUnit[0]:
            print("현재 사냥꾼을 지목하셨습니다. 움직일 수 있는 칸의 좌표는:"); HunterPositionDetector(target,x,y)# 사냥꾼 움직임 담당 함수
        else:
            print("현재 강아지를 지목하셨습니다. 움직일수 있는 칸의 좌표는:");DogPositionDetector(target,x,y)#사냥개 움직임 담당 함수

def Targeting(TN):#유닛 지정하는 기능 입력과 호출 둘다 (중요☆)
    if TurnName[TN] =="blue":
        print("버팔로 팀 턴 입니다. 움직이려는 말의 번호 입력하세요")
        x =int(input("X좌표"))
        y =int(input("Y좌표"))
        for i in range(0,11):
            #print("i",i ,"x",BlueBuffalos[i].xcor(), BlueBuffalos[i].xcor()/100 ==x,x,"y",BlueBuffalos[i].ycor(),BlueBuffalos[i].ycor()/100 ==y ,y)
            if BlueBuffalos[i].xcor()/100==x and BlueBuffalos[i].ycor()/100 ==y:
                UnitMovementRules(BlueBuffalos[i],x,y,TN)
                
            elif i==10 and BlueBuffalos[i].ycor() !=y and BlueBuffalos[i].xcor() !=x :
                print("아무것도 없습니다. 다시 선택창으로 이동합니다.");
                x=0;y=0;i=0;Targeting(1);
                
    elif TurnName[TN] =="red":
        print("사냥꾼 팀 턴 입니다. 움직이려는 말의 번호 입력하세요")
        x =int(input("X좌표"))
        y =int(input("Y좌표"))
        for i in range(0,5):
            if RedUnit[i].xcor()/100==x and RedUnit[i].ycor()/100 ==y: UnitMovementRules(RedUnit[i],x,y,TN);
            elif i==4 and RedUnit[i].xcor()/100!=x and RedUnit[i].ycor()/100 !=y:
                print("아무것도 없습니다. 다시 선택창으로 이동합니다.");i=0;Targeting(0);
            
def GameReferee(TN): # 승리 조건 검사
    if TurnName[TN] =="red":
        for i in range(0,11):
            if BlueBuffalos[i].isvisible()==True:
                break;
            elif i==10 and  BlueBuffalos[i].isvisible()==False:
                print("사냥꾼팀 승리!")
                winsound.PlaySound("Fanfare.wav",winsound.SND_FILENAME)
                turtle.bye()
    if TurnName[TN] =="blue":
        for i in range(0,11):
            if BlueBuffalos[i].ycor()/100 ==3:
                print("버팔로팀 승리!")
                winsound.PlaySound("Fanfare.wav",winsound.SND_FILENAME)
                turtle.bye()
    
# 프로그램 시작 =======================================

print("Up 버튼 누를시 게임 시작")

if Start=="false":
    s.onkey(InstallationFunction,"Up")
    s.listen()













