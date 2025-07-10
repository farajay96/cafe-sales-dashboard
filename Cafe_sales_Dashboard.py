import pandas as pd
from analysis_events import show_events_analysis
from analysis_temp import show_temperature_analysis
from analysis_category import show_category_performance
from analysis_discounts import show_discount_analysis
import streamlit as st

st.set_page_config(page_title="Cafe Sales Dashboard", layout="wide")

# --- Utility Function ---
def load_main_data(path):
    df = pd.read_csv(path)
    if 'Date' in df.columns:
        df['Date'] = pd.to_datetime(df['Date'])
    return df



# --- Streamlit Page Setup ---

# --- Data Loading ---
DATA_PATH = "CafeSales_clean.csv"
EVENTS_PATH = "Data Anaylst Task -Events_2023_2024.csv"
df = load_main_data(DATA_PATH)

section = st.sidebar.radio("Go to", [
    "Home",
    "Event Impact",
    "Temperature Effect",
    "Category Performance",
    "Discount Analysis",
    "Model Development",
    "Final Conclusion"
])

# --- Section Routing ---

if section == "Home":
    st.title("Cafe Sales Analysis Dashboard")
   # st.image("A_2D_infographic_titled_\"Cafe_Sales_Analysis_Overv.png\"", use_column_width=True, caption="Summary of Key Analysis Areas")
    st.markdown("""
    ### What This Dashboard Covers

    1. **Event Impact:**  
       Analyzing how sales respond to events and holidays.

    2. **Temperature Effect:**  
       Exploring the correlation between temperature and daily sales.

    3. **Product Category Performance:**  
       Comparing the sales and trends of each product category.

    4. **Discount Analysis:**  
       Investigating how different discount strategies affect sales quantity.

    5. **Model Development:**  
       Attempting to forecast sales using statistical and machine learning models.

    ---
    Use the sidebar to navigate to each section for details and interactive figures.
    """)
elif section == "Event Impact":
    show_events_analysis(df, EVENTS_PATH)
elif section == "Temperature Effect":
    show_temperature_analysis(df)
elif section == "Category Performance":
    show_category_performance(df)
elif section == "Discount Analysis":
    show_discount_analysis(df)
elif section == "Model Development":
    st.markdown("""
### **Model Development Summary**

- Tried **Linear Regression, Random Forest, XGBoost, and Prophet** to forecast daily sales.
- **Prophet with regressors** gave the best performance (lowest MAE and RMSE).
- **Random Forest** and **XGBoost** had competitive results, but didn’t outperform Prophet.
- **Main issue:** Streamlit app performance was slow when running model training and tuning live. This made real-time forecasting impractical.
- **Solution:** Model evaluation and tuning were done offline in Jupyter, and results are summarized here instead of re-running each time.

**Bottom line:**  
Prophet is currently the best option for sales forecasting on this dataset, but heavy model training should be kept outside Streamlit for speed.

---
"""
)
        
    
elif section == "Final Conclusion":
    st.markdown("""
# **Final Recommendations**

## **Events**
- **Long Weekends:** Only long weekends consistently drive significant sales growth. Go big on promotions, inventory, and staffing for these periods.
- **Other Events:** Don’t waste resources on other events (Middle Beast, Independence Day, Labor Day)—they have no proven sales impact.
- **Action:** Track event sales, but let data—not hype—drive event planning.

---

## **Temperature**
- **No Weather Effect:** Daily sales are not meaningfully affected by temperature.
- **Action:** Do not adjust inventory, promotions, or staffing based on weather forecasts.

---

## **Category Performance**
- **Coffee is King:** Coffee is your main revenue driver—keep prioritizing it.
- **Bundle Smart:** Use coffee sales to push pastries and sandwiches with bundles/combos.
- **Tea:** Run occasional promos, but don’t expect miracles.
- **Action:** Don’t make big pricing changes without testing. Keep tracking trends by category.

---

## **Discounts**
- **Sweet Spot = 5–10%:** Discounts in the 5–10% range move the most product across all categories.
- **Don’t Over-discount:** Steep discounts (>10%) don’t drive extra sales and hurt margins.
- **Category Tuning:** If you must push a category, start with Coffee or Pastries.
- **Action:** Stick to moderate, data-driven discounts.

---

## **Sales Forecasting / Model Development**
- **Prophet Wins:** Prophet (with calendar and sales features) is your best sales forecasting tool for now.
- **Don’t Train in Streamlit:** Model training and tuning is too slow for live dashboards—do this offline and present results only.
- **Action:** Use Prophet for operational planning; update models periodically outside the dashboard.

---

**Bottom line:**  
Focus on what works—long weekends, moderate discounts, and coffee. Ignore the rest.  
Let actual sales data drive every operational decision.
""")


