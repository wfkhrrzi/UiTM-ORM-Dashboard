import plotly
import requests
import pandas as pd
from env.config import BERTOPIC_HOST

def get_topic_info() -> pd.DataFrame:
    return pd.DataFrame.from_dict(requests.get(f"{BERTOPIC_HOST}/topic-info").json())

def get_all_topics():
    return requests.get(f"{BERTOPIC_HOST}/topics").json()

def get_topic_barchart() -> plotly.graph_objs.Figure:
    topic_barchart = requests.get(f"{BERTOPIC_HOST}/visualize-barchart").json()
    topic_barchart = plotly.io.from_json(topic_barchart)
    return topic_barchart

def get_dataset():
    return pd.read_csv('dataset/topic-labelled-20221226T173040-normalized-uitmRemoved-nr30.csv')

def get_ranked_topics() -> pd.DataFrame:
    df = get_dataset()
    topic_info = get_topic_info()
    ranked_topics_df = df.groupby(['Topic reassigned']).sum()[['RTs Count','Likes Count']].reset_index().rename(columns={"Topic reassigned":"Topic"})
    ranked_topics = pd.concat([topic_info.set_index('Topic'),ranked_topics_df.set_index('Topic')],axis=1,join='inner').reset_index().sort_values(by=['RTs Count'],ascending=False)
    ranked_topics = ranked_topics[ranked_topics['Topic'] != -1]
    return ranked_topics

def get_topics_over_time(topics: list) -> plotly.graph_objs.Figure:
    topic_over_time = requests.get(f"{BERTOPIC_HOST}/visualize-topics-over-time",params={'topics':topics}).json()
    topic_over_time = plotly.io.from_json(topic_over_time)
    return topic_over_time