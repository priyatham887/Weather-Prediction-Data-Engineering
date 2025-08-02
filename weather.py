import requests
from bs4 import BeautifulSoup
import pandas as pd
import sqlite3
import matplotlib.pyplot as plt


url = "https://weather.com/weather/today/l/772e009744e8daeb8736c08a36a6afcabd69ae3a1973390af86418232c2cbe14"

page = requests.get(url)

soup = BeautifulSoup(page.content, 'html.parser')

temp = soup.find('span', class_= 'CurrentConditions--tempValue--zUBSz' ).text
condition = soup.find('div', class_= 'CurrentConditions--phraseValue---VS-k').text

weather_data = {
    'timestamp' : pd.Timestamp.now(),
    'temperature' : temp,
    'condition' : condition
}

print(weather_data)

df = pd.DataFrame([weather_data])

df['temperature'] = df['temperature'].str.replace('°','').astype(int)

df['is_rainy'] = df['condition'].str.lower().str.contains('rain')

print(df)

conn = sqlite3.connect('weather.db')
df.to_sql('daily_weather', conn, if_exists='append', index=False)
conn.close()

conn = sqlite3.connect('weather.db')
df = pd.read_sql("SELECT * FROM daily_weather ORDER BY timestamp DESC LIMIT 7", conn)

plt.plot(df['timestamp'], df['temperature'])
plt.title('7-Day Temperature Trend')
plt.xlabel('Date')
plt.ylabel('Temperature (°F)')
plt.savefig('temperature_trend.png')





