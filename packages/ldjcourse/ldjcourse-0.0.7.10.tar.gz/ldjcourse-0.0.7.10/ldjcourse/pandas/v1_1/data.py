import pandas as pd


def data1():
    # 定义行索引
    index = ['01', '02', '03', '04']

    # 定义列索引
    columns = ['var1', 'var2', 'var3', 'var4', 'var5', 'var6', 'var7', 'var8']

    # 定义数据
    data = [
        [11, 21, 31, 41, 51, 61, 71, 81],
        [12, 22, 32, 42, 52, 62, 72, 82],
        [13, 23, 33, 43, 53, 63, 73, 83],
        [14, 24, 34, 44, 54, 64, 74, 84],
    ]

    # 创建 DataFrame
    df = pd.DataFrame(data, index=index, columns=columns)
    return df


def data2():
    # 定义行索引
    index = ['01', '02', '03']

    # 定义多级列索引
    columns = [
        ('var1', 'before'),
        ('var1', 'post'),
        ('var2', 'before'),
        ('var2', 'post'),
    ]
    names = ['var', 'stage']
    columns = pd.MultiIndex.from_tuples(columns, names=names)

    # 定义数据
    data = [
        [11, 21, 31, 41],
        [12, 22, 32, 42],
        [13, 23, 33, 43],
    ]

    # 创建 DataFrame
    df = pd.DataFrame(data, index=index, columns=columns)
    return df


def data3():
    # 定义行索引
    index = ['01', '02', '03']

    # 定义多级列索引
    columns = [
        ('var1', 'before', 1),
        ('var1', 'before', 2),
        ('var1', 'post', 1),
        ('var1', 'post', 2),
        ('var2', 'before', 1),
        ('var2', 'before', 2),
        ('var2', 'post', 1),
        ('var2', 'post', 2),
    ]
    names = ['var', 'stage1', 'stage2']
    columns = pd.MultiIndex.from_tuples(columns, names=names)

    # 定义数据
    data = [
        [11, 21, 31, 41, 51, 61, 71, 81],
        [12, 22, 32, 42, 52, 62, 72, 82],
        [13, 23, 33, 43, 53, 63, 73, 83],
    ]

    # 创建 DataFrame
    df = pd.DataFrame(data, index=index, columns=columns)
    return df


def data4(type=0):
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


def data5():
    # 定义多级行索引
    index = [
        ('01', 2023),
        ('01', 2024),
        ('02', 2023),
        ('02', 2024),
        ('03', 2023),
        ('03', 2024),
    ]
    names = ['id', 'year']
    index = pd.MultiIndex.from_tuples(index, names=names)

    # 定义多级列索引
    columns = ['var1', 'var2', 'var3']

    # 定义数据
    data = [
        [11, 21, 31],
        [12, 22, 32],
        [13, 23, 33],
        [14, 24, 34],
        [15, 25, 35],
        [16, 26, 36],
    ]

    # 创建 DataFrame
    df = pd.DataFrame(data, index=index, columns=columns)
    return df


def data6():
    # 定义多级行索引
    index = [
        ('01', 'A', 2023),
        ('01', 'A', 2024),
        ('01', 'B', 2023),
        ('01', 'B', 2024),
        ('02', 'A', 2023),
        ('02', 'A', 2024),
        ('02', 'B', 2023),
        ('02', 'B', 2024),
    ]
    names = ['id', 'area', 'year']
    index = pd.MultiIndex.from_tuples(index, names=names)

    # 定义多级列索引
    columns = ['var1', 'var2', 'var3']

    # 定义数据
    data = [
        [11, 21, 31],
        [12, 22, 32],
        [13, 23, 33],
        [14, 24, 34],
        [15, 25, 35],
        [16, 26, 36],
        [17, 27, 37],
        [18, 28, 38],
    ]

    # 创建 DataFrame
    df = pd.DataFrame(data, index=index, columns=columns)
    return df
