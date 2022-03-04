import requests
from bs4 import BeautifulSoup
import pandas as pd


def get_page_content(brand, name):
    URL = "https://www.wollplatz.de/wolle/" + brand + "/" + brand + "-" + name
    website = requests.get(URL)
    return BeautifulSoup(website.content, 'html.parser')


def get_price(page_content):
    span = page_content.find("span", {'class': "product-price"})
    price = span['content']
    return price


def get_delivery_time(page_content):
    tr = page_content.find("tr", {'class': "pbuy-voorraad"})
    delivery_time = tr.find("span")
    return delivery_time.text


def get_info_from_table(to_find, page_content):
    div = page_content.find("div", {'id': "pdetailTableSpecs"})
    tr = div.findAll("tr")
    for i in tr:
        if (i.text.find(to_find) > -1):
            td = i.find_all("td")[-1]
    return td.text


def create_list_obj(price, delivery_time, needle_size, compilation):
    obj = {
        'price': price,
        'delivery_time': delivery_time,
        'needle_size': needle_size,
        'compilation': compilation
    }
    return (obj)


def scrape(products):
    result_list = []
    for i in range(0, len(products)):
        page_content = get_page_content(products[i][0], products[i][1])
        try:
            price = get_price(page_content)
            delivery_time = get_delivery_time(page_content)
            needle_size = get_info_from_table("Nadelstärke", page_content)
            compilation = get_info_from_table("Zusammenstellung", page_content)
            result_list.append(create_list_obj(
                price, delivery_time, needle_size, compilation))
        except:
            print("Die gewünschten Daten waren aus dieser Website nicht auslesbar, bitte überprüfen Sie die angegebene URL")
    return result_list


def create_csv(result_list):
    df = pd.DataFrame(data=result_list)
    df.to_csv("test.csv")


def main():
    products = [["dmc", "natura-xl"], ["drops",  "safran"],
                ["drops", "baby-merino-mix"], ["Hahn", "Alpacca Speciale"]]
    result_list = scrape(products)
    create_csv(result_list)


if __name__ == '__main__':
    main()
