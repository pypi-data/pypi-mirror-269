import datetime
import os
import webbrowser
import pytest


# pytest 配置钩子
def pytest_configure(config):
    # 生成带时间戳的报告文件名
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    if not config.option.htmlpath:
        config.option.htmlpath = f"reports/report_{timestamp}.html"

# 测试会话结束钩子
@pytest.hookimpl(tryfirst=True)
def pytest_sessionfinish(session, exitstatus):
    htmlpath = session.config.option.htmlpath
    if htmlpath:
        report_path = str(htmlpath)
        if os.path.isfile(report_path):
            webbrowser.open_new_tab(report_path)
