from flask import Flask, render_template, request
from pattern.en import sentiment as pattern_sentiment
from googleapiclient.discovery import build
app = Flask(__name__)
API_KEY = 'AIzaSyDCQ7vn0EGWrLMnoDo5naxyD5UBOeVXQXI'
youtube = build('youtube', 'v3', developerKey=API_KEY)
@app.route('/', methods=['GET', 'POST'])
def sentiment_analysis():
    if request.method == 'POST':
        youtube_link = request.form['youtube_link']
        comments = extract_comments(youtube_link)
        sentiment_scores = perform_sentiment_analysis(comments)
        sentiment_counts = count_sentiments(sentiment_scores)
        return render_template('results.html', comments=comments, sentiment_scores=sentiment_scores, sentiment_counts=sentiment_counts)
    return render_template('index.html')

def perform_sentiment_analysis(comments):
    sentiment_scores = []
    for comment in comments:
        sentiment_score = pattern_sentiment(comment)[0]
        sentiment_scores.append(sentiment_score)
    return sentiment_scores

def count_sentiments(sentiment_scores):
    sentiment_counts = {
        'positive': 0,
        'negative': 0,
        'neutral': 0
    }
    for score in sentiment_scores:
        if score > 0:
            sentiment_counts['positive'] += 1
        elif score < 0:
            sentiment_counts['negative'] += 1
        else:
            sentiment_counts['neutral'] += 1
    return sentiment_counts

def extract_comments(youtube_link):
    video_id = extract_video_id(youtube_link)
    response = youtube.commentThreads().list(
        part='snippet',
        videoId=video_id,
        textFormat='plainText',
        maxResults=100 
    ).execute()

    comments = []
    for item in response['items']:
        comment = item['snippet']['topLevelComment']['snippet']['textDisplay']
        comments.append(comment)

    return comments

def extract_video_id(youtube_link):
    video_id = ''
    if 'youtube.com' in youtube_link:
        video_id = youtube_link.split('?v=')[1]
    elif 'youtu.be' in youtube_link:
        video_id = youtube_link.split('/')[-1]
    return video_id

if __name__ == '__main__':
    app.run(debug=True)

API_KEY = 'AIzaSyDCQ7vn0EGWrLMnoDo5naxyD5UBOeVXQXI'  

import nltk
nltk.download('wordnet')
