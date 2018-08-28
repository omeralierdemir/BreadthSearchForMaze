import cv2
import numpy as np

# img =  cv2.imread("bes.jpeg" , 0)
img = cv2.imread("re.png", 0)
# img = cv2.imread("6.png" , 0)
# img = cv2.imread("dort.png", 0)
# img = cv2.imread("ilk.png",0)
print(len(img[0]), len(img[1]), img.shape)
# gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)


thn = cv2.ximgproc.thinning(img, None, cv2.ximgproc.THINNING_ZHANGSUEN)


def birlestir(dizi, katman, sadeKatman):
    state = True
    count2 = 0

    path = []
    dugumKordinatları = []
    dugumKordinatlarıs = []
    paths = []
    sayac = []
    ters = []
    araDugumler = []
    ilkPath = []
    araKatman = []

    katman2 = []
    sayac3 = 0
    count = 0
    kopruDegerler = []
    kopruKatman = []

    print(len(sadeKatman), "sade katman")
    for a1 in katman:
        for a2 in a1:
            araKatman.append(a2 + [0])

        katman2.append(araKatman)
        araKatman = []

    print(len(katman2), len(katman))

    for k in katman[-1]:

        if ([k[0], k[1]] == [0, 0]):
            araDugumler.append(k[2][0])

            ilkPath.append(k[2])

    print("katman sayısı", len(katman2))

    for l in araDugumler:
        ara = l
        ters.extend(reversed(ilkPath[count]))
        path.extend(ters)
        count = count + 1
        print(sayac3, "sayac")
        sayac3 = sayac3 + 1

        araKatman = []

        for i in range(len(katman2) - 1, -1, -1):

            print(len(katman2[i]))
            for j in range(len(katman2[i])):

                if (ara == [katman2[i][j][0], katman2[i][j][1]] and katman2[i][j][3] == 0):
                    state = 0
                    ara = katman2[i][j][2][0]
                    katman2[i][j][3] = 1

                    path.extend(reversed(katman2[i][j][2]))
                    kopruDegerler.append(katman2[i][j][2][-1])

                    break  # fazladan ekliyorsun büyük ihtimalle burdaki ara katmandan kasıt 1 katman seviyesindeki tüm dügümler.

            if (state):

                for j in range(len(katman2[i])):

                    if (ara == [katman2[i][j][0], katman2[i][j][1]] and katman2[i][j][3] == 1):
                        ara = katman2[i][j][2][0]

                        path.extend(reversed(katman2[i][j][2]))

                        kopruDegerler.append(katman2[i][j][2][-1])

                        break

            state = True
        kopruKatman.append(kopruDegerler)
        kopruDegerler = []

        paths.append(path)
        path = []
        dugumKordinatları = []

    for s in paths:
        sayac.append([len(s), count2])
        count2 = count2 + 1

    sayac.sort()

    yonSaptama(kopruKatman[sayac[0][1]], sadeKatman)
    return dugumKordinatları, paths[sayac[0][1]]  # paths[sayac[0][1] en kısa yolu verir (countla ilişkili dikkat et)


