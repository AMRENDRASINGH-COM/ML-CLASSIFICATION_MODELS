import streamlit as st
import numpy as np
import pandas as pd
import pickle

with open ('final_model_gradient.pkl','rb') as file:
    model=pickle.load(file)


def prediction (lt,mst,spcl,price,adult,wkend,park,wk,ar_d,ar_m,ar_w):
    input_list=np.array(input_list,dtype='object')

    pred = model.predict_proba(input_list)[:,1][0]

    if pred>0.5:
        return f"THIS BOOKING IS MORE LIKELY TO GET CANCELED: PROBABILITY={round(pred*100,2)}"
    else:
        return f"THIS BOOKING IS LESS LIKELY TO GET CANCELED: PROBABILITY={round(pred*100,2)}"
    


    def main():
        st.image(r'C:\Users\amren\Desktop\ALL PROJECTS\INN HOTEL BOOKING CANCELATION PROJECT',use_column_width=True)
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

        input_list=[[lt,mst,spcl,price,adult,wkend,park,wk,ar_d,ar_m,ar_w]]

    if st.button('Predict'):
        responce=prediction(input_data)
        st.success(responce)


    if _name_ =='_main_':
        main()

