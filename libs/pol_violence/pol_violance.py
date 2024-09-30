import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

class DataLoader:
    @staticmethod
    @st.cache_data
    def load_data(file_path):
        """Load data from an Excel file and process it."""
        df = pd.read_excel(file_path, sheet_name='Data')
        df['month_of_year'] = df['Month'].str[:3] + '-' + df['Year'].astype(str).str[-2:]
        df['Fatalities'] = df['Fatalities'].astype(int)
        return df


class Dashboard:
    def __init__(self, df):
        self.df = df

    def display_title(self):
        st.title('Israel-Hamas Conflict Dashboard')
        st.write("""
        This dashboard provides an analysis of political violence events and fatalities 
        in the Israel-Hamas conflict from 2016 to 2024.
        """)

    def display_yearly_metrics(self):
        """Calculate and display yearly metrics and their visualizations."""
        yearly_metrics = self.df.groupby('Year').agg(
            total_events=('Events', 'sum'),
            total_fatalities=('Fatalities', 'sum'),
            avg_events=('Events', 'mean'),
            avg_fatalities=('Fatalities', 'mean')
        ).reset_index()

        st.header('Events and Fatalities by Year')
        fig, ax = plt.subplots(1, 2, figsize=(15, 6))

        ax[0].bar(yearly_metrics['Year'], yearly_metrics['total_events'], color='skyblue')
        ax[0].set_title('Total Events by Year')
        ax[0].set_xlabel('Year')
        ax[0].set_ylabel('Total Events')

        ax[1].bar(yearly_metrics['Year'], yearly_metrics['total_fatalities'], color='salmon')
        ax[1].set_title('Total Fatalities by Year')
        ax[1].set_xlabel('Year')
        ax[1].set_ylabel('Total Fatalities')

        plt.tight_layout()
        st.pyplot(fig)

        st.write("""
        The graphs show a significant spike in both events and fatalities in 2023 and 2024, 
        indicating an escalation in the conflict during these years.
        """)

    def display_monthly_trend(self):
        """Display the trend of total events by month-year."""
        st.header('Trend of Total Events by Month-Year')
        events_by_month_year = self.df.groupby('month_of_year')['Events'].sum().reset_index()
        events_by_month_year.sort_values(by='month_of_year', inplace=True)

        fig, ax = plt.subplots(figsize=(20, 6))
        ax.plot(events_by_month_year['month_of_year'], events_by_month_year['Events'], marker='o', linestyle='-', color='b')
        ax.set_xticklabels(events_by_month_year['month_of_year'], rotation=90)
        ax.set_xlabel('Month-Year')
        ax.set_ylabel('Total Events')
        ax.set_title('Trend of Total Events by Month-Year')
        ax.grid(True)

        st.pyplot(fig)

        st.write("""
        The trend line shows periodic spikes in events, with a massive increase in late 2023 and early 2024.
        """)

    def display_fatalities_by_region(self):
        """Display total fatalities by region."""
        st.header('Fatalities by Region')
        fatalities_by_region = self.df.groupby('Admin2')['Fatalities'].sum().reset_index()

        fig, ax = plt.subplots(figsize=(12, 6))
        ax.bar(fatalities_by_region['Admin2'], fatalities_by_region['Fatalities'], color='teal')
        ax.set_xlabel('Region (Admin2)')
        ax.set_ylabel('Total Fatalities')
        ax.set_title('Total Fatalities by Region (Admin2)')
        plt.xticks(rotation=45, ha='right')

        st.pyplot(fig)

        st.write("""
        The chart reveals that Gaza has suffered the highest number of fatalities, 
        followed by North Gaza and Khan Yunis.
        """)

    def display_correlation_heatmap(self):
        """Display the correlation heatmap between events and fatalities."""
        st.header('Correlation between Events and Fatalities')
        correlation_data = self.df[['Events', 'Fatalities']]
        correlation_matrix = correlation_data.corr()

        fig, ax = plt.subplots(figsize=(8, 6))
        sns.heatmap(correlation_matrix, annot=True, cmap="coolwarm", vmin=-1, vmax=1, ax=ax)
        ax.set_title('Correlation Heatmap: Events and Fatalities')

        st.pyplot(fig)

        st.write("""
        The heatmap shows a strong positive correlation (0.84) between the number of events and fatalities, 
        indicating that as the number of violent events increases, so does the number of fatalities.
        """)

    def display_fatalities_heatmap_by_region_year(self):
        """Display fatalities heatmap by region and year."""
        st.header('Fatalities Heatmap by Region and Year')
        fatalities_pivot = self.df.pivot_table(values='Fatalities', index='Admin2', columns='Year', aggfunc='sum', fill_value=0)

        fig, ax = plt.subplots(figsize=(12, 8))
        sns.heatmap(fatalities_pivot, annot=True, cmap="Reds", linewidths=0.5, linecolor='white', ax=ax)
        ax.set_title('Total Fatalities Heatmap by Region (Admin2) and Year')
        ax.set_xlabel('Year')
        ax.set_ylabel('Region (Admin2)')

        st.pyplot(fig)

        st.write("""
        The heatmap illustrates the concentration of fatalities across different regions over the years. 
        It clearly shows the intense escalation of the conflict in Gaza and surrounding areas in 2023 and 2024.
        """)

    def display_conclusion(self):
        """Display the conclusion of the dashboard analysis."""
        st.header('Conclusion')
        st.write("""
        This dashboard tells a story of escalating conflict between Israel and Hamas from 2016 to 2024. 
        Key observations include:

        1. A dramatic increase in both events and fatalities in 2023 and 2024, marking a significant escalation in the conflict.
        2. Gaza and its surrounding areas (North Gaza, Khan Yunis) have been the most affected regions, with the highest number of fatalities.
        3. There is a strong correlation between the number of violent events and fatalities, suggesting that more frequent conflicts lead to higher casualties.
        4. The conflict has seen periodic spikes over the years, but the scale of violence in recent years is unprecedented in this dataset.
        5. The geographical concentration of fatalities has shifted over time, with Gaza becoming the epicenter of the conflict in recent years.

        This data underscores the human cost of the ongoing conflict and highlights the urgent need for peaceful resolution and humanitarian intervention in the affected regions.
        """)


def pvmain():
    # Load data
    file_path = '/home/marktine/data Vis/Isreal_x_Hamas-BI-/libs/misic/data-points/spreadsheets/xslx/palestine_hrp_political_violence_events_and_fatalities_by_month-year_as-of-29may2024.xlsx'
    df = DataLoader.load_data(file_path)

    # Initialize Dashboard
    dashboard = Dashboard(df)

    # Display Dashboard components
    dashboard.display_title()
    dashboard.display_yearly_metrics()
    dashboard.display_monthly_trend()
    dashboard.display_fatalities_by_region()
    dashboard.display_correlation_heatmap()
    dashboard.display_fatalities_heatmap_by_region_year()
    dashboard.display_conclusion()


if __name__ == '__main__':
    pvmain()
