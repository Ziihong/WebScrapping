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


def extract_job(html):

    # 각 모집공고 제목 가져오기
    title = html.find("div", {"class": "title"}).find("a")["title"]

    # 각 모집공고 회사명 가져오기
    company = html.find("span", {"class": "company"})
    company_anchor = company.find("a")
    if company_anchor is not None:
        company = str(company_anchor.string)
    else:
        company = str(company.string)
    company = company.strip()       

    # 각 모집공고 위치 가져오기
    location = html.find("div", {"class": "recJobLoc"})["data-rc-loc"]

    # 각 모집공고 지원링크 id 가져오기
    job_id = html["data-jk"]

    return {
        "title": title, 
        "company": company, 
        "location": location, 
        "link": f"https://www.indeed.com/viewjob?jk={job_id}"
        }  



def extract_indeed_jobs(last_page):
    
    jobs = []
    for page in range(last_page):
        result = requests.get(f"{URL}&start={page*LIMIT}")
        soup = BeautifulSoup(result.text, 'html.parser')
        results = soup.find_all("div", {"class" : "jobsearch-SerpJobCard"})
        for job_result in results:
            job = extract_job(job_result)
            jobs.append(job)
            
    return jobs

