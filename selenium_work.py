import sys
import datetime
import logging

from selenium.webdriver import ActionChains, DesiredCapabilities
import time
import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
import hello

config = hello.app.config


class AutoBrowser:
    def __init__(self):
        options = Options()
        options.add_experimental_option("prefs", {
            "safebrowsing.enabled": True
        })
        options.add_argument('--no-sandbox')
        if config['DEBUG']:
            self.driver = webdriver.Chrome(chrome_options=options)
        else:
            self.driver = self.get_web_driver(options)
        self.devicePixelRatio = self.driver.execute_script("""return (window.devicePixelRatio)""")
        logging.info('self.devicePixelRatio %s', self.devicePixelRatio)

    def get_web_driver(self, options):
        """
        获取浏览器驱动（默认远程模式）
        :param remote:
        :return:
        """
        driver = webdriver.Remote(
            command_executor=config['REMOTE_SELENIUM'],
            desired_capabilities=DesiredCapabilities.CHROME,
            options=options,
        )
        return driver


    def login(self):
        """
        :return:
        """
        self.driver.get("https://www.weitoupiao.com/example/8793w3ye8w9pm.html?alllink=/rank")
        # self.driver.get("https://8793w3ye8w9pm.v.jisutp.com/")
        WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.TAG_NAME, 'iframe'))
        )
        iframe = self.driver.find_elements_by_tag_name("iframe")[0]
        self.driver.switch_to.frame(iframe)
        cname = 'table_rank'
        WebDriverWait(self.driver, 60).until(
            EC.visibility_of_element_located((By.CLASS_NAME, cname))
        )
        uname_input = self.driver.find_elements_by_tag_name('tr')
        key_value = {}
        for item in uname_input:
            tds = item.find_elements_by_tag_name('td')
            if len(tds) >= 3:
                key = tds[1].text
                value = tds[2].text
                key_value[key] = value

        save(key_value)


    def release(self):
        self.driver.close()

def save(info):
    now = datetime.datetime.now()
    db = hello.connect_db()
    print(info)
    for key, value in info.items():
        db.cursor().execute('insert into vote (username, num, create_time) values (%s, %s, %s)', [
            key, value, now])
    db.commit()
    db.close()



if __name__ == '__main__':
    auto_browser = None
    try:
        max_cnt = 240
        max_except_cnt = 30
        now_except_cnt = max_except_cnt
        time.sleep(30)
        print("start init", datetime.datetime.now())
        auto_browser = AutoBrowser()
        print("end init", datetime.datetime.now())
        while max_cnt and now_except_cnt:
            try:
                print("now cnt and exc", max_cnt, now_except_cnt)
                auto_browser.login()
            except Exception as e:
                print("get data fail", datetime.datetime.now())
                print(e)
                now_except_cnt -= 1
                time.sleep(10)
                continue
            else:
                now_except_cnt = min(now_except_cnt + 1, max_except_cnt)
                time.sleep(60)
            finally:
                max_cnt -= 1
    except Exception as e:
        print("init fail", datetime.datetime.now())
        print(e)
        time.sleep(10)
        exit(1)
    finally:
        if auto_browser:
            auto_browser.release()
