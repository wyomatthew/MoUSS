# Measurer Of University Subreddit Sentiment
The Measurer Of University Subreddit Sentiment, or MoUSS, (pronounced "mouse"),
is a tool that collects, analyzes, and compares the sentiment of posts in the
subreddits across various American universities. It was designed to fulfill
a final project requirement for Big Data Analytics (CIS 5450) in the Fall 2022
semester at the University of Pennsylvania.

## Authors
Imagined and designed by Tasneem Pathan, Christine Ngugi, and Matthew Pickering

## Modules
MoUSS is divided up into the following moduels:

### Rawr.py
Rawr.py is a wrapper around the Python Reddit API Wrapper (PRAW), hence called
the Reddit API Wrapper wRapper. It provides the Objects representing Subreddits,
Submissions, Comments, and Awards along with methods required to scrape each one.
