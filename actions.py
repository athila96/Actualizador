import datetime as dt
import hashlib

def calculate_hash():
    pre_shared_key = ""
    current_date_and_time = dt.datetime.now()
    milliseconds = int(current_date_and_time.timestamp() * 1000)
    key_union = str(milliseconds) + pre_shared_key

    hash265 = hashlib.sha256()
    hash265.update(key_union.encode('utf-8'))
    hash_result = hash265.hexdigest()


    return {'hash_result': hash_result, 'milliseconds': milliseconds}




