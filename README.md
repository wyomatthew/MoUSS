# Measurer Of University Subreddit Sentiment
The Measurer Of University Subreddit Sentiment, or MoUSS,
is a tool that collects, analyzes, and compares the sentiment of posts in the
subreddits across various prestigious American universities. It was designed to
fulfill a final project requirement for Big Data Analytics (CIS 5450) in the
Fall 2022 semester at the University of Pennsylvania.


## Authors
Imagined and designed by Tasneem Pathan, Christine Ngugi, and Matthew Pickering.

## Project Overview
### Motivation
One of the most common questions on the University of Pennsylvania's subreddit
[r/upenn](https://www.reddit.com/r/upenn) from prospective applicants and
recently admitted students is, "Is UPenn really as bad is it seems?" The
question is a result of rather frequent rant and advice posts that seem to
communicate an overall feeling of hopelessness:
- [I feel so stupid](https://www.reddit.com/r/UPenn/comments/y9k6if/i_feel_so_stupid/)
- [Nonexistent Social Life](https://www.reddit.com/r/UPenn/comments/xeeonr/nonexistent_social_life/)
- [Unintelligent person here looking to vent...](https://www.reddit.com/r/UPenn/comments/vsgchz/unintelligent_person_here_looking_to_vent/)

Qualitatively, these posts are quite common, so prospetive members of the Penn
community are frequently prompted to question if these feelings are the norm.

### Research Question
We set out to answer exactlty the question set out above: "Is the culture of
a University's subreddit representative of the culture of that University itself?"
We seek to answer this question through three lenses:
1. Do the frequent topics of discussion on the subreddit represent the popular
   topics of the university itself?
2. Does similarity between a pair of universities' subreddits imply the
   universities themselves are similar?
3. Does the sentiment of a university's subreddit imply the university itself
   has worse mental health outcomes?

### Methods
The notebooks corresponding to each of the above questions are:
1. [Question 1](/notebooks/School_Happenings.ipynb)
2. [Question 2](/notebooks/school_similarity.ipynb)
3. [Question 3](/notebooks/Combined_Sentiment_Analysis.ipynb)

Note that all notebooks were originally built and ran in Google Colab, so 
it uses Google's Colab environment and is built upon mounting a particular
Google Drive for file access.

## Rawr.py
Rawr.py is a wrapper around the Python Reddit API Wrapper (PRAW), hence called
the Reddit API Wrapper wRapper. It contains all the code necessary to get the
used data from the schools used for study. It provides the Objects representing 
Subreddits, Submissions, Comments, and Awards along with methods required to 
scrape each one.
