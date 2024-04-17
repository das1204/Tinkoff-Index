import numpy as np
import requests
import pandas as pd
from datetime import date
from colorama import Fore, Style
import warnings
import os

warnings.filterwarnings('ignore')

checkpoint = f'{date.today().month}.{date.today().year}'

url_glob = 'https://index.tinkoff.ru/corona-index/papi'

path_to_archive = './archive'

regs = ['Алтайский край',
        'Амурская область',
        'Архангельская область',
        'Астраханская область',
        'Белгородская область',
        'Брянская область',
        'Владимирская область',
        'Волгоградская область',
        'Вологодская область',
        'Воронежская область',
        'Забайкальский край',
        'Ивановская область',
        'Иркутская область',
        'Кабардино-Балкарская Республика',
        'Калининградская область',
        'Калужская область',
        'Камчатский край',
        'Карачаево-Черкесская Республика',
        'Кемеровская область',
        'Кировская область',
        'Костромская область',
        'Краснодарский край',
        'Красноярский край',
        'Курганская область',
        'Курская область',
        'Ленинградская область',
        'Липецкая область',
        'Москва',
        'Московская область',
        'Мурманская область',
        'Нижегородская область',
        'Новгородская область',
        'Новосибирская область',
        'Омская область',
        'Оренбургская область',
        'Орловская область',
        'Пензенская область',
        'Пермский край',
        'Приморский край',
        'Псковская область',
        'Республика Адыгея',
        'Республика Башкортостан',
        'Республика Бурятия',
        'Республика Дагестан',
        'Республика Калмыкия',
        'Республика Карелия',
        'Республика Коми',
        'Республика Крым',
        'Республика Марий Эл',
        'Республика Мордовия',
        'Республика Саха (Якутия)',
        'Республика Северная Осетия-Алания',
        'Республика Татарстан',
        'Республика Тыва',
        'Республика Хакасия',
        'Россия',
        'Ростовская область',
        'Рязанская область',
        'Самарская область',
        'Санкт-Петербург',
        'Саратовская область',
        'Сахалинская область',
        'Свердловская область',
        'Смоленская область',
        'Ставропольский край',
        'Тамбовская область',
        'Тверская область',
        'Томская область',
        'Тульская область',
        'Тюменская область',
        'Удмуртская Республика',
        'Ульяновская область',
        'Хабаровский край',
        'Ханты-Мансийский АО',
        'Челябинская область',
        'Чеченская Республика',
        'Чувашская Республика',
        'Ямало-Ненецкий АО',
        'Ярославская область']

regions = ['Белгородская область',
           'Брянская область',
           'Владимирская область',
           'Воронежская область',
           'Ивановская область',
           'Калужская область',
           'Костромская область',
           'Курская область',
           'Липецкая область',
           'Москва',
           'Московская область',
           'Орловская область',
           'Рязанская область',
           'Смоленская область',
           'Тамбовская область',
           'Тверская область',
           'Тульская область',
           'Ярославская область']

business_types = {
    1: 'E-commerce',
    2: 'IT-услуги и разработка ПО',
    3: 'Автоуслуги',
    4: 'Аренда и лизинг',
    5: 'Бытовые услуги',
    6: 'Гостиницы',
    7: 'Грузоперевозки',
    # 8: 'Неизвестность №8',
    # 9: 'Неизвестность №9',
    10: 'ЖКХ',
    # 11: 'Неизвестность №11',
    12: 'Кафе и рестораны',
    13: 'Консалтинг в различных сферах',
    14: 'Красота',
    15: 'Легкая промышленность',
    16: 'Научная и техническая деятельность',
    17: 'Обрабатывающая промышленность',
    18: 'Образование',
    19: 'Обслуживание транспорта, cкладов',
    20: 'Общественные организации',
    21: 'Оптовая торговля компьютерами и ПО',
    22: 'Оптовая торговля продуктами',
    23: 'Оптовая торговля стройматериалами',
    24: 'Организация конференций и выставок',
    25: 'Пассажироперевозки',
    26: 'Почта и курьеры',
    27: 'Продуктовые магазины',
    28: 'Производство',
    29: 'Прочая оптовая торговля',
    30: 'Прочая розничная торговля',
    # 31: 'Неизвестность №31',
    32: 'Развлечения, культура, спорт',
    33: 'Розничная торговля книгами и игрушками',
    34: 'Розничная торговля одеждой',
    35: 'Розничная торговля электроникой',
    36: 'Сельское хозяйство',
    37: 'Строительство',
    38: 'Телекоммуникации, связь, издательства',
    39: 'Туристические агентства',
    40: 'Услуги в сегменте недвижимости',
    # 41: 'Неизвестность №41',
    # 42: 'Неизвестность №42',
    # 43: 'Неизвестность №43'
}

