import string
import secrets
import pyperclip
import sys

from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivymd.uix.textfield import MDTextField
from kivymd.uix.button import MDButton, MDButtonText, MDIconButton
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.slider import MDSlider
from kivymd.uix.label import MDLabel
from kivymd.uix.selectioncontrol import MDCheckbox
from kivymd.uix.dialog import MDDialog, MDDialogSupportingText
from kivy.metrics import dp
from kivy.core.window import Window

# Optional: Set a fixed window size for better desktop view
Window.size = (400, 600)


class PasswordGeneratorApp(MDApp):
    """KivyMD app for generating secure random passwords."""

    def build(self):
        self.title = "Secure Password Generator"
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "Teal"
        self.theme_cls.accent_palette = "Blue"

        # --- Password Generator Logic Variables ---
        self.password_len = 12
        self.include_upper = True
        self.include_lower = True
        self.include_digits = True
        self.include_symbols = False

        # --- UI Layout ---
        self.screen = MDScreen()

        # Main vertical layout
        main_layout = MDBoxLayout(
            orientation="vertical",
            spacing=dp(20),
            padding=dp(30),
            size_hint_y=None,
            height=dp(550),
            pos_hint={"center_x": 0.5, "center_y": 0.5},
        )

        # --- 1. Title and Output ---
        main_layout.add_widget(
            MDLabel(text="Password Generator",
                    halign="center",
                    font_size="24sp",
                    bold=True)
        )

        # Text Field to Display Output Password
        self.output_field = MDTextField(
            hint_text="Generated Password",
            mode="outlined",  # <-- FINAL FIX: Changed deprecated 'rectangle' to 'outlined'
            readonly=True,
            font_size=dp(18),
            size_hint_x=1
        )
        main_layout.add_widget(self.output_field)

        # Copy Button
        copy_button = MDIconButton(
            icon="content-copy",
            pos_hint={"center_x": 0.5},
            on_release=self.copy_password,
        )
        main_layout.add_widget(copy_button)

        # --- 2. Length Slider ---
        main_layout.add_widget(
            MDLabel(text="Password Length:", halign="left", font_size="16sp")
        )
        self.len_label = MDLabel(text=f"{self.password_len}", halign="right", font_size="16sp")

        slider_layout = MDBoxLayout(orientation="horizontal", spacing=dp(10), size_hint_y=None, height=dp(30))
        self.slider = MDSlider(
            min=8, max=32, value=self.password_len, step=1,
            size_hint_x=0.8,
            on_value_change=self.update_length
        )
        slider_layout.add_widget(self.slider)
        slider_layout.add_widget(self.len_label)
        main_layout.add_widget(slider_layout)

        # --- 3. Checkboxes for Character Sets ---
        main_layout.add_widget(MDLabel(text="Include Character Types:", halign="left", font_size="16sp"))

        # Helper function to create checkbox rows
        def create_checkbox_row(text, active_state, callback):
            box = MDBoxLayout(orientation="horizontal", spacing=dp(10), size_hint_y=None, height=dp(30))
            checkbox = MDCheckbox(active=active_state, size_hint=(None, None), size=(dp(48), dp(48)),
                                  on_release=callback)
            label = MDLabel(text=text, font_size="14sp")
            box.add_widget(checkbox)
            box.add_widget(label)
            return box

        main_layout.add_widget(
            create_checkbox_row("Uppercase (A-Z)", self.include_upper, lambda x: self.toggle_char_set('upper')))
        main_layout.add_widget(
            create_checkbox_row("Lowercase (a-z)", self.include_lower, lambda x: self.toggle_char_set('lower')))
        main_layout.add_widget(
            create_checkbox_row("Digits (0-9)", self.include_digits, lambda x: self.toggle_char_set('digits')))
        main_layout.add_widget(
            create_checkbox_row("Symbols (!@#...)", self.include_symbols, lambda x: self.toggle_char_set('symbols')))

        # --- 4. Generate Button ---
        generate_button = MDButton(
            MDButtonText(
                text="Generate Password"
            ),
            style="filled",
            on_release=self.generate_password,
            pos_hint={"center_x": 0.5},
            size_hint_x=1
        )
        main_layout.add_widget(generate_button)

        self.screen.add_widget(main_layout)
        return self.screen

    # --- App Methods (Unchanged) ---

    def update_length(self, instance, value):
        self.password_len = int(value)
        self.len_label.text = str(self.password_len)

    def toggle_char_set(self, set_type):
        if set_type == 'upper':
            self.include_upper = not self.include_upper
        elif set_type == 'lower':
            self.include_lower = not self.include_lower
        elif set_type == 'digits':
            self.include_digits = not self.include_digits
        elif set_type == 'symbols':
            self.include_symbols = not self.include_symbols

    def generate_password(self, *args):
        chars = ''
        if self.include_upper:
            chars += string.ascii_uppercase
        if self.include_lower:
            chars += string.ascii_lowercase
        if self.include_digits:
            chars += string.digits
        if self.include_symbols:
            chars += string.punctuation

        if not chars:
            self.show_error_dialog("Please select at least one character type.")
            return

        password = ''.join(secrets.choice(chars) for _ in range(self.password_len))
        self.output_field.text = password

    def copy_password(self, *args):
        password = self.output_field.text
        if not password:
            self.show_error_dialog("Nothing to copy. Generate a password first.")
            return

        try:
            pyperclip.copy(password)
            self.show_info_dialog("Password copied to clipboard!")
        except NameError:
            self.show_error_dialog(
                "The 'pyperclip' module is not installed. Run 'pip install pyperclip' to enable copy.")
        except Exception as e:
            self.show_error_dialog(f"Could not access clipboard: {e}")

    def show_info_dialog(self, text):
        dialog = MDDialog(
            MDDialogSupportingText(text=text),
            buttons=[
                MDButton(
                    MDButtonText(text="CLOSE"),
                    on_release=lambda x: dialog.dismiss(),
                )
            ],
        )
        dialog.open()

    def show_error_dialog(self, text):
        dialog = MDDialog(
            MDDialogSupportingText(text=text),
            buttons=[
                MDButton(
                    MDButtonText(text="OK"),
                    on_release=lambda x: dialog.dismiss(),
                )
            ],
        )
        dialog.open()


if __name__ == "__main__":
    try:
        import pyperclip
    except ImportError:
        print("\n" + "=" * 50)
        print("🚨 CRITICAL: 'pyperclip' module not found. Run 'pip install pyperclip'.")
        print("=" * 50 + "\n")

    PasswordGeneratorApp().run()