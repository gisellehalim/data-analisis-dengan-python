import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from babel.numbers import format_currency
sns.set(style='dark')

def customer_city_orders(df):
    customer_city_orders = df.groupby('customer_city')['order_id'].count().reset_index()
    return customer_city_orders

def customer_states_orders(df):
    customer_states_orders = df.groupby('customer_state')['order_id'].count().reset_index()
    return customer_states_orders

def daily_orders_df(df):
    daily_orders_df = df.resample(rule='D', on='order_approved_at').agg({
        "order_id": "nunique",
        "price": "sum"
    })
    daily_orders_df = daily_orders_df.reset_index()
    daily_orders_df.rename(columns={
        "order_id": "order_count",
        "price": "revenue"
    }, inplace=True)
    
    return daily_orders_df

def monthly_orders_df(df):
    
    monthly_orders_df = df.groupby(by='YearMonth').agg({
        "order_id": "nunique",
        "price": "sum"
    })
    monthly_orders_df = monthly_orders_df.reset_index()
    monthly_orders_df.rename(columns={
        "order_id": "order_count",
        "price": "revenue"
    }, inplace=True)
    return monthly_orders_df

def product_orders(df):
    product_orders = df.groupby('product_id')['order_id'].count().reset_index()
    return product_orders

def product_revenue(df):
    product_revenue = df.groupby('product_id')['price'].sum().reset_index()
    return product_revenue

def product_cat_revenue(df):
    product_cat_revenue = df.groupby('product_category_name')['price'].sum().reset_index()
    return product_cat_revenue

def create_rfm_df(df):
    rfm_df = df.groupby(by="customer_id", as_index=False).agg({
    "order_approved_at": "max", 
    "order_id": "nunique", 
    "price": "sum" 
    })
    rfm_df.columns = ["customer_id", "max_order_timestamp", "frequency", "monetary"]

    rfm_df["max_order_timestamp"] = rfm_df["max_order_timestamp"].dt.date
    recent_date = df["order_approved_at"].dt.date.max()
    rfm_df["recency"] = rfm_df["max_order_timestamp"].apply(lambda x: (recent_date - x).days)

    rfm_df.drop("max_order_timestamp", axis=1, inplace=True)
    rfm_df.head()
    
    return rfm_df

all_df = pd.read_csv("all_data.csv")

datetime_columns = ["order_approved_at", "order_delivered_customer_date"]
all_df.sort_values(by="order_approved_at", inplace=True)
all_df.reset_index(inplace=True)
 
for column in datetime_columns:
    all_df[column] = pd.to_datetime(all_df[column])

min_date = all_df["order_approved_at"].min()
max_date = all_df["order_approved_at"].max()
 
with st.sidebar:
    # Menambahkan logo perusahaan
    st.image("https://i.ibb.co/pnMXQC2/Blue-and-White-Circle-Retail-Logo.png")
    
    # Mengambil start_date & end_date dari date_input
    start_date, end_date = st.date_input(
        label='Date',min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )

main_df = all_df[(all_df["order_approved_at"] >= str(start_date)) & 
                (all_df["order_approved_at"] <= str(end_date))]

customer_city_orders = customer_city_orders(main_df)
customer_states_orders = customer_states_orders(main_df)
monthly_orders_df = monthly_orders_df(main_df)
product_orders = product_orders(main_df)
product_revenue = product_revenue(main_df)
product_cat_revenue = product_cat_revenue(main_df)
daily_orders_df = daily_orders_df(main_df)
rfm_df = create_rfm_df(main_df)


st.markdown("<h1 style='text-align: center; color: white;'>Super E-Commerce Dashboard</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: white;'>Created by: Giselle Halim | gisellehalim27@gmail.com</p>", unsafe_allow_html=True)

st.subheader('Total Orders')
 
col1, col2 = st.columns(2)
 
with col1:
    total_orders = monthly_orders_df.order_count.sum()
    st.metric("Total orders", value=total_orders)
 
