from kivymd.app import MDApp
from kivy.core.window import Window
from kivy.lang import Builder
from kivy.core.clipboard import Clipboard
from kivy.metrics import dp
#from kivymd.toast import toast

from kivymd.uix.snackbar import (
    MDSnackbar,
    MDSnackbarSupportingText,
    MDSnackbarText,
)
from kivymd.uix.list import (
    MDListItem,
    MDListItemHeadlineText,
    MDListItemLeadingIcon)

from kivymd.uix.filemanager import MDFileManager
from kivymd.uix.button import MDIconButton


import webbrowser
import json
import os
import requests



## == Global variables == ##
method = "anon"
period = "1h"
last_screen = "catbox"
current_screen = "catbox"
list_to_show = "anon"

file_cb = r""
file_cb_name = ""
file_lb = r""

cba_items = []
cbb_items = []
lb_items = []

## == Load settings == ##

# Load settings
def load_settings():
    with open('settings.json', 'r') as f:
        settings = json.load(f)
    return settings

# Save settings
def save_settings(settings):
    with open('settings.json', 'w') as f:
        json.dump(settings, f, indent=4)

# List LB
def list_lb():
    with open('list_lb.json', 'r') as f:
        list_lb = json.load(f)
    return list_lb

# List CB-anon
def list_cb_a():
    with open('list_cb_a.json', 'r') as f:
        list_lb = json.load(f)
    return list_lb

# List CB-auth
def list_cb_b():
    with open('list_cb_b.json', 'r') as f:
        list_lb = json.load(f)
    return list_lb



## === App === ##
class MainApp(MDApp):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Window.bind(on_keyboard=self.events)

        # File Manager
        self.manager_open = False

        self.file_manager = MDFileManager(
            exit_manager=self.exit_manager,
            select_path=self.select_path,
            preview=True,
            #ext=[]
        )
        
    def build(self):
        # App color palette
        self.theme_cls.primary_palette = "Midnightblue"
        
        # Load theme
        settings = load_settings()
        current_theme = settings['theme']
        self.theme_cls.theme_style = current_theme
        
        # Load UI file
        return Builder.load_file('ui.kv')

    def on_start(self):
        self.title = "CatBox Client" # App title
        self.add_lb()
        self.add_cb_a()



    ### ===== File manager ===== ###

    # Open file manager
    def file_manager_open(self):
        self.file_manager.show_disks()
        self.file_manager.show(
            os.path.expanduser("~"))
        self.manager_open = True

    def select_path(self, path: str):

        self.exit_manager()

        global file_cb
        global file_cb_name
        global file_lb
        global file_lb_name
        global current_screen

        if os.path.isfile(path):
            print(f"Chosen file: {path}")
            snack_text = f"File: {path}"
        else:
            print("Choose file, not a folder!")
            snack_text = "Choose file, not a folder!"

        MDSnackbar(

            MDSnackbarSupportingText(
                text=snack_text,
            ),

            y=dp(24),
            pos_hint={"center_x": 0.5},
            size_hint_x=0.8,
        ).open()

        
        if current_screen == "catbox":
            file_cb = path
            file_cb_name = os.path.basename(file_cb)
            print("Chosen file for Catbox: ", file_cb)
            print("Chosen name for Catbox: ", file_cb_name)
        else:
            file_lb = path
            file_lb_name = os.path.basename(file_lb)
            print("Chosen file for Litterbox: ", file_lb)
            print("Chosen name for Litterbox:", file_lb_name)

    def exit_manager(self, *args):
        self.manager_open = False
        self.file_manager.close()

    def events(self, instance, keyboard, keycode, text, modifiers):
        if keyboard in (1001, 27):
            if self.manager_open:
                self.file_manager.back()
        return True





