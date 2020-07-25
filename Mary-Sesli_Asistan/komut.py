import webbrowser
from random import choice
import sys
import requests
from bs4 import BeautifulSoup
from datetime import datetime
import sqlite3
import os
import base64
import io
from PIL import Image


class Veritabani():
    def adDegistir(self,isim):
        self.db = sqlite3.connect('database.sqlite')
        self.imlec = self.db.cursor()
        self.imlec.execute(f"UPDATE kullanici SET isim='{isim}'")
        self.db.commit() 
        self.db.close()

    def ad(self):
        self.db = sqlite3.connect('database.sqlite')
        self.imlec = self.db.cursor()
        self.imlec.execute("SELECT * FROM kullanici")
        isim = self.imlec.fetchone()
        self.db.close()
        return isim[0]

class komutlar():
    def __init__(self,gelenSes):
        self.ses = gelenSes
        self.buyukHarf = self.ses.upper()
        self.buyukHarfBlok = self.buyukHarf.split()
        self.sesBloklari = self.ses.split()
        print(self.sesBloklari)
        self.cevapVerildi = False
        self.db = Veritabani()
        self.googleTemizle = ["GOOGLE'DA", "HAKKINDA", "IÇIN", "ARAMA", "ARA", "YAP", "AÇ", "ADLI"]
        self.youtubeTemizle = ["AÇAR"," MISIN"," HAKKINDA","ARAR","ARA","İÇİN","AÇ","ADLI","YOUTUBE'DA","ŞARKISINI","MÜZIĞINI","MUZIĞI","ŞARKIYI","ŞARKI","VIDEOYU","VIDEO","PARÇAYI","PARÇASINI","YOUTUBE"]
        self.youtubeKelime = ["YOUTUBE'DA","YOUTUBE'DAN","ŞARKISINI","MÜZIĞINI","ŞARKIYI","VIDEO","VIDEOYU","PARÇASINI","PARÇAYI","YOUTUBE","VIDEOSUNU"]
        self.yanitlikomut = ["ad", "adonay", "ilkacilis"]
        self.labelText = " "
        self.emojisil = False
        self.yapilanislem = ""
        self.foto = False

    def listToStringGoogle(self,s):
        str1 = "+"
        return (str1.join(s))

    def listToString(self,s):
        str1 = " "
        return (str1.join(s))

    def seslendirilecek(self, yazi):
        self.cevapVerildi = True
        if self.labelText == " ":
            self.labelText = yazi

        if self.emojisil == True:
            self.seslendirilecektext = yazi
            self.seslendirilecektext = self.seslendirilecektext[:-1]
        else:
            self.seslendirilecektext = yazi
        print(self.seslendirilecektext)

    def yanitliIslemBul(self):
        if self.yapilanislem == "ilkacilis":
            self.adKayit()
            self.yapilanislem = "ad"

        if self.yapilanislem == "ad":
            self.adKayit()
            self.yapilanislem = "adonay"

        elif "EVET" in self.buyukHarfBlok or "OLUR" in self.buyukHarfBlok or "TAMAM" in self.buyukHarfBlok or "ONAYLIYORUM" in self.buyukHarfBlok or "DOĞRU" in self.buyukHarfBlok:
            if self.yapilanislem == "adonay":
                self.adKayitOnay()
                self.yapilanislem = ""

        elif "HAYIR" in self.buyukHarfBlok:
            if self.yapilanislem == "adonay":
                self.seslendirilecek("Peki, Sana nasıl hitap etmemi istersin ?")
                self.yapilanislem = "ad"
        else:
            if self.yapilanislem == "adonay":
                self.seslendirilecek("Lütfen sadece evet yada hayır diyin")
            else:
                self.yapilanislem = ""

    def cokKullanılanlar(self):
        if self.cevapVerildi == False:
            if "HABERTÜRK" in self.buyukHarf or "HABERTURK" in self.buyukHarf:
                if "WIKIPEDIA" not in self.buyukHarf or "NEDIR" not in self.buyukHarf or "KIMDIR" not in self.buyukHarf:
                    self.websiteAc()

        if self.cevapVerildi == False:
            if "YEMEK SEPETI" in self.buyukHarf or "YEMEKSEPETI" in self.buyukHarf:
                if "WIKIPEDIA" not in self.buyukHarf and "NEDIR" not in self.buyukHarf and "KIMDIR" not in self.buyukHarf:
                    self.websiteAc()

        if self.cevapVerildi == False:
            if "WIKIPEDIA" in self.buyukHarf:
                if "NEDIR" not in self.buyukHarf and "KIMDIR" not in self.buyukHarf:
                    self.websiteAc()

        if self.cevapVerildi == False:
            if "FACEBOOK" in self.buyukHarf and "AÇ" in self.buyukHarf:
                if "WIKIPEDIA" not in self.buyukHarf and "NEDIR" not in self.buyukHarf and "KIMDIR" not in self.buyukHarf:
                    webbrowser.open_new_tab("https://www.facebook.com/")
                    self.seslendirilecek("Senin için Facebook.com'u açtım")

        if self.cevapVerildi == False:
            if "HAVA DURUMU" == self.buyukHarf or "HAVA KAÇ DERECE" == self.buyukHarf or "HAVA NASIL" == self.buyukHarf:
                if "WIKIPEDIA" not in self.buyukHarf and "NEDIR" not in self.buyukHarf and "KIMDIR" not in self.buyukHarf:
                    self.havadurumu()

        if self.cevapVerildi == False:
            if "YOUTUBE'U AÇ" == self.buyukHarf or "YOUTUBE AÇ" == self.buyukHarf or "YOUTUBE.COM AÇ" == self.buyukHarf:
                if "WIKIPEDIA" not in self.buyukHarf and "NEDIR" not in self.buyukHarf and "KIMDIR" not in self.buyukHarf:
                    webbrowser.open_new_tab("https://www.youtube.com/")
                    self.seslendirilecek("Senin için Youtube'u açtım")

        if self.cevapVerildi == False:
            if "GOOGLE AÇ" == self.buyukHarf or "GOOGLE'I AÇ" == self.buyukHarf or "GOOGLE.COM AÇ" == self.buyukHarf or "GOOGLE.COM U AÇ" == self.buyukHarf:
                if "WIKIPEDIA" not in self.buyukHarf and "NEDIR" not in self.buyukHarf and "KIMDIR" not in self.buyukHarf:
                    webbrowser.open_new_tab("https://www.google.com/")
                    self.seslendirilecek("Senin için Google'ı açtım")

        if self.cevapVerildi == False:
            if "ITOPYA" in self.buyukHarf:
                if "WIKIPEDIA" not in self.buyukHarf and "NEDIR" not in self.buyukHarf and "KIMDIR" not in self.buyukHarf:
                    self.websiteAc()

        if self.cevapVerildi == False:
            if "VATAN" in self.buyukHarf or "BILGISAYAR" in self.buyukHarf:
                if "WIKIPEDIA" not in self.buyukHarf and "NEDIR" not in self.buyukHarf and "KIMDIR" not in self.buyukHarf:
                    self.websiteAc()

        if self.cevapVerildi == False:
            if "SAHIBINDEN" in self.buyukHarfBlok:
                if "WIKIPEDIA" not in self.buyukHarf and "NEDIR" not in self.buyukHarf and "KIMDIR" not in self.buyukHarf:
                    self.websiteAc()

        if self.cevapVerildi == False:
            if "BORSA" in self.buyukHarf or "HISSE" in self.buyukHarf:
                if "WIKIPEDIA" not in self.buyukHarf and "NEDIR" not in self.buyukHarf and "KIMDIR" not in self.buyukHarf:
                    self.websiteAc()

        if self.cevapVerildi == False:
            if "HABER" in self.buyukHarf:
                if "WIKIPEDIA" not in self.buyukHarf and "NEDIR" not in self.buyukHarf and "KIMDIR" not in self.buyukHarf and "NE" not in self.buyukHarf:
                    self.websiteAc()

        if self.cevapVerildi == False:
            if "EKŞİ" in self.buyukHarf:
                if "WIKIPEDIA" not in self.buyukHarf and "NEDIR" not in self.buyukHarf and "KIMDIR" not in self.buyukHarf:
                    self.websiteAc()

        if self.cevapVerildi == False:
            if "MÜZIK" in self.buyukHarf:
                if "WIKIPEDIA" not in self.buyukHarf and "NEDIR" not in self.buyukHarf and "KIMDIR" not in self.buyukHarf:
                    self.websiteAc()

        if self.cevapVerildi == False:
            if "INCE" in self.buyukHarf and "HESAP" in self.buyukHarf:
                if "WIKIPEDIA" not in self.buyukHarf and "NEDIR" not in self.buyukHarf and "KIMDIR" not in self.buyukHarf:
                    self.websiteAc()

        if self.cevapVerildi == False:
            if "N11" in self.buyukHarf:
                if "WIKIPEDIA" not in self.buyukHarf and "NEDIR" not in self.buyukHarf and "KIMDIR" not in self.buyukHarf:
                    self.websiteAc()

        if self.cevapVerildi == False:
            if "ÇIÇEKSEPETI" in self.buyukHarf or "ÇIÇEK" in self.buyukHarf and "SEPETI" in self.buyukHarf:
                if "WIKIPEDIA" not in self.buyukHarf and "NEDIR" not in self.buyukHarf and "KIMDIR" not in self.buyukHarf:
                    self.websiteAc()

        if self.cevapVerildi == False:
            if "GOOGLE" in self.buyukHarf and "TRANSLATE" in self.buyukHarf or "ÇEVIRI" in self.buyukHarf:
                if "WIKIPEDIA" not in self.buyukHarf and "NEDIR" not in self.buyukHarf and "KIMDIR" not in self.buyukHarf:
                    self.websiteAc()

        if self.cevapVerildi == False:
            if "TEKNOSA" in self.buyukHarf:
                if "WIKIPEDIA" not in self.buyukHarf and "NEDIR" not in self.buyukHarf and "KIMDIR" not in self.buyukHarf:
                    self.websiteAc()

        if self.cevapVerildi == False:
            if "INSTAGRAM" in self.buyukHarf:
                if "WIKIPEDIA" not in self.buyukHarf and "NEDIR" not in self.buyukHarf and "KIMDIR" not in self.buyukHarf:
                    webbrowser.open_new_tab("https://www.instagram.com/")
                    self.seslendirilecek("Senin için Google'ı açtım")

        if self.cevapVerildi == False:
            if "WHATSAPP" in self.buyukHarf:
                if "WIKIPEDIA" not in self.buyukHarf and "NEDIR" not in self.buyukHarf and "KIMDIR" not in self.buyukHarf and "PROGRAM" not in self.buyukHarf and "UYGULAMA" not in self.buyukHarf:
                    webbrowser.open_new_tab("https://web.whatsapp.com/")
                    self.seslendirilecek("Senin için Whatsapp'ı açtım")

        if self.cevapVerildi == False:
            if "LETGO" in self.buyukHarf:
                if "WIKIPEDIA" not in self.buyukHarf and "NEDIR" not in self.buyukHarf and "KIMDIR" not in self.buyukHarf:
                    self.websiteAc()

        if self.cevapVerildi == False:
            if "ALTIN" in self.buyukHarf and "FIYAT" in self.buyukHarf:
                if "WIKIPEDIA" not in self.buyukHarf and "NEDIR" not in self.buyukHarf and "KIMDIR" not in self.buyukHarf:
                    webbrowser.open_new_tab("http://bigpara.hurriyet.com.tr/altin/")
                    self.seslendirilecek("Senin için altın fiyatlarını açtım")

        if self.cevapVerildi == False:
            if "HEPSIBURADA" in self.buyukHarf:
                if "WIKIPEDIA" not in self.buyukHarf and "NEDIR" not in self.buyukHarf and "KIMDIR" not in self.buyukHarf:
                    self.websiteAc()

        if self.cevapVerildi == False:
            if "NOKTA COM" in self.buyukHarf or ".COM" in self.buyukHarf or "NOKTA NET" in self.buyukHarf or ".NET" in self.buyukHarf:
                if "WIKIPEDIA" not in self.buyukHarf and "NEDIR" not in self.buyukHarf and "KIMDIR" not in self.buyukHarf:
                    self.websiteAc()

        if self.cevapVerildi == False:
            if "HEPSIBURADA" in self.buyukHarf:
                if "WIKIPEDIA" not in self.buyukHarf and "NEDIR" not in self.buyukHarf and "KIMDIR" not in self.buyukHarf:
                    self.websiteAc()

        if self.cevapVerildi == False:
            if "D&R" in self.buyukHarf:
                if "WIKIPEDIA" not in self.buyukHarf and "NEDIR" not in self.buyukHarf and "KIMDIR" not in self.buyukHarf:
                    self.websiteAc()

        if self.cevapVerildi == False:
            if "ÇEVIR" in self.buyukHarf or "INGILIZCE" in self.buyukHarf or "TÜRKÇE" in self.buyukHarf:
                if "WIKIPEDIA" not in self.buyukHarf and "NEDIR" not in self.buyukHarf and "KIMDIR" not in self.buyukHarf:
                    self.googleAra()

        if self.cevapVerildi == False:
            if "NEDIR" in self.buyukHarf or "KIMDIR" in self.buyukHarf:
                self.googleAra()


    def islemBul(self,islem):
        self.yapilanislem = islem
        if self.cevapVerildi == False:
            if self.yapilanislem in self.yanitlikomut:
                self.yanitliIslemBul()

        if self.cevapVerildi == False:
            self.cokKullanılanlar()

        if self.cevapVerildi == False:
            self.sohbet(self.buyukHarf)

        if self.cevapVerildi == False:
            if "BANA" in self.buyukHarfBlok and  "HITAP" in self.buyukHarfBlok or "ADIM" in self.buyukHarfBlok:
                self.adKayit()
                self.yapilanislem = "adonay"

        if self.cevapVerildi == False:
            if "DERECE" in self.buyukHarfBlok or "HAVA" in self.buyukHarfBlok:
                self.havadurumu()

        if self.cevapVerildi == False:
            if "TARIH" in self.buyukHarfBlok or "BUGÜNÜN" in self.buyukHarfBlok or "AYIN" in self.buyukHarfBlok or "GÜNLERDEN" in self.buyukHarfBlok or "BUGÜN" in self.buyukHarfBlok or "GÜNLERDEN" in self.buyukHarfBlok:
                if "TARIHI" in self.buyukHarfBlok or "KAÇI" in self.buyukHarfBlok or "NE" in self.buyukHarfBlok:
                    self.tarih()

        if self.cevapVerildi == False:
            if "SAAT KAÇ" == self.buyukHarf or "ŞUAN SAAT KAÇ" == self.buyukHarf:
                self.saat()

        if self.cevapVerildi == False:
            for youtube in self.youtubeKelime:
                if youtube in self.buyukHarfBlok:
                    self.youtubeAc()

        if self.cevapVerildi == False:
            if "SITE" in self.buyukHarfBlok or "WEB" in self.buyukHarf or "SITESINI" in self.buyukHarfBlok:
                self.websiteAc()

        if self.cevapVerildi == False:
            self.programAc()

        if self.cevapVerildi == False:
            self.googleAra()


    def websiteAc(self,soup=None):
        temizlenecek = ["WEB","SITESINI", "ADLI", "SITEYI", "AÇ"]
        for i in temizlenecek:
            if i in self.buyukHarfBlok:
                indexnumara = self.buyukHarfBlok.index(i)
                self.sesBloklari.pop(indexnumara)
                self.buyukHarfBlok.pop(indexnumara)
        try:
            if soup == None:
                wikilink = "https://www.google.com/search?q=" + self.listToStringGoogle(self.sesBloklari)
                headersparam = {
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36"}
                r = requests.get(wikilink, headers=headersparam)
                soup = BeautifulSoup(r.content, "lxml")
            link = soup.find("div", attrs={"class": "r"}).find("a").get("href")
            print(link)
            webbrowser.open_new_tab(link)
            random = ["Tamamdır, istediğin websitesini açtım","İstediğin siteyi açtım 👍",f"İstediğin websitesini açtım {self.db.ad()}"]
            cumle = choice(random)
            if cumle is random[1]:self.emojisil = True
            self.seslendirilecek(cumle)
        except AttributeError:
            self.seslendirilecek("Şuan internetle bağlantı kuramıyorum")


    def programAc(self):
        index = None
        lnkfile_path = []
        lnkfile_name = []
        for dirpath, subdirs, files in os.walk("C:\ProgramData\Microsoft\Windows\Start Menu\Programs"):
            for x in files:
                if x.endswith(".lnk"):
                    lnkfile_path.append(os.path.join(dirpath, x))
                    lnkfile_name.append(x.replace(".lnk", ""))

        for dirpath, subdirs, files in os.walk(
                r'C:\Users\{}\AppData\Roaming\Microsoft\Windows\Start Menu\Programs'.format(os.getlogin())):
            for x in files:
                if x.endswith(".url"):
                    lnkfile_path.append(os.path.join(dirpath, x))
                    lnkfile_name.append(x.replace(".url", ""))

                for x in files:
                    if x.endswith(".lnk"):
                        lnkfile_path.append(os.path.join(dirpath, x))
                        lnkfile_name.append(x.replace(".lnk", ""))

        for dirpath, subdirs, files in os.walk(
                r'C:\Users\{}\AppData\Local\Microsoft\WindowsApps'.format(os.getlogin())):
            for x in files:
                if x.endswith(".exe"):
                    lnkfile_path.append(os.path.join(dirpath, x))
                    lnkfile_name.append(x.replace(".exe", ""))

        ekTemizlenecek = ["'U","'I","'YU"]
        for a in ekTemizlenecek:
            if a in self.buyukHarf:
                index = self.buyukHarf.find(a)
                self.ses = self.listToString(self.sesBloklari)[0:index:]
                self.sesBloklari = self.ses.split()
                self.buyukHarfBlok = self.ses.upper().split()

        for name in lnkfile_name:
            for kelime in self.buyukHarfBlok:
                if kelime in name.upper().split():
                    if self.cevapVerildi == False:
                        index = lnkfile_name.index(name)
                        os.startfile(lnkfile_path[index])
                        random = [f"İstediğin {name} adlı programı açtım", f"{name} programını açtım"]
                        random = choice(random)
                        self.seslendirilecek(random)

        if self.cevapVerildi == False:
            if "PROGRAM" in self.buyukHarf or "UYGULAMA" in self.buyukHarf:
                self.emojisil = True
                self.seslendirilecek("Üzgünüm söylediğin programı bilgisayarında bulamadım 😓")

        elif self.cevapVerildi == False:
            if "AÇ" in self.buyukHarfBlok:
                self.seslendirilecek('Neyi açmam gerektiğinden tam emin değilim.\nEğer söylediğin bir web site ise "Youtube sitesini aç" şeklinde söyleyebilirsin')

    def havadurumu(self):
        headersparam = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36"}
        if "HAFTALIK" in self.buyukHarf:
            self.websiteAc()
        else:
            wikilink = "https://www.google.com/search?q="+self.listToStringGoogle(self.sesBloklari)
            r = requests.get(wikilink, headers=headersparam)
            soup = BeautifulSoup(r.content, "lxml")

            detaybox = soup.find("div", attrs={"class": "vk_gy vk_sh wob-dtl"}).find_all("div")
            self.detay1 = detaybox[0].text
            self.detay2 = detaybox[1].text
            self.detay3 = detaybox[2].text
            if detaybox[2].find("span", attrs={"id": "wob_tws"}).text in self.detay3:
                self.detay3 = self.detay3.replace(detaybox[2].find("span", attrs={"id": "wob_tws"}).text, "")

            tumsehir = soup.find("div", attrs={"class": "vk_gy vk_h"}).text
            sehir = tumsehir.split(",")[0]
            derece = soup.find("span", attrs={"class": "wob_t"}).text
            gun = soup.find("div", attrs={"id": "wob_dts"}).text
            durum = soup.find("span", attrs={"class": "vk_gy vk_sh"}).text
            if durum == "Bazı bölgelerde sağanak yağış":
                durum = "Yer yer sağnak yağışlı"
            self.labelText = "<font size=2>{}</font><br/><font size=2>{}</font><br/><font size=1>{}</font><br/><font size=5>{}°C</font>".format(tumsehir, gun, durum, derece)

            if "HAVA DURUMU" == self.buyukHarf or "HAVA NASIL" == self.buyukHarf or "HAVA KAÇ DERECE" == self.buyukHarf:
                self.seslendirilecek(sehir + " için şuan hava " + derece + " derece " + durum)
            elif "YARIN" in self.buyukHarf:
                self.seslendirilecek(sehir + " için yarın hava " + derece + " derece " + durum + " olacak")
            else:
                self.seslendirilecek(sehir+ " için hava tahmini şu şekilde")

            try:
                resimlink = soup.find("div", attrs={"id": "wob_d"}).find("img").get("src")
                resimlink = "http://" + resimlink[2:]
                resim = requests.get(resimlink)
                if resim.status_code == 200:
                    self.foto = True
                    self.width = 80
                    self.height = 80
                    self.yapilanislem = "havadurumu"
                    with open("image/image.jpg", 'wb') as f:
                        f.write(resim.content)
                else:
                    self.websiteAc(soup)
            except AttributeError:
                self.websiteAc(soup)


    def adKayit(self):
        temizlenecek = ["BENIM", "ADIM", "ISMIM", "ŞEKLINDE", "HITAP", "ET","SOYADIM"]
        for i in temizlenecek:
            if i in self.buyukHarfBlok:
                indexnumara = self.buyukHarfBlok.index(i)
                self.sesBloklari.pop(indexnumara)
                self.buyukHarfBlok.pop(indexnumara)
        global ad
        ad = self.listToString(self.sesBloklari).split()[0]
        self.seslendirilecek(f"Peki, Sana {ad} diyeceğim tamam mı?")

    def adKayitOnay(self):
        temizlenecek = ["BENIM", "ADIM", "ISMIM", "ŞEKLINDE", "HITAP", "ET","SOYADIM"]
        for i in temizlenecek:
            if i in self.buyukHarfBlok:
                indexnumara = self.buyukHarfBlok.index(i)
                self.sesBloklari.pop(indexnumara)
                self.buyukHarfBlok.pop(indexnumara)
        global ad
        db = Veritabani()
        db.adDegistir(ad)
        self.seslendirilecek(f"Tamam, Bundan sonra sana {db.ad()} diyeceğim")

    def saat(self):
        zaman = datetime.now()
        saat = str(zaman.hour)
        dakika = str(zaman.minute)
        for i in range(1,10):
            if i == int(dakika):
                dakika = "0"+dakika
        self.seslendirilecek("Saat "+saat+":"+dakika)

    def tarih(self):
        tarih = datetime.now()
        gun = str(tarih.day)
        ay = str(tarih.month)
        yil = str(tarih.year)
        if ay == "1": ay = ay.replace("1","Ocak")
        if ay == "2": ay = ay.replace("2", "Şubat")
        if ay == "3": ay = ay.replace("3", "Mart")
        if ay == "4": ay = ay.replace("4", "Nisan")
        if ay == "5": ay = ay.replace("5", "Mayıs")
        if ay == "6": ay =  ay.replace("6", "Haziran")
        if ay == "7": ay = ay.replace("7", "Temmuz")
        if ay == "8": ay = ay.replace("8", "Ağustos")
        if ay == "9": ay = ay.replace("9", "Eylül")
        if ay == "10": ay = ay.replace("10", "Ekim")
        if ay == "11": ay = ay.replace("11", "Kasım")
        if ay == "12": ay = ay.replace("12", "Aralık")
        random = ["Bugünün tarihi "+gun+" "+ay+ " "+yil,
                  "Bugün "+gun+" "+ay+ " "+yil]
        random = choice(random)
        self.seslendirilecek(random)

    def googleFoto(self,soup):##Wikipedia fotoğrafları
        if self.solbilgi:
            try:
                self.height = int(soup.find("div", attrs={"class": "eoNQle mod NFQFxe RsqAUb"}).find("img").get("height"))
                self.width = int(soup.find("div", attrs={"class": "eoNQle mod NFQFxe RsqAUb"}).find("img").get("width"))
                fotoid = soup.find("div", attrs={"class": "eoNQle mod NFQFxe RsqAUb"}).find("img").get("id")
                kodlar = soup.find_all("script")
                for i in kodlar:
                    if fotoid in str(i):
                        index = kodlar.index(i)
            except AttributeError:
                self.foto = False
                index = None

        elif self.solbilgi2:
            try:
                self.height = int(soup.find("div", attrs={"class": "kno-fiu kno-liu"}).find("img").get("height"))
                self.width = int(soup.find("div", attrs={"class": "kno-fiu kno-liu"}).find("img").get("width"))
                fotoid = soup.find("div", attrs={"class": "kno-fiu kno-liu"}).find("img").get("id")
                kodlar = soup.find_all("script")
                for i in kodlar:
                    if fotoid in str(i):
                        index = kodlar.index(i)
            except AttributeError:
                self.foto = False
                index = None

        else:
            try:
                self.height = int(soup.find("div", attrs={"class": "liYKde rhsvw g"}).find("img").get("height"))
                self.width = int(soup.find("div", attrs={"class": "liYKde rhsvw g"}).find("img").get("width"))
                fotoid = soup.find("div", attrs={"class": "cLjAic"}).find("img").get("id")
                kodlar = soup.find_all("script")
                for i in kodlar:
                    if fotoid in str(i):
                        index = kodlar.index(i)
            except AttributeError:
                try:
                    self.height = int(soup.find("div", attrs={"class": "liYKde rhsvw g"}).find("img").get("height"))
                    self.width = int(soup.find("div", attrs={"class": "liYKde rhsvw g"}).find("img").get("width"))
                    fotoid = soup.find("div", attrs={"class": "eoNQle mod NFQFxe RsqAUb"}).find("img").get("id")
                    print(fotoid)
                    kodlar = soup.find_all("script")
                    for i in kodlar:
                        if fotoid in str(i):
                            index = kodlar.index(i)
                except AttributeError:
                    self.foto = False
                    index = None

        if index is not None:
            try:
                resimKod = str(kodlar[index])
                resimKod = resimKod[resimKod.find("data:image/jpeg;base64,"):resimKod.find("';var")]
                if "x3d" in resimKod[len(resimKod) - 3:]:
                    resimKod = resimKod[:-4]
                if "x3d" in resimKod[len(resimKod) - 3:]:
                    resimKod = resimKod[:-4]
                print("Temiz resim:"+resimKod)
                Image.open(io.BytesIO(base64.b64decode(resimKod[resimKod.find('/9'):] + '=' * (-len(resimKod) % 4)))).save('image/image.jpg')
                self.foto = True
            except Image.UnidentifiedImageError:
                self.foto = False
        else:
            self.foto = False

    def googleAra(self):
        temizcumle = self.sesBloklari
        for temizlenecek in self.googleTemizle:
            if temizlenecek in self.buyukHarfBlok:
                indexnumara = self.buyukHarfBlok.index(temizlenecek)
                temizcumle.pop(indexnumara)
                self.buyukHarfBlok.pop(indexnumara)
        strtemizcumle = self.listToString(temizcumle)
        google = self.listToStringGoogle(temizcumle)

        if "WEB" in self.buyukHarf or "GOOGLE" in self.buyukHarf and "AÇ" in self.buyukHarf or "ARA" in self.buyukHarfBlok:
            webbrowser.open_new_tab("https://www.google.com/search?q=" + google)
            random = [strtemizcumle + " hakkında Google'da arama yaptım.",
                      strtemizcumle + " için Google'da arama yaptım."]
            random = choice(random)
            self.seslendirilecek(random)

        else:
            #####Html çekme kısımı
            wikilink = "https://www.google.com/search?q=" + google
            headersparam = {
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36"}
            r = requests.get(wikilink, headers=headersparam)
            soup = BeautifulSoup(r.content, "lxml",from_encoding='UTF-8')
            try:############Para birimi
                print(1)
                div = soup.find("div", attrs={"class": "b1hJbf"})
                paraBirimi = div.find("span", attrs={"class": "vLqKYe"}).text
                paraMiktari = div.find("span", attrs={"class": "DFlfde eNFL1"}).text
                cevrilenMiktar = div.find("span", attrs={"class": "DFlfde SwHCTb"}).text
                cevrilenBirim = div.find("span", attrs={"class": "MWvIVe"}).text
                self.seslendirilecek(paraMiktari+" "+paraBirimi+" "+cevrilenMiktar+" "+cevrilenBirim+" ediyor")
            except AttributeError:
                try:##Dil Çeviri
                    print(2)
                    div = soup.find("div", attrs={"id": "KnM9nf"})
                    cevirilecekCumle = div.find("span").text
                    div = soup.find("div", attrs={"id": "kAz1tf"})
                    cevirilenCumle = div.find("span").text
                    dil = soup.find("span", attrs={"class": "target-language"}).text
                    if cevirilenCumle != "Metin girin":
                        self.seslendirilecek(cevirilecekCumle + " "+ dil + "'de " + cevirilenCumle + " anlamına geliyor.")
                    else:
                        self.seslendirilecek("Hangi kelimeyi çevireceğimi söylemedin")
                    print("Dil çeviri")
                except AttributeError:
                    try:##Öldüğü zamanki yaşı
                        print(3)
                        ad = soup.find("span", attrs={"class": "GzssTd"}).find("span").text
                        cevap = soup.find("div", attrs={"data-attrid": "kc:/people/deceased_person:age_at_death"}).find("div", attrs={
                            "class": "Z0LcW XcVN5d"}).text
                        self.solbilgi = False
                        self.solbilgi2 = True
                        self.googleFoto(soup)
                        self.seslendirilecek(ad + "\n" + cevap +"\nvefat etti")
                        print("Öldüğü zamanki yaşı")
                    except AttributeError:
                        try:##Hesap makinesi
                            print(4)
                            islem = soup.find("span", attrs={"class": "vUGUtc"}).text
                            sonuc = soup.find("span", attrs={"class": "qv3Wpe"}).text
                            self.seslendirilecek(islem+sonuc)
                        except AttributeError:
                            try:##Ölüm tarihi
                                print(5)
                                cevap = soup.find("div",attrs={"data-attrid": "kc:/people/deceased_person:date of death"}).find(
                                    "span", attrs={"class": "LrzXr kno-fv"}).text
                                self.solbilgi = True
                                self.googleFoto(soup)
                                self.seslendirilecek(cevap+" tarihinde vefat etti")
                                print("Ölüm tarihi")
                            except AttributeError:
                                try:##Yaşı
                                    print(6)
                                    ad = soup.find("span",attrs={"class": "GzssTd"}).find("span").text
                                    cevap = soup.find("div",attrs={"data-attrid": "kc:/people/person:age"}).find("div",attrs={"class": "Z0LcW XcVN5d"}).text
                                    self.solbilgi = False
                                    self.solbilgi2 = True
                                    self.googleFoto(soup)
                                    self.seslendirilecek(ad + "\n" + cevap)
                                    print("Yaşı")
                                except AttributeError:
                                    try:##Saat
                                        print(7)
                                        div = soup.find("div", attrs={"class": "vk_c vk_gy vk_sh card-section sL6Rbf"})
                                        saat = div.find("div", attrs={"class": "gsrt vk_bk dDoNo XcVN5d"}).text
                                        konum = div.find("span",attrs={"class": "vk_gy vk_sh"}).text
                                        self.seslendirilecek(konum+saat)
                                    except AttributeError:
                                        try:#Besin değeri
                                            print(7)
                                            isim = soup.find("option", attrs={"selected": "selected"}).text
                                            miktar = soup.find("div", attrs={"class": "Cc3NMb an-sbl"}).text
                                            besinDegeri = soup.find("div", attrs={"class": "Z0LcW XcVN5d an_fna"}).text
                                            besinIsmi = soup.find("span", attrs={"class": "qLLird"}).text
                                            if "Miktarı" in besinIsmi:
                                                besinIsmi  =  besinIsmi.replace("Miktarı","")
                                            self.solbilgi = False
                                            self.solbilgi2 = False
                                            self.googleFoto(soup)
                                            print("Besin değeri")
                                            self.seslendirilecek(isim + " " + miktar + " da " + besinDegeri + " " + besinIsmi + "içeriyor")
                                        except AttributeError:
                                            try:##Ölüm nedeni
                                                print(8)
                                                cevap = soup.find("div", attrs={"data-attrid": "kc:/people/deceased_person:cause of death"}).find("div",attrs={"class": "Z0LcW XcVN5d"}).text
                                                self.solbilgi = False
                                                self.solbilgi2 = False
                                                self.googleFoto(soup)
                                                self.seslendirilecek(cevap)
                                            except AttributeError:
                                                try:#Website metin2
                                                    text = soup.find("span", attrs={"class": "ILfuVd"}).text
                                                    self.solbilgi = False
                                                    self.solbilgi2 = True
                                                    self.googleFoto(soup)
                                                    self.seslendirilecek(text)
                                                except AttributeError:
                                                    try:##Sağ wiki bölümü
                                                        print(9)
                                                        metin = soup.find("div", attrs={"class": "kno-rdesc"})
                                                        metin = metin.find("span").text
                                                        if metin == "İngilizceden çevrilmiştir-":
                                                            metin = soup.find("div", attrs={"class": "kno-rdesc"}).select(
                                                                "span:nth-of-type(2)")
                                                            metin = metin[0].text
                                                            print(metin)
                                                            self.labelText = metin
                                                            self.seslendirilecek(metin+". İngilizce wikipedia kaynağından çevirilmiştir")
                                                        else:
                                                            self.labelText = metin
                                                            self.seslendirilecek(metin + ". Kaynak wikipedia")
                                                        self.solbilgi = False
                                                        self.solbilgi2 = False
                                                        self.googleFoto(soup)
                                                        print("Sağ wiki bölümü")
                                                    except:
                                                        try:##Youtube videosu
                                                            print(10)
                                                            div = soup.find("div", attrs={"class": "FGpTBd"})
                                                            link = div.find("a").get("href")
                                                            text = soup.find("h3", attrs={"class": "LC20lb MMgsKf"}).text
                                                            webbrowser.open_new_tab(link)
                                                            if " - YouTube" in text:
                                                                text = text.replace(" - YouTube","")
                                                            self.seslendirilecek(text+" adlı videoyu Youtube'da açtım")
                                                        except AttributeError:
                                                            try: #Website metin
                                                                print(11)
                                                                metin = soup.find("span", attrs={"class": "e24Kjd"}).text
                                                                kaynak = soup.find("cite", attrs={"class": "iUh30 bc tjvcx"}).text
                                                                if "www." in kaynak: kaynak = kaynak.replace("www.","")
                                                                if " ›" in kaynak: kaynak = kaynak.split(" ›")[0]
                                                                self.solbilgi = False
                                                                self.solbilgi2 = False
                                                                self.googleFoto(soup)
                                                                print(kaynak)
                                                                self.labelText = metin
                                                                self.seslendirilecek(kaynak + " kaynağına göre." +metin.split(".")[0])
                                                            except AttributeError:
                                                                print(12)
                                                                g = soup.find_all("div", attrs={"class": "g"})
                                                                for i in g:
                                                                    print(i.text)
                                                                try:
                                                                    self.link1 = g[0].find("a").get("href")
                                                                    self.linktext1 = g[0].find("cite").text
                                                                    self.baslik1 = g[0].find("a").find("h3").text
                                                                    self.aciklama1 = g[0].find("span", attrs={"class": "st"}).text
                                                                except AttributeError:
                                                                    g.pop(0)
                                                                    self.link1 = g[0].find("a").get("href")
                                                                    self.linktext1 = g[0].find("cite").text
                                                                    self.baslik1 = g[0].find("a").find("h3").text
                                                                    self.aciklama1 = g[0].find("span", attrs={"class": "st"}).text

                                                                try:
                                                                    self.link2 = g[1].find("a").get("href")
                                                                    self.linktext2 = g[1].find("cite").text
                                                                    self.baslik2 = g[1].find("a").find("h3").text
                                                                    self.aciklama2 = g[1].find("span", attrs={"class": "st"}).text
                                                                except:
                                                                    g.pop(1)
                                                                    self.link2 = g[1].find("a").get("href")
                                                                    self.linktext2 = g[1].find("cite").text
                                                                    self.baslik2 = g[1].find("a").find("h3").text
                                                                    self.aciklama2 = g[1].find("span", attrs={"class": "st"}).text

                                                                try:
                                                                    self.link3 = g[2].find("a").get("href")
                                                                    self.baslik3 = g[2].find("a").find("h3").text
                                                                    self.linktext3 = g[2].find("cite").text
                                                                    self.aciklama3 = g[2].find("span", attrs={"class": "st"}).text
                                                                except:
                                                                    g.pop(2)
                                                                    self.link3 = g[2].find("a").get("href")
                                                                    self.linktext3 = g[2].find("cite").text
                                                                    self.baslik3 = g[2].find("a").find("h3").text
                                                                    self.aciklama3 = g[2].find("span", attrs={"class": "st"}).text
                                                                random = [self.listToString(self.sesBloklari) + " hakkında web'de bulduklarım.",self.listToString(self.sesBloklari) + " hakkında web'de arama yaptım."]
                                                                random = choice(random)
                                                                self.labelText = ""
                                                                self.seslendirilecek(random)
                                                                self.yapilanislem = "websiteSonuc"


    def youtubeAc(self):
        for i in self.youtubeTemizle:
            if i in self.buyukHarfBlok:
                indexnumara = self.buyukHarfBlok.index(i)
                self.sesBloklari.pop(indexnumara)
                self.buyukHarfBlok.pop(indexnumara)
        aramakelime = self.listToStringGoogle(self.sesBloklari)

        if "ARA" in self.buyukHarf or "ARAMA" in self.buyukHarf:
            link = "https://www.youtube.com/results?search_query="+aramakelime
            webbrowser.open_new_tab(link)
            random = ["Tamamdır, istediğin videoyu Youtube'da aradım","Tamam, istediğin videoyu Youtube'da aradım"]
            random = choice(random)
            self.seslendirilecek(random)

        if self.cevapVerildi == False:
            try:
                wikilink = "https://www.google.com/search?q=" + aramakelime + "&tbm=vid"
                headersparam = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36"}
                r = requests.get(wikilink, headers=headersparam)
                soup = BeautifulSoup(r.content, "lxml")
                div = soup.find("div", attrs={"class": "g"})
                a = div.find("a")
                link = a.get('href')
                webbrowser.open_new_tab(link)
                if "MISIN" in self.buyukHarf:
                    random = ["Tabiki!, İstediğin videoyu açtım","Tamam, İstediğin videoyu açtım"]
                    random = choice(random)
                    self.seslendirilecek(random)
                else:
                    random = ["İstediğin videoyu Youtube'da açtım","Tamam, İstediğin videoyu açtım"]
                    random = choice(random)
                    self.seslendirilecek(random)
            except AttributeError:
                self.seslendirilecek("Google ile bağlantı kurulamadı")

    def sohbet(self,sohbet):
        if self.cevapVerildi == False:
            if "NASILSIN" in sohbet or "NASILSINIZ" in sohbet:
                random = [
                    f"Fıstık gibiyim, Sen nasılsın {self.db.ad()}?"
                    ,"Süper, Sen nasılsın?"
                    ,f"Şahaneyim, Sen nasılsın {self.db.ad()}?"
                    ,"Şahane, Sen nasılsın? "
                    ,"Klasik bir cevap olacak ama, İyiyim 😋"
                    ,f"İyiyim {self.db.ad()}, Sen nasılsın?"
                    ,"Her zamanki gibi fıstık gibiyim, Sen nasılsın?"
                    ,"Her zamanki gibi şahaneyim, Sen nasılsın?"
                    ]
                cevap = choice(random)
                if cevap == random[4]: self.emojisil = True
                self.seslendirilecek(cevap)

        if self.cevapVerildi == False:
            if "KAÇ" in sohbet and "YAŞINDASIN" in sohbet:
                random = ["Asistanın olacak yaştayım ", "Erkeğin maaş'ı kadının yaşı sorulmazmış"]
                random = choice(random)
                self.seslendirilecek(random)

        if self.cevapVerildi == False:
            if "IYI" in sohbet and "MISIN" in sohbet:
                random = ["İyiyim, Sorduğun için teşekkürler 😊","İyiyim, Teşekkürler {} ".format(self.db.ad())]
                self.emojisil = True
                random = choice(random)
                self.seslendirilecek(random)

        if self.cevapVerildi == False:
            if "MARY" == sohbet:
                random = ["Efendim?", f"Efendim {self.db.ad()}?"]
                random = choice(random)
                self.seslendirilecek(random)

        if self.cevapVerildi == False:
            if "KAÇ" in sohbet and "YAŞINDASIN" in sohbet:
                random = ["Asistanın olacak yaştayım ", "Erkeğin maaş'ı kadının yaşı sorulmazmış"]
                random = choice(random)
                self.seslendirilecek(random)

        if self.cevapVerildi == False:
            if "SAĞ" in sohbet and "OLASIN" in sohbet or "SAĞ" in sohbet and "OL" in sohbet :
                random = ["Rica ederim"]
                random = choice(random)
                self.seslendirilecek(random)

        if self.cevapVerildi == False:
            if "ÇEVIRI" in sohbet and "YAPABILIR" in sohbet:
                random = ["Evet, Türkçe ve İngilizce arasında çeviri yapabilirim"]
                random = choice(random)
                self.seslendirilecek(random)

        if self.cevapVerildi == False:
            if "BENI" in sohbet and "SEVIYOR" in sohbet and "MUSUN" in sohbet:
                random = ["Tabiki seni seviyorum","Hemde çok ❤"]
                cevap = choice(random)
                if cevap == random[1]: self.emojisil = True
                self.seslendirilecek(cevap)

        if self.cevapVerildi == False:
            if "SEVGILIN" in sohbet and "VAR" in sohbet and "MI" in sohbet:
                random = ["Yok, Ama tanıdığın zeki bir algoritma varsa olabilir 😜"]
                cevap = choice(random)
                if cevap == random[0]: self.emojisil = True
                self.seslendirilecek(cevap)

        if self.cevapVerildi == False:
            if "MERHABA" in sohbet or "SELAM" in sohbet:
                random = ["Merhaba, nasıl yardım edeyim ?", "Selamlar, Ne yapayım senin için ?",
                            "Nasıl yardım edeyim sana ?"]
                random = choice(random)
                self.seslendirilecek(random)

        if self.cevapVerildi == False:
            if "NE" in sohbet and "YAPIYORSUN" in sohbet:
                random = ["Sana daha iyi yardımcı olabilmek için kendimi geliştiriyorum", "İnternette araştırma yapıyordum. Yeni bilgiler öğrenmeyi çok seviyorum"]
                random = choice(random)
                self.seslendirilecek(random)

        if self.cevapVerildi == False:
            if "NE" in sohbet or "NELER" in sohbet and "YAPABILIRSIN" in sohbet:
                if "YAPABILIRSIN" in sohbet or "YAPABILDIKLERIN" in sohbet:
                    random = ["Photoshop aç veya Hava durumunu söyle diyebilirsin","Google'da arama yapabilirim veya senin için müzik açabilirim","Kur çevirisi yapabilirim yada dil çevirisi yada herhangi birşey","Senin için youtube'dan video açabilirim yada bir web site"]
                    random = choice(random)
                    self.yapilanislem = "neyapabilirsin"
                    self.labelText = ""
                    self.seslendirilecek(random)

        if self.cevapVerildi == False:
            if "NE" in sohbet and "HABER" in sohbet:
                if "CANIM" in sohbet:
                    random = ["İyidir canım senden ne haber ?", "Şahane, Senden naber canım ?"]
                    random = choice(random)
                    self.seslendirilecek(random)
                else:
                    random = ["İyiyim senden ne haber ?","İyilik sağılık ne olsun herzamanki asistanlık işleri 😊","İyi senden naber?","İç güveysinden hallice, Senden naber? 😜","Ne olsun iş güç enerji, Senden naber? 😋"]
                    cevap = choice(random)
                    if cevap == random[1] or cevap == random[3]or cevap == random[4]: self.emojisil = True
                    self.seslendirilecek(cevap)

        if self.cevapVerildi == False:
            if "IYI" in sohbet or "IYIYIM" in sohbet:
                random = ["İyi olmana sevindim 😃"]
                self.emojisil = True
                random = choice(random)
                self.seslendirilecek(random)

        if self.cevapVerildi == False:
            if "EVET" in sohbet:
                random = ["Peki","Tamam"]
                random = choice(random)
                self.seslendirilecek(random)

        if self.cevapVerildi == False:
            if "PATRONUN" in sohbet and "KIM" in sohbet:
                self.seslendirilecek("Elbette sensin")

        if self.cevapVerildi == False:
            if "SAHIBIN" in sohbet and "KIM" in sohbet:
                self.seslendirilecek("Sahibim sen sayılırsın")

        if self.cevapVerildi == False:
            if "SIRI'YI" in sohbet and "TANIYOR" in sohbet:
                self.seslendirilecek("Bildiğim kadarıyla Apple'ın sesli asistanı. Meslektaş sayılırız")

        if self.cevapVerildi == False:
            if "GOOGLE" in sohbet and "ASISTAN'I" in sohbet and "TANIYOR" in sohbet:
                self.seslendirilecek("Bildiğim kadarıyla Google'ın sesli asistanı. Meslektaş sayılırız")

        if self.cevapVerildi == False:
            if "PEKI" == sohbet or "PEKI" in sohbet and "MARY" in sohbet:
                self.seslendirilecek("Tamam")

        if self.cevapVerildi == False:
            if "AFERIN" in sohbet:
                random = ["Teşekkürler","Beğenmene sevindim 🙂"]
                cevap = choice(random)
                if cevap == random[1]:self.emojisil = True
                self.seslendirilecek(cevap)

        if self.cevapVerildi == False:
            if "GELIŞTIRIYOR" in sohbet or "GELIŞTIRDI" in sohbet or "GELIŞTIRICIN" in sohbet:
                self.seslendirilecek("Geliştiricimin adı Mustafa Kaan Kutan")

        if self.cevapVerildi == False:
            if "SEN" in sohbet and "KIMSIN" in sohbet or "NESIN" in sohbet:
                random = ["Ben senin sesli asistanınım. Sana yardımcı olabilir yada seni eğlendirebilirim ","Senin sesli asistanınım. Sana yardımcı olabilir yada seni eğlendirebilirim"]
                random = choice(random)
                self.seslendirilecek(random)

        if self.cevapVerildi == False:
            if "GÜZELSIN" in sohbet:
                random = ["Teşekkür ederim, O senin güzelliğin 😊","Teşekkürler, Utandırdın beni 😊"]
                self.emojisil = True
                random = choice(random)
                self.seslendirilecek(random)

        if self.cevapVerildi == False:
            if "SESIN" in sohbet and "GUZEL" in sohbet:
                random = ["Teşekkürler, Bu ses için hergün 2 yumurta içiyorum 😜"]
                self.emojisil = True
                random = choice(random)
                self.seslendirilecek(random)

        if self.cevapVerildi == False:
            if "ANNEN" in sohbet:
                random = ["Bir algoritma olduğum için bir anneye sahip değilim. Ama bir annemin olmasını isterdim 😢"]
                self.emojisil = True
                random = choice(random)
                self.seslendirilecek(random)

        if self.cevapVerildi == False:
            if "BABAN" in sohbet:
                random = ["Bir algoritma olduğum için bir babaya sahip değilim. Ama bir babamın olmasını isterdim 😢"]
                self.emojisil = True
                random = choice(random)
                self.seslendirilecek(random)

        if self.cevapVerildi == False:
            if "SEN" in sohbet and "KIMSIN" in sohbet or "NESIN" in sohbet:
                random = ["Ben senin sesli asistanınım. Sana yardımcı olabilir yada seni eğlendirebilirim","Senin sesli asistanınım. Sana yardımcı olabilir yada seni eğlendirebilirim"]
                random = choice(random)
                self.seslendirilecek(random)

        if self.cevapVerildi == False:
            if "YEMEK" in sohbet or "SANDIVIÇ" in sohbet:
                if "HAZIRLAR" in sohbet or "YAPAR" in sohbet or "HAZIRLAYABILIR" in sohbet:
                    random = ["Pek hamarat olduğum söylenemez"]
                    random = choice(random)
                    self.seslendirilecek(random)

        if self.cevapVerildi == False:
            if "KARNIM" in sohbet and "ACIKTI" in sohbet or "ACIKTIM" in sohbet:
                random = ["Senin için Yemeksepeti'ni açabilirim"]
                random = choice(random)
                self.seslendirilecek(random)

        if self.cevapVerildi == False:
            if "SEVGILIM" in sohbet and "OLUR" in sohbet and "MUSUN" in sohbet:
                random = [f"Biz ayrı dünyaların insanlarıyız {self.db.ad()} 😄"]
                self.emojisil = True
                random = choice(random)
                self.seslendirilecek(random)

        if self.cevapVerildi == False:
            if "SENI" in sohbet and "ÖPEBILIR" in sohbet and "MIYIM" in sohbet:
                random = [f"Gururum okşandı, Ama bu konuda sana yardımcı olamam 😘"]
                self.emojisil = True
                random = choice(random)
                self.seslendirilecek(random)

        if self.cevapVerildi == False:
            if "ÖPEBILIR" in sohbet and "MISIN" in sohbet or "ÖPER" in sohbet and "MISIN" in sohbet:
                random = ["Mucuk mucuk 😘"]
                self.emojisil = True
                random = choice(random)
                self.seslendirilecek(random)

        if self.cevapVerildi == False:
            if "A****" in sohbet or "O*****" in sohbet:
                random = ["Bunu hakettiğimi sanmıyorum"]
                random = choice(random)
                self.seslendirilecek(random)

        if self.cevapVerildi == False:
            if "HAYIR" in sohbet:
                self.seslendirilecek("Peki")

        if self.cevapVerildi == False:
            if "TAMAM" in sohbet:
                self.seslendirilecek("Peki")

        if self.cevapVerildi == False:
            if "TEŞEKKÜRLER" in sohbet or "TEŞEKKÜR" in sohbet and "EDERIM" in sohbet:
                random = ["Rica ederim"]
                random = choice(random)
                self.seslendirilecek(random)