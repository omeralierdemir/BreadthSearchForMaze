import cv2
import numpy as np


#img = cv2.imread("6.png" , 0)
img = cv2.imread("a.jpg", 0)
#img = cv2.imread("bes.jpeg",0)
print(len(img[0]), len(img[1]),img.shape)
#gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)



thn = cv2.ximgproc.thinning(img,None,cv2.ximgproc.THINNING_ZHANGSUEN)


def birlestir(dizi,katman):
    """ for k in reversed(dizi):  # burada tersten dizinin elemanlarını gerezerek [0,0] olan düğüm noktasının indix numarasını bulmaya çalıştık

            if([k[0],k[1]] == [0,0]):


                break

            count = count + 1 """

    """for i in range(len(katman) -1): # katman sayısının bir eksiği kadar dönmesini istedik

         for j in dizi:

             if(koordinat == [j[0],j[1]]):

                 dugumKordinatları.append([j[0],j[1]])
                 path.extend(j[2])
                 koordinat = j[2][-1]
                 break

                 # koordinat tek değer atıyor  bak ona hacıv """
    count = 0
    path = []
    dugumKordinatları = []




    ara = katman[-1][-1][2][0]

    koordinat = dizi[-1][-1][-1]  # path in [0,0] noktasına erişecek yukarıya kadar gidecek ondan böyle silme doğru bu :) yani büyük ihtimalle :D
    path.extend(katman[-1][-1][2])



    for i in reversed(katman):

        for j in i:

            if(ara == [j[0],j[1]]):

                ara = j[2][0]
                path.extend(j[2])
                dugumKordinatları.append([j[0],j[1]])
                break






    return dugumKordinatları,path


def sıralıSonuc(startP,end,backPath,img): # ab bitiş noktalrı arguman uyuşmazlığı var kontrol et


    y,x = startP
    kopruler = []
    lastDugum = []  # 0-0 olabilir null değerden iyidir test et
    dugumler=[[y,x]]  #iç içe dizilerin mantığını kontrol et  [[x,y,0]] yapman gerekebilir diğer alternatif [[x,y]]
    dugumKoordinat = dugumler[:]
    backDugum = []
    sayac = []
    katman = []
    while(len(dugumler)>0):




        dugumler,path,checkP, backPath = sıralıArama(dugumKoordinat,end,backPath ,img)  #while den çıkması demek dugumun = 0 olması demek buda doğru sonucu bulduğu anlamına gelmekte kodu inceleve gereksiz ise checkP ortadan kaldır. # burada dugumkordinatları eklememizin sebebi bir önceki katmandaki dugumlere yani geriye gitmeyi önlemek amaç

        dugumKoordinat = []


        for i in dugumler:
            kopruler.append([i[0], i[1]])  # dugum nokları sıra ile ekleniyo

            if ([i[0], i[1]] != [-1, -1]):
                dugumKoordinat.append([i[0], i[
                    1]])  # [-1,-1] olan düğümler filtrelendi ve bu değer olmayan düğümler yani koordinatlar bulunuyor

        lastDugum.extend(dugumKoordinat)
        sayac.extend(dugumler)  # append maybe...  checP ==1 ise dugum --> 0-0 olanı bul birleştirme algoritmasını çağır. breakleye  bilirsin

        for k in backPath:

            k.extend(lastDugum)



        if (checkP == 1):


            katman.append(dugumler)
         #   sayac.extend(dugumler)  # append maybe...  checP ==1 ise dugum --> 0-0 olanı bul birleştirme algoritmasını çağır. breakleye  bilirsin

            break

        elif (len(dugumler) == 1 and ([dugumler[-1][0], dugumler[-1][1]] == [-1, -1])):

            break # hacı bunu etraflıca düşün  # bu olay gerçekleşirse bir daha fotoğraf çektirilip çözüm olayı tekrarlanılabilir










        katman.append(dugumler)



    dugum,path = birlestir(sayac,katman)

    #img2 = cv2.imread("6.png",1)
    img2 = cv2.imread("a.jpg", 1)
   # img2 = cv2.imread("bes.jpeg", 1)



    for i in path:

        y,x = i

        img2[y][x] = [255,0,0]

    cv2.namedWindow("omer", cv2.WINDOW_NORMAL)
    cv2.resizeWindow("omer", 1174, 1117)
    cv2.imshow("omer",img2)
    cv2.waitKey(0)






