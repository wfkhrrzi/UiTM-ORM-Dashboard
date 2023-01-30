import pandas as pd
from datetime import datetime as dt
from pages.topics.topics_data import get_ranked_topics, get_dataset as topic_dataset, get_topic_info
import numpy as np

def get_dataset() -> pd.DataFrame:
    return pd.read_csv('dataset/labelled_pred_set_14-12-23.csv')
    # return pd.read_csv('dataset/final_dataset_cleaned_neutral_resetIndex.csv')

def get_processed_dataset():
    df = get_dataset()
    topic_df = topic_dataset()

    # required processes
    df = pd.merge(df,topic_df[['Tweet Id','Processed noisy tweet']],on='Tweet Id',how='left')
    df.dropna(inplace=True)

    return df

def get_sentiment_count() -> pd.DataFrame:
    df = get_dataset()
    df['Sentiment'] = df['Sentiment'].str.capitalize()
    sentiment_count = df['Sentiment'].value_counts().reset_index(drop=False).rename(columns={"index":"Sentiment","Sentiment":"Count"})
    return sentiment_count

def get_sentiment_over_time() -> pd.DataFrame:
    df = get_dataset()
    df['Timestamp'] = df['Timestamp'].apply(lambda x: dt.strptime(x,'%Y-%m-%d %H:%M:%S%z').strftime('%Y-%m'))
    sentiment_over_time = df.groupby(by=['Timestamp','Sentiment']).count()
    sentiment_over_time = sentiment_over_time[['Tweet Id']].reset_index().pivot(index='Timestamp', columns='Sentiment', values='Tweet Id')
    sentiment_over_time = sentiment_over_time.reset_index()
    return sentiment_over_time

def get_sentiment_by_topic() -> pd.DataFrame:
    topic_df = topic_dataset()
    df = get_dataset()

    # required processes
    topic_sentiment_df = pd.merge(df,topic_df[['Tweet Id','Topic reassigned']],on='Tweet Id',how='left')
    topic_sentiment_df.dropna(inplace=True)
    topic_sentiment_df['Topic reassigned'] = topic_sentiment_df['Topic reassigned'].astype(np.int64)
    topic_sentiment_df['Topic reassigned'].dtype
    topic_sentiment_df.rename(columns={'Topic reassigned':'Topic'},inplace=True)

    topic_sentiment_df = topic_sentiment_df.groupby(by=['Topic','Sentiment']).count()
    topic_sentiment_df = topic_sentiment_df[['Tweet Id']].reset_index().pivot(index='Topic', columns='Sentiment', values='Tweet Id')
    topic_sentiment_df = topic_sentiment_df.reset_index()
    
    topic_sentiment_df = topic_sentiment_df[topic_sentiment_df['Topic'] != -1]
    topic_sentiment_df['total'] = topic_sentiment_df['positive'] + topic_sentiment_df['neutral'] + topic_sentiment_df['negative']

    ranked_topics = get_ranked_topics()
    topic_sentiment_df = topic_sentiment_df.iloc[pd.Index(topic_sentiment_df['Topic']).get_indexer(ranked_topics[:10]['Topic'].tolist())]
    topic_name = ranked_topics[:10]['Name'].apply(lambda x: " ".join(x.split('_')[1:3]))
    topic_sentiment_df.insert(1,topic_name.name,topic_name)

    return topic_sentiment_df

def get_trending_topics():
    df = get_dataset()
    topic_df = topic_dataset()

    # merge processed tweet
    df = pd.merge(df,topic_df[['Tweet Id','Processed noisy tweet','Topic reassigned']],on='Tweet Id',how='left')
    df.dropna(inplace=True)
    
    topic_info = get_topic_info()
    trending_topics = df.groupby(by=['Sentiment','Topic reassigned']).count()[['RTs Count','Likes Count']].sort_values(by=['RTs Count','Likes Count'],ascending=False).reset_index()
    trending_topics = trending_topics[trending_topics['Topic reassigned']!=-1]
    topic_name = trending_topics['Topic reassigned'].apply(lambda x: topic_info['Name'][topic_info['Topic']==x].tolist()[0])
    trending_topics['Name'] = topic_name

    return trending_topics



