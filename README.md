# GitHub Rating Analysis for Top 20 Programming Languages
This Python script utilizes Selenium to extract information about the top 20 programming languages from the TIOBE Index and then analyzes their popularity on GitHub. The main functionalities include retrieving TIOBE ratings for programming languages and determining the number of repositories on GitHub associated with each language.

## Prerequisites
Make sure you have the ChromeDriver executable installed and specify the correct path in the script.
Install the required Python packages by running:

`pip install selenium pandas matplotlib`

## Usage
1. Clone this repository or download the script.
2. Install the required packages.
3. Execute the script by running:

`python script_name.py`

4. The script will open a Chrome browser, fetch TIOBE ratings for the top 20 programming languages, and then determine the number of GitHub repositories associated with each language.
5. Results will be printed to the console and saved in two text files: "Tiobe Top 20 Lenguajes.txt" and "Resultados.txt."
6. A bar chart illustrating GitHub ratings for the top 20 languages will be displayed.

## Script Overview
*get_Top20_languages(browser)*: Retrieves TIOBE ratings for the top 20 programming languages and saves the information in a text file.

*github_topics_top20(browser, topic)*: Determines the number of GitHub repositories associated with a specific programming language topic.

*github_rating(list_top20_repositories)*: Calculates GitHub ratings for the top 20 languages based on the number of repositories.

*github_rating_dataframe(dictionary_top20_languages)*: Creates a Pandas DataFrame and prints the GitHub ratings, repositories, and TIOBE ratings for each language.

*bar_chart(df)*: Generates a bar chart illustrating GitHub ratings for the top 20 programming languages.

*main(browser)*: Executes the main functionalities, fetching TIOBE ratings and GitHub information, and generating the final bar chart.

Contributors
Emilio Ginzo
