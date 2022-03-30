import requests
from bs4 import BeautifulSoup

LIMIT = 100
URL = f"https://search.indeed.jobs/main/jobs?keywords=python&location=&page=1&limit={LIMIT}&sortBy=relevance"
#stackoverflow_URL = f"https://stackoverflow.com/questions/tagged/python?tab=newest&page=1&pagesize={LIMIT}"

def extract_indeed_pages():
    result = requests.get(URL)
    soup = BeautifulSoup(result.text, 'html.parser')

    pagination = soup.find("div", {"class": "pagination"})

    links = pagination.find_all('a')
    pages = []
    for link in links[:-1]:
        pages.append(int(link.string))

    max_page = pages[-1]
    return max_page

def extract_indeed_jobs(last_page):
    for page in range(last_page):
        requests.get(f"{URL}&start={page*LIMIT}")

