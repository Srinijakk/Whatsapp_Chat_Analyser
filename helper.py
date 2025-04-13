from urlextract import URLExtract
from wordcloud import WordCloud
from collections import Counter
import emoji
import pandas as pd
extractor = URLExtract()

def fetch_stats(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    num_messages = df.shape[0]

    words = []
    for message in df['message']:
        words.extend(message.split())

    num_media_messages = df[df['message'] == '<Media omitted>\n'].shape[0]

    links = []
    for message in df['message']:
        links.extend(extractor.find_urls(message))




    return num_messages, len(words), num_media_messages, len(links)

def most_busy_users(df):
    x = df['user'].value_counts().head()

    # Also return a DataFrame with percentages
    new_df = round((df['user'].value_counts() / df.shape[0]) * 100, 2).reset_index()
    new_df.columns = ['Name', 'Percent']

    return x, new_df

def create_wordcloud (selected_user, df):
     if selected_user != 'Overall':
        df =df[df['user'] == selected_user]
     wc = WordCloud (width=500,height=500,min_font_size=10, background_color='white')
     df_wc = wc.generate(df ['message'].str.cat (sep=" "))
     return df_wc

def emoji_helper(selected_user, df):
    if selected_user != 'Overall':
       df =df[df['user'] == selected_user]
    emojis = []

    for message in df['message']:
        emojis.extend([d['emoji'] for d in emoji.emoji_list(message)])

    emoji_df = pd.DataFrame(Counter(emojis).most_common(len(Counter(emojis))), columns=['emoji', 'count'])
    return emoji_df


def monthly_timeline(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    # Make sure the column 'message' exists before grouping
    if 'message' not in df.columns:
        raise KeyError("The 'message' column is missing from the DataFrame")

    # Group by year, month_num, and month, and count the number of messages
    timeline = df.groupby(['year', 'month_num', 'month']).size().reset_index(name='message_count')

    # Create a formatted 'time' column like "January-2022"
    timeline['time'] = timeline['month'] + "-" + timeline['year'].astype(str)

    return timeline

def daily_timeline(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    daily_timeline = df.groupby("only_date").count()['message'].reset_index()
    daily_timeline.rename(columns={'message': 'message_count'}, inplace=True)
    return daily_timeline

def week_activity_map(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    return df["day_name"].value_counts()

def month_activity_map(selected_user, df) :
    if selected_user != 'Overall':
        df = df[df [ 'user' ] == selected_user]
    return df[ 'month' ].value_counts()

def activity_heatmap(selected_user, df) :
    if selected_user != 'Overall' :
       df = df[df [ 'user' ] == selected_user]

    activity_heatmap = df.pivot_table(index='day_name', columns='period', values='message',aggfunc='count' ).fillna(0)
    return activity_heatmap