
import configparser

file = open("C:/Users/Pupul/Desktop/getlog.log", "r")

config = configparser.ConfigParser()
config.read("C:/Users/Pupul/Desktop/getkeys.ini")

count = 0
total=0
for lines in file:
    x = (lines.split("--"))[3]
    s = config.get("Section2", "key4")
    s = s + "\n"
    if (x == s):
        count = count + 1
    total=total+1

print("no of new kmz files added: ", count)

file=open("C:/Users/Pupul/Desktop/getlog.log", "r")
b=0
sec1=0
sec2=0
min1=0
min2=0
ho1=0
ho2=0
for j in file:
    b=b+1
    if(b==1):
        tq = (j.split("--"))[1]
        x= tq.split(":")
        sec1=int(x[2])
        min1=int(x[1])
        ho1=int(x[0])
    if(b==total):
        tq = (j.split("--"))[1]
        x = tq.split(":")
        sec2 = int(x[2])
        min2 = int(x[1])
        ho2 = int(x[0])
processingTime=""
if(sec2<sec1):
    sec2=sec2+60
    min1=min1-1
processingTime=str(sec2-sec1)+"seconds"+processingTime

if(min2<min1):
    min2=min2+60
    ho2=ho2-1
processingTime=str(min2-min1)+"minutes"+processingTime

processingTime=str(ho2-ho1)+"hours"+processingTime
print (processingTime)





while (1):
    print("Enter the no of file whose execution time , you want to find.")
    r = int(input())
    c = 0
    d = 0
    tq = 0
    tf = 0
    eq = 0
    ef = 0
    s = config.get("Section2", "key1")
    f = config.get("Section2", "key4")
    f = f + "\n"
    s = s + "\n"
    file = open("C:/Users/Pupul/Desktop/getlog.log", "r")
    for j in file:
        x = (j.split("--"))[3]
        if (x == s and d == 0):
            c = c + 1
            if (c == r):
                tq = (j.split("--"))[1]
                eq = (j.split("--"))[2]
                d = d + 1
        if (x == f and d == 1):
            tf = (j.split("--"))[1]
            ef = (j.split("--"))[2]
            d = d + 1
        if (d == 2):
            print(tq, tf)
            x = tq.split(":")
            y = tf.split(":")
            cv = ""
            sec1 = 0
            sec2 = 0
            min1 = 0
            min2 = 0
            ho1 = 0
            ho2 = 0;
            for j in reversed(range(3)):
                if (j == 2):
                    sec1 = int(x[j])
                    sec2 = int(y[j])
                    if (sec1 > sec2):
                        min2 = min2 - 1
                        sec2 = sec2 + 60
                    df = sec2 - sec1
                    cv = cv+str(df) + "seconds"
                elif (j == 1):
                    min1 = int(x[j])
                    min2 = int(y[j])
                    if(min1 > min2):
                        ho2=ho2-1
                        min2=min2+60
                    df = min2-min1
                    cv = cv+str(df)+"minutes"
                elif(j==0):
                    ho1= int (x[j])
                    ho2=int (y[j])
                    df=ho2-ho1
                    cv=cv+str(df)+"hours"
            print(cv)
            break
