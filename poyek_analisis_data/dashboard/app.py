# app.py

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

# Load datasets
geolocation = pd.read_csv('https://raw.githubusercontent.com/mashumabduljabbar/dataset/master/E-Commerce/geolocation_dataset.csv')
order_items = pd.read_csv('https://raw.githubusercontent.com/mashumabduljabbar/dataset/master/E-Commerce/order_items_dataset.csv')
order_payments = pd.read_csv('https://raw.githubusercontent.com/mashumabduljabbar/dataset/master/E-Commerce/order_payments_dataset.csv')
order_reviews = pd.read_csv('https://raw.githubusercontent.com/mashumabduljabbar/dataset/master/E-Commerce/order_reviews_dataset.csv')
orders = pd.read_csv('https://raw.githubusercontent.com/mashumabduljabbar/dataset/master/E-Commerce/orders_dataset.csv')
product_category_translation = pd.read_csv('https://raw.githubusercontent.com/mashumabduljabbar/dataset/master/E-Commerce/product_category_name_translation.csv')
products = pd.read_csv('https://raw.githubusercontent.com/mashumabduljabbar/dataset/master/E-Commerce/products_dataset.csv')
sellers = pd.read_csv('https://raw.githubusercontent.com/mashumabduljabbar/dataset/master/E-Commerce/sellers_dataset.csv')
customers = pd.read_csv('https://raw.githubusercontent.com/mashumabduljabbar/dataset/master/E-Commerce/customers_dataset.csv')

# Sidebar for navigation
st.sidebar.title('Dashboard Menu')
option = st.sidebar.selectbox('Choose a Visualization', 
                              ['Payment Value Distribution', 
                               'Payment Value vs Review Score', 
                               'Delivery Time vs Order Status',
                               'Category Purchase Counts', 
                               'Description Length vs Sales Frequency'])

# Main content
st.title('E-Commerce Dashboard')

if option == 'Payment Value Distribution':
    st.header('Distribusi Nilai Pembayaran Berdasarkan Metode Pembayaran')

    # Box Plot
    plt.figure(figsize=(12, 6))
    sns.boxplot(x='payment_type', y='payment_value', data=order_payments)
    plt.title('Distribusi Nilai Pembayaran Berdasarkan Metode Pembayaran')
    plt.xlabel('Metode Pembayaran')
    plt.ylabel('Nilai Pembayaran')
    plt.xticks(rotation=45)
    st.pyplot()

    # Violin Plot
    plt.figure(figsize=(12, 6))
    sns.violinplot(x='payment_type', y='payment_value', data=order_payments)
    plt.title('Distribusi Nilai Pembayaran Berdasarkan Metode Pembayaran')
    plt.xlabel('Metode Pembayaran')
    plt.ylabel('Nilai Pembayaran')
    plt.xticks(rotation=45)
    st.pyplot()

elif option == 'Payment Value vs Review Score':
    st.header('Hubungan Antara Nilai Pembayaran dan Skor Ulasan Produk')

    # Scatter Plot
    plt.figure(figsize=(12, 6))
    sns.scatterplot(x='payment_value', y='review_score', data=order_reviews.merge(order_payments, on='order_id'))
    plt.title('Hubungan antara Nilai Pembayaran dan Skor Ulasan Produk')
    plt.xlabel('Nilai Pembayaran')
    plt.ylabel('Skor Ulasan')
    st.pyplot()

    # Heatmap
    plt.figure(figsize=(12, 6))
    sns.heatmap(pd.crosstab(order_reviews['review_score'], order_payments['payment_value']), cmap='YlGnBu')
    plt.title('Peta Panas: Nilai Pembayaran vs Skor Ulasan')
    plt.xlabel('Nilai Pembayaran')
    plt.ylabel('Skor Ulasan')
    st.pyplot()

elif option == 'Delivery Time vs Order Status':
    st.header('Waktu Pengiriman vs Status Pesanan')

    # Calculate delivery time
    orders['order_purchase_timestamp'] = pd.to_datetime(orders['order_purchase_timestamp'])
    orders['order_delivered_customer_date'] = pd.to_datetime(orders['order_delivered_customer_date'])
    orders['delivery_time'] = (orders['order_delivered_customer_date'] - orders['order_purchase_timestamp']).dt.days

    # Box Plot
    plt.figure(figsize=(12, 6))
    sns.boxplot(x='order_status', y='delivery_time', data=orders)
    plt.title('Distribusi Waktu Pengiriman Berdasarkan Status Pesanan')
    plt.xlabel('Status Pesanan')
    plt.ylabel('Waktu Pengiriman (Hari)')
    plt.xticks(rotation=45)
    st.pyplot()

elif option == 'Category Purchase Counts':
    st.header('Jumlah Pembelian per Kategori Produk')

    # Merge datasets
    merged_orders_items = pd.merge(order_items, orders, on='order_id')
    merged_orders_items_products = pd.merge(merged_orders_items, products, on='product_id')

    # Calculate total payment per product category
    merged_orders_items_products['total_payment'] = merged_orders_items_products['price'] * merged_orders_items_products['order_item_id']

    # Group by product category
    category_summary = merged_orders_items_products.groupby('product_category_name').agg(
        total_amount=pd.NamedAgg(column='total_payment', aggfunc='sum'),
        order_count=pd.NamedAgg(column='order_id', aggfunc='count')
    ).reset_index()

    # Plot
    fig, ax1 = plt.subplots(figsize=(12, 6))

    # Total amount
    sns.barplot(x='product_category_name', y='total_amount', data=category_summary, ax=ax1, color='b', alpha=0.6)
    ax1.set_xlabel('Kategori Produk')
    ax1.set_ylabel('Total Pembayaran (dalam mata uang)', color='b')
    ax1.tick_params(axis='y', labelcolor='b')
    ax1.set_xticklabels(ax1.get_xticklabels(), rotation=45, ha='right')

    # Order count
    ax2 = ax1.twinx()
    sns.lineplot(x='product_category_name', y='order_count', data=category_summary, ax=ax2, color='r', marker='o')
    ax2.set_ylabel('Jumlah Pesanan', color='r')
    ax2.tick_params(axis='y', labelcolor='r')

    plt.title('Jumlah Pembelian dan Pengaruhnya Terhadap Nilai Total Pembayaran per Kategori Produk')
    st.pyplot()

elif option == 'Description Length vs Sales Frequency':
    st.header('Panjang Deskripsi Produk vs Frekuensi Penjualan')

    # Merge datasets
    order_items_products = pd.merge(order_items, products, on='product_id')

    # Calculate length of product description
    order_items_products['description_length'] = order_items_products['product_description_lenght']

    # Group by product_id
    product_summary = order_items_products.groupby('product_id').agg(
        description_length=('description_length', 'mean'),
        order_count=('order_id', 'count')
    ).reset_index()

    # Scatter Plot
    plt.figure(figsize=(12, 6))
    sns.scatterplot(x='description_length', y='order_count', data=product_summary)
    plt.title('Hubungan antara Panjang Deskripsi Produk dan Frekuensi Penjualan')
    plt.xlabel('Panjang Deskripsi Produk')
    plt.ylabel('Frekuensi Penjualan')
    st.pyplot()
