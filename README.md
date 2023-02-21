# UiTM Online Reputation using Sentiment Analysis and Topic Modelling

This file contains a complete guideline for installing the dashboard and machine learning (ML) models for the project on a Windows-based machine.

## Dashboard Installation & Build

1. Install Python 3.10 from Microsoft Store

2. Download and extract the zip file named <b>dashboard</b> to your preferred location. The file structure should look like this

        📦dash board
        ┣ 📂assets
        ┣ 📂dataset
        ┣ 📂env
        ┃ ┣ 📜.env
        ┃ ┣ 📜.gitignore
        ┃ ┗ 📜config.py
        ┣ 📂instance
        ┃ ┗ 📜UitmCorporateDept.db
        ┣ 📂layout
        ┃ ┣ 📜layout.py
        ┃ ┗ 📜utils.py
        ┣ 📂pages
        ┃ ┣ 📂auth
        ┃ ┃ ┣ 📜login.py
        ┃ ┃ ┗ 📜register.py
        ┃ ┣ 📂classify_tweet
        ┃ ┃ ┣ 📜classify_tweet.py
        ┃ ┃ ┗ 📜classify_tweet_data.py
        ┃ ┣ 📂reputation
        ┃ ┃ ┣ 📜reputation.py
        ┃ ┃ ┗ 📜reputation_data.py
        ┃ ┣ 📂sentiment
        ┃ ┃ ┣ 📜sentiment.py
        ┃ ┃ ┗ 📜sentiment_data.py
        ┃ ┗ 📂topics
        ┃ ┃ ┣ 📜topics.py
        ┃ ┃ ┗ 📜topics_data.py
        ┣ 📂utils
        ┃ ┗ 📜constants.py
        ┣ 📜.gitignore
        ┣ 📜app.py
        ┣ 📜db.ipynb
        ┣ 📜index.py
        ┣ 📜models.py
        ┣ 📜Procfile
        ┣ 📜README.md
        ┣ 📜requirements.txt
        ┣ 📜routes.py

3. Open a command prompt and navigate to the project directory
   
    `> cd /path/to/project`

4. A virtual environment is needed to store specific dependencies for the project later. In this case, a built-in **venv** library is used as the virtual environment tool

    Use the below command to create a virtual environment called <b>.venv</b>

    `> python -m venv .venv`

    Then, activate the created environment to assign the environment as the current Python interpreter for a duration of a shell session

    `> .venv\Scripts\activate`

5. Install all required dependencies listed in  [requirements.txt](requirements.txt) by using **pip**, which is a standard package manager for Python

    `> pip install -r requirements.txt`

6. Once the dependencies installation is completed, run the [index.py](index.py) to build and run the entire application

    `> python index.py`

7. The website then can be accessed at http://127.0.0.1:80

## Extras

Visit this [link](README-full.md) for the full guideline including the ML models deployment.