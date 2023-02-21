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

<br>

## ML Model Installation

It is important to note that the ML model installation is <b>OPTIONAL</b> because the dashboard does not depend on the models. The models are only required when the user wants to utilize the <b>tweet classification</b> functionality in the 'Classify Tweet' page within the dashboard.

This process deploys the models in **Google Colab**. Hence, a **Google Drive (GD)** account is required to complete the process.

1. Create a folder named <b>uitm-orm</b>, within <b>My Drive</b> directory in GD

2. Upload all contents within <b>Model deployment</b> folder into the created GD folder

3. In GD, open the `bertopic-flask.ipynb` in Google Colab. **right-click the file** > **Open with** > **Google Colaboratory**

    <img src="README\Screenshot_20230221_052038.png" width="500">
    
    <br>
    
    You need to install the plugin if the Google Colab option is unavailable:-
    
    1. Click Connect more apps

        <img src="README\Screenshot_20230221_052038.png" width="500" style="margin-bottom:15px">

    2. Search Colaboratory and click on the app

        <img src="README\Screenshot_20230221_043124.png" width="500" style="margin-bottom:15px">

    3. Install the app  

        <img src="README\Screenshot_20230221_043139.png" width="500">
    <br>
    
4. Before running the notebook, click **Runtime** > **Change runtime type** > select **GPU** for hardware accelerator > **Save** 
    
    <img src="README\Screenshot_20230221_054811.png" width="250" style="margin-right:15px">
    <img src="README\Screenshot_20230221_054822.png" width="250">

5. Run all cells in the notebook by clicking **Runtime** > **Run all** or using the shortcut **Ctrl+F9**

6. You'll need to give permission to mount the Google Drive. Just follow the instructions

7. Navigate to the output of the last cell 'Start FLASK'. Copy the **URL address**  in line as pointed below

    <img src="README\Screenshot 2023-02-21 181030.png" width="550">

8. In the local project directory, navigate to the [env/.env](env/.env) file

9. Paste the copied URL in `BERTOPIC_HOST` entry

    <img src="README\Screenshot_20230221_061937.png" width="450">

10. Repeat **steps 3 - 9** for `sentiment-flask.ipynb`
    
    At step 9, the copied URL address should be pasted in `SENTIMENT_HOST` entry

11. Re-run the `index.py` in the local project directory to run the application and utilize the tweet classification functionality






