# Imports:
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Functions:
def getRestraunt(url):
  try:
    items = []
    # Selenium:
    options = Options()
    options.binary_location = r'C:\Program Files\Mozilla Firefox\firefox.exe'
    options.add_argument("--headless")
    driver = webdriver.Firefox(executable_path='utils/geckodriver.exe',options=options)

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
