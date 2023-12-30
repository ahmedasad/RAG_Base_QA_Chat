from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common import by
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement


'''
    - function for reading url and fetch all the input fields in the html form tag
    - collect those fields in array or comma separated string
'''

def web_page_attributes(url):
    
    opts = Options()
    opts.add_argument("--headless=new")
    driver = webdriver.Chrome(opts)
    driver.get(url)

    print(driver.title)
    
    web_elements = [element for element in driver.find_elements(by=By.TAG_NAME, value="input") if element.get_attribute(
        'type') == 'password' or element.get_attribute('type') == 'text']

    # web_elements.extend([element for element in driver.find_elements(
    #     by=By.TAG_NAME, value="button") if element.get_attribute('type') == "submit"])

    elements = []
    for item in web_elements:
        elements.append(item.get_attribute('id'))

    driver.quit()
    
    return elements
    
