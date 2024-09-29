import pandas as pd
import streamlit as st
import plotly.express as px

# load data
customers_df = pd.read_csv("https://raw.githubusercontent.com/Sipa02/Proyek_analisis_data/main/customers_clean.csv")
order_items_df = pd.read_csv("https://raw.githubusercontent.com/Sipa02/Proyek_analisis_data/main/order_items_clean.csv")
order_payments_df = pd.read_csv("https://raw.githubusercontent.com/Sipa02/Proyek_analisis_data/main/order_payments_clean.csv")
product_category_df = pd.read_csv("https://raw.githubusercontent.com/Sipa02/Proyek_analisis_data/main/product_category_clean.csv")
products_df = pd.read_csv("https://raw.githubusercontent.com/Sipa02/Proyek_analisis_data/main/products_clean.csv")
orders_df = pd.read_csv("https://raw.githubusercontent.com/Sipa02/Proyek_analisis_data/main/order_clean.csv")

# merge order_items_df dan products_df berdasarkan product_id
items_products_df = pd.merge(order_items_df, products_df, on='product_id', how='inner')
items_products_category_df = pd.merge(items_products_df, product_category_df, on='product_category_name', how='inner')
items_product_category_order_df = pd.merge(items_products_category_df, orders_df, on='order_id', how='inner')

px.defaults.template = "plotly_dark"
px.defaults.color_continuous_scale = "reds"

st.title("E-Commerce Dashboard :sparkles:")

st.subheader("Payment Method Distribution")

# Menghitung frekuensi setiap metode pembayaran
payment_method_counts = order_payments_df['payment_type'].value_counts()

# Membuat persentase frekuensi setiap metode pembayaran
payment_method_percentage = payment_method_counts / payment_method_counts.sum() * 100

# Membuat Pie Chart untuk distribusi metode pembayaran
fig_pie = px.pie( 
    values=payment_method_percentage.values, 
    names=payment_method_percentage.index, 
    title="Distribusi Metode Pembayaran",
    hole=0.4  # membuat donut chart
)
st.plotly_chart(fig_pie)


# Menampilkan 5 kota dengan penjualan tertinggi
st.subheader("Kota dengan Penjualan Tertinggi")

cust_order_df = pd.merge(customers_df, orders_df, on='customer_id', how='inner')

# mengelompokkan berdasarkan kota dan menghitung jumlah order
sales_by_city = cust_order_df.groupby('customer_city')['order_id'].count()

# mengurutkan kota berdasarkan penjualan (ascending=False untuk tertinggi di atas)
sorted_sales = sales_by_city.sort_values(ascending=False)

# menampilkan 5 kota dengan penjualan tertinggi
top_5_cities = sorted_sales.head(5)

# Membuat bar chart vertikal untuk 5 kota teratas
fig_city = px.bar(
    x=top_5_cities.index, 
    y=top_5_cities.values, 
    title="Kota dengan Penjualan Tertinggi", 
    orientation='v',
    labels={'x': 'Kota', 'y': 'Penjualan'}
)
st.plotly_chart(fig_city)


# membuat subheader untuk kategori produk dengan penjualan tertinggi
st.subheader("Kategori Produk dengan Penjualan Tertinggi")

# Menghitung frekuensi pembelian setiap kategori produk
category_counts = items_products_category_df['product_category_name_english'].value_counts()

# mengurutkan product category berdasarkan penjualan (ascending=False untuk tertinggi di atas) 
sorted_category = category_counts.sort_values(ascending=False)

# Menampilkan kategori produk dengan penjualan tertinggi
top_5_category = sorted_category.head(5)


# Membuat bar chart horizontal untuk kategori produk
fig_category = px.bar(
    x=top_5_category.values, 
    y=top_5_category.index, 
    title="Kategori Produk dengan Penjualan Tertinggi", 
    orientation='h',
    labels={'x': 'Penjualan', 'y': 'Kategori Produk'},

    color_discrete_sequence=px.colors.qualitative.Pastel
)
st.plotly_chart(fig_category)
