import feedparser
import json
from openai import OpenAI


# RSS 피드에서 뉴스 기사 추출
def fetch_news_from_rss(rss_url):
    news_feed = feedparser.parse(rss_url)
    articles = []
    for entry in news_feed.entries:
        articles.append({
            'title': entry.title,
            'summary': entry.summary if hasattr(entry, 'summary') else 'No summary available',
            'link': entry.link
        })
    return articles

# ChatGPT 모델을 사용하여 시장 상황 분석
# gpt-3.5-turbo , gpt-4-turbo-preview 

def analyze_market_sentiment(text):

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "By analyzing news articles, predict future prospects of Bitcoin and enter one json value in summary and state format as the result. Write down the overall analysis in the summary and enter sell, buy, hold in state"},
            {"role": "user", "content": text}
        ],
        response_format={"type":"json_object"}
    )
    return response.choices[0].message.content




# OpenAI API 키 설정
client = OpenAI(api_key = 'your-api_key')


# RSS 피드 URL 설정 (예제 URL입니다, 실제 사용가능한 URL로 교체 필요)
rss_url = 'https://www.coinreaders.com/rss/rss_news.php'

# 뉴스 기사 가져오기
articles = fetch_news_from_rss(rss_url)

news=''


for index, article in enumerate(articles):
    if index < 10:  # 인덱스가 10 미만인 경우에만 실행
        news += '제목:' + article['title'] + '\n'
        news += '내용:' + article['summary'] + '\n\n'
    else:
        break  # 인덱스가 10에 도달하면 루프 중단



market_analysis = analyze_market_sentiment(news)
market_analysis = json.loads(market_analysis)


summary = market_analysis['summary']
state = market_analysis['state']

#print('summary: ',summary)
#print('state: ',state)
