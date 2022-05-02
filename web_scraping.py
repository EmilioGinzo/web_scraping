from asyncio.windows_events import NULL
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def getTop(browser):
    try:
        browser.get("https://www.tiobe.com/tiobe-index/")
        tiobe_file = open('tiobe_top_20.txt', 'w', encoding = 'utf-8')
        table_top = WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.ID, "top20"))
        )
        
        languages = table_top.find_element(by=By.TAG_NAME, value="tbody").find_elements(by=By.TAG_NAME, value="tr")
        list_top20_name_rating = [["Nombre", "Rating"]]

        for language in languages:
            td = language.find_elements(by=By.TAG_NAME, value="td")
            tiobe_file.write(td[4].text + "\t\t\t\t\t\t" + td[5].text + '\n')
            list_top20_name_rating.append([td[4].text, td[5].text])
        return list_top20_name_rating
    except:
        return NULL
    finally:
        tiobe_file.close()

def github_topics_top20(browser, topic):
    try:
        link_prefix = "https://github.com/topics/"
        list_of_wrong_names = ['C#','C++','Delphi/Object Pascal','Classic Visual Basic','Visual Basic']
        list_of_right_names = ['c-sharp','cpp','pascal','visual basic','vbnet']
        
        if topic in list_of_wrong_names:
            link = link_prefix + list_of_right_names[list_of_wrong_names.index(topic)]
        else:
            link = link_prefix + topic.lower()

        browser.get(link)
        resultados = open('Resultados.txt', 'a', encoding = 'utf-8')
        repositories = WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.XPATH, "/html/body/div[4]/main/div[2]/div[2]/div/div[1]/h2"))
        )

        for s in repositories.text.split():
            if s[:1].isdigit():
                repositories_str = s
        
        resultados.write(topic + "\t" + repositories_str + '\n')
        

    finally:
        resultados.close()

def main(browser):
    top = getTop(browser)
    for lenguaje in top[1:]:
        github_topics_top20(browser, lenguaje[0])

browser = webdriver.Chrome("driver\\chromedriver.exe")
main(browser)
browser.quit()
