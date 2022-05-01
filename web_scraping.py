from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

PATH = "driver\\chromedriver.exe"
driver = webdriver.Chrome(PATH)
driver.get("https://www.tiobe.com/tiobe-index/")

try:
    tiobe_file = open('tiobe_top_20.txt', 'w', encoding = 'utf-8')
    table_top = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "top20"))
    )
    
    lenguajes = table_top.find_element(by=By.TAG_NAME, value="tbody").find_elements(by=By.TAG_NAME, value="tr")
    
    for lenguaje in lenguajes:
        td = lenguaje.find_elements(by=By.TAG_NAME, value="td")
        tiobe_file.write(td[0].text + "\t\t" + td[4].text + "\t\t\t\t\t\t" + td[5].text + '\n')
finally:
    driver.quit()
    tiobe_file.close()