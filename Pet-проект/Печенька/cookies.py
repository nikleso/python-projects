import customtkinter as ctk
import random
from PIL import Image
import psycopg2

class PredictionApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        # Настройки подключения к БД
        self.db_config = {
            'dbname': 'cookies',
            'user': 'postgres',
            'password': '123',
            'host': 'localhost',
            'port': '5432',
            'client_encoding': 'utf8'  # Добавляем параметр кодировки
        }

        
        # Подключение к БД
        try:
            self.connection = psycopg2.connect(**self.db_config)
            self.cursor = self.connection.cursor()
        except Exception as e:
            print(f"Ошибка подключения к БД: {e}")
            return
        
        # Настройка окна
        self.title("Печенька с предсказанием")
        self.geometry("480x380") 
        self.resizable(False, False)
        self.iconbitmap("icon.ico") 
        
        try:
            # Открываем изображение
            self.bg_image = Image.open("фон.jpg")
            
            # Создаем CTkImage
            self.ctk_image = ctk.CTkImage(light_image=self.bg_image, size=(480, 380))
            
            # Создаем метку без текста
            self.bg_label = ctk.CTkLabel(self, image=self.ctk_image, text="")  # Добавляем text=""
            self.bg_label.place(x=0, y=0, relwidth=1, relheight=1)
            
            # Создаем кнопку
            self.button = ctk.CTkButton(self, 
                                       text="Испытать удачу", 
                                       command=self.on_button_click,  # добавляем обработчик
                                       width=150,
                                       height=40,
                                       fg_color=("#6A0DAD", "#B388FF"),  # от темно-фиолетового к светло-синему
                                       hover_color=("#800080", "#FFC0CB"),  # от пурпурного к розовому
                                       corner_radius=10)  # скругленные углы
            
            # Размещаем кнопку по центру
            self.button.place(relx=0.5, rely=0.45, anchor=ctk.CENTER)
            
            # Метка для предсказания
            self.prediction_label = ctk.CTkLabel(self, 
                                                text="",
                                                width=250,
                                                height=40,
                                                fg_color=("#FFFFFF", "#FFFFFF")
            )            
        except FileNotFoundError:
            print("Ошибка: файл изображения не найден!")

    def on_button_click(self):
        try:
            # Получаем все предсказания из БД
            self.cursor.execute("SELECT pred_text FROM predictions")
            predictions = self.cursor.fetchall()
            
            if not predictions:
                raise Exception("В базе данных нет предсказаний")
            
            # Выбираем случайное предсказание
            random_prediction = random.choice(predictions)[0]
            
            # Скрываем кнопку
            self.button.place_forget()
            
                        # Показываем предсказание
            self.prediction_label.configure(text=random_prediction)
            self.prediction_label.configure(
                corner_radius=0,
                text_color="#9C55FF",
                font=ctk.CTkFont(
                    size=24,  # размер текста
                    weight="bold"
                )
            )
            self.prediction_label.place(relx=0.5, rely=0.45, anchor=ctk.CENTER)

            # Добавляем кнопку обновления
            self.refresh_button = ctk.CTkButton(
                self, 
                text="↺", 
                command=self.reset,
                width=20,
                height=20,
                fg_color=("#6A0DAD", "#B388FF"),
                hover_color=("#800080", "#FFC0CB"),
                corner_radius=0,
                border_width=0
            )
            self.refresh_button.place(relx=0.755, rely=0.454, anchor=ctk.CENTER)  # Размещаем справа от текста

        except Exception as e:
            print(f"Произошла ошибка: {str(e)}")
            self.show_error_message(str(e))

    def reset(self, event=None):  # добавили event для обработки клика
        # Скрываем текущие элементы
        self.prediction_label.place_forget()
        self.refresh_button.place_forget()
        
        # Показываем начальную кнопку
        self.button.place(relx=0.5, rely=0.45, anchor=ctk.CENTER)
        
        # Очищаем текст предсказания
        self.prediction_label.configure(text="")


    def __del__(self):
        try:
            # Закрываем соединение с БД при завершении работы
            if hasattr(self, 'cursor'):
                self.cursor.close()
            if hasattr(self, 'connection'):
                self.connection.close()
        except Exception as e:
            print(f"Ошибка при закрытии соединения с БД: {e}")

if __name__ == "__main__":
    try:
        app = PredictionApp()
        app.mainloop()
    except Exception as e:
        print(f"Критическая ошибка: {str(e)}")
