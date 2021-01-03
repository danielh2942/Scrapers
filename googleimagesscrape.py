from selenium import webdriver
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from datetime import datetime
from PIL import Image
from io import BytesIO
import re
import shutil
import requests
import time
import os
import base64

directory = "src"
query = input("What would you like to search? ")
query.replace(" ", "+")
url = 'https://www.google.com/search?q='+str(query)
url = url + '&source=lnms&tbm=isch&sa=X&ved=2ahUKEwie44_AnqLpAhUhBWMBHUFGD90Q_'
url = url + 'AUoAXoECBUQAw&biw=1920&bih=947'
qty = int(input("How many pictures? "))
# Timestring so queries can be run more than once without conflict
runtime = datetime.now().strftime("%Y%m%d%H%M%S")
# run headless
options = FirefoxOptions()
options.add_argument("--headless")
driver = webdriver.Firefox(options=options)


def save_img(inp, img, i):
    try:
        filename = runtime + "_" + inp + "_" + str(i)+".jpg"
        image_path = os.path.join(os.getcwd(), directory, filename)
        if (img.startswith("http")):
            image = requests.get(img, stream=True)

            with open(image_path, "wb") as file:
                shutil.copyfileobj(image.raw, file)
        else:
            # Google sometimes stores images in base64 strings, this deals with
            # that
            print("Base64 image (lower res, Sorry!)")
            img = re.sub('^data:image/.+;base64,', '', img)
            byte_data = base64.b64decode(img)
            img_data = BytesIO(byte_data)
            imgfile = Image.open(img_data)
            imgfile.save(image_path, "jpeg")
    except Exception:
        print("Image failed to save!")
        pass


def scrape_images(input, url, driver, quantity):
    try:
        driver.get(url)
        time.sleep(3)
        for j in range(1, quantity+1):
            print("Downloading image: %d" % (j))
            imgurl = driver.find_element_by_xpath('//div//div//div//div//div//div//div//div//div//div['+str(j)+']//a[1]//div[1]//img[1]')
            imgurl.click()
            time.sleep(5)
            # n3VNCb
            # //body/div[2]/c-wiz/div[3]/div[2]/div[3]/div/div/div[3]/div[2]/c-wiz/div[1]/div[1]/div/div[2]/a/img
            img = driver.find_element_by_xpath("//body/div[2]/c-wiz/.//img[contains(@class, 'n3VNCb')]").get_attribute("src")
            save_img(input, img, j)
    except Exception as e:
        print("Could not scrape")
        print(str(e))


scrape_images(query, url, driver, qty)
driver.close()
