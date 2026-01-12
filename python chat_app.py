from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.clock import Clock
from datetime import datetime
from kivy.core.window import Window
from kivy.utils import get_color_from_hex
from kivy.graphics import Color, RoundedRectangle

# Optional: Set window size
Window.size = (400, 600)

class ChatApp(App):
    def build(self):
        main_layout = BoxLayout(orientation='vertical', padding=10, spacing=10)

        # Scrollable chat area
        self.chat_layout = GridLayout(cols=1, spacing=10, size_hint_y=None)
        self.chat_layout.bind(minimum_height=self.chat_layout.setter('height'))

        self.scroll_view = ScrollView(size_hint=(1, 0.85))
        self.scroll_view.add_widget(self.chat_layout)

        # Input field + send button
        input_layout = BoxLayout(size_hint=(1, 0.1), spacing=10)
        self.user_input = TextInput(multiline=False, hint_text="Type a message...")
        send_button = Button(text="Send", size_hint=(0.2, 1))
        send_button.bind(on_press=self.send_message)

        input_layout.add_widget(self.user_input)
        input_layout.add_widget(send_button)

        main_layout.add_widget(self.scroll_view)
        main_layout.add_widget(input_layout)

        return main_layout

    def send_message(self, instance):
        message = self.user_input.text.strip()
        if message:
            self.add_message(message, sent_by_user=True)
            self.user_input.text = ""
            Clock.schedule_once(lambda dt: self.scroll_view.scroll_to(self.chat_layout.children[0]), 0.1)
            Clock.schedule_once(lambda dt: self.add_message("This is a reply!", sent_by_user=False), 1)

    def add_message(self, message, sent_by_user=True):
        time_stamp = datetime.now().strftime("%H:%M")
        full_text = f"{message}\n{time_stamp}"

        # Bubble alignment
        halign = 'right' if sent_by_user else 'left'
        color = get_color_from_hex("#25D366") if sent_by_user else get_color_from_hex("#E5E5EA")
        text_color = get_color_from_hex("#FFFFFF") if sent_by_user else get_color_from_hex("#000000")

        # Bubble label
        label = Label(
            text=full_text,
            size_hint_y=None,
            halign=halign,
            valign='middle',
            text_size=(250, None),
            padding=(10,10),
            color=text_color,
            markup=True
        )

        # Update label height dynamically
        label.bind(texture_size=lambda instance, value: setattr(label, 'height', value[1]+20))

        # Add rounded rectangle background
        with label.canvas.before:
            Color(*color)
            label.bg = RoundedRectangle(pos=label.pos, size=label.size, radius=[10])
        label.bind(pos=self.update_bg, size=self.update_bg)

        self.chat_layout.add_widget(label, index=0)

    def update_bg(self, instance, value):
        instance.bg.pos = instance.pos
        instance.bg.size = instance.size

if __name__ == "__main__":
    ChatApp().run()