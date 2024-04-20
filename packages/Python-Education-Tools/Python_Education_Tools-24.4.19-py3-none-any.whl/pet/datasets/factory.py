import datetime,os,re,shutil
from importlib.abc import Traversable
from importlib.resources import files
from pathlib import Path
from random import choices, randrange, random,choice
from subprocess import check_output

import numpy as np
import pandas as pd

# 创建用户使用本案例的工作目录
pet_home = Path.home() / 'pet_home'
pet_home.mkdir(parents=True, exist_ok=True)
pet_desktop = Path.home() / 'Desktop/Python与数据分析及可视化教学案例'


def download_textbook1(dst=pet_desktop):
    """
    将教学案例拷贝到用户桌面
    :param dst: 拷贝文件的目标目录，默认是用户桌面
    :return:
    """
    src: Traversable = files('pet.textbook1')
    print('Copying,please wait....')
    shutil.copytree(str(src), dst, dirs_exist_ok=True)
    print('done!!')
    os.startfile(dst)


def gen_iid(init=240151000, number=40):
    """ 生成从init起始的一批学号
    init:起始学号：整数值 ，建议大于4位，首位不要为零
    number:元素个数
    """
    if not isinstance(init, int): init=240151000
    return pd.Series(data=range(init, init + number))


def gen_name(xm=None, number=40):
    """ 生成姓名， 生成虚假的名字（长度2~3个中文）
    xm=['姓字符串','名字字符串],若传入的是空字符串"",则生成默认姓名
    根据姓，名，生成n个假名字
    number: 要生成元素个数
    """
    if not isinstance(xm, (list, tuple)):
        x=['赵', '钱', '孙', '李', '周', '吴', '郑', '王', '冯', '陈', '褚', '卫', '蒋', '沈', '韩', '杨', '朱', '秦', '尤', '许', '何', '吕', '施', '张', '孔', '曹', '严', '华', '金', '魏', '陶', '姜', '戚', '谢', '邹', '喻', '柏', '水', '窦', '章', '云', '苏', '潘', '葛', '奚', '范', '彭', '郎', '鲁', '韦', '昌', '马', '苗', '凤', '花', '方', '俞', '任', '袁', '柳', '酆', '鲍', '史', '唐', '费', '廉', '岑', '薛', '雷', '贺', '倪', '汤', '滕', '殷', '罗', '毕', '郝', '邬', '安', '常', '乐', '于', '时', '傅', '皮', '卞', '齐', '康', '伍', '余', '元', '卜', '顾', '孟', '平', '黄', '和', '穆', '萧', '尹', '姚', '邵', '湛', '汪', '祁', '毛', '禹', '狄', '米', '贝', '明', '臧', '计', '伏', '成', '戴', '谈', '宋', '茅', '庞', '熊', '纪', '舒', '屈', '项', '祝', '董', '梁', '杜', '阮', '蓝', '闵', '席', '季', '麻', '强', '贾', '路', '娄', '危', '江', '童', '颜', '郭', '梅', '盛', '林', '刁', '钟', '徐', '邱', '骆', '高', '夏', '蔡', '田', '樊', '胡', '凌', '霍', '虞', '万', '支', '柯', '昝', '管', '卢', '莫', '经', '房', '裘', '缪', '干', '解', '应', '宗', '丁', '宣', '贲', '邓', '郁', '单', '杭', '洪', '包', '诸', '左', '石', '崔', '吉', '钮', '龚', '程', '嵇', '邢', '滑', '裴', '陆', '荣', '翁', '荀', '羊', '於', '惠', '甄', '曲', '家', '封', '芮', '羿', '储', '靳', '汲', '邴', '糜', '松', '井', '段', '富', '巫', '乌', '焦', '巴', '弓', '牧', '隗', '山', '谷', '车', '侯', '宓', '蓬', '全', '郗', '班', '仰', '秋', '仲', '伊', '宫', '宁', '仇', '栾', '暴', '甘', '钭', '历', '戎', '祖', '武', '符', '刘', '景', '詹', '束', '龙', '叶', '幸', '司', '韶', '郜', '黎', '蓟', '溥', '印', '宿', '白', '怀', '蒲', '邰', '从', '鄂', '索', '咸', '籍', '赖', '卓', '蔺', '屠', '蒙', '池', '乔', '阳', '郁', '胥', '能', '苍', '双', '闻', '莘', '党', '翟', '谭', '贡', '劳', '逄', '姬', '申', '扶', '堵', '冉', '宰', '郦', '雍', '郤', '璩', '桑', '桂', '濮', '牛', '寿', '通', '边', '扈', '燕', '冀', '姓', '浦', '尚', '农', '温', '别', '庄', '晏', '柴', '瞿', '阎', '充', '慕', '连', '茹', '习', '宦', '艾', '鱼', '容', '向', '古', '易', '慎', '戈', '廖', '庾', '终', '暨', '居', '衡', '步', '都', '耿', '满', '弘', '匡', '国', '文', '寇', '广', '禄', '阙', '东', '欧', '殳', '沃', '利', '蔚', '越', '夔', '隆', '师', '巩', '厍', '聂', '晁', '勾', '敖', '融', '冷', '訾', '辛', '阚', '那', '简', '饶', '空', '曾', '毋', '沙', '乜', '养', '鞠', '须', '丰', '巢', '关', '蒯', '相', '查', '后', '荆', '红', '游', '竺', '权', '逮', '盍', '益', '桓', '公', '万俟', '司马', '上官', '欧阳', '夏侯', '诸葛', '闻人', '东方', '赫连', '皇甫', '尉迟', '公羊', '澹台', '公冶', '宗政', '濮阳', '淳于', '单于', '太叔', '申屠', '公孙', '仲孙', '轩辕', '令狐', '徐离', '宇文', '长孙', '慕容', '司徒', '司空']
        m=("群平风华正茂仁义礼智媛强章太极武当天霸红和丽平世莉冲婻少林寺界中华正义伟岸茂盛繁望"
           "印树枝松涛圆一懿贵妃彭桂花民波凰凤春卿玺波嬴政帝国荣智慧睿兴平风清扬思自成世民嬴旺"
           "品网红丽文天学与翔斌霸学花琪缺祥非常承诺保证施云北京漳州洛阳阴区次翔文蒙教学忠谋书")

        xm=[x,m]
    names = ["".join(choices(xm[0], k=1) + choices(xm[1], k=choice([1,2,2]))) for _ in range(number)]
    # 姓名， 姓，名字为1~2个字，2个字的概率为2/3
    return pd.Series(names)


