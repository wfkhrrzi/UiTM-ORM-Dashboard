import dash
from dash import callback, callback_context as ctx, ALL, dcc, html
from dash.exceptions import PreventUpdate
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc
# import pandas as pd
# import requests
# import plotly
import plotly.graph_objs as go
import plotly.express as px
from wordcloud import WordCloud
from datetime import datetime
import math
from pages.topics.topics_data import get_ranked_topics,get_dataset,get_topics_over_time,get_all_topics
from layout.utils import title_chart

dash.register_page(__name__,path='/topics')

# INITIALIZATION
topics_all = get_all_topics()

df = get_dataset()

ranked_topics = get_ranked_topics()

DISPLAY_TOPICS_NUMBER = 10
TOPIC_CONFIG_PAGE_SIZE = 10
TOTAL_TOPIC = ranked_topics['Topic'].count()

topic_over_time = get_topics_over_time(ranked_topics[:10]['Topic'])
topic_over_time.update_layout(
    {
        "width":None,
        "title_text":None,
        "margin":dict(
            # pad=10
        ),
        "paper_bgcolor":'rgba(0,0,0,0)',
        "plot_bgcolor":'rgba(0,0,0,0)',
        "yaxis":{
            "title":{
                "font":dict(
                    family = 'Roboto, sans-serif',
                    size = 15,
                    color = '#f4f4f4'
                ),
            }
        },
        "yaxis_zeroline":True,
        "yaxis_zerolinecolor":'#212529',
        "yaxis_zerolinewidth":1.5,
        "yaxis_gridcolor":"#212529",
        "yaxis_gridwidth":0.5,
        "yaxis_tickfont":dict(
            family = 'Roboto, sans-serif',
            size = 13,
            color = '#f4f4f4'
        ),
        "xaxis_gridcolor":"#212529",
        "xaxis_gridwidth":0.5,
        "xaxis_tickfont":dict(
            family = 'Roboto, sans-serif',
            size = 13,
            color = '#f4f4f4'
        ),
        "legend":dict(
            font_color="#f4f4f4",
            # orientation="h",
            # yanchor="bottom",
            # y=1.02,
            # xanchor="center",
            # x=0.5
        ),
    }
)

