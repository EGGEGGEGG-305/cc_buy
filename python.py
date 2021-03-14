from time import sleep
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.common.proxy import Proxy, ProxyType
from selenium.webdriver.common.by import By
from datetime import datetime
import threading
import pickle
import queue
import random
import requests
import asyncio
from random import shuffle

# proxies = ["69.30.242.214:20001","69.30.242.214:20002","69.30.242.214:20003"]

ignored_exceptions=(NoSuchElementException,StaleElementReferenceException,)
DRIVER_PATH = '.\geckodriver.exe'

firefox_profile = webdriver.FirefoxProfile()
firefox_profile.set_preference('permissions.default.image', 2)
firefox_profile.set_preference('dom.ipc.plugins.enabled.libflashplayer.so', 'false')
options = Options()
# options.add_argument("--headless")

class MyQueue(asyncio.Queue):
    def shuffle(self):
        shuffle(self._queue)

# proxy_driver = webdriver.Firefox(options=options, executable_path=DRIVER_PATH, firefox_profile=firefox_profile)
# proxy_driver.get("https://sslproxies.org/")
# proxy_driver.execute_script("return arguments[0].scrollIntoView(true);", WebDriverWait(proxy_driver, 20).until(EC.visibility_of_element_located((By.XPATH, "//table[@class='table table-striped table-bordered dataTable']//th[contains(., 'IP Address')]"))))
# proxy_driver.find_element_by_xpath("/html/body/section[1]/div/div[2]/div/div[1]/div[2]/div/label/input").send_keys("United States")
# ips = [my_elem.get_attribute("innerHTML") for my_elem in WebDriverWait(proxy_driver, 5).until(EC.visibility_of_all_elements_located((By.XPATH, "//table[@class='table table-striped table-bordered dataTable']//tbody//tr[@role='row']/td[position() = 1]")))]
# ports = [my_elem.get_attribute("innerHTML") for my_elem in WebDriverWait(proxy_driver, 5).until(EC.visibility_of_all_elements_located((By.XPATH, "//table[@class='table table-striped table-bordered dataTable']//tbody//tr[@role='row']/td[position() = 2]")))]
# proxies = []
# proxy_driver.close()
# for i in range(0, len(ips)):
#     proxies.append(ips[i]+':'+ports[i])

