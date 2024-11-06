import os
import sqlite3
import pandas as pd
import numpy as np
import re
from datetime import datetime
from sqlalchemy import create_engine

from .models import ReportRuskVolumeCheck, ReportSued16010, ReportSued7108

from env import database

time_check_base = {}


def transfer_files_to_model(model, path, period):
    check_time(transfer_files_to_model.__name__)
    # df_check = transfer_files_to_df(path_prod, True)
    # check_source_files(df_check, model_prod)
    df = transfer_files_to_df(path)

    column_names_in_model = []
    for el in model._meta.fields[1:]:
        column_names_in_model.append(el.verbose_name)
        if el.verbose_name not in list(df):
            df[el.verbose_name] = None

    for el in list(df):
        if el not in column_names_in_model:
            f"В модели {model} отсутствует столбец {el}"

    transfer_df_to_db_table(df, 'sqlite:///db.sqlite3', model._meta.db_table + '_temp')
    transfer_db_table_to_model(model, period)
    delete_db_table(model._meta.db_table + '_temp')
    check_time(transfer_files_to_model.__name__)
    print('\n')


def check_source_files(df, model):
    check_time(check_source_files.__name__)

    column_names_in_model = {}
    for el in model._meta.fields:
        column_names_in_model[el.name] = el.verbose_name

    for a in list(column_names_in_model.values())[1:]:
        c = False
        for b in list(df):
            if a == b:
                c = True
        if not c:
            check_time(check_source_files.__name__)
            return print("Error: в исходных файлах нет параметра", a)

    check_time(check_source_files.__name__)
    return print("Проверка исходных файлов пройдена")


def transfer_files_to_df(path, check=False):
    """

    :param check:
    :param path:
    :type path: str
    :return: DataFrame
    """
    check_time(transfer_files_to_df.__name__)

    def transfer_excel_to_df(path_excel, skip_rows_excel, skip_footer_excel, sheet_name_excel=0):
        """

        :param skip_footer_excel:
        :param path_excel:
        :param skip_rows_excel:
        :param sheet_name_excel:
        :type sheet_name_excel: str
        :return:
        """
        for root_excel, dirs_excel, files_excel in os.walk(path_excel):
            df_main = pd.DataFrame()
            for filename in files_excel:
                if filename[:2] != "~$":
                    if filename.split('.')[-1] in ['xls', 'xlsx', 'xlsm', 'xlsb', 'odf', 'ods']:
                        df_temp = pd.read_excel(root_excel + "\\" + filename, sheet_name=sheet_name_excel,
                                                skiprows=skip_rows_excel, skipfooter=skip_footer_excel, nrows=rows)
                        df_temp['ОСП (определенный)'] = define_subdivision(filename)

                        df_temp['Расчетный период (определенный)'] = re.findall(r'(\d{4}-\d{2})', root_excel)[0] + '-01'
                        df_main = pd.concat([df_main, df_temp], ignore_index=True)
            return df_main

    def transfer_csv_to_df(path_csv):
        df_main = pd.DataFrame()
        for root_csv, dirs_csv, files_csv in os.walk(path_csv):
            for filename in files_csv:
                if filename[:2] != "~$":
                    if filename.split('.')[-1] in ['csv']:
                        df_temp = pd.read_csv(filepath_or_buffer=root_csv + "\\" + filename, sep=';',
                                               encoding='Windows-1251', header=None, low_memory=False) # encoding='Windows-1251',

                        df_temp.fillna(value='', inplace=True)

                        index_frame = df_temp.loc[df_temp[0] == '1.'].index.values[0] - 1

                        for index_frame_el in range(index_frame, index_frame + 1):
                            default = ''
                            for el in range(0, len(df_temp.columns)):
                                if df_temp.iloc[index_frame_el, el] == '':
                                    df_temp.iloc[index_frame_el, el] = default
                                else:
                                    default = df_temp.iloc[index_frame_el, el]

                        for el in range(0, len(df_temp.columns)):
                            df_temp.iloc[0, el] = ''
                        for el in range(0, len(df_temp.columns)):
                            for index_frame_el in range(index_frame, index_frame + 5):
                                if df_temp.iloc[index_frame_el, el] != '':
                                    if df_temp.iloc[0, el] == '':
                                        df_temp.iloc[0, el] = df_temp.iloc[index_frame_el, el]
                                    else:
                                        df_temp.iloc[0, el] = (df_temp.iloc[0, el] + ' ' +
                                                               df_temp.iloc[index_frame_el, el])

                        df_temp.columns = df_temp.iloc[0]

                        for el in range(0, index_frame+5):
                            df_temp.drop(labels=[el], axis=0, inplace=True)

                        df_temp['ОСП (определенный)'] = define_subdivision(filename)
                        df_temp['Расчетный период (определенный)'] = re.findall(r'(\d{4}-\d{2})', root_csv)[0] + '-01'
                        df_main = pd.concat([df_main, df_temp], ignore_index=True)
        df_main.reset_index()
        return df_main

    if check:
        rows = 1
    else:
        rows = None

    df = pd.DataFrame()
    if "Сверка ПО" in path:
        df = transfer_excel_to_df(path, 2, 0, "Сверка ПО")

    if "71_08" in path:
        df = transfer_csv_to_df(path)
        print(list(df))
        try:
            df.rename(columns={' 3.1 10 значный номер лицевого счета':
                                   '3.1. 10 значный номер лицевого счета',
                               'Отгружено "Д"\xa0 20. кВт.ч (ст.22.1+ст.23.1+ст.24.1+ст.25.1) кВтч.':
                                   'Отгружено \"Д\" 20. кВт.ч (ст.22.1+ст.23.1+ст.24.1+ст.25.1) кВтч.'},
                      inplace=True)
            print(list(df))

        finally:
            pass

        try:
            df['3.1. 10 значный номер лицевого счета'] = df['3.1. 10 значный номер лицевого счета'].str.replace("'", "")
        finally:
            pass




    if "160_10" in path:
        df = transfer_excel_to_df(path, [0, 2], 4, "Расчет объемов на общед в МКЖД")

    df = df.replace(np.nan, None)

    check_time(transfer_files_to_df.__name__)
    return df


