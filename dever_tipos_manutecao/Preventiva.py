import sqlite3
import os
import time

os.system("cls")
conn = sqlite3.connect("exemplo_preventiva.db")
cursor = conn.cursor()
cursor.execute("""
                       CREATE TABLE IF NOT EXISTS numeros(
                       resultados INTEGER)
                       """)
#medias
def carregar():
    for i in range(101):
        time.sleep(0.0100)
        print(f"{i}%", end="\r")
    print("concluido!✅")
    time.sleep(2)

def codigo_certo():
    repetir = True
    while repetir == True:
        total = 0
        os.system("cls")
        while True:
            try:
                quantidade_de_numeros = int(input("Deseja fazer a media de quantos números: "))
                break
            except ValueError:
                print("ERRO: usuario digitou algo que não deveria")
        os.system("cls")
        for i in range(quantidade_de_numeros):
            while True:
                try:
                    numeros = int(input(f"escreva o {i+1}o número da média: "))
                    total = total + numeros
                    break
                except ValueError:
                    print("ERRO: usuario digitou algo que não deveria")
        os.system("cls")
        media = total / quantidade_de_numeros
        carregar()
        print(f"A media dos números digitados é: {media}")
        print("")
        while True:
            resposta = str(input("deseja que esse resultado vá para o banco de dados(S/N): "))
            if resposta in ["S", "N"]:
                break
            print("digite apenas 'S' para 'SIM' e 'N' para 'NÃO' ")
        if (resposta == "N"):
            print("O resultado não será enviado para o banco de dados")
            print("")
        else:
            cursor.execute("INSERT INTO numeros (resultados) VALUES(?)", (media,))
            conn.commit()
            print("Resultado salvo no banco de dados!")
            print("")
        while True:
            deseja_repetir = str(input("deseja repetir: (S/N): "))
            if deseja_repetir in ["S", "N"]:
                break
            print("digite apenas 'S' para 'SIM' e 'N' para 'NÃO' ")
        if deseja_repetir == "S":
            repetir = True
        else:
            repetir = False
        
codigo_certo()