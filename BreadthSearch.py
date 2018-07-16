import cv2
import numpy as np


img = cv2.imread("om.png" , 0)

print(len(img[0]), len(img[1]),img.shape)
#gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)



thn = cv2.ximgproc.thinning(img,None,cv2.ximgproc.THINNING_ZHANGSUEN)




cv2.imshow("omer",thn)
cv2.waitKey(0)


def birlestir(dizi,katman):

    path = []
    koordinat = []
    dugumKordinatları = []
    path.extend(dizi[-1][-1])
    koordinat = dizi[-1][-1][-1]

    for i in range(len(katman) -1): # katman sayısının bir eksiği kadar dönmesini istedik

        for j in dizi:

            if(koordinat == [j[0][1]]):

                dugumKordinatları.append([j[0]],j[1])
                path.extend(j[2])
                koordinat = j[2][-1]
                break



def sıralıSonuc(x,y,a,b,img):

    dizi=[[x,y]]   #iç içe dizilerin mantığını kontrol et  [[x,y,0]] yapman gerekebilir diğer alternatif [[x,y]]
    sayac = []
    katman = []
    while(len(dizi)>0):

        dizi,path,checkP = sıralıArama(dizi,a,b,img)  #while den çıkması demek dugumun = 0 olması demek buda doğru sonucu bulduğu anlamına gelmekte kodu inceleve gereksiz ise checkP ortadan kaldır.

        sayac.extend(dizi) # append maybe...  checP ==1 ise dugum --> 0-0 olanı bul birleştirme algoritmasını çağır. breakleye  bilirsin

        katman.append(dizi)
        if (checkP == 1):
            break

    birlestir(dizi,katman)

def sıralıArama(dugumSa, a, b, img):  # dizi döndörme arguman olarak sıkıntı olabilir pythonda
    dugumler = []
    for i in dugumSa:


        dugum,path, checkP = komsuluk(i[0], i[1], a, b, img)     # i[0,0,0] uyumsuzluğu dikkat et # hacı burda i[][] de olabilir dikkat!!!!
        dugumler.extend(dugum)  # append de olabilir.

    return dugumler ,path,checkP     # path i döndürmek sıkıntılı olabiblir


def komsuluk(x,y,end,img):
    i, j = x, y
    state = True
    dugum = []

    dizi= [[0,0]]  # burada hata olabilir...  burada başlangıcı belirledik  ----> Hacı burada boş küme ile başlattım. return evresinden önce o elemanı silmelisin
    deg = 0
    dogruYol = 0

    while state:

        yon = []

        if (img[i][j + 1] == 255 and dizi[-1] != [i,j]): # burda bug var i,j dizinin ilk elamanını 0-0 yapıyorum ama etraflıca düşün
            yon.append(0)
            kopru = 0

        if (img[i + 1][j + 1] == 255 and dizi[-1] != [i,j]):
            yon.append(1)
            kopru = 1

        if (img[i + 1][j] == 255 and dizi[-1] != [i,j]):
            yon.append(2)
            kopru = 2


        if (img[i + 1][j - 1] == 255 and dizi[-1] != [i,j]):
            yon.append(3)
            kopru = 3

        if (img[i][j - 1] == 255 and dizi[-1] != [i,j]):
            yon.append(4)
            kopru = 4

        if (img[i - 1][j - 1] == 255 and dizi[-1] != [i,j]):
            yon.append(5)
            kopru = 5

        if (img[i - 1][j] == 255 and dizi[-1] != [i,j]):
            yon.append(6)  #duvgum değikeninin adını yon olarak değiştir.
            kopru = 6

        if (img[i - 1][j + 1] == 255 and dizi[-1] != [i,j]):  # buralara dikkat et ve 255 değerine de

            yon.append(7)
            kopru = 7




        if (len(yon) > 1):# dugum içini başka bir değişkene ata sebebi bu şekilde dugum her zaman 0 büyük oluyor. !!!!DİKKAT ETMELİSİN!!!!!!!!!

            dugum = dugumNoktalari(i, j, yon)
            for i in range(len(dugum)):

                dugum[i].extend(dizi)  #append olabilir


          # buradaki amacımız  [[dugum1],[dugum2],[yol dizisi]] burada yol dizisinin son elemaın dugumun başlangıc noktasındaki pikselin bir önceki pikselidir"""
            break

        elif (len(yon) <= 0 and [i,j] in end ):# dugum == yon

            print("hatalı deger elde edildi...")# burada ileriyi kontrol edicek kodu yazmalısın  bitiş noktasını burda kıyasla eğer eşitse doğru yolu bulduğun umulur
            dogruYol = 1
            dugum=[[0,0,dizi]] #şuna bi bak
            break

        elif (len(yon) <= 0 and [i,j] not  in  end ):


            dugum = [[-1,-1,dizi]]
            break



        else:  # yon ==1 ise diye de koşul koyabilirsin

            dizi.append([i,j])

            interim = dugumNoktalari(i, j, yon)  #x,ydi değiştirdim i,j ile hata yapmış olabilirim...

            i,j = interim[0][0],interim[0][1] # sebebi dizi içinde dizi döndermesidir.



    dizi.pop(0)
    return dizi,dugum , dogruYol






def dugumNoktalari(x,y,dugum):


    deger = []
    for i in dugum:

        if (i == 0):

            x, y = x, y + 1

            deger.append([x, y])

        elif (i == 1):

            x, y = x + 1, y + 1
            deger.append([x , y])

        elif (i == 2):

            x, y = x + 1, y
            deger.append([x, y])

        elif (i == 3):

            x, y = x + 1, y - 1
            deger.append([x, y])

        elif (i == 4):

            x, y = x, y - 1
            deger.append([x, y])

        elif (i == 5):

            x, y = x - 1, y - 1
            deger.append([x, y])

        elif (i == 6):

            x, y = x - 1, y
            deger.append([x, y])

        elif (i == 7):

            x, y = x - 1, y + 1
            deger.append([x, y])

    return deger




def dugumFiltre(i,j,dugum,img):


    dizi = []

    kopru = 0



    for i in dugum:

        for j in dugum:

            res = i[0] - j[0]

            res2 = i[1] - j[1]

            if(res > 1 or res2 > 1 or (res == 1 and res2 == 1)):

                dizi = dugum

                kopru = 1

                break

        if(kopru == 1):

            break

    if(kopru == 0):

        for i in dugum:


            if([[i],[j + 1]] == i):


                dizi.append(i)

            elif([[i + 1],[j]] == i):

                dizi.append(i)


            elif ([[i], [j - 1]] == i):

                dizi.append(i)

            elif ([[i -1], [j]] == i):

                dizi.append(i)


    return dizi





