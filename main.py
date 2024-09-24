import os
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import keyboard
import threading
import time


listings = "https://rit-csm.symplicity.com/students/app/career-fairs/c44d4e872414c27ed31d34e6d3767018/employers"

def check_quit(driver):
    while True:
        if keyboard.is_pressed("q"):
            driver.quit()

def get_data():
    response = requests.get(listings).text
    soup = BeautifulSoup(response, 'html.parser')

    print(soup)

def get_data_selenium():
    service = Service(executable_path="../../../../Program Files/chromedriver-win64/chromedriver.exe")
    driver = webdriver.Chrome(service=service)
    driver.get("https://rit-csm.symplicity.com/students/app/home")

    WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.ID, "ritUsername"))
    )

    input_element = driver.find_element(By.ID, "ritUsername")
    input_element.clear()
    input_element.send_keys(os.getenv("RIT_USERNAME"))

    thread = threading.Thread(target=check_quit(driver))
    thread.start()

    time.sleep(30)


def main():
    get_data_selenium()
    


if __name__ == "__main__":
    main()