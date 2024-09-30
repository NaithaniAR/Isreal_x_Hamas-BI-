import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import sys
sys.path.append('../')


#Pages
from libs.health_care_incidents.health_care_incidents import HCanalysis
from libs.displacement.displacement import main
from libs.civilian_fatalities.civfatalities import cfmain
from libs.pol_violence.pol_violance import pvmain

# Set page configuration
st.set_page_config(layout="wide", page_title="Israel-Hamas Conflict Analysis Dashboard")

# Sidebar with radio buttons

st.sidebar.title("Analysis Categories")
analysis_category = st.sidebar.radio(
    "Select a category to analyze:",
    ("Health Care Incidents", "Commodity Market", "Political Violance", 
     "Civilian Fatalities Analysis", "Gaza IDP", "Displacement due to Demolition")
)

# Main content
st.title("Israel-Hamas Conflict Analysis Dashboard")

@st.cache_data

def load_commodity_data():
    file_path = r"data-points\spreadsheets\xslx\commodity-prices-in-gaza-4-1.xlsx"
    commodity_data = pd.read_excel(file_path)
    commodity_data = commodity_data.drop(columns=['Unnamed: 0', 'commodity name (arabic)', 'amount (arabic)'])
    commodity_data['commodity name (english)'] = commodity_data['commodity name (english)'].str.replace(r'\(.*\)', '', regex=True).str.strip()
    commodity_data.columns = ['Commodity Name', 'Amount', 'Price-7th October', 
                              'average price after 7 October 2023', 'Monthly Percent Change % (Oct-Sep)', 
                              'Nov-23', 'Monthly Percent Change % (Nov-Oct)', 'Dec-23', 
                              'Monthly Percent Change % (Nov-Dec)', 'Jan-24', 
                              'Monthly Percent Change % (Dec-Jan)', 'Feb-24', 
                              'Monthly Percent Change % (Jan-Feb)', 'Mar-24', 
                              'Monthly Percent Change % (Feb-Mar)', 'Apr-24', 
                              'Monthly Percent Change % (Mar-Apr)', 'Acumulative change']
    return commodity_data
# Load the dataset
def load_health_data():
    file_path = r'/home/marktine/data Vis/Isreal_x_Hamas-BI-/libs/misic/data-points/spreadsheets/xslx/2023-2024-israel-and-opt-attacks-on-health-care-incident-data.xlsx'
    data = pd.read_excel(file_path)
    data_cleaned = data.dropna(axis=1)
    df = data_cleaned
    df['Date'] = pd.to_datetime(df['Date'], errors='coerce')
    return df



print('ok')

if analysis_category == "Health Care Incidents":

    HCanalysis.run_analysis()



