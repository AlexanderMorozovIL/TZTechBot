import re
from statistics import mean

import pandas as pd
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager


df = pd.read_excel('data.xlsx')

url = df['url'][0]
xpath_query = df['xpath'][0]

chrome_options = Options()
chrome_options.add_experimental_option('detach', True)

driver = Chrome(
    service=Service(ChromeDriverManager().install()),
    options=chrome_options
)

driver.get(url)
driver.maximize_window()


def get_numeric_prices():
    """
    Получает числовые значения цен из элементов веб-страницы,
    основываясь на заданных XPath-запросах.
    """
    prices = []
    results = driver.find_elements('xpath', xpath_query)

    for result in results:
        str_price = result.get_attribute('innerHTML')
        str_price = re.sub(r'[^\d.,]', '', str_price)
        str_price = str_price.replace(',', '.')
        numeric_price = float(str_price)
        prices.append(numeric_price)

    return prices


def get_avg_price(prices):
    """Вычисляет среднее значение цен из списка числовых значений цен."""
    avg_price = round(mean(prices), 2)
    return avg_price


def main():
    """
    Основная функция для вычисления и вывода средней цены.
    Выводит среднюю цену, вычисленную на основе числовых значений цен,
    полученных из веб-страницы.
    """
    print(
            get_avg_price(
                get_numeric_prices()
            )
    )


if __name__ == '__main__':
    main()
