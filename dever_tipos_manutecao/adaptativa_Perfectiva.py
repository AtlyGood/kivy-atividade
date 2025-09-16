import sqlite3
import os
import time

os.system("cls")
conn = sqlite3.connect("exemplo_adaptativa_perfectiva.db")
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

def exportar_resultados():
    """Exporta todos os resultados para um arquivo TXT"""
    try:
        cursor.execute("SELECT * FROM numeros")
        resultados = cursor.fetchall()
        
        if not resultados:
            print("Não há resultados para exportar!")
            return False
        
        with open("resultados_media.txt", "w", encoding="utf-8") as arquivo:
            arquivo.write("RESULTADOS DE MÉDIAS CALCULADAS\n")
            arquivo.write("=" * 40 + "\n")
            arquivo.write(f"Data da exportação: {time.strftime('%d/%m/%Y %H:%M:%S')}\n")
            arquivo.write("=" * 40 + "\n\n")
            
            for i, resultado in enumerate(resultados, 1):
                arquivo.write(f"Resultado {i}: {resultado[0]:.2f}\n")
            
            arquivo.write("\n" + "=" * 40 + "\n")
            arquivo.write(f"Total de resultados exportados: {len(resultados)}\n")
            arquivo.write("=" * 40 + "\n")
        
        print("Resultados exportados com sucesso para 'resultados_media.txt'!")
        return True
        
    except Exception as e:
        print(f"Erro ao exportar resultados: {e}")
        return False

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
        resposta = str(input("deseja que esse resultado vá para o banco de dados(S/N): ")).upper()
        if (resposta == "N"):
            print("O resultado não será enviado para o banco de dados")
            print("")
        else:
            cursor.execute("INSERT INTO numeros (resultados) VALUES(?)", (media,))
            conn.commit()
            print("Resultado salvo no banco de dados!")
            print("")
        deseja_repetir = str(input("deseja repetir: (S/N): ")).upper()
        if deseja_repetir == "S":
            repetir = True
        else:
            repetir = False
        
codigo_certo()
lista = str(input("Deseja uma lista com os resultados (S/N):")).upper()
if lista == "S":
    exportar_resultados()
else:
    print("execusão finalizada")