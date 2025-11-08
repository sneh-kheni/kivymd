import kivy
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label
from kivy.uix.button import Button
import google.generativeai as genai
import os

kivy.require('1.0.6')

# Silence logs
os.environ["GRPC_VERBOSITY"] = "NONE"
os.environ["GLOG_minloglevel"] = "2"

# Configure Gemini
genai.configure(api_key="AIzaSyDUBHj48GewPtzog0PxxGRsrFZ-X_eqtyw")  # 👈 Replace with your actual API key
model = genai.GenerativeModel("gemini-2.5-flash")

# Main UI
class UserInterface(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(orientation='vertical', padding=10, spacing=10, **kwargs)

        self.user_input = TextInput(
            hint_text='Type your message...',
            multiline=False,
            font_size=20,
            size_hint_y=None,
            height=50
        )
        self.add_widget(self.user_input)

        send_button = Button(
            text='Ask Gemini 🤖',
            font_size=20,
            size_hint_y=None,
            height=50
        )
        send_button.bind(on_press=self.update_output)
        self.add_widget(send_button)

        self.output_label = Label(
            text='AI response will appear here.',
            font_size=20,
            color=(0.1, 0.5, 0.8, 1)
        )
        self.add_widget(self.output_label)

    def update_output(self, instance):
        user_text = self.user_input.text.strip()
        if not user_text:
            self.output_label.text = "Please type something first!"
            return

        try:
            response = model.generate_content(user_text)
            self.output_label.text = f"AI: {response.text}"
        except Exception as e:
            self.output_label.text = f"Error: {e}"

        self.user_input.text = ''


class InputOutputApp(App):
    def build(self):
        return UserInterface()


if __name__ == '__main__':
    InputOutputApp().run()
