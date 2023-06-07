
# Carbon Footprint Score Calculator

The Carbon Footprint Score Calculator is a Python Streamlit web application that allows users to answer questions about their lifestyle choices during the pandemic and the current period, helping determine the environmental impact of these choices. The application will display information on how your Carbon Footprint Score has changed from the pandemic to the present. The application is divided into two parts:

1. Carbon_Footprint_Calc.py - main application where users answer the survey
2. Submission_Score.py - where the analysis of all the submissions is displayed

# Web App
Click [Here](https://kaludii-carbon-footprint-calc-bios-carbon-footprint-calc-xgt0yx.streamlit.app/ "Here") To View This Application Online!
![image](https://github.com/Kaludii/Carbon-Footprint-Calc-BIOS365/assets/63890666/cabb3141-96c7-4a27-9f89-b70e8237de35)

## Features

* Survey-style questions to calculate your Carbon Footprint Score
* Comparison of your Carbon Footprint Score from during the pandemic to the current period
* Submissions analysis visualization in the 'pages/Submission_Score.py'

## Usage

1. Fill in the survey questions on the main page of the application.
2. Submit the survey by clicking on the "Submit" button.
3. View your score on the next page, along with comparison charts and suggestions on how to improve it.

## Installation

1. Clone the repository
   ```
   git clone https://github.com/Kaludii/Carbon-Footprint-Score-Calculator.git
   ```
2. Change your directory to the cloned project
   ```
   cd Carbon-Footprint-Score-Calculator
   ```
3. Install necessary dependencies
   ```
   pip install -r requirements.txt
   ```
4. Run the Streamlit application
   ```
   streamlit run Carbon_Footprint_Score_Calculator.py
   ```
5.  Open your web browser and visit `http://localhost:8501`.

## Submission Scores Analysis

The "Submission_Score.py" is a 2nd part of the application that displays all submissions and various visualizations showing the distribution of responses for each question from **[this](https://docs.google.com/spreadsheets/d/1aHgyMoxp7aINImqu3eXiwAzq5QvTqbfhUaKv2fkdHss/edit?usp=sharing)** Google Sheet. You can also download the data for each folder ("Submission-Now" or "Submission-Pandemic") as a CSV file.

## License

[MIT](https://choosealicense.com/licenses/mit/)
