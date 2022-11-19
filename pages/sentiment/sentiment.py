from datetime import datetime
import dash
from dash import dcc, html, callback, ALL, callback_context as ctx
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
import dash_bootstrap_components as dbc
from wordcloud import WordCloud
from pages.sentiment.sentiment_data import get_dataset, get_processed_dataset, get_sentiment_by_topic, get_sentiment_count, get_sentiment_over_time, get_trending_topics
from layout.utils import title_chart
import plotly.express as px
import plotly.graph_objs as go


df = get_dataset()
processed_df = get_processed_dataset()
trending_topics = get_trending_topics()

sentiment_count = get_sentiment_count()
sentiment_count_fig = px.pie(sentiment_count,values='Count',names='Sentiment',hole=.5,)
sentiment_count_fig.update_traces(
    hoverinfo='label+value', 
    textinfo='label+percent',
    marker=dict(
        colors=['#00ba7c','#ea3b30','#ef8823',],
    ),
    insidetextfont=dict(
        family = 'Roboto, sans-serif',
        size = 13,
        color = '#f4f4f4'
    ),
)
sentiment_count_fig.update_layout({
    "margin":dict(
        l=20,
        r=20,
        b=50,
        t=50,
        pad=10
    ),
    "legend":dict(
        orientation="h",
        font_color="#f4f4f4",
        yanchor="bottom",
        y=1.10,
        xanchor="center",
        x=0.5
    ),
    "paper_bgcolor":'rgba(0,0,0,0)',
    "plot_bgcolor":'rgba(0,0,0,0)',
})

sentiment_over_time = get_sentiment_over_time()

topic_sentiment_df = get_sentiment_by_topic()

