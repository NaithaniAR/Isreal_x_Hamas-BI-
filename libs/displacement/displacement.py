import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px

# Load the data
idps_since_2009 = pd.read_excel(r'libs\data-points\spreadsheets\xslx\West Bank - Displacement due to Demolitions.xlsx', sheet_name='IDPs in WestBank since 2009')
idps_by_year = pd.read_excel(r'libs\data-points\spreadsheets\xslx\West Bank - Displacement due to Demolitions.xlsx', sheet_name='IDPs in WestBank by Year')

# Streamlit title
st.title("Displacement Due to Demolitions in West Bank")

# Calculate total stats
total_demolished_structures = idps_since_2009['Demolished Structures'].sum()
total_displaced_people = idps_since_2009['IDPs'].sum()
total_affected_people = idps_since_2009['Affected people'].sum()

# Display key figures using columns in Streamlit
col1, col2, col3 = st.columns(3)
with col1:
    st.metric(label="Total Demolished Structures", value=total_demolished_structures)
with col2:
    st.metric(label="Total Displaced People", value=total_displaced_people)
with col3:
    st.metric(label="Total Affected People", value=total_affected_people)

# Barplot: Total Internally Displaced Persons (2009-present) by Governorate
st.subheader("Total Internally Displaced Persons (IDPs) by Governorate (2009-present)")
fig, ax = plt.subplots(figsize=(14, 6))
sns.barplot(data=idps_since_2009, x='Governorate', y='IDPs', palette='viridis', ax=ax)
ax.set_title('Total Internally Displaced Persons (2009-present)')
ax.set_xticklabels(ax.get_xticklabels(), rotation=45)
ax.set_ylabel('IDPs')
st.pyplot(fig)

# Plotly interactive line plot: Number of IDPs over time by governorate
st.subheader("Number of IDPs over Time (Yearly)")
fig = px.line(idps_by_year, x='Year', y='IDPs', color='Governorate',
              title='Number of IDPs over Time (Yearly)',
              labels={'IDPs': 'Number of Internally Displaced Persons', 'Year': 'Year'},
              markers=True)
fig.update_layout(hovermode="x unified", template="plotly_white")
st.plotly_chart(fig)

# Matplotlib bar charts for Demolished Structures and Affected People by Governorate
st.subheader("Demolished Structures and Affected People by Governorate (2009-present)")
fig, axs = plt.subplots(1, 2, figsize=(15, 7))
axs[0].bar(idps_since_2009['Governorate'], idps_since_2009['Demolished Structures'], color='gray')
axs[0].set_title('Demolished Structures')
axs[0].set_ylabel('Number of Structures')
axs[0].set_xticklabels(idps_since_2009['Governorate'], rotation=45, ha='right')

axs[1].bar(idps_since_2009['Governorate'], idps_since_2009['Affected people'], color='salmon')
axs[1].set_title('Affected People')
axs[1].set_ylabel('Number of People')
axs[1].set_xticklabels(idps_since_2009['Governorate'], rotation=45, ha='right')

plt.tight_layout()
st.pyplot(fig)

# Plotly histogram: Demolished structures by governorate
st.subheader("Distribution of Demolished Structures by Governorate")
fig = px.histogram(idps_by_year, x='Governorate', y='Demolished Structures', nbins=len(idps_by_year['Governorate'].unique()), 
                   title='Distribution of Demolished Structures by Governorate',
                   labels={'Demolished Structures': 'Number of Demolished Structures', 'Governorate': 'Governorate'},
                   color='Year', barmode='group')
fig.update_layout(template="plotly_white", bargap=0.2)
st.plotly_chart(fig)

# Additional Barplots with Seaborn: Demolished Structures and Affected People
st.subheader("Total Demolished Structures by Governorate (2009-present)")
fig, ax = plt.subplots(figsize=(14, 6))
sns.barplot(data=idps_since_2009, x='Governorate', y='Demolished Structures', palette='plasma', ax=ax)
ax.set_title('Total Demolished Structures by Governorate (2009-present)')
ax.set_xticklabels(ax.get_xticklabels(), rotation=45)
ax.set_ylabel('Demolished Structures')
st.pyplot(fig)

st.subheader("Total Affected People by Governorate (2009-present)")
fig, ax = plt.subplots(figsize=(14, 6))
sns.barplot(data=idps_since_2009, x='Governorate', y='Affected people', palette='magma', ax=ax)
ax.set_title('Total Affected People by Governorate (2009-present)')
ax.set_xticklabels(ax.get_xticklabels(), rotation=45)
ax.set_ylabel('Affected People')
st.pyplot(fig)

# Plotly Histogram: Distribution of Demolished Structures by Year
st.subheader("Distribution of Demolished Structures by Year")
fig = px.histogram(idps_by_year, x='Year', y='Demolished Structures', nbins=len(idps_by_year['Year'].unique()), 
                   title='Distribution of Demolished Structures by Year',
                   labels={'Demolished Structures': 'Number of Demolished Structures', 'Year': 'Year'},
                   color='Governorate', barmode='stack')
fig.update_layout(template="plotly_white", bargap=0.05, bargroupgap=0.1,
                  title={'text': "Distribution of Demolished Structures by Year",
                         'y': 0.9, 'x': 0.5, 'xanchor': 'center', 'yanchor': 'top'})
fig.update_xaxes(tickmode='linear', tick0=1, dtick=1)
st.plotly_chart(fig)

# Bubble chart: Affected People Over Time by Governorate
st.subheader("Affected People Over Time by Governorate")
fig = px.scatter(idps_by_year, x='Year', y='Governorate', size='Affected people', color='Governorate',
                 title='Affected People Over Time by Governorate', size_max=60)
fig.update_layout(template="plotly_white")
st.plotly_chart(fig)