### ===== Buttons ===== ###

    # Copy link
    def link(self, option):
        link = option
        Clipboard.copy(link)
        #toast("Link copied to the clipboard")
        print("Link copied to the clipboard")


    # Github
    def github(self):
        webbrowser.open("https://github.com/pythonCBK/catbox-client")

    # Swicth app theme
    def switch_theme(self):
        settings = load_settings()
        current_theme = settings['theme']

        if current_theme == "Light":
            self.theme_cls.theme_style = "Dark"
            new_theme = "Dark"

            settings['theme'] = new_theme
            save_settings(settings)
        else:
            self.theme_cls.theme_style = "Light"
            new_theme = "Light"

            settings['theme'] = new_theme
            save_settings(settings)

    # Save hash
    def save_hash(self):
        settings = load_settings()
        current_hash = settings['userhash']
        new_hash = self.root.ids.entry.text.strip()

        if new_hash == current_hash:
            return
        
        if new_hash == "":
            return

        settings['userhash'] = new_hash
        save_settings(settings)
    
    # Copy userhash
    def copy_hash(self):
        settings = load_settings()
        current_hash = settings['userhash']

        Clipboard.copy(current_hash)

    # Update method
    def method_upd(self, option):
        global method
        method = option
        print("Method updated:", method)

    # Update period
    def period_upd(self, option):
        global period
        period = option
        print("Period updated:", period)
    
    # Update list choise
    def list_choice_upd(self, option):
        global list_to_show

        if option == "anon":
            list_to_show = "anon"
        else:
            list_to_show = "auth"

        print("List to show updated:", list_to_show)



    ### ===== UPLOADS ===== ###


    # Save file Catbox - ANON
    def add_list_cb_a(self, option):
        global file_cb_name

        link = option
        filename = file_cb_name
        datalist = list_cb_a()

        # Object to add
        new_filename = filename
        new_link = {
            "link": link
        }

        datalist[new_filename] = new_link

        with open('list_cb_a.json', 'w', encoding='utf-8') as file:
            json.dump(datalist, file, ensure_ascii=False, indent=4)


    # Save file Catbox - AUTH
    def add_list_cb_b(self, option):
        global file_cb_name

        link = option
        filename = file_cb_name
        datalist = list_cb_b()

        # Object to add
        new_filename = filename
        new_link = {
            "link": link
        }

        datalist[new_filename] = new_link

        with open('list_cb_b.json', 'w', encoding='utf-8') as file:
            json.dump(datalist, file, ensure_ascii=False, indent=4)


    # Save file Litterbox
    def add_list_lb(self, option):
        global file_lb_name

        link = option
        filename = file_lb_name
        datalist = list_lb()

        # Object to add
        new_filename = filename
        new_link = {
            "link": link
        }

        datalist[new_filename] = new_link

        with open('list_lb.json', 'w', encoding='utf-8') as file:
            json.dump(datalist, file, ensure_ascii=False, indent=4)


    # Upload to Catbox - ANON
    def upl_anon(self):
        global file_cb
        url = "https://catbox.moe/user/api.php"

        with open(file_cb, 'rb') as file:
            files = {'fileToUpload': file}
            data = {'reqtype': 'fileupload'}
            
            response = requests.post(url, files=files, data=data)
            
            if response.status_code == 200:
                return response.text.strip()
            else:
                return f"Upload error. Status code: {response.status_code}"


    # Upload to Catbox - AUTH
    def upl_auth(self):
        global file_cb
        url = "https://catbox.moe/user/api.php"

        settings = load_settings()
        userhash = settings['userhash']
        
        with open(file_cb, 'rb') as file:
            files = {'fileToUpload': file}
            data = {
                'reqtype': 'fileupload',
                'userhash': userhash
            }
            
            response = requests.post(url, files=files, data=data)
            
            if response.status_code == 200:
                return response.text.strip()
            else:
                return f"Upload error. Status code: {response.status_code}"


    # Upload to Litterbox
    def upl_lb(self):
        global file_lb
        global period

        url = "https://litterbox.catbox.moe/resources/internals/api.php"
    
        try:
            with open(file_lb, 'rb') as file:
                response = requests.post(
                    url,
                    files={'fileToUpload': file},
                    data={
                        'reqtype': 'fileupload',
                        'time': period
                    }
                )
                return response.text if response.ok else f"Ошибка {response.status_code}"
        except Exception as error:
            return f"Errr: {str(error)}"



    # Call Catbox uploads
    def upload_cb(self):
        global method
        global list_to_show
        global file_cb

        if file_cb == "":
            return
        else:

            if method == "anon":
                result = self.upl_anon()
                print("Anon uploaded file:", result)
                self.add_list_cb_a(result)
            else:
                result = self.upl_auth()
                print("Auth uploaded file:", result)
                self.add_list_cb_b(result)


    # Call Litterbox uploads
    def call_upload_lb(self):
        global file_lb

        if file_lb == "":
            return
        else:
            result = self.upl_lb()
            print("Litterbox uploaded file:", result)
            self.add_list_lb(result)
            self.add_lb()


    # Remove LB
    def remove_from_lb(self, option):

        datalist = list_lb()
        to_remove = option

        if to_remove in datalist:
            del datalist[to_remove]
        else:
            print(f"Name {to_remove} not found!")

        with open('list_lb.json', 'w', encoding='utf-8') as file:
            json.dump(datalist, file, ensure_ascii=False, indent=4)
        
        self.add_lb()


    # Remove CB-a
    def remove_cb_a(self, option):

        datalist = list_cb_a()
        to_remove = option

        if to_remove in datalist:
            del datalist[to_remove]
        else:
            print(f"Name {to_remove} not found!")

        with open('list_cb_a.json', 'w', encoding='utf-8') as file:
            json.dump(datalist, file, ensure_ascii=False, indent=4)
        
        self.add_cb_b()
        self.add_cb_a()


    # Remove CB-b
    def remove_cb_b(self, option):
        global cbb_items

        datalist = list_cb_b()
        to_remove = option
        
        settings = load_settings()
        userhash = settings['userhash']
        url = "https://catbox.moe/user/api.php"

        if to_remove in datalist:
            link = datalist[to_remove]["link"]
            print(link)
        else:
            print(f"File {to_remove} not found")
            return

        link = datalist[to_remove]["link"]
        new_link = link.replace("https://files.catbox.moe/", "")

        # Remove from Catbox
        data = {
        'reqtype': 'deletefiles',
        'files': new_link,
        'userhash': userhash
        }
        
        response = requests.post(url, data=data)

        # Remove from .json
        if to_remove in datalist:
            del datalist[to_remove]
        else:
            print(f"Name {to_remove} not found!")

        with open('list_cb_b.json', 'w', encoding='utf-8') as file:
            json.dump(datalist, file, ensure_ascii=False, indent=4)
        
        self.add_cb_a()
        self.add_cb_b()
        print(response)

        if response.status_code == 200:
            if "success" in response.text.lower():
                return "File was deleted from server"
            else:
                return f"Error: {response.text}"
        else:
            return f"Request error. Error code: {response.status_code}"




