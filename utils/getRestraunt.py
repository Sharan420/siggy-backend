from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

options = Options()
options.binary_location = r'C:\Program Files\Mozilla Firefox\firefox.exe'

def getRestraunt(url):
  driver = webdriver.Firefox(options=options)
  driver.get(url)
  dishes = WebDriverWait(driver, 20).until(
    EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'div[data-testid="normal-dish-item"]'))
  )
  for item in dishes:
    dishWrapper = item.find_element(By.CSS_SELECTOR, ':first-child')
    
    
  driver.quit()
  

getRestraunt('https://www.swiggy.com/city/delhi/california-burrito-vasant-vihar-vasant-kunj-rest737075')