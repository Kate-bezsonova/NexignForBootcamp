from selenium.webdriver.common.by import By
from selenium import webdriver
import requests
import enchant
import re



def GetLinks():
    linkForOpen = "https://nexign.com/ru"
    linkForSort = "https://nexign.com"
    links = GetUniqueLinks(linkForOpen)
    links = GetLocalLinks(linkForSort, links)
    return links


def GetUniqueLinks(linkForOpen):  # метод, который открывает нужный сайт и ищет на нём уникальные ссылки
    driver = webdriver.Chrome()
    driver.maximize_window()
    driver.get(linkForOpen)  # открыли сайт в Хроме в полном окне
    elementsA = driver.find_elements(By.XPATH, "//a[@href]")  # получили все элементы с сылками
    links = []
    for x in elementsA:
        links.append(x.get_attribute('href'))  # достали из элементов адреса гиперссылок
    links = list(set(links))  # конвертировала в множество и обратно, чтобы убрать дубли
    driver.quit()
    return links


def GetLocalLinks(linkForSort, links):  # метод, который оставляет ссылки с нашим доменом
    for link in links:
        if linkForSort not in link[:len(linkForSort)] or 'linkedin' in link:
            links.remove(link)  # убираем ссылки на внешние источники
    return links


def DoParsing(links):
    driver = webdriver.Chrome()
    driver.maximize_window()
    searchText = "nord"  # можно поменять искомое слово
    amountOfSearchText = 0  # переменная для подсчета слов
    mistakes = []
    for x in links:
        driver.get(x)  # открываем каждую страницу сайта, по уникальным ссылкам с нашим доменом
        response = requests.get(x)  # пингуем, что сайт открылся успешно
        if response.status_code == 200:
            content = driver.page_source  # берем всю информацию на странице
            content = content.lower() #понизили регистр
            amountOfSearchText += content.count(searchText)  # считаем количество искомых слов nord
            mistakes.extend(CheckOrthography(content, mistakes))    #получаем ошибки в контенте (по версии словаря)
            mistakes = list(set(mistakes)) #снова убираем дубли, потому что в общем массиве уже могут быть слова с других страниц
            # CheckMistakes(mistakes, x)
            # #предлагаю усовершенствовать программу и записать верные слова в словарь, а неверные оставить в массиве,
            # возможный вариант программы в комментариях внизу
    mistakes.sort() #вывод по алфавиту для удобства
    print("Массив ошибок на сайте по версии библиотеки enchant: ", mistakes)
    print("Количество слов nord: ", amountOfSearchText)
    driver.quit()
def CheckOrthography(content, mistakes):  # метод для проверки орфографии
    orthog = [x.strip() for x in re.findall(r'[а-яА-ЯёЁ]+', content)]
        # составили массив только из русских слов и убрали пробелы по краям
    orthog = list(filter(lambda x: x != '' and x != '-' and x != '--', orthog))
        # убрали элементы, состоящие только из пробелов и дефисов
    dictionary = enchant.Dict("ru_RU") #русский словарь пришлось добавлять, потому что в enchant русскго по умолчанию нет
    for o in orthog: #пробегаем по всем словам и проверяем, что слова нет в словаре
        if not dictionary.check(o):
            mistakes.append(o)
    mistakes = list(set(mistakes)) #убираем дубли на странице
    return mistakes

def test_find_text_on_site_and_check_orthography(): #сам тест на нахождение слова и ошибок в орфографии
    links = GetLinks() #сначала найдем ссылки на главной странице, уберем дубли и ссылки на внешние источники
    DoParsing(links)    #запустим парсинг

# def CheckMistakes(mistakes, x): #передали массив с ошибками и гиперссылку
#     dictionary = enchant.Dict("ru_RU")
#     toReplaseOnSite = [] #массив cловарей вида {'Слово с ошибкой': m, 'Правильное слово': sug[num], 'Адрес сайта': x}
#     for m in mistakes: #для каждого слова в массиве ошибок спрашиваем у пользователя верное оно или нет
#         print("В слове, возможно, есть ошибка: ", m)
#         sug = dictionary.suggest(m)
#         print("Предлагаю варианты написания", sug)
#         question = int(input("Это верное слово? 0 - да, 1 - нет, но предложено верное, 2 - нет, я напишу как надо"))
#         match question:
#             case 0:
#                 enchant.Dict.add(m)
#                 mistakes.remove(m)
#             case '1':
#                 toReplaseOnSite.append(writeMistakesInDict(m, sug, x))
#             case '2':
#                 toReplaseOnSite.append(userWriteMistakesInDict(m, x))
#             case _:
#                 toReplaseOnSite.append(userDidntAnswer(m, x))
#
# def writeMistakesInDict(m, sug, x): #записываем слово с ошибкой, верное слово из предложенных и гиперссылку в массив
#         num = int(input("Напишите номер верного слова из предложенных")) - 1 #пользователь указывает слово, а мы вычитаем 1, так как в массиве счет с 0
#         return {'Слово с ошибкой': m, 'Правильное слово': sug[num], 'Адрес сайта': x}
#
# def userWriteMistakesInDict(m, x): #записываем слово с ошибкой, верное слово от пользователя и гиперссылку в массив
#     word = input("Напишите слово верно: ")
#     return {'Слово с ошибкой': m, 'Правильное слово': word, 'Адрес сайта': x}
#
# def userDidntAnswer(m, x): #записываем слово с ошибкой и гиперссылку в массив
#     print("Я все равно запишу в словарик")
#     return {'Слово с ошибкой': m, 'Адрес сайта': x}


