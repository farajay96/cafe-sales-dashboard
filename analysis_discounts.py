import streamlit as st
import pandas as pd
import plotly.express as px

def show_discount_analysis(df):
    st.header("Discount Analysis")

    # --- 0. Discounted vs Non-Discounted: Total Quantity Sold ---
    st.subheader("Total Quantity Sold: Discounted vs Non-Discounted")
    discount_comparison = df.groupby("Discount Applied")["Quantity Sold"].sum().reset_index()
    discount_comparison["Discount Label"] = discount_comparison["Discount Applied"].map({
        "Yes": "Discounted",
        "No": "Non-Discounted"
    })
    fig0 = px.bar(
        discount_comparison,
        x="Discount Label",
        y="Quantity Sold",
        text="Quantity Sold",
        title="🧮 Total Quantity Sold: Discounted vs Non-Discounted",
        color="Discount Label",
        color_discrete_map={"Discounted": "#00bfc4", "Non-Discounted": "#f8766d"},
    )
    fig0.update_traces(texttemplate="%{text}", textposition="outside")
    fig0.update_layout(
        xaxis_title="",
        yaxis_title="Total Quantity Sold",
        bargap=0.4,
        margin=dict(t=60, b=60),
        yaxis=dict(tickformat=",", range=[0, discount_comparison["Quantity Sold"].max() * 1.15])
    )
    st.plotly_chart(fig0, use_container_width=True)

    # --- 1. Calculate Discount Percentage ---
    df = df.copy()
    df['Discount %'] = df['Discount Amount'] / (df['Sale Amount'] + df['Discount Amount'])

    # --- 2. Distribution of Discount Percentages (Excl. 0%) ---
    st.subheader("Distribution of Discount Percentages (Excl. 0%)")
    fig1 = px.histogram(
        df[df['Discount %'] > 0], 
        x='Discount %', 
        nbins=30,
        title="Distribution of Discount Percentages (Excl. 0%)"
    )
    fig1.update_layout(
        xaxis_title="Discount %",
        yaxis_title="Frequency",
        bargap=0.1,
        margin=dict(t=60, b=60, l=60, r=60)
    )
    st.plotly_chart(fig1, use_container_width=True)

    # --- 3. Quantity Sold per Discount Bin ---
    bins = [0, 0.025, 0.05, 0.10, 0.20, 0.50]
    labels = ['Very Low (0–2.5%)', 'Low (2.5–5%)', 'Moderate (5–10%)', 'High (10–20%)', 'Very High (>20%)']
    df['Discount Bin'] = pd.cut(
        df['Discount %'],
        bins=bins,
        labels=labels,
        include_lowest=False
    )

    avg_quantity_per_bin = (
        df[df['Discount %'] > 0]
        .groupby('Discount Bin', observed=True)['Quantity Sold']
        .sum()
        .reset_index()
    )

    color_map = {
        'Very Low (0–2.5%)': '#a6cee3',
        'Low (2.5–5%)': '#1f78b4',
        'Moderate (5–10%)': '#33a02c',
        'High (10–20%)': '#fb9a99',
        'Very High (>20%)': '#e31a1c',
    }

    fig2 = px.bar(
        avg_quantity_per_bin,
        x='Discount Bin',
        y='Quantity Sold',
        title='🧮 Quantity Sold per Discount Bin',
        color='Discount Bin',
        color_discrete_map=color_map,
        text='Quantity Sold'
    )
    fig2.update_traces(texttemplate='%{text:.0f}', textposition='outside')
    fig2.update_layout(
        xaxis_title='Discount Bin',
        yaxis_title='Total Quantity Sold',
        bargap=0.2,
        showlegend=False,
        margin=dict(t=60, b=60, l=60, r=60)
    )
    max_val = avg_quantity_per_bin['Quantity Sold'].max()
    fig2.update_yaxes(range=[0, max_val * 1.15])
    st.plotly_chart(fig2, use_container_width=True)

    # --- 4. Quantity Sold per Discount Bin by Item Category ---
    discount_grouped = (
        df[df['Discount %'] > 0]
        .groupby(['Item Category', 'Discount Bin'], observed=True)['Quantity Sold']
        .sum()
        .reset_index(name='Total Quantity')
    )

    custom_colors = {
        'Coffee': '#6f4e37',
        'Pastries': '#f5c16c',
        'Tea': '#8cbf26',
        'Sandwiches': '#d1bfa7'
    }

    fig3 = px.bar(
        discount_grouped,
        x='Discount Bin',
        y='Total Quantity',
        color='Item Category',
        title='Quantity Sold per Discount Bin by Item Category',
        color_discrete_map=custom_colors,
        barmode='group',
        text='Total Quantity'
    )
    fig3.update_layout(
        xaxis_title='Discount Bin',
        yaxis_title='Total Quantity Sold',
        bargap=0.2,
        showlegend=True,
        yaxis_range=[0, discount_grouped['Total Quantity'].max() * 1.10],
        title_x=0.5,
        xaxis_tickangle=-30,
        height=500,
        width=800,
        margin=dict(t=60, b=100, l=60, r=40)
    )
    fig3.update_traces(textposition='outside')
    st.plotly_chart(fig3, use_container_width=True)
    st.markdown("""
    ### Conclusion & Recommendations

    - **Recap of Findings:**
        - Most discounts applied are on the lower end (under 10%), with a sharp drop-off above 10%.
        - **Quantity sold is highest for discounts in the 5–10% (“Moderate”) range.**  
        Steeper discounts (over 10%) do not result in higher sales volumes, and “Very High” discounts (>20%) move the least product.
        - This pattern holds across all major categories—Coffee, Pastries, Sandwiches, and Tea.

    #### Strategic Recommendations

    - **Target 5–10% Discounts:**  
    Use “moderate” discounts (5–10%) as your default promotional strategy. This zone drives the highest total sales volume without heavy margin sacrifice.
    - **Don’t Over-Discount:**  
    Avoid frequent or deep discounts above 10%. They do not generate higher sales and just eat into profits.
    - **Segment by Category if Needed:**  
    If you want to be aggressive in one product line, focus on Pastries and Coffee—these categories are most responsive to moderate discounts.
    - **Monitor and Adjust:**  
    Keep tracking what works, but for now, there’s zero evidence to support routine deep discounting or flash sales.
    """)
