"""
File: web_crawler_avg.py
Name:
--------------------------
This file demonstrates how to get
averages on www.imdb.com/chart/top
Do you know the average score of 250 movies?
Let's use Python code to find out the answer
"""

import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException


def main():
    driver = webdriver.Chrome()

    # Open the dynamic webpage
    driver.get('http://www.imdb.com/chart/top')

    # Wait for the page to load completely
    # Use explicit waits to wait for a specific element to be present
    try:
        element_present = EC.presence_of_element_located((By.ID, 'specific-element-id'))
        WebDriverWait(driver, 5).until(element_present)
    except TimeoutException:
        print("Timed out waiting for page to load")

    # Get the entire HTML content of the page
    html_content = driver.page_source

    soup = BeautifulSoup(html_content)
    tags = soup.find_all('span', {
        'class': 'ipc-rating-star ipc-rating-star--base ipc-rating-star--imdb ratingGroup--imdb-rating'})
    counter, total = 0, 0
    for tag in tags:
        counter += 1
        target = tag['aria-label']
        print(target)  # IMDb rating: 8.8
        score = float(target.split()[2])
        total += score
    print(f"The Avg of {counter} Movies: {total / counter}")


if __name__ == '__main__':
    main()
