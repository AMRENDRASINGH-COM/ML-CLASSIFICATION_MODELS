import gradio as gr
import joblib  # Use joblib instead of pickle
import numpy as np
from warnings import filterwarnings

filterwarnings('ignore')

# Load the trained model
try:
    model = joblib.load("final_model_gradient.pkl")
except Exception as e:
    print(f"Error loading model: {e}. Please ensure the model file exists and is compatible.")
    model = None

# Check if the model has the required attribute
if model is not None and hasattr(model, 'feature_names_in_'):
    print("Model loaded successfully. Feature names:", model.feature_names_in_)
else:
    print("Model is not loaded or does not have the required attributes.")

# Prediction function
def prediction(lt, mst, spcl, price, adult, wkend, park, wk, ar_d, ar_m, ar_w):
    if model is None:
        return "Model not loaded. Cannot make predictions."
    try:
        input_data = [[lt, mst, spcl, price, adult, wkend, park, wk, ar_d, ar_m, ar_w]]
        pred = model.predict_proba(input_data)[:, 1][0]
        if pred > 0.5:
            return f"THIS BOOKING IS MORE LIKELY TO GET CANCELED: PROBABILITY={round(pred * 100, 2)}%"
        else:
            return f"THIS BOOKING IS LESS LIKELY TO GET CANCELED: PROBABILITY={round(pred * 100, 2)}%"
    except Exception as e:
        return f"Error during prediction: {e}"

# Gradio interface
iface = gr.Interface(
    fn=prediction,
    inputs=[
        gr.Number(label='HOW MANY PRIOR DAYS BOOKING WAS MADE'),
        gr.Dropdown([('Online', 1), ('Offline', 0)], label='HOW THE BOOKING WAS MADE'),
        gr.Dropdown([0, 1, 2, 3, 4, 5], label='HOW MANY SPECIAL REQUEST MADE'),
        gr.Number(label='WHAT IS THE PRICE PER ROOM OFFERED'),
        gr.Dropdown([1, 2, 3, 4], label='How Many ADULTS PER ROOM'),
        gr.Number(label='HOW MANY WEEKEND NIGHTS IN THE STAY'),
        gr.Dropdown([('YES', 1), ('NO', 0)], label='DOES BOOKING INCLUDES PARKING FACILITY'),
        gr.Number(label='HOW MANY WEEK NIGHTS IN STAY'),
        gr.Slider(minimum=1, maximum=31, step=1, label='WHAT IS DAY OF ARRIVAL'),
        gr.Slider(minimum=1, maximum=12, step=1, label='WHAT IS MONTH OF ARRIVAL'),
        gr.Dropdown([('Mon', 0), ('Tue', 1), ('Wed', 2), ('Thu', 3), ('Fri', 4), ('Sat', 5), ('Sun', 6)], label='WHAT IS THE WEEKDAY OF ARRIVAL')
    ],
    outputs=gr.Textbox(label='Prediction'),
    title='INN Group of Hotels',
    description='This application will forecast the cancellation of booking',
    allow_flagging='never'
)

# Launch the interface
iface.launch()
