from kivy.uix.popup import Popup
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.app import App
from kivy.core.window import Window
from kivy.uix.image import Image
import anydbm, sys
from kivy.config import Config, ConfigParser
from kivy.uix.settings import Settings
from kivy.uix.colorpicker import ColorPicker
from kivy.uix.scrollview import ScrollView

Config.set('kivy', 'exit_on_escape', 0)


class CustomPopup(Popup):
    pass


class EVMApp(App):
    def __init__(self, **kwargs):
        super(EVMApp, self).__init__(**kwargs)
        self.number = None
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
            for i in range(self.number):
                self.buttons.append(Button(text = self.candidates[i], font_size = 24))
        except:
            self.candidates = list()
            for i in range(self.number):
                s = "Candidate " + str(i)
                self.temp = self.temp + s + ";"
                self.buttons.append(Button(text = s, font_size = 24))
                self.candidates.append(s)
        self.counter = None
        self.color = ""
        self.post = None
        self.path = ""
        self.im_path = ""
        self.school = ""
        self.code1 = ""
        self.code3 = ""
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
                "title": "Where should the results be stored?",
                "desc": "Specify the path where the results should be stored. Note that if there is an I/O error, it will be stored in the default location without any indication. Note that the file name must also be mentioned.",
                "section": "EVM",
                "key": "path"
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
                "key": "code3"
            }
        ]
        '''


    def initscript(self):
        try:
            db = anydbm.open("config.db", "r")
            color1 = db["color"]
            self.school = db["school"]
            self.path = db["path"]
            self.im_path = db["image"]
            self.post = db["post"]
            self.code1 = db["voters"]
            self.code3 = db["results"]
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
             self.path = "results.db"
             self.im_path = "logo.jpg"
             self.school = "Unknown"
             self.code1 = "jvoter"
             self.code3 = "results"
             db = anydbm.open("config.db", "c")
             db["color"] = self.color
             db["school"] = self.school
             db["path"] = self.path
             db["image"] = self.im_path
             db["post"] = self.post
             db["voters"] = self.code1
             db["results"] = self.code3
             s = ""
             for i in self.candidates:
                 s = s + i + ";"
             db["names"] = s
             db.close()
        try:
            db = anydbm.open(self.path)
            try:
                count = int(db[self.counter])
                for i in range(number):
                    s = "Candidate " + str(i)
                    c = db[s]
            except:
                count = 0
                for i in range(self.number):
                    s = "Candidate " + str(i)
                    db[s] = "0"
                db.close()
        except:
                db = anydbm.open(self.path, "c")
                for i in range(self.number):
                    s = "Candidate " + str(i)
                    db[s] = "0"
                db[self.counter] = "0"
                count = 0
                db.close()

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
        elif key == "path":
            self.path = value
        elif key == "im_path":
            self.im_path = value
        elif key == "code1":
            self.code1 = value
        elif key == "code3":
            self.code3 = value

       
    def save_settings(self, setting):
        db = anydbm.open("config.db", "c")
        db["names"] = self.temp
        db["number"] = self.number
        db["post"] = self.post
        db["color"] = self.color
        db["school"] = self.school
        db["path"] = self.path
        db["image"] = self.im_path
        db["juniors"] = self.code1
        db["results"] = self.code3
        db.close()
        info_l = Label(text = "The configuration settings have been saved.\nPlease restart the program to apply all saved changes.\nPress Escape to close the settings.")
        info = CustomPopup(title = "Configuration saved", content = info_l)
        info.open()


    def settings_func(self, p, evmgrid):
        s = Settings()
        config = ConfigParser()
        try:
            config.setdefaults('EVM', {'school': self.school, 'names': self.temp, 'post': self.post, 'p_col': self.color, 'path': self.path, 'im_path': self.im_path, "code1": self.code1, "code3": self.code3, 'number':self.number})
        except:
            config.setdefaults('EVM', {'school': 'Unknown', 'names': self.temp, 'post': "Unknown", 'p_col': 'FFFFFF', 'path': self.path, 'im_path': self.im_path, "code1": "jvoter", "code3": "results", 'number':self.number})
        s.add_json_panel('EVM', config, data = self.json)
        s.bind(on_config_change = self.settings_change)
        setting = CustomPopup(title = "Settings", content = s)
        s.bind(on_close = lambda *func: self.save_settings(s))
        setting.open()


    def messageShow(self, passcode, p, evmgrid):
        if passcode == self.code1:
            self.vt = 1
            p.dismiss()
        elif passcode == "exitevm":
            p.dismiss()
            sys.exit()
        elif passcode == self.code3:
            db = anydbm.open(self.path)
            a = db[self.can1]
            b = db[self.can2]
            c = db[self.counter]
            db.close()
            gres = GridLayout(rows = 3)
            l1 = Label(text = self.can1 + " : " + a, font_size = 28)
            l2 = Label(text = self.can2 + " : " + b, font_size = 28)
            l3 = Label(text = "Number of voters : " + c, font_size = 28)
            gres.add_widget(l1)
            gres.add_widget(l2)
            gres.add_widget(l3)
            result = CustomPopup(title = "Results", content = gres)
            p.content.text = ""
            result.open()
        elif passcode == "resetallvotes":
            db = anydbm.open(self.path, "w")
            for key in list(db):
                db[key] = "0"
            db.close()
            p.content.text = ""
        elif passcode == "factoryreset":
            db = anydbm.open(self.path, "w")
            for key in list(db):
                del db[key]
            db.close()
            p.content.text = ""
        elif passcode == "settings":
            self.settings_func(p, evmgrid)
            p.content.text = ""
        elif passcode == "colorpicker":
            color_w = ColorPicker()
            color_p = CustomPopup(title = "Color Picker", content = color_w)
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
        evmgrid = ScrollView()
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
            self.buttons[i].bind(on_press = lambda *f:self.results(self.buttons[i].text, evmgrid))
        evmgrid.add_widget(grid)
        return evmgrid

    def show_popup(self, evmgrid):
        t1 = TextInput(password = True, multiline = False, write_tab = False)
        p = CustomPopup(title = "Enter password", auto_dismiss = False, content = t1, size_hint=(None, None), size=(400, 105), title_align = 'center', separator_height = 3)
        t1.bind(on_text_validate = lambda *func: self.messageShow(t1.text, p, evmgrid))
        p.bind(on_open = self.on_popup_parent)
        p.open()

    def results(self, name, evmgrid):
        if self.vt == 0:
            pass
        else:
            db = anydbm.open(self.path, "w")
            v1 = db[name]
            v1 = float(v1) + self.vt
            db[name] = str(v1)
            count = db[self.counter]
            count = int(count) + 1
            db[self.counter] = str(count)
            db.close()
        self.show_popup(evmgrid)


if __name__ == "__main__":
    EVMApp().run()
