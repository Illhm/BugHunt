from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from kivy.uix.label import Label
import os
from main import parse_vless_url, check_vless_connection, load_bugs_from_file

class Layout(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(orientation='vertical', spacing=10, padding=10, **kwargs)
        self.entry = TextInput(hint_text='Domain atau file', size_hint_y=None, height=40)
        self.add_widget(self.entry)
        btn = Button(text='Scan', size_hint_y=None, height=40)
        btn.bind(on_release=self.scan)
        self.add_widget(btn)
        self.out = Label(size_hint_y=None, halign='left', valign='top')
        self.out.bind(size=self.out.setter('text_size'))
        sc = ScrollView()
        sc.add_widget(self.out)
        self.add_widget(sc)
        self.proxy = parse_vless_url('vless://8e1de14a-6873-4c92-b5bf-f9cb25aedb97@kang.cepu.us.kg:443?encryption=none&security=tls&sni=kang.cepu.us.kg&fp=randomized&type=ws&host=kang.cepu.us.kg&path=/146.235.18.248=45137#GUI')

    def scan(self, *args):
        target = self.entry.text.strip()
        if not target:
            return
        bugs = load_bugs_from_file(target) if os.path.isfile(target) else [target]
        self.out.text = ''
        for bug in bugs:
            cfg = self.proxy.copy()
            cfg['server'] = bug
            status = 'Terkoneksi' if check_vless_connection(cfg, timeout=10) else 'Gagal'
            self.out.text += f'{bug} - {status}\n'

class BugHuntApp(App):
    def build(self):
        return Layout()

if __name__ == '__main__':
    BugHuntApp().run()
