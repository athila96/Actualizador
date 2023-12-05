import time
import datetime
import pytz

from actions import data_organizer, product_comparator, deactivador_comparator
from api_conect import create_tokens, put_price, put_qty, put_product_deactivator


    
start_time = time.time()

# Obtén la zona horaria de Venezuela/Caracas
tz_caracas = pytz.timezone('America/Caracas')

tiempo_actual = datetime.datetime.now(tz_caracas)

print('Analizando informacion ...')
token = create_tokens()
data_organizer(token)
product_comparator()
put_price(token)
put_qty(token)

print('Analizando informacion para desactivar productos...')
deactivador_comparator()
put_product_deactivator(token)


end_time = time.time()

elapsed_time = end_time - start_time

data_de_ejecucion = f"Inicio de la ejecucion: {tiempo_actual.strftime('%d-%m-%Y %H:%M:%S')} Tiempo en ejecucion {elapsed_time} segundos"

with open('data_de_ejecucion.txt', 'a') as log_file:
     log_file.write(str(data_de_ejecucion) + '\n')
