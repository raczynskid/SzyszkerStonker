import os
import time
from datetime import datetime

import pandas as pd

save_to_location = "C:/Stonker/"
if not os.path.isdir(save_to_location):
    os.mkdir(save_to_location)


def get_all_stocks(page: int = 0, dataframes=[]):
    # recursively paginate through stock price tables
    url = "https://strefainwestorow.pl/notowania/spolki"
    try:
        df = pd.read_html(url + "?page=" + str(page))[0]
        print(f"getting from page {page + 1}...")
    except ValueError:
        return pd.concat(dataframes).reset_index(drop=True)

    dataframes.append(df)
    page += 1
    time.sleep(.300)
    return get_all_stocks(page, dataframes)


def get_dividends(year: int):
    url = f"https://strefainwestorow.pl/dane/dywidendy/lista-dywidend/{str(year)}"
    tables = pd.read_html(url)
    return tables[0], tables[1]


if __name__ == '__main__':
    # get stock prices
    results = get_all_stocks()
    # save stock prices
    results.to_csv(save_to_location + f"stocks{datetime.now().strftime('%Y_%m_%d')}.csv")

    # get dividends data for current year
    cy = datetime.now().year
    to_buy, already_set = get_dividends(cy)

    # save dividends data
    # to_buy - Akcje spółek z prawem do dywidendy, które możesz kupić, aby otrzymać dywidendę z zysku za bieżacy rok
    # already_set - Akcje spółek, które miały już ustalenie prawa do dywidendy w bieżącym roku
    to_buy.to_csv(save_to_location + f"dividends_to_buy_{cy}.csv")
    already_set.to_csv(save_to_location + f"dividends_already_set_{cy}.csv")
