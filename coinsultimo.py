import requests
import time
from binance.client import Client
import pandas as pd
from os import system, name
  
#Conectar a la API  
api_key = ''
  
client = Client('', '')

#Establece la URL de la API de Binance
base_url = "https://api.binance.com"

#Establece el tiempo límite en minutos (en milisegundos)
timestamp_limit = 15 * 60 * 1000

#Fecha y hora actual (en milisegundos)
current_timestamp = int(time.time() * 1000)

#Tiempo límite para la consulta (en milisegundos)
timestamp = current_timestamp - timestamp_limit

coins = ['BTC','ETH', 'XRP', 'ADA', 'BNB', 'BCH','LTC', 'TRX', 'ETC', 'LINK','MATIC','IOTA', 'NEO', 'CHZ', 'UNFI', 'FTM', 'DASH', 'ROSE', 'ALICE', 'XMR', 'THETA', 'KAVA', 'DOT','WAVES', 'RVN', 'BLZ', 'MANA', 'ICP', 'DOGE','SHIB','OCEAN']
lista_valores = []

# Clase para poner colores al texto
class bcolors:
    OKGREEN = '\033[92m'
    FAIL = '\033[91m'
    WHITE = '\033[37m'

# define our clear function
def clear():
 
    # for windows
    if name == 'nt':
        _ = system('cls')
 
    # for mac and linux(here, os.name is 'posix')
    else:
        _ = system('clear')

while True:


    for coin in coins:
        coin = coin 
        symbol = coin+"USDT"
        #URL de la consulta
        url = f"{base_url}/api/v3/klines?symbol={symbol}&interval=1m&limit=1&startTime={timestamp}"

        # Realiza la consulta a la API de Binance y obtén la respuesta
        response = requests.get(url, headers={"X-MBX-APIKEY": api_key})

        # Convierte la respuesta a formato JSON
        data = response.json()

        # Obtén el precio de la cripto en Binance hace unos minutos
        ago_price = float(data[0][4])

        # Obtener el precio actual de la moneda utilizando la API de Binance
        url = f"https://api.binance.com/api/v3/ticker/price?symbol={coin}USDT"
        response = requests.get(url)
        data = response.json()
        current_price = float(data['price'])
        # print("Precio actual de BTC: ",current_price)

        # Calcular el cambio porcentual entre el precio actual y el precio hace 1 hora
        change = float((current_price - float(ago_price)) / float(ago_price) * 100)
        lista_valores.append(f"{coin} : {change:.2f}%")

    mayor_a_menor = sorted(lista_valores, key=lambda x: (x.split(":")[1].strip()), reverse=True)

    #menores
    def obtener_valor_negativo(elemento):
        valor = elemento.split(':')[1]
        valor = float(valor.strip().strip('%'))
        return valor

    # Ordenar la lista usando sorted() y proporcionando la función de clave
    lista_menores_al_final = sorted(lista_valores, key=obtener_valor_negativo, reverse=True)
    menor_a_mayor = list(reversed(lista_menores_al_final))

    df1 = pd.DataFrame(menor_a_mayor)
    df2 = pd.DataFrame(mayor_a_menor)

    clear()

    print(f"{bcolors.WHITE}Monedas que más han subido en los últimos minutos:\033[0m ", bcolors.OKGREEN + df2.head(7))
    print(f"{bcolors.WHITE}Monedas que más han bajado en los últimos minutos:\033[0m ", bcolors.FAIL + df1.head(7))

    time.sleep(10)