def sıralıSonuc(startP, end, backPath, img):  # ab bitiş noktalrı arguman uyuşmazlığı var kontrol et

    count = 1
    y, x = startP
    kopruler = []
    lastDugum = []  # 0-0 olabilir null değerden iyidir test et
    dugumler = [[y, x]]  # iç içe dizilerin mantığını kontrol et  [[x,y,0]] yapman gerekebilir diğer alternatif [[x,y]]
    dugumKoordinat = dugumler[:]
    backDugum = []
    sayac = []
    katman = []
    sadeKatman = []
    while (len(dugumler) > 0):

        dugumler, path, checkP, backPath = sıralıArama(dugumKoordinat, end, backPath,
                                                       img)  # while den çıkması demek dugumun = 0 olması demek buda doğru sonucu bulduğu anlamına gelmekte kodu inceleve gereksiz ise checkP ortadan kaldır. # burada dugumkordinatları eklememizin sebebi bir önceki katmandaki dugumlere yani geriye gitmeyi önlemek amaç

        dugumKoordinat = []

        for k in backPath:
            k.extend(lastDugum)

        for i in dugumler:
            kopruler.append([i[0], i[1]])  # dugum nokları sıra ile ekleniyo

            if ([i[0], i[1]] != [-1, -1]):
                dugumKoordinat.append([i[0], i[
                    1]])  # [-1,-1] olan düğümler filtrelendi ve bu değer olmayan düğümler yani koordinatlar bulunuyor

        sadeKatman.append(dugumKoordinat)
        lastDugum.extend(dugumKoordinat)
        sayac.extend(
            dugumler)  # append maybe...  checP ==1 ise dugum --> 0-0 olanı bul birleştirme algoritmasını çağır. breakleye  bilirsin

        if (checkP >= 1):  # checkPoint

            katman.append(dugumler)
            #   sayac.extend(dugumler)  # append maybe...  checP ==1 ise dugum --> 0-0 olanı bul birleştirme algoritmasını çağır. breakleye  bilirsin

            break

        elif (len(dugumler) == 1 and ([dugumler[-1][0], dugumler[-1][1]] == [-1, -1])):

            break  # hacı bunu etraflıca düşün  # bu olay gerçekleşirse bir daha fotoğraf çektirilip çözüm olayı tekrarlanılabilir

        katman.append(dugumler)

    dugum, path = birlestir(sayac, katman, sadeKatman)

    # img2 = cv2.imread("dort.png",1)
    img2 = cv2.imread("res.png", 1)
    # img2 = cv2.imread("ilk.png", 1)
    # img2 = cv2.imread("gercek.png", 1)
    # img2 = cv2.imread("bes.jpeg", 1)

    for i in path:
        y, x = i

        img2[y][x] = [255, 0, 0]

    cv2.namedWindow("omer", cv2.WINDOW_NORMAL)
    cv2.resizeWindow("omer", 1174, 1117)
    cv2.imshow("omer", img2)
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
    checkToplam = 0
    for i in dugumSa:

        for j in backPoint:

            if (i in j):

                # araci2 = araci2 + araci1[:] # şuan için tüm dügümler için eklemen gerektiğini düşünmüyorum bu yüzden alttaki satırda sadece araci1 i ekledim bu satır yorum satırı
                # pathAraci2 = pathAraci1 + pathAraci2
                # j.extend(araci1)
                path, dugum, checkP, backP = komsuluk(i[0], i[1], end, [j],
                                                      img)  # i[0,0,0] uyumsuzluğu dikkat et # hacı burda i[][] de olabilir dikkat!!!!

                checkToplam = checkP + checkToplam

                for k in dugum:
                    araDeger.append([k[0], k[1]])

                backPath.append(backP)  # bu satırdaki amaç her düğümün backPath ini bulmak
                araDeger = []
                break

        dugumler.extend(dugum)  # append de olabilir.

    return dugumler, path, checkToplam, backPath  # path i döndürmek sıkıntılı olabiblir


