# Импортируем библиотеку CustomTkinter и даем ей короткое имя ctk
import customtkinter as ctk

# Создаем класс калькулятора, который наследуется от базового класса CTk
class CalculatorApp(ctk.CTk):
    def __init__(self):
        # Вызываем конструктор родительского класса (CTk)
        super().__init__()
        
        # Настройка внешнего вида окна калькулятора
        self.title("Калькулятор")  # Устанавливаем заголовок окна
        self.geometry("340x330")  # Задаем размеры окна (ширина x высота)
        self.resizable(False, False)  # Запрещаем изменение размеров окна
        self.iconbitmap("icon.ico")  # Устанавливаем иконку окна
        ctk.set_appearance_mode("Dark")  # Устанавливаем темную тему оформления

        # Создаем поле для ввода чисел и отображения результатов
        self.entry = ctk.CTkEntry(
            self,  # Родительское окно, где будет располагаться поле ввода
            width=320,  # Ширина поля ввода в пикселях
            height=50,  # Высота поля ввода в пикселях
            font=("Arial", 24),  # Шрифт и его размер
            justify="right"  # Выравнивание текста по правому краю
        )
        
        # Размещаем поле ввода в окне с помощью сетки (grid)
        self.entry.grid(
            row=0,  # Размещаем в первой строке сетки
            column=0,  # Размещаем в первом столбце
            columnspan=4,  # Объединяем 4 столбца
            padx=10,  # Отступы по бокам
            pady=10  # Отступы сверху и снизу
        )

        # Список всех кнопок калькулятора
        buttons = [
            '(', ')', '%', '↩',  # Первая строка кнопок
            '7', '8', '9', '/',  # Вторая строка
            '4', '5', '6', '*',  # Третья строка
            '1', '2', '3', '-',  # Четвертая строка
            '.', '0', '=', '+'  # Пятая строка
        ]

        # Создаем кнопку "Сброс" (Clear)
        reset_button = ctk.CTkButton(
            self,  # Родительское окно
            text="Сброс",  # Текст на кнопке
            width=330,  # Ширина кнопки
            height=40,  # Высота кнопки
            font=("Arial", 20, "bold"),  # Шрифт кнопки
            fg_color="#333333",  # Основной цвет кнопки
            hover_color="#666666",  # Цвет при наведении мыши
            command=lambda: self.button_click('C')  # Действие при нажатии
        )
        
        # Размещаем кнопку сброса
        reset_button.grid(
            row=6,  # Строка размещения
            column=0,  # Колонка размещения
            columnspan=4,  # Объединяем 4 колонки
            padx=5,  # Отступы по бокам
            pady=5  # Отступы сверху и снизу
        )

        # Переменные для размещения кнопок в сетке
        row_val = 1  # Текущая строка (начинаем со второй, так как первая занята полем ввода)
        col_val = 0  # Текущая колонка

        # Создаем и размещаем все кнопки калькулятора
        for button in buttons:
            # Создаем функцию-обработчик нажатия для каждой кнопки
            action = lambda x=button: self.button_click(x)
            
            # Создаем кнопку с заданными параметрами
            btn = ctk.CTkButton(
                self,  # Родительское окно
                text=button,  # Текст на кнопке
                width=75,  # Ширина кнопки
                height=40,  # Высота кнопки
                font=("Arial", 20, "bold"),  # Шрифт кнопки
                command=action  # Действие при нажатии
            )
            
            # Размещаем кнопку в сетке
            btn.grid(
                row=row_val,  # Текущая строка
                column=col_val,  # Текущая колонка
                padx=1,  # Отступы по бокам
                pady=1,  # Отступы сверху и снизу
                sticky="nsew"  # Растягиваем кнопку по всей ячейке
            )

            # Увеличиваем значение переменной col_val на 1
            # Эта переменная отвечает за расположение кнопок по горизонтали
            col_val += 1

            # Проверяем, не превысило ли значение col_val число 3
            # Если да, то:
            if col_val > 3:
                # Обнуляем счетчик колонок
                col_val = 0
                # Переходим на следующую строку
                row_val += 1

    # Функция для обработки нажатий кнопок
    def button_click(self, char):
        # Получаем текущий текст из поля ввода
        current_text = self.entry.get()
        
        # Проверяем, является ли нажатая кнопка математическим оператором
        if char in ['+', '-', '*', '/', '%']:
            # Если в поле есть текст и последний символ - тоже оператор:
            if current_text and current_text[-1] in ['+', '-', '*', '/', '%']:
                # Удаляем последний символ (предыдущий оператор)
                self.entry.delete(len(current_text)-1, ctk.END)
            # Добавляем новый оператор в конец выражения
            self.entry.insert(ctk.END, char)
            
        # Обработка нажатия кнопки процента (%)
        elif char == '%':
            try:
                # Проверяем, есть ли текст для обработки
                if current_text:
                    # Если перед процентом есть математический оператор
                    if current_text[-1] in ['+', '-', '*', '/']:
                        # Ищем последнее число перед оператором
                        for i in range(len(current_text)-2, -1, -1):
                            if current_text[i] in ['+', '-', '*', '/']:
                                break
                        # Преобразуем найденное число в число с плавающей точкой
                        number = float(current_text[i+1:])
                        # Сохраняем оператор
                        operator = current_text[i]
                        
                        # Вычисляем процент от числа
                        result = number * 0.01
                        
                        # Обновляем выражение в поле ввода
                        self.entry.delete(0, ctk.END)
                        self.entry.insert(0, current_text[:i+1] + str(result))
                    else:
                        # Если перед процентом нет оператора, просто вычисляем процент
                        number = float(current_text)
                        result = number * 0.01
                        self.entry.delete(0, ctk.END)
                        self.entry.insert(0, str(result))
                else:
                    # Если поле ввода пустое, просто добавляем символ %
                    self.entry.insert(ctk.END, char)
            except:
                # Если произошла ошибка при вычислении
                self.entry.delete(0, ctk.END)
                self.entry.insert(0, "Ошибка")
                
        # Обработка кнопки равно (=)
        elif char == '=':
            try:
                # Заменяем все % на *0.01 для корректного вычисления
                expression = current_text.replace('%', '*0.01')
                # Вычисляем результат
                result = eval(expression)
                # Очищаем поле ввода и выводим результат
                self.entry.delete(0, ctk.END)
                self.entry.insert(0, str(result))
            except:
                # Если произошла ошибка при вычислении
                self.entry.delete(0, ctk.END)
                self.entry.insert(0, "Ошибка")
                
        # Обработка кнопки сброса (C)
        elif char == 'C':
            # Очищаем поле ввода
            self.entry.delete(0, ctk.END)
            
        # Обработка кнопки удаления (←)
        elif char == '↩':
            # Если в поле ввода есть символы, удаляем последний
            if len(current_text) > 0:
                self.entry.delete(len(current_text)-1, ctk.END)
                
        # Обработка цифр и точки
        else:
            # Если в поле ввода стоит 0 и нажата не точка, очищаем поле
            if current_text == '0' and char != '.':
                self.entry.delete(0, ctk.END)
            # Добавляем символ в конец выражения
            self.entry.insert(ctk.END, char)

# Запуск приложения
if __name__ == "__main__":
    app = CalculatorApp()
    app.mainloop()