### ===== CB List UPDATE ===== ###

    # Remove CB list
    def remove_cb(self, option):
        global cba_items
        global cbb_items

        if option == 'b':
            for item_id in cba_items:
                item = self.root.ids[item_id]
                item.parent.remove_widget(item)
        else:
            for item_id in cbb_items:
                item = self.root.ids[item_id]
                item.parent.remove_widget(item)
        

    # CB-a list
    def add_cb_a(self):
        wordlist = list_cb_a()
        global cba_items

        self.remove_cb('a')
        cba_items.clear()

        # Add to list
        for name in wordlist:

            list_container = self.root.ids.menu_cb
            
            link = wordlist[name]["link"]
            
            ## === Item settings === ##
            item = MDListItem()

            # ID
            item_id = name
            item.my_custom_id = item_id
            
            # Icon
            icon = MDListItemLeadingIcon(
                icon = 'folder-multiple-image')
            item.add_widget(icon)

            # Text
            text = MDListItemHeadlineText(
                text = name)
            item.add_widget(text)

            # Buttons
            btn1 = MDIconButton(
                icon = 'link',
                on_release=
                lambda x, link=link: self.link(link)
            )
            btn2 = MDIconButton(
                icon = 'close-circle-outline',
                on_release=
                lambda x, name=name: self.remove_cb_a(name)
            )
            item.add_widget(btn1)
            item.add_widget(btn2)

            # Adding item
            list_container.add_widget(item)

            self.root.ids[item_id] = item
            cba_items.append(item_id)

        print("CB-a items:", cba_items)


    # CB-b list
    def add_cb_b(self):
        wordlist = list_cb_b()
        global cbb_items

        self.remove_cb('b')
        cbb_items.clear()

        # Add to list
        for name in wordlist:

            list_container = self.root.ids.menu_cb

            link = wordlist[name]["link"]
            
            ## === Item settings === ##
            item = MDListItem()

            # ID
            item_id = name
            item.my_custom_id = item_id
            
            # Icon
            icon = MDListItemLeadingIcon(
                icon = 'folder-multiple-image')
            item.add_widget(icon)

            # Text
            text = MDListItemHeadlineText(
                text = name)
            item.add_widget(text)

            # Buttons
            btn1 = MDIconButton(
                icon = 'link',
                on_release=
                lambda x, link=link: self.link(link)
            )
            btn2 = MDIconButton(
                icon = 'close-circle-outline',
                on_release=
                lambda x, name=name: self.remove_cb_b(name)
            )
            item.add_widget(btn1)
            item.add_widget(btn2)

            # Adding item
            list_container.add_widget(item)

            self.root.ids[item_id] = item
            cbb_items.append(item_id)

        print("CB-b items:", cbb_items)