def komsuluk(y, x, end, backPath, img):  # unutma i == y ekseni  j == x ekseni
    i, j = y, x
    state = True
    backPath[-1].extend([[i, j]])
    dugum = []
    count = 0

    dizi = [[0, 0], [0,
                     0]]  # burada hata olabilir...  burada en son 3 eleman eklemede sıkıntı çıkarıyor ondan böyle 2 tane 0-0 dizisi atadın  ----> Hacı burada boş küme ile başlattım. return evresinden önce o elemanı silmelisin
    deg = 0
    dogruYol = 0

    while state:

        yon = []

        if (img[i - 1][j + 1] == 255 and [i - 1, j + 1] not in backPath[-1]):  # buralara dikkat et ve 255 değerine de

            yon.append(0)
            kopru = 0

        if (img[i][j + 1] == 255 and [i, j + 1] not in backPath[
            -1]):  # burda bug var i,j dizinin ilk elamanını 0-0 yapıyorum ama etraflıca düşün
            yon.append(1)
            kopru = 1

        if (img[i + 1][j + 1] == 255 and [i + 1, j + 1] not in backPath[-1]):
            yon.append(2)
            kopru = 2

        if (img[i + 1][j] == 255 and [i + 1, j] not in backPath[-1]):
            yon.append(3)
            kopru = 3

        if (img[i + 1][j - 1] == 255 and [i + 1, j - 1] not in backPath[-1]):
            yon.append(4)
            kopru = 4

        if (img[i][j - 1] == 255 and [i, j - 1] not in backPath[-1]):
            yon.append(5)
            kopru = 5

        if (img[i - 1][j - 1] == 255 and [i - 1, j - 1] not in backPath[-1]):
            yon.append(6)
            kopru = 6

        if (img[i - 1][j] == 255 and [i - 1, j] not in backPath[-1]):
            yon.append(7)  # duvgum değikeninin adını yon olarak değiştir.
            kopru = 7

        if ([i, j] in end):  # dugum == yon

            print(
                "umulur ki doğru yolu bulasın... ")  # burada ileriyi kontrol edicek kodu yazmalısın  bitiş noktasını burda kıyasla eğer eşitse doğru yolu bulduğun umulur
            dizi.append([i, j])
            dizi.pop(0)
            dizi.pop(0)

            dogruYol = 1
            dugum = [[0, 0, dizi]]  # şuna bi bak
            break





        elif (len(
                yon) > 1):  # dugum içini başka bir değişkene ata sebebi bu şekilde dugum her zaman 0 büyük oluyor. !!!!DİKKAT ETMELİSİN!!!!!!!!!

            dizi.append([i, j])

            dugum = dugumNoktalari(i, j, yon)

            filtreDugum = dugumFiltre(i, j, dugum)  # filtreDugum2 == backPath için dügüm

            if (len(filtreDugum) > 1):

                backPath.append([dizi[-1], dizi[-2], dizi[
                    -3]])  # dugum noktalarında geri dönüşü engellemek için yaptık burada path son ve dugum pikselleri eklenmesi amçlanmıştır.
                backPath[-1].extend(filtreDugum[:])  # buradaki kodda o anki katmandaki düğümlere gitmek engellenmiştir.

                dizi.pop(0)
                dizi.pop(0)

                for k in range(len(dugum)):
                    dugum[k] = dugum[k] + [dizi]  # buranın filtre dugum olası lazım değil mi?

                # k = k + dizi

                # buradaki amacımız  [[dugum1],[dugum2],[yol dizisi]] burada yol dizisinin son elemaın dugumun başlangıc noktasındaki pikselin bir önceki pikselidir""

                break  # ana döngüye ait break




            else:

                # dizi.append(filtreDugum[0])  # append olabilir hacı dikkat   # hacı burada ekleme yapmaya gerek yok sadece ive j nin yeni konumunu ayarlaman yeterlidir.
                i, j = filtreDugum[0]
                backPath.append([dizi[-1], dizi[-2], [i, j]])
                backPath[-1] = backPath[-1] + backPath[
                    0]  # aşağıda ekleme yaptık burada eklemeye gerek var mı bilmiyorum %90 yok ilerleyen zamanda sil



        elif (len(yon) <= 0 and [i, j] not in end):

            dizi.append([i, j])
            dizi.pop(0)
            dizi.pop(0)

            dugum = [[-1, -1, dizi]]
            break







        else:  # yon ==1 ise diye de koşul koyabilirsin
            # dizi == path
            dizi.append([i, j])

            interim = dugumNoktalari(i, j, yon)  # x,ydi değiştirdim i,j ile hata yapmış olabilirim...

            i, j = interim[0][0], interim[0][1]  # sebebi dizi içinde dizi döndermesidir.

            backPath.append([dizi[-1], dizi[-2], dizi[-3]])  # 3 tane eklemene gerek kalmayabilir

            backPath[-1] = backPath[-1] + backPath[
                0]  # burada geri dönüşü engellemek için ilk başta gönderdiğin düğüm bilgilerinide ekleyerek ilerliyoruz sisteme yük bindiriyor( fazla veri gerekirse silinecek) ileleyen süreçte elden geçir kodu

    # dizi.pop(0)
    # dizi.pop(0)   bunları diğer durumlar içinde yazabilirsin düğümler yoksa diye

    geriDonus = backPath[-1]
    return dizi, dugum, dogruYol, geriDonus