with col2:
    total_revenue = format_currency(monthly_orders_df.revenue.sum(), "USD", locale='es_CO') 
    st.metric("Total Revenue", value=total_revenue)

st.subheader('Daily Orders')

fig, ax = plt.subplots(figsize=(16, 8))
ax.plot(
    daily_orders_df["order_approved_at"],
    daily_orders_df["order_count"],
    marker='o', 
    linewidth=2,
    color="#90CAF9"
)
ax.tick_params(axis='y', labelsize=20)
ax.tick_params(axis='x', labelsize=15)
ax.set_title("Daily Orders", loc="center", fontsize=20)
 
st.pyplot(fig)
st.markdown("<p style='color: white;'>Highest order in a day reached almost 800 orders.</p>", unsafe_allow_html=True)

st.subheader('Daily Revenue')

fig, ax = plt.subplots(figsize=(16, 8))
ax.plot(
    daily_orders_df["order_approved_at"],
    daily_orders_df["revenue"],
    marker='o', 
    linewidth=2,
    color="#4BA150"
)
ax.set_title("Daily Revenue", loc="center", fontsize=20)
ax.tick_params(axis='y', labelsize=20)
ax.tick_params(axis='x', labelsize=15)
 
st.pyplot(fig)
st.markdown("<p style='color: white;'>Highest revenue in a day reached around US$100.000</p>", unsafe_allow_html=True)

st.subheader('Monthly Orders')

fig, ax = plt.subplots(figsize=(16, 8))
ax.plot(
    monthly_orders_df["YearMonth"],
    monthly_orders_df["order_count"],
    marker='o', 
    linewidth=2,
    color="#90CAF9"
)
ax.set_title("Monthly Orders", loc="center", fontsize=20)
ax.tick_params(axis='y', labelsize=15)
ax.tick_params(axis='x', labelsize=9)
 
st.pyplot(fig)
st.markdown("<p style='color: white;'>Highest order in a month reached around 7000 orders, precisely in November 2017.</p>", unsafe_allow_html=True)

st.subheader('Monthly Revenue')

fig, ax = plt.subplots(figsize=(16, 8))
ax.plot(
    monthly_orders_df["YearMonth"],
    monthly_orders_df["revenue"],
    marker='o', 
    linewidth=2,
    color="#4BA150"
)
ax.set_title("Monthly Revenue (in Million)", loc="center", fontsize=20)
ax.tick_params(axis='y', labelsize=15)
ax.tick_params(axis='x', labelsize=8)
 
st.pyplot(fig)
st.markdown("<p style='color: white;'>Highest revenue in a month reached around US$1 million, precisely in May 2018.</p>", unsafe_allow_html=True)

st.subheader("Customer Order per City")
 
fig, ax = plt.subplots(nrows=1, ncols=2, figsize=(35, 15))
 
colors = ["#105E20", "#167429", "#198E30", "#24AA3F", "#63C777"]
colors2 = ["#5A0505", "#5A0505", "#5A0505", "#5A0505", "#5A0505"]
 
sns.barplot(x="order_id", y="customer_city", data=customer_city_orders.sort_values(by="order_id", ascending=False).head(5), palette=colors, ax=ax[0])
ax[0].set_ylabel(None)
ax[0].set_xlabel("Number of Orders", fontsize=30)
ax[0].set_title("Top 10 Cities with Most Orders", loc="center", fontsize=50)
ax[0].tick_params(axis='y', labelsize=35)
ax[0].tick_params(axis='x', labelsize=30)
 
sns.barplot(x="order_id", y="customer_city", data=customer_city_orders.sort_values(by="order_id", ascending=True).head(5), palette=colors2, ax=ax[1])
ax[1].set_ylabel(None)
ax[1].set_xlabel("Number of Orders", fontsize=30)
ax[1].invert_xaxis()
ax[1].yaxis.set_label_position("right")
ax[1].yaxis.tick_right()
ax[1].set_title("Top 10 Cities with Least Orders", loc="center", fontsize=50)
ax[1].tick_params(axis='y', labelsize=35)
ax[1].tick_params(axis='x', labelsize=30)
 
