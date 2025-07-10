import streamlit as st
import pandas as pd
import plotly.express as px
from scipy.stats import ttest_ind, ttest_1samp

def show_events_analysis(df, events_path):
    st.header("Event Effects on Sales")

    # Load events data
    events = pd.read_csv(events_path)
    events['Date'] = pd.to_datetime(events['Date'])

    # Daily sales aggregation
    daily_sales = df.groupby('Date')['Sale Amount'].sum().reset_index()
    daily_sales['Date'] = pd.to_datetime(daily_sales['Date'])

    # Merge with events (now both Date columns are datetime)
    daily_sales = daily_sales.merge(events, on='Date', how='left')

    # Create binary flag
    daily_sales['Is Event'] = daily_sales['Event Description'].notna()

    # Summary stats
    event_sales_summary = daily_sales.groupby('Is Event')['Sale Amount'].agg(['count', 'mean', 'std'])
    event_sales_summary.index = ['Non-Event Day', 'Event Day']
    st.subheader("Summary Statistics: Event vs Non-Event Days")
    st.dataframe(event_sales_summary)

    # T-test between event and non-event days
    event_sales = daily_sales[daily_sales['Is Event']]['Sale Amount']
    non_event_sales = daily_sales[~daily_sales['Is Event']]['Sale Amount']
    t_stat, p_value = ttest_ind(event_sales, non_event_sales, equal_var=False)
    st.write(f"**T-statistic:** {t_stat:.2f}, **P-value:** {p_value:.4f}")

    # One-sample t-test for each event vs non-event days
    individual_events = daily_sales[daily_sales['Is Event']][['Date', 'Event Description', 'Sale Amount']]
    results = []
    for _, row in individual_events.iterrows():
        event_name = row['Event Description']
        event_date = row['Date']
        event_sale = row['Sale Amount']
        t_stat_evt, p_val_evt = ttest_1samp(non_event_sales, event_sale)
        results.append({
            'Date': event_date,
            'Event': event_name,
            'Sale Amount': event_sale,
            'T-stat': t_stat_evt,
            'P-value': round(p_val_evt,9)
        })

    event_outlier_results = pd.DataFrame(results).sort_values(by='P-value')
    # Add label for plot
    event_outlier_results['Label'] = event_outlier_results['Event'] + " (" + event_outlier_results['Date'].dt.strftime('%Y-%m-%d') + ")"

    st.subheader("Statistical Test: Individual Event Days vs Non-Event Day Sales")
    st.dataframe(event_outlier_results[['Date', 'Event', 'Sale Amount', 'T-stat', 'P-value']])

    # Plot with Plotly (interactive)
    average_non_event_sales = non_event_sales.mean()
    fig = px.bar(
        event_outlier_results.sort_values(by='Sale Amount', ascending=False),
        x='Label',
        y='Sale Amount',
        title="Sales on Event Days vs. Average Non-Event Sales",
        labels={'Sale Amount': 'Total Sales (SAR)', 'Label': 'Event'},
        color='Sale Amount'
    )
    # Add average non-event sales line
    fig.add_hline(y=average_non_event_sales, line_dash="dash", line_color="red",
                  annotation_text="Avg Non-Event Sales", annotation_position="bottom left")
    fig.update_layout(xaxis_tickangle=-45, height=500)

    st.plotly_chart(fig, use_container_width=True)

    st.caption("Only the Long Weekend boosted sales. All other events actually saw a drop in sales, and that drop was statistically significant.")
    st.markdown("""
    ### Conclusion & Recommendations

    - **Recap of Findings:**
        - Only the **Long Weekend** event produced a notable increase in sales compared to non-event days.
        - All other events (Middle Beast Festival, Independence Day, Labor Day) saw **no uplift**—in fact, sales were below or close to the average non-event day.
        - The t-test confirms these differences are statistically significant.

    #### Strategic Recommendations

    - **Focus on Long Weekends:**  
      Double down on inventory, promotions, and staffing during long weekends, as they are the only events proven to drive a real sales boost.
    - **Don’t Over-invest in Other Events:**  
      For events that have shown no impact (or negative impact), there’s no business case for extra marketing or preparation unless new data indicates otherwise.
    - **Monitor Event Performance:**  
      Keep tracking sales during all events, but don’t let event hype drive operational decisions—let the numbers speak.
    """)
