import streamlit as st
import pandas as pd
import joblib
import json

crop_data = pd.read_csv("./dataset/final_data.csv")


model = joblib.load('./model/crop_yield_predictor_model.joblib')

with open('model_columns.json', 'r') as f:
    model_columns = json.load(f)

st.title('Andhra Pradesh Crop Yield Predictor')
st.write("Enter the details below to get a predicted crop yield (in tonnes per hectare).")

col1, col2 = st.columns(2)

with col1:
    
    districts = crop_data['District'].unique()
    crops = crop_data['Crop'].unique()
    seasons = crop_data['Season'].unique()

    district = st.selectbox('Select District:', districts)
    crop = st.selectbox('Select Crop:', crops)
    season = st.selectbox('Select Season:', seasons)

with col2:
    year = st.slider('Select Year for Scenario:', min_value=2000, max_value=2020,value=2020)
    area = st.number_input('Area (in Hectares):', min_value=1.0, value=100.0)
    rainfall = st.slider('Total Seasonal Rainfall (mm):', 0, 1500, 500)
    avg_temp_max = st.slider('Average Max Temperature (°C):', 25.0, 45.0, 35.0)
    avg_temp_min = st.slider('Average Min Temperature (°C):', 10.0, 30.0, 24.0)



if st.button('Predict Yield'):
    input_data = {
        'Year': [year],
        'Area': [area],
        'Rainfall_mm': [rainfall],
        'Temp_Max_C': [avg_temp_max],
        'Temp_Min_C': [avg_temp_min],
        'District': [district],
        'Season': [season],
        'Crop': [crop]
    }
    input_df = pd.DataFrame(input_data)

    input_df_encoded = pd.get_dummies(input_df)
    
    final_df = input_df_encoded.reindex(columns=model_columns, fill_value=0)
    
    prediction = model.predict(final_df)
    
    st.success(f"Predicted Crop Yield: {prediction[0]:.2f} tonnes per hectare")