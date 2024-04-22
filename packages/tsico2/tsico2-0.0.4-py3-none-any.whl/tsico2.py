import os.path
import requests
import netCDF4
import matplotlib.pyplot as plt
import numpy as np
import datetime
from matplotlib.dates import DateFormatter
from matplotlib.ticker import FixedLocator
from bs4 import BeautifulSoup # Import BeautifulSoup
import statsmodels.api as sm
import pandas as pd
import subprocess as sp
import warnings
warnings.filterwarnings('ignore', category=UserWarning)

# Set the base URL for downloading files
base_url = "https://www.ncei.noaa.gov/data/total-solar-irradiance/access/monthly/"

# Set the number of x-ticks
num_xticks = 15

# Ask the user for the beginning and end years and months
begin_year_month = input("Enter the beginning year-month (e.g. 1978-11): ")
end_year_month = input("Enter the end year-month (e.g. 2023-3): ")

begin_year, begin_month = map(int, begin_year_month.split("-"))
end_year, end_month = map(int, end_year_month.split("-"))

# Create empty lists to store the data for plotting
dates = []
tsi_values = []

# Loop through each year in the specified range to download files
for year in range(begin_year, end_year + 1):
    # Construct the partial filename based on the year
    if year == 2023:
        partial_filename = f"tsi_v02r01-preliminary_monthly_s{year}"
    else:
        partial_filename = f"tsi_v02r01_monthly_s{year}01"
    
    # Get the list of available files from the website
    response = requests.get(base_url)
    soup = BeautifulSoup(response.text, 'html.parser')
    available_files = [link.get('href') for link in soup.find_all('a')]
    
    # Find all matching files from the list of available files
    matching_files = []
    for file in available_files:
        if partial_filename in file:
            matching_files.append(file.strip())
    
    # Check if any matching files were found
    if len(matching_files) == 0:
        print(f"No matching files found for {partial_filename}")
        continue
    
    # Loop through each matching file to download and process it
    for matching_file in matching_files:
        # Use the matching file as the filename
        filename = matching_file
        
        # Check if the file already exists on disk
        if not os.path.exists(filename):
            # Construct the full URL for downloading the file
            url = base_url + filename
            
            # Download the file using requests
            response = requests.get(url)
            
            # Check if the download was successful
            if response.status_code == 200:
                # Save the downloaded file to disk
                with open(filename, "wb") as f:
                    f.write(response.content)
                print(f"Downloaded {filename}")
            else:
                print(f"Failed to download {filename}")
        
        # Open the file using netCDF4
        with netCDF4.Dataset(filename) as dataset:
            # Read the time and TSI variables
            time_var = dataset.variables["time"]
            tsi_var = dataset.variables["TSI"]
            
            # Convert the time values to dates
            time_dates = netCDF4.num2date(time_var[:], time_var.units)
            
            # Append only dates and TSI values within specified range to lists.
            for date, tsi_value in zip(time_dates, tsi_var[:]):
                if date.year == begin_year and date.month < begin_month:
                    continue
                
                if date.year == end_year and date.month > end_month:
                    continue
                
                dates.append(datetime.datetime(date.year, date.month, date.day))
                tsi_values.append(tsi_value)

# Download CO2 data file.
sp.call('wget -nc ftp://aftp.cmdl.noaa.gov/products/trends/co2/co2_mm_mlo.csv', shell=True)

# Load CO2 data into DataFrame.
co2 = pd.read_csv('co2_mm_mlo.csv',comment='#')
co2=co2.iloc[:,[0,1,3]]

# Convert year and month columns into a single date column.
co2['date'] = pd.to_datetime(co2[['year', 'month']].assign(DAY=1)).dt.to_period('M').astype(str)

# Extract only rows within specified range.
start_date = begin_year_month
end_date = end_year_month

start_year, start_month = map(int, start_date.split("-"))
end_year, end_month = map(int, end_date.split("-"))

mask = ((co2['year'] > start_year) | ((co2['year'] == start_year) & (co2['month'] >= start_month))) & ((co2['year'] < end_year) | ((co2['year'] == end_year) & (co2['month'] <= end_month)))
co2 = co2.loc[mask]

# Convert co2['date'] column from str to datetime.
co2['date'] = pd.to_datetime(co2['date'])


# Create a figure and axes for plotting.
fig, ax1 = plt.subplots()

# Perform a first-order linear regression on TSI data.
X = sm.add_constant(range(len(tsi_values)))
y = tsi_values
model = sm.OLS(y,X)
results = model.fit()

r_squared_tsi = results.rsquared_adj

p_value_intercept_tsi, p_value_slope_tsi = results.pvalues

# Plot TSI regression line.
tsi_reg, = ax1.plot(dates, tsi_values, linestyle=':',color='k')
tsi_reg, = ax1.plot(dates, results.fittedvalues, linestyle=':',color='k')

# Create a second y-axis for CO2 data.
ax2 = ax1.twinx()

# Plot CO2 data using matplotlib.
color = 'tab:black'
ax2.set_ylabel('CO2', color='k')
co2_raw, = ax2.plot(dates, co2['average'], color='k')
ax2.tick_params(axis='y', labelcolor='k')

# Perform a first-order linear regression on CO2 data.
y = co2['average']

model = sm.OLS(y,X)
results = model.fit()

r_squared_co2 = results.rsquared_adj

p_value_intercept_co2, p_value_slope_co2 = results.pvalues

# Plot CO2 regression line.
co2_reg, = ax2.plot(dates, results.fittedvalues, color='k')

# Display r-squared and p-value on the graph.
ax1.text(0.05, 0.95, f"TSI:\nR-squared: {r_squared_tsi:.4f}\nP-value (slope): {p_value_slope_tsi:.4f}\n\nCO2:\nR-squared: {r_squared_co2:.4f}\nP-value (slope): {p_value_slope_co2:.4f}", transform=ax1.transAxes, fontsize=14, verticalalignment='top')

# Set the x-tick labels to rotate 90 degrees and show only year-month without day using DateFormatter.
ax1.xaxis.set_major_formatter(DateFormatter('%Y-%m'))
ax1.set_xticklabels(ax1.get_xticklabels(), rotation=90)

# Set the number of x-ticks using MaxNLocator.
ax1.xaxis.set_major_locator(plt.MaxNLocator(num_xticks))

# Set the title using set_title method of Axes object ax.
ax1.set_title(f"Total Solar Irradiance and CO2 from {begin_year}-{begin_month} to {end_year}-{end_month}")

# Save the plot as a PNG image using savefig method of Figure object fig.
def main():
 plt.savefig(f"{begin_year}-{begin_month}-{end_year}-{end_month}.png", bbox_inches="tight")
 plt.show()
if __name__ == "__main__":
 main()
