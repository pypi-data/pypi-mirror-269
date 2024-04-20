import pandas as pd


def data1():
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


def data2():
    # 定义行索引
    index = ['01', '02', '03']

    # 定义多级列索引
    columns = [
        ('var1', 'before', 2),
        ('var1', 'before', 1),
        ('var1', 'post', 1),
        ('var1', 'post', 2),
        ('var2', 'before', 2),
        ('var2', 'before', 1),
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
