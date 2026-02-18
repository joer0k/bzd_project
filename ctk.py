import customtkinter as ctk

# Настройка внешнего вида (System, Dark, Light)
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("green")

class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Настройка окна
        self.title("Базовая программа.py")
        self.geometry("400x200")
        self.
        # Добавление виджетов
        self.label = ctk.CTkLabel(self, text="Привет, CustomTkinter!", font=("Arial", 20))
        self.label.pack(pady=20)

        self.button = ctk.CTkButton(self, text="Нажми меня", command=self.button_click)
        self.button.pack(pady=10)

    def button_click(self):
        print("Кнопка нажата!")

if __name__ == "__main__":
    app = App()
    app.mainloop()
