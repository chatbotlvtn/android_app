from kivymd.app import MDApp
from kivy.lang.builder import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import ObjectProperty
from kivy.core.window import Window
from rasa_ans import response
from rasa_nlu_speech import nlu, speech_recognize
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDRectangleFlatButton, MDFlatButton
import requests
from playsound import playsound


class MainScreen(Screen):
    namee = ObjectProperty(None)

    def timkiem(self):
        sm.current = "third"
        intention = rasa_module.rasa_nlu(self.namee.text)
        ThirdScreen.data_re = replies.user_ans(intention)
        self.namee.text = "" ### xoa user input


    def check_internet(self):
        url = "https://www.geeksforgeeks.org"
        timeout = 10
        try:
            request = requests.get(url, timeout=timeout)
            self.result = True
        except (requests.ConnectionError, requests.Timeout) as exception:
            self.result = False
        return self.result

    def speak(self):
        internet = self.check_internet()
        close_btn = MDFlatButton(text='Đóng', on_release=self.close_dia)
        if internet == True:
            playsound('listening.mp3')
            heard = listen.bot_listen()
            if heard != None:
                intention = rasa_module.rasa_nlu(heard)
                ThirdScreen.data_re = replies.user_ans(intention)
                find_btn = MDFlatButton(text = 'Tìm', on_release =self.find_lis)
                pop_text = heard
                self.dialog = MDDialog(title='Bạn đã nói', text = pop_text,
                              size_hint=(0.7,1),
                              buttons=[close_btn, find_btn])
            elif heard == None:
                 self.dialog = MDDialog(title="Mời bạn nói lại",
                                       size_hint=(0.7, 1),
                                       buttons=[close_btn])
            self.dialog.open()
        else:
            self.dialog = MDDialog(title='Không có Internet', text = 'Vui lòng thử lại', size_hint=(0.7,1), buttons=[close_btn])
            self.dialog.open()

    def find_lis(self, obj):
        self.dialog.dismiss()
        sm.current = "third"
        playsound('response.mp3')

    def close_dia(self,obj):
        self.dialog.dismiss()


class SecondScreen(Screen):
    def back_main(self):
        sm.current = "main"

    def ket_hon(self):
        sm.current = "third"
        ThirdScreen.data_re = replies.ket_hon_re()

    def nvqs(self):
        sm.current = "third"
        ThirdScreen.data_re = replies.nvqs_re()

    def giam_ho(self):
        sm.current = "third"
        ThirdScreen.data_re = replies.giam_ho_re()

    def ho_ngheo(self):
        sm.current = "third"
        ThirdScreen.data_re = replies.ho_ngheo_re()

    def di_chuc(self):
        sm.current = "third"
        ThirdScreen.data_re = replies.di_chuc_re()

class ThirdScreen(Screen):
    reply = ObjectProperty(None)
    data_re = ""
    def on_enter(self, *args):
        self.reply.text = self.data_re

    def back_main(self):
        sm.current = "main"
        self.reply.text = ""   #### xoa user_answ

    def back_list(self):
        sm.current = "second"
        self.reply.text =""     #####xoa user_answ

class FourthScreen(Screen):
    def back_main(self):
        sm.current = "main"

    def kethon_tamtru(self):
        sm.current = "third"
        ThirdScreen.data_re = replies.kethon_tamtru()

    def tu_y_kethon(self):
        sm.current = "third"
        ThirdScreen.data_re = replies.tu_y_kethon()

    def thgian_nghi_kh(self):
        sm.current = "third"
        ThirdScreen.data_re = replies.thgian_nghi_kh()

    def hoan_nvqs(self):
        sm.current = "third"
        ThirdScreen.data_re = replies.hoan_nvqs()

    def congchung_dichuc(self):
        sm.current = "third"
        ThirdScreen.data_re = replies.congchung_dichuc()

    def dk_giamho(self):
        sm.current = "third"
        ThirdScreen.data_re = replies.dk_giamho()


class WindowManager(ScreenManager):
    pass
#######################################
sm = WindowManager()
rasa_module = nlu()
replies = response()
listen = speech_recognize()
######################################
class DemoApp(MDApp):
    def build(self):
        screen = Builder.load_file("Main_m.kv")
        screens = [MainScreen(name='main'), SecondScreen(name='second'), ThirdScreen(name='third'),
                   FourthScreen (name = 'fourth')]
        for screen in screens:
            sm.add_widget(screen)
        return sm

DemoApp().run()
