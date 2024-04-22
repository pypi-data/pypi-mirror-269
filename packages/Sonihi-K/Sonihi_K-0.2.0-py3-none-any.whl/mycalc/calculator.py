import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import webbrowser

def open_naver_sports_baseball_schedule():
    url = "https://sports.news.naver.com/schedule/scoreBoard.nhn?category=mlb&date=20220416"
    webbrowser.open(url)

open_naver_sports_baseball_schedule()

def open_naver_weather():
    url = "https://search.naver.com/search.naver?sm=top_hty&fbm=1&ie=utf8&query=오늘+날씨"
    webbrowser.open(url)

open_naver_weather()