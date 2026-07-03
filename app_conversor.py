import customtkinter as ctk
import requests

### ICONE ###
import os
import sys
import tkinter as tk

#Retorna o caminho absoluto para o recurso, seja no modo desenvolvimento ou no PyInstaller
def caminho_recurso(relative_path):
    try:
        # O PyInstaller cria uma pasta temporária e guarda o caminho em _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

####

#Configuração visual do aplicativo
ctk.set_appearance_mode("System") #Segue o tema do seu computador (Claro/Escuro)
ctk.set_default_color_theme("blue") #Cor padrão dos botões

#Função que busca os dados na internet
def obter_cotacao(moeda):
    url = f"https://economia.awesomeapi.com.br/last/{moeda}-BRL"

    try:
        resposta = requests.get(url)
        resposta.raise_for_status()
        dados = response_json = resposta.json()
        chave_moeda = f"{moeda}BRL"
        cotacao = float(dados[chave_moeda]['bid'])
        return float(dados[chave_moeda]['bid'])
    
    except Exception as e:
        #Mostra o erro real no terminal abaixo da janela
        print(f"Erro na API: {e}")
        return None
    
#Função que roda quando o usuário clicka no botão
def acao_botao_converter(event=None):
    moeda_selecionada = menu_moeda.get()
    direcao_selecionada = menu_direcao.get() # Pega a direção escolhida

    #Mapeia o nome do menu para código API
    codigos = {"Dólar (USD)": "USD", "Euro (EUR)": "EUR", "Bitcoin (BTC)": "BTC"}
    codigo_moeda = codigos[moeda_selecionada]

    #Busca a cotação atual
    cotacao = obter_cotacao(codigo_moeda)

    if cotacao:
        try:
            valor_inserido = float(campo_valor.get())
            
            #Opção de Moeda Estrangeira para Real
            if direcao_selecionada == "Moeda Estrangeira ➔ Real (BRL)":
                total = valor_inserido * cotacao
                simbolo = "R$"
                texto_final = f"Cotação: R$ {cotacao:.2f}\nTotal: {simbolo} {total:.2f}"

            #Opção de Real para Moeda Estrangeira
            else:
                total = valor_inserido / cotacao
                simbolos = {"USD": "$", "EUR": "€", "BTC": "₿"} #Define o símbolo correto para mostrar na tela
                simbolo = simbolos[codigo_moeda]

                # [CORRIGIDO] Se for Bitcoin, mostra até 6 casas decimais. Se não, mostra 2.
                if codigo_moeda == "BTC":
                    texto_final = f"Cotação: R$ {cotacao:.2f}\nTotal: {simbolo} {total:.6f}"
                else:
                    texto_final = f"Cotação: R$ {cotacao:.2f}\nTotal: {simbolo} {total:.2f}"

            texto_resultado.configure(text=texto_final, text_color="green")
            
        except ValueError:
            texto_resultado.configure(text="Erro: Digite um número válido!", text_color="red")
    else:
        texto_resultado.configure(text="Erro ao buscar cotação. Verifique a internet.", text_color="red")

#[NOVO] Função para limpar
def acao_botao_limpar():
    campo_valor.delete(0, 'end') #Apaga o texto digitado do início ao fim
    texto_resultado.configure(text="")  #Remove a mensagem de resultado da tela

## ---- CONSTRUINDO A INTERFACE ---- ##

#Cria a janela principal
janela = ctk.CTk()
janela.title("Conversor de Moedas")
janela.geometry("400x500") #Largura e altura da janela

#[NOVO] Adiciona o ícone na barra de título da janela
import tkinter as tk
try:
    icone_imagem = tk.PhotoImage(file=caminho_recurso("icone_conversor.ico"))
    janela.iconphoto(False, icone_imagem)
except Exception as e:
    print(f"Aviso: Não foi possível carregar o ícone na barra, mas o app vai abrir: {e}")

#Título do App
titulo = ctk.CTkLabel(janela, text="Conversor de Moedas", font=("Arial", 20, "bold"))
titulo.pack(pady=40) #'pady' é o espaçamento em cima e embaixo

#[NOVO] Menu para escolher o sentido da conversão
rotulo_direcao = ctk.CTkLabel(janela, text="Escolha o sentido da conversão:", font=("Arial", 12))
rotulo_direcao.pack(pady=2)
menu_direcao = ctk.CTkOptionMenu(janela, values=["Moeda Estrangeira ➔ Real (BRL)", "Real (BRL) ➔ Moeda Estrangeira"])
menu_direcao.pack(pady=5)

#Menu para escolher a moeda estrangeira
rotulo_moeda = ctk.CTkLabel(janela, text="Escolha a moeda estrangeira:", font=("Arial", 12))
rotulo_moeda.pack(pady=2)
menu_moeda = ctk.CTkOptionMenu(janela, values=["Dólar (USD)", "Euro (EUR)", "Bitcoin (BTC)"])
menu_moeda.pack(pady=10)

#Campo para digitar o valor (Input)
campo_valor = ctk.CTkEntry(janela, placeholder_text="Quantidade a converter")
campo_valor.pack(pady=15)
campo_valor.bind("<Return>", acao_botao_converter) #Vincula a tecla 'Enter' do teclado

#Botão de converter
botao = ctk.CTkButton(janela, text="Converter", command=acao_botao_converter)
botao.pack(pady=10)

#Texto onde vai aparecer o resultado
texto_resultado = ctk.CTkLabel(janela, text="", font=("Arial", 16, "bold"))
texto_resultado.pack(pady=10)

#[NOVO] Criação e posicionamento do botação limpar
botao_limpar = ctk.CTkButton(
    janela, 
    text = "Limpar", 
    command = acao_botao_limpar, #Conecta com a nova função ali de cima
    fg_color = "transparent", #Cor transparente
    hover_color="#E0E0E0", #Cor ao passar o mouse
    text_color = "#555555", #Cor do texto
    font=("Arial", 14, "underline") #Aplica o sublinhado na fonte
)
botao_limpar.pack(pady=25) #Desenha o botão na tela

#Mantém a janela aberta e rodando
janela.mainloop()



#......................................................................
#.................................................~§§§§§'..............
#...........=##################################§§§§§§§.................
#..........=#################################§§§§§§§...................
#........=###################%%%%%%%%%%%%%%%%%%%%§.....................
#......=####.......&&#####''.........&######"'.........................
#..................&&#####'..........&######'..........................
#..................&#####'...........&######'..........................
#..................&#####'...........&#####'...........................
#..................&#####'..........&######'...........................
#.................&&####'...........&######'...........................
#.................&&####'...........&######'...........................
#................&&&####'..........&&######'...........................
#..............&&&&#####'..........&&#######'..........................
#...........&&&&#########'.........&&#########'........................
#..........&&&&&#########'.........&&&#########§´......................
#..........&&&&&&########'.........&&&##########§'.....................
#...........&&&&&&#######'.........&&&########&'.......................
#............`&&&&&&&&&´............'&&&&&&&&&"........................
#......................................................................          