# LAYOUT 
layout = dbc.Container(    
    [
        # first layer
        dbc.Row(
            [
                # trending topics
                dbc.Col(
                    [
                        title_chart("trending topics"),
                                            
                        html.Div(
                            [
                                html.Div(
                                    [
                                        html.Span(f"#{index+1}",className='trending-topic-index', ),
                                        html.Span(" ".join(topic.split('_')[1:3]),className="trending-topic-text")
                                    ],
                                    className="mb-1 p-2 trending-topic-content",
                                )
                                for index,topic in enumerate(ranked_topics[:10]['Name'].tolist())
                            ]
                        )
                    ],
                    width=12,
                    lg=6,
                    md=6,
                    xl=2,
                    class_name="mb-3 mb-lg-0",
                ),
                # topic ranks by rts and likes
                dbc.Col(
                    [
                        title_chart('topics ranking'),                           
                        dcc.Graph(
                            figure=go.Figure({
                                "data":[
                                    {'x': ranked_topics[:DISPLAY_TOPICS_NUMBER]['Name'].apply(lambda x: ' '.join(x.split('_')[1:3])), 'y': ranked_topics[:DISPLAY_TOPICS_NUMBER]['RTs Count'],'type': 'bar', 'name': 'Retweets','marker_color':'#00ba7c',},
                                    {'x': ranked_topics[:DISPLAY_TOPICS_NUMBER]['Name'].apply(lambda x: ' '.join(x.split('_')[1:3])), 'y': ranked_topics[:DISPLAY_TOPICS_NUMBER]['Likes Count'],'type': 'bar', 'name': 'Likes','marker_color':'#f2c4cb',},
                                ],
                                "layout":{
                                    # "width":600,
                                    # "autosize":False,
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
                                        y=1.02,
                                        xanchor="center",
                                        x=0.5
                                    ),
                                    # "xaxis_title":"Topics",
                                    # "yaxis_title":"Count",
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
                # topic over time
                dbc.Col(
                    [                        
                        dbc.Row(
                            dbc.Col(
                                [
                                    title_chart('topics over time'),
                                    dcc.Graph(
                                        figure=topic_over_time,
                                    )     
                                ]
                            )
                        ) 
                                       
                    ],
                    width=12,
                    lg=12,
                    md=12,
                    xl=6,
                ),
            ]
        ),
        html.Hr(),
        # second layer
        dbc.Row([
            #topics
            dbc.Col([
                html.Div(
                    [
                        html.Div(
                            [
                                html.Span("Topics",className="second-topic-config-title title-chart-size"), 
                                html.Span(
                                    " ".join(ranked_topics['Name'][ranked_topics['Topic'] == 3].iloc[0].split('_')[1:3]),
                                    id="second-topic-config-selected",className="badge bg-success d-none")                           
                            ],
                            className="d-flex justify-content-between mb-3"
                        ),
                        html.Div(
                            id="second-topic-config-buttons",
                            className="d-grid gap-3",
                        ),
                        
                        #pagination
                        dcc.Store(id="store-selected-topic"),
                        html.Div(
                            dbc.Pagination(
                                id="topic-pagination",
                                active_page=1,
                                max_value=math.ceil(ranked_topics['Name'].count()/TOPIC_CONFIG_PAGE_SIZE),
                                class_name="justify-content-center",
                                previous_next=True,
                                size="sm",
                            ),
                            className="pt-4 justify-content-center"
                        )
                    ],
                    className="second-topic-config-container p-4"
                ),
            ],md=12,lg=6,xl=3,xxl=2,class_name="mt-3 mt-xxl-0"),

            dbc.Col(
                [
                    dbc.Row(
                        [
                            #topic name
                            dbc.Col(
                                [
                                    html.Div([
                                        html.H6('Topic',className="text-uppercase fw-bold mb-1"),
                                    ],className="second-topic-stats-title",style={"color":"#b9f3e5"}),

                                    html.Div(
                                        html.P('Example topic',id="second-topic-name",style={"color":"whitesmoke","font-size":"20px"}),
                                        className="py-2"
                                    )
                                ],class_name="",xs=6,md=3,
                                
                            ),
                            #topic desc
                            dbc.Col(
                                [
                                    html.Div([
                                        html.H6('description',className="text-uppercase fw-bold mb-1"),
                                    ],className="second-topic-stats-title",style={"color":"#cdf0b1"}),

                                    html.Div(
                                        html.P(
                                            '''Lorem Ipsum is simply dummy text of the printing and typesetting industry. 
                                            Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, 
                                            when an unknown printer took a galley of type and scrambled it to make a type 
                                            specimen book.''',
                                            style={"color":"whitesmoke","font-size":"13px"}
                                        ),
                                        className="py-2"
                                    )
                                ],class_name="order-3 order-md-2",xs=12,md=5,
                            ),
                            #trend metrics
                            dbc.Col(
                                [
                                    html.Div([
                                        html.H6('total retweets & likes',className="text-uppercase fw-bold mb-1"),
                                    ],className="second-topic-stats-title",style={"color":"#f2c4cb"}),

                                    html.Div(
                                        [
                                            #retweets
                                            html.Div([
                                                html.I(className="fa-solid fa-retweet me-2",style={"color":"#00ba7c"}),
                                                html.Span(
                                                    "20000",
                                                    id="second-topic-rts",
                                                    className="fw-bold",
                                                    style={"color":"#00ba7c"}
                                                ),
                                            ],className="mb-2"),
                                            #likes
                                            html.Div([
                                                html.I(className="fa-solid fa-heart me-2",style={"color":"#f91880"}),
                                                html.Span(
                                                    "3000",
                                                    id="second-topic-likes",
                                                    className="fw-bold",
                                                    style={"color":"#f91880"}
                                                ),
                                            ],className="mb-2"),
                                        ],
                                        className="py-2",style={"font-size":"22px"}
                                    ),
                                ],
                                class_name="order-2 order-md-3",xs=6,md=4,
                            ),
                        ]
                    ),
                    dbc.Row(
                        [
                            #topic score
                            dbc.Col([
                                html.Div([
                                    title_chart('topic scores'),
                                    dcc.Graph(id='second-topic-score'),
                                ]),
                            ],md=12,lg=6,xl=6,xxl=6,),

                            #wordcloud
                            dbc.Col([
                                html.Div([
                                    title_chart('word cloud'),
                                    dcc.Graph(id='second-topic-wordcloud')
                                ])
                            ],md=12,lg=6,xl=6,xxl=6,),
                        ]
                    ),
                ],
                md=12,lg=12,xl=9,xxl=7,class_name="mt-3 mt-xxl-2"
            ),
            
            # top tweets
            dbc.Col([
                title_chart('top tweets'),
                html.Div(id="second-top-tweets",style={"overflow-y":"scroll","max-height":"600px"})
            ],md=12,lg=12,xl=12,xxl=3,class_name="mt-3 mt-xxl-0"),
        ]),        
    ],
    fluid=True
)

@callback(
    Output("second-topic-config-buttons","children"),
    Input("topic-pagination","active_page"),
)
def generate_topics_buttons(active_page):
    start_index = (active_page - 1) * 10
    end_index = start_index + 10

    buttons = []
    for topic_id, topic in zip(ranked_topics[start_index:end_index]['Topic'],ranked_topics[start_index:end_index]['Name'].apply(lambda x: " ".join(x.split('_')[1:3]))):
        button = dbc.Button(id={"type":"second-topic-button","topic_id":topic_id,"index":start_index}, children=topic, class_name="second-topic-config-button", color="light",active=False)
        buttons.append(button)
        start_index+=1
        
    return buttons

@callback(
    Output("store-selected-topic","data"),
    Input({
        "type":"second-topic-button",
        "topic_id":ALL,
        "index":ALL
    },'n_clicks'),    
    State("store-selected-topic","data"),
    State("topic-pagination","active_page"),
)
def update_store_selected_topic(args,data,active_page,):
    if not ctx.triggered_id or not any(args):
        if data is None:
            topic_id = ranked_topics['Topic'].iloc[0]
            index = 0
        else:            
            raise PreventUpdate
    else:
        topic_id = ctx.triggered_id['topic_id']
        index = ctx.triggered_id['index']
    
    return {
        "topic_id":topic_id,
        "index":index,
        "active_page":active_page
    }

@callback(
    Output({
        "type":"second-topic-button",
        "topic_id":ALL,
        "index":ALL
    },'color'),
    Input("store-selected-topic","data"),
    Input("topic-pagination","active_page"),
)
def set_active_button(data,active_page):

    active = "secondary"
    not_active = "light"
    
    if data is None:
        button_id = 0
    else:
        index = str(data['index'])
        button_id = int(index[-1])

    return [
        active if button_id == i and int(data['active_page']) == active_page else not_active for i in range(10)
    ]

@callback(
    Output('second-topic-name','children'),
    Output('second-topic-config-selected','children'),
    Input('store-selected-topic','data'),
)
def update_topic_name(data):
    return [
        " ".join(ranked_topics['Name'][ranked_topics['Topic'] == int(data['topic_id'])].iloc[0].split('_')[1:3])
        for _ in range(2)
    ] 

@callback(
    Output('second-topic-rts','children'),
    Input('store-selected-topic','data'),
)
def update_rts(data):
    return ranked_topics["RTs Count"][ranked_topics["Topic"] == data['topic_id']]

@callback(
    Output('second-topic-likes','children'),
    Input('store-selected-topic','data'),
)
def update_likes(data):
    return ranked_topics["Likes Count"][ranked_topics["Topic"] == data['topic_id']]

@callback(
    Output('second-top-tweets','children'),
    Input('store-selected-topic','data'),
)
def generate_top_tweets(data):
    top_tweets = df[df['Topic reassigned'] == data['topic_id']].sort_values(by=['RTs Count', 'Likes Count'],ascending=False).iloc[:5]
    
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

@callback(
    Output('second-topic-score','figure'),
    Input('store-selected-topic','data'),
)
def generate_topic_score(data):
    topics_list = list(topics_all[str(data['topic_id'])])
    topics_list.reverse()
    x_topic,y_topic = zip(*topics_list)

    return go.Figure(
        go.Bar(
            x=y_topic,
            y=x_topic,
            orientation='h',
            marker_color='#099ad9'
        ),
        {
            "yaxis_showgrid":False,
            "yaxis_showline":False,
            # "yaxis_gridcolor":"#212529",
            # "yaxis_gridwidth":0.5,
            "xaxis_zeroline":True,
            "xaxis_zerolinecolor":'#212529',
            "xaxis_zerolinewidth":2,
            "xaxis_gridcolor":"#212529",
            "xaxis_gridwidth":0.5,
            "paper_bgcolor":'rgba(0,0,0,0)',
            "plot_bgcolor":'rgba(0,0,0,0)',
            "margin":dict(
                l=20,
                r=20,
                b=50,
                t=50,
                pad=10
            ),
            "yaxis_tickfont":dict(
                family = 'Roboto, sans-serif',
                size = 13,
                color = '#f4f4f4'
            ),
            "xaxis_tickfont":dict(
                family = 'Roboto, sans-serif',
                size = 15,
                color = '#099ad9'
            ),
        }
    )

@callback(
    Output('second-topic-wordcloud','figure'),
    Input('store-selected-topic','data'),
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
    wordcloud_text = " ".join(text for text in df[df['Topic reassigned'] == data['topic_id']]["Processed noisy tweet"])
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