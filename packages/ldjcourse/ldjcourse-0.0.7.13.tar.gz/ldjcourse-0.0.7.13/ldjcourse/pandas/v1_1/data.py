import pandas as pd


def _pure_data1():
    data = [
        range(11, 91 + 1, 10),
        range(12, 92 + 1, 10),
        range(13, 93 + 1, 10),
        range(14, 94 + 1, 10),
        range(15, 95 + 1, 10),
        range(16, 96 + 1, 10),
        range(17, 97 + 1, 10),
        range(18, 98 + 1, 10),
        range(19, 99 + 1, 10),
    ]
    return data


def data1():
    # 定义行索引
    index = ['0{}'.format(i) for i in range(1, 10)]
    index = pd.Index(index, name='id')

    # 定义列索引
    columns = ['var{}'.format(i) for i in range(1, 10)]
    columns = pd.Index(columns, name='var')

    # 定义数据
    data = _pure_data1()

    # 创建 DataFrame
    df = pd.DataFrame(data, index=index, columns=columns)
    return df


def data2():
    # 定义行索引
    index = ['0{}'.format(i) for i in range(1, 10)]
    index = pd.Index(index, name='id')

    # 定义列索引
    columns = [
        ('var1', 'A'),
        ('var1', 'B'),
        ('var1', 'C'),
        ('var1', 'D'),
        ('var1', 'E'),
        ('var2', 'A'),
        ('var2', 'B'),
        ('var2', 'C'),
        ('var2', 'D'),
    ]
    names = ['var', 'area']
    columns = pd.MultiIndex.from_tuples(columns, names=names)

    # 定义数据
    data = _pure_data1()

    # 创建 DataFrame
    df = pd.DataFrame(data, index=index, columns=columns)
    return df


def data3():
    # 定义行索引
    index = ['0{}'.format(i) for i in range(1, 10)]
    index = pd.Index(index, name='id')

    # 定义列索引
    columns = [
        ('var1', 'A', 2023),
        ('var1', 'A', 2024),
        ('var1', 'B', 2023),
        ('var1', 'B', 2024),
        ('var1', 'C', 2023),
        ('var1', 'C', 2024),
        ('var2', 'A', 2024),
        ('var2', 'B', 2024),
        ('var2', 'C', 2024),
    ]
    names = ['var', 'area', 'year']
    columns = pd.MultiIndex.from_tuples(columns, names=names)

    # 定义数据
    data = _pure_data1()

    # 创建 DataFrame
    df = pd.DataFrame(data, index=index, columns=columns)
    return df


def data4():
    # 定义行索引
    index = [
        ('01', 'A', 2023),
        ('01', 'A', 2024),
        ('01', 'B', 2023),
        ('01', 'B', 2024),
        ('01', 'C', 2023),
        ('01', 'C', 2024),
        ('02', 'A', 2024),
        ('02', 'B', 2024),
        ('02', 'C', 2024),
    ]
    names = ['id', 'area', 'year']
    index = pd.MultiIndex.from_tuples(index, names=names)

    # 定义列索引
    columns = ['var{}'.format(i) for i in range(1, 10)]
    columns = pd.Index(columns, name='var')

    # 定义数据
    data = _pure_data1()

    # 创建 DataFrame
    df = pd.DataFrame(data, index=index, columns=columns)
    return df


def data5():
    # 定义行索引
    index = [
        ('01', 'A', 2023),
        ('01', 'A', 2024),
        ('01', 'B', 2023),
        ('01', 'B', 2024),
        ('01', 'C', 2023),
        ('01', 'C', 2024),
        ('02', 'A', 2024),
        ('02', 'B', 2024),
        ('02', 'C', 2024),
    ]
    names = ['id', 'area', 'year']
    index = pd.MultiIndex.from_tuples(index, names=names)

    # 定义列索引
    columns = ['var{}'.format(i) for i in range(1, 10)]
    columns = pd.Index(columns, name='var')

    # 定义数据
    data = _pure_data1()

    # 创建 DataFrame
    df = pd.DataFrame(data, index=index, columns=columns)
    return df


def data9(type=0):
    df = data3()
    df = df.copy()

    columns = list(df.columns)
    if type == 0:
        columns[3] = ('var1', 'post', 1)
    elif type == 1:
        columns[3] = ('var1', 'post', '')

    df.columns = pd.MultiIndex.from_tuples(columns, names=df.columns.names)
    df.sort_index(axis=1, inplace=True)
    return df
