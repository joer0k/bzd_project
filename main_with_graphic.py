import customtkinter as ctk
from tkinter import messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np

ctk.set_appearance_mode("Light")
ctk.set_default_color_theme("green")

CONSTS = {"g": 9.81, "b": 1.5, "n": 0.4}
# Константы
# g = 9.81
# p = 1029.3
# b = 1.5
# n = 0.4
# Ввод
H = 20
Vt = 0.00135
t = 20


# Функция для расчета плотности молока в зависимости от температуры
def milk_density(temperature):


    rho_0 = 1030  # плотность при 20°C (кг/м³)
    alpha = 0.4  # температурный коэффициент (кг/(м³·°C))
    t0 = 20  # эталонная температура (°C)

    density = rho_0 - alpha * (temperature - t0)
    return max(990, min(1040, density))  # Ограничиваем диапазон плотности

def useful_power(Vt, temperature, H):
    return round(milk_density(temperature) * CONSTS["g"] * H * Vt / 1000, 2)


def nominal_power(u_p):
    return u_p / CONSTS["n"]


def installed_capacity(nom_power):
    return round(CONSTS["b"] * nom_power), round(CONSTS["b"] * nom_power, 2)
class GraphWindow(ctk.CTkToplevel):
    def __init__(self, parent):
        super().__init__(parent)

        # Используем стандартные шрифты Windows
        self.little_font = ("Segoe UI", 20, "bold")
        self.big_font = ("Segoe UI", 25, "bold")
        self.medium_font = ("Segoe UI", 18, "bold")

        self.title("График зависимости мощности")
        self.geometry("850x900")
        self.resizable(False, False)

        # Начальные значения переменных
        self.H = 10.0  # м
        self.Vt = 1.0  # м3/с
        self.temperature = 20.0  # °С

        # Создаем фрейм для ползунков
        sliders_frame = ctk.CTkFrame(self)
        sliders_frame.pack(pady=20, padx=20, fill="x")

        # Заголовок для ползунков
        sliders_title = ctk.CTkLabel(sliders_frame, text="Параметры регулировки",
                                     font=self.big_font)
        sliders_title.pack(pady=(0, 15))

        # Ползунок для H
        self.h_slider = ctk.CTkSlider(sliders_frame, from_=0, to=50, number_of_steps=100,
                                      command=self.update_graph)
        self.h_slider.pack(pady=10, fill="x")
        self.h_slider.set(self.H)

        self.h_label = ctk.CTkLabel(sliders_frame, text=f"H = {self.H:.1f} м",
                                    font=self.medium_font)
        self.h_label.pack()

        # Ползунок для Vt
        self.vt_slider = ctk.CTkSlider(sliders_frame, from_=0, to=10, number_of_steps=100,
                                       command=self.update_graph)
        self.vt_slider.pack(pady=10, fill="x")
        self.vt_slider.set(self.Vt)

        self.vt_label = ctk.CTkLabel(sliders_frame, text=f"Vт = {self.Vt:.2f} м³/с",
                                     font=self.medium_font)
        self.vt_label.pack()

        # Ползунок для температуры
        self.temp_slider = ctk.CTkSlider(sliders_frame, from_=-50, to=100, number_of_steps=150,
                                         command=self.update_graph)
        self.temp_slider.pack(pady=10, fill="x")
        self.temp_slider.set(self.temperature)

        self.temp_label = ctk.CTkLabel(sliders_frame, text=f"t = {self.temperature:.1f} °С",
                                       font=self.medium_font)
        self.temp_label.pack()

        # Кнопка для применения текущих значений к основному окну
        self.apply_button = ctk.CTkButton(sliders_frame, text="Применить к основному окну",
                                          command=self.apply_to_main, font=self.medium_font,
                                          height=40)
        self.apply_button.pack(pady=15)

        # Фрейм для графика
        plot_frame = ctk.CTkFrame(self)
        plot_frame.pack(expand=True, fill="both", padx=20, pady=20)

        # Создаем фигуру для графика с стандартными шрифтами Windows
        plt.rcParams['font.family'] = 'Segoe UI'
        plt.rcParams['font.size'] = 12
        plt.rcParams['axes.labelsize'] = 14
        plt.rcParams['axes.titlesize'] = 16
        plt.rcParams['legend.fontsize'] = 12
        plt.rcParams['font.weight'] = 'bold'

        self.fig, self.ax = plt.subplots(figsize=(9, 6))

        # Встраиваем график в окно
        self.canvas = FigureCanvasTkAgg(self.fig, master=plot_frame)
        self.canvas.get_tk_widget().pack(expand=True, fill="both")

        # Первоначальное построение графика
        self.plot_graph()

    def update_graph(self, value=None):
        # Обновляем значения с ползунков
        self.H = self.h_slider.get()
        self.Vt = self.vt_slider.get()
        self.temperature = self.temp_slider.get()

        # Обновляем метки с новым шрифтом
        self.h_label.configure(text=f"H = {self.H:.1f} м")
        self.vt_label.configure(text=f"Vт = {self.Vt:.2f} м³/с")
        self.temp_label.configure(text=f"t = {self.temperature:.1f} °С")

        # Перестраиваем график
        self.plot_graph()

    def plot_graph(self):
        # Очищаем текущий график
        self.ax.clear()

        # Создаем данные для графика
        Vt_range = np.linspace(0.1, 10, 100)
        powers = []

        for vt in Vt_range:
            try:
                # ИСПРАВЛЕНИЕ: Передаем H в функцию useful_power
                P_useful = useful_power(vt, self.temperature, self.H)  # Добавлен параметр H
                P_nominal = nominal_power(P_useful)
                P_installed = installed_capacity(P_nominal)[0]
                powers.append(P_installed)
            except Exception as e:
                print(f"Ошибка расчета: {e}")
                powers.append(0)

        # Строим график с улучшенным оформлением
        self.ax.plot(Vt_range, powers, 'b-', linewidth=2.5, label='Зависимость мощности')
        self.ax.set_xlabel('Расход Vт (м³/с)', fontname='Segoe UI', fontsize=14, fontweight='bold')
        self.ax.set_ylabel('Установочная мощность (Вт)', fontname='Segoe UI', fontsize=14, fontweight='bold')
        self.ax.set_title(f'Зависимость мощности от расхода\nH={self.H:.1f} м, t={self.temperature:.1f}°С',
                          fontname='Segoe UI', fontsize=16, fontweight='bold')
        self.ax.grid(True, alpha=0.3, linestyle='--')

        # Отмечаем текущую точку
        try:
            # ИСПРАВЛЕНИЕ: Передаем H в функцию useful_power для текущей точки
            current_power = installed_capacity(
                nominal_power(
                    useful_power(self.Vt, self.temperature, self.H)  # Добавлен параметр H
                )
            )[0]
            self.ax.plot(self.Vt, current_power, 'ro', markersize=10, label='Текущее значение',
                         markeredgecolor='darkred', markeredgewidth=2)
            self.ax.legend(loc='upper left', framealpha=0.9, prop={'family': 'Segoe UI', 'size': 12, 'weight': 'bold'})
        except Exception as e:
            print(f"Ошибка отображения текущей точки: {e}")

        # Добавляем подписи к осям с улучшенным форматированием
        self.ax.tick_params(axis='both', which='major', labelsize=12)

        # Обновляем canvas
        self.canvas.draw()

    def apply_to_main(self):
        # Применяем текущие значения к основному окну
        self.master.entryH.delete(0, ctk.END)
        self.master.entryH.insert(0, f"{self.H:.1f}")

        self.master.entryVt.delete(0, ctk.END)
        self.master.entryVt.insert(0, f"{self.Vt:.2f}")

        self.master.entryTemperature.delete(0, ctk.END)
        self.master.entryTemperature.insert(0, f"{self.temperature:.1f}")

        messagebox.showinfo("Успешно", "Значения применены к основному окну")

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        # Используем стандартные шрифты Windows для основного окна
        little_font = ("Segoe UI", 20, "bold")
        big_font = ("Segoe UI", 25, "bold")

        # Настройка окна
        self.title("Калькулятор мощности.py")
        self.geometry("400x600")
        self.resizable(False, False)
        self.label = ctk.CTkLabel(self, text="Калькулятор установочной\nмощности двигателя", font=big_font)
        self.label.pack(pady=20)

        self.entryH = ctk.CTkEntry(self, placeholder_text="Введите H (м)", font=little_font, width=250)
        self.entryH.pack(pady=10)

        self.entryVt = ctk.CTkEntry(self, placeholder_text="Введите Vт (м3/c)", font=little_font, width=250)
        self.entryVt.pack(pady=10)

        self.entryTemperature = ctk.CTkEntry(self, placeholder_text="Введите t (°С)", font=little_font, width=250)
        self.entryTemperature.pack(pady=10)

        # Кнопка расчета
        self.button = ctk.CTkButton(self, text="Рассчитать", command=self.button_click,
                                    font=big_font, width=200, height=150)
        self.button.pack(pady=20)

        # Кнопка для открытия графика
        self.graph_button = ctk.CTkButton(self, text="Открыть график", command=self.open_graph_window,
                                          font=little_font, width=200, height=50)
        self.graph_button.pack(pady=10)

    def button_click(self):
        try:
            H = float(self.entryH.get())
            Vt = float(self.entryVt.get())
            temperature = float(self.entryTemperature.get())

            result = installed_capacity(nominal_power(useful_power(Vt, temperature,H)))[0]
            messagebox.showinfo("Готово", f"~{result:.1f} кВт")

        except Exception as exp:
            messagebox.showerror("Ошибка", "Данные введены неверно")
            self.entryH.delete(0, ctk.END)
            self.entryVt.delete(0, ctk.END)
            self.entryTemperature.delete(0, ctk.END)
            print(exp)

    def open_graph_window(self):
        # Открываем окно с графиком
        graph_window = GraphWindow(self)
        graph_window.grab_set()  # Делает окно модальным


if __name__ == "__main__":
    app = App()
    app.mainloop()