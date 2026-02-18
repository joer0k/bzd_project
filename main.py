import customtkinter as ctk

# Настройка внешнего вида (System, Dark, Light)
ctk.set_appearance_mode("Light")
ctk.set_default_color_theme("green")

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        little_font = ("TT Travels text",20)
        big_fon = ("TT Travels text",25)
        # Настройка окна
        self.title("Калькулятор мощности.py")
        self.geometry("400x600")
        self.label = ctk.CTkLabel(self, text="Калькулятор установочной\nмощности двигателя", font=big_fon)
        self.label.pack(pady=20)
        self.entryH = ctk.CTkEntry(self, placeholder_text = "Введите H",font = little_font,width=200)
        self.entryH.pack(pady=20)
        self.entryVt = ctk.CTkEntry(self, placeholder_text = "Введите Vt", font= little_font,width= 200)
        self.entryVt.pack(pady=20)
        self.entryt = ctk.CTkEntry(self, placeholder_text = "Введите t", font = little_font,width=200)
        self.entryt.pack(pady=20)
        # Добавление виджетов


        self.button = ctk.CTkButton(self, text="Рассчитать", command=self.button_click,font =little_font)
        self.button.pack(pady=100)

    def button_click(self):
        print("Кнопка нажата!")

if __name__ == "__main__":
    app = App()
    app.mainloop()
