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


def print_DataFrame_info(df, txt2='*', num=30):
    print_txt('DataFrame', txt2, num, is_first=True)
    print(df)

    print_txt('index', txt2, num, is_first=False)
    print(df.index)

    print_txt('columns', txt2, num, is_first=False)
    print(df.columns)

    print_txt('shape', txt2, num, is_first=False)
    print(df.shape)
