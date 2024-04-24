# -*- coding: utf-8 -*-
import csv
import json
import os
import pickle

import pandas as pd


def read_csv_file(file_path, file_name):
    """讀取csv檔案"""
    file = "{}/{}".format(file_path, file_name)
    with open(file, newline=os.linesep) as stream:
        content = csv.reader(stream)
        result = [row for row in content]
    return result


def read_json_file(file_path, file_name):
    """讀取json檔案"""
    file = "{}/{}".format(file_path, file_name)
    with open(file) as stream:
        content = json.load(stream)
    return content


def read_excel_file(file_path, file_name):
    """讀取excel檔案"""
    file = "{}/{}".format(file_path, file_name)
    xlsx = pd.ExcelFile(file)
    result_dict = {}
    for sheet in xlsx.sheet_names:
        datas = result_dict.get(sheet)
        if not datas:
            datas = []
            result_dict.setdefault(sheet, datas)
        # read rows
        df = xlsx.parse(sheet)
        for x in df.index:
            d = []
            for y in df.columns:
                d.append(df.iloc[x][y])
            datas.append(d)
    return result_dict


def save_pickle_file(file_path, file_name, data):
    """存入pickle檔案"""
    if not os.path.exists(file_path):
        os.makedirs(file_path)
    file = "{}/{}".format(file_path, file_name)
    with open(file, 'wb') as fp:
        pickle.dump(data, fp, protocol=4)


def load_pickle_file(file_path, file_name):
    """讀取pickle檔案"""
    file = "{}/{}".format(file_path, file_name)
    if not os.path.exists(file):
        raise FileNotFoundError
    with open(file, 'rb') as fp:
        dataset = pickle.load(fp)
    return dataset
