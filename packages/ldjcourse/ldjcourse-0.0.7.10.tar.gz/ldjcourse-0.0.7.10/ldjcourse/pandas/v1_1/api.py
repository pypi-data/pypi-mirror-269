import pandas as pd

from . import data as _data


def get_data(data_name, *args, **kwargs):
    obj = getattr(_data, data_name)
    result = obj(*args, **kwargs)
    return result


def print_txt(txt1, txt2='*', num=30, is_first=False):
    if not is_first:
        print('\n')
    print('{}'.format(txt2) * num)
    print('{}:'.format(txt1))


def print_info(data, txt2='*', num=30):
    if isinstance(data, pd.DataFrame):
        print_txt('DataFrame', txt2, num, is_first=True)
        print(data)

        print_txt('index', txt2, num, is_first=False)
        print(data.index)

        print_txt('columns', txt2, num, is_first=False)
        print(data.columns)

        print_txt('shape', txt2, num, is_first=False)
        print(data.shape)
    elif isinstance(data, pd.Series):
        print_txt('Series', txt2, num, is_first=True)
        print(data)

        print_txt('index', txt2, num, is_first=False)
        print(data.index)

        print_txt('name', txt2, num, is_first=False)
        print(data.name)

        print_txt('shape', txt2, num, is_first=False)
        print(data.shape)
