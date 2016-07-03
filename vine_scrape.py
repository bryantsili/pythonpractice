import requests 
import bs4
import re
import time
import csv
from selenium import webdriver


PAGINATED_URL = 'http://vineoftheday.com/?order_by=rating&thisPage='
paginated_urls = [PAGINATED_URL + str(i) for i in range(1, 2)]

# get_votd_urls :: [String]
def get_votd_urls():
	total_votd_urls = []
	for url in paginated_urls:
		response = requests.get(url)
		html = response.content
		soup = bs4.BeautifulSoup(html, "html.parser")
		row = soup.findAll('div', attrs={'class': 'col-lg-4 col-sm-4 col-xs-12 element yolo'})
		votd_urls = [div.a['href'] for div in row]
		# total_votd_urls :: [String]
		total_votd_urls = total_votd_urls + votd_urls
	print(total_votd_urls)
	return total_votd_urls

# get_vine_urls :: [String] -> [String]
def get_vine_urls(total_votd_urls):
	source_urls = []
	for url in total_votd_urls:
		response = requests.get(url)
		html = response.content
		soup = bs4.BeautifulSoup(html, "html.parser")
		try:
			panel = soup.find('a', text = 'Source')
			source_urls.append(panel['href'])
		except TypeError:
			pass
	print(source_urls)
	return source_urls
	

def get_account_urls(driver, vine_urls):
	BASE_URL = 'https://vine.co/'

	account_urls = []
	for url in vine_urls:
		driver.get(url)
		try:
			user_account = driver.find_element_by_css_selector('.username a').get_attribute('href')
			account_urls.append(user_account)
		except:
			pass
	print(account_urls)
	return account_urls

def followers(driver, account_urls):
	follower_boxes = []
	for url in account_urls:
		driver.get(url)
		time.sleep(2)
		followers = driver.find_element_by_css_selector('div.metic-count').get_attribute('textContent')
		follower_boxes.append(followers)	
	return follower_boxes

def get_description_boxes(driver, account_urls):
	description_boxes = []
	for url in account_urls:
		driver.get(url)
		time.sleep(2)
		description = driver.find_element_by_css_selector('div.timeline-header-content .description').get_attribute('textContent')
		description_boxes.append(description)
	return description_boxes

def extract_emails(description_boxes):
	emails = []
	for description in description_boxes:
		single_email = extract_email(description)
		emails.append(single_email)
	print(emails)
	return emails

def extract_email(description):
	match = re.search(r'\b[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,4}\b', description)
	if match:
		return match.group(0)

def run_program():
	try:
		driver = webdriver.PhantomJS()

		votd_urls = get_votd_urls()
		vine_urls = get_vine_urls(votd_urls)
		account_urls = get_account_urls(driver, vine_urls)
		description_boxes = get_description_boxes(driver, account_urls)
		emails = extract_emails(description_boxes)
		f = csv.writer(open("output.csv", "r"), delimiter=',')
		f.writerow(emails)
		return f

	finally:
		driver.quit()	



print(run_program())
