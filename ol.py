import cv2
import numpy as np


img = cv2.imread("ilk.png" , 0)

print(len(img[0]), len(img[1]),img.shape)
#gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)



thn = cv2.ximgproc.thinning(img,None,cv2.ximgproc.THINNING_ZHANGSUEN)





# bu metodun amacı dugumlerin yanına ek olarak elenmiş olan path ile birlikte tüm dügümleri tek dizide toplamaktır. path döndermek gerekesiz olabilir ilerleyen zamanlarda temizlemelisin
def sıralıArama(dugumSa, end, backPoint, img):  # dizi döndörme arguman olarak sıkıntı olabilir pythonda
    dugumler = []
    for i in dugumSa:


        path,dugum, checkP, backPoint = komsuluk(i[0], i[1], end, backPoint, img)     # i[0,0,0] uyumsuzluğu dikkat et # hacı burda i[][] de olabilir dikkat!!!!
        dugumler.extend(dugum)  # append de olabilir.

    return dugumler ,path,checkP     # path i döndürmek sıkıntılı olabiblir





def komsuluk(y,x,end,backPath,img):  # unutma i == y ekseni  j == x ekseni
    i, j = y,x
    state = True
    dugum = []


    dizi= [[0,0],[0,0]]  # burada hata olabilir...  burada en son 3 eleman eklemede sıkıntı çıkarıyor ondan böyle 2 tane 0-0 dizisi atadın  ----> Hacı burada boş küme ile başlattım. return evresinden önce o elemanı silmelisin
    deg = 0
    dogruYol = 0

    while state:

        yon = []

        if (img[i][j + 1] == 255 and [i,j+1] not in backPath[-1]): # burda bug var i,j dizinin ilk elamanını 0-0 yapıyorum ama etraflıca düşün
            yon.append(0)
            kopru = 0

        if (img[i + 1][j + 1] == 255 and [i+1,j+1] not in backPath[-1]):
            yon.append(1)
            kopru = 1

        if (img[i + 1][j] == 255 and [i+1,j] not in backPath[-1]):
            yon.append(2)
            kopru = 2


        if (img[i + 1][j - 1] == 255 and [i+1,j-1] not in backPath[-1]):
            yon.append(3)
            kopru = 3

        if (img[i][j - 1] == 255 and [i,j-1] not in backPath[-1]):
            yon.append(4)
            kopru = 4

        if (img[i - 1][j - 1] == 255 and [i-1,j-1] not in backPath[-1]):
            yon.append(5)
            kopru = 5

        if (img[i - 1][j] == 255 and [i-1,j] not in backPath[-1]):
            yon.append(6)  #duvgum değikeninin adını yon olarak değiştir.
            kopru = 6

        if (img[i - 1][j + 1] == 255 and [i-1,j+1] not in backPath[-1]):  # buralara dikkat et ve 255 değerine de

            yon.append(7)
            kopru = 7




        if (len(yon) > 1):# dugum içini başka bir değişkene ata sebebi bu şekilde dugum her zaman 0 büyük oluyor. !!!!DİKKAT ETMELİSİN!!!!!!!!!


            dizi.append([i, j])



            dugum = dugumNoktalari(i, j, yon)

            ara = dugum[:]

            filtreDugum = dugumFiltre(i,j,ara)

            if(len(filtreDugum) > 1):

                dizi.pop(0)
                dizi.pop(0)

                aralık = filtreDugum[:]
                backPath.append([dizi[-1], dizi[-2], dizi[-3]])  # dugum noktalarında geri dönüşü engellemek için yaptık burada path son ve dugum pikselleri eklenmesi amçlanmıştır.
                backPath[-1].extend(filtreDugum[:])

                for k in dugum:

                    k.extend(dizi)



                    # buradaki amacımız  [[dugum1],[dugum2],[yol dizisi]] burada yol dizisinin son elemaın dugumun başlangıc noktasındaki pikselin bir önceki pikselidir"""







                break  # ana döngüye ait break




            else:

                # dizi.append(filtreDugum[0])  # append olabilir hacı dikkat   # hacı burada ekleme yapmaya gerek yok sadece ive j nin yeni konumunu ayarlaman yeterlidir.
                i,j = filtreDugum[0]
                backPath.append([dizi[-1], dizi[-2], dizi[-3]])














        elif (len(yon) <= 0 and [i,j] in end ):# dugum == yon

            print("hatalı deger elde edildi...")# burada ileriyi kontrol edicek kodu yazmalısın  bitiş noktasını burda kıyasla eğer eşitse doğru yolu bulduğun umulur
            dizi.append([i, j])
            dizi.pop(0)
            dizi.pop(0)

            dogruYol = 1
            dugum=[[0,0,dizi]] #şuna bi bak
            break





        elif (len(yon) <= 0 and [i,j] not  in  end ):

            dizi.append([i, j])
            dizi.pop(0)
            dizi.pop(0)


            dugum = [[-1,-1,dizi]]
            break







        else:  # yon ==1 ise diye de koşul koyabilirsin
            #dizi == path
            dizi.append([i,j])

            interim = dugumNoktalari(i, j, yon)  #x,ydi değiştirdim i,j ile hata yapmış olabilirim...

            i,j = interim[0][0],interim[0][1] # sebebi dizi içinde dizi döndermesidir.

            backPath.append([dizi[-1],dizi[-2],dizi[-3]])# 3 tane eklemene gerek kalmayabilir

    #dizi.pop(0)
    #dizi.pop(0)   bunları diğer durumlar içinde yazabilirsin düğümler yoksa diye


    geriDonus = backPath[-1]
    return dizi,dugum , dogruYol, geriDonus








def dugumNoktalari(x1,y1,dugum):


    deger = []
    for i in dugum:
        x,y = x1,y1
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





def dugumFiltre(i1,j1,dugum,img=None):


    dizi = []

    kopru = 0



    for i in dugum:
        dizi = []
        for j in dugum:

            res = abs(i[0] - j[0])

            res2 = abs(i[1] - j[1])

            if(res > 1 or res2 > 1 or (res == 1 and res2 == 1)):

                dizi = dugum[:]

                kopru = 1

                break

        if(kopru == 1):

            break

    if(kopru == 0):

        for n in dugum:

            if ([i1, j1 + 1] == n):  # ----> 0

                dizi.append(n)


            elif([i1 + 1,j1] == n):  # ----> 2

                dizi.append(n)


            elif ([i1, j1 - 1] == n): # ----> 4

                dizi.append(n)

            elif ([i1 -1, j1] == n):  # ----> 6

                dizi.append(n)


    return dizi




x,y,z,a = komsuluk(42,28,[[41,28]],[[[41,28]]],thn)

print("path:", x)
#print("sadece dugumler : " , y[0][0], y[0][1] ,  " - ", y[1][0], y[1][1])

print("sadece dugumler : " )
for i in y:
    print(i[0],i[1])
    print()
print("dugumler : " , y)
print("point : " ,z)

print("backPoint : " ,a)


#a,b,c = sıralıArama([[113,52],[114,51],[114,50]],[[90,103]],[[[41,28]]],thn)
"""print("path:", b)
#print("sadece dugumler : " , y[0][0], y[0][1] ,  " - ", y[1][0], y[1][1])

print("sadece dugumler : " )
for i in a:
    print(i[0],i[1])
    print()
print("dugumler : " , y)
print("point : " ,z)"""