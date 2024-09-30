import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import sys
sys.path.append('../')



@st.cache_data
def load_data():
    """Load data from Excel and preprocess it."""
    file_path = 'libs\misic\data-points\spreadsheets\xslx\palestine_hrp_civilian_targeting_events_and_fatalities_by_month-year_as-of-29may2024.xlsx'
    df = pd.read_excel(file_path, sheet_name='Data')
    df['month_of_year'] = df['Month'].str[:3] + '-' + df['Year'].astype(str).str[-2:]
    df['Fatalities'] = df['Fatalities'].astype(int)
    return df


class PalestineDashboard:
    def __init__(self):
        self.df = load_data()  # Load data using the standalone function
        self.filtered_df = None

    def filter_data(self, selected_years, selected_regions):
        """Filter the dataframe based on selected years and regions."""
        self.filtered_df = self.df[(self.df['Year'].isin(selected_years)) & (self.df['Admin1'].isin(selected_regions))]

    def calculate_yearly_metrics(self):
        """Calculate yearly metrics for the filtered data."""
        return self.filtered_df.groupby('Year').agg(
            total_events=('Events', 'sum'),
            total_fatalities=('Fatalities', 'sum'),
            avg_events=('Events', 'mean'),
            avg_fatalities=('Fatalities', 'mean')
        ).reset_index()

    def display_metrics(self, metrics):
        """Display key metrics in the sidebar."""
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Total Events", metrics['total_events'].sum())
        col2.metric("Total Fatalities", metrics['total_fatalities'].sum())
        col3.metric("Avg Events per Year", round(metrics['avg_events'].mean(), 2))
        col4.metric("Avg Fatalities per Year", round(metrics['avg_fatalities'].mean(), 2))

    def plot_total_events_by_year(self, metrics):
        """Plot total events by year."""
        st.subheader("Total Events by Year")
        fig = px.bar(metrics, x='Year', y='total_events', title='Total Events by Year')
        st.plotly_chart(fig, use_container_width=True)

    def plot_total_fatalities_by_year(self, metrics):
        """Plot total fatalities by year."""
        st.subheader("Total Fatalities by Year")
        fig = px.bar(metrics, x='Year', y='total_fatalities', title='Total Fatalities by Year')
        st.plotly_chart(fig, use_container_width=True)

    def plot_trend_by_month_year(self):
        """Plot trend of total events by month-year."""
        st.subheader("Trend of Total Events by Month-Year")
        events_by_month_year = self.filtered_df.groupby('month_of_year')['Events'].sum().reset_index()
        events_by_month_year = events_by_month_year.sort_values('month_of_year')
        fig = px.line(events_by_month_year, x='month_of_year', y='Events', title='Trend of Total Events by Month-Year')
        st.plotly_chart(fig, use_container_width=True)

    def plot_fatalities_by_region(self):
        """Plot total fatalities by region."""
        st.subheader("Total Fatalities by Region")
        fatalities_by_region = self.filtered_df.groupby('Admin2')['Fatalities'].sum().reset_index()
        fig = px.bar(fatalities_by_region, x='Admin2', y='Fatalities', title='Total Fatalities by Region (Admin2)')
        fig.update_layout(xaxis_tickangle=-45)
        st.plotly_chart(fig, use_container_width=True)

    def plot_bubble_chart(self):
        """Plot a bubble chart of fatalities by region and year."""
        st.subheader("Bubble Chart of Fatalities by Region and Year")
        fig = px.scatter(self.filtered_df, x='Admin2', y='Year', size='Fatalities', color='Admin1',
                         title='Bubble Chart of Fatalities by Region (Admin2) and Year')
        fig.update_layout(xaxis_tickangle=-45)
        st.plotly_chart(fig, use_container_width=True)

    def plot_correlation_heatmap(self):
        """Plot a correlation heatmap between events and fatalities."""
        st.subheader("Correlation Heatmap: Events and Fatalities")
        correlation_data = self.filtered_df[['Events', 'Fatalities']]
        correlation_matrix = correlation_data.corr()
        fig, ax = plt.subplots()
        sns.heatmap(correlation_matrix, annot=True, cmap="coolwarm", vmin=-1, vmax=1, ax=ax)
        st.pyplot(fig)

    def plot_total_events_heatmap(self):
        """Plot total events heatmap by region and year."""
        st.subheader("Total Events Heatmap by Region and Year")
        events_pivot = self.filtered_df.pivot_table(values='Events', index='Admin1', columns='Year', aggfunc='sum', fill_value=0)
        fig = px.imshow(events_pivot, title='Total Events Heatmap by Region (Admin1) and Year')
        st.plotly_chart(fig, use_container_width=True)

    def plot_total_fatalities_heatmap(self):
        """Plot total fatalities heatmap by region and year."""
        st.subheader("Total Fatalities Heatmap by Region and Year")
        fatalities_pivot = self.filtered_df.pivot_table(values='Fatalities', index='Admin2', columns='Year', aggfunc='sum', fill_value=0)
        fig = px.imshow(fatalities_pivot, title='Total Fatalities Heatmap by Region (Admin2) and Year')
        st.plotly_chart(fig, use_container_width=True)


def cfmain():
    # Set page configuration
    # st.set_page_config(page_title="Palestine Civilian Targeting Events Dashboard", layout="wide")

    # Initialize the dashboard
    dashboard = PalestineDashboard()

    # Main title
    st.title("Palestine Civilian Targeting Events Dashboard")

    # Sidebar for filtering
    st.sidebar.header("Filters")
    selected_years = st.sidebar.multiselect("Select Years", options=sorted(dashboard.df['Year'].unique()), 
                                             default=sorted(dashboard.df['Year'].unique()))
    selected_regions = st.sidebar.multiselect("Select Regions", options=sorted(dashboard.df['Admin1'].unique()), 
                                               default=sorted(dashboard.df['Admin1'].unique()))

    # Filter the dataframe
    dashboard.filter_data(selected_years, selected_regions)

    # Calculate yearly metrics
    yearly_metrics = dashboard.calculate_yearly_metrics()

    # Display metrics
    dashboard.display_metrics(yearly_metrics)

    # Create two columns for charts
    col1, col2 = st.columns(2)

    with col1:
        dashboard.plot_total_events_by_year(yearly_metrics)

    with col2:
        dashboard.plot_total_fatalities_by_year(yearly_metrics)

    # Other visualizations
    dashboard.plot_trend_by_month_year()
    dashboard.plot_fatalities_by_region()
    dashboard.plot_bubble_chart()
    dashboard.plot_correlation_heatmap()
    dashboard.plot_total_events_heatmap()
    dashboard.plot_total_fatalities_heatmap()


if __name__ == "__main__":
    cfmain()
