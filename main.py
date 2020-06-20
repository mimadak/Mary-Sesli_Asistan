import speech_recognition as sr
from komut import komutlar,Veritabani
from PyQt5 import QtWidgets, uic ,QtGui,QtCore
import sys
from responsive_voice import ResponsiveVoice
import threading
import time
from os import remove,environ,getcwd
environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
from pygame import mixer
import webbrowser
import sounddevice as sd
import numpy as np

r = sr.Recognizer()
with sr.Microphone() as source:
    r.adjust_for_ambient_noise(source)


engine = ResponsiveVoice(lang=ResponsiveVoice.TURKISH, gender=ResponsiveVoice.FEMALE, pitch=0.53, rate=0.52,key="8FCWWns8")


class ses_cal():
    def __init__(self,file_path):
        file = open(file_path)
        mixer.init()
        mixer.music.load(file)
        mixer.music.play()
        while mixer.music.get_busy():
            time.sleep(0.05)
            if window.ttsIptal:
                break
        mixer.stop()
        mixer.quit()
        file.close()
        remove(file_path)
        sys.exit()


class Ui(QtWidgets.QMainWindow):
    def __init__(self):
        super(Ui, self).__init__()
        uic.loadUi('iwsss.ui', self)
        self.micButton = self.findChild(QtWidgets.QPushButton, 'micButton')
        self.Kelime_Label = self.findChild(QtWidgets.QLabel,'Kelime_Label')
        self.Yanit_Label = self.findChild(QtWidgets.QLabel,'Yanit_Label')
        self.Tip_Label = self.findChild(QtWidgets.QLabel,'Tip_Label')
        self.Yanit_Layout = self.findChild(QtWidgets.QLayout, 'horizontalLayout_2')
        self.Image_Label = self.findChild(QtWidgets.QLabel, 'Image_Label')
        self.sitelink1 = self.findChild(QtWidgets.QLabel, 'sitelink1')
        self.sitelink2 = self.findChild(QtWidgets.QLabel, 'sitelink2')
        self.sitelink3 = self.findChild(QtWidgets.QLabel, 'sitelink3')
        self.sitebaslik1 = self.findChild(QtWidgets.QLabel, 'sitebaslik1')
        self.sitebaslik2 = self.findChild(QtWidgets.QLabel, 'sitebaslik2')
        self.sitebaslik3 = self.findChild(QtWidgets.QLabel, 'sitebaslik3')
        self.sitebaslik1.setOpenExternalLinks(True)
        self.sitebaslik2.setOpenExternalLinks(True)
        self.sitebaslik3.setOpenExternalLinks(True)
        self.siteaciklama1 = self.findChild(QtWidgets.QLabel, 'siteaciklama1')
        self.siteaciklama2 = self.findChild(QtWidgets.QLabel, 'siteaciklama2')
        self.siteaciklama3 = self.findChild(QtWidgets.QLabel, 'siteaciklama3')
        self.web_sonuc1.setSpacing(0)
        self.web_sonuc2.setSpacing(0)
        self.web_sonuc3.setSpacing(0)
        self.web_sonuc1 = self.findChild(QtWidgets.QLayout, 'web_sonuc1')
        self.web_sonuc2 = self.findChild(QtWidgets.QLayout, 'web_sonuc2')
        self.web_sonuc3 = self.findChild(QtWidgets.QLayout, 'web_sonuc3')
        self.web_sonuc1.setContentsMargins(0 ,0 ,0 ,0)
        self.web_sonuc2.setContentsMargins(0, 0, 0, 0)
        self.web_sonuc3.setContentsMargins(0, 0, 0, 0)
        self.micButton.clicked.connect(self.micButtonPressed)
        self.setWindowIcon(QtGui.QIcon('image/mary.png'))
        self.animasyon = False
        self.ttsIptal = False
        self.listenAktif = False
        self.micButtonClickable = True
        self.Image_Label.show()
        self.dosyakonumu = getcwd()
        for i in range(10):
            self.dosyakonumu = self.dosyakonumu.replace("\\","/")
        i = "border-image: url('{}/image/background.png');".format(self.dosyakonumu)
        stylesheet = "#centralwidget{"+i+"}"
        self.setStyleSheet(stylesheet)
        self.micButton.setStyleSheet("border-image: url('{}/image/mic_1.png');".format(self.dosyakonumu))
        self.yapilanislem = ""

        self.db = Veritabani()
        if self.db.ad() == "":
            self.yapilanislem = "ilkacilis"
            konus = threading.Thread(target=self.ilkCalistirma)
            konus.start()
        self.show()


    def ilkCalistirma(self):
        mixer.init()
        self.micButton.setMaximumSize(0, 0)
        self.micButton.setMinimumSize(0, 0)
        self.Tip_Label.setText("")
        file_path = engine.get_mp3("Hoşgeldin, Adım Mary.\nBen senin sesli asistanınım.")
        threading.Thread(target=self.setYanitLabel, args={"Hoşgeldin, Adım Mary. Ben senin sesli asistanınım."}).start()
        mixer.music.load(file_path)
        mixer.music.play()
        while mixer.music.get_busy():
            time.sleep(0.1)
        file_path = engine.get_mp3("Öncelikle adını öğrenebilir miyim? Adını söylemek için lütfen butona tıkla")
        threading.Thread(target=self.setYanitLabel,args={"Öncelikle adını öğrenebilir miyim?\nAdını söylemek için lütfen butona tıkla"}).start()
        mixer.music.load(file_path)
        mixer.music.play()
        while mixer.music.get_busy():
            time.sleep(0.1)
        self.micButton.setMaximumSize(80, 80)
        self.micButton.setMinimumSize(80, 80)
        self.Tip_Label.setText("Konuşmak için butona tıklayın")
        while True:
            time.sleep(0.1)
            if self.db.ad() != "":
                time.sleep(5)
                self.setYanitLabel("")
                self.Image_Label.show()
                self.Image_Label.setStyleSheet("border-image: url('{}/image/neler_yapabilirsin.png');".format(self.dosyakonumu))
                self.Image_Label.setMaximumSize(630, 270)
                self.Image_Label.setMinimumSize(630, 270)
                file_path = engine.get_mp3(f"Yapabileceklerimin bazıları şunlar {self.db.ad()}. Şimdi başlayabilirsin")
                ses_cal(file_path)
                sys.exit()


    def micButtonPressed(self):
        print("micButton Basıldı")
        if self.listenAktif:
            self.micButtonClickable = False
            self.ttsIptal = True
            self.listenAktif = False
            self.animasyon = False
            self.Tip_Label.setText("Konuşmak için butona tıklayın")
            self.Tip_Label.setStyleSheet("color: rgb(255, 255, 255);")
            self.micButton.setStyleSheet("border-image: url('{}/image/mic_1.png');".format(self.dosyakonumu))
            def i():
                time.sleep(2)
                self.micButtonClickable = True
            threading.Thread(target=i).start()
        else:
            if self.micButtonClickable:
                self.listenAktif = True
                self.ttsIptal = True
                self.animasyon = True
                self.Tip_Label.setText("Dinleniyor")
                self.micButton.setStyleSheet("border-image: url('{}/image/mic_2.png');".format(self.dosyakonumu))
                self.Tip_Label.setStyleSheet("background-color:#ff0000;color: rgb(255, 255, 255);")
                threading.Thread(target=self.sesanimasyon).start()
                threading.Thread(target=self.dinle).start()


    def sesanimasyon(self):
        def sound(indata, outdata, frames, time, status):
            if window.animasyon:
                volume_norm = np.linalg.norm(indata) * 400
                window.Tip_Label.setMinimumSize(70+volume_norm, 0)
        with sd.Stream(callback=sound):
            sd.sleep(10000)
        sys.exit()


    def setYanitLabel(self,yazi,foto=False):
        self.Yanit_Label.setWordWrap(False)
        QtCore.QMetaObject.invokeMethod(self.Yanit_Label, "setText", QtCore.Qt.QueuedConnection, QtCore.Q_ARG(str,yazi))
        yaziBoyutu = QtGui.QFont()
        yaziBoyutu.setPointSize(22)
        def animasyon():
            pozisyon = 100
            for i in range(20):
                if pozisyon>0: pozisyon -= 5
                self.Yanit_Layout.setContentsMargins(0,0,0, pozisyon)
                time.sleep(0.01)
            sys.exit()
        if foto:
            self.Yanit_Label.setWordWrap(True)
            self.Yanit_Label.setAlignment(QtCore.Qt.AlignLeft)
        else:
            self.Yanit_Label.setAlignment(QtCore.Qt.AlignCenter)
        if len(yazi)<=40:
            print("40'dan küçük")
            yaziBoyutu.setPointSize(22)
            self.Yanit_Label.setMaximumSize(1000, 99999)

        elif len(yazi)>=40 and len(yazi)<=50:
            print("40-50")
            yaziBoyutu.setPointSize(20)

        elif len(yazi)>=50 and len(yazi)<=60:
            print("50-60")
            yaziBoyutu.setPointSize(18)

        elif len(yazi)>=60 and len(yazi)<=70:
            print("60-70")
            yaziBoyutu.setPointSize(17)
            if foto:
                self.Yanit_Label.setMaximumSize(600, 99999)
            else:
                self.Yanit_Label.setMaximumSize(800, 99999)

        elif len(yazi)>=70 and len(yazi)<=130:
            print("70-130")
            if foto:
                self.Yanit_Label.setMaximumSize(800, 99999)
                self.Yanit_Label.setWordWrap(True)
                yaziBoyutu.setPointSize(18)
            else:
                self.Yanit_Label.setMaximumSize(1000, 99999)
                self.Yanit_Label.setWordWrap(True)
                yaziBoyutu.setPointSize(18)
        else:
            print(len(yazi))
            print("130 üstü")
            yaziBoyutu.setPointSize(14)
            if foto:
                self.Yanit_Label.setMaximumSize(400, 99999)
                self.Yanit_Label.setWordWrap(True)
            else:
                self.Yanit_Label.setMaximumSize(600, 99999)
                self.Yanit_Label.setWordWrap(True)

        self.Yanit_Label.setFont(yaziBoyutu)
        threading.Thread(target=animasyon).start()


    def veriIsle(self,ses):
        text = r.recognize_google(ses, language='tr-tr')
        if "Merih" in text:
            text = text.replace("Merih","Mary")
        if "Melih" in text:
            text = text.replace("Melih","Mary")
        if "Meri" in text:
            text = text.replace("Meri","Mary")
        self.Kelime_Label.setText(text)
        komut = komutlar(text)
        komut.islemBul(window.yapilanislem)
        self.yapilanislem = komut.yapilanislem
        if self.listenAktif == False:
            self.siteaciklama1.setText("")
            self.siteaciklama2.setText("")
            self.siteaciklama3.setText("")
            self.sitebaslik1.setText("")
            self.sitebaslik2.setText("")
            self.sitebaslik3.setText("")
            self.sitelink1.setText("")
            self.sitelink2.setText("")
            self.sitelink3.setText("")
            self.web_sonuc1.setSpacing(0)
            self.web_sonuc2.setSpacing(0)
            self.web_sonuc3.setSpacing(0)
            self.web_sonuc1.setContentsMargins(0, 0, 0, 0)
            self.web_sonuc2.setContentsMargins(0, 0, 0, 0)
            self.web_sonuc3.setContentsMargins(0, 0, 0, 0)
            self.Image_Label.setAlignment(QtCore.Qt.AlignLeft)
            file_path = engine.get_mp3(komut.seslendirilecektext)
            if komut.yapilanislem == "neyapabilirsin":
                self.Image_Label.show()
                self.Image_Label.setStyleSheet("border-image: url('{}/image/neler_yapabilirsin.png');".format(self.dosyakonumu))
                self.Image_Label.setMinimumSize(630, 270)
                self.Image_Label.setMinimumSize(630, 270)
                self.Yanit_Layout.setSpacing(0)
                self.setYanitLabel(komut.labelText,foto=True)
                self.yapilanislem = ""
            elif komut.yapilanislem == "websiteSonuc":
                self.Image_Label.hide()
                self.sitebaslik1.setCursor(QtCore.Qt.PointingHandCursor)
                self.sitebaslik2.setCursor(QtCore.Qt.PointingHandCursor)
                self.sitebaslik3.setCursor(QtCore.Qt.PointingHandCursor)
                self.web_sonuc1.setContentsMargins(0, 15, 0, 15)
                self.web_sonuc2.setContentsMargins(0, 0, 0, 15)
                self.web_sonuc3.setContentsMargins(0, 0, 0, 15)
                self.web_sonuc1.setSpacing(3)
                self.web_sonuc2.setSpacing(3)
                self.web_sonuc3.setSpacing(3)
                self.Yanit_Label.setText("")
                self.sitelink1.setText(komut.linktext1)
                self.sitelink2.setText(komut.linktext2)
                self.sitelink3.setText(komut.linktext3)
                QtCore.QMetaObject.invokeMethod(self.sitebaslik1, "setText", QtCore.Qt.QueuedConnection, QtCore.Q_ARG(str,"<a href='{}'><font color=white>{}</font></a>".format(komut.link1,komut.linktext1)))
                QtCore.QMetaObject.invokeMethod(self.sitebaslik2, "setText", QtCore.Qt.QueuedConnection, QtCore.Q_ARG(str,"<a href='{}'><font color=white>{}</font></a>".format(komut.link2,komut.linktext2)))
                QtCore.QMetaObject.invokeMethod(self.sitebaslik3, "setText", QtCore.Qt.QueuedConnection, QtCore.Q_ARG(str,"<a href='{}'><font color=white>{}</font></a>".format(komut.link3,komut.linktext3)))
                self.siteaciklama1.setText(komut.aciklama1)
                self.siteaciklama2.setText(komut.aciklama2)
                self.siteaciklama3.setText(komut.aciklama3)
                self.yapilanislem = ""
            elif komut.foto:
                self.Image_Label.show()
                self.Image_Label.setStyleSheet("border-image: url('{}/image/image.jpg');".format(self.dosyakonumu))
                self.Image_Label.setMinimumSize(komut.width, komut.height)
                self.Image_Label.setMaximumSize(komut.width, komut.height)
                if komut.yapilanislem == "havadurumu":
                    self.Yanit_Label.setAlignment(QtCore.Qt.AlignLeft)
                    QtCore.QMetaObject.invokeMethod(self.Yanit_Label, "setText", QtCore.Qt.QueuedConnection,QtCore.Q_ARG(str, komut.labelText))
                    self.Yanit_Layout.setSpacing(15)
                    self.Image_Label.setAlignment(QtCore.Qt.AlignBottom)
                    self.sitebaslik1.setText(komut.detay1)
                    self.sitebaslik2.setText(komut.detay2)
                    self.sitebaslik3.setText(komut.detay3)
                    self.sitebaslik1.setCursor(QtCore.Qt.ArrowCursor)
                    self.sitebaslik2.setCursor(QtCore.Qt.ArrowCursor)
                    self.sitebaslik3.setCursor(QtCore.Qt.ArrowCursor)
                    self.yapilanislem = ""
                else:
                    self.Yanit_Layout.setSpacing(30)
                    self.setYanitLabel(komut.labelText,foto=True)
            else:
                self.Image_Label.setStyleSheet("")
                self.Image_Label.setMinimumSize(0, 0)
                self.Image_Label.setMaximumSize(0, 0)
                self.Image_Label.hide()
                self.Yanit_Layout.setSpacing(6)
                self.setYanitLabel(komut.labelText)
            threading.Thread(target=ses_cal, args={file_path}).start()


    def dinle(self):
        def callback(recognizer, audio):
            try:
                self.Tip_Label.setText("Konuşmak için butona tıklayın")
                self.Tip_Label.setStyleSheet("color: rgb(255, 255, 255);")
                self.micButton.setStyleSheet("border-image: url('{}/image/mic_1.png');".format(window.dosyakonumu))
                if window.listenAktif:
                    window.ttsIptal = False
                    window.listenAktif = False
                    window.animasyon = False
                    self.veriIsle(audio)
                sys.exit()
            except sr.UnknownValueError:
                print("Ne dediğini anlayamadım.")
                self.micButton.setStyleSheet("border-image: url('{}/image/mic_1.png');".format(window.dosyakonumu))
                self.Kelime_Label.setText("Anlaşılmadı")
                window.listenAktif = False
                sys.exit()
            except sr.RequestError:
                print("İnternet bağlanıtısı kurulamadı.")
                self.micButton.setStyleSheet("border-image: url('{}/image/mic_1.png');".format(window.dosyakonumu))
                window.listenAktif = False
                sys.exit()
        with sr.Microphone() as source:
            r.adjust_for_ambient_noise(source,duration=0.3)
        r.listen_in_background(sr.Microphone(),callback)
        for i in range(100):
            time.sleep(0.1)
            if self.listenAktif != True:
                break
        self.Tip_Label.setText("Konuşmak için butona tıklayın")
        self.micButton.setStyleSheet("border-image: url('{}/image/mic_1.png');".format(self.dosyakonumu))
        self.Tip_Label.setStyleSheet("color: rgb(255, 255, 255);")
        self.animasyon = False
        sys.exit()

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = Ui()
    sys.exit(app.exec_())