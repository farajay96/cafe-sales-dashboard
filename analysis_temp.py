import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

def show_temperature_analysis(df):
    st.header("Temperature Effects on Sales")

    # Make a copy and ensure Date column is datetime
    df = df.copy()
    df['Date'] = pd.to_datetime(df['Date'])

    # --- 1. Total Daily Sales vs Temperature ---
    daily_summary = df.groupby('Date').agg({
        'Sale Amount': 'sum',
        'Temperature (°F)': 'mean'
    }).reset_index()

    # Pearson correlation
    correlation = daily_summary['Sale Amount'].corr(daily_summary['Temperature (°F)'])
    st.write(f"**Correlation between temperature and total sales:** {correlation:.3f}")

    # Scatter plot
    fig, ax = plt.subplots(figsize=(7, 4))
    ax.scatter(daily_summary['Temperature (°F)'], daily_summary['Sale Amount'], alpha=0.6)
    ax.set_title('Temperature vs. Total Daily Sales')
    ax.set_xlabel('Temperature (°F)')
    ax.set_ylabel('Total Sales (SAR)')
    ax.grid(True)
    st.pyplot(fig)

    # --- 2. Product-wise correlation with temperature ---
    st.subheader("Product-wise correlation with temperature")
    product_temp_sales = df.groupby(['Date', 'Product Description']).agg({
        'Sale Amount': 'sum',
        'Temperature (°F)': 'mean'
    }).reset_index()

    pivoted_sales = product_temp_sales.pivot(index='Date', columns='Product Description', values='Sale Amount')
    daily_temp = product_temp_sales.groupby('Date')['Temperature (°F)'].mean()
    pivoted_sales['Temperature (°F)'] = daily_temp

    product_temp_correlation = pivoted_sales.corr()['Temperature (°F)'].drop('Temperature (°F)').sort_values()
    st.dataframe(product_temp_correlation)

    fig2, ax2 = plt.subplots(figsize=(7, max(2, len(product_temp_correlation) * 0.3)))
    product_temp_correlation.plot(kind='barh', ax=ax2)
    ax2.set_title("Product Sales vs Temperature Correlation")
    ax2.set_xlabel("Correlation with Temperature")
    st.pyplot(fig2)

    # --- 3. Recap and Recommendations ---
    st.markdown("""
    ### Conclusion & Recommendations

    - **Overall Impact:**  
      The correlation between average daily temperature and total sales is weak (**r = -0.072**), suggesting that temperature does not meaningfully drive overall sales volume for this cafe.

    - **By Product:**  
      When analyzed by product, all correlations between temperature and individual product sales are also weak (see chart above). No product shows a strong positive or negative sensitivity to daily temperature changes.

    #### Recommendations

    - **No Need for Weather-Based Sales Strategies:**  
      At this time, there is no justification for adjusting inventory, promotions, or staffing based on expected weather/temperature.  
    - **Focus on Other Drivers:**  
      Management should focus on other external factors (e.g., events, seasonality, discounts) rather than temperature when planning sales strategies.
    - **Continue to Monitor:**  
      Continue tracking temperature to detect if patterns emerge in future years, but do not prioritize temperature-based interventions unless a stronger relationship is established.
    """)
