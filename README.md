# Reddit Product Sentiment Analysis

This project allows users to **analyze Reddit sentiment for any product**. Enter a product name, and the app will:

- Search Reddit for relevant threads and posts
- Scrape comments and titles using `praw`
- Analyze sentiment using `TextBlob`
- Save structured results in a SQLite database
- Export summaries to CSV and plot a sentiment bar chart

---

## Features

- Automatic product thread search on Reddit
- Sentiment analysis on post + comment text
- Stores results in `reviews.db` using SQLModel
- CSV and bar chart export for comparisons
- Compare multiple products in one command
- Organizes all outputs in a `results/` folder

---

## Installation

1. **Clone the repo**

```bash
git clone https://github.com/zef-yeh/reddit-sentiment-analysis.git
cd reddit-sentiment-analysis
```

```bash
python -m venv venv
venv\Scripts\activate # On Windows
```

# or

```bash
source venv/bin/activate # On macOS/Linux
```

# Install Dependencies

```bash
pip install -r requirements.txt
python -m textblob.download_corpora
```

# Set up Reddit API credentials

- Go to https://www.reddit.com/prefs/apps
  - Create a new "script" app and get:
    - client_id
    - client_seceret
    - user_agent
- then create a file named .env in the directory, with contents:

```bash
REDDIT_CLIENT_ID=your_id
REDDIT_CLIENT_SECRET=your_secret
REDDIT_USER_AGENT=your_user_agent
```

## Usage

Analyze One or more products,

```bash
python app.py "product1_name" "product2_name", ... ""
```

- Each product gets its own \*\_summary.csv in results/
- Combined data is saved in results/combined_product_reviews.csv
- A sentiment bar chart is saved as results/product_sentiment_comparison.png

- To compare existing summaries without re-fetching data, run:

```bash
python compare_products.py
```
