# -*- coding: utf-8 -*-
"""dashboard.py

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1796DU3G7BHXk9awlnOFBbRkfPr41GUtq
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from babel.numbers import format_currency
sns.set(style='dark')
st.header('Analisa Data E-Commerce')

def create_monthly_orders_df(df):
  monthly_orders_df = df.resample(rule='M', on='order_purchase_timestamp').agg({
      "order_id" : "nunique"

  })
  monthly_orders_df = monthly_orders_df.reset_index()
  monthly_orders_df.rename(columns={
      "order_id": "order_count"
  }, inplace = True)

  return monthly_orders_df

def create_bycity_df(df):
    bycity_df = df.groupby(by="customer_city").customer_id.nunique().reset_index()
    bycity_df.rename(columns={"customer_id": "customer_count", "customer_city": "city"}, inplace=True)
    return bycity_df

all_df = pd.read_csv('data.csv')

# datetime_column = ["order_purchase_timestamp"]
# all_df.sort_values(by="order_purchase_timestamp", inplace=True)
# all_df.reset_index(inplace=True)

# for column in datetime_column:
#   all_df[column] = pd.to_datetime(all_df[column])

min_month = all_df["order_purchase_timestamp"].min()
max_month = all_df["order_purchase_timestamp"].max()

start_month, end_month = st.date_input(
    label = 'Rentang Waktu', min_value=min_month, max_value=max_month, value = [min_month, max_month]
)

main_df = all_df[(all_df["order_purchase_timestamp"] >= str(start_month)) & (all_df["order_purchase_timestamp"] <= str(end_month))]

monthly_orders_df = create_monthly_orders_df(main_df)

bycity_df = create_bycity_df(main_df)

st.subheader('Monthly Orders')

col1, col2 = st.columns(2)

with col1:
    total_orders = monthly_orders_df.order_count.sum()
    st.metric("Total orders", value=total_orders, delta=None)

with col2:

    percentage_change = ((monthly_orders_df.order_count.iloc[-1] - monthly_orders_df.order_count.iloc[0]) / monthly_orders_df.order_count.iloc[0]) * 100
    st.metric("Percentage Change", value=percentage_change, delta=None)

fig, ax = plt.subplots(figsize=(16, 8))
ax.plot(
    monthly_orders_df["order_purchase_timestamp"],
    monthly_orders_df["order_count"],
    marker='o',
    linewidth=2,
    color="#87CEEB"
)

ax.tick_params(axis='y', labelsize=20)
ax.tick_params(axis='x', labelsize=15)

st.pyplot(fig)

# customer demographic
st.subheader("Customer Demographics")

# Top 5 cities with the most users
fig, ax = plt.subplots(figsize=(20, 10))

top_cities_df = bycity_df.nlargest(5, 'customer_count')

colors = ["#90CAF9", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3"]

sns.barplot(x="customer_count",
            y="city",
            data=top_cities_df,
            palette=colors,
            ax=ax
)
ax.set_title("Number of Customer in Top 5 Cities", loc="center", fontsize=30)
ax.set_ylabel('City')
ax.set_xlabel('')
ax.set_title("Top 5 Cities", loc="center", fontsize=50)
ax.tick_params(axis='y', labelsize=20)
ax.tick_params(axis='x', labelsize=15)

st.pyplot(fig)
