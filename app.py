from dotenv import load_dotenv
import os 
from langchain_core.tools import tool
import math
import requests
import yfinance as yf
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.agents import initialize_agent , AgentType
import streamlit as st







load_dotenv()


GOOGLE_API_KEY = os.environ.get('GOOGLE_API_KEY')



@tool
def calculator(expression):
  "this is calculator for evaluate any math expression"
  def add(a: float, b: float) -> float:
      """
      Adds two numbers and returns the result.

      Args:
          a (float): The first number.
          b (float): The second number.

      Returns:
          float: The sum of `a` and `b`.

      Examples:
          >>> add(3, 5)
          8
      """
      return a + b


  def subtract(a: float, b: float) -> float:
      """
      Subtracts the second number from the first and returns the result.

      Args:
          a (float): The first number.
          b (float): The second number.

      Returns:
          float: The difference of `a` and `b`.

      Examples:
          >>> subtract(10, 4)
          6
      """
      return a - b


  def multiply(a: float, b: float) -> float:
      """
      Multiplies two numbers and returns the result.

      Args:
          a (float): The first number.
          b (float): The second number.

      Returns:
          float: The product of `a` and `b`.

      Examples:
          >>> multiply(2, 3)
          6
      """
      return a * b


  def divide(a: float, b: float) -> float:
      """
      Divides the first number by the second and returns the result.

      Args:
          a (float): The numerator.
          b (float): The denominator.

      Returns:
          float: The quotient of `a` and `b`.

      Raises:
          ValueError: If `b` is zero.

      Examples:
          >>> divide(10, 2)
          5.0
      """
      if b == 0:
          raise ValueError("Division by zero is not allowed.")
      return a / b


  def power(base: float, exponent: float) -> float:
      """
      Raises a number to a specified power.

      Args:
          base (float): The base number.
          exponent (float): The exponent.

      Returns:
          float: `base` raised to the power of `exponent`.

      Examples:
          >>> power(2, 3)
          8
      """
      return math.pow(base, exponent)


  def square_root(number: float) -> float:
      """
      Calculates the square root of a number.

      Args:
          number (float): The number to find the square root of.

      Returns:
          float: The square root of `number`.

      Raises:
          ValueError: If `number` is negative.

      Examples:
          >>> square_root(16)
          4.0
      """
      if number < 0:
          raise ValueError("Cannot calculate the square root of a negative number.")
      return math.sqrt(number)


  def calculator():
      """
      A simple calculator that lets users perform basic math operations.
      """
      print("Welcome to the Calculator!")
      print("Operations:")
      print("1. Addition (+)")
      print("2. Subtraction (-)")
      print("3. Multiplication (*)")
      print("4. Division (/)")
      print("5. Power (^)")
      print("6. Square Root (√)")
      print("Type 'exit' to quit.")

      while True:
          operation = input("\nEnter the operation you want to perform: ").strip().lower()

          if operation == "exit":
              print("Thank you for using the Calculator. Goodbye!")
              break

          try:
              if operation in ['+', '1', 'addition']:
                  a = float(input("Enter the first number: "))
                  b = float(input("Enter the second number: "))
                  print(f"Result: {add(a, b)}")

              elif operation in ['-', '2', 'subtraction']:
                  a = float(input("Enter the first number: "))
                  b = float(input("Enter the second number: "))
                  print(f"Result: {subtract(a, b)}")

              elif operation in ['*', '3', 'multiplication']:
                  a = float(input("Enter the first number: "))
                  b = float(input("Enter the second number: "))
                  print(f"Result: {multiply(a, b)}")

              elif operation in ['/', '4', 'division']:
                  a = float(input("Enter the numerator: "))
                  b = float(input("Enter the denominator: "))
                  print(f"Result: {divide(a, b)}")

              elif operation in ['^', '5', 'power']:
                  base = float(input("Enter the base number: "))
                  exponent = float(input("Enter the exponent: "))
                  print(f"Result: {power(base, exponent)}")

              elif operation in ['√', '6', 'square root']:
                  number = float(input("Enter the number: "))
                  print(f"Result: {square_root(number)}")

              else:
                  print("Invalid operation. Please try again.")
          except ValueError as e:
              print(f"Error: {e}")














