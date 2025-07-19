import customtkinter as ctk
import psycopg2

class DuoApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        # Настройка главного окна
        self.title("Duo")
        self.geometry("540x480")
        self.resizable(False, False)
        self.iconbitmap("icon.ico")
        ctk.set_appearance_mode("Light")

        # Инициализация виджетов
        self.add_word_label = None
        self.english_entry = None
        self.translation_entry = None
        self.add_button = None

        # Подключение к базе данных
        self.conn = psycopg2.connect(
            dbname="duo",
            user="postgres",
            password="123",
            host="localhost",
            port="5432"
        )
        self.cursor = self.conn.cursor()

        # Создание интерфейса
        self.create_widgets()

    def create_widgets(self):
        # Основной фрейм
        self.main_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.main_frame.pack(pady=20, padx=20, fill="both", expand=True)

        # Фрейм для уведомлений
        self.notification_frame = ctk.CTkFrame(
            self.main_frame,
            height=40,
            corner_radius=10,
            fg_color="transparent"
        )
        self.notification_label = ctk.CTkLabel(
            self.notification_frame,
            text="",
            font=("Roboto", 12),
            wraplength=400,
            anchor="w"
        )
        self.close_button = ctk.CTkButton(
            self.notification_frame,
            text="✕",
            width=28,
            height=28,
            fg_color="transparent",
            hover_color="#444444",
            command=self.hide_message
        )

        # Меню
        self.menu_label = ctk.CTkLabel(
            self.main_frame,
            text="Меню",
            font=("Roboto", 20, "bold"),
            fg_color="transparent"
        )
        self.menu_label.pack(pady=(10, 15))

        # Кнопки меню
        self.buttons_frame = ctk.CTkFrame(self.main_frame)
        self.buttons_frame.pack(pady=10)

        self.words_button = ctk.CTkButton(
            self.buttons_frame,
            text="Слова",
            command=self.show_random_word,
            width=150,
            height=40
        )
        self.words_button.pack(side=ctk.LEFT, padx=5)

        self.pair_button = ctk.CTkButton(
            self.buttons_frame,
            text="Пара",
            command=self.start_pair_mode,
            width=150,
            height=40
        )
        self.pair_button.pack(side=ctk.LEFT, padx=5)

        self.add_words_button = ctk.CTkButton(
            self.buttons_frame,
            text="Добавить слова",
            command=self.on_add_words_button_click,
            width=150,
            height=40
        )
        self.add_words_button.pack(side=ctk.LEFT, padx=5)

        # Виджеты для режимов
        self.word_label = ctk.CTkLabel(
            self.main_frame,
            text="",
            font=("Roboto", 16),
            fg_color="transparent"
        )
        
        self.translation_label = ctk.CTkLabel(
            self.main_frame,
            text="",
            font=("Roboto", 14),
            fg_color="transparent"
        )
        
        self.next_button = ctk.CTkButton(
            self.main_frame,
            text="Следующее",
            command=self.show_random_word,
            width=150,
            height=40
        )

        self.pair_word_label = ctk.CTkLabel(
            self.main_frame,
            text="",
            font=("Roboto", 16),
            fg_color="transparent"
        )
        
        self.pair_entry = ctk.CTkEntry(self.main_frame, width=150)
        
        self.pair_check_button = ctk.CTkButton(
            self.main_frame,
            text="Проверить",
            command=self.check_pair_answer,
            width=150,
            height=40
        )

        self.next_pair_button = ctk.CTkButton(
            self.main_frame,
            text="Следующее",
            command=self.next_pair_word,
            width=150,
            height=40
        )

    def show_message(self, text, message_type="info"):
        colors = {
            "error": {"fg": "#ff4444", "bg": "#2b0b0b"},
            "success": {"fg": "#00C853", "bg": "#0d2b16"},
            "warning": {"fg": "#ff9100", "bg": "#2b200b"}
        }

        self.notification_frame.configure(fg_color=colors[message_type]["bg"])
        self.notification_label.configure(
            text=text,
            text_color=colors[message_type]["fg"]
        )
        self.notification_label.pack(side=ctk.LEFT, padx=10, fill='x', expand=True)
        self.close_button.pack(side=ctk.RIGHT, padx=5)
        self.notification_frame.pack(pady=5, fill='x')
        self.after(5000, self.hide_message)

    def hide_message(self):
        self.notification_frame.pack_forget()

    def hide_all_widgets(self):
        widgets = [
            self.word_label, self.translation_label, self.next_button,
            self.pair_word_label, self.pair_entry, 
            self.pair_check_button, self.next_pair_button
        ]
        for widget in widgets:
            widget.pack_forget()
        
        if self.add_word_label:
            self.add_word_label.pack_forget()
            self.english_entry.pack_forget()
            self.translation_entry.pack_forget()
            self.add_button.pack_forget()
        
        self.hide_message()

    def show_random_word(self):
        self.hide_all_widgets()
        try:
            self.cursor.execute("SELECT w_text, translate FROM words ORDER BY RANDOM() LIMIT 1")
            result = self.cursor.fetchone()
            if result:
                word, translation = result
                self.word_label.configure(text=f"Слово: {word}")
                self.translation_label.configure(text=f"Перевод: {translation}")
                self.word_label.pack(pady=(10, 5))
                self.translation_label.pack(pady=5)
                self.next_button.pack(pady=(10, 20))
            else:
                self.show_message("База данных пуста", "warning")
        except Exception as e:
            self.conn.rollback()
            self.show_message(f"Ошибка БД: {str(e)}", "error")

    def start_pair_mode(self):
        self.hide_all_widgets()
        try:
            self.cursor.execute("SELECT w_text, translate FROM words ORDER BY RANDOM() LIMIT 1")
            result = self.cursor.fetchone()
            if result:
                self.current_word, self.correct_translation = result
                self.pair_word_label.configure(text=f"Слово: {self.current_word}")
                self.pair_word_label.pack(pady=(10, 5))
                self.pair_entry.pack(pady=5)
                self.pair_check_button.pack(pady=5)
                self.next_pair_button.pack(pady=5)
                self.pair_check_button.configure(
                    text="Проверить",
                    fg_color="#3B8EC2",
                    text_color="white"
                )
        except Exception as e:
            self.conn.rollback()
            self.show_message(f"Ошибка БД: {str(e)}", "error")

    def check_pair_answer(self):
        user_answer = self.pair_entry.get().strip().lower()
        if user_answer == self.correct_translation.lower():
            self.pair_check_button.configure(text="Правильно!", fg_color="green")
        else:
            self.pair_check_button.configure(
                text=f"Неверно! Правильно: {self.correct_translation}", 
                fg_color="red"
            )

    def next_pair_word(self):
        self.pair_entry.delete(0, "end")
        self.start_pair_mode()

    def on_add_words_button_click(self):
        self.hide_all_widgets()
        
        if not self.add_word_label:
            self.add_word_label = ctk.CTkLabel(
                self.main_frame,
                text="Добавить новое слово",
                font=("Roboto", 16, "bold")
            )
            self.english_entry = ctk.CTkEntry(
                self.main_frame,
                placeholder_text="Английское слово",
                width=300
            )
            self.translation_entry = ctk.CTkEntry(
                self.main_frame,
                placeholder_text="Перевод",
                width=300
            )
            self.add_button = ctk.CTkButton(
                self.main_frame,
                text="Добавить",
                command=self.add_word_to_db,
                width=150
            )

        self.add_word_label.pack(pady=(10, 5))
        self.english_entry.pack(pady=5)
        self.translation_entry.pack(pady=5)
        self.add_button.pack(pady=10)

    def add_word_to_db(self):
        en_word = self.english_entry.get().strip()
        ru_word = self.translation_entry.get().strip()
        
        if not (en_word and ru_word):
            self.show_message("Заполните оба поля", "error")
            return
        
        try:
            self.cursor.execute("SELECT 1 FROM words WHERE w_text = %s", (en_word,))
            if self.cursor.fetchone():
                self.show_message("Слово уже существует", "warning")
                return
            
            self.cursor.execute(
                "INSERT INTO words (w_text, translate) VALUES (%s, %s)",
                (en_word, ru_word)
            )
            self.conn.commit()
            self.show_message("Слово успешно добавлено!", "success")
            self.english_entry.delete(0, "end")
            self.translation_entry.delete(0, "end")
        
        except Exception as e:
            self.conn.rollback()
            self.show_message(f"Ошибка БД: {str(e)}", "error")

    def __del__(self):
        if hasattr(self, 'conn'):
            self.cursor.close()
            self.conn.close()

if __name__ == "__main__":
    app = DuoApp()
    app.mainloop()
