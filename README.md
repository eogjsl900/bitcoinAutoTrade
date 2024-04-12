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
