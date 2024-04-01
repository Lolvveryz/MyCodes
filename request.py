import requests
def geter():
    url = "https://www.ratatype.ua/api/v1/user/info/exercise-entrypoint/0"

    payload = ""
    headers = {
        # переходите на сайт , відкриваєте Тренажер
        # ПКМ > Переглянути код елементу 
        # У менюшці що відкрилась переходите на вкладку "Network"
        # Оновлюєте сторінку і шукаєте файл з назвою "0/"

        "cookie": "vse_u=", # У файлі "0/" відкриваєте вкладку "Cookies" і копіюєте значання , відповідне до "vse_u" і вставляєте сюди !!після знаку "="!!
                       # ^ тобто сюди
        "authorization": "Bearer.." # У файлі "0/" відкриваєте вкладку "Headers" , і шукаєте "Аuthorization" , і копіюєте відповідне значення що починається з Bearer і закінчується аж над "Cookies"
    }

    response = requests.request("GET", url, data=payload, headers=headers).json()['exercise']['string']
    return response