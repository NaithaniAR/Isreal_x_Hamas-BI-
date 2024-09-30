# Import necessary libraries
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import numpy as np
import sys
sys.path.append('../')

class DataAnalyzer:
    def __init__(self, file_path):
        self.file_path = file_path
        self.data = self.load_data()
        self.clean_data = self.clean_data()

    def load_data(self):
        """Load dataset from the given file path."""
        try:
            return pd.read_excel(self.file_path)
        except Exception as e:
            print(f"Error reading Excel file: {e}")
            return None

    def clean_data(self):
        """Clean the dataset by removing empty columns and converting dates."""
        if self.data is None:
            return None
        clean_data = self.data.dropna(axis=1, how='all')
        clean_data['date'] = pd.to_datetime(clean_data['date'])
        return clean_data


    def get_summary_statistics(self):
        """Compute summary statistics."""
        return {
            'killed_female_total': self.clean_data['killed female'].sum(),
            'killed_male_total': self.clean_data['killed male'].sum(),
            'killed_undefined_total': self.clean_data['killed undefined'].sum(),
            'total_injuries': self.clean_data['injured'].sum(),
            'total_displaced': self.clean_data['displaced'].sum(),
            'total_killed': self.clean_data['killed total'].sum(),
        }

class DataVisualizer:
    def __init__(self, clean_data):
        self.clean_data = clean_data

    def plot_killed_and_injured(self):
        """Plot total killed and injured over time."""
        fig, ax1 = plt.subplots(figsize=(10, 6))

        ax1.set_xlabel('Date')
        ax1.set_ylabel('Killed', color='red')
        ax1.plot(self.clean_data['date'], self.clean_data['killed total'], color='red', label='Total Killed')
        ax1.tick_params(axis='y', labelcolor='red')

        ax2 = ax1.twinx()
        ax2.set_ylabel('Injured', color='blue')
        ax2.plot(self.clean_data['date'], self.clean_data['injured'], color='blue', label='Injured')
        ax2.tick_params(axis='y', labelcolor='blue')

        plt.title('Comparison of Killed and Injured Over Time')
        return fig

    def plot_killed_by_gender(self, gender_killed_totals):
        """Plot total killed by gender."""
        fig, ax = plt.subplots(figsize=(10, 7))
        ax.bar(gender_killed_totals.keys(), gender_killed_totals.values(), color=['orange', 'blue', 'green'])

        plt.title('Total Killed by Gender')
        plt.xlabel('Gender')
        plt.ylabel('Number of Killed')

        plt.yticks(np.arange(0, max(gender_killed_totals.values()) + 100000, 100000))
        ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, pos: f'{int(x / 100000)}L'))
        return fig

    def plot_injured_and_displaced(self):
        """Plot injured and displaced over time."""
        fig, ax = plt.subplots(figsize=(10, 6))
        ax.plot(self.clean_data['date'], self.clean_data['injured'], label='Injured', color='blue')
        ax.plot(self.clean_data['date'], self.clean_data['displaced'], label='Displaced', color='green')

        plt.title('Injured and Displaced Over Time')
        plt.xlabel('Date')
        plt.ylabel('Count')
        plt.legend()
        plt.grid(True)
        return fig

    def plot_damaged_housing_units(self):
        """Plot damaged housing units over time."""
        fig, ax = plt.subplots(figsize=(12, 6))
        ax.plot(self.clean_data['date'], self.clean_data['damaged housing units'], label='Damaged Housing Units', color='purple')

        plt.title('Damaged Housing Units Over Time')
        plt.xlabel('Date')
        plt.ylabel('Number of Units')
        plt.legend()
        plt.grid(True)
        return fig

    def plot_total_displaced(self):
        """Plot total number of displaced people over time."""
        fig, ax = plt.subplots(figsize=(12, 7))
        ax.plot(self.clean_data['date'], self.clean_data['displaced'], label='Total Displaced', color='purple', marker='o', alpha=0.7)

        plt.title('Total Number of Displaced People Over Time')
        plt.xlabel('Date')
        plt.ylabel('Total Number of Displaced People')
        ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f'{int(x):,}'))

        plt.grid(True)
        plt.legend()
        return fig

def main():
    # File path for the dataset
    file_path = r'/home/marktine/data Vis/Isreal_x_Hamas-BI-/libs/misic/data-points/spreadsheets/xslx/palestine_hrp_civilian_targeting_events_and_fatalities_by_month-year_as-of-29may2024.xlsx'
    
    # Load and clean data
    data_analyzer = DataAnalyzer(file_path)
    clean_data = data_analyzer.clean_data

    # Streamlit App
    st.title('Israel-Hamas Conflict: Data Analysis and Visualization')

    # Section 1: Display Raw Data
    st.header('Dataset Preview')
    st.write(clean_data.head())

    # Section 2: Summary Statistics
    st.header('Summary Statistics')
    summary_stats = data_analyzer.get_summary_statistics()

    st.write(f"**Total Female Killed:** {summary_stats['killed_female_total']:,}")
    st.write(f"**Total Male Killed:** {summary_stats['killed_male_total']:,}")
    st.write(f"**Total Undefined Killed:** {summary_stats['killed_undefined_total']:,}")
    st.write(f"**Total Injuries:** {summary_stats['total_injuries']:,}")
    st.write(f"**Total Displaced:** {summary_stats['total_displaced']:,}")
    st.write(f"**Total People Killed:** {summary_stats['total_killed']:,}")

    # Section 3: Total Killed and Injured Visualization
    st.header('Total Killed and Injured Over Time')
    visualizer = DataVisualizer(clean_data)
    fig_killed_injured = visualizer.plot_killed_and_injured()
    st.pyplot(fig_killed_injured)

    # Section 4: Total Killed by Gender Visualization
    st.header('Total Killed by Gender')
    gender_killed_totals = {
        'Killed Female': summary_stats['killed_female_total'],
        'Killed Male': summary_stats['killed_male_total'],
        'Killed Undefined': summary_stats['killed_undefined_total']
    }
    fig_killed_gender = visualizer.plot_killed_by_gender(gender_killed_totals)
    st.pyplot(fig_killed_gender)

    # Section 5: Injured and Displaced Over Time
    st.header('Injured and Displaced Over Time')
    fig_injured_displaced = visualizer.plot_injured_and_displaced()
    st.pyplot(fig_injured_displaced)

    # Section 6: Damaged Housing Units Over Time
    st.header('Damaged Housing Units Over Time')
    fig_damaged_housing = visualizer.plot_damaged_housing_units()
    st.pyplot(fig_damaged_housing)

    # Section 7: Total Displaced People Over Time
    st.header('Total Number of Displaced People Over Time')
    fig_total_displaced = visualizer.plot_total_displaced()
    st.pyplot(fig_total_displaced)

    # Section 8: Insights
    st.header('Key Insights')
    st.write(f"The total number of people displaced is **{summary_stats['total_displaced']:,}**. The number of killed individuals is heavily gender-skewed, with a total of **{summary_stats['killed_male_total']:,} males** and **{summary_stats['killed_female_total']:,} females**.")

if __name__ == "__main__":
    main()
