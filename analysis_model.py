from turtle import st

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
""")