def gen_int_series(int_range_lst=[0, 100], name='mark', number=40):
    """  生成整数随机series
       int_range_lst：[start，end]
        记录条数：number，默认40
        默认名称是：mark
        返回：series
    """
    if int_range_lst is not isinstance(int_range_lst, (list, tuple)):
        int_range_lst = [0, 100]
    low, high = int_range_lst
    return pd.Series(np.random.randint(low, high, number), name=name)


def gen_float_series(float_range_lst=[0, 100, 2], name='mark', number=40):
    """  生成浮点数 series
        float_range_lst：[start，end，length] ，length:小数点的位数
        记录条数：number 默认40
        返回：series
    """
    if float_range_lst is not isinstance(float_range_lst, (list, tuple)):
        float_range_lst = [0, 100, 2]


    low, high, length = float_range_lst
    out = map(lambda x: round(x, length), (np.random.rand(number) * (high - low) + low))
    return pd.Series(out, name=name)


def gen_date_time_series(period=['2020-2-24 00:00:00', '2022-12-31 00:00:00'], number=40, frmt="%Y-%m-%d %H:%M:%S"):
    """
    print(gen_date_time_series('2022-1-01 07:00:00', '2020-11-01 09:00:00', 10))
    随机生成某一时间段内的日期,时刻：
    :param period:
    :param number: 记录数
    :param frmt: 格式
    :return: series
    """
    if period is not isinstance(period, (list, tuple)):
        period = ['2020-2-24 00:00:00', '2022-12-31 00:00:00']
    start, end = period
    stime = datetime.datetime.strptime(start, frmt)
    etime = datetime.datetime.strptime(end, frmt)
    time_datetime = [random() * (etime - stime) + stime for _ in range(number)]
    time_str = [t.strftime(frmt) for t in time_datetime]
    return pd.Series(time_str)


