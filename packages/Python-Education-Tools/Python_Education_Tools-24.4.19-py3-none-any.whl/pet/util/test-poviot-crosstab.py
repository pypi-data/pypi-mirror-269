import pandas as pd

# 创建示例 DataFrame
df = pd.DataFrame({
    'Date': ['2023-01-01', '2023-01-01', '2023-01-02', '2023-01-02'],
    'Category': ['A', 'B', 'A', 'B'],
    'Value': [10, 20, 30, 40]
})

# 使用 pivot 函数
pivot_df = df.pivot(index='Date', columns='Category', values='Value')
print(pivot_df)
print('*'*33)
# 使用 crosstab 函数
cross_tab = pd.crosstab(index=df['Date'], columns=df['Category'], values=df['Value'], aggfunc='sum')
print(cross_tab)
print('='*33)

import pandas as pd

# 创建示例 DataFrame
df = pd.DataFrame({
    'Date': ['2023-01-01', '2023-01-01', '2023-01-02', '2023-01-02'],
    'Category': ['A', 'B', 'A', 'B'],
    'Value1': [10, 20, 30, 40],
    'Value2': [100, 200, 300, 400]
})

# 使用 pivot 函数
pivot_df = df.pivot(index='Date', columns='Category', values=['Value1', 'Value2'])
print("Using pivot:")
print(pivot_df)

# 使用 crosstab 函数
cross_tab = pd.crosstab(index=df['Date'], columns=df['Category'], values=df['Value1'], aggfunc='sum')
cross_tab['Value2'] = pd.crosstab(index=df['Date'], columns=df['Category'], values=df['Value2'], aggfunc='sum')
print("\nUsing crosstab:")
print(cross_tab)