@tool
def news(api_key = "39f54e1bc5cd444d960059aa227a0b77", country='us', category=None):
    """
    Fetches the latest news headlines from a specified country and category using the NewsAPI.

    Parameters:
        api_key (str): Your API key for accessing the NewsAPI.
        country (str): The country code for the news (default is 'us').
                      Example: 'us' for United States, 'in' for India.
        category (str): The news category to filter by (default is None).
                        Example categories: 'business', 'entertainment', 'general', 'health', 'science', 'sports', 'technology'.

    Returns:
        dict: A dictionary containing the status, total results, and a list of articles.
              Each article includes keys like 'source', 'author', 'title', 'description', 'url', 'publishedAt', etc.

    Raises:
        ValueError: If the API response indicates an error or invalid parameters.

    Example:
        >>> api_key = 'api_ley'
        >>> headlines = news(api_key, country='us', category='technology')
        >>> for article in headlines['articles']:
        ...     print(article['title'])
    """
    url = "https://newsapi.org/v2/top-headlines"
    params = {
        'apiKey': api_key,
        'country': country,
        'category': category
    }

    response = requests.get(url, params=params)
    data = response.json()

    if response.status_code != 200 or data.get('status') != 'ok':
        raise ValueError(f"Error fetching news: {data.get('message', 'Unknown error')}")

    return data

@tool
def get_stock_price(stock_symbol: str) -> str:
    """
    Function to fetch the latest stock price using Yahoo Finance.

    Parameters:
    stock_symbol (str): The symbol of the stock whose price needs to be fetched (e.g., 'AAPL' for Apple, 'TSLA' for Tesla).

    Returns:
    str: The latest stock price or an error message if the stock cannot be found.

    Example:
    >>> get_stock_price("AAPL")
    "The latest price for AAPL is $175.30."
    """
    print("function is called")

    try:
        # Fetch stock data using Yahoo Finance
        stock = yf.Ticker(stock_symbol)
        stock_info = stock.history(period="1d")  # Get the most recent stock price

        if stock_info.empty:
            return f"Error: No data available for stock symbol {stock_symbol}."

        # Extract the latest closing price
        latest_price = stock_info['Close'].iloc[0]

        # Format the result
        return f"The latest price for {stock_symbol} is ${latest_price:.2f}."

    except Exception as e:
        return f"Error fetching stock price: {str(e)}"


tools = [calculator , news , get_stock_price]

llm = ChatGoogleGenerativeAI(model = "gemini-2.0-flash-exp" , api_key = GOOGLE_API_KEY)

# response = llm.invoke("what is 3 times 2?")#The invoke() method sends the prepared input to the LLM for processing.
# response.content

agent = initialize_agent(tools , llm , agent = AgentType.STRUCTURED_CHAT_ZERO_SHOT_REACT_DESCRIPTION )

# response = agent.invoke("what is 3 times 3?")
# print(response["output"])

st.title("Gemini Tool calling Agent✨")
st.write("👋 Welcome to my Gemini Tool Calling Agent! 🚀")
st.write("💡 Your go-to assistant for all your AI needs. Let's get started! 💻")
user_input = st.text_input("📝Enter your prompt")


if st.button("Submit✨"):
    respose = agent.invoke(user_input)
    st.write(respose["output"])

# Simple agent logic (you can customize this)
if user_input:
    # For simplicity, we'll respond based on keywords in the user input.
    if 'Assalam o alikum' and 'hello' in user_input.lower().strip():
        response = "👋Walikum assalm✨! How can I assist you today?"
    elif 'help' in user_input.lower():
        response = "💡 Sure! What do you need help with?"
    elif 'bye' in user_input.lower():
        response = "👋 Goodbye! See you again soon."
    else:
        response = f"🔍 I'm processing your request: '{user_input}'... Stay tuned!"
    
    # Display the agent's response
    st.write(response)    