consumer_types = {
    # 1: 'Неизвестность №1',
    2: 'Авиабилеты',
    3: 'Автоуслуги',
    4: 'Аптеки',
    5: 'Аренда авто',
    # 6: 'Неизвестность №6',
    7: 'Дом, ремонт',
    8: 'Ж/д билеты',
    9: 'Животные',
    # 10: 'Неизвестность №10',
    11: 'Кино',
    12: 'Книги',
    13: 'Красота',
    14: 'Мед. услуги',
    # 15: 'Неизвестность №15',
    # 16: 'Неизвестность №16',
    17: 'Образование',
    18: 'Одежда, обувь',
    19: 'Отели',
    20: 'Развлечения',
    21: 'Рестораны',
    22: 'Связь, телеком',
    # 23: 'Неизвестность №23',
    24: 'Спорттовары',
    # 25: 'Неизвестность №25',
    26: 'Супермаркеты',
    27: 'Топливо',
    28: 'Транспорт',
    29: 'Турагентства',
    30: 'Фастфуд',
    # 31: 'Неизвестность №31',
    32: 'Цветы',
    # 33: 'Неизвестность №33'
}


def pars_consumer(region_name, request_total, request_charts, dict_types, curve_date):
    dates = []
    index = []
    var_of_shopping = []
    for index_20 in range(len(request_total.get('consumerTotalPoints'))):
        dates.append(request_total.get('consumerTotalPoints')[index_20].get('date')[:10])
        index.append(request_total.get('consumerTotalPoints')[index_20].get('index_20'))
        var_of_shopping.append(request_total.get('consumerTotalPoints')[index_20].get('customers_activity_20'))

    df = pd.DataFrame(
        {
            'Регион': region_name,
            'Дата': dates,
            'Tinkoff Index': index,
            'Разнообразие покупок': var_of_shopping
        }
    ).drop_duplicates(subset=['Дата'])

    for key, value in dict_types.items():
        values = []
        for activity_20 in range(len(request_charts.get('consumer').get(str(key)))):
            if request_charts.get('consumer').get(str(key))[activity_20].get('date')[:10] in curve_date:
                values.append(request_charts.get('consumer').get(str(key))[activity_20 - 1].get('activity_20'))
            values.append(request_charts.get('consumer').get(str(key))[activity_20].get('activity_20'))
        if len(values) < len(df['Дата']):
            values = values + [np.NAN] * (len(df['Дата']) - len(values))
        df[f'{value}, %'] = values
        df = df.sort_values(by=['Дата'])
    return df


def pars_business(region_name, request_total, request_charts, dict_types):
    dates = []
    index = []
    for business_activity_20 in range(len(request_total.get('businessTotalPoints'))):
        dates.append(request_total.get('businessTotalPoints')[business_activity_20].get('date')[:10])
        index.append(request_total.get('businessTotalPoints')[business_activity_20].get('business_activity_20'))

    df = pd.DataFrame(
        {
            'Регион': region_name,
            'Дата': dates,
            'Обороты бизнеса': index
        }
    ).drop_duplicates(subset=['Дата']).sort_values(by=['Дата'])

    for key, value in dict_types.items():
        values = []
        for activity_20 in range(len(request_charts.get('business').get(str(key)))):
            values.append(request_charts.get('business').get(str(key))[activity_20].get('activity_20'))
        df[f'{value}, %'] = values
        df = df.sort_values(by=['Дата'])
    return df


def old_file_killer(file_name):
    if 'Business' in file_name:
        try:
            os.remove(file_name)
            print(f'[-] Старый файл по оборотам бизнеса {Fore.RED + "удалён" + Style.RESET_ALL}.\n')
        except Exception as e:
            print(f'[-] {e}')
    else:
        try:
            os.remove(file_name)
            print(f'[-] Старый файл по тратам потребителей {Fore.RED + "удалён" + Style.RESET_ALL}.\n')
        except Exception as e:
            print(f'\n[-] {e}')


