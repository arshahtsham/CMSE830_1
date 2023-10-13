import streamlit as st
import pandas as pd
import base64
import altair as alt
import yfinance as yf

st.title('S&P 500 Stock Price Analysis')

st.markdown("""
This app retrieves the list of **S&P 500** companies and their corresponding **stock closing prices** for analysis.
* **Python libraries:** base64, pandas, streamlit, numpy, altair, yfinance
* **Data source:** [Wikipedia](https://en.wikipedia.org/wiki/List_of_S%26P_500_companies).
""")

st.sidebar.header('User Input Features')

# Web scraping of S&P 500 data
@st.cache
def load_data():
    url = 'https://en.wikipedia.org/wiki/List_of_S%26P_500_companies'
    html = pd.read_html(url, header=0)
    df = html[0]
    return df

df = load_data()
sector = df.groupby('GICS Sector')

# Sidebar - Sector selection
sorted_sector_unique = sorted(df['GICS Sector'].unique())
selected_sector = st.sidebar.multiselect('Select Sectors', sorted_sector_unique, sorted_sector_unique)

# Filtering data based on selected sectors
df_selected_sector = df[df['GICS Sector'].isin(selected_sector)]

st.header('Display Companies in Selected Sectors')
st.write(f'Data Dimension: {df_selected_sector.shape[0]} rows and {df_selected_sector.shape[1]} columns.')
st.dataframe(df_selected_sector)

# Download S&P500 data as CSV
def filedownload(df):
    csv = df.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()  # strings <-> bytes conversions
    href = f'<a href="data:file/csv;base64,{b64}" download="SP500.csv">Download CSV File</a>'
    return href

st.markdown(filedownload(df_selected_sector), unsafe_allow_html=True)

# Stock data retrieval and visualization
st.sidebar.subheader('Stock Visualization Options')
start_date = st.sidebar.date_input('Start Date', pd.to_datetime('2023-01-01'))
end_date = st.sidebar.date_input('End Date', pd.to_datetime('2023-12-31'))

selected_symbol = st.sidebar.selectbox('Select a Company', list(df_selected_sector['Symbol']))
company_data = yf.download(selected_symbol, start=start_date, end=end_date)

st.header('Stock Closing Price for ' + selected_symbol)
st.write(f'Data for {selected_symbol} from {start_date} to {end_date}')
st.line_chart(company_data['Close'])

# Show a table with detailed stock data
st.subheader('Stock Data')
st.write(company_data)

# Provide insights and explanations
st.markdown("""
**Insights:**
- This chart displays the closing price of the selected company's stock.
- You can select a specific date range using the sidebar options.
- Analyze the stock's performance during the selected period.
""")

