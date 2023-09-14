# -*- coding: utf-8 -*-
"""
Created on Wed Sep  6 01:14:26 2023

@author: Andrew
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Plotting functions

# Line plot showing each service center's production by team
def plot_bills_per_hour(service_center_data, service_center):
    plt.figure(figsize=(12, 6))
    sns.lineplot(data=service_center_data, x='Date', y='Bills per Hour', hue='Team', markers=True, ci=None)
    average_bills_per_hour = service_center_data.groupby('Date')['Bills per Hour'].mean().reset_index()
    plt.plot(average_bills_per_hour['Date'], average_bills_per_hour['Bills per Hour'], linestyle='--', label='Average', color='black')
    plt.title(f'Team Production at {service_center}')
    plt.xlabel('Date')
    plt.ylabel('Bills per Hour')
    plt.xticks(rotation=45)
    plt.legend(title='Team')
    plt.grid(True)
    plt.tight_layout()
    plt.show()

# Line plot showing production by service center
def plot_bills_per_hour_comparison(dock_merged):
    plt.figure(figsize=(10, 6))
    sns.lineplot(x='Date', y='Bills per Hour', hue='Service Center', data=dock_merged, ci=None)
    plt.title('Daily Production by Service Center')
    plt.xlabel('Date')
    plt.ylabel('Bills per Hour')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.legend(title='Service Center')
    plt.show()

# Bar plot showing daily production by service center
def plot_individual_bills_per_hour(dock_merged):
    # Convert the 'Date' column to a datetime object
    dock_merged['Date'] = pd.to_datetime(dock_merged['Date'])
    
    # Get unique dates
    unique_dates = dock_merged['Date'].unique()
    
    # Create individual bar plots for each day
    for date in unique_dates:
        plt.figure(figsize=(6, 4))
        plt.title(f'Bills per Hour for {date}')
        sns.barplot(data=dock_merged[dock_merged['Date'] == date], x='Service Center', y='Bills per Hour')
        plt.xlabel('Service Center')
        plt.ylabel('Bills per Hour')
        plt.tight_layout()
        plt.show()

# Define start and end dates as user inputs (in yyyy-mm-dd format)
#start_date and end_date can be entered by user with commented out code below
#start_date = input("Enter start date (yyyy-mm-dd): ") 
#end_date = input("Enter end date (yyyy-mm-dd): ")
start_date = '2023-08-08'
end_date = '2023-08-23'

# Load data from each file
dock = pd.read_csv('company_data.csv')
reweigh = pd.read_csv('reweigh.csv')
dimension = pd.read_csv('dimension.csv')

# Merge data into single dataframe
merged_first = pd.merge(dock, reweigh, how='left')
dock_merged = pd.merge(merged_first, dimension, how='left')

# Output merged dataframe to csv file
dock_merged.to_csv('merged.csv')

# Initialize a dictionary to store teams per Service Center
teams_per_service_center = {}

# Group the data by 'Service Center' and aggregate 'Employee ID' values into a list
grouped = dock_merged.groupby('Service Center')['Employee ID'].unique().agg(list)

# Create three teams for each Service Center
for service_center, unique_employee_ids in grouped.items():
    number_of_teams = 3
    # Ensure we have at least three unique employees in the Service Center
    if len(unique_employee_ids) < number_of_teams:
        print(f"Warning: Service Center '{service_center}' does not have enough unique employees for three teams.")
        continue
    
    # Calculate the size of each team and initialize the teams
    team_size = len(unique_employee_ids) // number_of_teams
    teams = [[] for _ in range(number_of_teams)]
    
    # Distribute the unique Employee IDs into three teams
    for i, emp_id in enumerate(unique_employee_ids):
        teams[i % number_of_teams].append(emp_id)
    
    # Store the teams in the dictionary
    teams_per_service_center[service_center] = teams

# Add a new column 'Team' to the original dock_merged DataFrame
dock_merged['Team'] = None

# Assign the team to each employee based on 'Service Center'
for service_center, teams in teams_per_service_center.items():
    for i, team in enumerate(teams, 1):
        dock_merged.loc[dock_merged['Employee ID'].isin(team), 'Team'] = f'Team {i}'
        # Create a file name for the team
        file_name = f'team {i} {service_center}.csv'
        
        # Filter the merged DataFrame for the current team's Employee IDs
        team_data = dock_merged[dock_merged['Employee ID'].isin(team)]
        
        # Save the team's data to a CSV file
        team_data.to_csv(file_name, index=False)
        
# Create plots from functions
for service_center, _ in teams_per_service_center.items():
    service_center_data = dock_merged[(dock_merged['Service Center'] == service_center) & (dock_merged['Date'] >= start_date) & (dock_merged['Date'] <= end_date)]
    plot_bills_per_hour(service_center_data, service_center)

# Function calls for plots
plot_bills_per_hour_comparison(dock_merged[(dock_merged['Date'] >= start_date) & (dock_merged['Date'] <= end_date)])
plot_bills_per_hour(service_center_data, service_center)
plot_individual_bills_per_hour(dock_merged[(dock_merged['Date'] >= start_date) & (dock_merged['Date'] <= end_date)])

# Get unique service centers from the dock_merged DataFrame
unique_service_centers = dock_merged['Service Center'].unique()

# Save text file of employee monthly averages by service center
for service_center in unique_service_centers:
    file_name = f'{service_center}_employee_production.txt'
    with open(file_name, 'w') as file:
        service_center_data = dock_merged[dock_merged['Service Center'] == service_center]
        grouped = service_center_data.groupby(['Name'])
        for name, group_data in grouped:
            mean_dock_time = group_data['Dock Time'].mean()
            mean_handled_shipments = group_data['Handled Shipments'].mean()
            mean_bills_per_hour = (group_data['Handled Shipments'] / group_data['Bills per Hour']).mean()
            mean_first_punch_to_scan = group_data['First Punch to Scan'].mean()
            mean_first_scan_to_punch = group_data['First Scan to Punch'].mean()
            mean_second_punch_to_scan = group_data['Second Punch to Scan'].mean()
            mean_second_scan_to_punch = group_data['Second Scan to Punch'].mean()
            file.write(f'Service Center: {service_center}, Employee Name: {name}\n')
            file.write(f'Mean Dock Time: {mean_dock_time:.2f} hours\n')
            file.write(f'Mean Handled Shipments: {mean_handled_shipments:.2f}\n')
            file.write(f'Mean Bills per Hour (per shipment): {mean_bills_per_hour:.2f}\n')
            file.write(f'Mean First Punch to Scan: {mean_first_punch_to_scan:.2f} minutes\n')
            file.write(f'Mean First Scan to Punch: {mean_first_scan_to_punch:.2f} minutes\n')
            file.write(f'Mean Second Punch to Scan: {mean_second_punch_to_scan:.2f} minutes\n')
            file.write(f'Mean Second Scan to Punch: {mean_second_scan_to_punch:.2f} minutes\n')
            file.write('\n')

