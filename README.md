# TE_DE_Homework
Homework solution for TietoEvry recruitment

## Usage
Clone the git repository and add rest of the files that were included in task zip in the same folder.

Command line:
python main.py [prepare|task1|task2|task3|task4|task5|taskbonus|clean]
Prepare should be executed before running any tasks.
Task commands will each run their respective tasks.
Clean will remove all files created by preparation or any task.

## Task answers and decisions made
Answers to questions in addition to reasoning for main decisions made during the development.

### Task 1
I chose SQLite for storing and processing the data, since the amount of data and its estimated growth speed is very small. This makes it fairly easy for me to handle the aggregates the way I am most comfortable with.

### Task 2
I decided to use the data loaded in the SQLite db for assert. I checked that the import/staging table from SQLite db matches with all the listed conditions.
The automated tests can be ran either via the main script or directly with "pytest DE_Homework_Mikko_Hirvola.py".

### Task 3
I started with SQLite, and in the third question I came to conclusion that SQLite is not the most convenient and switched to using Pandas dataframes. The results are visualised with matplotlib.

The plots show that:
- jalkakyykky was the most popular device 
- hour of the day had a significant impact on the usage, with hours between 6 and 18 being the most popular 
- the effect of a weekday was smaller, with weekdays having slightly higher usage

### Task 4
I used original unaggregated gym data and continued using dataframes. Results are written to a csv file on disk instead of database, for potential future use.

### Task 5
For this task, I continued using the SQLite database, so I can use queries on the existing aggregated data. I visualised the data as a heatmap over precipitation/temperature and daytime, because in Task 3 I have discovered that the hour had the most significant effect on the gym usage; and, for example, temperature is affected by daytime.

Results show that both Precipitation and Temperature have effect on the outdoor gym usage.
It should be also noted that the Y-axis of the graphs are not absolute values, but relative array indexes. This however does not change the answer.

Another notable feature is that, since the lowest usage values are rounded to 2, the coolest areas in the graphs show lack of data, while coolest colored areas are of relatively low-use.

### Bonus Task
I start from using raw weather data and adding missing columns to it.
Similarly to Task 5, I use hour, usage prediction, temperature and precipation as variables to visualize the results as heatmaps.
Comparing these heatmaps against the ones created in Task 5, I see that the model gives estimates too large usage for nighttime hours, and from that are not believable.

## Library Dependencies

| Name | Version | Build |
| --- | --- | --- |
| joblib | 1.1.0 | pyhd3eb1b0_0 |
| matplotlib | 3.5.1 | py39haa95532_0 |
| matplotlib-base | 3.5.1 | py39hd77b12b_0 |
| numpy | 1.20.3 | py39ha4e8547_0 |
| numpy-base | 1.20.3 | py39hc2deb75_0 |
| pandas | 1.4.1 | py39hd77b12b_0 |
| pytest | 6.2.5 | py39haa95532_2 |
| python | 3.9.7 | h6244533_1 |
| python-dateutil | 2.8.2 | pyhd3eb1b0_0 |
| scikit-learn | 1.0.2 | py39hf11a4ad_1 |
| sqlite | 3.37.2 | h2bbff1b_0 |
