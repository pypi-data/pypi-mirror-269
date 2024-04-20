from pet.datasets import factory

df = factory.load_data('上海地铁线路')
print(df)

# 获取所有站点信息
dfs = df.melt()
dfs.dropna(inplace=True)
print(dfs)

# 创建收集分析结果的DataFrame
result = dfs.groupby('value').agg(list)
result = result.reset_index()
result.columns = ['站名', '换乘线路']
result['线路数量'] = result['换乘线路'].apply(len)
result = result[result['线路数量'] > 1]
result = result.sort_values(by='线路数量', ascending=False)
result.to_excel('stations-exchange.xlsx', index=None)
# 得到分类汇总数据
visual_result = result.groupby('线路数量').agg('count')
visual_result = visual_result.reset_index()

# 可视化分类汇总数据

import matplotlib.pyplot as plt

plt.rcParams['font.family'] = 'SimHei'
plt.rcParams['axes.unicode_minus'] = False
fig = plt.figure(figsize=(10, 10), dpi=400)

plt.pie(visual_result['换乘线路'], labels=visual_result['线路数量'],
        textprops={'fontsize': 24},
        autopct='%1.1f%%', startangle=90)
plt.title('上海地铁换乘线路分布', fontsize=48)

# 在图中添加文字标注
for i, (label, value) in enumerate(zip(visual_result['线路数量'], visual_result['换乘线路'])):
    plt.text(1, 0.8 - 0.2 * i, f'{label}条换乘--{value}个站点', fontsize=12, color='black')
# 保存图像
plt.savefig('地铁换乘站点统计图.jpg', dpi=400)
plt.show()