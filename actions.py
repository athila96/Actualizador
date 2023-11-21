from api_conect import get_products_farmarket, get_product_yummy, products_farmarket, products_yummy

# Para Yummy
new_price = []
new_qty = []


def stores():

    # Para que el diccionario se vea como espero deben estar en orden los arreglos ya que el for lo ordena pocision por pocision 
    # uno de cada lista 1 a 1 .........
    # El location de yummy debe corresponder en pocision a el nombre de la tienda 
    locations_yummy = ['WmOOoWTnYB']
    store_name = ['Lido']
    
    array_store_location = [
        {
            'stores': [] 
        }
    ]

    for stores, locations in zip(store_name, locations_yummy):
        locations_prueba = {
            'stores': [
                {
                    'location': locations,
                    'store_name': stores
                }
            ]
        }
        array_store_location[0]['stores'].append(locations_prueba['stores'][0])

    return array_store_location

# Organiza la informacion de farmarket y de yummy en sus respectivas listas o arrays
def data_organizer(token):   # SE DEBE PROBAR CON AL MENOS 2 TIENDAS PARA VALIDAR QUE EL ARRAY GUARDE LO NECESARIO

   
    result_stores = stores()

    
    for obj_stores in result_stores:
        for store in obj_stores['stores']:
            location = store['location']
            store_name = store['store_name']

            get_products_farmarket(store_name)
            get_product_yummy(token, location)


# Comparamos las listas products_farmarket y products_yummy
def product_comparator():
        # Recorre ambos arreglos y cuenta las coincidencias luego se valida la diferencia de precios y la cantidad para reemplazarlos con los de farmarket.

        for farmarket in products_farmarket:
            for yummy in products_yummy:
                if farmarket['Equivalencia'] == str(yummy['sku']):

                    if farmarket['PVP'] != str(yummy['price']):
                    
                        updated_price = {
                            'location': yummy['location'],
                            'sku': yummy['sku'],
                            'price': farmarket['PVP']
                        }
                
                        new_price.append(updated_price)

                    if farmarket['Cantidad'] != str(yummy['qty_available']):

                        updated_qty = {
                            'location': yummy['location'],
                            'sku': yummy['sku'],
                            'qty_available': farmarket['Cantidad']
                        }

                        new_qty.append(updated_qty)
                        
                        return
    
