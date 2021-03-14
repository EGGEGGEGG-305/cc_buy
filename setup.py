from selenium import webdriver
# from selenium.webdriver.phantomjs import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.common.by import By
from time import sleep 
import getpass
import pickle
from twocaptcha import TwoCaptcha

solver = TwoCaptcha('a85f0c6e8c7473a9f7c66de2b369da91')

DRIVER_PATH = '.\geckodriver.exe'
# options = Options()
# options.headless = False
# options.add_argument("--window-size=1920,1200")
driver = webdriver.Firefox(executable_path=DRIVER_PATH)
driver.get("https://www.canadacomputers.com/login.php")
driver.find_element_by_xpath("/html/body/div[2]/div/div/div[2]/div[2]/form/div[1]/div[3]/input").send_keys("xxsb5214")
driver.find_element_by_xpath("/html/body/div[2]/div/div/div[2]/div[2]/form/div[1]/div[5]/input").send_keys("Caonima1!")
try:
    result = solver.recaptcha(sitekey='6LcyQTsUAAAAAI8ba3w-OPXYiz3nUu6H4onGtBPm', url='https://www.canadacomputers.com/login.php')
    driver.execute_script("""document.getElementById("g-recaptcha-response").innerHTML = arguments[0]""", result['code'])
    driver.execute_script("""onSubmit(arguments[0])""", result['code'])
    print(result)
except Exception as e:
    print(e)
driver.find_element_by_xpath("/html/body/div[2]/div/div/div[2]/div[2]/form/a").click()
wait = WebDriverWait(driver, 100)
wait.until( lambda driver: driver.current_url == "https://www.canadacomputers.com/account.php")
pickle.dump( driver.get_cookies() , open("cookies.pkl","wb"))
driver.close() 