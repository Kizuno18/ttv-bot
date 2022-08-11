import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
import pickle

def SpawnBot(settings):
    chrome_options = uc.ChromeOptions()
    chrome_options.add_argument("--mute-audio")
    driver = uc.Chrome(options=chrome_options)
    driver.get("https://www.twitch.tv/")


    # log in
    cookie_loaded = pickle.load(open("tools/gruthekiller.dump","rb"))
    for part in cookie_loaded:
        if 'sameSite' in part:
            if part["sameSite"] == "None":
                part["sameSite"] = "Strict"
            driver.add_cookie(part)
    
    time.sleep(1)
    driver.refresh()


    search_box = driver.find_element(By.XPATH,"/html/body/div[1]/div/div[2]/nav/div/div[2]/div/div/div/div/div[1]/div/div/div/input")

    search_box.send_keys(settings["streamer"])
    search_box.send_keys(Keys.ENTER)

    time.sleep(2)

    elements = driver.find_elements(By.TAG_NAME,"a")

    for element in elements:
        if element.text == settings["streamer"]:
            element.click()
            break
    
    
    time.sleep(3)

    driver.execute_script("document.getElementsByClassName('persistent-player')[0].style='';")


    while True:
        time.sleep(10)