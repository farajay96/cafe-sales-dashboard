import streamlit as st
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns

def show_category_performance(df):
    st.header("Category Performance Analysis")

    # Clean up categories
    category_order = ['Coffee', 'Pastries', 'Tea', 'Sandwiches']
    custom_colors = {
        'Coffee': '#6f4e37',
        'Pastries': '#f5c16c',
        'Tea': '#8cbf26',
        'Sandwiches': '#d1bfa7'
    }
    # Compute total and average sales per category
    category_stats = df.groupby('Item Category').agg(
        Total_Sales=('Sale Amount', 'sum'),
        Total_Quantity=('Quantity Sold', 'sum')
    ).reset_index()
    category_stats['Avg_Price'] = category_stats['Total_Sales'] / category_stats['Total_Quantity']
    category_stats['Item Category'] = pd.Categorical(
        category_stats['Item Category'], categories=category_order, ordered=True
    )
    category_stats = category_stats.sort_values('Item Category')

    st.subheader("Total Sales and Average Revenue per Item by Category")
    fig1 = px.bar(
        category_stats,
        x='Item Category',
        y='Total_Sales',
        color='Item Category',
        text=category_stats['Avg_Price'].apply(lambda x: f"{x:.2f} SAR/item"),
        title='Total Sales and Avg Revenue per Item',
        labels={'Total_Sales': 'Total Sales (SAR)', 'Item Category': 'Category'},
        color_discrete_map=custom_colors
    )
    fig1.update_traces(textposition='outside')
    fig1.update_layout(showlegend=False, title_x=0.5)
    st.plotly_chart(fig1, use_container_width=True)

    # Revenue by category
    st.subheader("Total Revenue by Item Category")
    category_revenue = df.groupby('Item Category')['Sale Amount'].sum().reset_index()
    category_revenue['Item Category'] = pd.Categorical(category_revenue['Item Category'], categories=category_order, ordered=True)
    category_revenue = category_revenue.sort_values('Item Category')
    fig2 = px.bar(
        category_revenue,
        x='Item Category',
        y='Sale Amount',
        title="Total Revenue by Item Category",
        labels={'Sale Amount': 'Total Revenue (SAR)', 'Item Category': 'Category'},
        color='Item Category',
        color_discrete_map=custom_colors,
        text=category_revenue['Sale Amount'].apply(lambda x: f"{x:,.0f} SAR")
    )
    fig2.update_traces(textposition='outside', textfont_size=10)
    fig2.update_layout(showlegend=False, title_x=0.5)
    st.plotly_chart(fig2, use_container_width=True)

    # Monthly sales by item category (lineplot)
    st.subheader("Monthly Sales Trend by Category")
    df['Date'] = pd.to_datetime(df['Date'])
    monthly_category_sales = df.groupby([
        pd.Grouper(key='Date', freq='M'), 'Item Category'
    ])['Sale Amount'].sum().reset_index()
    plt.figure(figsize=(14, 7))
    sns.lineplot(
        data=monthly_category_sales,
        x='Date',
        y='Sale Amount',
        hue='Item Category',
        linewidth=2.5
    )
    plt.title("Monthly Sales by Item Category")
    plt.xlabel("Month")
    plt.ylabel("Total Sales (SAR)")
    plt.legend(title="Item Category")
    plt.grid(True)
    plt.tight_layout()
    st.pyplot(plt.gcf())
    plt.clf()

    # Text Recap
    st.markdown("""
    **Key Takeaways:**
    - Coffee is the top seller by both revenue and units.
    - Pastries, tea, and sandwiches make up a smaller but still important portion of sales.
    - The average price per item is highest for sandwiches, but coffee dominates in volume.
    - Monthly trends are stable, with small seasonal shifts.
    """)
