# -*- coding: utf-8 -*-
"""
Created on Mon Sep  4 14:06:35 2023

@author: Andrew
"""

import pandas as pd
from faker import Faker
import random
import datetime

# Initialize the Faker instance
fake = Faker()

# Define the number of names and days for which you want data
num_names = 150
start_date = datetime.date(2023, 8, 1)  # Start date for the month
end_date = datetime.date(2023, 8, 31)   # End date for the month
centers = ['DAL','FTW','OKC','STX','HOU','SHV']  # Available service centers for assignment

# Create empty lists for each column
names = []
employee_number = []
service_center = []
dates = []
bills_per_hour = []
damaged = []
handled_shipments = []
reweigh_total = []
reweigh_captured = []
dimension_total = []
dimension_captured = []
punch_to_scan = []
scan_to_punch = []
second_punch_to_scan = []
second_scan_to_punch = []

# Create empty lists for each column in gaps DataFrame
gaps = {
    'Name': [],
    'Employee ID': [],
    'Service Center': [],
    'Date': [],
    'Gap Time': [],
    'First Pro Number': [],
    'First Pro HU': [],
    'Second Pro Number': [],
    'Second Pro HU': []
}

#  Create list of names, employee id numbers, and service center
name_id = [(fake.first_name() + ' ' + fake.last_name(), fake.random_number(digits=8), random.choice(centers)) for _ in range(num_names)]

#  Ranges for punch to scan and scan to punch columns
slow_start = [x for x in range(21,70)]
normal_start = [x for x in range(2,20)]

# Generate data for each day of the specified month
current_date = start_date
count= 0
while current_date <= end_date:
    # Generate data for each employee on each weekday in August 2023
    for name, emp_id, center in name_id:
        names.append(name)
        employee_number.append(emp_id)
        service_center.append(center)
        
        # Store the current date (weekday)
        dates.append(current_date.strftime("%Y-%m-%d"))
        
        # Generate a random value for 'Bills per Hour' between 0.5 and 11.9
        bills_per_hour.append(round(random.uniform(0.5, 11.9), 1))
        
        #Generate handled shipment count
        handled_shipments.append(random.randint(int(bills_per_hour[-1]*2), int(bills_per_hour[-1]*12)))
        
        # Generate a random value for 'Damaged' between 0 and 3
        if count%22 == 0:
            damaged.append(random.randint(2, 3))
        else:
            damaged.append(random.randint(0,1))
        
        # Generate a random value for 'Reweigh Total' between 0 and 60
        reweigh_total.append(random.randint(0, handled_shipments[-1]))
        
        # Generate 'Reweigh Captured' as a random value less than or equal to 'Reweigh Total'
        reweigh_captured.append(random.randint(0, reweigh_total[-1]))
        
        # Generate 'Dimension Total'
        dimension_total.append(random.randint(0,reweigh_total[-1]))
        
        #Generate 'Dimension Captured'
        dimension_captured.append(random.randint(0,dimension_total[-1]))
        
        # Generate 'Punch to Scan' as random value between 2 and 70 minutes
        if count%17 == 0:
            punch_to_scan.append(random.choice(slow_start))
        else:
            punch_to_scan.append(random.choice(normal_start))
        
        # Generate 'Scan to Punch' as random value between 2 and 70 minutes
        if count%17 == 0:
            scan_to_punch.append(random.choice(slow_start))
        else:
            scan_to_punch.append(random.choice(normal_start))
        
        # Generate 'Punch to Scan' as random value between 2 and 70 minutes
        if (count%13 == 0) |(count%24 == 0):
            second_punch_to_scan.append(random.choice(slow_start))
        else:
            second_punch_to_scan.append(random.choice(normal_start))
        
        # Generate 'Scan to Punch' as random value between 2 and 70 minutes
        if (count%11 == 0) |(count%29 == 0):
            second_scan_to_punch.append(random.choice(slow_start))
        else:
            second_scan_to_punch.append(random.choice(normal_start))
        
        # Create columns for gaps DateFrame
        num_rows = random.randint(0, 8)
        for _ in range(num_rows):
            gaps['Name'].append(name)
            gaps['Employee ID'].append(emp_id)
            gaps['Service Center'].append(center)
            gaps['Date'].append(current_date.strftime("%Y-%m-%d"))
            gaps['Gap Time'].append(round(random.uniform(20, 35), 2))
            gaps['First Pro Number'].append(fake.random_number(digits=10))
            gaps['First Pro HU'].append(random.randint(1,8))
            gaps['Second Pro Number'].append(fake.random_number(digits=10))
            gaps['Second Pro HU'].append(random.randint(1,8))
        count += 1
        
    # Move to the next weekday
    current_date += datetime.timedelta(days=1)
    while current_date.weekday() >= 5:  # Skip weekends (Saturday and Sunday)
        current_date += datetime.timedelta(days=1)

# Create dock DataFrame
dock = {
    'Name': names,
    'Employee ID': employee_number,
    'Service Center': service_center,
    'Date': dates,
    'Bills per Hour': bills_per_hour,
    'Handled Shipments': handled_shipments,
    'Damaged': damaged,
    'First Punch to Scan': punch_to_scan,
    'First Scan to Punch': scan_to_punch,
    'Second Punch to Scan': second_punch_to_scan,
    'Second Scan to Punch': second_scan_to_punch
}

dock_df = pd.DataFrame(dock)

# Create reweigh DataFrame
reweigh = {
    'Name': names,
    'Employee ID': employee_number,
    'Service Center': service_center,
    'Date': dates,
    'Reweigh Total': reweigh_total,
    'Reweigh Captured': reweigh_captured,}

reweigh_df = pd.DataFrame(reweigh)

# Create dimension DataFrame
dimension = {
    'Name': names,    
    'Employee ID': employee_number,
    'Service Center': service_center,
    'Date': dates,
    'Dimension Total': dimension_total,
    'Dimension Captured': dimension_captured,}

dimension_df = pd.DataFrame(dimension)

gaps_df = pd.DataFrame(gaps)

#  Create new columns based on generated numbers
reweigh_df['Reweigh Percentage'] = round(reweigh_df['Reweigh Captured']/reweigh_df['Reweigh Total'],2)
dimension_df['Dimension Percentage'] = round(dimension_df['Dimension Captured']/dimension_df['Dimension Total'],2)
dock_df['Dock Time'] = round(dock_df['Handled Shipments']/dock_df['Bills per Hour'],2)

# Save the DataFrame to a CSV file or any other desired format
dock_df.to_csv('company_data.csv', index=False)
reweigh_df.to_csv('reweigh.csv', index=False)
dimension_df.to_csv('dimension.csv', index=False)
gaps_df.to_csv('gaps.csv', index=False)