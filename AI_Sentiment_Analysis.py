import streamlit as st
from transformers import pipeline
#from amazon_product_review_scraper import amazon_product_review_scraper  # Uncomment if you use this package

st.title("Product Review Sentiment Analyzer")

product_url = st.text_input("Enter Amazon product link:")

reviews = []

if product_url:
    # For Amazon, extract ASIN from URL (regex or string split)
    import re
    match = re.search(r"/dp/([A-Z0-9]{10})", product_url)
    if match:
        asin = match.group(1)
        # Use package for review scraping
        # scraper = amazon_product_review_scraper(amazon_site="amazon.in", product_asin=asin)
        # reviews_df = scraper.scrape()
        # reviews = reviews_df['review_text'].tolist()
        # For demonstration, fake reviews:
        reviews = [
            "Good value for money.",
            "Stopped working after a week.",
            "Excellent quality!",
            "Not worth the price.",
            "I am satisfied with this product."
        ]
    else:
        st.error("Could not extract ASIN from the link!")
else:
    st.info("Please enter a product link above.")

if reviews:
    sentiment_pipeline = pipeline("sentiment-analysis")
    results = sentiment_pipeline(reviews)
    counts = {"POSITIVE": 0, "NEGATIVE": 0, "NEUTRAL": 0}
    for r in results:
        label = r["label"].upper()
        if label in counts:
            counts[label] += 1
        else:
            counts["NEUTRAL"] += 1
    total = sum(counts.values())
    percentages = {label: round(count / total * 100, 2) for label, count in counts.items()}
    st.subheader("Sentiment Summary")
    st.write(percentages)
    st.bar_chart(percentages)
else:
    st.write("No reviews found yet.")
