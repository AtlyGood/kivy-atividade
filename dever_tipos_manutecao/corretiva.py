import sqlite3
import os
import time

os.system("cls")
conn = sqlite3.connect("exemplo_corretiva.db")
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


def codigo_errado():
    repetir = True
    while repetir == True:
        total = 0
        os.system("cls")
        quantidade_de_numeros = int(input("Deseja fazer a media de quantos números: "))
        os.system("cls")
        for i in range(quantidade_de_numeros):
            numeros = int(input(f"escreva o {i+1}o número da média: "))
            total = total + numeros
        os.system("cls")
        media = total / 2
        carregar()
        print(f"A media dos números digitados é: {media}")
        print("")
        resposta = str(input("deseja que esse resultado vá para o banco de dados(S/N): "))
        if (resposta == "N"):
            print("O resultado não será enviado para o banco de dados")
            print("")
        else:
            cursor.execute("INSERT INTO numeros (resultados) VALUES(?)", (media,))
            print("Resultado salvo no banco de dados!")
            print("")
        deseja_repetir = str(input("deseja repetir: (S/N): "))
        if deseja_repetir == "S":
            repetir = False
        else:
            repetir = False

def codigo_certo():
    repetir = True
    while repetir == True:
        total = 0
        os.system("cls")
        quantidade_de_numeros = int(input("Deseja fazer a media de quantos números: "))
        os.system("cls")
        for i in range(quantidade_de_numeros):
            numeros = int(input(f"escreva o {i+1}o número da média: "))
            total = total + numeros
        os.system("cls")
        media = total / quantidade_de_numeros
        carregar()
        print(f"A media dos números digitados é: {media}")
        print("")
        resposta = str(input("deseja que esse resultado vá para o banco de dados(S/N): "))
        if (resposta == "N"):
            print("O resultado não será enviado para o banco de dados")
            print("")
        else:
            cursor.execute("INSERT INTO numeros (resultados) VALUES(?)", (media,))
            conn.commit()
            print("Resultado salvo no banco de dados!")
            print("")
        deseja_repetir = str(input("deseja repetir: (S/N): "))
        if deseja_repetir == "S":
            repetir = True
        else:
            repetir = False
        
codigo_certo()