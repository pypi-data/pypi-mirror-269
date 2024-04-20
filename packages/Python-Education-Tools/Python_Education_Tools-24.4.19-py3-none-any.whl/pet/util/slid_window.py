def slide_window(data,window_size=4,stride=2,fun=sum):
    '''
    参数：

    data：列表，要处理的数据。
    window_size：整数，窗口大小。
    stride：整数，每次移动的步长。
    fun：函数，对每个窗口进行的运算。默认是求和。
    :return: 滑动窗口数据，处理数据
    '''
    data_lst = (data[i::stride] for i in range(window_size))
    result1 = zip(*data_lst)
    result1 = list(result1)
    result2=list(map(fun,result1))
    return result1,result2
if __name__ == '__main__':
    data=[9,6,8,4,7,3,8,4,2,1,3,2]
    print(slide_window(data))
    print(slide_window(data=data,fun=max))
    print(slide_window(data=data, fun=min))
    print(slide_window(data=data, fun=sum))
