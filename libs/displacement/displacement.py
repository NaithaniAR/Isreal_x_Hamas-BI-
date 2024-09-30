import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import sys
sys.path.append('../')

class DisplacementDashboard:
    def __init__(self, data_path):
        self.data_path = data_path
        self.idps_since_2009 = None
        self.idps_by_year = None
        self.load_data()

    def load_data(self):
        """Load the data from Excel files."""
        self.idps_since_2009 = pd.read_excel(self.data_path, sheet_name='IDPs in WestBank since 2009')
        self.idps_by_year = pd.read_excel(self.data_path, sheet_name='IDPs in WestBank by Year')

    def calculate_totals(self):
        """Calculate total statistics."""
        totals = {
            "total_demolished_structures": self.idps_since_2009['Demolished Structures'].sum(),
            "total_displaced_people": self.idps_since_2009['IDPs'].sum(),
            "total_affected_people": self.idps_since_2009['Affected people'].sum()
        }
        return totals

    def display_metrics(self, totals):
        """Display key figures in Streamlit."""
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric(label="Total Demolished Structures", value=totals['total_demolished_structures'])
        with col2:
            st.metric(label="Total Displaced People", value=totals['total_displaced_people'])
        with col3:
            st.metric(label="Total Affected People", value=totals['total_affected_people'])

    def plot_idps_by_governorate(self):
        """Plot total IDPs by Governorate."""
        st.subheader("Total Internally Displaced Persons (IDPs) by Governorate (2009-present)")
        fig, ax = plt.subplots(figsize=(14, 6))
        sns.barplot(data=self.idps_since_2009, x='Governorate', y='IDPs', palette='viridis', ax=ax)
        ax.set_title('Total Internally Displaced Persons (2009-present)')
        ax.set_xticklabels(ax.get_xticklabels(), rotation=45)
        ax.set_ylabel('IDPs')
        st.pyplot(fig)

    def plot_idps_over_time(self):
        """Plot the number of IDPs over time by governorate."""
        st.subheader("Number of IDPs over Time (Yearly)")
        fig = px.line(self.idps_by_year, x='Year', y='IDPs', color='Governorate',
                      title='Number of IDPs over Time (Yearly)',
                      labels={'IDPs': 'Number of Internally Displaced Persons', 'Year': 'Year'},
                      markers=True)
        fig.update_layout(hovermode="x unified", template="plotly_white")
        st.plotly_chart(fig)

    def plot_demolished_structures_and_affected_people(self):
        """Plot demolished structures and affected people by governorate."""
        st.subheader("Demolished Structures and Affected People by Governorate (2009-present)")
        fig, axs = plt.subplots(1, 2, figsize=(15, 7))
        axs[0].bar(self.idps_since_2009['Governorate'], self.idps_since_2009['Demolished Structures'], color='gray')
        axs[0].set_title('Demolished Structures')
        axs[0].set_ylabel('Number of Structures')
        axs[0].set_xticklabels(self.idps_since_2009['Governorate'], rotation=45, ha='right')

        axs[1].bar(self.idps_since_2009['Governorate'], self.idps_since_2009['Affected people'], color='salmon')
        axs[1].set_title('Affected People')
        axs[1].set_ylabel('Number of People')
        axs[1].set_xticklabels(self.idps_since_2009['Governorate'], rotation=45, ha='right')

        plt.tight_layout()
        st.pyplot(fig)

    def plot_histograms(self):
        """Plot various histograms."""
        st.subheader("Distribution of Demolished Structures by Governorate")
        fig = px.histogram(self.idps_by_year, x='Governorate', y='Demolished Structures', 
                           nbins=len(self.idps_by_year['Governorate'].unique()), 
                           title='Distribution of Demolished Structures by Governorate',
                           labels={'Demolished Structures': 'Number of Demolished Structures', 'Governorate': 'Governorate'},
                           color='Year', barmode='group')
        fig.update_layout(template="plotly_white", bargap=0.2)
        st.plotly_chart(fig)

        st.subheader("Distribution of Demolished Structures by Year")
        fig = px.histogram(self.idps_by_year, x='Year', y='Demolished Structures',
                           nbins=len(self.idps_by_year['Year'].unique()),
                           title='Distribution of Demolished Structures by Year',
                           labels={'Demolished Structures': 'Number of Demolished Structures', 'Year': 'Year'},
                           color='Governorate', barmode='stack')
        fig.update_layout(template="plotly_white", bargap=0.05, bargroupgap=0.1,
                          title={'text': "Distribution of Demolished Structures by Year",
                                 'y': 0.9, 'x': 0.5, 'xanchor': 'center', 'yanchor': 'top'})
        fig.update_xaxes(tickmode='linear', tick0=1, dtick=1)
        st.plotly_chart(fig)

    def plot_bubble_chart(self):
        """Plot bubble chart for affected people over time."""
        st.subheader("Affected People Over Time by Governorate")
        fig = px.scatter(self.idps_by_year, x='Year', y='Governorate', size='Affected people', color='Governorate',
                         title='Affected People Over Time by Governorate', size_max=60)
        fig.update_layout(template="plotly_white")
        st.plotly_chart(fig)

def main():
    # Streamlit title
    st.title("Displacement Due to Demolitions in West Bank")
    
    # Path to data
    data_path = r'/home/marktine/data Vis/Isreal_x_Hamas-BI-/libs/misic/data-points/spreadsheets/xslx/West Bank - Displacement due to Demolitions.xlsx'
    
    # Create the dashboard
    dashboard = DisplacementDashboard(data_path)

    # Calculate totals and display metrics
    totals = dashboard.calculate_totals()
    dashboard.display_metrics(totals)

    # Generate various plots
    dashboard.plot_idps_by_governorate()
    dashboard.plot_idps_over_time()
    dashboard.plot_demolished_structures_and_affected_people()
    dashboard.plot_histograms()
    dashboard.plot_bubble_chart()

if __name__ == "__main__":
    main()