st.pyplot(fig)

st.subheader("Customer Order per States")
 
fig, ax = plt.subplots(nrows=1, ncols=2, figsize=(35, 15))
 
colors = ["#105E20", "#167429", "#198E30", "#24AA3F", "#63C777"]
colors2 = ["#5A0505", "#7B0F0F", "#953D3D", "#C15050", "#CB6969"]
 
sns.barplot(x="order_id", y="customer_state", data=customer_states_orders.sort_values(by="order_id", ascending=False).head(5), palette=colors, ax=ax[0])
ax[0].set_ylabel(None)
ax[0].set_xlabel("Number of Orders", fontsize=30)
ax[0].set_title("Top 10 States with Most Orders", loc="center", fontsize=50)
ax[0].tick_params(axis='y', labelsize=35)
ax[0].tick_params(axis='x', labelsize=30)
 
sns.barplot(x="order_id", y="customer_state", data=customer_states_orders.sort_values(by="order_id", ascending=True).head(5), palette=colors2, ax=ax[1])
ax[1].set_ylabel(None)
ax[1].set_xlabel("Number of Orders", fontsize=30)
ax[1].invert_xaxis()
ax[1].yaxis.set_label_position("right")
ax[1].yaxis.tick_right()
ax[1].set_title("Top 10 States with Least Orders", loc="center", fontsize=50)
ax[1].tick_params(axis='y', labelsize=35)
ax[1].tick_params(axis='x', labelsize=30)

st.pyplot(fig)

st.subheader("Best & Worst Performing Product based on Order")
 
fig, ax = plt.subplots(nrows=1, ncols=2, figsize=(35, 15))
 
colors = ["#105E20", "#167429", "#198E30", "#24AA3F", "#63C777"]
colors2 = ["#5A0505", "#5A0505", "#5A0505", "#5A0505", "#5A0505"]
 
sns.barplot(x="order_id", y="product_id", data=product_orders.sort_values(by="order_id", ascending=False).head(5), palette=colors, ax=ax[0])
ax[0].set_ylabel(None)
ax[0].set_xlabel("Number of Sales", fontsize=30)
ax[0].set_title("Best Performing Product", loc="center", fontsize=50)
ax[0].tick_params(axis='y', labelsize=35)
ax[0].tick_params(axis='x', labelsize=30)
 
sns.barplot(x="order_id", y="product_id", data=product_orders.sort_values(by="order_id", ascending=True).head(5), palette=colors2, ax=ax[1])
ax[1].set_ylabel(None)
ax[1].set_xlabel("Number of Sales", fontsize=30)
ax[1].invert_xaxis()
ax[1].yaxis.set_label_position("right")
ax[1].yaxis.tick_right()
ax[1].set_title("Worst Performing Product", loc="center", fontsize=50)
ax[1].tick_params(axis='y', labelsize=35)
ax[1].tick_params(axis='x', labelsize=30)

st.pyplot(fig)

st.subheader("Best & Worst Performing Product based on Revenue")
 
fig, ax = plt.subplots(nrows=1, ncols=2, figsize=(35, 15))
 
colors = ["#105E20", "#167429", "#198E30", "#24AA3F", "#63C777"]
colors2 = ["#5A0505", "#7B0F0F", "#953D3D", "#C15050", "#CB6969"]
 
sns.barplot(x="price", y="product_id", data=product_revenue.sort_values(by="price", ascending=False).head(5), palette=colors, ax=ax[0])
ax[0].set_ylabel(None)
ax[0].set_xlabel("Total Revenue", fontsize=30)
ax[0].set_title("Best Performing Product", loc="center", fontsize=50)
ax[0].tick_params(axis='y', labelsize=35)
ax[0].tick_params(axis='x', labelsize=30)
 
