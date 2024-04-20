import re
from functools import  reduce
'''
s='他的基础工资123.45元，加班234.56元，奖金56.77元，补贴33元！！'
d=re.findall('(\d+\.?\d*)',s)
d=set(d) #去重
table=dict(zip(d,map(lambda x:str(round(float(x)*1.1,2)),d)))
print(table)
print('涨工资前:',s)
s=reduce(lambda x,y:x.replace(y,table[y]),table.keys(),s)
print('涨工资后:',s)
'''

from datetime import datetime



def id_card_to_age(id_card):
    if len(id_card) != 18:
        raise ValueError("身份证号码长度错误")

    birth_year = int(id_card[6:10])
    birth_month = int(id_card[10:12])
    birth_day = int(id_card[12:14])

    current_year = datetime.now().year
    current_month = datetime.now().month
    current_day = datetime.now().day

    age = current_year - birth_year

    if (birth_month, birth_day) > (current_month, current_day):
        age -= 1

    return age
def replace(content,table):
    return reduce(lambda x,y:x.replace(y,table[y]),table.keys(),content)

if __name__ == '__main__':
    s = '他的基础工资123.45元，加班234.56元，奖金56.77元，补贴33元！！'
    d = re.findall('(\d+\.?\d*)', s)
    d = set(d)  # 去重
    table = dict(zip(d, map(lambda x: str(round(float(x) * 1.1, 2)), d)))
    print(table)
    print('涨工资前:', s)
    s = replace(s,table)
    print('涨工资后:', s)