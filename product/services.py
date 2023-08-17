import json
import random
import time

import jwt
import requests
from PIL import Image
from sqlalchemy.orm import Session

from ml_analytics.full_pipeline import get_product_by_link
from ml_analytics.get_analytics import get_analytics
from ml_analytics.get_regressor_predict_by_product import get_predict
from product.constants import *
from product.crud import create_product, get_products
from product.models import Product, ProductCreate
from storage_functions import upload_file, get_file_url
from user.models import User


def _login_gpt() -> str:
    now = int(time.time())
    payload = {'aud': 'https://iam.api.cloud.yandex.net/iam/v1/tokens', 'iss': SERVICE_ACCOUNT_ID,
               'iat': now, 'exp': now + 360}
    # JWT generation
    encoded_token = jwt.encode(payload, PRIVATE_KEY, algorithm='PS256', headers={'kid': KEY_ID})
    url = 'https://iam.api.cloud.yandex.net/iam/v1/tokens'
    x = requests.post(url, headers={'Content-Type': 'application/json'},
                      json={'jwt': encoded_token}).json()
    token = x['iamToken']
    return token


def get_text_from_gpt(mode: str, description: str):
    token = _login_gpt()
    url = 'https://api.ml.yandexcloud.net/llm/v1alpha/instruct'

    # Building a prompt
    data = {"model": "general"}

    # Specify an instruction for YandexGPT
    if mode == 'comment':
        data['instruction_text'] = 'Ты купил товар. Теперь ты должен написать отзыв о нем.'
    else:
        data['instruction_text'] = 'Ты должен придумать описание товара, которое поможет продать ' \
                                   'товар в интернет магазине.'
    # Set up advanced model parameters
    data['generation_options'] = {'max_tokens': 1500,
                                  'temperature': 0.5}
    # Enter the request text
    if mode == 'comment':
        data['request_text'] = "Придумай реалистичный отзыв о " + description + '.'
    else:
        data['request_text'] = "Придумай описание " + description + '.'

    # Get the model's response
    response = requests.post(url, headers={'Authorization': 'Bearer ' + token}, json=data).json()
    print(response)
    response_text = response['result']['alternatives'][0]['text']
    return response_text


def product_analytics(product: Product | ProductCreate) -> dict:
    dict_product = product.dict()
    pop_args = ["id", "user_id", "created_datatime"]
    for el in pop_args:
        if el in dict_product:
            dict_product.pop(el)
    if "text_params" in dict_product:
        dict_product["text_params"] = dict_product["text_params"].split("~")
    else:
        dict_product["text_params"] = []
    analytics = get_analytics(dict_product)
    img_link = dict_product["img_link"]
    img_data = requests.get(img_link).content
    if isinstance(product, Product):
        file_name = f'{product.id}.jpg'
    else:
        file_name = f"{''.join(random.choices([chr(i) for i in range(ord('A'), ord('Z') + 1)], k=4))}.jpg"
    with open(file_name, 'wb') as handler:
        handler.write(img_data)
    img = Image.open(file_name)
    predict = get_predict(dict_product, img)
    os.remove(file_name)
    analytics["predict"] = predict
    return analytics


async def get_product_from_wb(product_url: str, user: User, session: Session) -> Product:
    product_json = get_product_by_link(product_url)
    product_json["user_id"] = user.id
    if product_json["text_params"] is not None:
        product_json["text_params"] = '~'.join(product_json["text_params"])
    product = ProductCreate(**product_json)
    product = create_product(product_create=product, session=session)
    data = product_analytics(product)
    with open(f"{product.id}.json", 'w') as f:
        json.dump(data, f)
    file = open(f"{product.id}.json", "rb")
    await upload_file(f"product_analytic/{product.id}.json", file.read())
    os.remove(f"{product.id}.json")
    return product


def get_product_list(user: User, session: Session) -> list[Product]:
    return get_products(session=session, user_id=user.id)


async def get_product_stat(product: Product) -> dict:
    file_url = get_file_url(f"product_analytic/{product.id}.json")
    data = requests.get(file_url).json()
    return {"product": product, "statistic": data}
