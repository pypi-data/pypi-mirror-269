from . import data as _data


def get_data(data_name, *args, **kwargs):
    obj = getattr(_data, data_name)
    result = obj(*args, **kwargs)
    return result


def print_txt(txt1, txt2='*', num=30):
    print('\n')
    print('{}'.format(txt2) * num)
    print('{}:'.format(txt1))
