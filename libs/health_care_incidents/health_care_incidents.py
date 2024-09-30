import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st

import sys
sys.path.append('../')

class HealthCareIncidentsAnalysis:
    def __init__(self, data_loader):
        self.df = data_loader()

    def run_analysis(self):
        st.header("Health Care Incidents Analysis")
        st.write("This analysis provides insights into the health care incidents during the Israel-Hamas conflict.")
        
        self.plot_time_series()
        self.plot_incidents_by_location()
        self.analyze_impact_on_health_workers()
        self.plot_weapon_usage()
        self.conclude_analysis()

    def plot_time_series(self):
        st.subheader("Incidents Over Time")
        df_time_series = self.df.groupby(self.df['Date'].dt.to_period('M')).size()
        fig, ax = plt.subplots(figsize=(12, 6))
        df_time_series.plot(kind='line', marker='o', ax=ax)
        ax.set_title('Number of Incidents Over Time (Monthly)')
        ax.set_ylabel('Number of Incidents')
        ax.set_xlabel('Date (Monthly)')
        plt.xticks(rotation=45)
        plt.grid(True)
        st.pyplot(fig)
        
        st.write("The graph shows the trend of health care incidents over time. We can observe periods of increased activity, which may correlate with escalations in the conflict.")

    def plot_incidents_by_location(self):
        st.subheader("Top Locations by Number of Incidents")
        df_location = self.df['Admin 1'].value_counts().head(10)
        fig, ax = plt.subplots(figsize=(12, 6))
        df_location.plot(kind='bar', ax=ax)
        ax.set_title('Top Locations by Number of Incidents')
        ax.set_ylabel('Number of Incidents')
        ax.set_xlabel('Location')
        plt.xticks(rotation=45)
        st.pyplot(fig)
        
        st.write("This chart highlights the areas most affected by health care incidents. Understanding the geographical distribution can help in allocating resources and planning interventions.")

    def analyze_impact_on_health_workers(self):
        st.subheader("Impact on Health Workers")
        df_workers_impacted = self.df[['Health Workers Killed', 'Health Workers Injured', 'Health Workers Kidnapped']].apply(pd.to_numeric, errors='coerce')
        impact_totals = df_workers_impacted.sum()
        
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))
        
        # Bar chart for total killed
        ax1.bar('Health Workers Killed', impact_totals['Health Workers Killed'], color='red')
        ax1.set_title('Total Number of Health Workers Killed')
        ax1.set_ylabel('Number of People')
        
        # Pie chart for overall impact
        colors = ['#ff9999','#66b3ff','#99ff99']
        ax2.pie(impact_totals, labels=impact_totals.index, autopct='%1.1f%%', startangle=90, colors=colors, shadow=True)
        ax2.set_title('Distribution of Impact on Health Workers')
        
        st.pyplot(fig)
        
        st.write(f"The data shows a significant impact on health workers. {int(impact_totals['Health Workers Killed'])} health workers have been killed, which is a tragic loss for the healthcare system and the communities they serve.")
        st.write(f"Additionally, {int(impact_totals['Health Workers Injured'])} have been injured and {int(impact_totals['Health Workers Kidnapped'])} kidnapped, further straining the healthcare capacity in the affected areas.")

    def plot_weapon_usage(self):
        st.subheader("Weapons Used in Incidents")
        weapon_counts = self.df['Weapon Carried/Used'].value_counts()
        
        fig, ax = plt.subplots(figsize=(12, 6))
        weapon_counts.plot(kind='bar', ax=ax)
        ax.set_title('Frequency of Weapons Used')
        ax.set_ylabel('Number of Incidents')
        ax.set_xlabel('Weapon Type')
        plt.xticks(rotation=45, ha='right')
        st.pyplot(fig)
        
        st.write("This chart shows the types of weapons most frequently used in incidents affecting healthcare. Understanding the nature of these attacks can inform protective measures and international advocacy efforts.")

    def conclude_analysis(self):
        st.subheader("Key Takeaways")
        st.write("1. The conflict has had a severe impact on healthcare infrastructure and personnel.")
        st.write("2. Certain areas are disproportionately affected, suggesting a need for targeted interventions.")
        st.write("3. The loss of health workers will have long-lasting effects on the healthcare system's capacity.")
        st.write("4. A variety of weapons have been used in these incidents, highlighting the complex nature of the threats faced by healthcare providers.")
        st.write("5. Continuous monitoring and reporting of these incidents is crucial for advocacy and protection efforts.")

# Usage
def load_health_data():
    # Replace this with your actual data loading logic
    file_path = r'/home/marktine/data Vis/Isreal_x_Hamas-BI-/libs/misic/data-points/spreadsheets/xslx/2023-2024-israel-and-opt-attacks-on-health-care-incident-data.xlsx'
    data = pd.read_excel(file_path)
    data_cleaned = data.dropna(axis=1)
    df = data_cleaned
    df['Date'] = pd.to_datetime(df['Date'], errors='coerce')

    return df

HCanalysis = HealthCareIncidentsAnalysis(load_health_data)

