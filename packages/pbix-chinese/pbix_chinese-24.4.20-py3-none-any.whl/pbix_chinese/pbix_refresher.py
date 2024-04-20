import time
import os
import psutil
from pywinauto.application import Application


def refresher(file_path, re_timeout=300):
    """
    file_path: pbi文件路径
    re_timeout: 刷新等待时间
    仅支持2023年9月以前版本的power bi 软件, 2023年10月及之后的不支持
    """
    procname = "PBIDesktop.exe"
    for proc in psutil.process_iter():
        if proc.name() == procname:
            proc.kill()
    time.sleep(1)

    # 启动 Power bi
    os.system('start "" "' + file_path + '"')
    time.sleep(5)

    # 连接power bi
    app = Application(backend='uia').connect(path=procname)
    win = app.window(title_re='.*Power BI Desktop')
    time.sleep(5)
    try:
        win['刷新'].wait("enabled", timeout=120)
        win['刷新'].click()
    except TimeoutError:
        print(f'{file_path}, 未识别窗口句柄, 连接超时')

    try:
        win['保存'].wait("enabled", timeout=re_timeout)
        win['保存'].click()
    except TimeoutError:
        print(f'{file_path}, 刷新等待超时')
    # win.type_keys("^s")
    win.wait("enabled", timeout=15)
    win.close()

    for proc in psutil.process_iter():
        if proc.name() == procname:
            proc.kill()


if __name__ == '__main__':
    path = r'C:\Users\Administrator\Downloads\数据.pbix'
    refresher(path)
