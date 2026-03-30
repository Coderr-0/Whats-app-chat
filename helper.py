from urlextract import URLExtract
from wordcloud import WordCloud
import pandas as pd
from collections import Counter
import emoji

extractor = URLExtract()

from textblob import TextBlob

def sentiment_analysis(selected_user, df):

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    sentiments = []

    for message in df['message']:
        analysis = TextBlob(message)
        sentiments.append(analysis.sentiment.polarity)

    df['sentiment'] = sentiments

    return df
def fetch_stats(selected_user, df):

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    # number of messages
    num_messages = df.shape[0]

    # number of words
    words = []
    for message in df['message']:
        words.extend(message.split())

    # media messages
    num_media_messages = df[df['message'] == '<Media omitted>\n'].shape[0]

    # links
    links = []
    for message in df['message']:
        links.extend(extractor.find_urls(message))

    return num_messages, len(words), num_media_messages, len(links)


def monthly_timeline(selected_user, df):

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    timeline = df.groupby(['year', 'month_num', 'month']).count()['message'].reset_index()

    time = []
    for i in range(timeline.shape[0]):
        time.append(timeline['month'][i] + "-" + str(timeline['year'][i]))

    timeline['time'] = time

    return timeline


def daily_timeline(selected_user, df):

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    daily_timeline = df.groupby('only_date').count()['message'].reset_index()

    return daily_timeline


def week_activity_map(selected_user, df):

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    return df['day_name'].value_counts()


def month_activity_map(selected_user, df):

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    return df['month'].value_counts()


def activity_heatmap(selected_user, df):

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    user_heatmap = df.pivot_table(index='day_name', columns='period', values='message', aggfunc='count').fillna(0)

    return user_heatmap


def most_busy_users(df):
    x = df['user'].value_counts().head()
    df_percent = round((df['user'].value_counts() / df.shape[0]) * 100, 2).reset_index()
    return x, df_percent


def create_wordcloud(selected_user, df):

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    wc = WordCloud(width=500, height=500, min_font_size=10, background_color='white')
    df_wc = wc.generate(df['message'].str.cat(sep=" "))
    return df_wc


def most_common_words(selected_user, df):

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    words = []

    for message in df['message']:
        words.extend(message.lower().split())

    most_common_df = pd.DataFrame(Counter(words).most_common(20))
    return most_common_df


def emoji_helper(selected_user, df):

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    emojis = []

    for message in df['message']:
        emojis.extend([c for c in message if c in emoji.EMOJI_DATA])

    emoji_df = pd.DataFrame(Counter(emojis).most_common(len(Counter(emojis))))
    return emoji_df
def activity_heatmap(selected_user, df):

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    user_heatmap = df.pivot_table(
        index='day_name',
        columns='period',
        values='message',
        aggfunc='count'
    ).fillna(0)

    return user_heatmap
def prepare_features(df):

    df['msg_length'] = df['message'].apply(len)
    df['word_count'] = df['message'].apply(lambda x: len(x.split()))
    df['has_link'] = df['message'].apply(lambda x: 1 if 'http' in x else 0)
    df['has_media'] = df['message'].apply(lambda x: 1 if '<Media omitted>' in x else 0)

    return df
from textblob import TextBlob

def sentiment_analysis(selected_user, df):

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    df['sentiment'] = df['message'].apply(
        lambda x: TextBlob(str(x)).sentiment.polarity
    )

    return df
from sklearn.cluster import KMeans

def user_clustering(df):

    user_df = df.groupby('user').agg({
        'message': 'count',
        'msg_length': 'mean',
        'word_count': 'mean'
    }).reset_index()

    kmeans = KMeans(n_clusters=3)
    user_df['cluster'] = kmeans.fit_predict(user_df[['message','msg_length','word_count']])

    return user_df
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB

def train_message_classifier(df):

    # Dummy labels (you can improve later)
    df['label'] = df['message'].apply(lambda x: 'question' if '?' in x else 'statement')

    cv = CountVectorizer()
    X = cv.fit_transform(df['message'])
    y = df['label']

    model = MultinomialNB()
    model.fit(X, y)

    return model, cv
from sklearn.ensemble import RandomForestRegressor
import pandas as pd

def activity_prediction(df):

    # Remove invalid dates
    df = df.dropna(subset=['date'])

    # If no data left, return None
    if df.shape[0] == 0:
        return None

    # Convert date to ordinal
    df['day_num'] = df['date'].apply(lambda x: x.toordinal())

    # Count messages per day
    daily_msgs = df.groupby('day_num').size().reset_index(name='message_count')

    # If still empty
    if daily_msgs.shape[0] == 0:
        return None

    X = daily_msgs[['day_num']]
    y = daily_msgs['message_count']

    model = RandomForestRegressor()
    model.fit(X, y)

    return model, y

    return model
