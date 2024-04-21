import requests
from bs4 import BeautifulSoup


def get_html(url):
  """URL로부터 HTML을 가져오고, 에러 발생 시 에러 코드를 출력한다."""
  response = requests.get(url)
  if response.status_code == 200:
    return response.text
  else:
    print(f"Request Error: {response.status_code}")
    return None

def parse_html(html):
  """html을 파싱한다"""
  return BeautifulSoup(html, 'html.parser')
  
def extract_text(soup, selector):
  """특정 텍스트를 추출한다."""
  elements = soup.select(selector)
  text_list = []
  for element in elements:
     text = element.get_text()
     text_list.append(text)
  return text_list

def extract_links(soup):
  """모든 링크를 추출한다."""
  links = soup.find_all('a', href=True)
  extract_links = []
  for link in links:
    extract_links.append(link['href'])
  return extract_links
