from dash import html
import dash_bootstrap_components as dbc

# generate pill title for each component
def title_chart(title):
    return html.Div(
        html.H6(title,className="text-uppercase fw-bold m-0"),   
        className="title-chart-container p-2 mb-2 ps-3"
    )

def title_page_row(title:str):
    # page title
    return dbc.Row(
        [
            html.H2(
                children=title,
                style={'color':'#f4f4f4',},
                className="text-center fw-bold",
            ),
        ],
        class_name="my-4"
    )
    

# def trending_topics_list()