def dugumNoktalari(x1, y1, dugum):
    deger = []
    for i in dugum:
        x, y = x1, y1
        if (i == 0):

            x, y = x - 1, y + 1
            deger.append([x, y])



        elif (i == 1):

            x, y = x, y + 1

            deger.append([x, y])



        elif (i == 2):

            x, y = x + 1, y + 1
            deger.append([x, y])



        elif (i == 3):
            x, y = x + 1, y
            deger.append([x, y])



        elif (i == 4):
            x, y = x + 1, y - 1
            deger.append([x, y])



        elif (i == 5):
            x, y = x, y - 1
            deger.append([x, y])


        elif (i == 6):
            x, y = x - 1, y - 1
            deger.append([x, y])


        elif (i == 7):

            x, y = x - 1, y
            deger.append([x, y])

    return deger


def noDuplicateValue(list):
    s = []
    for i in list:
        if i not in s:
            s.append(i)

    return s


def dugumFiltre2(y, x, dugum):
    dizi = komsulukSaptama([y, x], dugum)

    gurultu = []
    for i in dizi:

        for j in dizi:

            y = abs(i[0] - j[0])
            x = abs(i[1] - j[1])

            if ([y, x] == [1, 0] and i[2] in [0, 2, 4, 6]):

                gurultu.append([i[0], i[1]])

            elif ([y, x] == [0, 1] and i[2] in [0, 2, 4, 6]):

                gurultu.append([i[0], i[1]])

    gurultu = noDuplicateValue(gurultu)
    for i in range(len(dizi)):
        dizi[i].pop(2)

    for i in gurultu:
        dizi.remove(i)

    return dizi


def dugumFiltre(i1, j1, dugum):
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

    if (len(
            dugum) == 3 and res == 0):  # dugum sayısı 3 e eşit olduğunda ve geliş guzergahının sagında veya solunda dugumlerin oldugu durum (y   ekseni için) # dikkat et bu durum gerçekleştiğinde dugum sayısı 3 de olsa aralarındaki fark 0 olmuyor. fark sıfır olsa dugum sayısı == 2 olmuş oluyor

        kopru = 0


    elif (len(
            dugum) == 3 and res2 == 0):  # dugum sayısı 3 e eşit olduğunda ve geliş guzergahının altında veya ustunde dugumlerin oldugu durum (x ekseni için)

        kopru = 0


    elif (res > 1 or res2 > 1 or (res == 1 and res2 == 1)):

        dizi = dugumFiltre2(i1, j1, dugum)
        kopru = 1

    if (kopru == 0):

        for n in dugum:

            if ([i1, j1 + 1] == n):  # ----> 0

                dizi.append(n)


            elif ([i1 + 1, j1] == n):  # ----> 2

                dizi.append(n)


            elif ([i1, j1 - 1] == n):  # ----> 4

                dizi.append(n)

            elif ([i1 - 1, j1] == n):  # ----> 6

                dizi.append(n)

    return dizi


def dugumSonrası(dugum):
    for k in dugum:

        i, j = k
        for k in range(5):

            yon = []
            backPath = []

            if (thn[i - 1][j + 1] == 255 and [i - 1, j + 1] not in backPath[
                -1]):  # buralara dikkat et ve 255 değerine de

                yon.append(0)
                kopru = 0

            if (thn[i][j + 1] == 255 and [i, j + 1] not in backPath[
                -1]):  # burda bug var i,j dizinin ilk elamanını 0-0 yapıyorum ama etraflıca düşün
                yon.append(1)
                kopru = 1

            if (thn[i + 1][j + 1] == 255 and [i + 1, j + 1] not in backPath[-1]):
                yon.append(2)
                kopru = 2

            if (thn[i + 1][j] == 255 and [i + 1, j] not in backPath[-1]):
                yon.append(3)
                kopru = 3

            if (thn[i + 1][j - 1] == 255 and [i + 1, j - 1] not in backPath[-1]):
                yon.append(4)
                kopru = 4

            if (thn[i][j - 1] == 255 and [i, j - 1] not in backPath[-1]):
                yon.append(5)
                kopru = 5

            if (thn[i - 1][j - 1] == 255 and [i - 1, j - 1] not in backPath[-1]):
                yon.append(6)
                kopru = 6

            if (thn[i - 1][j] == 255 and [i - 1, j] not in backPath[-1]):
                yon.append(7)  # duvgum değikeninin adını yon olarak değiştir.
                kopru = 7


