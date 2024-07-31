"""
File: web_crawler_avg.py
Name: Leonie
--------------------------
This file demonstrates how to get
averages on www.imdb.com/chart/top
Do you know the average score of 250 movies?
Let's use Python code to find out the answer
"""

import requests 
from bs4 import BeautifulSoup


def main():
	url = 'http://www.imdb.com/chart/top'
	header = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36(KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36"}
	response = requests.get(url, headers=header)
	html = response.text
	soup = BeautifulSoup(html)
  
	tags = soup.find_all('span', {'class': 'ipc-rating-star ipc-rating-star--base ipc-rating-star--imdb ratingGroup--imdb-rating'})
	# print(tags)
	counter, total = 0, 0
	for tag in tags:
		counter += 1
		target = tag['aria-label']  # aria-label's value is a variable
		print(target)  # IMDb rating: 8.8
		score = float(target.split()[2])
		total += score
	print(f"The Avg of {counter} Movies: {total/counter}")


if __name__ == '__main__':
	main()
