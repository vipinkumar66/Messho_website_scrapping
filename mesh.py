import time
from bs4 import BeautifulSoup as bs
from lxml import etree
from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException

class Messho:
    def __init__(self): 

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
             if count==6:
                break
    
    def get_all_details(self):
       '''Function to get all the important details related to the item'''

       page = self.driver.page_source
       soup = bs(page, "lxml")
       dom = etree.HTML(str(soup))
       product_cards = dom.xpath('//div[@class = "sc-iBYQkv sc-pyfCe cxNXNj bOKdJv products"]//div[@class = "sc-ftTHYK ProductList__GridCol-sc-8lnc8o-0 cRCBPy FGMeB"]//a//@href')

       with open("print_file.txt", "w") as f:
          for card in product_cards:
            try:
              f.write(card)
              f.write('\n')
            except UnicodeEncodeError:
               pass
      
obj = Messho()
obj.scroll_to_bottom()
obj.get_all_details()

