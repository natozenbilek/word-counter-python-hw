# Introduction to Python, Ödev 5
# IEEE Hacettepe University Student Branch, Güz 2026
#
# Bu ödevin sonunda dict ve set ile sayabilecek, file'a yazıp file'dan
# okuyabilecek ve ilk derste söz verdiğimiz kahve falı programını kendiniz
# yazmış olacaksınız.
#
# Son teslim: 22 Kasım 2026 Pazar 23.59
# Teslim formu: https://forms.gle/GoDQP1oTpEdeC2RD6
# Ödev reposu: https://github.com/natozenbilek/word-counter-python-hw
#
# Ödevi nasıl yapacaksınız
# 1. Bu dosyayı python-kurs klasörünüze kaydedin ve PyCharm'da açın.
#    Bu haftanın kısa kod örnekleri ve turtle komutları reponun
#    README'sinde.
# 2. Her görevde "# TODO" satırının yerine kodunuzu yazın.
# 3. Görev 1, 3, 4 ve 5'te test satırları comment olarak duruyor. Kodunuzu
#    yazdıktan sonra bu satırları seçin ve Ctrl+/ (macOS: Cmd+/) ile açın.
# 4. Dosyayı Run ile çalıştırın. Her görevin başlık satırından sonraki
#    çıktısı, o görevin "Beklenen çıktı" kısmıyla birebir aynı olmalı.
#    Görev 5'in son adımı rastgele çalışır: orada satırların biçimi aynı
#    kalır, sayı ve fal her seferinde değişir.
# 5. Bitince formda "İsim" alanına isminizi yazın, odev5.py'yi "Ödev dosyası"
#    alanına yükleyin ve onay kutusunu işaretleyin. Söylemek istediğiniz bir
#    şey varsa isteğe bağlı "Açıklama" alanına yazın.
#
# Dosya bu haliyle de hatasız çalışır ve yalnızca görev başlıklarını yazar.
# Görev 5 Run penceresinde adınızı sorar; yazıp Enter'a basın. Fincan ayrı
# bir pencerede çizilir, o pencereyi kapatınca program biter.
# Program bu dosyanın yanına transcript.txt ve fal.txt yazar; PyCharm'ın
# Project penceresinde görünmezlerse File, Reload All from Disk deyin.
# File açarken her seferinde encoding="utf-8" yazın.
# Yalnızca Ders 1-5'te gördüğümüz yapıları kullanın.

import random
import turtle


print("=== 1. Dersi bul ===")
# Ders 4'teki transkript list'i, bu kez Ders 5'teki None ile.
# find_credits(transcript, code) adlı bir function yazın. transcript,
# (code, credits, letter) tuple'larından oluşan bir list'tir. Aranan ders
# transcript'te varsa function kredisini return etsin, yoksa None return
# etsin. Test satırları sonucu is None ile kontrol ediyor.
# TODO
#
# Test satırları (function'ı yazınca açın):
# courses = [("MAT123", 4, "C1"), ("FIZ127", 3, "B2"), ("BBM101", 3, "A3")]
# for wanted in ["FIZ127", "EEM101"]:
#     result = find_credits(courses, wanted)
#     if result is None:
#         print(wanted, "transkriptte yok")
#     else:
#         print(wanted, result, "kredi")
#
# Beklenen çıktı:
# FIZ127 3 kredi
# EEM101 transkriptte yok


print("=== 2. Kelime sayma ===")
text = "Bir berber bir berbere gel beraber bir berber dükkanı açalım demiş"
# a) text'i lower() ile küçük harfe çevirin ve split() ile words adlı bir
#    list'e ayırın.
# b) Derste gördüğümüz sayma kalıbıyla her kelimenin kaç kez geçtiğini
#    word_counts adlı bir dict'te sayın:
#    word_counts[word] = word_counts.get(word, 0) + 1
# c) items() ile dolaşın ve yalnızca birden çok geçen kelimeleri sayısıyla
#    yazdırın.
# d) Son satırda toplam kelime sayısını ve kaç farklı kelime olduğunu
#    len() ile yazdırın.
# TODO
#
# Beklenen çıktı:
# bir 3
# berber 2
# 11 kelime, 8 farklı kelime


