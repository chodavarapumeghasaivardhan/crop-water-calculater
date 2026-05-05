import streamlit as st
import pyodbc
import pandas as pd

# Database connection
conn = pyodbc.connect(
    "DRIVER={SQL Server};"
    "SERVER=SAIVARDHAN;"
    "DATABASE=farm_db;"
    "Trusted_Connection=yes;"
)

cursor = conn.cursor()

# Load crop data
query = "SELECT * FROM crops_water"
df = pd.read_sql(query, conn)

st.title("🌾 Crop Water Requirement Calculator")

# Crop dropdown
crop = st.selectbox("Select Crop", df["crop_name"])

# Land input
land = st.number_input("Enter Land Size (Acres)", min_value=0.0)

# Calculate button
if st.button("Calculate Water Requirement"):

    water_per_acre = df[df["crop_name"] == crop]["water_per_acre"].values[0]

    total_water = water_per_acre * land

    st.success(f"Water Required: {total_water} Liters")

    # Save result in irrigation_records table
    cursor.execute(
        "INSERT INTO irrigation_records (crop_name, land_size, water_required) VALUES (?, ?, ?)",
        crop, land, int(total_water)
    )
    conn.commit()


# -------------------------------
# Feature 1: Irrigation History
# -------------------------------

st.subheader("📊 Irrigation History")

history_query = "SELECT * FROM irrigation_records"
history_df = pd.read_sql(history_query, conn)

st.dataframe(history_df)


# -------------------------------
# Feature 2: Crop Water Chart
# -------------------------------

st.subheader("🌾 Crop Water Requirement Chart")

chart_data = pd.read_sql("SELECT * FROM crops_water", conn)

st.bar_chart(chart_data.set_index("crop_name"))