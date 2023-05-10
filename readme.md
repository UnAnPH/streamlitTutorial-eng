# Streamlit Tutorial: Live Coding

Creation of a multi-page web application in Streamlit by interacting with a MySQL database to view and add data.

```git clone https://github.com/Cryst4lDr4g0n/streamlitTutorial-eng.git```

## Warm up 
* Branch *live_coding* is the starting point, branch *live_coding_complete* is the final application, branch *base* is the starting point for a new generic project.
* For more information about the database, refer to https://www.mysqltutorial.org/mysql-sample-database.aspx.
* For the step-by-step guide on creating the application, refer to *guide.md*
* To add emojis use https://emojifinder.com with copy-past.

## Environment
### For more information about the different OS and Streamlit: https://docs.streamlit.io/library/get-started/installation

#### 1. Install the MySQL environment (with Docker and Docker-compose https://github.com/Cryst4lDr4g0n/mysql-docker-eng.git)
#### 2. Create a new Python virtual environment (e.g. *pipenv*).

Install pipenv:
```
pip install pipenv
```
Start the virtual env:
```
pipenv shell
```
Install the dependencies:
```
pip install -r requirements.txt

```
#### 3. Verify the installation of streamlit:
```
streamlit hello
```

To stop it:

```Ctrl + C```

#### 4. Launch the application:
```
python -m streamlit run 01_🏠_Home.py
```
Or directly with the command *streamlit*:
```
streamlit run 01_🏠_Home.py
```
To prevent the browser from opening automatically:
```
streamlit run 01_🏠_Home.py --server.headless true
```
