import streamlit as st
import pickle 
import numpy as np
import pandas as pd
from PIL import Image

# Load the trained model
try:
    with open("final_model_xgb.pkl", 'rb') as file:
        model = pickle.load(file)
except Exception as e:
    st.error(f"Error loading model: {e}")

# Prediction function
def prediction(input_data):
    try:
        pred = model.predict_proba(input_data)[:,1][0]
        if pred > 0.5:
            return f"This booking is more likely to get canceled: Chances = {round(pred*100,2)}%"
        else:
            return f"This booking is less likely to get canceled: Chances = {round(pred*100,2)}%"
    except Exception as e:
        return f"Error during prediction: {e}"

# Main app
def main():
    st.title("INN Hotels - Cancellation Prediction")

    # Display hotel image
    image = Image.open("hotel image inn.jpeg")
    st.image(image, use_container_width=True)

    # User inputs
    st.title('INN HOTEL')
        lt=st.text_input('ENTER LEAD TIME')
        market={'online':1,'offline':0}
        spcl=st.selectbox('HOW MANY SPECIAL REQUESTS HAVE BEEN MADE ?',[0,1,2,3,4,5])
        price=st.text_input('ENTER THE PRICE OF ROOM')
        adults=st.selectbox('HOW MANY ADULTS PER ROOM?',[1,2,3,4])
        wknd=st.text_input('HOW MANY WEEKEND NIGHTS?')
        prk=(lambda x:1 if x=='Yes' else 0)(st.selectbox['DOES BOOKING INCLUDE PARKING FARE'])
        arr_d=st.slider('WHAT WILL BE DAY OF ARRIVAL',min_value=1,max_value=31,step=1)
        arr_m=st.slider('WHAT WILL BE MONTH OF ARRIVAL',min_value=1,max_value=12,step=1)
        wwekd_lambda=(lambda x:0 if x=='Mon' else 1 if x=='Tue' else 2 if x=='Wed' else 3 if x=='Thu' else 4 if x=='Fri' else 5 if x=='Sat' else 6) 
        arr_wd=wwekd_lambda(st.selectbox('WHAT IS THE WEEKDAY OF ARRIVAL?',['Mon','Tue','Wed','Thu','Fri','Sat']))


    # Preparing input data for prediction
    input_data = [[lead_time, market_segment_type, no_of_special_requests,
                   avg_price_per_room, no_of_adults, no_of_weekend_nights,
                   required_car_parking_space, no_of_week_nights, arrival_day,
                   arrival_month, arrival_weekday]]

    # Predict and display the result
    if st.button("Predict"):
        response = prediction(input_data)
        st.success(response)

if __name__ == '__main__':
    main()

