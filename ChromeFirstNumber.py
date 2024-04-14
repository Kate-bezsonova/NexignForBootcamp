from selenium.webdriver.common.by import By
from selenium import webdriver
import time

def OpenPages():
    driver = webdriver.Chrome() #открыли браузер
    driver.maximize_window() #на полное окно

    driver.get('https://nexign.com/ru') #открыли наш сайт
    Store = "/html/body/div[1]/main/header/div/div/div[2]/nav/ul/li[3]/span" #исплоьзовала абсолютный путь, но можно было и относительный вполне
    driver.find_element(By.XPATH, Store).click() #нашли элемент и кликнули
    ProdForDev = "/html/body/div[1]/main/header/div/div/div[2]/nav/ul/li[3]/ul/li[1]/a"
    driver.find_element(By.XPATH, ProdForDev).click()
    time.sleep(5) #поставила небольшую паузу, чтобы было видно, что ссылка открывалась
    driver.quit() #закрыли браузер

def test_open_pages():
    OpenPages()