def gen_date_series(date_period=['2020-2-24', '2024-12-31'], number=40):
    """
    随机生成某一时间段内的日期：
    print(gen_date_time_series('2022-1-01', '2020-11-01', 10))
     :param date_period:
    :param number: 记录数
    :return: series
    """
    if date_period is not isinstance(date_period, (list, tuple)):
        date_period = ['2020-2-24', '2024-12-31']

    return gen_date_time_series(date_period, number, frmt="%Y-%m-%d")


def gen_time_series(time_period=['00:00:00', '23:59:59'], number=40):
    """
    随机生成某一时间段内的时刻：
    print(gen_time_series('07:00:00', '12:00:00', 10))
     :param time_period:
    :param number: 记录数
    :return: series
    """
    if time_period is  not isinstance(time_period, (list, tuple)):
        time_period = ['00:00:00', '23:59:59']
    return gen_date_time_series(time_period, number, frmt="%H:%M:%S")


def gen_category_series(lst, number=40):
    """  生成category数据 series
        lst:可选数据列表
        记录条数：number

    """

    return pd.Series(np.random.choice(lst, size=number))


'''
对上述函数做简化名称，目的为了选择解析模板数据后调用函数名称。自动实现一一对应。
'''

func_dict = {
    'iid': gen_iid,
    'n': gen_name,
    'i': gen_int_series,
    'f': gen_float_series,
    'd': gen_date_series,
    't': gen_time_series,
    'dt': gen_date_time_series,
    'c': gen_category_series

}

sample_order = {

    '学号.iid': 220151000,
    '考号.i': [151000, 789000],
    '姓名.n': '',  # ""生成默认的随机名字，也可以设置姓名字符串，['赵钱孙李','微甜地平天下'],
    '性别.c': ['男', '女'],
    '报名时间.d': ['2016-1-1', '2022-12-31'],
    '录入时间.t': ['00:00:00', '23:59:59'],
    '年龄.i': [18, 34],
    '政治面貌.c': ['中共', '群众', '民革', '九三'],
    '专业.c': ['计算机科学与技术', '人工智能', '软件工程', '自动控制', '机械制造', '自动控制'],
    '学校.c': ['清华大学', '北京大学', '复旦大学', '上海交通大学', '华东理工大学', '中山大学', '上海师范大学',
               '中国科技大学', '上海大学'],
    '政治成绩.i': [36, 100],
    '英语成绩.i': [29, 100],
    '英语类别.c': ['英语一', '英语二'],
    '数学成绩.i': (40, 150),
    '数学类别.c': ['数学一', '数学二', '数学三'],
    '专业课成绩.i': [55, 150],
    '六级证书.c': ['是', '否'],
    '在线时长.f': (1000.3, 9999.55, 2)
}


def add_noise(df, noise=0.1, repeat=2) -> pd.DataFrame:
    """
    对 DataFrame加入噪声，非法数据
    noise：默认0.1 指每列数据为空的概率
    repeat： 出现重复数据的最大次数
    :param repeat:
    :param noise:
    :param df:
    :return:
    """
    scope_n = int(df.shape[0] * df.shape[1])
    noise_n = int(scope_n * noise)
    df = pd.concat([df] * repeat)
    df = df.sample(frac=1 / repeat).reset_index(drop=True)

    for i in df.columns:
        df[i] = df[i].apply(lambda x: None if np.random.randint(1, scope_n) in range(noise_n) else x)

    return df


