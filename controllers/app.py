import streamlit as st
import numpy as np
import pickle

# Load the trained model
with open('which_crop.pickle', 'rb') as f:
    model = pickle.load(f)

# Define the Streamlit app
def main():
    st.title("Crop Recommendation System")

    # Collect user input
    st.sidebar.header("Input Parameters")

    nitrogen = st.sidebar.slider('Nitrogen (N)', 0, 200, 50)
    phosphorous = st.sidebar.slider('Phosphorous (P)', 0, 200, 50)
    potassium = st.sidebar.slider('Potassium (K)', 0, 200, 50)
    temperature = st.sidebar.slider('Temperature (°C)', 0, 50, 25)
    humidity = st.sidebar.slider('Humidity (%)', 0, 100, 50)
    ph = st.sidebar.slider('pH of Soil', 0, 14, 7)
    rainfall = st.sidebar.slider('Rainfall (mm)', 0, 300, 100)

    # Make prediction
    input_features = np.array([[nitrogen, phosphorous, potassium, temperature, humidity, ph, rainfall]])
    prediction = model.predict(input_features)

    # Display result
    st.write("### Crop Recommendation:")
    st.write(f"The suggested crop for the given climatic conditions is: **{prediction[0]}**")

if __name__ == "__main__":
    main()
