import re
from subprocess import check_output
import pandas as pd

def get_wifi_password():
    cmd = 'netsh wlan show profile key=clear '
    get_results = lambda cmd, res: re.findall(res, check_output(cmd, universal_newlines=True))
    wifi_ssid = get_results(cmd, ':\s(.+)')
    return {i: get_results(cmd + i, '[关键内容|Content]\s+:\s(\w+)') for i in wifi_ssid}


def get_nic():
    cmd = 'netsh trace show interfaces'
    get_results = lambda cmd, res: re.findall(res, check_output(cmd, universal_newlines=True))

    return get_results(cmd, '描述:\s+(.+)')



if __name__ == '__main__':
    d = get_wifi_password()
    print(pd.DataFrame(get_wifi_password()).melt(var_name='AP', value_name='password'))
    print(get_nic())