def generator(order: dict = sample_order,
              number: int = 40,
              dst: str = f'{pet_home}/generated_dataset_{datetime.datetime.now().strftime("%Y-%m-%d %H-%M-%S")}.xlsx',
              noise: float = 0,
              repeat: int = 1):
    """
    根据订单生成数据
    :param repeat:
    :param noise:
    :param dst:
    :param order: 订单字典
    :param number: 数据元素个数
    :return:

    """
    df = pd.DataFrame()
    for k, v in order.items():
        na, func = k.split('.')
        # df[na] = eval(func)(v, number=number)
        df[na] = func_dict[func](v, number=number)
    if noise > 0.0:
        df = add_noise(df, noise=noise, repeat=repeat)
    df.to_excel(dst, index=None)
    print(f'Dataset is generated in {dst} ！！！')

    return df


def gen_sample_series(number: int = 40,
                      dst=f'{pet_home}/generated_sample_series_{datetime.datetime.now().strftime("%Y-%m-%d %H-%M-%S")}.xlsx',
                      noise=0,
                      repeat=1):
    order = {
        '姓名.n': '',  # ""生成默认的随机名字，也可以设置姓名字符串，['赵钱孙李','微甜地平天下'],
        '成绩.i': ''
    }
    df = generator(order, number, dst)
    df = pd.concat([df] * repeat)
    df = df.sample(frac=1 / repeat).reset_index(drop=True)

    df.set_index(df['姓名'], inplace=True)
    df['成绩'] = df['成绩'].apply(lambda x: None if np.random.randint(1, len(df)) in range(int(noise * len(df))) else x)

    return df['成绩']


def gen_sample_dataframe(sample_order=sample_order,
                         number: int = 40,
                         dst=f'{pet_home}/generated_sample_dataframe_{datetime.datetime.now().strftime("%Y-%m-%d %H-%M-%S")}.xlsx',
                         noise=0,
                         repeat=1):
    print('*' * number)
    from pprint import pprint
    print('订单格式：')
    pprint(sample_order)
    print("*" * number)
    os.startfile(pet_home)
    return generator(order=sample_order, number=number, dst=dst, noise=noise, repeat=repeat)


def gen_sample_dataframe_12():
    sample_order = {

        '考号.iid': 220151000,
        '姓名.n': '',  # ""生成默认的随机名字，也可以设置姓名字符串，['赵钱孙李','微甜地平天下'],
        '性别.c': ['男', '女'],
        '学校.c': ['清华大学', '北京大学', '复旦大学', '上海交通大学', '华东理工大学', '中山大学', '上海师范大学',
                   '中国科技大学', '上海大学'],
        '英语.i': [29, 100],
        '政治.i': [36, 100],
        '线代.i': [20, 100],
        '高数.i': [15, 150],
        '专业课.i': [39, 150],
        '表达能力.i': [49, 150],
        '面试.i': [29, 150]
    }
    return gen_sample_dataframe(sample_order=sample_order)


def show_order_sample():
    # 打印样本订单
    from pprint import pprint
    pprint(sample_order)


# 提供的数据集
datafile_dict = {
    '中国大学': 'China_universities .xlsx',
    '学科专业分类': 'Edu_subjects.xlsx',
    '2023年世界高校QS前200位':'2023QS.xlsx',
    '上海师范大学教务处认定学科竞赛目录': '2023xkjs.xlsx',
    '2023-2024-1上海师范大学课程表': '2023-2024-1.xlsx',
    '2022年上海师范大学通识课': '2022tsk.xlsx',
    '2022年上海师范大学优秀毕业论文': '2022pst.xlsx',
    '2022年上海师范大学转专业-报名名单': '2022zzy.xlsx',
    '2023年上海师范大学转专业-报名名单': '2023zzy.xlsx',
    '2023年上海师范大学转专业-录取名单': '2023zzy-ok.xlsx',
    '2019年研究生初试成绩': 'st.xlsx',

    '上海地铁线路': 'shanghai-subway.xlsx',
    '北京公交车': 'beijing_bus.xlsx',
    '北京地铁线路': 'beijing-subway.xlsx',
    'ip地址分类': 'ip_address.xlsx',
    '双色球': 'ssq_22134.xlsx',
    '2023上海市二级程序员大赛名单': '20231118-players.xlsx',
    '八卦卦象': 'bg.xlsx',
    '六十四卦象': '64gx.xlsx',
    'iris数据集': 'iris.xlsx',
    'titanic数据集': 'titanic.xlsx',

    'Python二级考试大纲.txt': '2023ejkg.txt',
    '道德经.txt': 'ddj.txt',
    '心经.txt': 'xj.txt',
    '三字经.txt': 'szj.txt',
    '太乙金华宗旨.txt': 'tyjhzz.txt',
    '重阳立教十五论.txt': 'cylj.txt',
    '荷塘月色.txt': 'htys.txt',
    'sample_cookies.txt': 'sample_cookies.txt',
    '微信接龙投票.txt': 'votes.txt'

}


