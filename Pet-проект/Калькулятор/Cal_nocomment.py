import customtkinter as ctk

class CalculatorApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        self.title("Калькулятор")
        self.geometry("340x330")
        self.resizable(False, False)
        self.iconbitmap("icon.ico") 
        ctk.set_appearance_mode("Dark")

        self.entry = ctk.CTkEntry(
            self,
            width=320,
            height=50,
            font=("Arial", 24),
            justify="right"
        )
        
        self.entry.grid(
            row=0,
            column=0,
            columnspan=4,
            padx=10,
            pady=10
        )

        buttons = [
            '(', ')', '%', '↩',
            '7', '8', '9', '/',
            '4', '5', '6', '*',
            '1', '2', '3', '-',
            '.', '0', '=', '+'
        ]
        
        reset_button = ctk.CTkButton(
            self,
            text="Сброс",
            width=330,
            height=40,
            font=("Arial", 20, "bold"),
            fg_color="#333333",
            hover_color="#666666",
            command=lambda: self.button_click('C')
        )

        reset_button.grid(
            row=6,
            column=0,
            columnspan=4,
            padx=5,
            pady=5
        )

        row_val = 1
        col_val = 0

        for button in buttons:
            action = lambda x=button: self.button_click(x)
            
            btn = ctk.CTkButton(
                self,
                text=button,
                width=75,
                height=40,
                font=("Arial", 20, "bold"),
                command=action
            )
            
            btn.grid(
                row=row_val,
                column=col_val,
                padx=1,
                pady=1,
                sticky="nsew"
            )
            
            col_val += 1
            
            if col_val > 3:
                col_val = 0
                row_val += 1
                
    def button_click(self, char):
        current_text = self.entry.get()
        
        if char in ['+', '-', '*', '/', '%']:
            if current_text and current_text[-1] in ['+', '-', '*', '/', '%']:
                self.entry.delete(len(current_text)-1, ctk.END)
            self.entry.insert(ctk.END, char)
        elif char == '%':
            try:
                # Проверяем, есть ли перед процентом число
                if current_text:
                    # Если есть знак перед числом, обрабатываем как процент от числа
                    if current_text[-1] in ['+', '-', '*', '/']:
                        # Находим последнее число перед оператором
                        for i in range(len(current_text)-2, -1, -1):
                            if current_text[i] in ['+', '-', '*', '/']:
                                break
                        number = float(current_text[i+1:])
                        operator = current_text[i]
                        
                        # Вычисляем процент от числа
                        result = number * 0.01
                        
                        # Обновляем выражение
                        self.entry.delete(0, ctk.END)
                        self.entry.insert(0, current_text[:i+1] + str(result))
                    else:
                        # Просто вычисляем процент от числа
                        number = float(current_text)
                        result = number * 0.01
                        self.entry.delete(0, ctk.END)
                        self.entry.insert(0, str(result))
                else:
                    self.entry.insert(ctk.END, char)
            except:
                self.entry.delete(0, ctk.END)
                self.entry.insert(0, "Ошибка")
        
        elif char == '=':
            try:
                # Заменяем % на *0.01 для корректного вычисления
                expression = current_text.replace('%', '*0.01')
                result = eval(expression)
                self.entry.delete(0, ctk.END)
                self.entry.insert(0, str(result))
            except:
                self.entry.delete(0, ctk.END)
                self.entry.insert(0, "Ошибка")
                
        elif char == 'C':
            self.entry.delete(0, ctk.END)
        
        elif char == '↩':
            if len(current_text) > 0:
                self.entry.delete(len(current_text)-1, ctk.END)
        
        else:
            if current_text == '0' and char != '.':
                self.entry.delete(0, ctk.END)
            self.entry.insert(ctk.END, char)

if __name__ == "__main__":
    app = CalculatorApp()
    app.mainloop()
