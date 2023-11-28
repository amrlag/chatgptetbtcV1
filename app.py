import streamlit as st
import openai
import os
from dotenv import load_dotenv
import requests


# Set your OpenAI API key here
#load_dotenv()
#openai.api_key = os.getenv("openai_api_key")

openai.api_key = openai.api_key = st.secrets["openai_api_key"]

def BasicGeneration(userPrompt):
    completion= openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "user", "content": userPrompt}
        ]
    )
    return completion.choices[0].message.content

st.title('Analyse du cours du BTC grâce à CHATGPT')
st.subheader(
    'ECONOMISE TES LARMES T EN AURA BESOIN POUR PLUS TARD ...')

def GetBitCoinPrices():
    # Define the API endpoint and query parameters
    url = "https://coinranking1.p.rapidapi.com/coin/Qwsogvtv82FCd/history"
    querystring = {
        "referenceCurrencyUuid": "yhjMzLPhuIDl",
        "timePeriod": "7d"
    }
    # Define the request headers with API key and host
    headers = {
        "X-RapidAPI-Key": "d1e9d1f689mshde3780b3a33e51dp18d382jsnecbc336ae076",
        "X-RapidAPI-Host": "coinranking1.p.rapidapi.com"
    }
    # Send a GET request to the API endpoint with query parameters and headers
    response = requests.request(
        "GET", url, headers=headers, params=querystring)
    # Parse the response data as a JSON object
    JSONResult = json.loads(response.text)
    # Extract the "history" field from the JSON response
    history = JSONResult["data"]["history"]
    # Extract the "price" field from each element in the "history" array and add to a list
    prices = []
    for change in history:
        prices.append(change["price"])
    # Join the list of prices into a comma-separated string
    pricesList = ','.join(prices)
    # Return the comma-separated string of prices
    return pricesList

def AnalyzeBitCoin(bitcoinPrices):
    chatGPTPrompt = f"""You are an expert crypto trader with more than 10 years of experience, 
    I will provide you with a list of bitcoin prices for the last 7 days
    can you provide me with a technical analysis
    of Bitcoin based on these prices. here is what I want: 
    Price Overview, 
    Moving Averages, 
    Relative Strength Index (RSI),
    Moving Average Convergence Divergence (MACD),
    Advice and Suggestion,
    Do I buy or sell?
    Please be as detailed as you can, and explain in a way any beginner can understand. and make sure to use headings
    Here is the price list: {bitcoinPrices}"""

    try:
        completion = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[

                {"role": "user", "content": chatGPTPrompt}
            ]
        )
        message = completion.choices[0].message.content.strip()
    except Exception as e:
        message = "Sorry, I was not able to process your request at this time. Please try again later."
    return message


if st.button('Analyze'):
    with st.spinner('Getting Bitcoin Prices...'):
        bitcoinPrices = GetBitCoinPrices()
        st.success('Done!')
    with st.spinner('Analyzing Bitcoin Prices...'):
        analysis = AnalyzeBitCoin(bitcoinPrices)
        st.text_area("Analysis", analysis,
                     height=500, max_chars=None, key=None,)
        st.success('Done!')