print("=== 3. Alfabenin harfleri ===")
alphabet = "abcçdefgğhıijklmnoöprsştuüvyz"
# a) alphabet'teki 29 harfi for, range(len(alphabet)) ve add() ile
#    alphabet_set adlı bir set'e koyun: her turda alphabet[i] bir harftir.
# b) letters_of(sentence) adlı bir function yazın: sentence'ı lower() ile
#    küçük harfe çevirsin, onu da range(len()) ile dolaşıp alphabet_set'te
#    olan her karakteri yeni bir set'e eklesin ve bu set'i return etsin.
#    Boşluk alphabet_set'te olmadığı için dışarıda kalır.
# Test satırları -, & ve | ile eksik, ortak ve toplam harfleri sayıyor.
# İlk cümle bir pangram, yani alfabenin bütün harflerini kullanıyor.
# TODO
#
# Test satırları (kodunuzu yazınca açın):
# pangram = letters_of("Pijamalı hasta yağız şoföre çabucak güvendi")
# school = letters_of("Hacettepe Üniversitesi")
# major = letters_of("Bilgisayar Mühendisliği")
# print(len(alphabet_set), "harf")
# print(len(alphabet_set - pangram), "harf eksik")
# print(len(alphabet_set - school), "harf eksik")
# print(len(school & major), "ortak harf")
# print(len(school | major), "farklı harf")
#
# Beklenen çıktı:
# 29 harf
# 0 harf eksik
# 17 harf eksik
# 8 ortak harf
# 19 farklı harf


print("=== 4. Not dökümü dosyası ===")
lines = ["MAT123;4;C1", "FIZ127;3;B2", "BBM101;3;F3",
         "TKD103;2;A2", "BBM101;3;A3"]
# a) transcript.txt'yi "w" ile açın ve lines'taki her satırı ayrı bir satır
#    olarak yazın. write() satır sonu eklemez; her satırın sonuna "\n"
#    karakterini siz ekleyin.
# b) read_grades(file_name) adlı bir function yazın. file_name adlı file'ı
#    with open() ile satır satır okusun; her satırı strip() ile temizleyip
#    split(";") ile code, credits ve grade'e ayırsın ve
#    latest_grade[code] = grade ile bir dict'e koysun. BBM101 iki kez
#    geçiyor; son not geçerlidir. Function bu dict'i return etsin.
#    File yoksa program traceback vermesin: FileNotFoundError'ı yakalayıp
#    "<file'ın adı> bulunamadı" yazsın ve boş dict'i return etsin.
# TODO
#
# Test satırları (kodunuzu yazınca açın):
# grades = read_grades("transcript.txt")
# print(grades)
# print(len(grades), "ders")
# old = read_grades("transcript_2025.txt")
# print(len(old), "ders")
#
# Beklenen çıktı:
# {'MAT123': 'C1', 'FIZ127': 'B2', 'BBM101': 'A3', 'TKD103': 'A2'}
# 4 ders
# transcript_2025.txt bulunamadı
# 0 ders


print("=== 5. Kahve falı ===")
# İlk derste söz verdiğimiz program: ekrana bir kahve fincanı çizen, içine
# telve serpen ve falınıza bakan program. Fincanı çizen kısım hazır; siz üç
# adımda telveyi serpip falı okuyacaksınız. Fincanın merkezi (0, 0)
# noktasıdır: x büyüdükçe sağa, y büyüdükçe yukarı gidilir.
CUP_RADIUS = 150
HANDLE_RADIUS = 40
RIM_WIDTH = 10
TELVE_RADIUS = 130  # the dots stay inside the rim
DOT_COUNT = 100

# Her çeyreğin üç falı var; isterseniz kendi fallarınızı yazın.
FORTUNES = {
    "sağ üst": [
        "Önünüzde bir yol var: Beytepe ringi sizi bekliyor.",
        "Üç vakte kadar bir yolculuk: kütüphaneden kantine.",
        "Bir merdiven görüyorum; derse yine de yetişeceksiniz.",
    ],
    "sol üst": [
        "Bir kuş görüyorum, ağzında güzel bir e-posta var.",
        "Grupta biri 'ödev ne zamandı?' diye soracak.",
        "Bu hafta yemekhanede sevdiğiniz yemek çıkacak.",
    ],
    "sol alt": [
        "Bir yılan görüyorum; korkmayın, bu Python.",
        "Bir error message geliyor; sonuna kadar okuyun.",
        "Fincanın dibinde dört boşluk var; girintiniz kaymayacak.",
    ],
    "sağ alt": [
        "Kütüphanede prizin yanında boş bir masa bulacaksınız.",
        "Kantinde uzun bir kuyruk var ama sıra size çabuk gelecek.",
        "Fincanda bir fincan daha var: ikinci kahve yolda.",
    ],
}


def draw_circle(x, y, radius):
    # turtle.circle() draws around a centre that is radius above the turtle
    turtle.penup()
    turtle.goto(x, y - radius)
    turtle.pendown()
    turtle.circle(radius)
    turtle.penup()


def draw_cup():
    # The cup seen from above: a ring for the cup, a small ring for the handle
    turtle.speed(0)
    turtle.hideturtle()
    draw_circle(0, 0, CUP_RADIUS)
    draw_circle(0, 0, CUP_RADIUS - RIM_WIDTH)
    handle_x = CUP_RADIUS + HANDLE_RADIUS
    draw_circle(handle_x, 0, HANDLE_RADIUS)
    draw_circle(handle_x, 0, HANDLE_RADIUS - RIM_WIDTH)


