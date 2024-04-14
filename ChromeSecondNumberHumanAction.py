from selenium.webdriver.common.by import By
from selenium import webdriver

# этот вариант решения имитирует действия пользователя
# (Более автоматизированное решение я добавила в ChromeSecondAndThirdNuber.py)
def HumanAction():
    driver = webdriver.Chrome() #открыли браузер на полное окно и наш сайт
    driver.maximize_window()
    driver.get('https://nexign.com/ru')

    Search = "/html/body/div[1]/main/header/div/div/div[3]/div[2]/a" #клик по иконке поиска
    driver.find_element(By.XPATH, Search).click()

    Input = "/html/body/div[1]/div[1]/div/div[2]/div[1]/div[1]/input" #написали в поисковике nord
    driver.find_element(By.XPATH, Input).send_keys("nord")

    Submit = ".//input[@id='edit-submit-search']" #клик по поиску
    driver.find_element(By.XPATH, Submit).click()

    PagesButtons = "/html/body/div/main/div[3]/div/div/div[1]/div/nav/ul/li" #нашли кнопку вперед для листания страниц (если их будет больше двух)
    elementPages = driver.find_elements(By.XPATH, PagesButtons)  # посчитали сколько сейчас кнопок со страницами
    amountOfPages = len(elementPages) - 2  # сколько конкретно страниц без кнопки листания вперед/назад
    amountNord = 0

    for p in range(1, amountOfPages+1): #цикл подсчета слова nord на каждой странице поиска на сайте
        NordSearchMark = driver.find_elements(By.CLASS_NAME, "search__mark")  # посчитали найденные nord сайтом
        amountNord += len(NordSearchMark)

        elementsNordInTitle = driver.find_elements(By.CLASS_NAME, "line-group-search__title")  # выбрали все заголовки

        for x in elementsNordInTitle:
            if "nord" in x.text.lower(): amountNord += 1  # добавили к сумме уже найденных nord заголовки, где тоже есть это слово
                                                        #(тут кстати можно было проверить, сколько слов nord в заголовке, будем считать, что 1)
        if p < amountOfPages:
            x = driver.find_element(By.XPATH, "//a[@rel='next']").get_attribute('href') #пока кнопка вперед не пропала будем переходить на следующую страницу
            driver.get(x)

    elementsNordInFooter = driver.find_elements(By.CLASS_NAME, "footer__col") #ну и посчитаем сколько слов в футере
    for x in elementsNordInFooter:
        if "nord" in x.text.lower(): amountNord += 1

    print(amountNord)
    driver.quit()

def test_human_action():
    HumanAction()


