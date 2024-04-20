import re

def extract_code(text):
    # 正则表达式，用于匹配Python代码块
    pattern = re.compile(r'```python(.*?)```', re.DOTALL)
    code_blocks = re.findall(pattern, text)
    print(code_blocks)

    for i, code_block in enumerate(code_blocks):
        with open(f"code_{i}.py", "w") as f:
            f.write(code_block)

# 读取大文件
with open("big_file.txt", "r",encoding='utf-8') as f:
    text = f.read()

# 提取代码块并保存到多个文件中
extract_code(text)