async def func(url_queue, number_thread, list_total) :
    
    # new_driver
    # firefox_capabilities = webdriver.DesiredCapabilities.FIREFOX
    # firefox_capabilities['marionette'] = True
    # # driver_proxy = proxies.pop()
    # # response = requests.get("http://httpbin.org/ip", proxies=proxies)
    # # driver_proxy = response.json().get('origin')+":2000"
    # driver_proxy = "69.30.242.214:2000"
    # firefox_capabilities['proxy'] = {
    #     'proxyType': "MANUAL",
    #     'httpProxy': driver_proxy,
    #     'sslProxy': driver_proxy
    # }
    # print("Using: " + driver_proxy)
    # new_driver = webdriver.Firefox(options=options, executable_path=DRIVER_PATH, firefox_profile=firefox_profile, capabilities=firefox_capabilities)
    new_driver = webdriver.Firefox(options=options, executable_path=DRIVER_PATH, firefox_profile=firefox_profile)
    wait = WebDriverWait(new_driver, 5)

    # Dump Cookie
    new_driver.get("https://www.canadacomputers.com")
    
    item_count = 0

    while not url_queue.empty():
        if (item_count >= list_total):
            shuffle(url_queue._queue)
            item_count = 0
        else:
            item_count += 1
        current_url = await url_queue.get()
        try:
            cookies = pickle.load(open("cookies.pkl", "rb"))
            for cookie in cookies:
                new_driver.add_cookie(cookie)
        except Exception:
            pass
        try:
            new_driver.get(current_url)
            try:
                new_driver.find_elements_by_xpath("/html/body/main/div/section[2]/div[2]/div[1]/div/form/div[1]/div[2]/div[1]/button")
            except Exception:
                pass
            try:
                wait.until(EC.presence_of_element_located((By.XPATH, "/html/body/div[3]/div[1]/div/div[3]/div[2]")))
            except TimeoutException:
                await url_queue.put(current_url)
                continue
            # pickle.dump(new_driver.get_cookies() , open("cookies.pkl","wb"))
            if ("IN STOCK" in new_driver.find_element_by_xpath('/html/body/div[3]/div[1]/div/div[3]/div[2]').text) :
                print('\033[92m' + datetime.now().strftime("%d/%m/%Y %H:%M:%S") + " : " + new_driver.title + " X" + '\033[0m')
                add_to_cart_button = new_driver.find_element_by_id("btn-addCart")
                add_to_cart_button.click()
                check_out_button = new_driver.find_element_by_id("btn-checkout")
                wait.until(EC.element_to_be_clickable((By.ID, "btn-checkout")))
                check_out_button.click()

                wait.until( lambda driver: driver.current_url == "https://www.canadacomputers.com/?checkout-shipping")
                try:
                    new_driver.find_element_by_xpath('/html/body/div[2]/div/div/div[2]/button').click()
                except NoSuchElementException:
                    print("No privacy banner") 
                
                try:
                    pick_up_radio_button = new_driver.find_element_by_id("ch-shipto-store")
                    pick_up_radio_button.click()
                    store_radio_button = new_driver.find_element_by_xpath("/html/body/div[1]/div[2]/form/div[1]/div[1]/div[4]/div[2]/div[1]/div/input")
                    store_radio_button.click()
                    next_button = new_driver.find_element_by_xpath("/html/body/div[1]/div[2]/form/div[2]/div/button[2]")
                    next_button.click()
                except NoSuchElementException:
                    print("Item not avaialbe anymore")
                    await url_queue.put(current_url)
                    continue

                wait.until( lambda driver: driver.current_url == "https://www.canadacomputers.com/?checkout-payment")
                try:
                    new_driver.find_element_by_xpath('/html/body/div[1]/div[2]/form/div[1]/div[1]/div[1]/div[4]/div/div[6]/input[1]').send_keys('7988')
                    new_driver.find_element_by_xpath('/html/body/div[1]/div[2]/form/div[1]/div[1]/div[1]/div[4]/div/div[8]/input[1]').send_keys('dutta')
                except NoSuchElementException:
                    print("not found extra valid")
                new_driver.find_element_by_xpath('/html/body/div[1]/div[2]/form/div[2]/div/button[2]').click()

                wait.until( lambda driver: driver.current_url == "https://www.canadacomputers.com/?checkout-confirmation")

                print("Item Added")
                new_driver.find_element_by_xpath('/html/body/div[1]/div[2]/form/div[3]/div/button[2]').click()
                new_driver.save_screenshot('./0.png')
            else:
                print('\033[93m' + datetime.now().strftime("%d/%m/%Y %H:%M:%S") + " : " + new_driver.title + " X" + '\033[0m')
            await url_queue.put(current_url)
            sleep(random.uniform(0.5, 1.5))
        except Exception:
            print("Proxy not worked for:" + current_url)
            await url_queue.put(current_url)



#item_urls = open('list.txt', 'r').readlines()
#url_queue = asyncio.Queue()
#for url in item_urls:
#    await url_queue.put(url)
#shuffle(url_queue._queue)

async def main():   
    item_urls = open('list.txt', 'r').readlines()
    url_queue = MyQueue()
    list_total = 0
    for url in item_urls:
        await url_queue.put(url)
        list_total += 1

    number_of_threads = 1
    threads = []
    for number_thread in range(number_of_threads):
        t = threading.Thread(target=asyncio.run, args=(func(url_queue, number_thread, list_total),)) # get number for place in list `buttons`
        t.start()
        threads.append(t)
    for t in threads:
        t.join()

if __name__ == '__main__':
    asyncio.run(main())