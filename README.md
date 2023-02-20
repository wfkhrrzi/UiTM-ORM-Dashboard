# Direct Lending Intern Assessment - Wan Fakhrurrazi

This file contains an installation guidelines for Windows-based machine and list of assumptions made throughout the task.

## Installation

1. Install Python 3.10 from Microsoft Store.

2. Download and extract the zip file containing the application to your preferred location. The file structure should look like this.
    ```
    📦path/to/project
    ┣ 📂website
    ┃ ┣ 📂app
    ┃ ┃ ┣ 📂static
    ┃ ┃ ┃ ┗ 📜index.js
    ┃ ┃ ┣ 📂templates
    ┃ ┃ ┃ ┗ 📜home.html
    ┃ ┃ ┣ 📜model.py
    ┃ ┃ ┣ 📜view.py
    ┃ ┃ ┗ 📜__init__.py
    ┃ ┣ 📂instance
    ┃ ┃ ┗ 📜database.db
    ┃ ┣ 📜index.py
    ┃ ┗ 📜requirements.txt
    ┗ 📜read.md
    ```

3. Open a command prompt and navigate to the project directory.
    
    `> cd /path/to/project`

4. A virtual environment is needed to store specific dependencies for the project later. In this case, a built-in **venv** library is used as the virtual environment tool.

    Use the below command to create a virtual environment called 'venv'.

    `> python -m venv venv`

    Then, activate the created environment to assign the environment as the current Python interpreter for a duration of a shell session. 

    `> venv\Scripts\activate`

<br>

## Program build & execution

1. Navigate to the website directory.

    `> cd website`

2. Install all required dependencies listed in  `requirement.txt` by using **pip**, which is a standard package manager for Python.

    `> pip install -r requirements.txt`

3. Once the dependencies installation is completed, run the `index.py` to build and run the entire application.

    `> python index.py`

4. The website then can be accessed through http://127.0.0.1:5000

<br>

## Assumptions

1. Instruction #6 requires a query of the submitted data. All submitted information is retrieved and displayed in the form of table.

2. Also, for instruction #6, once the form is submitted through AJAX request, the page reloads itself to refresh the data in the table.

3. There is no specific direction to how the backend should be developed. in this case, Flask web framework is utilized to ease and speed up the development. 

4. The web app is already being tested using the provided test cases. To restart the testing, remove the `instance/database.db` folder and rerun `index.py`.