def transfer_df_to_db_table(df, db, db_table):
    check_time(transfer_df_to_db_table.__name__)

    engine = create_engine(db, echo=False)

    with engine.begin() as connection:
        df.to_sql(name=db_table, con=connection, if_exists='append', index=False)

    print(df)
    check_time(transfer_df_to_db_table.__name__)
    return


def transfer_db_table_to_model(model, period):
    check_time(transfer_db_table_to_model.__name__)

    connection = None
    try:
        connection = sqlite3.connect(database.NAME)
        cursor = connection.cursor()

        sql_query_result = ("DELETE FROM" + " `" + model._meta.db_table + "` " + "WHERE `Define_period`='" +
                            period + "-01';")
        # print(sql_query_result)
        try:
            cursor.execute(sql_query_result)
        except sqlite3.DatabaseError as error:
            print("Error: ", error)
        else:
            connection.commit()

        column_names_in_model = {}
        for el in model._meta.fields:
            column_names_in_model[el.name] = el.verbose_name

        sql_query_1 = ""
        sql_query_2 = ""
        for column_name in list(column_names_in_model)[1:]:
            sql_query_1 += " `" + column_name + "`,"
            sql_query_2 += " `" + column_names_in_model[column_name] + "` AS `" + column_name + "`,"
        sql_query_1 = sql_query_1[1:-1]
        sql_query_2 = sql_query_2[1:-1]

        sql_query_result = ("INSERT or REPLACE INTO `" + model._meta.db_table + "` (" + sql_query_1 + " ) " +
                            "SELECT " + sql_query_2 + " " +
                            "FROM `" + model._meta.db_table + "_temp`;\n")
        # print(sql_query_result)
        try:
            cursor.execute(sql_query_result)
        except sqlite3.DatabaseError as error:
            print("Error: ", error)
        else:
            connection.commit()

        cursor.close()
    except sqlite3.Error as error:
        print(error)
    finally:
        if connection:
            connection.close()

    check_time(transfer_db_table_to_model.__name__)


def delete_db_table(db_table):
    check_time(delete_db_table.__name__)

    sqlite_connection = None
    try:
        sqlite_connection = sqlite3.connect(database.NAME)
        cursor = sqlite_connection.cursor()
        sql_delete_query = f"DROP TABLE {db_table}"
        cursor.execute(sql_delete_query)
        sqlite_connection.commit()
        cursor.close()

    except sqlite3.Error as error:
        print(error)
    finally:
        if sqlite_connection:
            sqlite_connection.close()

    check_time(delete_db_table.__name__)


def check_time(function_name):
    global time_check_base

    try:
        time_check_base[function_name]
    except KeyError:
        time_check_base[function_name] = dict.fromkeys(['stopwatch_index', 'start'])
        time_check_base[function_name]['stopwatch_index'] = 0

    if time_check_base[function_name]['stopwatch_index'] == 0:
        time_check_base[function_name]['stopwatch_index'] = 1
        time_check_base[function_name]['start'] = datetime.now()
    else:
        time_check_base[function_name]['stopwatch_index'] = 0
        return print(function_name, datetime.now() - time_check_base[function_name]['start'])


def define_subdivision(text):
    if "белок" in text.lower():
        return "Белокурихинское"
    elif "бийск" in text.lower():
        return "Бийское"
    elif "горн" in text.lower():
        return "Горно-Алтайский"
    elif "зме" in text.lower():
        return "Змеиногорское"
    elif "кам" in text.lower():
        return "Каменское"
    elif "кул" in text.lower():
        return "Кулундинское"
    elif "ново" in text.lower():
        return "Новоалтайское"
    elif "руб" in text.lower():
        return "Рубцовское"
    elif "центр" in text.lower():
        return "Центральное"
    else:
        return ""


def define_period(variation):
    now = datetime.now()

    if now.day > 9:
        month_report = str(now.month)
        year_report = str(now.year)
    else:
        if now.month == 1:
            month_report = '12'
            year_report = str(now.year - 1)
        else:
            month_report = str(now.month - 1)
            year_report = str(now.year)

    if len(month_report) == 1:
        month_report = '0' + month_report

    if variation == 'year-month':
        return year_report + '-' + month_report

    if variation == 'year':
        return year_report

    if variation == 'month':
        return month_report


# years = ['2024']
# months = ['07']
# for year in years:
#     for month in months:
#         print('start: ', year, month)
#         period = f'{year}-{month}'
#         path = f'D:/Алтайэнергосбыт/ПО/{period}/_asuse/Сверка ПО'
#         transfer_files_to_model(ReportRuskVolumeCheck, path, period)
#         print('stop: ', year, month)