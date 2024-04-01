import requests
from bs4 import BeautifulSoup
from data import user, session, url, csrfmiddlewaretoken, journal, objects


def main():
    data = dict(username=user["username"], password=user["password"],
                csrfmiddlewaretoken=csrfmiddlewaretoken, next='/')
    response = session.post(url, data=data, headers=dict(Referer=url))

    cookies_dict = [
        {"domain": key.domain, "name": key.name,
            "path": key.path, "value": key.value}
        for key in session.cookies
    ]

    session2 = requests.Session()

    for cookies in cookies_dict:
        session2.cookies.set(**cookies)

    resp = session2.get(journal, headers=dict(Referer=url)).text

    def getInfo():
        # Заголовки предметів
        soup = BeautifulSoup(resp, "lxml")

        verify = soup.find('div', class_="login")
        if verify:
            return False
        else:
            div = soup.find_all('div', class_="st_journal__info")
            for item in div:
                objects[(str(item.find('h1').text).split(
                    " - ")[1])] = {}

            # дата клітинки
            temp_date = []

            tables_objects = soup.find_all(
                'tr', class_="st_journal__journal_row journal_row")
            for i in range(len(tables_objects)):
                temp_date.append([])
                table = tables_objects[i].find_all('th', class_=["journal__cell journal_header lesson_date",
                                                   "journal__cell journal_header journal__cell_name", "journal__cell journal_header journal__cell_number"])
                for j in table:
                    temp_date[i].append({j.text.strip(): "-"})

            temp_date = [i for i in temp_date if i]

            b = 0
            for key, value in objects.items():
                objects[key] = temp_date[b]
                b += 1
            b = 0

            table_marks = soup.find_all('td', class_='journal__cell')
            for key, value in objects.items():

                for days in value:
                    days[list(days.keys())[0]] = table_marks[b].text.strip()
                    b += 1
            b = 0
            print("+")
            return True
    return getInfo()
