import math
import tkinter as tk
from tkinter import colorchooser


def rgb_para_hsi(r, g, b):
    # Normaliza para a escala 0 a 1
    r = r / 255  
    g = g / 255 
    b = b / 255
    
    '''Ajusta os valores para proporções relativas dentro do total RGB,
    que é a base do modelo HSI para calcular matiz e saturação.'''
    soma_rgb = r + g + b
    
    i = (soma_rgb) / 3

    rn = r / soma_rgb  # Proporção de vermelho
    gn = g / soma_rgb  # Proporção de verde
    bn = b / soma_rgb  # Proporção de azul
    
    # Calcula o numerador e o denominador da fórmula para H
    numerador_h = 0.5 * ((rn - gn) + (rn - bn))
    denominador_h = math.sqrt((rn - gn) ** 2 + (rn - bn) * (gn - bn))
    
    # Garanti que o denominador não seja zero para evitar divisões inválidas
    if denominador_h == 0:
        h = 0
    else:
        h = math.acos(numerador_h / denominador_h)
    
    # Ajusta H se o componente azul for maior que o verde
    if b > g:
        h = 2 * math.pi - h

    # Converte H de radianos para graus
    h = math.degrees(h)

    # Calcula a saturação (S)
    s = 1 - 3 * min(rn, gn, bn)
    
    # Retorna os valores arredondados de H, S e I
    return round(h, 5), round(s, 5), round(i, 5)


def hsi_para_rgb(h, s, i):
    desaturacao = i * (1 - s)
    h_rad = math.radians(h)  # Converter para radianos para cálculos trigonométricos
    
    if h < 120:  # h está no primeiro terço do círculo de cores
        parte_brilhante = i * (1 + (s * math.cos(h_rad)) / math.cos(math.radians(60) - h_rad))
        parte_restante = 3 * i - (desaturacao + parte_brilhante)
        b, r, g = desaturacao, parte_brilhante, parte_restante
    elif h < 240:  # h está no segundo terço
        h_rad -= math.radians(120)
        parte_brilhante = i * (1 + (s * math.cos(h_rad)) / math.cos(math.radians(60) - h_rad))
        parte_restante = 3 * i - (desaturacao + parte_brilhante)
        r, g, b = desaturacao, parte_brilhante, parte_restante
    else:  # h está no último terço
        h_rad -= math.radians(240)
        parte_brilhante = i * (1 + (s * math.cos(h_rad)) / math.cos(math.radians(60) - h_rad))
        parte_restante = 3 * i - (desaturacao + parte_brilhante)
        r, g, b = parte_restante, desaturacao, parte_brilhante

    # Ajustar valores para a escala de 0 a 255
    r = max(0, min(int(r * 255), 255))
    g = max(0, min(int(g * 255), 255))
    b = max(0, min(int(b * 255), 255))

    return r, g, b


def escolhe_cor():
    cor = colorchooser.askcolor()[0]  # Escolher cor RGB
    if cor:
        r, g, b = map(int, cor)
        H, S, I = rgb_para_hsi(r, g, b)
        altera_interface(r, g, b, H, S, I)

def altera_interface(r, g, b, H, S, I):
    # Atualizar o retângulo RGB
    canvas_rgb.config(bg=f"#{r:02x}{g:02x}{b:02x}")
    rgb_label.config(text=f"RGB: ({r}, {g}, {b})")

    # Converter HSI para RGB para exibir no canvas HSI
    r_hsi, g_hsi, b_hsi = hsi_para_rgb(H, S, I)
    canvas_hsi.config(bg=f"#{r_hsi:02x}{g_hsi:02x}{b_hsi:02x}")
    hsi_label.config(text=f"HSI: (H: {H:.2f}°, S: {S:.2f}, I: {I:.2f})")

# Configurar janela principal
root = tk.Tk()
root.title("Conversor RGB para HSI")
root.geometry("500x350")
root.config(bg="white")

# Frame para os widgets
frame = tk.Frame(root, bg="white")
frame.pack(pady=30)

# Botão para selecionar cor com bordas arredondadas e cor azul
btn_selecionar = tk.Button(frame, text="Selecionar Cor", command=escolhe_cor, font=("Segoe UI", 12), fg="white", bg="#007BFF", relief="flat", height=2, width=20, borderwidth=0, padx=10, pady=5)
btn_selecionar.grid(row=0, column=0, columnspan=2, pady=20)


canvas_rgb = tk.Canvas(frame, width=130, height=130, bd=1, relief="solid", highlightthickness=0, bg="#eeeeee")
canvas_rgb.grid(row=1, column=0, padx=20, pady=10)
canvas_rgb.config(bg="#eeeeee", relief="flat")  # Remover borda de destaque

rgb_label = tk.Label(frame, text="RGB: (0, 0, 0)", font=("Segoe UI", 12), bg="white")
rgb_label.grid(row=2, column=0, pady=10)


canvas_hsi = tk.Canvas(frame, width=130, height=130, bd=1, relief="solid", highlightthickness=0, bg="#eeeeee")
canvas_hsi.grid(row=1, column=1, padx=20, pady=10)
canvas_hsi.config(bg="#eeeeee", relief="flat")  # Remover borda de destaque

hsi_label = tk.Label(frame, text="HSI: (H: 0.00°, S: 0.00, I: 0.00)", font=("Segoe UI", 12), bg="white")
hsi_label.grid(row=2, column=1, pady=10)

root.mainloop()