layout = dbc.Container(
    [
        # first layer
        dbc.Row(
            [
                # trending topics
                dbc.Col(
                    [
                        title_chart('sentiment count'),
                        html.Div(
                            dcc.Graph(
                                figure=sentiment_count_fig
                            )
                        ),
                    ],
                    width=12,
                    lg=6,
                    md=6,
                    xl=3,
                    class_name="mb-3 mb-lg-0",
                ),
                # sentiment over time
                dbc.Col(
                    [
                        title_chart('sentiment over time'),                           
                        dcc.Graph(
                            figure=go.Figure({
                                "data":[
                                    {'x': sentiment_over_time['Timestamp'].tolist(), 'y': sentiment_over_time['positive'].tolist(),'type': 'scatter', 'name': 'Positive','marker_color':'#00ba7c','mode':'lines',},
                                    {'x': sentiment_over_time['Timestamp'].tolist(), 'y': sentiment_over_time['neutral'].tolist(),'type': 'scatter', 'name': 'Neutral','marker_color':'#ef8823','mode':'lines',},
                                    {'x': sentiment_over_time['Timestamp'].tolist(), 'y': sentiment_over_time['negative'].tolist(),'type': 'scatter', 'name': 'Negative','marker_color':'#ea3b30','mode':'lines',},
                                ],
                                "layout":{
                                #     # "width":600,
                                #     # "autosize":False,
                                    "margin":dict(
                                        l=20,
                                        r=20,
                                        b=50,
                                        t=50,
                                        pad=10
                                    ),
                                    "legend":dict(
                                        orientation="h",
                                        font_color="#f4f4f4",
                                        yanchor="bottom",
                                        y=1.07,
                                        xanchor="center",
                                        x=0.5
                                    ),
                                #     # "xaxis_title":"Topics",
                                #     # "yaxis_title":"Count",
                                    "yaxis_tickfont":dict(
                                        family = 'Roboto, sans-serif',
                                        size = 13,
                                        color = '#f4f4f4'
                                    ),
                                    "xaxis_tickfont":dict(
                                        family = 'Roboto, sans-serif',
                                        size = 13,
                                        color = '#f4f4f4'
                                    ),
                                    "yaxis_gridcolor":"#212529",
                                    "yaxis_gridwidth":0.5,
                                    "yaxis_zeroline":True,
                                    "yaxis_zerolinecolor":'#212529',
                                    "yaxis_zerolinewidth":1.5,
                                    "xaxis_gridcolor":"#212529",
                                    "xaxis_gridwidth":0.5,
                                    "paper_bgcolor":'rgba(0,0,0,0)',
                                    "plot_bgcolor":'rgba(0,0,0,0)',
                                }
                            })
                        )
                    ],
                    width=12,
                    lg=6,
                    md=6,
                    xl=4,
                    class_name="mb-3 mb-lg-0",
                ),
                # sentiment by topic
                dbc.Col(
                    [                        
                        dbc.Row(
                            dbc.Col(
                                [
                                    title_chart('sentiment by topic'),
                                    dcc.Graph(
                                        figure=go.Figure(data=
                                            [
                                                {'y': topic_sentiment_df['Name'], 'x': [(x/t)*100 for x,t in zip(topic_sentiment_df['positive'],topic_sentiment_df['total'])],'type': 'bar', 'name': 'Positive','marker_color':'#00ba7c','orientation':'h'},
                                                {'y': topic_sentiment_df['Name'], 'x': [(x/t)*100 for x,t in zip(topic_sentiment_df['neutral'],topic_sentiment_df['total'])],'type': 'bar', 'name': 'Neutral','marker_color':'#ef8823','orientation':'h'},
                                                {'y': topic_sentiment_df['Name'], 'x': [(x/t)*100 for x,t in zip(topic_sentiment_df['negative'],topic_sentiment_df['total'])],'type': 'bar', 'name': 'Negative','marker_color':'#ea3b30','orientation':'h'},
                                            ],
                                            layout={
                                                'barmode':'stack',
                                                "paper_bgcolor":'rgba(0,0,0,0)',
                                                "plot_bgcolor":'rgba(0,0,0,0)',
                                                "yaxis_tickfont":dict(
                                                    family = 'Roboto, sans-serif',
                                                    size = 13,
                                                    color = '#f4f4f4'
                                                ),
                                                "xaxis_tickfont":dict(
                                                    family = 'Roboto, sans-serif',
                                                    size = 13,
                                                    color = '#f4f4f4'
                                                ),
                                                "legend":dict(
                                                    orientation="h",
                                                    font_color="#f4f4f4",
                                                    yanchor="bottom",
                                                    y=1.07,
                                                    xanchor="center",
                                                    x=0.5
                                                ),
                                                "margin":dict(
                                                    l=20,
                                                    r=20,
                                                    b=50,
                                                    t=50,
                                                    pad=10
                                                ),
                                            }
                                        ),
                                    )     
                                ]
                            )
                        ) 
                                       
                    ],
                    width=12,
                    lg=12,
                    md=12,
                    xl=5,
                ),
            ]
        ),
        html.Hr(),
        # second layer 
        dcc.Store(id='store-selected-sentiment'),
        dbc.Row(
            [
                # sentiment buttons
                dbc.Col(
                    [
                        dbc.Button("positive",id={'type':'sentiment-button','sentiment':'positive'},class_name="mx-3", color="success"),
                        dbc.Button("neutral",id={'type':'sentiment-button','sentiment':'neutral'},class_name="mx-3", color="warning"),
                        dbc.Button("negative",id={'type':'sentiment-button','sentiment':'negative'},class_name="mx-3", color="danger"),
                    ]
                ),
            ],
            class_name="text-center mb-3"
        ),
        # third layer
        dbc.Row(
            [
                # trending topics
                dbc.Col(
                    [
                        title_chart("trending topics"),
                                            
                        html.Div(
                            id = "sentiment-trending-topics",
                        )
                    ],
                    width=12,
                    lg=6,
                    md=6,
                    xl=2,
                    class_name="mb-3 mb-lg-0",
                ),
                # word cloud
                dbc.Col(
                    [
                        html.Div([
                            title_chart('word cloud'),
                            dcc.Graph(id='sentiment-wordcloud')
                        ])
                    ],
                    width=12,
                    lg=6,
                    md=6,
                    xl=5,
                ),
                # top tweets
                dbc.Col(
                    [
                        html.Div([
                            title_chart('top tweets'),
                            html.Div(id="sentiment-top-tweets",style={"overflow-y":"scroll","max-height":"400px"}),
                        ]),
                    ],
                    width=12,
                    lg=6,
                    md=6,
                    xl=5,
                ),
            ]
        ),
    ],
    fluid=True
)