# bu metodun amacı dugumlerin yanına ek olarak elenmiş olan path ile birlikte tüm dügümleri tek dizide toplamaktır. path döndermek gerekesiz olabilir ilerleyen zamanlarda temizlemelisin
def sıralıArama(dugumSa, end, backPoint, img):  # dizi döndörme arguman olarak sıkıntı olabilir pythonda

    dugumler = []
    backPath = []
    count = 0
    araci1 = []
    araci2 = []
    pathAraci1 = []
    pathAraci2 = []
    araDeger = []
    for i in dugumSa:


        for j in backPoint:


            if(i in j):

                #araci2 = araci2 + araci1[:] # şuan için tüm dügümler için eklemen gerektiğini düşünmüyorum bu yüzden alttaki satırda sadece araci1 i ekledim bu satır yorum satırı
               # pathAraci2 = pathAraci1 + pathAraci2
               # j.extend(araci1)
                path, dugum, checkP, backP = komsuluk(i[0], i[1], end, [j], img)  # i[0,0,0] uyumsuzluğu dikkat et # hacı burda i[][] de olabilir dikkat!!!!


                for k in dugum:

                    araDeger.append([k[0],k[1]])



                backPath.append(backP) # bu satırdaki amaç her düğümün backPath ini bulmak
                araDeger = []
                break


        if(checkP == 1):

            dugumler.extend(dugum)  # append de olabilir.

            break



        dugumler.extend(dugum)  # append de olabilir.



    return dugumler ,path,checkP,backPath    # path i döndürmek sıkıntılı olabiblir





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





        if ([i, j] in end):  # dugum == yon

            print(
                "umulur ki doğru yolu bulasın...")  # burada ileriyi kontrol edicek kodu yazmalısın  bitiş noktasını burda kıyasla eğer eşitse doğru yolu bulduğun umulur
            dizi.append([i, j])
            dizi.pop(0)
            dizi.pop(0)

            dogruYol = 1
            dugum = [[0, 0, dizi]]  # şuna bi bak
            break





        elif (len(yon) > 1):# dugum içini başka bir değişkene ata sebebi bu şekilde dugum her zaman 0 büyük oluyor. !!!!DİKKAT ETMELİSİN!!!!!!!!!


            dizi.append([i, j])



            dugum = dugumNoktalari(i, j, yon)



            filtreDugum = dugumFiltre(i,j,dugum)

            if(len(filtreDugum) > 1):




                backPath.append([dizi[-1], dizi[-2], dizi[-3]])  # dugum noktalarında geri dönüşü engellemek için yaptık burada path son ve dugum pikselleri eklenmesi amçlanmıştır.
                backPath[-1].extend(filtreDugum[:])  # buradaki kodda o anki katmandaki düğümlere gitmek engellenmiştir.

                dizi.pop(0)
                dizi.pop(0)

                for k in range(len(dugum)):

                    dugum[k] = dugum[k] + [dizi]

                   # k = k + dizi




                    # buradaki amacımız  [[dugum1],[dugum2],[yol dizisi]] burada yol dizisinin son elemaın dugumun başlangıc noktasındaki pikselin bir önceki pikselidir"""







                break  # ana döngüye ait break




            else:

                # dizi.append(filtreDugum[0])  # append olabilir hacı dikkat   # hacı burada ekleme yapmaya gerek yok sadece ive j nin yeni konumunu ayarlaman yeterlidir.
                i,j = filtreDugum[0]
                backPath.append([dizi[-1], dizi[-2], [i,j]])
                backPath[-1] = backPath[-1] + backPath[0]  # aşağıda ekleme yaptık burada eklemeye gerek var mı bilmiyorum %90 yok ilerleyen zamanda sil




















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

            backPath[-1] = backPath[-1] + backPath[0]  # burada geri dönüşü engellemek için ilk başta gönderdiğin düğüm bilgilerinide ekleyerek ilerliyoruz sisteme yük bindiriyor( fazla veri gerekirse silinecek) ileleyen süreçte elden geçir kodu

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
    resDizi = []
    res2Dizi = []

    kopru = 0
    kopru2 = 0



    for i in dugum:
        for j in dugum:

            resDizi.append(abs(i[0] - j[0]))
            res2Dizi.append(abs(i[1] - j[1]))


    resDizi.sort()
    res2Dizi.sort()

    res = resDizi[-1]
    res2 = res2Dizi[-1]

    if(len(dugum) == 3 and res == 0): # dugum sayısı 3 e eşit olduğunda ve geliş guzergahının sagında veya solunda dugumlerin oldugu durum (y   ekseni için) # dikkat et bu durum gerçekleştiğinde dugum sayısı 3 de olsa aralarındaki fark 0 olmuyor. fark sıfır olsa dugum sayısı == 2 olmuş oluyor

        kopru = 0


    elif(len(dugum) ==  3 and res2 == 0):  # dugum sayısı 3 e eşit olduğunda ve geliş guzergahının altında veya ustunde dugumlerin oldugu durum (x ekseni için)

        kopru = 0


    elif(res > 1 or res2 > 1 or (res == 1 and res2 == 1)):

        dizi = dugum[:]

        kopru = 1





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




