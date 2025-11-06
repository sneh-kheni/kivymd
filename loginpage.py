from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.core.window import Window
from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
# REMOVE: from kivymd.uix.divider import MDDivider
from kivymd.uix.label import MDLabel
from kivymd.uix.button import MDButton # Corrected Button Import
# REMOVE: from kivymd.uix.button import MDIconButton (unless you use it)
from kivymd.uix.card import MDCard
from kivymd.uix.fitimage import FitImage # Corrected FitImage Import
from kivymd.uix.textfield import MDTextField

# Set a fixed size for the window for development convenience
Window.size = (400, 700)

class ProfileScreen(MDScreen):
    pass

class LoginApp(MDApp):
    def build(self):
        self.theme_cls.primary_palette = "Teal"  # Modern primary color
        self.theme_cls.accent_palette = "LightGreen" # A nice accent
        self.theme_cls.theme_style = "Light" # Default to light theme

        # Load the KV file for the screen
        Builder.load_file('login.kv') # Assuming your KV file is named login.kv
                                      # If it's profile_design.kv, change this line!

        # Set up the screen manager
        sm = ScreenManager()
        sm.add_widget(ProfileScreen(name='profile'))
        return sm

    def toggle_dark_mode(self, active):
        """Toggles between 'Light' and 'Dark' themes."""
        self.theme_cls.theme_style = "Dark" if active else "Light"
        print(f"Theme switched to: {self.theme_cls.theme_style}")

    def edit_profile(self):
        print("Edit Profile button pressed!")

    def show_settings(self):
        print("Settings button pressed!")

    def on_start(self):
        pass

if __name__ == '__main__':
    LoginApp().run()