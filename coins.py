import requests
import time
from binance.client import Client
import pandas as pd

#Conectar a la API
api_key = "Q8VOvbFQm74uY9y6drB0YfjYtuotdqqVfZ6dyYVu4VvGE4FtPejb99DIJ9ZKQWVX"

client = Client("Q8VOvbFQm74uY9y6drB0YfjYtuotdqqVfZ6dyYVu4VvGE4FtPejb99DIJ9ZKQWVX", "DVGwkX9h4t61AOW6bCpaH9AmTyHaHL77HJEab5WXfmCv6lKot1fbPirAOGj6SdVa")

#Establece la URL de la API de Binance
base_url = "https://api.binance.com"

#Establece el tiempo límite en minutos (en milisegundos)
timestamp_limit = 18 * 60 * 1000

#Fecha y hora actual (en milisegundos)
current_timestamp = int(time.time() * 1000)

#Tiempo límite para la consulta (en milisegundos)
timestamp = current_timestamp - timestamp_limit

coins = ['BTC','ETH', 'XRP', 'ADA', 'BNB', 'BCH', 'EOS','LTC', 'TRX', 'ETC', 'LINK', 'IOTA', 'NEO', 'ALGO', 'CHZ', 'UNFI', 'FTM']
lista_valores = []

for coin in coins:
    coin = coin 
    symbol = coin+"USDT"
    #URL de la consulta
    url = f"{base_url}/api/v3/klines?symbol={symbol}&interval=1m&limit=1&startTime={timestamp}"

    # Realiza la consulta a la API de Binance y obtén la respuesta
    response = requests.get(url, headers={"X-MBX-APIKEY": api_key})

    # Convierte la respuesta a formato JSON
    data = response.json()

    # Obtén el precio de BTC en Binance hace 18 minutos
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

df1 = pd.DataFrame(menor_a_mayor, columns=["Valores"])
df2 = pd.DataFrame(mayor_a_menor, columns=["Valores"])

print("Monedas que más han bajado en los últimos minutos: ", df1)
print("Monedas que más han subido en los últimos minutos: ", df2)
