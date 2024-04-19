import feedparser
import openai
import json

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
def analyze_market_sentiment(text):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "Analyze the sentiment and implications of this Bitcoin news article, and the result is returned in the form of 'state' and 'score' JSON"},
            {"role": "user", "content": text}
        ]
    )
    return response['choices'][0]['message']['content'].strip()




# OpenAI API 키 설정
openai.api_key = 'your-api_key'


# RSS 피드 URL 설정 (예제 URL입니다, 실제 사용가능한 URL로 교체 필요)
rss_url = 'https://cryptoslate.com/feed/'

# 뉴스 기사 가져오기
articles = fetch_news_from_rss(rss_url)
totalScore=0


# # 분석 결과 출력
for article in articles:
    print("Article Title:", article['title'])
    print("Link:", article['link'])
    market_analysis = analyze_market_sentiment(article['summary'])
    print("Market Sentiment Analysis:", market_analysis)

    #가중치 계산
    market_analysis = json.loads(market_analysis)
    totalScore = totalScore + market_analysis['score']



    print("---------------------------------------------------")

print("totalScore:",totalScore)