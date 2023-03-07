import time
import json
import csv
from bs4 import BeautifulSoup as bs
from lxml import etree
from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException

'''Opening a csv file to write the data'''
headers = ['product_name', 'price', 'star_ratings', 'sold_by', 'seller_ratings']
with open ('pro_details.csv', "w") as f:
   writer = csv.writer(f)
   writer.writerow(headers)


class Messho:
    def __init__(self): 
      
      self.product_links = []
      self.prod_dict = {}
      self.driver = webdriver.Chrome(ChromeDriverManager().install())
      self.driver.get("https://www.meesho.com/women-kurtis/pl/3j0")
      self.driver.implicitly_wait(5)
      self.driver.maximize_window()

    def scroll_to_bottom(self):
      '''Function to scroll to the bottom of the page'''

      count = 0
      scroll_pause_time = 1
      screen_height = self.driver.execute_script("return window.screen.height;") 
      i = 1
      while True:
          self.driver.execute_script("window.scrollTo(0, {screen_height}*{i});"\
                                     .format(screen_height=screen_height, i=i))
          i += 0.4
          count+=1
          time.sleep(scroll_pause_time)
          scroll_height = self.driver.execute_script("return document.body.scrollHeight;")
          if (screen_height) * i > scroll_height:
              break
          else:
             if count==2:
                break
    
    def get_product_links(self):
       '''Function to get links of all the items present on the page'''

       page = self.driver.page_source
       soup = bs(page, "lxml")
       dom = etree.HTML(str(soup))
       productlink_xpath = dom.xpath('//div[@class = "sc-iBYQkv sc-pyfCe cxNXNj bOKdJv products"]//div[@class = "sc-ftTHYK ProductList__GridCol-sc-8lnc8o-0 cRCBPy FGMeB"]//a//@href')

       for link in productlink_xpath:
          self.product_links.append("https://www.meesho.com"+link)
    
    def product_details(self):
       '''This will load the product pages and get the details of those'''
       print(self.product_links)
       for link in self.product_links:
          
          self.driver.get(link)
          page = self.driver.page_source
          soup = bs(page, "lxml")
          dom = etree.HTML(str(soup))

          product_name = dom.xpath('//div[@class = "sc-jSUZER ibSIpo"]//p[@class = "sc-gswNZR VDXnl pre pre"][1]//text()')
          price = dom.xpath('//h4[@class = "sc-dkrFOg ddQBQ"]//text()')
          star_ratings = dom.xpath('//span[@class = "ShippingInfo__RatingsRow-sc-frp12n-2 edtAlz"]//text()')
          sold_by = dom.xpath('//span[@class = "sc-dkrFOg kTOwRq ShopCardstyled__ShopName-sc-du9pku-6 bdcHGu ShopCardstyled__ShopName-sc-du9pku-6 bdcHGu"]//text()')
          seller_ratings = dom.xpath('//span[@class = "sc-dkrFOg gTprEm"]//text()')

          self.details_to_csv(product_name,price,star_ratings,sold_by,seller_ratings)

    def details_to_csv(self, product_name,price,star_ratings,sold_by,seller_ratings):
       '''Function to write the output values to csv file'''

       value_ = [product_name,price,star_ratings,sold_by,seller_ratings]
       with open ('pro_details.csv', 'a', encoding='utf8') as f:
          writer = csv.writer(f)
          writer.writerow(value_)
          
      
obj = Messho()
obj.scroll_to_bottom()
obj.get_product_links()
obj.product_details()

