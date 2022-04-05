import requests
import re
from bs4 import BeautifulSoup

URL = "https://stackoverflow.com/jobs/companies"

def extract_last_page():

    result = requests.get(URL)
    soup = BeautifulSoup(result.text, "html.parser")
    pagination = soup.find("div", {"class": "s-pagination"}).find_all("a")
    pages = pagination[0:-1]
    last_page = pages[-1].find("span").get_text(strip=True)
    return int(last_page)


def extract_job(html):
    
    title = html.find("div", {"class": "flex--item fl1 text mb0"}).find("h2").find("a").string

    company, location = html.find("div", {"class": "flex--item fl1 text mb0"}).find_all("div", {"class": "flex--item fc-black-500 fs-body1"})
    company = company.get_text(strip=True)

    location = location.get_text(strip=True)

    # title을 소문자로 변경후, 모든 특수문자를 '-'로 변경하는 과정(link 형식에 따라)
    job_id_lst = re.sub(r"[^a-z0-9]", " ", title.lower()).split()
    job_id = '-'.join(job_id_lst)
    link = f"{URL}/{job_id}"

    return {
        "title": title,
        "company": company,
        "location": location,
        "link": link
        }

def extract_so_jobs(last_page):
    
    jobs = []
    for page in range(last_page):
        result = requests.get(f"{URL}?pg={page}")
        soup = BeautifulSoup(result.text, "html.parser")
        results = soup.find_all("div", {"class": "dismissable-company"})
        for job_result in results:
            job = extract_job(job_result)
            jobs.append(job)

    return jobs


def get_jobs():
    last_page = extract_last_page()
    jobs = extract_so_jobs(last_page)
    return jobs