def get_datasets_list():
    return datafile_dict.keys()


def load_data(key='道德经', prompt=True):
    # 默认提示 数据集可选项
    print(f'共有{len(datafile_dict)}个可选数据集:\n {list(get_datasets_list())}') if prompt else ''
    # 若找不到用户输入数据集名称，则默认把error.txt装载
    file_name = datafile_dict.get(key, "error.txt")
    data_file: Traversable = files('pet.datasets.database').joinpath(file_name)

    if file_name.split('.')[-1] == 'xlsx':
        return pd.read_excel(data_file)

    elif file_name.split('.')[-1] == 'txt':
        try:
            contents = open(data_file, encoding="UTF-8").read()  # .replace('\n', '')
        except Exception:
            contents = open(data_file, encoding="gbk").read()  # .replace('\n', '')
        return contents

    elif file_name.split('.')[-1] == 'csv':
        return pd.read_csv(data_file)

    else:
        print('目前仅支持 xlsx，txt，csv 文件类型')
        # f = files('pet.datasets.database.ddj.txt')
        return open(data_file, encoding="UTF-8").read()


def get_directory_info_dataframe(directory=Path.home(), dst=Path.home() / 'files_info.xlsx'):
    """
    将目录下的文件子目录转化为DataFrame表格
    :param directory: 目录名称
    :param dst: 保存为xlsx的文件路径
    :return:
    """
    from datetime import datetime
    p = Path(directory)
    data = [
        (i.name, i.is_file(), i.stat().st_size, datetime.fromtimestamp(i.stat().st_mtime).strftime("%Y-%m-%d %H:%M:%S"))
        for i in p.iterdir()]

    df = pd.DataFrame(data, columns=['文件名', '类型', '文件大小', '修改时间'])
    df.to_excel(dst, index=None)
    return df


import psutil
# 获取进程信息
def get_pid_memory_info_dataframe():
    """
     每个进程内存使用情况
    :return:
    """
    # 获取内存信息
    memory = psutil.virtual_memory()
    print(f'Total memory: {memory.total}, Available memory: {memory.available}')
    data = [(i.name(), i.pid, i.memory_info().rss, i.memory_info().vms) for i in psutil.process_iter()]
    return pd.DataFrame(data, columns=['进程名', 'pid', '物理内存', '虚拟内存'])


# read_count=0, write_count=0, read_bytes=0, write_bytes=0, other_count=0, other_bytes=0
def get_pid_network_info_dataframe():
    """
    获取当前PC上的进程网络数据
    :return: DataFrame
    """
    columns = ['进程名称', 'pid', '收到数据包', '发送数据包', '收到字节数', '发送字节', '其它包数', '其它字节']
    data = [(i.name(), i.pid, *i.io_counters()) for i in psutil.process_iter()]
    df = pd.DataFrame(data, columns=columns)
    print(df[:5])
    return df


def get_pid_info_dataframe():
    data = [i.as_dict() for i in psutil.process_iter()]
    return pd.DataFrame(data)


def get_nic_info_series():
    """

    :return: 返回当前计算机网卡，Series格式
    """
    cmd = 'netsh trace show interfaces'
    get_results = lambda cmd, res: re.findall(res, check_output(cmd, universal_newlines=True))

    return pd.Series(get_results(cmd, '描述:\s+(.+)'))


