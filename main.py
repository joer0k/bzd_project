import customtkinter as ctk
from base import *
from tkinter import messagebox
# Настройка внешнего вида (System, Dark, Light)
ctk.set_appearance_mode("Light")
ctk.set_default_color_theme("green")

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        little_font = ("TT Travels text",20)
        big_font = ("TT Travels text",25)
        # Настройка окна
        self.title("Калькулятор мощности.py")
        self.geometry("400x600")
        self.label = ctk.CTkLabel(self, text="Калькулятор установочной\nмощности двигателя", font=big_font)
        self.label.pack(pady=20)
        self.entryH = ctk.CTkEntry(self, placeholder_text = "Введите H (м)",font = little_font,width=250)
        self.entryH.pack(pady=20)
        self.entryVt = ctk.CTkEntry(self, placeholder_text = "Введите Vт (м3/c)", font= little_font,width= 250)
        self.entryVt.pack(pady=20)
        self.entryTemperature = ctk.CTkEntry(self, placeholder_text = "Введите t (°С)", font = little_font,width=250)
        self.entryTemperature.pack(pady=20)


        # Добавление виджетов
        self.button = ctk.CTkButton(self, text="Рассчитать", command=self.button_click,font = big_font,width=200, height=200)
        self.button.pack(pady=100)

    def button_click(self):

        try:
            H = float(self.entryH.get())
            Vt = float(self.entryVt.get())
            temperature = float(self.entryTemperature.get())

            messagebox.showinfo("Готово",f"~{installed_capacity(nominal_power(useful_power(Vt,temperature)))[0]} Вт")
        except Exception as exp:
            messagebox.showerror("Ошибка", "Данные введены неверно")
            self.entryH.delete(0,ctk.END)
            self.entryH.delete(0, ctk.END)
            self.entryH.delete(0, ctk.END)
            print(exp)


if __name__ == "__main__":
    app = App()
    app.mainloop()
