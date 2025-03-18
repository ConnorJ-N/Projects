# -*- coding: utf-8 -*-
"""
Created on Tue Feb 04 01:23:28 2025

@author: Connor
"""

import numpy as np
import pandas as pd
from transformers import AutoTokenizer, AutoModelForSequenceClassification, pipeline

"""df is in the form n*['date', 'Headline', 'Article']"""
df = pd.read_csv(r"C:\file.csv", encoding='cp1252')
main_body = df['Article']
headline = df['Headline']

def sentiment(body):
    
    tokenizer = AutoTokenizer.from_pretrained("ProsusAI/finbert")
    model = AutoModelForSequenceClassification.from_pretrained("ProsusAI/finbert")
    classifier = pipeline("text-classification", model=model, tokenizer=tokenizer)
    sentiment_result = classifier(body)
    return sentiment_result[0]['score']

sentiments = [sentiment(i) for i in headline]
avg_sentiment = np.average(sentiments)

def monte_carlo_price(sp0, strike, maturity, r, volatility, n_iters=1000, steps=252):
    step_size = maturity / steps
    pnl = []
    
    for i in range(n_iters):
        price_n = sp0
        for t in range(steps):
            Wt = np.random.normal()
            price_n *= np.exp((r-0.5*volatility**2)*step_size+volatility*np.sqrt(step_size)*Wt)
            
        pnl.append(max(price_n-strike, 0))
        
    options_price = np.exp(-r*maturity)*np.mean(pnl)
    return options_price

"""Option params"""
sp0 = 100  #price at t=0
strike = 105   #Strike price
maturity = 1.0   #maturity time
r = 0.05  #Treasury bond yield (risk free yield)
volatility = 0.15+(avg_sentiment*0.05)  # Use sentiment-adjusted volatility

price = monte_carlo_price(sp0, strike, maturity, r, avg_sentiment)

