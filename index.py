from app import app, server

from routes import render_page_content

from env.config import APP_DEBUG

if __name__=="__main__":
    app.run(
        debug=APP_DEBUG,
        host= '0.0.0.0',
        port='8050'
        # dev_tools_hot_reload=False,
    )