""""x,y,z,a = komsuluk(42,28,[[41,28]],[[[41,28]]],thn)

print("path:", x)
#print("sadece dugumler : " , y[0][0], y[0][1] ,  " - ", y[1][0], y[1][1])

print("sadece dugumler : " )
for i in y:
    print(i[0],i[1])
    print()
print("dugumler : " , y)
print("point : " ,z)

print("backPoint : " ,a)"""

#sıralıSonuc([108,21],[[926,1013]],[[[108,20],[108,21]]],thn) # real
#sıralıSonuc([214,218],[[101,101]],[[[214,218],[214,219]]],thn) # 6.png
#sıralıSonuc([4,120],[[160,120]],[[[3,120],[4,120]]],thn) # 7.png


#sıralıSonuc([116,124],[[69,79]],[[[116,124],[116,125]]],thn) # bes.jpeg
#sıralıSonuc([61,57],[[69,79]],[[[61,57],[62,57]]],thn) # bes.jpeg
#sıralıSonuc([80,131],[[60,69]],[[[80,131],[81,131]]],thn) # bes.jpeg

#sıralıSonuc([135,164],[[69,79]],[[[135,164],[135,165]]],thn) # bes.jpeg
#sıralıSonuc([135,164],[[69,79]],[[[135,164],[135,165]]],thn)

#sıralıSonuc([5,360],[[754,397]],[[[5,360],[4,360]]],thn) # dort.png
sıralıSonuc([136,178],[[627,629]],[[[136,178],[137,179]]],thn) # oval

#sıralıSonuc([3,144],[[312,176]],[[[2,144],[3,144]]],thn)
#sıralıSonuc([114,57],[[1012,933]],[[[114,56],[144,57]]],thn)

"""print()
print()
print()
a,b,c,z = sıralıArama([[42,28]],[[320,28]],[[[42,28],[41,28]]],thn)
print("path:", b)
#print("sadece dugumler : " , y[0][0], y[0][1] ,  " - ", y[1][0], y[1][1])

print("sadece dugumler : " )
for i in a:
    print(i[0],i[1])
    print()
print("dugumler : " )
print()
for i in a:
    print(i)
    print()
print("backPoint : " ,z)"""
