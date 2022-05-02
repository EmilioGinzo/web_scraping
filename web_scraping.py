from asyncio.windows_events import NULL
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def getTop(PATH, link):
    try:
        driver = webdriver.Chrome(PATH)
        driver.get(link)
        tiobe_file = open('tiobe_top_20.txt', 'w', encoding = 'utf-8')
        table_top = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "top20"))
        )
        
        lenguajes = table_top.find_element(by=By.TAG_NAME, value="tbody").find_elements(by=By.TAG_NAME, value="tr")
        top_array = [[["Nombre"], ["Rating"]]]

        for lenguaje in lenguajes:
            td = lenguaje.find_elements(by=By.TAG_NAME, value="td")
            tiobe_file.write(td[4].text + "\t\t\t\t\t\t" + td[5].text + '\n')
            top_array.append([[td[4].text], [td[5].text]])
        return top_array
    except:
        return NULL
    finally:
        driver.quit()
        tiobe_file.close()

top = getTop("driver\\chromedriver.exe", "https://www.tiobe.com/tiobe-index/")
for lenguaje in top:
    print(lenguaje)
