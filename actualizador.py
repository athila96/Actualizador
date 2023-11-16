import requests
import urllib.parse
import time
import datetime

from actions import calculate_hash
from links import url, url_create_token, url_get_product, locations, url_put_product_price, url_put_product_qty


# Variables globales
products_farmarket = []
products_yummy = []


# PARA YUMMI

new_price = []
new_qty = []

            # FARMARKET


# Comunicacion con el api de Farmarket para obtener los productos o stock actualizado

def get_products_farmarket():
    key = calculate_hash()
    data_hash = {'auth': key['hash_result']}
    data_seed = {'seed': key['milliseconds']}
    
    auth_hash = urllib.parse.urlencode(data_hash)
    seed = urllib.parse.urlencode(data_seed)
    store_name = "storeName=Lido"    # ESTA VARIABLE DEBE SER DINAMICA YA QUE DEBE ITERAR POR LAS 23 TIENDAS
    

    data = seed + '&' + auth_hash + '&' + store_name

    headers = {
        'Content-Type': 'application/x-www-form-urlencoded'
    }

    try:
        response = requests.post(url, data=data, headers=headers)
        if response.status_code == 200:
            data_products = response.json()
            all_product_fmkt = data_products['data']

            for fmkt in all_product_fmkt:
                products_items_farmarket = {
                    'Equivalencia': fmkt['Equivalencia'],
                    'PVP': fmkt['PVP'],
                    'Cantidad': fmkt['cantidad']
                }

                products_farmarket.append(products_items_farmarket)
            
            # Guardar la respuesta en un archivo de registro (log.txt)
                ''' with open("log.txt", "a") as log_file:
                    log_file.write(str(products_items_farmarket) + "\n") '''

            return 
        
        print(f"La solicitud falló con el código: {response.status_code}")
    except Exception as error:
        print(error)

    


                # YUMMY

# Esta funcion interactua con el api de Yummy y permite crear un token y lo guarda en una variable global.
def create_tokens():
    
    headers = {
         'Content-Type': 'application/json'

    }

# Estas credenciales tienen que estar en otro archivo.
    data ={
        "username":"balbino.brito@gmail.com",
        "password":"P9RsfZY6vEFn" 
    }

    try:
        response = requests.post(url=url_create_token, json=data, headers=headers)

        if response.status_code == 200:
            data_token = response.json()
            access_token = data_token['data']['access_token']

            return access_token

    
    except Exception as error:
        print(error)



# La funcion recibe los productos actuales en Yummy

def get_product_yummy():


    headers = {
        'Content-Type': 'application/json',
        "Authorization": f"Bearer {token}"
    }

    try:
        response = requests.get(url=url_get_product, headers=headers)

        if response.status_code == 200:
            data_product = response.json()

            sort = data_product['data']['menu']['sort']

            for data_sort in sort:
                for all_product in data_product['data']['menu'][data_sort]:
                    product_items_yummy = {
                        'sku': all_product['sku'],
                        'price': all_product['price'],
                        'qty_available': all_product['qty_available']
                    }

                    products_yummy.append(product_items_yummy) 

                    ''' with open("product.txt", "a") as log_file:
                        log_file.write(str(product_items_yummy) + "\n") '''

        return 


    except Exception as error:
        print(error)

   


#   SE DEBE MODIFICAR EL TIPO DE DATO YA QUE FMKT DEVUELVE STRING Y YUMMI DEVUELVE INT
def product_comparator():

    get_products_farmarket()
    get_product_yummy()

    # Recorre ambos arreglos y cuenta las coincidencias luego se valida la diferencia de precios y se actualizan con los de farmarket

    for farmarket in products_farmarket:
        for yummy in products_yummy:
            if farmarket['Equivalencia'] == str(yummy['sku']):

                if farmarket['PVP'] != str(yummy['price']):
                  
                    updated_price = {
                        'sku': yummy['sku'],
                        'price': farmarket['PVP']
                    }
             
                    new_price.append(updated_price)

                if farmarket['Cantidad'] != str(yummy['qty_available']):

                    updated_qty = {
                        'sku': yummy['sku'],
                        'qty_available': farmarket['Cantidad']
                    }

                    new_qty.append(updated_qty)
                    
                    return
            


def put_price():

    headers = {
        "Authorization": f"Bearer {token}",
        'Content-Type': 'application/json'
    }

    array_products_price = []
    for prices in new_price:
        price_ultimate = {
                    'sku': prices['sku'], 
                    'locations':[
                        {
                            'location': locations,
                            'price': float(prices['price']) 
                        }
                    ]
                }
        array_products_price.append(price_ultimate)
        
    
    data = {
        'type': 'price',
        'products': array_products_price
    }


    with open("data_price.txt", "a") as log_file:
                    log_file.write(str(data) + "\n")

    try:
        response = requests.put(url=url_put_product_price, json=data, headers=headers)

        if response.status_code == 200:
             print('Precio de los roductos actualizados con exito')
             return
        elif response.status_code == 400:
             print("No hay nuevas actualizaciones para aplicar")
             return
        
        print('Error de put_price: ', response.status_code)
        
    
    except Exception as error:
        print(error)

    

def put_qty():
        
    headers = {
        "Authorization": f"Bearer {token}",
        'Content-Type': 'application/json'
    }
        
    
    array_product_qty = []
    for qty in new_qty:
        qty_ultimate = {
                    'sku': qty['sku'], 
                    'qty':[
                        {
                          locations : qty['qty_available']
                        }
                    ]
                }
        array_product_qty.append(qty_ultimate)
        
    
    data = {
        'type': 'inventory',
        'products': array_product_qty,
        'toggle_mode' : False
    }

    with open("data_qty.txt", "a") as log_file:
                    log_file.write(str(data) + "\n")

    try:
        response = requests.put(url=url_put_product_qty, json=data, headers=headers)

        if response.status_code == 200:
            print('La cantidad se actualizo correctamente')
            return
            
        elif response.status_code == 400:
             print("No hay nuevas actualizaciones para aplicar")
             return
        
        print('Error de put_qty: ', response.status_code)
            
        
        

    except Exception as error:
        print(error)

    
start_time = time.time()

tiempo_actual = datetime.datetime.now()

token = create_tokens()
product_comparator()
put_price()
put_qty()

end_time = time.time()

elapsed_time = end_time - start_time

data_de_ejecucion = f"Inicio de la ejecucion: {tiempo_actual.strftime('%d-%m-%Y %H:%M:%S')} \n Tiempo en ejecucion {elapsed_time} segundos"

with open('data_de_ejecucion.txt', 'a') as log_file:
     log_file.write(str(data_de_ejecucion) + '\n')
