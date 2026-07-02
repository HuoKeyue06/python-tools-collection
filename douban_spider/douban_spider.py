import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
movies = []
for page in range(0, 10):
  url = f'https://movie.douban.com/top250?start={page*25}'
  headers = { 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36' }
  print(f'正在爬取第{page+1}页数据...')
  try:
    response = requests.get(url, headers=headers,timeout=10)
    soup = BeautifulSoup(response.text, 'html.parser')
    items = soup.find_all('div', class_='item')
    for item in items:
      title = item.find('span', class_='title').text
      rating = item.find('span', class_='rating_num').text
      movies.append({'title': title, 'rating': rating})
    time.sleep(1)
  except Exception as e:
    print(f'爬取第{page+1}页数据时出错: {e}')
    break
df = pd.DataFrame(movies)
df.to_excel('douban_movies.xlsx', index=False)
print("豆瓣电影数据已保存到douban_movies.xlsx文件中")
