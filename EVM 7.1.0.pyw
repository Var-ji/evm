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

Config.set('kivy', 'exit_on_escape', 0)


class CustomPopup(Popup):
    pass


class EVMApp(App):
    def __init__(self, **kwargs):
        super(EVMApp, self).__init__(**kwargs)
        self.vt = 0
        self.can1 = self.can2 = None
        self.counter = None
        self.indicator_vc_c = None
        self.color = ""
        self.flag = None
        self.path = ""
        self.im_path = ""
        self.school = ""
        self.code1 = ""
        self.code2 = ""
        self.code3 = ""
        self.json = '''
        [
            {
                "type": "string",
                "title": "School Name",
                "desc": "Set the school name! It defaults to Unknown otherwise",
                "section": "EVM",
                "key": "school"
            },
            {
                "type": "string",
                "title": "Candidate 1's name",
                "desc": "Set the name of the first candidate",
                "section": "EVM",
                "key": "name1"
            },
            {
                "type": "string",
                "title": "Candidate 2's name",
                "desc": "Set the name of the second candidate",
                "section": "EVM",
                "key": "name2"
            },
            {
                "type": "string",
                "title": "House",
                "desc": "Set the text for the post",
                "section": "EVM",
                "key": "house"
            },
            {
                "type": "string",
                "title": "Color of house",
                "desc": "Set the color for the given house. Use the color picker to select the color. Enter it in hex format.",
                "section": "EVM",
                "key": "h_col"
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
                "type": "bool",
                "title": "Vice Captain?",
                "desc": "Are the elections for vice captain?",
                "section": "EVM",
                "key": "vc_flag"
            },
            {
                "type": "string",
                "title": "Password for Juniors",
                "desc": "Set the password for the junior section. Note that the junior section has a weightage of 1 per voter.",
                "section": "EVM",
                "key": "code1"
            },
            {
                "type": "string",
                "title": "Password for Seniors",
                "desc": "Set the password for the senior section. Note that the senior section has a weightage of 1.5 per voter.",
                "section": "EVM",
                "key": "code2"
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
            self.can1 = db["name1"]
            self.can2 = db["name2"]
            color1 = db["color"]
            self.school = db["school"]
            self.flag = db["flag"]
            self.path = db["path"]
            self.im_path = db["image"]
            self.indicator = db["indicator"]
            self.code1 = db["juniors"]
            self.code2 = db["seniors"]
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
            temp = self.indicator.split(' '); house = temp[0];
            if "vc" in self.flag.lower():
                self.counter = "counter" + house + "vc"
                self.indicator_vc_c = house + " House Vice Captain"
                if "school" in house.lower():
                    self.indicator_vc_c = "School Vice Captain"
            else:
                self.counter = "counter" + house
                self.indicator_vc_c = house + " House Captain"
                if "school" in house.lower():
                    self.indicator_vc_c = "School Captain"

        except:
             self.can1 = "CANDIDATE 1"
             self.can2 = "CANDIDATE 2"
             self.color = "FFFFFF"
             self.indicator_vc_c = "Unknown"
             self.path = "results.db"
             self.im_path = "logo.jpg"
             self.school = "Unknown"
             self.flag = "Flag = C"
             self.code1 = "jvoter"
             self.code2 = "svoter"
             self.code3 = "results"
             db = anydbm.open("config.db", "c")
             db["name1"] = self.can1
             db["name2"] = self.can2
             db["color"] = self.color
             db["school"] = self.school
             db["flag"] = self.flag
             db["path"] = self.path
             db["image"] = self.im_path
             db["indicator"] = self.indicator_vc_c
             db["juniors"] = self.code1
             db["seniors"] = self.code2
             db["results"] = self.code3
             db.close()
        try:
            db = anydbm.open(self.path)
            try:
                count = int(db[self.counter])
                c1 = db[self.can1]
                c2 = db[self.can2]
            except:
                count = 0
                db[self.can1] = "0"
                db[self.can2] = "0"
                db.close()
        except:
                db = anydbm.open(self.path, "c")
                db[self.can1] = "0"
                db[self.can2] = "0"
                db[self.counter] = "0"
                count = 0
                db.close()

    def settings_change(self, config, section, key, value):
        if key == "school":
            self.school = value
        elif key == "name1":
            self.can1 = value
        elif key == "name2":
            self.can2 = value
        elif key == "house":
            self.indicator_vc_c = value
        elif key == "h_col":
            self.color = value
        elif key == "path":
            self.path = value
        elif key == "im_path":
            self.im_path = value
        elif key == "vc_flag":
            if value == '0':
                self.flag = "Flag = C"
            if value == '1':
                self.flag = "Flag = VC"
        elif key == "code1":
            self.code1 = value
        elif key == "code2":
            self.code2 = value
        elif key == "code3":
            self.code3 = value

       
    def save_settings(self, setting):
        db = anydbm.open("config.db", "c")
        db["name1"] = self.can1
        db["name2"] = self.can2
        db["color"] = self.color
        db["school"] = self.school
        db["flag"] = self.flag
        db["path"] = self.path
        db["image"] = self.im_path
        db["indicator"] = self.indicator_vc_c
        db["juniors"] = self.code1
        db["seniors"] = self.code2
        db["results"] = self.code3
        db.close()
        info_l = Label(text = "The configuration settings have been saved.\nPlease restart the program to apply all saved changes.\nPress Escape to close the settings.")
        info = CustomPopup(title = "Configuration saved", content = info_l)
        info.open()


    def settings_func(self, p, evmgrid):
        s = Settings()
        config = ConfigParser()
        try:
            if "vc" in flag.lower():
                config.setdefaults('EVM', {'school': self.school, 'name1': self.can1, 'name2': self.can2, 'house': self.indicator_vc_c, 'h_col': self.color, 'path': self.path, 'im_path': self.im_path, 'vc_flag': True, "code1": self.code1, "code2": self.code2, "code3": self.code3})
            else:
                config.setdefaults('EVM', {'school': self.school, 'name1': self.can1, 'name2': self.can2, 'house': self.indicator_vc_c, 'h_col': self.color, 'path': self.path, 'im_path': self.im_path, 'vc_flag': False, "code1": self.code1, "code2": self.code2, "code3": self.code3})
        except:
            config.setdefaults('EVM', {'school': 'Unknown', 'name1': self.can1, 'name2': self.can2, 'house': "Unknown", 'h_col': 'FFFFFF', 'path': self.path, 'im_path': self.im_path, 'vc_flag': False, "code1": "jvoter", "code2": "svoter", "code3": "results"})
        s.add_json_panel('EVM', config, data = self.json)
        s.bind(on_config_change = self.settings_change)
        setting = CustomPopup(title = "Settings", content = s)
        s.bind(on_close = lambda *func: self.save_settings(s))
        setting.open()


    def messageShow(self, passcode, p, evmgrid):
        if passcode == self.code1:
            self.vt = 1
            p.dismiss()
        elif passcode == self.code2:
            self.vt = 1.5
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
        indicator_l = color2 + self.indicator_vc_c + "[/color]"
        #Window.fullscreen = "auto"
        Window.window_state = "maximized"
        Window.bind(on_request_close = self.close_event)
        evmgrid = GridLayout(rows = 4, padding = [50, 50, 50, 50], spacing = [5, 25])
        titlegrid = GridLayout(cols = 2, padding = [250, 0, 450, 0])
        cand1 = Button(text = self.can1, font_size = 24)
        cand2 = Button(text = self.can2, font_size = 24)
        try:
            image = Image(source = self.im_path)
            titlegrid.add_widget(image)
        except:
            pass
        titlename = Label(text = self.school, font_size = 36)
        indicator_label = Label(text = indicator_l, font_size = 28, markup = True)
        titlegrid.add_widget(titlename)
        evmgrid.add_widget(titlegrid)
        evmgrid.add_widget(indicator_label)
        evmgrid.add_widget(cand1)
        evmgrid.add_widget(cand2)
        cand1.bind(on_press = lambda *f1: self.results(self.can1, evmgrid))
        cand2.bind(on_press = lambda *f2: self.results(self.can2, evmgrid))
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
        elif name == self.can1:
            db = anydbm.open(self.path, "w")
            v1 = db[name]
            v1 = float(v1) + self.vt
            db[name] = str(v1)
            count = db[self.counter]
            count = int(count) + 1
            db[self.counter] = str(count)
            db.close()
        elif name == self.can2:
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
