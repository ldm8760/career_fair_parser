import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import time


listings = "https://rit-csm.symplicity.com/students/app/career-fairs/c44d4e872414c27ed31d34e6d3767018/employers"

def get_data():
    response = requests.get(listings).text
    soup = BeautifulSoup(response, 'html.parser')

    print(soup)

def get_data_selenium():
    service = Service(executable_path="../../../../Program Files/chromedriver-win64/chromedriver.exe")
    driver = webdriver.Chrome(service=service)
    driver.get("https://rit-csm.symplicity.com/students/app/home")
    time.sleep(10)
    driver.quit()


def main():
    get_data_selenium()
    


if __name__ == "__main__":
    main()