### ===== LB List UPDATE ===== ###

    # Remove LB list
    def remove_lb(self):
        global lb_items

        for item_id in lb_items:
            item = self.root.ids[item_id]
            item.parent.remove_widget(item)
        
    # Add LB list
    def add_lb(self):
        wordlist = list_lb()
        global lb_items

        self.remove_lb()
        lb_items.clear()

        # Add to list
        for name in wordlist:

            list_container = self.root.ids.menu_lb

            link = wordlist[name]["link"]
            
            ## === Item settings === ##
            item = MDListItem()

            # ID
            item_id = name
            item.my_custom_id = item_id
            
            # Icon
            icon = MDListItemLeadingIcon(
                icon = 'folder-multiple-image')
            item.add_widget(icon)

            # Text
            text = MDListItemHeadlineText(
                text = name)
            item.add_widget(text)

            # Buttons
            btn1 = MDIconButton(
                icon = 'link',
                on_release=
                lambda x, link=link: self.link(link)
            )
            btn2 = MDIconButton(
                icon = 'close-circle-outline',
                on_release=
                lambda x, name=name: self.remove_from_lb(name)
            )
            
            item.add_widget(btn1)
            item.add_widget(btn2)

            # Adding item
            list_container.add_widget(item)

            self.root.ids[item_id] = item
            lb_items.append(item_id)

        print("LB items:", lb_items)




    ### ===== Settings ===== ###

    # Current Screen upd
    def current_screen_upd(self):
        global current_screen
        if current_screen == "catbox":
            current_screen = "litterbox"
        else:
            current_screen = "catbox"
        print("Current screen:", current_screen)

    # Last Screen upd to cb
    def last_screen(self):
        global last_screen
        global current_screen
        if current_screen == "catbox":
            last_screen = "catbox"
        else:
            last_screen = "litterbox"

    # Go back
    def back(self):
        global last_screen
        if last_screen == "litterbox":
            self.root.current = "litterbox"
        else:
            self.root.current = "catbox"


### === Notifications === ###

    # Show current userhash
    def show_hash(self):
        settings = load_settings()
        current_hash = settings['userhash']

        if current_hash == "":
            support_text = "No userhash provided"
        else:
            support_text = current_hash

        show = MDSnackbar(
            MDSnackbarText(
                text = "Current userhash:",
            ),
            MDSnackbarSupportingText(
                text = support_text,
            ),
            y=dp(10),
            orientation="horizontal",
            pos_hint={"center_x": 0.5},
            size_hint_x=0.8,
        )
        show.open()


MainApp().run()