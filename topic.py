from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import pandas as pd
import matplotlib.pyplot as plt

def bar_graphic(dict_axis, topic):
    fig, ax = plt.subplots(figsize =(16, 8))
    ax.bar(dict_axis['Topic'][:20], dict_axis['Amount'][:20])
    plt.xlabel('Topic Relacionado')
    plt.ylabel('Cantidad')
    plt.title('Grafico de los Topics relacionados a' + topic + 'con relacion a la cantidad de apariciones', loc ='left')
    for s in ['top', 'bottom', 'left', 'right']:
        ax.spines[s].set_visible(False)
    ax.xaxis.set_ticks_position('none')
    ax.yaxis.set_ticks_position('none')
    plt.xticks(rotation=90)
    ax.grid(b = True, color ='grey',
        linestyle ='solid', linewidth = 0.5,
        alpha = 0.2)
    plt.subplots_adjust(bottom=0.23, right=0.95, top=0.94, left=0.05)
    plt.show()

def get_associated_topics(browser, topic):
    link_prefix = 'https://github.com/topics/'
    link = link_prefix + topic.lower() + '?o=desc&s=updated&page=' 
    wait = WebDriverWait(browser, 10)
    dict_of_related_topics = {}
    
    # every article has many repositories topics
    for page_nr in range(1,2):
        browser.get(link + str(page_nr))
        list_articles = WebDriverWait(browser, 10).until(EC.presence_of_all_elements_located((By.TAG_NAME, 'article')))
        for article in list_articles:
            list_of_related_topics_of_the_article = article.find_elements(by=By.CLASS_NAME, value='topic-tag')
            for related_topic in list_of_related_topics_of_the_article:
                if related_topic.text in dict_of_related_topics.keys():
                    dict_of_related_topics[related_topic.text] += 1
                else:
                    dict_of_related_topics[related_topic.text] = 1
    dict_axis = {'Related Topic': [], 'Amount':[]}
    dict_sorted = sorted(dict_of_related_topics.items(), key=lambda kv: kv[1], reverse= True)
    for key, val in  dict_sorted:
        dict_axis['Related Topic'].append(key)
        dict_axis['Amount'].append(val)

    bar_graphic(dict_axis, topic)


def main(browser):
    dict_axis = get_associated_topics(browser, 'bot')
    

if __name__ == '__main__':
    try:
        browser = webdriver.Chrome("driver\\chromedriver.exe")
        main(browser)
    finally:
        browser.quit()