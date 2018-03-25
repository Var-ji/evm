from kivy.uix.popup import Popup
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.app import App
from kivy.core.window import Window
from kivy.uix.image import Image
import anydbm, sys
import pymongo
from kivy.config import Config, ConfigParser
from kivy.uix.settings import Settings
from kivy.uix.colorpicker import ColorPicker
from kivy.uix.scrollview import ScrollView
from operator import itemgetter
from functools import partial

Config.set('kivy', 'exit_on_escape', 0)

class EVMApp(App):
    def __init__(self, **kwargs):
        super(EVMApp, self).__init__(**kwargs)
        self.number = None
        self.evmgrid = None

        try:
            ptr = open("connection.dat", "r")
            connectString = ptr.read()
            ptr.close()
            connectString.strip()
            if connectString == "" or connectString == None:
                connectString = "mongodb://localhost:27017/"
        except:
            connectString = "mongodb://localhost:27017/"
            ptr = open("connection.dat", "c")
            ptr.write(connectString)
            ptr.close()

        self.client = pymongo.MongoClient("mongodb://localhost:27017/")
        self.database = self.client.Database
        self.result = None
        
        try:
            db = anydbm.open("config.db", "r")
            self.number = int(db["number"])
            db.close()
        except:
            self.number = 2
        self.vt = 0
        self.buttons = list()
        self.candidates = None
        self.temp = ""
        try:
            db = anydbm.open("config.db", "r")
            self.candidates = db["candidates"]
            self.temp = self.candidates
            db.close()
            self.candidates.strip()
            self.candidates = self.candidates.split(';')
            if len(self.candidates) < self.number:
                for i in range(self.number - len(self.candidates)):
                    s = "Candidate " + str(i)
                    self.candidates.append(s)
                    self.temp = self.temp + s + ";"                   
            for i in range(self.number):
                self.buttons.append(Button(text = self.candidates[i], font_size = 24))
        except:
            self.candidates = list()
            for i in range(self.number):
                s = "Candidate " + str(i)
                self.temp = self.temp + s + ";"
                self.buttons.append(Button(text = s, font_size = 24))
                self.candidates.append(s)
        self.color = ""
        self.post = None
        self.im_path = ""
        self.school = ""
        self.code1 = ""
        self.code2 = ""
        self.json = '''
        [
            {
                "type": "string",
                "title": "Name of Institution",
                "desc": "Set the name of the institution! It defaults to Unknown otherwise",
                "section": "EVM",
                "key": "school"
            },
            {
                "type": "numeric",
                "title": "Number of candidates",
                "desc": "Set the number of candidates! The default value is 2",
                "section": "EVM",
                "key": "number"
            },
            {
                "type": "string",
                "title": "Candidate Names",
                "desc": "Set the names of the candidates. Names must be separated by a semi-colon(;).",
                "section": "EVM",
                "key": "names"
            },
            {
                "type": "string",
                "title": "Post",
                "desc": "Set the text for the post",
                "section": "EVM",
                "key": "post"
            },
            {
                "type": "string",
                "title": "Color",
                "desc": "Set the color. Use the color picker to select the color. Enter it in hex format.",
                "section": "EVM",
                "key": "p_col"
            },
            {
                "type": "string",
                "title": "Image of logo to be loaded",
                "desc": "Specify the path where the logo is stored. Note that if there is an I/O error, no image will be loaded. Note that the file name must also be mentioned. Supported formats are .jpg, .png and .bmp",
                "section": "EVM",
                "key": "im_path"
            },
            {
                "type": "string",
                "title": "Password for voting",
                "desc": "Set the password for allowing votes to be cast. Note that the weightage of each vote is 1",
                "section": "EVM",
                "key": "code1"
            },
            {
                "type": "string",
                "title": "Password for viewing the results",
                "desc": "Set the password for viewing the results.",
                "section": "EVM",
                "key": "code2"
            }
        ]
        '''


    def initscript(self):
        try:
            db = anydbm.open("config.db", "r")
            color1 = db["color"]
            self.school = db["school"]
            self.im_path = db["image"]
            self.post = db["post"]
            self.code1 = db["voters"]
            self.code2 = db["results"]
            db.close()
            try:
                if color1.startswith('#'):
                    for i in range(1, 7):
                        self.color = self.color + color1[i]
                else:
                    for i in range(6):
                        self.color = self.color + color1[i]
                self.color = self.color.upper()
            except:
                self.color = "FFFFFF"

        except:
             self.color = "FFFFFF"
             self.post = "Unknown"
             self.im_path = "logo.jpg"
             self.school = "Unknown"
             self.code1 = "voting"
             self.code2 = "results"
             db = anydbm.open("config.db", "c")
             db["color"] = self.color
             db["school"] = self.school
             db["image"] = self.im_path
             db["post"] = self.post
             db["voters"] = self.code1
             db["results"] = self.code2
             s = ""
             for i in self.candidates:
                 s = s + i + ";"
             db["candidates"] = s
             db.close()
        self.result = self.database[self.post]
        try:
            c = self.result.find_one({"name": "counter"})
            for i in self.candidates:
                s = self.result.find_one({"name": i})
                if s == None:
                    raise IOError
        except IOError:
            self.result.insert_one({'name': 'counter', 'votes': 0})
            for i in self.candidates:
                self.result.insert_one({"name": i, "votes":0})

    def settings_change(self, event, config, section, key, value):
        if key == "school":
            self.school = value
        elif key == "names":
            self.temp = value
        elif key == "number":
            self.number = value
        elif key == "post":
            self.post = value
        elif key == "p_col":
            self.color = value
        elif key == "im_path":
            self.im_path = value
        elif key == "code1":
            self.code1 = value
        elif key == "code2":
            self.code2 = value

       
    def save_settings(self, setting):
        db = anydbm.open("config.db", "w")
        db["candidates"] = self.temp
        db["number"] = str(self.number)
        db["post"] = self.post
        db["color"] = self.color
        db["school"] = self.school
        db["image"] = self.im_path
        db["voters"] = self.code1
        db["results"] = self.code2
        db.close()
        self.close_settings()
        UpdateEVM().Update()


    def settings_func(self, p):
        s = Settings()
        config = ConfigParser()
        try:
            config.setdefaults('EVM', {'school': self.school, 'names': self.temp, 'post': self.post, 'p_col': self.color, 'im_path': self.im_path, "code1": self.code1, "code2": self.code2, 'number':self.number})
        except:
            config.setdefaults('EVM', {'school': 'Unknown', 'names': self.temp, 'post': "Unknown", 'p_col': 'FFFFFF', 'im_path': self.im_path, "code1": "voting", "code2": "results", 'number':self.number})
        s.add_json_panel('EVM', config, data = self.json)
        s.bind(on_config_change = self.settings_change)
        setting = Popup(title = "Settings", content = s)
        s.bind(on_close = lambda *func: self.save_settings(s))
        setting.open()


    def messageShow(self, passcode, p):
        if passcode == self.code1:
            self.vt = 1
            p.dismiss()
        elif passcode == "exitevm":
            p.dismiss()
            sys.exit()
        elif passcode == self.code2:
            res = list()
            result_grid = GridLayout(cols = 2, padding = [50, 50, 50, 50], spacing = [5, 50], size_hint_y = None)
            for btn in self.buttons:
                a = self.result.find_one({'name': btn.text})
                res.append(a)
            res = sorted(res, key = itemgetter('votes'), reverse = True)
            for doc in res:
                result_grid.add_widget(Label(text = doc['name'], font_size = 24))
                result_grid.add_widget(Label(text = str(doc['votes']), font_size = 24))
            a = self.result.find_one({'name': 'counter'})
            result_grid.add_widget(Label(text = "Number of Voters", font_size = 32))
            result_grid.add_widget(Label(text = str(a['votes']), font_size = 32))
            scrollbar = ScrollView()
            scrollbar.add_widget(result_grid)
            result = Popup(title = "Results", content = scrollbar)
            p.content.text = ""
            result.open()
        elif passcode == "resetallvotes":
            self.result.update_many({'name': {'$exists': True}}, {'$set': {'votes': 0}})
            p.content.text = ""
        elif passcode == "factoryreset":
            self.client.drop_database(self.database)
            p.content.text = ""
            UpdateEVM().Update()
        elif passcode == "settings":
            self.settings_func(p)
            p.content.text = ""
        elif passcode == "colorpicker":
            color_w = ColorPicker()
            color_p = Popup(title = "Color Picker", content = color_w)
            p.content.text = ""
            color_p.open()


    def close_event(self, event):
        return True

    def on_popup_parent(self, p):
        if p:
            p.content.focus = True
   
    def build(self):
        self.initscript()
        color2 = "[color=" + self.color + "]"
        indicator_l = color2 + self.post + "[/color]"
        #Window.fullscreen = "auto"
        Window.window_state = "maximized"
        Window.bind(on_request_close = self.close_event)
        grid = GridLayout(cols = 1, padding = [50, 50, 50, 50], spacing = [5, 50], size_hint_y = None, height = (self.number+3)*150)
        self.evmgrid = ScrollView()
        titlegrid = GridLayout(cols = 2, padding = [250, 0, 450, 0])
        try:
            image = Image(source = self.im_path)
            titlegrid.add_widget(image)
        except:
            pass
        titlename = Label(text = self.school, font_size = 36)
        indicator_label = Label(text = indicator_l, font_size = 28, markup = True)
        titlegrid.add_widget(titlename)
        grid.add_widget(titlegrid)
        grid.add_widget(indicator_label)
        for i in self.buttons:
            grid.add_widget(i)
        for i in range(self.number):
            button_callback = partial(self.results, self.buttons[i].text)
            self.buttons[i].bind(on_press = button_callback)
        self.evmgrid.add_widget(grid)
        return self.evmgrid

    def show_popup(self):
        t1 = TextInput(password = True, multiline = False, write_tab = False)
        p = Popup(title = "Enter password", auto_dismiss = False, content = t1, size_hint=(None, None), size=(400, 105), title_align = 'center', separator_height = 3)
        t1.bind(on_text_validate = lambda *func: self.messageShow(t1.text, p))
        p.bind(on_open = self.on_popup_parent)
        p.open()

    def results(self, text, event):
        if self.vt == 0:
            pass
        else:
            self.result.update_one({'name': text}, {'$inc': {'votes': 1}})
            self.result.update_one({'name': 'counter'}, {'$inc': {'votes': 1}})
        self.show_popup()


class UpdateEVM:
    def Update(self):
        App.get_running_app().stop()
        EVMApp().run()


if __name__ == "__main__":
    EVMApp().run()
