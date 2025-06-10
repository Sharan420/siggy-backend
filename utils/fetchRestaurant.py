# Imports:
import traceback
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from dotenv import load_dotenv
from selenium.webdriver.firefox.service import Service
import os, time

load_dotenv()

# Functions:
def check404(driver):
  try:
    driver.find_element("xpath", "//div[text()='Page not found']")
    return True
  except:
    return False

def getMenu(url):
  options = Options()
  options.binary_location = os.getenv('BINARY_LOCATION')
  options.add_argument("--headless")
  driver = webdriver.Firefox(options=options)
  try:
    items = []

    # Get the URL:
    driver.get(url)
    if check404(driver):
      return []
    dishes = WebDriverWait(driver, 20).until(
      EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'div[data-testid="normal-dish-item"]'))
    )

    # Get the dishes:
    for item in dishes:
      dishWrapper = item.find_element(By.CSS_SELECTOR, ':first-child')
      dishWrapper2 = dishWrapper.find_element(By.CSS_SELECTOR, ':nth-child(2)')
      dishName = dishWrapper2.find_element(By.CSS_SELECTOR, 'div.sc-aXZVg.eqSzsP.sc-eeDRCY.dwSeRx').text
      dishPrice = dishWrapper2.find_element(By.CSS_SELECTOR, 'div.sc-aXZVg.chixpw').text
      try:
        dishDescription = dishWrapper2.find_element(By.CSS_SELECTOR, 'div.sc-aXZVg.gCijQr.sc-gMFoeA.kaRUEI').text
      except:
        dishDescription = 'No Description'
      try:
        dishImage = dishWrapper.find_element(By.CSS_SELECTOR, 'img._3XS7H').get_attribute('src')
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
    print("Quitting driver")
    driver.quit()

def getRestaurant(url):
  options = Options()
  options.binary_location = os.getenv('BINARY_LOCATION')
  #options.add_argument("--headless")
  driver = webdriver.Firefox(options=options)
  try:
    # Selenium:
    driver.get(url)

    if check404(driver):
      return {}

    RestaurantName = WebDriverWait(driver, 20).until(
      EC.presence_of_element_located((By.CSS_SELECTOR, 'h1.sc-aXZVg.gONLwH'))
    ).text
    RestaurantDetailWrapper = WebDriverWait(driver, 20).until(
      EC.presence_of_element_located((By.CSS_SELECTOR, 'div.sc-bJBgwP.bxtKCW'))
    )
    RestaurantRating = RestaurantDetailWrapper.find_element(By.CSS_SELECTOR, 'div:nth-child(2)').text
    RestaurantPrice = RestaurantDetailWrapper.find_element(By.CSS_SELECTOR, 'div:nth-child(4)').get_attribute('innerText')
    RestaurantLocationWrapper = driver.find_element(By.CSS_SELECTOR, 'div.sc-bfhvDw.sURFq')
    RestaurantLocation = RestaurantLocationWrapper.find_element(By.CSS_SELECTOR, 'div:nth-child(2)').text
    return ({
      'name': RestaurantName,
      'rating': RestaurantRating,
      'price': RestaurantPrice,
      'location': RestaurantLocation,
    })
  
  except Exception as e:
    print(f"🔍 Error Type: {type(e).__name__}")
    print(str(e))
    traceback.print_exc()
    return "Error"
  finally:
    print("Quitting driver")
    driver.quit()

def testFunc():
  service = Service(os.getenv('DRIVER_LOC'))
  options = Options()
  options.binary_location = os.getenv('BINARY_LOCATION')
  options.add_argument("--headless")
  driver = webdriver.Firefox(service=service,options=options)
  driver.get("https://www.swiggy.com/")
  driver.quit()
if __name__ == '__main__':
  #testFunc()
  print(getRestaurant("https://www.swiggy.com/city/delhi/mcdonalds-e-block-south-extension-2-rest253734"))