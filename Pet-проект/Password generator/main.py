from string import ascii_lowercase, ascii_uppercase, digits, punctuation
import tkinter as tk
from PIL import Image
import customtkinter as CTk
import secrets

class PasswordGenerator:
    @staticmethod
    def create_new(length: int, characters: str) -> str:
        if not characters:
            return "Select character sets!"
        return ''.join(secrets.choice(characters) for _ in range(length))

class App(CTk.CTk):
    def __init__(self):
        super().__init__()

        self.geometry("460x360")  # Увеличили высоту окна
        self.title("Password Generator")
        self.resizable(False, False)

        # Контейнер для уведомлений
        self.notification_frame = CTk.CTkFrame(self, height=30, fg_color="transparent")
        self.notification_frame.grid(row=3, column=0, padx=20, pady=(0, 10), sticky="ew")
        
        self.notification_label = CTk.CTkLabel(
            self.notification_frame, 
            text="",
            fg_color="transparent",
            font=("Arial", 12)
        )
        self.notification_label.pack(expand=True)

        try:
            self.logo = CTk.CTkImage(dark_image=Image.open("img.png"), size=(460, 150))
            self.logo_label = CTk.CTkLabel(master=self, text="", image=self.logo)
            self.logo_label.grid(row=0, column=0)
        except FileNotFoundError:
            self.logo_label = CTk.CTkLabel(master=self, text="Password Generator", font=("Arial", 24))
            self.logo_label.grid(row=0, column=0, pady=20)

        self.password_frame = CTk.CTkFrame(master=self, fg_color="transparent")
        self.password_frame.grid(row=1, column=0, padx=20, pady=(20, 0), sticky="nsew")

        self.entry_password = CTk.CTkEntry(master=self.password_frame, width=300)
        self.entry_password.grid(row=0, column=0, padx=(0, 20))

        self.btn_generate = CTk.CTkButton(
            master=self.password_frame,
            text="Generate",
            width=100,
            command=self.set_password
        )
        self.btn_generate.grid(row=0, column=1)


        self.settings_frame = CTk.CTkFrame(master=self)
        self.settings_frame.grid(row=2, column=0, padx=20, pady=20, sticky="nsew")

        self.password_length_slider = CTk.CTkSlider(
            master=self.settings_frame,
            from_=8,  # Минимальная длина 8 символов
            to=50,
            number_of_steps=42,
            command=self.slider_event
        )
        self.password_length_slider.grid(row=1, column=0, columnspan=3, pady=(20, 10), sticky="ew")

        self.password_length_entry = CTk.CTkEntry(master=self.settings_frame, width=50)
        self.password_length_entry.grid(row=1, column=3, padx=(20, 10), sticky="we")

        self.checkbox_vars = {
            'digits': tk.StringVar(value=digits),
            'lower': tk.StringVar(value=ascii_lowercase),
            'upper': tk.StringVar(value=ascii_uppercase),
            'symbols': tk.StringVar(value=punctuation)
        }

        self.cb_digits = CTk.CTkCheckBox(
            master=self.settings_frame,
            text="0-9",
            variable=self.checkbox_vars['digits'],
            onvalue=digits,
            offvalue=""
        )
        self.cb_digits.grid(row=2, column=0, padx=10)

        self.cb_lower = CTk.CTkCheckBox(
            master=self.settings_frame,
            text="a-z",
            variable=self.checkbox_vars['lower'],
            onvalue=ascii_lowercase,
            offvalue=""
        )
        self.cb_lower.grid(row=2, column=1)

        self.cb_upper = CTk.CTkCheckBox(
            master=self.settings_frame,
            text="A-Z",
            variable=self.checkbox_vars['upper'],
            onvalue=ascii_uppercase,
            offvalue=""
        )
        self.cb_upper.grid(row=2, column=2)

        self.cb_symbols = CTk.CTkCheckBox(
            master=self.settings_frame,
            text="@#$%",
            variable=self.checkbox_vars['symbols'],
            onvalue=punctuation,
            offvalue=""
        )
        self.cb_symbols.grid(row=2, column=3)

        self.appearance_mode_option_menu = CTk.CTkOptionMenu(
            self.settings_frame,
            values=["Light", "Dark", "System"],
            command=self.change_appearance_mode_event
        )
        self.appearance_mode_option_menu.grid(row=3, column=0, columnspan=4, pady=(10, 10))

        self.appearance_mode_option_menu.set("System")
        self.password_length_slider.set(12)
        self.password_length_entry.insert(0, "12")

    def slider_event(self, value):
        self.password_length_entry.delete(0, 'end')
        self.password_length_entry.insert(0, str(int(value)))

    def change_appearance_mode_event(self, new_appearance_mode):
        CTk.set_appearance_mode(new_appearance_mode)

    def get_characters(self):
        return ''.join(var.get() for var in self.checkbox_vars.values())

    def set_password(self):
        try:
            length = int(self.password_length_slider.get())
            characters = self.get_characters()

            if not characters:
                raise ValueError("Select at least one character set")

            password = PasswordGenerator.create_new(length, characters)
            self.entry_password.delete(0, 'end')
            self.entry_password.insert(0, password)

        except ValueError as e:
            self.entry_password.delete(0, 'end')
            self.entry_password.insert(0, str(e))

    def show_notification(self, message: str, is_success: bool = True):
        """Показывает уведомление в основном окне"""
        fg_color = "#2AA876" if is_success else "#E74C3C"
        text_color = "white"
        
        self.notification_label.configure(
            text=message,
            fg_color=fg_color,
            text_color=text_color
        )
        
        # Автоматическое скрытие через 3 секунды
        self.after(3000, lambda: self.notification_label.configure(
            text="",
            fg_color="transparent"
        ))

    def copy_to_clipboard(self):
        password = self.entry_password.get()
        if password and password != "Select character sets!":
            self.clipboard_clear()
            self.clipboard_append(password)
            self.show_notification("Password copied to clipboard!", is_success=True)
        else:
            self.show_notification("Nothing to copy!", is_success=False)

if __name__ == "__main__":
    app = App()
    app.mainloop()
