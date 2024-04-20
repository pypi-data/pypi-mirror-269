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