def yonSaptama(kopruDegerleri, katman):
    cıkısYonu = []
    katman.pop(-1)

    for i in range(len(katman) - 1, -1, -1):
        cıkısYonu.append(komsulukSaptama(kopruDegerleri[(len(kopruDegerleri)) - i - 1], katman[i]))


def komsulukSaptama(koordinat, dugum):
    i, j = koordinat
    yon = []

    for k in range(len(dugum)):

        araDeger = [dugum[k][0], dugum[k][1]]

        if ([i - 1, j + 1] == araDeger):  # buralara dikkat et ve 255 değerine de

            yon.append(0)
            dugum[k].append(0)
            kopru = 0
        elif ([i, j + 1] == araDeger):  # burda bug var i,j dizinin ilk elamanını 0-0 yapıyorum ama etraflıca düşün
            yon.append(1)

            dugum[k].append(1)
            kopru = 1

        elif ([i + 1, j + 1] == araDeger):
            yon.append(2)
            dugum[k].append(2)
            kopru = 2

        elif ([i + 1, j] == araDeger):
            yon.append(3)
            dugum[k].append(3)
            kopru = 3

        elif ([i + 1, j - 1] == araDeger):
            yon.append(4)
            dugum[k].append(4)
            kopru = 4

        elif ([i, j - 1] == araDeger):
            yon.append(5)
            dugum[k].append(5)
            kopru = 5

        elif ([i - 1, j - 1] == araDeger):
            yon.append(6)
            dugum[k].append(6)
            kopru = 6

        elif ([i - 1, j] == araDeger):
            yon.append(7)

            dugum[k].append(7)  # duvgum değikeninin adını yon olarak değiştir.
            kopru = 7

    return dugum


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

# sıralıSonuc([136,178],[[627,629]],[[[136,178],[137,179]]],thn) # oval
sıralıSonuc([108, 21], [[926, 1013]], [[[108, 20], [108, 21]]], thn)  # reall

# sıralıSonuc([48,28],[[143,257]],[[[48,28],[47,28]]],thn) # ilk
# sıralıSonuc([101,21],[[932,1013]],[[[101,20],[101,21]]],thn) # real
# sıralıSonuc([214,218],[[101,101]],[[[214,218],[214,219]]],thn) # 6.png
# sıralıSonuc([4,120],[[160,120]],[[[3,120],[4,120]]],thn) # 7.png


# sıralıSonuc([116,124],[[69,79]],[[[116,124],[116,125]]],thn) # bes.jpeg
# sıralıSonuc([61,57],[[69,79]],[[[61,57],[62,57]]],thn) # bes.jpeg
# sıralıSonuc([80,131],[[60,69]],[[[80,131],[81,131]]],thn) # bes.jpeg

# sıralıSonuc([76,119],[[60,69]],[[[76,119],[76,118]]],thn) # bes.jpeg


# sıralıSonuc([82,113],[[60,69]],[[[82,113],[82,114]]],thn) # bes.jpeg

# sıralıSonuc([115,147],[[52,115]],[[[115,147],[115,148]]],thn) # bes.jpeg # hatalı nokta tespiti

# sıralıSonuc([115,147],[[63,72]],[[[115,147],[115,148]]],thn) # bes.jpeg # hatalı nokta tespiti

# sıralıSonuc([85,117],[[49,52]],[[[85,117],[86,117]]],thn) # bes.jpeg


# sıralıSonuc([89,123],[[60,69]],[[[89,123],[89,124]]],thn) # bes.jpeg # 2. hata


# sıralıSonuc([95,130],[[60,69]],[[[95,130],[95,129]]],thn) # bes.jpeg  # hata 1.

# sıralıSonuc([135,164],[[69,79]],[[[135,164],[135,165]]],thn) # bes.jpeg
# sıralıSonuc([135,164],[[69,79]],[[[135,164],[135,165]]],thn)

# sıralıSonuc([5,360],[[754,397]],[[[5,360],[4,360]]],thn) # dort.png

# sıralıSonuc([3,144],[[312,176]],[[[2,144],[3,144]]],thn)
# sıralıSonuc([114,57],[[1012,933]],[[[114,56],[144,57]]],thn)

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
