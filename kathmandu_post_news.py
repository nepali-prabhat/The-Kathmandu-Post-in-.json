#makes a json file from news of the kathmandu post
def ktm_post_news(categories):
    from bs4 import BeautifulSoup as soup
    from urllib.request import urlopen as uReq
    
    #home page of the kathmandu post
    home_url= "http://kathmandupost.ekantipur.com"
    uClient = uReq(home_url)
    home_html = uClient.read()
    uClient.close()
    
    home_soup= soup(home_html, "html.parser")
    
    sticky_news = home_soup.find_all("div","sticky-news")
    news_container = home_soup.find("div", "news-container")
    main_news_items = news_container.find("div",{"class":"main-news"}).find_all("div",{"class":"item"})
    news_list_items = []
    for news_list in  news_container.find_all("div","newslist"):
        for item in news_list.find_all("div", "item"):
            news_list_items.append(item) 
    def make_home_news_dict(news_items):
        home_page_news= []
        for item in news_items:
            news_item_dict = {}
            news_item_dict["title"] = item.a.text
            news_item_dict["post_details"]  = item.find("div","post").text
            news_item_dict["summary"] = item.find("div","text").text
            news_item_dict["full_story_in"] = home_url + item.a["href"]
            home_page_news.append(news_item_dict)
        return home_page_news
    
    home_page_news = make_home_news_dict(sticky_news)+ make_home_news_dict(main_news_items) + make_home_news_dict(news_list_items)
    
    def sub_category_news(url):
        uClient = uReq(url)
        url_html = uClient.read()
        uClient.close()
        
        url_soup = soup(url_html,"html.parser")
        url_items = url_soup.find("div","categories").find_all("div","item")
        
        url_news = []
        for item in url_items:
            news_item_dict = {}
            title = item.h2.a.text
            full_story =home_url + item.h2.a["href"]
            post = item.find("p","author").text
            summary = item.find("div","teaser").text
            news_item_dict["title"] = title
            news_item_dict["post_details"]  = post
            news_item_dict["summary"] = summary
            news_item_dict["full_story_in"] = full_story
            url_news.append(news_item_dict)
        return url_news
    
    news_tuple_array = []
    news_tuple_array.append(("main",home_page_news))
#this code is not tested but still implemented.
    for category in categories:
        category_url = "http://kathmandupost.ekantipur.com/category/"+category
        news_tuple_array.append((category,sub_category_news(category_url)))
    news = dict(news_tuple_array)
    
    import datetime
    now = datetime.datetime.now()
    date = now.strftime("%Y-%m-%d")
    import json
    with open("news-"+date+".json","w") as fp:
        json.dump(news,fp)
'''
    possible categories = "national","sports","world","technology","horoscope"
    main page is by default
'''
if __name__ == "__main__":
    categories = ["national"]
    ktm_post_news(categories)


'''
alternate and tested code code:

    national_url = "http://kathmandupost.ekantipur.com/category/national"
    national_news = sub_category_news(national_url)
    
    sports_url = "http://kathmandupost.ekantipur.com/category/sports"
    sports_news = sub_category_news(sports_url)
    
    world_url = "http://kathmandupost.ekantipur.com/category/world"
    world_news = sub_category_news(world_url)
    
    technology_url = "http://kathmandupost.ekantipur.com/category/technology"
    technology_news = sub_category_news(technology_url)
    
    horoscope_url = "http://kathmandupost.ekantipur.com/category/horoscope"
    horoscope_news = sub_category_news(horoscope_url)
    
    news = {"main_page": home_page_news, "national_news":national_news,"sports_news":sports_news,"world_news":world_news,"technology_news":technology_news,"horoscope":horoscope_news}

'''