import matplotlib.pyplot as plt
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException
from datetime import date
from datetime import timedelta


def bar_chart(dict_of_related_topics: dict, topic: str):
    """
    receives dict_of_related_topics as follows: 
    dict_of_related_topics = {'<TopicX_Name>': <number_of_appearence>,
    '<TopicX_Name>': <number_of_appearence>,
    '<TopicX_Name>': <number_of_appearence>,
    ...}
    """
    dict_axis = {'Related Topic': [], 'Counter':[]}

    for key, val in  dict_of_related_topics:
        dict_axis['Related Topic'].append(key)
        dict_axis['Counter'].append(val)

    fig, ax = plt.subplots(figsize =(16, 8))
    ax.bar(dict_axis['Related Topic'][:20], dict_axis['Counter'][:20])
    plt.xlabel('Topic Relacionado')
    plt.ylabel('Cantidad')
    plt.title('Grafico de los Topics relacionados a ' + topic + ' con relacion a la cantidad de apariciones', loc ='left')
    for s in ['top', 'bottom', 'left', 'right']:
        ax.spines[s].set_visible(False)
    ax.xaxis.set_ticks_position('none')
    ax.yaxis.set_ticks_position('none')
    plt.xticks(rotation=90)
    ax.grid(visible = True, color ='grey',
        linestyle ='solid', linewidth = 0.5,
        alpha = 0.2)
    plt.subplots_adjust(bottom=0.23, right=0.95, top=0.94, left=0.05)
    plt.show()

def relative_time_is_present(article):
    try:
        article.find_element(by=By.TAG_NAME, value='relative-time')
        return True
    except NoSuchElementException:
        return False


def get_related_topics(browser: webdriver, topic: str):
    """
    receives the open browser and the topic to search in https://github.com/topics/
    and return a dictionary containing the related topics and the number of times these topics were related to
    the topic we chose, is returned as follows:
    dict_of_related_topics = {'<TopicX_Name>': <number_of_appearence>,
    '<TopicX_Name>': <number_of_appearence>,
    '<TopicX_Name>': <number_of_appearence>,
    ...}
    """
    link = 'https://github.com/topics/' + topic.lower() + '?o=desc&s=updated&page=' 
    dict_of_related_topics = dict()
    max_date = date.today() - timedelta(days=30)

    # every article has many repositories topics
    # if the article has relative time, we compare it wit the maximum datetime, if it is greater thanthe maximum datetime, we return the dictionary
    for page_nr in range(1,11):
        browser.get(link + str(page_nr))
        list_articles = WebDriverWait(browser, 10).until(EC.presence_of_all_elements_located((By.TAG_NAME, 'article')))
        for article in list_articles:
            list_of_related_topics_of_the_article = article.find_elements(by=By.CLASS_NAME, value='topic-tag')
            if relative_time_is_present(article):
                date_created_str = article.find_element(by=By.TAG_NAME, value='relative-time').get_attribute('datetime')
                # example: date_created_str[:10] => 2022-05-17
                date_created = date.fromisoformat(date_created_str[:10])
                if date_created > max_date:
                    for related_topic in list_of_related_topics_of_the_article:
                        if related_topic.text in dict_of_related_topics.keys():
                            dict_of_related_topics[related_topic.text] += 1
                        else:
                            dict_of_related_topics[related_topic.text] = 1

    return dict_of_related_topics

def main(browser: webdriver):
    file_related_topics = open('Related Topics.txt', 'w', encoding = 'utf-8')

    dict_related_topics = get_related_topics(browser, 'bot')
    dict_related_topics = sorted(dict_related_topics.items(), key=lambda kv: kv[1], reverse= True)

    text_format = '{:25} {}\n'.format('Topic relacionado', 'cantidad de apariciones')
    print('{:25} {}'.format('Topic relacionado', 'cantidad de apariciones'))
    file_related_topics.write(text_format)

    for key, val in dict_related_topics:
        text_format = '{:25} {}\n'.format(key, str(val))
        print('{:25} {}'.format(key, str(val)))
        file_related_topics.write(text_format)

    file_related_topics.close()
    bar_chart(dict_related_topics, 'bot')

if __name__ == '__main__':
    try:
        browser = webdriver.Chrome("driver\\chromedriver.exe")
        main(browser)
    finally:
        browser.quit()