@callback(
    Output("store-selected-sentiment","data"),
    Input({
        "type":"sentiment-button",
        "sentiment":ALL,
    },'n_clicks'),    
    State("store-selected-sentiment","data"),
)
def update_store_selected_topic(args,data,):
    if not ctx.triggered_id or not any(args):
        if data is None:
            sentiment = "positive"
        else:            
            raise PreventUpdate
    else:
        sentiment = ctx.triggered_id['sentiment']
    
    return {
        "sentiment":sentiment,
    }

@callback(
    Output('sentiment-wordcloud','figure'),
    Input('store-selected-sentiment','data'),
)
def generate_wordcloud(data):

    # instantiate wordcloud
    wordcloud = WordCloud(
        background_color='rgba(0,0,0,0)',
        min_font_size=8,
        scale=2.5,
        collocations=True,
        # regexp=r"[a-zA-z#&]+",
        # max_words=200,
        min_word_length=4,
        # font_path='storage/fonts/Arial-Unicode.ttf',
        # collocation_threshold=3,
    )

    # generate image
    wordcloud_text = " ".join(str(text) for text in processed_df[processed_df['Sentiment'] == data['sentiment']]["Processed noisy tweet"])
    wordcloud_image = wordcloud.generate(wordcloud_text)
    wordcloud_image = wordcloud_image.to_array()
    
    fig = px.imshow(wordcloud_image)
    fig.update_layout(
        xaxis={'visible': False},
        yaxis={'visible': False},
        margin={'t': 0, 'b': 0, 'l': 0, 'r': 0},
        hovermode=False,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
    )
    return fig

@callback(
    Output('sentiment-trending-topics','children'),
    Input('store-selected-sentiment','data'),
)
def generate_trending_topics(data):
    trending_topics_list = trending_topics[trending_topics['Sentiment']==data['sentiment']][:10]
    display_trending_topics = [
        html.Div(
            [
                html.Span(f"#{index+1}",className='trending-topic-index', ),
                html.Span(" ".join(topic.split('_')[1:3]),className="trending-topic-text")
            ],
            className="mb-1 p-2 trending-topic-content",
        )
        for index,topic in enumerate(trending_topics_list['Name'].tolist())
    ]

    return display_trending_topics

@callback(
    Output('sentiment-top-tweets','children'),
    Input('store-selected-sentiment','data'),
)
def generate_top_tweets(data):
    top_tweets = df[df['Sentiment'] == data['sentiment']].sort_values(by=['RTs Count', 'Likes Count'],ascending=False).iloc[:5]
    
    return [
        dbc.Card(
            [
                dbc.Row(
                    [                    
                        dbc.Col(
                            dbc.CardBody(
                                [                                    
                                    # html.H4("Card title", className="card-title"),
                                    html.P(
                                        tweet,
                                        className="card-text",
                                    ),
                                    html.Div([
                                        # retweets
                                        html.Span([
                                            html.I(className="fa-solid fa-retweet me-1",style={"color":"#00ba7c"}),
                                            html.Span(
                                                f"{rts}",
                                                className="card-text fw-bold",
                                            ),
                                        ],className="me-3"),
                                        #likes
                                        html.Span([
                                            html.I(className="fa-solid fa-heart me-1",style={"color":"#f91880"}),
                                            html.Span(
                                                f"{likes}",
                                                className="card-text fw-bold",
                                            ),
                                        ],className="me-3"),
                                        #timestamp
                                        html.Span([
                                            html.Span(
                                                f"{datetime.strptime(timestamp, '%Y-%m-%d %H:%M:%S%z').strftime('%d-%m-%Y')}",
                                                className="card-text text-muted",
                                            ),
                                        ],className="me-3"),
                                        #go to tweet
                                        html.A([
                                            html.I(className="fa-solid fa-arrow-up-right-from-square me-1",style={"color":"#1d9bf0"}),                                            
                                        ],className="me-3",href=url,target="_blank"),
                                    ]),
                                ]
                            ),
                            class_name=""
                        ),
                    ],
                    className="g-0 d-flex align-items-center",
                )
            ],
            className="mb-3 top-tweet-container shadow",
            # style={"maxWidth": "540px"},
        )

        for tweet,rts,likes,timestamp,url in zip(top_tweets['Tweet'],top_tweets['RTs Count'],top_tweets['Likes Count'],top_tweets['Timestamp'],top_tweets['URL'],)
    ]