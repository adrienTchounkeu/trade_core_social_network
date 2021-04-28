from celery import shared_task
from .models import User
import requests
from .settings import env
import json


@shared_task
def data_enrichment(email):
    print("Data enrichment")
    user = User.objects.get(pk=email)
    response = requests.get("https://ipgeolocation.abstractapi.com/v1/?api_key={}"
                            .format(env('GEOLOCATION_API_KEY')))
    content = json.loads(response.content)
    ip_address = content['ip_address']
    print(ip_address)
    country = content['country']
    user.geolocation_data_ip = ip_address
    user.geolocation_data_country = country

    country_code = content['country_code']
    from datetime import datetime
    current_day = datetime.now().day
    current_month = datetime.now().month
    current_year = datetime.now().year
    response = requests.get("https://holidays.abstractapi.com/v1/?api_key={}&country={}&year={}&month={}&day={}"
                            .format(env('HOLIDAY_API_KEY'), country_code, current_year, current_month, current_day))
    content = json.loads(response.content)
    if len(content) != 0:
        holiday = content[0]
        user.holiday = holiday.name

    print("Data enrichment -- last")
    user.save()