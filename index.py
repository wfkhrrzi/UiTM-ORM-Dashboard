from app import app, server

from routes import render_page_content

from env.config import APP_DEBUG

if __name__=="__main__":
    app.run(
        debug=True,
        host= '0.0.0.0',
        port='80'
        # dev_tools_hot_reload=False,
    )