def URL_form(region, iteration, start_date, end_date):
    print(f'\t[+] {region} - ' + f'{Fore.GREEN + f"{iteration + 1}/{len(regs)}" + Style.RESET_ALL}')
    if str(region) == 'Россия':
        url_total = f'{url_glob}/period_region_total?regionName=all&start={start_date}&end={end_date}'
        url_charts = f'{url_glob}/period_categories_charts?regionName=all&start={start_date}&end={end_date}'
    else:
        url_total = f'{url_glob}/period_region_total?regionName={region}&start={start_date}&end={end_date}'
        url_charts = f'{url_glob}/period_categories_charts?regionName={region}&start={start_date}&end={end_date}'

    return [url_total, url_charts]


def main():
    print(f'[!] Парсинг {Fore.YELLOW + "Тинькофф Индекса" + Style.RESET_ALL} от СОД ЭУ ГУ ЦБ РФ по ЦФО:')
    try:
        file_name_c = f'Tinkoff_Index_Customers_2024_{date.today().year}.xlsx'

        combined_df_customers = pd.DataFrame()

        for region, i in zip(regs, range(len(regs))):
            URLs = URL_form(region=region, iteration=i, start_date='01.2024', end_date=checkpoint)
            df_consumer = pars_consumer(region_name=region,
                                        request_total=requests.get(url=URLs[0]).json(),
                                        request_charts=requests.get(url=URLs[1]).json(),
                                        dict_types=consumer_types,
                                        curve_date=['2022-03-02', '2023-03-02', '2024-03-02'])
            combined_df_customers = pd.concat(([combined_df_customers, df_consumer]))

        old_file_killer(file_name=file_name_c)

        with pd.ExcelWriter(path=file_name_c, engine='xlsxwriter') as writer:
            combined_df_customers.to_excel(writer, sheet_name='Tinkoff_Index_Customers', index=False)

        df_customers = pd.concat([pd.read_excel(f'{path_to_archive}\Tinkoff_Index_Customers_2020_2023.xlsx'), combined_df_customers])
        df_customers = df_customers.loc[df_customers['Регион'].isin(regions)].sort_values(by=['Регион', 'Дата'])
        df_customers['Дата'] = pd.to_datetime(df_customers['Дата'], format='%Y-%m-%d')
        df_customers = df_customers.groupby(['Регион', df_customers['Дата'].dt.to_period('M')]).mean(numeric_only=True).reset_index()
        df_customers['Дата'] = df_customers['Дата'].dt.to_timestamp().dt.strftime('%d.%m.%Y')

        print('[!] Обороты бизнеса:')

        file_name_b = f'Tinkoff_Index_Business_2024_{date.today().year}.xlsx'

        combined_df_business = pd.DataFrame()

        for region, i in zip(regs, range(len(regs))):
            URLs = URL_form(region=region, iteration=i, start_date='01.2024', end_date=checkpoint)

            df_business = pars_business(region_name=region,
                                        request_total=requests.get(url=URLs[0]).json(),
                                        request_charts=requests.get(url=URLs[1]).json(),
                                        dict_types=business_types)
            combined_df_business = pd.concat(([combined_df_business, df_business]))

        old_file_killer(file_name=file_name_b)

        with pd.ExcelWriter(path=file_name_b, engine='xlsxwriter') as writer:
            combined_df_business.to_excel(writer, sheet_name='Tinkoff_Index_Business', index=False)

        df_business = pd.concat([pd.read_excel(f'{path_to_archive}\Tinkoff_Index_Business_2020_2023.xlsx'), combined_df_business])
        df_business = df_business.loc[df_business['Регион'].isin(regions)].sort_values(by=['Регион', 'Дата'])
        df_business['Дата'] = pd.to_datetime(df_business['Дата'], format='%Y-%m-%d')
        df_business = df_business.groupby(['Регион', df_business['Дата'].dt.to_period('M')]).mean(numeric_only=True).reset_index()
        df_business['Дата'] = df_business['Дата'].dt.to_timestamp().dt.strftime('%d.%m.%Y')

        print('\n[!] Среднемесячные значения')

        with pd.ExcelWriter('Tinkoff_Index_monthly_averages.xlsx') as writer:
            df_business.to_excel(writer, sheet_name='Tinkoff_Index_Business', index=False)
            df_customers.to_excel(writer, sheet_name='Tinkoff_Index_Customers', index=False)

        print('\n[!] Процесс завершен!')
    except Exception as e:
        print(f'[-] {Fore.RED + f"{e}" + Style.RESET_ALL}')


if __name__ == '__main__':
    main()