elif analysis_category == "Commodity Market":

    commodity_data = load_commodity_data()

    st.header("Commodity Market Analysis")
    
    st.write("This analysis provides insights into the commodity market trends in Gaza during the Israel-Hamas conflict.")
    
    # Initial Commodity Prices
    st.subheader("Initial Commodity Prices")
    average_prices = commodity_data.groupby('Commodity Name')['average price after 7 October 2023'].mean()
    fig, ax = plt.subplots(figsize=(20, 10))
    average_prices.plot(kind='bar', color='skyblue', ax=ax)
    ax.set_title('Initial Commodity Prices after October 7, 2023')
    ax.set_xlabel('Commodity')
    ax.set_ylabel('Average Price')
    plt.xticks(rotation=90)
    plt.grid(axis='y')
    st.pyplot(fig)
    
    st.write("This chart shows the average prices of commodities immediately after October 7, 2023. We can observe significant variations in prices across different commodities, which may reflect their availability and demand during the conflict.")

    # Price Change Analysis
    st.subheader("Price Change Analysis")
    price_change_columns = ['% Sept-Oct', '% Oct-Nov', '% Nov-Dec', '% Dec-Jan', '% Jan-Feb', '% Feb-Mar', '% March-April']
    for col in price_change_columns:
        commodity_data[col] = ((commodity_data[col.replace('% ', '')] - commodity_data[col.replace('% ', '').replace('-', ' ').split()[0]]) / 
                                commodity_data[col.replace('% ', '').replace('-', ' ').split()[0]]) * 100

    price_change_data = commodity_data[['Commodity Name'] + price_change_columns].melt(id_vars=['Commodity Name'], var_name='Period', value_name='Percent Change')
    
    fig, ax = plt.subplots(figsize=(15, 8))
    sns.boxplot(x='Period', y='Percent Change', data=price_change_data, ax=ax)
    ax.set_title('Distribution of Price Changes Over Time')
    ax.set_xlabel('Time Period')
    ax.set_ylabel('Percent Change')
    plt.xticks(rotation=45)
    st.pyplot(fig)
    
    st.write("This box plot illustrates the distribution of price changes for all commodities over different time periods. The wide range of price changes, especially in the initial months, reflects the market's volatility during the conflict.")

    # Most Volatile Commodities
    st.subheader("Most Volatile Commodities")
    commodity_data['Price Volatility'] = commodity_data[['Nov-23', 'Dec-23', 'Jan-24', 'Feb-24', 'Mar-24', 'Apr-24']].std(axis=1)
    top_volatile = commodity_data.nlargest(10, 'Price Volatility')
    
    fig, ax = plt.subplots(figsize=(12, 6))
    sns.barplot(x='Price Volatility', y='Commodity Name', data=top_volatile, ax=ax)
    ax.set_title('Top 10 Most Volatile Commodities')
    ax.set_xlabel('Price Volatility (Standard Deviation)')
    ax.set_ylabel('Commodity')
    st.pyplot(fig)
    
    st.write("This chart shows the commodities with the highest price volatility. These items experienced the most significant price fluctuations, likely due to supply chain disruptions, changes in demand, or other conflict-related factors.")

    # Cumulative Price Change
    st.subheader("Cumulative Price Change")
    top_cumulative_change = commodity_data.nlargest(10, 'Acumulative change')
    
    fig, ax = plt.subplots(figsize=(12, 6))
    sns.barplot(x='Acumulative change', y='Commodity Name', data=top_cumulative_change, ax=ax)
    ax.set_title('Top 10 Commodities by Cumulative Price Change')
    ax.set_xlabel('Cumulative Price Change (%)')
    ax.set_ylabel('Commodity')
    st.pyplot(fig)
    
    st.write("This chart displays the commodities with the highest cumulative price changes. These items have seen the most significant overall increase in price since the start of the conflict, indicating severe supply issues or increased demand.")

    # Conclusion
    st.subheader("Key Takeaways")
    st.write("1. The conflict has led to significant volatility in commodity prices, with some items experiencing extreme fluctuations.")
    st.write("2. Certain commodities have seen substantial cumulative price increases, potentially making them unaffordable for many residents.")
    st.write("3. The initial months of the conflict saw the most dramatic price changes, likely due to immediate supply chain disruptions and panic buying.")
    st.write("4. Essential items like food and fuel appear to be among the most affected, which could have severe implications for the population's well-being.")
    st.write("5. The ongoing volatility in prices suggests that the market has not stabilized, indicating continued challenges in supply and distribution.")

elif analysis_category == "Political Violance":
    st.header("Necessary Dependencies Analysis")
    st.write("This section is under development. It will analyze the impact of the conflict on essential resources and infrastructure.")
    pvmain()

elif analysis_category == "Civilian Fatalities Analysis":
    st.header("Civilian Fatalities Analysis")
    st.write("This section is under development. It will provide a detailed analysis of civilian casualties during the conflict.")
    cfmain()

elif analysis_category == "Gaza IDP":
    st.header("Gaza Internally Displaced Persons (IDP) Analysis")
    st.write("This section is under development. It will examine the situation of internally displaced persons in Gaza.")

elif analysis_category == "Displacement due to Demolition":
    st.header("Displacement due to Demolition Analysis")
    st.write("This section is under development. It will analyze displacement caused by the demolition of structures during the conflict.")
    main()

# Add a note about the data source
st.sidebar.markdown("---")
st.sidebar.info("Data source: WHO Surveillance System for Attacks on Health Care (SSA)")

# Instructions for running the app
st.sidebar.markdown("---")
st.sidebar.info("To run this app:\n1. Save the code to a file (e.g., dashboard.py)\n2. Install required libraries: streamlit, pandas, matplotlib, seaborn\n3. Run 'streamlit run dashboard.py' in your terminal")