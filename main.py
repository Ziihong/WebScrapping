import requests

indeed_result = requests.get("https://search.indeed.jobs/main/jobs?keywords=python&location=&limit=100&page=1")

# indeed_result.text: html 전부 가져오기
print(indeed_result.text)