sns.barplot(x="price", y="product_id", data=product_revenue.sort_values(by="price", ascending=True).head(5), palette=colors2, ax=ax[1])
ax[1].set_ylabel(None)
ax[1].set_xlabel("Total Revenue", fontsize=30)
ax[1].invert_xaxis()
ax[1].yaxis.set_label_position("right")
ax[1].yaxis.tick_right()
ax[1].set_title("Worst Performing Product", loc="center", fontsize=50)
ax[1].tick_params(axis='y', labelsize=35)
ax[1].tick_params(axis='x', labelsize=30)

st.pyplot(fig)

st.subheader("Best & Worst Performing Product Category")
 
fig, ax = plt.subplots(nrows=1, ncols=2, figsize=(35, 15))
 
colors = ["#105E20", "#167429", "#198E30", "#24AA3F", "#63C777"]
colors2 = ["#5A0505", "#7B0F0F", "#953D3D", "#C15050", "#CB6969"]
 
sns.barplot(x="price", y="product_category_name", data=product_cat_revenue.sort_values(by="price", ascending=False).head(5), palette=colors, ax=ax[0])
ax[0].set_ylabel(None)
ax[0].set_xlabel("Total Revenue", fontsize=30)
ax[0].set_title("Best Performing Product Category (revenue in Million)", loc="center", fontsize=50)
ax[0].tick_params(axis='y', labelsize=35)
ax[0].tick_params(axis='x', labelsize=30)
 
sns.barplot(x="price", y="product_category_name", data=product_cat_revenue.sort_values(by="price", ascending=True).head(5), palette=colors2, ax=ax[1])
ax[1].set_ylabel(None)
ax[1].set_xlabel("Total Revenue", fontsize=30)
ax[1].invert_xaxis()
ax[1].yaxis.set_label_position("right")
ax[1].yaxis.tick_right()
ax[1].set_title("Worst Performing Product Category", loc="center", fontsize=50)
ax[1].tick_params(axis='y', labelsize=35)
ax[1].tick_params(axis='x', labelsize=30)

st.pyplot(fig)

st.subheader("Best Customer Based on RFM Parameters")
 
col1, col2, col3 = st.columns(3)
 
with col1:
    avg_recency = round(rfm_df.recency.mean(), 1)
    st.metric("Average Recency (days)", value=avg_recency)
 
with col2:
    avg_frequency = round(rfm_df.frequency.mean(), 2)
    st.metric("Average Frequency", value=avg_frequency)
 
with col3:
    avg_frequency = format_currency(rfm_df.monetary.mean(), "USD", locale='es_CO') 
    st.metric("Average Monetary", value=avg_frequency)
 
fig, ax = plt.subplots(nrows=1, ncols=2, figsize=(35, 15))
colors = ["#90CAF9", "#90CAF9", "#90CAF9", "#90CAF9", "#90CAF9"]
 
sns.barplot(y="customer_id", x="frequency", data=rfm_df.sort_values(by="frequency", ascending=False).head(5), palette=colors, ax=ax[0])
ax[0].set_ylabel("customer_id", fontsize=30)
ax[0].set_xlabel("Frequency", fontsize=30)
ax[0].set_title("By Frequency", loc="center", fontsize=50)
ax[0].tick_params(axis='y', labelsize=30)
ax[0].tick_params(axis='x', labelsize=35)
 
sns.barplot(y="customer_id", x="monetary", data=rfm_df.sort_values(by="monetary", ascending=False).head(5), palette=colors, ax=ax[1])
ax[1].set_ylabel("customer_id", fontsize=30)
ax[1].set_xlabel("Frequency", fontsize=30)
ax[1].invert_xaxis()
ax[1].yaxis.set_label_position("right")
ax[1].yaxis.tick_right()
ax[1].set_title("By Monetary", loc="center", fontsize=50)
ax[1].tick_params(axis='y', labelsize=30)
ax[1].tick_params(axis='x', labelsize=35)
 
st.pyplot(fig)
 
st.caption('Copyright (c) Giselle Halim - 2024')
st.caption('Source: Dicoding "Analisis Data dengan Python" Course')


