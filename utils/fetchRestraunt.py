# Imports:
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from dotenv import load_dotenv
import os, time

load_dotenv()

# Functions:
def getMenu(url):
  try:
    items = []
    # Selenium:
    options = Options()
    options.binary_location = r'/usr/bin/firefox'
    options.add_argument("--headless")
    driver = webdriver.Firefox(options=options)

    # Get the URL:
    driver.get(url)
    dishes = WebDriverWait(driver, 20).until(
      EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'div[data-testid="normal-dish-item"]'))
    )

    # Get the dishes:
    for item in dishes:
      dishWrapper = item.find_element(By.CSS_SELECTOR, ':first-child')
      dishWrapper2 = dishWrapper.find_element(By.CSS_SELECTOR, ':nth-child(2)')
      dishName = dishWrapper2.find_element(By.CSS_SELECTOR, 'div.sc-aXZVg.cjJTeQ.sc-hIUJlX.gCYyvX').text
      dishPrice = dishWrapper2.find_element(By.CSS_SELECTOR, 'div.sc-aXZVg.kCbDOU').text
      try:
        dishDescription = dishWrapper2.find_element(By.CSS_SELECTOR, 'div.sc-aXZVg.iPKpeL.sc-jnOGJG.gaxbGu').text
      except:
        dishDescription = 'No Description'
      try:
        dishImage = dishWrapper.find_element(By.CSS_SELECTOR, 'img.styles_itemImage__DHHqs').get_attribute('src')
      except:
        dishImage = 'No Image'
      items.append({
        'name': dishName,
        'price': dishPrice,
        'description': dishDescription,
        'image': dishImage
      })
    return items
  except Exception as e:
    print(e)
    return []
  finally:
    driver.quit()

def getRestraunt(url):
  try:
    # Selenium:
    options = Options()
    options.binary_location = os.getenv('BINARY_LOCATION')
    options.add_argument("--headless")
    driver = webdriver.Firefox(options=options)

    driver.get(url)
    restrauntName = WebDriverWait(driver, 20).until(
      EC.presence_of_element_located((By.CSS_SELECTOR, 'h1.sc-aXZVg.cNRZhA'))
    ).text
    restrauntDetailWrapper = WebDriverWait(driver, 20).until(
      EC.presence_of_element_located((By.CSS_SELECTOR, 'div.sc-eIcdZJ.coysQn'))
    )
    restrauntRating = restrauntDetailWrapper.find_element(By.CSS_SELECTOR, 'div:nth-child(2)').text
    restrauntPrice = restrauntDetailWrapper.find_element(By.CSS_SELECTOR, 'div:nth-child(4)').get_attribute('innerText')
    restrauntLocationWrapper = driver.find_element(By.CSS_SELECTOR, 'div.sc-dwalKd.jzDxBO')
    restrauntLocation = restrauntLocationWrapper.find_element(By.CSS_SELECTOR, 'div:nth-child(2)').text
    return ({
      'name': restrauntName,
      'rating': restrauntRating,
      'price': restrauntPrice,
      'location': restrauntLocation,
    })
  
  except Exception as e:
    print(e)
    return "Error"
  finally:
    driver.quit()


if __name__ == '__main__':
  print(getRestraunt("https://www.swiggy.com/city/delhi/mcdonalds-e-block-south-extension-2-rest253734"))