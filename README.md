# **Windows 인공지능 (Prophet) 자동매매 환경 설치 방법**

● 아나콘다(https://www.anaconda.com/) 설치

● Prophet이 3.9 부터 미지원으로 아나콘다 3.8 버전으로 설치

● pip install pyupbit

● pip install schedule

● conda install -c conda-forge prophet

● pip install pystan --upgrade



### **prophet라이브러리와 holidaysPython 라이브러리 간의 호환성 문제로 인해 오류가 발생할수 있음.**

● 호환되는 버전 설치 ->
pip install holidays==0.10.3

#



+  fig1 = model.plot(forecast)  최근 200시간 동안 데이터를 통계로 24시간뒤를 예측
![output](https://github.com/eogjsl900/bitcoinAutoTrade/assets/34729371/489e968b-02cf-45d4-abba-2694c398d13f)




+ fig2 = model.plot_components(forecast) 전체 trend 와  시간별 추세를 알 수있다.
![output2](https://github.com/eogjsl900/bitcoinAutoTrade/assets/34729371/aa48cb14-48ba-44af-a193-e44dbdca8fcd)



+ 위 그래프는 vscode에서 보는 방법은 
+ jupyter 확장설치 후 ctrl + shift +p  창에서 jupyter 대화형 창 만들기 창을 열어 pricePredict.py 코드를 실행해주면 된다.






# ** chatGPT openaiAPI를 활용하여 시장동향 파악하기**
+ openaiAPI.py 코드
+ RSS 피드를 이용하여 뉴스기사를 추출하고 openaiAPI에 추출한 내용을 넣어 JSON 형식으로 받아온다
+ ChatGPT 모델을 사용하여 시장 상황 분석


           def analyze_market_sentiment(text):
        
            response = openai.ChatCompletion.create(
            
                model="gpt-3.5-turbo",
                
                messages=[
                
                    {"role": "system", "content": "Analyze the sentiment and implications of this Bitcoin news article, and the result is returned in the form of 'state' and 'score' JSON"},
                    
                    {"role": "user", "content": text}
                    
                ]
                
            )
            
            return response['choices'][0]['message']['content'].strip()
    

+ JSON값은 "status" , "score"
+ status는 긍정 = "positive" , 부정 = "nagetive" , 중립 = "neutral"
+ score는 긍정일때 양수 부정일때 음수값이 들어가며 전체 점수의 합을 totalScore에 기록한다.