# a) find_quarter(x, y) adlı bir function yazın: (x, y) noktası fincanın
#    hangi çeyreğindeyse onun adını return etsin: "sağ üst", "sol üst",
#    "sol alt" ya da "sağ alt". x = 0 sağ, y = 0 üst sayılsın.
# TODO
#
# Test satırları (function'ı yazınca açın):
# print(find_quarter(30, 40))
# print(find_quarter(-30, 40))
# print(find_quarter(-30, -40))
# print(find_quarter(30, -40))
# print(find_quarter(0, 0))
#
# Beklenen çıktı:
# sağ üst
# sol üst
# sol alt
# sağ alt
# sağ üst

# b) busiest_quarter(counts) adlı bir function yazın. counts, her çeyreğin
#    adını o çeyrekteki nokta sayısına eşleyen bir dict'tir. Function, en
#    çok noktası olan çeyreğin adını return etsin. Şimdiye kadarki en
#    kalabalık çeyreği best adlı bir isimde tutun ("sağ üst" ile başlayın);
#    items() ile dolaşın ve daha kalabalık bir çeyrek görünce best'i
#    değiştirin. İki çeyrek eşitse önce gelen kalsın.
# TODO
#
# Test satırları (function'ı yazınca açın):
# sample = {"sağ üst": 21, "sol üst": 23, "sol alt": 40, "sağ alt": 16}
# print(busiest_quarter(sample))
# tie = {"sağ üst": 30, "sol üst": 30, "sol alt": 20, "sağ alt": 20}
# print(busiest_quarter(tie))
#
# Beklenen çıktı:
# sol alt
# sağ üst

# c) Programın kendisi. Sırayla:
#    1. name = input("Adınız: ").strip() ile adı sorun, sonra draw_cup()
#       ile fincanı çizin.
#    2. quarter_counts adlı bir dict'i dört çeyreğin adı ve 0 ile kurun.
#       Sonra while ile fincana DOT_COUNT kadar, yani 100 nokta serpin.
#       Her turda rastgele bir nokta seçin:
#           dot_x = random.randint(-TELVE_RADIUS, TELVE_RADIUS)
#           dot_y = random.randint(-TELVE_RADIUS, TELVE_RADIUS)
#       -TELVE_RADIUS, -130 demektir: x ve y -130 ile 130 arasında seçilir.
#       Nokta fincanın içindeyse, yani
#       dot_x ** 2 + dot_y ** 2 < TELVE_RADIUS ** 2 ise:
#       - turtle.goto(dot_x, dot_y) ile oraya gidin;
#       - turtle.dot(random.randint(4, 10), "brown") ile noktayı koyun;
#       - find_quarter() ile noktanın çeyreğini bulup quarter_counts'ta o
#         çeyreği bir artırın; dict'i 0'larla kurduğunuz için += yeter;
#       - serpilen noktaları sayan sayacı bir artırın.
#       Fincanın dışına düşen nokta sayılmaz; döngü yeni bir nokta seçer.
#    3. busiest = busiest_quarter(quarter_counts) ile en kalabalık çeyreği
#       bulun. options = FORTUNES[busiest] üç fallık bir list; içinden
#       birini rastgele bir index ile seçin:
#       fortune = options[random.randint(0, len(options) - 1)]
#    4. Örnek çıktıda "Adınız" satırından sonraki üç satırı yazdırın;
#       sayıyı quarter_counts[busiest]'ten alın. Falı fal.txt'nin sonuna
#       "a" ile ekleyin: f.write(f"{name}: {fortune}\n"). Sonra son iki
#       satırı yazdırın.
#    5. En son turtle.done() yazın: fincan penceresi siz kapatana kadar
#       açık kalır.
# TODO
#
# Örnek çıktı (Mehmet yazınca; telve her çalıştırmada başka yere düştüğü
# için sayı ve fal değişir, satırların biçimi aynı kalır):
# Adınız: Mehmet
# Telvenin çoğu sol alt çeyrekte: 40 tane.
# Mehmet, falınız şöyle:
# Bir yılan görüyorum; korkmayın, bu Python.
# Bu fal, fal.txt dosyasının sonuna eklendi.
# Falınıza bir sayaç ile bir if baktı; tutarsa tesadüf.
# Fincan penceresinde kulplu bir fincan ve içinde 100 kahverengi nokta
# görünür.


print("=== Meraklısına ===")
# Zorunlu değil. Görev 5'teki fincan penceresini kapatınca çalışır.
# fal.txt'nin her satırı "ad: fal" biçiminde. Dosyayı okuyun; kaç fala
# bakıldığını ve kaç farklı kişiye bakıldığını yazdırın. Kişileri bir
# set'te toplayın: her satırda ad, split(": ") ile ayrılan ilk parçadır.
# TODO
#
# Beklenen çıktı (fal.txt yokken, ilk çalıştırmada):
# 1 fal, 1 kişi
# Dosyayı sonra Zehra ve yine Mehmet adıyla iki kez daha çalıştırırsanız
# son çalıştırma 3 fal, 2 kişi yazar.