def get_local_packages_info_dataframe():
    import importlib_metadata
    # 获取已安装的模块列表
    installed_packages = importlib_metadata.distributions()
    pkg = [(package.metadata['Name'],
            package.version,

            package.metadata.get('Author', 'N/A'),
            package.metadata.get('Summary', 'N/A'),
            package.files,
            package.locate_file(package.metadata['Name'])) for package in installed_packages]

    return pd.DataFrame(pkg, columns=['Package', 'Version', 'Author', 'Description', 'files', 'Location'])


def get_wifi_password_info_dataframe():
    """
    直接取得当前计算机登陆过的 wifi Ap和密码
    :return:
    """
    cmd = 'netsh wlan show profile key=clear '
    get_results = lambda cmd, res: re.findall(res, check_output(cmd, universal_newlines=True))
    wifi_ssid = get_results(cmd, ':\s(.+)')
    wifi_data = {i: get_results(cmd + i, '[关键内容|Content]\s+:\s(\w+)') for i in wifi_ssid}
    return pd.DataFrame(wifi_data).melt(var_name='AP', value_name='password')


def gen_zmt_series(start='1/1/2023', end='12/31/2023', freq='M', data_range=(1000, 80000)):
    """

    :param start: 开始日期
    :param end: 结束日期
    :param freq: 频率，M：月，D：日期
    :param data_range:  收入上下限
    :return: series， 每个间隔收入

    """

    date_rng = pd.date_range(start=start, end=end, freq=freq)
    data = np.random.uniform(*data_range, len(date_rng))
    data = np.round(data, decimals=2)
    data = pd.Series(data, index=date_rng, name='净收入')
    return data


def get_reg_parameters(x, y, data):
    """

    :param x: dataframe colum name_x
    :param y: dataframe colum name_x
    :param data: dataframe name
    :return:
    {'slope': -0.384322, 'intercept': 3.7414,
    'r_value': -0.389, 'p_value': 0.339, 'std_err ': 0.3705}
	Slope：如果斜率接近于1，则表明数据之间存在较强的线性关系。
	Intercept：截距的大小表示回归模型的拟合程度。
	r-value：r-value表示回归线和数据之间的相关性。r-value越接近于1，则说明回归模型对数据的拟合越好。
	p-value：p-value表示回归系数是否有统计学意义。如果p-value小于0.05，则说明回归系数有统计学意义。
	std_err：标准误差反映了拟合数据的精度。std_err越小，拟合数据的精度越高。

    """
    from scipy.stats import linregress
    x, y = data[x], data[y]
    names = 'slope', 'intercept', 'r_value', 'p_value', 'std_err '
    values = linregress(x, y)
    return dict(zip(names, values))



from pathlib import Path

def directory_to_str(directory_path=Path.home(), sep='\n'):
    """
    :param directory_path: 目录名
    :param sep: 分隔符
    :return: 返回一个目录下的子目录和文件，返回字符串
    """

    directory = Path(directory_path)
    print(f'Please wait for browsing {directory_path}..... ')
    # 获取目录下的所有子目录和文件（包括子目录的子目录）
    all_items = map(str, list(directory.rglob('*')))
    return sep.join(all_items)


def list_subdirectories(directory_path=Path.home()):
    """
    :param directory_path: 目录
    :return: 目录下的子目录 list
    """
    directory = Path(directory_path)

    # 获取目录下的所有子目录
    return [subdir for subdir in directory.iterdir() if subdir.is_dir()]




if __name__ == '__main__':
    '''
    df = gen_sample_dataframe(number=500, noise=.08, repeat=2)
    print(df)
    # print(gen_sample_series(number=30, noise=0.1, repeat=2))
    print(gen_sample_series())
    df = gen_sample_dataframe_12()
    print(df.head(3))
    print(f'{df.shape=},{df.ndim=}')
    print(f'{df.size=},{df.index=}')
    print(f'{df.columns=}')
    print(f'{df.dtypes=}')
    print(f'{df.values=}')
    '''
    txt = load_data('titanic')
    print(txt)
    print(gen_name( number=140))
    #print(directory_to_str())
    # print(gen_zmt_series())
