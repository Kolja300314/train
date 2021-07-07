# -*- coding: utf-8 -*-
from kivy.app import App
from kivy.lang import Builder
from kivy.config import Config
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.widget import Widget
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.gridlayout import GridLayout
from kivy.storage.jsonstore import JsonStore
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.properties import ObjectProperty, StringProperty


Config.set('graphics', 'width', '400')
Config.set('graphics', 'height', '500')

with open('style.kv', encoding='utf-8') as f:
    Builder.load_string(f.read())


class MenuScreen(Screen):
    pass


class AddScreen(Screen):
    txt_inpt = ObjectProperty(None)

    def check_status(self, btn1):
        if self.txt_inpt.text:
            save_name_exercises(self.txt_inpt.text)
            sm.current = 'save'
        else:
            print('empty field')


class SaveScreen(Screen):

    grid2 = ObjectProperty(None)
    inputs = []

    def add_line(self):
        a = TextInput(size_hint=(1, None), height=30)
        b = TextInput(size_hint=(1, None), height=30, input_filter='int')

        self.grid2.add_widget(a)
        self.grid2.add_widget(b)

        self.inputs.append((a, b))

    def save_exercises(self):
        for i in self.grid2.children[:-2:]:
            if i.text == ' ' or not i.text:
                break
        else:
            reinputs = [i[0].text.strip() + ' 0 ' + i[1].text.strip() for i in self.inputs]
            stora = JsonStore('exercises.json')
            stora.put(name, exerc=reinputs)

            sm.current = 'menu'


class ShowScreen(Screen):
    grd = ObjectProperty(None)

    def on_pre_enter(self, *args):

        stora = JsonStore('exercises.json')

        for k in stora.keys():
            a = Button(text=k, size_hint=(1, None), height=40, on_release=self.on_press)
            self.grd.add_widget(a)

    def on_press(self, btn):
        remember_train(btn.text)
        sm.current = 'train'

    def on_leave(self, *args):
        for i in self.grd.children[:-1]:
            self.grd.remove_widget(i)


class TrainScreen(Screen):
    grd = ObjectProperty(None)

    def on_enter(self, *args):
        stora = JsonStore('exercises.json')
        if stora.exists(train):
            for i in stora.get(train)['exerc']:
                if i != ' ':
                    tr, maked, am = i.split()
                    self.grd.add_widget(Label(size_hint=(1, None), height=30, text=tr))
                    self.grd.add_widget(Label(size_hint=(1, None), height=30, text=maked))
                    self.grd.add_widget(Label(size_hint=(1, None), height=30, text=am))

    def change(self):
        sm.current = 'change'

    def reset(self):
        spisok = []
        stora = JsonStore('exercises.json')
        k = 0
        for i in stora.get(train)['exerc']:
            a, b, c = i.split()
            spisok.append(a + ' ' + '0' + ' ' + c)
        stora.put(train, exerc=spisok)
        sm.current = 'show'

    def delete(self):
        stora = JsonStore('exercises.json')
        stora.delete(train)
        sm.current = 'show'

    def on_leave(self, *args):
        for i in self.grd.children[:-3]:
            self.grd.remove_widget(i)


class ChangeScreen(Screen):
    grd = ObjectProperty(None)

    def on_enter(self, *args):
        stora = JsonStore('exercises.json')
        if stora.exists(train):
            for i in stora.get(train)['exerc']:
                if i != ' ':
                    tr, maked, am = i.split()
                    self.grd.add_widget(Label(size_hint=(1, None), height=30, text=tr))
                    self.grd.add_widget(Label(size_hint=(1, None), height=30, text=maked))
                    self.grd.add_widget(TextInput(size_hint=(1, None), height=30, input_filter='int'))

    def save(self):
        spisok = []
        stora = JsonStore('exercises.json')
        childrens = self.grd.children[:-3:3]
        childrens.reverse()
        k = 0
        for i in stora.get(train)['exerc']:
            print(childrens[k].text)
            a, b, c = i.split()
            if not childrens[k].text or childrens[k].text == ' ':
                spisok.append(a+' '+b+' '+c)
            else:
                spisok.append(a+' '+str(int(b)+int(childrens[k].text.strip()))+' '+c)
            k += 1
        stora.put(train, exerc=spisok)
        sm.current = 'train'

    def on_leave(self, *args):
        for i in self.grd.children[:-3]:
            self.grd.remove_widget(i)


def save_name_exercises(nme):
    global name
    name = nme


def remember_train(trn):
    global train
    train = trn


sm = ScreenManager()
sm.add_widget(MenuScreen(name='menu'))
sm.add_widget(AddScreen(name='add'))
sm.add_widget(SaveScreen(name='save'))
sm.add_widget(ShowScreen(name='show'))
sm.add_widget(TrainScreen(name='train'))
sm.add_widget(ChangeScreen(name='change'))


class TestApp(App):
    def build(self):
        return sm


if __name__ == '__main__':
    TestApp().run()