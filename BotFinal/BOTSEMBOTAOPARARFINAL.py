import tkinter as tk
from tkinter import filedialog
import pyautogui
import os
import keyboard
import winsound
import threading

# Lista de imagens a serem procuradas
images = []
# Lista de imagens especiais
special_images = []

# Variável para controle da busca
executando_busca = False

# Rótulo para exibir o status da busca
def update_status_label(text):
    status_label.config(text=text)

# Função para iniciar a busca por imagens
def iniciar_busca():
    global executando_busca
    executando_busca = True
    botao_iniciar.config(state="disabled")
    botao_parar.config(state="normal")
    botao_adicionar.config(state="disabled")
    botao_adicionar_especial.config(state="disabled")
    update_status_label("Busca em andamento...")
    buscar_imagens()

# Função para parar a busca
def parar_busca():
    global executando_busca
    executando_busca = False
    botao_iniciar.config(state="normal")
    botao_parar.config(state="disabled")
    botao_adicionar.config(state="normal")
    botao_adicionar_especial.config(state="normal")
    update_status_label("Busca finalizada.")

# Função que contém o loop de busca por imagens
def buscar_imagens():
    global executando_busca
    while executando_busca:
        for image in images:
            if move_to_image(image):
                print("Imagem encontrada:", image)
                break
        if special_images and move_to_image(special_images[0]):
            print("Imagem especial encontrada.")
            pressionar_tecla_end()
            reproduzir_alerta()
            parar_busca()
            break
    if executando_busca:
        update_status_label("Busca finalizada. Nenhuma imagem encontrada.")

# Função para mover o cursor para a posição da imagem encontrada
def move_to_image(image_path):
    try:
        pos = pyautogui.locateCenterOnScreen(image_path, confidence=0.7)
        if pos:
            pyautogui.moveTo(pos[0], pos[1] + 80)
            print("Posição encontrada: ", pos[0], pos[1] + 80)
            return True
    except pyautogui.ImageNotFoundException:
        pass  # Se a imagem não for encontrada, não faz nada
    return False

# Função para reproduzir alerta sonoro
def reproduzir_alerta():
    try:
        winsound.PlaySound("alerta.wav", winsound.SND_FILENAME)
    except Exception as e:
        print("Erro ao reproduzir o alerta sonoro:", e)
        
# Função para pressionar a tecla End
def pressionar_tecla_end():
    keyboard.press_and_release('End')

# Função para pressionar a tecla End e iniciar a busca
def iniciar_busca_pressionando_end():
    iniciar_busca()
    
# Função para adicionar imagens à lista
def adicionar_imagem():
    file_path = filedialog.askopenfilename(initialdir=os.getcwd(), title="Selecionar imagem", filetypes=(("PNG files", "*.png"), ("All files", "*.*")))
    if file_path:
        images.append(file_path)
        nome_arquivo_label.config(text=os.path.basename(file_path))  # Atualiza o nome do arquivo na caixa de texto
        print("Imagem adicionada:", file_path)

# Função para adicionar imagem especial à lista
def adicionar_imagem_especial():
    file_paths = filedialog.askopenfilenames(initialdir=os.getcwd(), title="Selecionar imagem especial", filetypes=(("PNG files", "*.png"), ("All files", "*.*")))
    for file_path in file_paths:
        special_images.append(file_path)
        print("Imagem especial adicionada:", file_path)
    atualizar_nome_arquivos_especiais()
    
# Função para atualizar o rótulo com o nome dos arquivos das imagens especiais selecionadas
def atualizar_nome_arquivos_especiais():
    nomes_arquivos_especiais = ", ".join(os.path.basename(image) for image in special_images)
    nome_arquivo_especial_label.config(text=nomes_arquivos_especiais)

# Criar a janela principal
janela = tk.Tk()
janela.title("Busca por imagens")

# Rótulo para exibir o status da busca
status_label = tk.Label(janela, text="Aguardando início da busca...")
status_label.pack()

# Configurar o evento do teclado para iniciar a busca com a tecla "End"
keyboard.add_hotkey('End', iniciar_busca_pressionando_end)
    
# Botão para iniciar a busca por imagens
botao_iniciar = tk.Button(janela, text="Iniciar busca por imagens", command=iniciar_busca)
botao_iniciar.pack()

# Botão para parar a busca
botao_parar = tk.Button(janela, text="Parar busca", command=parar_busca, state="disabled")
botao_parar.pack()

# Caixa de texto para o nome do arquivo da imagem selecionada
nome_arquivo_label = tk.Label(janela, text="", wraplength=250)
nome_arquivo_label.pack(side="right", padx=5)

# Botão para adicionar imagem à lista
botao_adicionar = tk.Button(janela, text="Adicionar imagem", command=adicionar_imagem)
botao_adicionar.pack(side="right", padx=5)

# Caixa de texto para o nome do arquivo da imagem especial selecionada
nome_arquivo_especial_label = tk.Label(janela, text="", wraplength=250)
nome_arquivo_especial_label.pack(side="right", padx=5)

# Botão para adicionar imagem especial à lista
botao_adicionar_especial = tk.Button(janela, text="Adicionar imagem especial", command=adicionar_imagem_especial)
botao_adicionar_especial.pack(side="right", padx=5)

# Caixa de texto para o nome do arquivo da imagem especial selecionada
nome_arquivo_especial_label = tk.Label(janela, text="", wraplength=250)
nome_arquivo_especial_label.pack(side="right", padx=5)

# Rodar o loop principal da interface gráfica
janela.mainloop()
