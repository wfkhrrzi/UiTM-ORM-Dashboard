import plotly
import requests
import pandas as pd
from env.config import BERTOPIC_HOST
import pickle
import json

def get_topic_info() -> pd.DataFrame:
    # return pd.DataFrame.from_dict(requests.get(f"{BERTOPIC_HOST}/topic-info").json())
    with open('dataset/topic-info.pkl', 'rb') as f:
        return pd.DataFrame.from_dict(pickle.load(f))

def get_all_topics():
    # return requests.get(f"{BERTOPIC_HOST}/topics").json()
    with open('dataset/topic-topics.json', 'r') as f:
        return json.load(f)

# def get_topic_barchart() -> plotly.graph_objs.Figure:
#     topic_barchart = requests.get(f"{BERTOPIC_HOST}/visualize-barchart").json()
#     topic_barchart = plotly.io.from_json(topic_barchart)
#     return topic_barchart

def get_dataset():
    return pd.read_csv('dataset/topic-labelled-20221226T173040-normalized-uitmRemoved-nr20.csv')

topic_info = get_topic_info()
df = get_dataset()

def get_ranked_topics() -> pd.DataFrame:
    # df = get_dataset()
    # topic_info = get_topic_info()
    ranked_topics_df = df.groupby(['Topic reassigned']).sum()[['RTs Count','Likes Count']].reset_index().rename(columns={"Topic reassigned":"Topic"})
    ranked_topics = pd.concat([topic_info.set_index('Topic'),ranked_topics_df.set_index('Topic')],axis=1,join='inner').reset_index().sort_values(by=['RTs Count'],ascending=False)
    ranked_topics = ranked_topics[(ranked_topics['Topic'] != -1)&(ranked_topics['Topic'] != 1)]
    return ranked_topics

ranked_topics = get_ranked_topics()

def get_topics_over_time(topics: list) -> plotly.graph_objs.Figure:

    with open('dataset/topic-over-time.pkl', 'rb') as f:
        topic_over_time = plotly.graph_objs.Figure(pickle.load(f))

    # topic_over_time = requests.get(f"{BERTOPIC_HOST}/visualize-topics-over-time",params={'topics':topics}).json()
    # topic_over_time = plotly.io.from_json(topic_over_time)
    
    topic_over_time=topic_over_time.to_dict()
    # topic_info = get_topic_info()
    
    #change topic name
    for i, data in enumerate(topic_over_time["data"]):
        topic_id = int(data['name'].split("_")[0])
        topic_over_time["data"][i]['name']=topic_info.query(f'Topic == {str(topic_id)}')['CustomName'].values[0]
    
    topic_over_time['layout']['legend']['title']['text'] = 'Topic' #change legend title

    return plotly.graph_objs.Figure(topic_over_time)