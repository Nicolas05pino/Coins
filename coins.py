import requests
import time
from binance.client import Client
import pandas as pd
import config

#colores
class bcolors:
    OKGREEN = '\033[92m'
    FAIL = '\033[91m'
    WHITE = '\033[37m'

#Conectar a la API
api_key = config.API_KEY

client = Client(config.API_KEY, config.API_SECRET)

#Establece la URL de la API de Binance
base_url = "https://api.binance.com"

tiempos = [8,15,30]

for tiempo in tiempos: 

    def calcular():

        timestamp_limit = tiempo * 60 * 1000  #Establece el tiempo límite en minutos (en milisegundos)
        #Fecha y hora actual (en milisegundos)
        current_timestamp = int(time.time() * 1000)

        #Tiempo límite para la consulta (en milisegundos)
        timestamp = current_timestamp - timestamp_limit

        response = requests.get("https://api.binance.com/api/v3/ticker/24hr")
        data = response.json()

        #vol

        # URL de la API de Binance
        url = "https://fapi.binance.com/fapi/v1/ticker/24hr"

        # Realiza una solicitud a la API
        response = requests.get(url)

        # Verifica si la respuesta es exitosa
        if response.status_code == 200:
            # Convierte la respuesta en un diccionario de Python
            data1 = response.json()
            # Crea una lista para guardar las criptomonedas con volumen mayor a 100.000.000
            criptomonedas = []
            # Recorre todas las criptomonedas
            for moneda in data1:
                # Verifica si el volumen es mayor a 100.000.000 y si el par es USDT
                if moneda["symbol"].endswith("USDT") and float(moneda["quoteVolume"]) > 100000000:
                    # Agrega la criptomoneda a la lista
                    criptomonedas.append(moneda["symbol"][:-4])
            # print(criptomonedas)

        def remove_numbers_from_names(coins_list):
            for i, coin in enumerate(coins_list):
                new_coin = ''.join([c for c in coin if not c.isdigit()])
                coins_list[i] = new_coin
            return coins_list

        output = remove_numbers_from_names(criptomonedas)

        for coin in output:
            if coin in ["FTT", "SRM", "BNX", "C", "INCH",'API']:
                output.remove(coin)

        # print(output)

        #//vol 

        # coins = ['BTC','ETH', 'XRP', 'ADA', 'BNB', 'BCH','LTC', 'TRX', 'ETC', 'LINK','MATIC','IOTA', 'NEO', 'CHZ', 'UNFI', 'FTM', 'DASH', 'ROSE', 'ALICE', 'XMR', 'THETA', 'KAVA', 'DOT','WAVES', 'RVN', 'BLZ', 'MANA', 'ICP', 'DOGE','SHIB','OCEAN']
        lista_valores = []

        for coin in output:
            coin = coin
            symbol = coin+'USDT' 

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
            # print("Precio actual de la moneda: ",current_price)

            # Calcular el cambio porcentual entre el precio actual y el precio hace 15 min
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

        print(f"{bcolors.WHITE}Monedas que más han subido en los últimos {tiempo} minutos:\033[0m ", bcolors.OKGREEN + df2.head(5))
        print(f"{bcolors.WHITE}Monedas que más han bajado en los últimos {tiempo} minutos:\033[0m ", bcolors.FAIL + df1.head(5))

    calcular()