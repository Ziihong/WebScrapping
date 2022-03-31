import requests
from bs4 import BeautifulSoup

LIMIT = 100
URL = f"https://search.indeed.jobs/main/jobs?keywords=python&location=&page=1&limit={LIMIT}&sortBy=relevance"
#stackoverflow_URL = f"https://stackoverflow.com/questions/tagged/python?tab=newest&page=1&pagesize={LIMIT}"

def extract_indeed_pages():

    # indeed 사이트 pagination(=page numbering) 찾기
    result = requests.get(URL)
    soup = BeautifulSoup(result.text, 'html.parser')
    pagination = soup.find("div", {"class" : "pagination"})

    # 각 page로 이동하는 anchor 태그에서 페이지 수 찾기
    links = pagination.find_all('a')
    pages = []
    for link in links[:-1]:
        pages.append(int(link.string))

    last_page = pages[-1]
    return last_page


def extract_indeed_jobs(last_page):
    jobs = []

    # 페이지에서 각 title, company 가져오기
    for page in range(last_page):
        result = requests.get(f"{URL}&start={page*LIMIT}")
        soup = BeautifulSoup(result.text, 'html.parser')
        results = soup.find_all("div", {"class" : "jobsearch-SerpJobCard"})

        for job_result in results:
            title = job_result.find("div", {"class": "title"}).find("a")["title"]
            company = job_result.find("span", {"class": "company"})
            company_anchor = company.find("a")
            if company_anchor is not None:
                company = str(company_anchor.string)
            else:
                company = str(company.string)
            company = company.strip()         

    return jobs

