# tsico2
This is under review.

tsico2 is a tool available on PyPI that allows users to visualize monthly values of Total Solar Irradiance (TSI) and global CO2 levels. Users can specify a start and end date for the period they wish to visualize, and the tool will display a graph with four lines representing the raw and linear regression values for both TSI and CO2. 

Additionally, the calculated R-squared and p-value for the linear regression lines are also displayed on the graph. This provides users with an easy and convenient way to analyze trends in TSI and CO2 levels over time.

# How to run tsico2

Before running tsico2, you must install it by pip command.

$ pip install tsico2

$ tsico2

Enter start-date for March 2007 in this example

Enter the beginning year-month (e.g. 1978-11): 2007-3

Enter end-date for March 2014

Enter the end year-month (e.g. 2023-3): 2014-3

The result will be popped on the screen. 
The solid lines are the original and regression lines for CO2 and the dotted lines are the original and regression lines for TSI.

<img src="https://github.com/y-takefuji/tsico2/raw/main/2007-3-2014-3.png" width=640 height=480>

