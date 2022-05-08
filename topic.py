from asyncio.windows_events import NULL
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import StaleElementReferenceException
import pandas as pd
import time

def get_associated_topics(browser, topic):
    link_prefix = "https://github.com/topics/"
    
    link = link_prefix + topic.lower() + '?o=desc&s=updated'
    browser.get(link)
    wait = WebDriverWait(browser, 10)
    
    for i in range(0,2):
        wait.until(EC.presence_of_element_located((By.XPATH, "/html/body/div[4]/main/div[2]/div[2]/div/div[1]/form")))
        load_more_button = wait.until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[4]/main/div[2]/div[2]/div/div[1]/form/button")))
        load_more_button.click()
        print(i)
    
    div_articles = WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.XPATH, "/html/body/div[4]/main/div[2]/div[2]/div/div[1]")))
    list_articles = div_articles.find_elements(by=By.TAG_NAME, value="article")

    list_repository_topics = []
    for article in list_articles:
        list_repository_topics.append(article.find_elements(by=By.CLASS_NAME, value="topic-tag"))
    
    for list_topics in list_repository_topics:
        for topic in list_topics:
            print(topic.text)
    print("FUNCIONA")


def main(browser):
    get_associated_topics(browser, "python")


browser = webdriver.Chrome("driver\\chromedriver.exe")
main(browser)

