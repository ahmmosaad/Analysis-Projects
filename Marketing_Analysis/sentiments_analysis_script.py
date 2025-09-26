import pandas as pd
import pyodbc as dbc
import nltk as nl
from nltk.sentiment import SentimentIntensityAnalyzer


def get_data_from_sql():

    conn_str = (
        "Driver={SQL Server};"  # Specify the driver for SQL Server
        "Server=.;"  # Specify your SQL Server instance
        "Database=MarketingAnalytics;"  # Specify the database name
        "Trusted_Connection=yes;"  # Use Windows Authentication for the connection
    )

    connect = dbc.connect(conn_str)
    query = "SELECT ReviewID, CustomerID, ProductID, ReviewDate, Rating, ReviewText FROM customer_reviews"
    table = pd.read_sql( query,connect)
    
    return table


customer_rview = get_data_from_sql()

sia = SentimentIntensityAnalyzer()

def calculate_sentiment(review):
    analysis = sia.polarity_scores(review)
    return analysis["compound"]

# Define a function to categorize sentiment using both the sentiment score and the review rating
def categorize_sentiment(score, rating):
    # Use both the text sentiment score and the numerical rating to determine sentiment category
    if score > 0.05:  # Positive sentiment score
        if rating >= 4:
            return 'Positive'  # High rating and positive sentiment
        elif rating == 3:
            return 'Mixed Positive'  # Neutral rating but positive sentiment
        else:
            return 'Mixed Negative'  # Low rating but positive sentiment
    elif score < -0.05:  # Negative sentiment score
        if rating <= 2:
            return 'Negative'  # Low rating and negative sentiment
        elif rating == 3:
            return 'Mixed Negative'  # Neutral rating but negative sentiment
        else:
            return 'Mixed Positive'  # High rating but negative sentiment
    else:  # Neutral sentiment score
        if rating >= 4:
            return 'Positive'  # High rating with neutral sentiment
        elif rating <= 2:
            return 'Negative'  # Low rating with neutral sentiment
        else:
            return 'Neutral'

def sentiment_bucket(score):

    if score >= 0.5:
        return '0.5 to 1.0'  # Strongly positive sentiment
    elif 0.0 <= score < 0.5:
        return '0.0 to 0.49'  # Mildly positive sentiment
    elif -0.5 <= score < 0.0:
        return '-0.49 to 0.0'  # Mildly negative sentiment
    else:
        return '-1.0 to -0.5' 
    


customer_rview['SentimentScore'] = customer_rview['ReviewText'].apply(calculate_sentiment)

# Apply sentiment categorization using both text and rating
customer_rview['SentimentCategory'] = customer_rview.apply(
    lambda row: categorize_sentiment(row['SentimentScore'], row['Rating']), axis=1)

# Apply sentiment bucketing to categorize scores into defined ranges
customer_rview['SentimentBucket'] = customer_rview['SentimentScore'].apply(sentiment_bucket)

customer_rview.to_csv('customer_reviews_with_sentiment.csv', index=False)