from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes

from app.optidata.core.src.config import settings, constantes
from app.optidata.core.src.database import MongoAPI
from app.optidata.core.src.enums.enums import EventsLogsEnum
from app.optidata.core.src.log import AuditoryLogs
from app.optidata.core.src.utility import get_datetime


def set_config_params(json_dict: dict):
    data = {
        'collection': settings.MONGO_COLLECTION_DATA_CONFIG_PARAMS,
        'Filter': {
            'name_param': 'aes_key'
        }
    }
    mongodb = MongoAPI(data)
    response = mongodb.read()
    if len(response) == 0:
        aes_key = get_random_bytes(16)
        data = {
            'collection': settings.MONGO_COLLECTION_DATA_CONFIG_PARAMS,
            'Document': {
                'name_param': 'aes_key',
                'value_param': aes_key,
                'created_at': get_datetime()
            },
            'Filter': {
                'name_param': 'aes_key'
            }
        }
        mongodb = MongoAPI(data)
        mongodb.write(data)
    else:
        aes_key = response['value_param']

    cipher = AES.new(aes_key, AES.MODE_OCB)
    ciphertext, tag = cipher.encrypt_and_digest(json_dict.get('value_param').encode())

    response = None
    try:
        data = {
            'collection': settings.MONGO_COLLECTION_DATA_CONFIG_PARAMS,
            'Document': {
                'name_param': json_dict.get('name_param'),
                'tag_param': tag,
                'nonce_param': cipher.nonce,
                'text_param': ciphertext,
                'created_date': get_datetime()
            },
            'Filter': {
                'name_param': json_dict.get('name_param')
            }
        }

        mongodb = MongoAPI(data)
        response = mongodb.write(data)
    except Exception as ex:
        AuditoryLogs.registry_log(
            origin=f'{__name__}.set_config_params',
            event=EventsLogsEnum.EVENT_ERROR,
            description=f'Error al obtener los datos: {ex}',
            user=constantes.USER_DEFAULT
        )

    return response


def get_config_params(json_dict: dict):
    response = None
    data = {
        'collection': settings.MONGO_COLLECTION_DATA_CONFIG_PARAMS,
        'Filter': {
            'name_param': 'aes_key'
        }
    }
    mongodb = MongoAPI(data)
    result = mongodb.read()
    aes_key = result['value_param']
    try:
        data = {
            'collection': settings.MONGO_COLLECTION_DATA_CONFIG_PARAMS,
            'Filter': {
                'name_param': json_dict.get('name_param')
            }
        }

        mongodb = MongoAPI(data)
        response = mongodb.read()
        if len(response) > 0:
            key = dict(response[0])
            ciphertext = key.get('text_param')
            tag = key.get('tag_param')
            nonce = key.get('nonce_param')

            cipher = AES.new(aes_key, AES.MODE_OCB, nonce=nonce)
            try:
                message = cipher.decrypt_and_verify(ciphertext, tag)
                response = message.decode()
            except ValueError as ex:
                AuditoryLogs.registry_log(
                    origin=f'{__name__}.get_config_params',
                    event=EventsLogsEnum.EVENT_ERROR,
                    description=f'Error al obtener los datos: {ex}',
                    user=constantes.USER_DEFAULT
                )
        else:
            AuditoryLogs.registry_log(
                origin=f'{__name__}.get_config_params',
                event=EventsLogsEnum.EVENT_ERROR,
                description=f'El parámetro {json_dict.get("name_param")} no existe',
                user=constantes.USER_DEFAULT
            )

    except Exception as ex:
        AuditoryLogs.registry_log(
            origin=f'{__name__}.get_config_params',
            event=EventsLogsEnum.EVENT_ERROR,
            description=f'Error al obtener los datos: {ex}',
            user=constantes.USER_DEFAULT
        )

    return response
