
# Dependencies
from os import getcwd
from os.path import join
from bs4 import BeautifulSoup as bs
import requests
from splinter import Browser
import time
import pandas as pd

def init_browser():
    executable_path = {"executable_path": "/usr/local/bin/chromedriver"}
    return Browser("chrome", **executable_path, headless=False)

def scrape():
    browser = init_browser()
    # create surf_data dict that we can insert into mongo
    mars_data = {}
    # get_ipython().system('pip install splinter')
    # # Nasa Mars News
    #websites that needs to be scrapped
    url = 'https://mars.nasa.gov/news/'
    time.sleep(2)
    #Retrieve page with the requests module
    html = requests.get(url)
    # print(html)

    soup = bs(html.text, 'html.parser')

    # print(soup.prettify())

    # soup.body

    time.sleep(1)

    results = soup.find_all(class_='content_title')

    news_title= results[0].text

    mars_data["news_title"]= news_title

    time.sleep(3)

    # print(news_title)


    results1=soup.find_all(class_='rollover_description_inner')


    p_news= results1[0].text

    mars_data["p_news"]=p_news

    # print(p_news)


    # # JPL Mars Space Image - Featured Image

    
    url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url)

    time.sleep(2)


    browser.click_link_by_partial_text('FULL IMAGE')

    time.sleep(2)

    html=browser.html
    soup=bs(html, "html.parser")

    body = soup.find_all('body')
    # result = soup.find_all('img',class_='fancybox-image')

    time.sleep(2)


    results = soup.find('body')


    second_half= results.find_all('a', class_='button fancybox')[0]['data-fancybox-href']

    first_half = "https://www.jpl.nasa.gov"

    featured_image_url = first_half+second_half

    mars_data["featured_image_url"]=featured_image_url

    # print(featured_image_url)

    # 
    # # Mars Weather 

    #websites that needs to be scrapped
    url = 'https://twitter.com/marswxreport?lang=en'

    html = requests.get(url)
    # print(html)

    time.sleep(2)

    soup = bs(html.text, 'html.parser')

    # print(soup.prettify())


    soup.find('body')


    res= soup.find_all('p', class_='TweetTextSize TweetTextSize--normal js-tweet-text tweet-text')

    mars_weather= res[0].text

    # print(mars_weather)

    mars_data["mars_weather"]=mars_weather


    # # Mars Facts

    # In[72]:

    url = 'https://space-facts.com/mars/'
    time.sleep(2)
    tables = pd.read_html(url)

    # tables

    df = tables[0]
    df.columns = ['Planet Profile', 'Values']

    # df


    html_table = df.to_html()
    # html_table


    # In[76]:


    html_table=html_table.replace('\n', '')

    html_table=df.to_html('table.html')

    mars_data["html_table"]=html_table

    df.to_html('mars_facts.html')

    soup=bs(open("mars_facts.html"),"html.parser")
    ## Stripping the soup data and saving in mars_facts disctionary, mars_info is a temperory list used
    mars_info=[]
    mars_facts={}
    for z in soup.table('td'):
        #print(z.text)
        mars_info.append(z.text.strip(':'))
    mars_facts=dict([(k, v) for k,v in zip (mars_info[::2], mars_info[1::2])])
    # print(mars_facts)

    mars_data["mars_facts"]=mars_facts

    mars_info1=[]

    mars_info1.append(mars_facts)

    # print(mars_info1)

    mars_data["mars_info1"]=mars_info1




    # In[77]:


    # df.to_html('table.html')

    # get_ipython().system('open table.html')


    # # Mars Hemisphere 

    # In[80]:


    #websites that needs to be scrapped

    url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'

    

    #Retrieve page with the requests module
    html = requests.get(url)
    time.sleep(2)
    # print(html)

    soup = bs(html.text, 'html.parser')

    # print(soup.prettify())

    # soup.find('body')


    # In[168]:


    rel = soup.find_all(class_='itemLink product-item')


    # In[177]:


    rel1 = soup.find_all(class_='thumb')


    # In[179]:


    # rel1[0]['src']


    # In[187]:


    title=[]
    for titles in rel:
        title.append(titles.text)
        


    # In[188]:


    urls=[]

    for url in rel1:
        image_url="https://astrogeology.usgs.gov/"+url['src']
        urls.append(image_url)
        


    # In[212]:


    hemisphere_image_urls=[]
    i=0
    for i in range(4):
        d = {"title":title[i], "image_url":urls[i]}
        hemisphere_image_urls.append(d)



    # In[213]:


    mars_data["hemisphere_image_urls"]=hemisphere_image_urls

    return mars_data

