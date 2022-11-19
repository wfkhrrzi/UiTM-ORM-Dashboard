from dash import html

# generate pill title for each component
def title_chart(title):
    return html.Div(
        html.H6(title,className="text-uppercase fw-bold m-0"),   
        className="title-chart-container p-2 mb-2 ps-3"
    )

# def trending_topics_list()