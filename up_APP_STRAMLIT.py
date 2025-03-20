import streamlit as st
import pickle 
import numpy as np
from PIL import Image

# Initialize model as None
model = None

# Load the trained model
try:
    with open("final_model_gradient.pkl", 'rb') as file:
        model = pickle.load(file)
except Exception as e:
    st.error(f"Error loading model: {e}. Please ensure the model file exists and is compatible.")

# Prediction function
def prediction(input_data):
    if model is None:
        return "Model not loaded. Cannot make predictions."
    try:
        # Ensure input_data is a 2D array
        input_data = np.array(input_data).reshape(1, -1)
        pred = model.predict_proba(input_data)[:, 1][0]
        if pred > 0.5:
            return f"This booking is more likely to get canceled: Chances = {round(pred*100, 2)}%"
        else:
            return f"This booking is less likely to get canceled: Chances = {round(pred*100, 2)}%"
    except Exception as e:
        return f"Error during prediction: {e}"

# Main app
def main():
    st.title("INN Hotels - Cancellation Prediction")

    # Display hotel image (with error handling)
    try:
        # Load the image directly (since it's in the same directory)
        image = Image.open("hotel image inn.jpg")
        st.image(image, use_column_width=True)
    except FileNotFoundError:
        st.warning("Hotel image not found. Using a placeholder image.")
        image_url = "https://via.placeholder.com/600x400.png?text=Hotel+Image"
        st.image(image_url, use_column_width=True)
    except Exception as e:
        st.error(f"An error occurred while loading the image: {e}")

    # User inputs
    st.header('Booking Details')
    lead_time = st.number_input('ENTER LEAD TIME', min_value=0, step=1)
    market_segment_type = st.selectbox('SELECT MARKET SEGMENT', ['online', 'offline'])
    no_of_special_requests = st.selectbox('HOW MANY SPECIAL REQUESTS HAVE BEEN MADE?', [0, 1, 2, 3, 4, 5])
    avg_price_per_room = st.number_input('ENTER THE PRICE OF ROOM', min_value=0.0, step=0.1)
    no_of_adults = st.selectbox('HOW MANY ADULTS PER ROOM?', [1, 2, 3, 4])
    no_of_weekend_nights = st.number_input('HOW MANY WEEKEND NIGHTS?', min_value=0, step=1)
    required_car_parking_space = st.selectbox('DOES BOOKING INCLUDE PARKING FARE?', ['Yes', 'No'])
    arrival_day = st.slider('WHAT WILL BE DAY OF ARRIVAL', min_value=1, max_value=31, step=1)
    arrival_month = st.slider('WHAT WILL BE MONTH OF ARRIVAL', min_value=1, max_value=12, step=1)
    arrival_weekday = st.selectbox('WHAT IS THE WEEKDAY OF ARRIVAL?', ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'])

    # Convert categorical inputs to numeric
    market_segment_type = 1 if market_segment_type == 'online' else 0
    required_car_parking_space = 1 if required_car_parking_space == 'Yes' else 0
    arrival_weekday = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'].index(arrival_weekday)

    # Preparing input data for prediction
    input_data = [lead_time, market_segment_type, no_of_special_requests,
                  avg_price_per_room, no_of_adults, no_of_weekend_nights,
                  required_car_parking_space, 0, arrival_day,
                  arrival_month, arrival_weekday]

    # Predict and display the result
    if st.button("Predict"):
        if model is None:
            st.error("Model is not loaded. Cannot make predictions.")
        else:
            response = prediction(input_data)
            st.success(response)

if __name__ == '__main__':
    main()
