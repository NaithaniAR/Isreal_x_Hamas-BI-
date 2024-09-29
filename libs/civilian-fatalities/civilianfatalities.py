# Import necessary libraries
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import numpy as np

# Load dataset
file_path = r'data-points\spreadsheets\xslx\opt_-escalation-of-hostilities-impact.xlsx'
data = pd.read_csv(file_path)

# Clean data
clean_data = data.dropna(axis=1, how='all')
clean_data['date'] = pd.to_datetime(clean_data['date'])

# Streamlit App
st.title('Israel-Hamas Conflict: Data Analysis and Visualization')

# Section 1: Display Raw Data
st.header('Dataset Preview')
st.write(clean_data.head())

# Section 2: Summary Statistics
st.header('Summary Statistics')
killed_female_total = clean_data['killed female'].sum()
killed_male_total = clean_data['killed male'].sum()
killed_undefined_total = clean_data['killed undefined'].sum()
total_injuries = clean_data['injured'].sum()
total_displaced = clean_data['displaced'].sum()
total_killed = clean_data['killed total'].sum()

st.write(f"**Total Female Killed:** {killed_female_total:,}")
st.write(f"**Total Male Killed:** {killed_male_total:,}")
st.write(f"**Total Undefined Killed:** {killed_undefined_total:,}")
st.write(f"**Total Injuries:** {total_injuries:,}")
st.write(f"**Total Displaced:** {total_displaced:,}")
st.write(f"**Total People Killed:** {total_killed:,}")

# Section 3: Total Killed and Injured Visualization
st.header('Total Killed and Injured Over Time')

fig, ax1 = plt.subplots(figsize=(10, 6))

# Plotting killed on the first axis
ax1.set_xlabel('Date')
ax1.set_ylabel('Killed', color='red')
ax1.plot(clean_data['date'], clean_data['killed total'], color='red', label='Total Killed')
ax1.tick_params(axis='y', labelcolor='red')

# Create a second y-axis for injured
ax2 = ax1.twinx()
ax2.set_ylabel('Injured', color='blue')
ax2.plot(clean_data['date'], clean_data['injured'], color='blue', label='Injured')
ax2.tick_params(axis='y', labelcolor='blue')

# Add a title
plt.title('Comparison of Killed and Injured Over Time')
st.pyplot(fig)

# Section 4: Total Killed by Gender Visualization
st.header('Total Killed by Gender')

gender_killed_totals = {
    'Killed Female': killed_female_total,
    'Killed Male': killed_male_total,
    'Killed Undefined': killed_undefined_total
}

# Function to format y-axis in Lakhs (L)
def lakhs_formatter(x, pos):
    return f'{int(x / 100000)}L'

fig, ax = plt.subplots(figsize=(10, 7))
ax.bar(gender_killed_totals.keys(), gender_killed_totals.values(), color=['orange', 'blue', 'green'])

# Adding titles and labels
plt.title('Total Killed by Gender')
plt.xlabel('Gender')
plt.ylabel('Number of Killed')

# Set y-axis intervals of 100,000 and format them in Lakhs (L)
plt.yticks(np.arange(0, max(gender_killed_totals.values()) + 100000, 100000))
ax.yaxis.set_major_formatter(plt.FuncFormatter(lakhs_formatter))
st.pyplot(fig)

# Section 5: Injured and Displaced Over Time
st.header('Injured and Displaced Over Time')

fig, ax = plt.subplots(figsize=(10, 6))
ax.plot(clean_data['date'], clean_data['injured'], label='Injured', color='blue')
ax.plot(clean_data['date'], clean_data['displaced'], label='Displaced', color='green')
plt.title('Injured and Displaced Over Time')
plt.xlabel('Date')
plt.ylabel('Count')
plt.legend()
plt.grid(True)
st.pyplot(fig)

# Section 6: Damaged Housing Units Over Time
st.header('Damaged Housing Units Over Time')

fig, ax = plt.subplots(figsize=(12, 6))
ax.plot(clean_data['date'], clean_data['damaged housing units'], label='Damaged Housing Units', color='purple')
plt.title('Damaged Housing Units Over Time')
plt.xlabel('Date')
plt.ylabel('Number of Units')
plt.legend()
plt.grid(True)
st.pyplot(fig)

# Section 7: Total Displaced People Over Time
st.header('Total Number of Displaced People Over Time')

fig, ax = plt.subplots(figsize=(12, 7))
ax.plot(clean_data['date'], clean_data['displaced'], label='Total Displaced', color='purple', marker='o', alpha=0.7)

plt.title('Total Number of Displaced People Over Time')
plt.xlabel('Date')
plt.ylabel('Total Number of Displaced People')

# Format the y-axis to show the exact count with commas for thousands
ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f'{int(x):,}'))

plt.grid(True)
plt.legend()
st.pyplot(fig)

# Section 8: Insights
st.header('Key Insights')
st.write(f"The total number of people displaced is **{total_displaced:,}**. The number of killed individuals is heavily gender-skewed, with a total of **{killed_male_total:,} males** and **{killed_female_total:,} females**. The number of housing units damaged is significant, affecting infrastructure severely.")
