import requests
import urllib.parse
import datetime as dt
import hashlib


from utils import url, url_create_token, user_data

import actions 


# Variables globales
products_farmarket = []
products_yummy = []


# FARMARKET

def calculate_hash():
    pre_shared_key = "F4rm4rk3t_S13mpr3_H4y!"
    current_date_and_time = dt.datetime.now()
    milliseconds = int(current_date_and_time.timestamp() * 1000)
    key_union = str(milliseconds) + pre_shared_key

    hash265 = hashlib.sha256()
    hash265.update(key_union.encode('utf-8'))
    hash_result = hash265.hexdigest()


    return {'hash_result': hash_result, 'milliseconds': milliseconds}

# Comunicacion con el api de Farmarket para obtener los productos o stock actualizado
def get_products_farmarket(name_store): # Recordar eliminar esta funcion de actualizador
    key = calculate_hash()
    data_hash = {'auth': key['hash_result']}
    data_seed = {'seed': key['milliseconds']}
    
    auth_hash = urllib.parse.urlencode(data_hash)
    seed = urllib.parse.urlencode(data_seed)

    store_name = f'storeName={name_store}'   # ESTA VARIABLE DEBE SER DINAMICA YA QUE DEBE ITERAR POR LAS 23 TIENDAS
    

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

# Esta funcion interactua con el api de Yummy, permite crear un token y lo returna
def create_tokens(): 
    
    headers = {
         'Content-Type': 'application/json'

    }

    try:
        response = requests.post(url=url_create_token, json=user_data, headers=headers)

        if response.status_code == 200:
            data_token = response.json()
            access_token = data_token['data']['access_token']

            return access_token

    
    except Exception as error:
        print(error)

# La funcion recibe los productos actuales en Yummy
def get_product_yummy(token, location, partner_id): # Mudamos esta funcion a api_conect

    url_get_product = f""

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
                        'location': location,
                        'partner_id': partner_id,
                        'sku': all_product['sku'],
                        'price': all_product['price'],
                        'qty_available': all_product['qty_available'],
                        'enabled': all_product['enabled'],
                        'objectId': all_product['objectId']
                    }

                    products_yummy.append(product_items_yummy) 

                    ''' with open("product.txt", "a") as log_file:
                        log_file.write(str(product_items_yummy) + "\n") '''

        return 
    
    except Exception as error:
        print(error)


# Actualiza el precio en la app de Yummy
def put_price(token):

    headers = {
        "Authorization": f"Bearer {token}",
        'Content-Type': 'application/json'
    }

    array_products_price = []
    partner_id = ''
    for prices in actions.new_price:
        price_ultimate = {
                    'sku': prices['sku'], 
                    'locations':[
                        {
                            'location': prices['location'],
                            'price': float(prices['price']) 
                        }
                    ]
                }
        partner_id = prices['partner_id']
        array_products_price.append(price_ultimate)
        
    if array_products_price == []:
         print('Todo marcha bien...')
         return

    data = {
        'type': 'price',
        'products': array_products_price
    }

    
    with open("Logs/data_price.txt", "a") as log_file:
                    log_file.write(str(data) + "\n")

    url_put_product_price = f''

    try:
        response = requests.put(url=url_put_product_price, json=data, headers=headers)

        if response.status_code == 200:
             print('Precio de los roductos actualizados con exito')
             return
        elif response.status_code == 400:
             print("No hay nuevas actualizaciones para aplicar")
             return
        
        with open("Error/Errores_price.txt", "a") as log_file:
            log_file.write(str(response.status_code) + "\n")

        print('Error de put_price: ', response.status_code)
        
    
    except Exception as error:
        print(error)


# Actualiza la cantidad (el stock) en la app de Yummy
def put_qty(token):
        
    headers = {
        "Authorization": f"Bearer {token}",
        'Content-Type': 'application/json'
    }
        
    
    array_product_qty = []
    partner_id = ''
    for qty in actions.new_qty:
        qty_ultimate = {
                    'sku': qty['sku'], 
                    'qty':[
                        {
                          qty['location'] : qty['qty_available']
                        }
                    ]
                }
        partner_id = qty['partner_id']
        array_product_qty.append(qty_ultimate)
        
    if array_product_qty == []:
         print('Todo marcha bien...')
         return
    
    data = {
        'type': 'inventory',
        'products': array_product_qty,
        'toggle_mode' : False
    }

    with open("Logs/data_qty.txt", "a") as log_file:
                    log_file.write(str(data) + "\n")

    url_put_product_qty = f'h' 

    try:
        response = requests.put(url=url_put_product_qty, json=data, headers=headers)

        if response.status_code == 200:
            print('La cantidad se actualizo correctamente')
            return
            
        elif response.status_code == 400:
             print("No hay nuevas actualizaciones para aplicar")
             return

        with open("Error/Errores_qty.txt", "a") as log_file:
                    log_file.write(str(response.status_code) + "\n")
        
        print('Error de put_qty: ', response.status_code)
        

    except Exception as error:
        print(error)

# Desactiva los productos de la app de yummy cuando farmarket no tiene stock
def put_product_deactivator(token):
     
    headers = {
        "Authorization": f"Bearer {token}",
        'Content-Type': 'application/json'
    }


    deactivate = []
    partner_id = ''

    for list_product in actions.desactivate:
        partner_id = list_product['partner_id']
        deactivate.append(list_product['sku'])
        

    
    if deactivate == []:
        print('No hay ningun producto para desactivar')
        return
    

    data = {
         'type': 'deactivate',
         'productsSku': deactivate
    }

    url = f''

    try: 
         response = requests.put(url=url, json=data, headers=headers)

         if response.status_code == 200: 
              print('Se desactivaron los productos correctamente')
              return
         
         elif response.status_code == 400:
            print("Ningun producto a desactivar")
            return
         
         with open("Error/Errores_desactivando.txt", "a") as log_file:
                    log_file.write(str(response.status_code) + "\n")

         print('Error al desactivar productos: ', response.status_code)
    
    except Exception as error:
        print(error)


def put_prduct_activate(token):
     
    headers = {
        "Authorization": f"Bearer {token}",
        'Content-Type': 'application/json'
    }

    if actions.activate == []:
         print('El arreglo activate esta vacio. No hay nada que actualizar.')
         return
    
    location = ''
    product_id = ''
    enabled = ''

    for activate_product in actions.activate:
         location = activate_product['location']
         product_id = activate_product['objectId']
         enabled = activate_product['enabled']

    data = {'enabled': enabled}

    url = f''

    try:
         
        response = requests.put(url=url, json=data, headers=headers)

        if response.status_code == 200:
             
             data_json = response.json()

             with open("Logs/Productos_activados.txt", "a") as log_file:
                  log_file.write(str(data_json) + '\n')

                  return

        with open("Error/Error_productos_activados.txt", "a") as log_file:
                  log_file.write(str('Error: ', response.status_code) + '\n')

                  return 
        
        

    except Exception as error:
         print(error)
    


