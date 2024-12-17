import streamlit as st
import streamlit.components.v1 as components

import pandas as pd
import time
import math
from datetime import datetime
import numpy as np
import plotly.express as px
import yfinance as yf
import google.generativeai as genai

import login as log
#import contact_us
import dash
import neccessity as ns
from sklearn.preprocessing import StandardScaler, MinMaxScaler
from tensorflow.keras.models import Sequential # type: ignore
from tensorflow.keras.layers import LSTM, Dense# type: ignore

graph_dict = {}


def logout():
    # Clear session state variables
    for key in st.session_state.keys():
        del st.session_state[key]
    # Redirect to login page
    st.experimental_set_query_params(page="home")
    st.experimental_rerun()

def main():



    query_params = st.experimental_get_query_params()
    page = query_params.get("page", ["home"])[0]

    if page == "home":
        main_content()
    elif page=="Log out":
        logout()
    #elif page == "contact":
    #    contact_us.content()
   

def main_content():
    genai.configure(api_key="AIzaSyDGII91j6AeLADRUwAZG3D91cbph82QmGk")
    model = genai.GenerativeModel(model_name="gemini-1.5-flash")
    #https://www.kommunicate.io/livechat-demo?appId=66bb54c666b024ed3206701e2d30ef08&botIds=stock-chat-bot-mn0je&assignee=stock-chat-bot-mn0je
    kommunicate_html = """
            <!--Kommunicate live chat widget-->
            
            <script type="text/javascript">
            (function(d, m){
                var kommunicateSettings = 
                    {"appId":"66bb54c666b024ed3206701e2d30ef08","botIds":["stock-chat-bot-mn0je"],"assignee":"stock-chat-bot-mn0je","popupWidget":true,"automaticChatOpenOnNavigation":true};
                var s = document.createElement("script"); s.type = "text/javascript"; s.async = true;
                s.src = "https://widget.kommunicate.io/v2/kommunicate.app";
                var h = document.getElementsByTagName("head")[0]; h.appendChild(s);
                window.kommunicate = m; m._globals = kommunicateSettings;
            })(document, window.kommunicate || {});
            </script>
            <!--End of Kommunicate live chat widget-->


                """
        #with contact_col:
        #    if st.button("Contact Us"):
        #        st.experimental_set_query_params(page="contact")
        #        st.experimental_rerun()

    try:
        def toggle_sidebar():
            if 'sidebar_visible' not in st.session_state:
                st .session_state.sidebar_visible = True
            st.session_state.sidebar_visible = not st.session_state.sidebar_visible

        if 'sidebar_visible' not in st.session_state or st.session_state.sidebar_visible:
            with st.sidebar:
                
                initialize_session_state()
                if st.button("Log Out  !!"):
                        st.experimental_set_query_params(page="Log out")
                        st.experimental_rerun()
                st.session_state.navbar = st.selectbox("Select", ["dashboard", "data analysis and prediction"])
                
                
                if st.session_state.navbar == "dashboard":
                    placeholder_1=st.empty
                    placeholder_2=st.empty
                    
                else:
                    handle_data_input()
                # Embed Kommunicate chat widget https://www.kommunicate.io/livechat-demo?appId=1aae2ce04fa51dbbd2e01c443dc492332&botIds=stocker-rfcxg&assignee=stocker-rfcxg

                components.html(kommunicate_html, height=700)
        if st.session_state.navbar == "dashboard":
              dash.dashboard_content(placeholder_1,placeholder_2)
        else:
            handle_analysis_and_prediction(model)
    except Exception as e:
        st.write(e)

def initialize_session_state():
    if 'chatbot_active' not in st.session_state:
        st.session_state.chatbot_active = False
    if 'data' not in st.session_state:
        st.session_state.data = None
    if 'messages' not in st.session_state:
        st.session_state.messages = []
    if 'stock_symbol' not in st.session_state:
        st.session_state.stock_symbol = ""
    if 'uploaded_file' not in st.session_state:
        st.session_state.uploaded_file = None

def handle_data_input():
    selection = st.selectbox("Select the data input type:", ["download from internet", "upload files"])
    try:
        if selection == "download from internet":
            st.session_state.stock_symbol = st.text_input("Give a stock symbol:", st.session_state.stock_symbol)
            if st.session_state.stock_symbol:
                end_date = datetime.today().date()
                data = yf.download(st.session_state.stock_symbol, start="2020-01-01", end=end_date)
        else:
            st.session_state.uploaded_file = st.file_uploader("Upload a file", type=["csv"], key='file_uploader')
            if st.session_state.uploaded_file is not None:
                data = pd.read_csv(st.session_state.uploaded_file)
    except ValueError as e:
        st.write("No files uploaded yet")
    try:
        if st.session_state.data is None or not st.session_state.data.equals(data):
            st.session_state.data = pd.DataFrame(data)
        if st.session_state.data is not None:
            st.write("Original Data:")
            st.write(st.session_state.data.head(2000))
            st.session_state.data = ns.preprocess(st.session_state.data)
    except Exception as e:
        print()

def handle_analysis_and_prediction(model):
    data = st.session_state.data
    try:
        if 'data' in locals():
            prompt = ns.get_prompt(data.columns)
            response = model.generate_content(prompt)
            response_text = response.text

            content = parse_response(response_text)

            if 'Date' not in data.columns and isinstance(data.index, pd.DatetimeIndex):
                data['Date'] = data.index

            predicted_data = content.get('predicted_data', '').replace('_', ' ')
            graphs = {key: value for key, value in content.items() if key != 'predicted_data'}
            st.markdown(f"Data size: {data.shape}")
            st.write(data)
            st.session_state.x_axis, st.session_state.y_axis = select_axes(content)
            x_axis,y_axis=st.session_state.x_axis,st.session_state.y_axis

            fig, graph_type = ns.plot_graph(data, graphs, x_axis, y_axis)
            st.plotly_chart(fig)
                
            
            train_and_predict(data, predicted_data)
    except Exception as e:
        st.spinner("please wait")
   
def parse_response(response_text):
    content = {}
    cnt = 0
    entries = response_text.strip().split("\\")
    for entry in entries:
        elements = entry.strip().split(",")
        if len(elements) == 1:
            content["predicted_data"] = elements[0].strip()
        else:
            content[f"graph{cnt}"] = [e.strip() for e in elements]
            cnt += 1
    return content

def select_axes(content):
    col1, col2 = st.columns(2)
    with col1:
        x_axis = st.selectbox("x_axis", set([i[0] for i in content.values() if i != 'predicted_data' and len(i[0]) > 1]))
    with col2:
        y_axis = st.selectbox("y_axis", set([i[1] for i in content.values() if i != 'predicted_data' and len(i[1]) > 1]))
    return x_axis, y_axis

def train_and_predict(data, predicted_data):
    # Set epochs and batch size
    epochs = st.slider("epochs", 0, 100, 9)
    batch_size = 1
    data = yf.download(st.session_state.stock_symbol, start="2022-01-01", end=datetime.today())

    # Filter and prepare data
    df = data.filter([predicted_data])
    dataset = df.values

    # Define the length of training data
    training_data_len = math.ceil(len(dataset) * 0.8)

    # Check dataset shape
    if data.shape[0] != len(data):
        st.error("The dataset has an incorrect shape for processing.")
    else:
        # Scale the data
        scaler = MinMaxScaler(feature_range=(0, 1))
        scaled_data = scaler.fit_transform(dataset)

        # Prepare training data
    train_data = scaled_data[0:training_data_len]
    x_train, y_train = [], []

    for i in range(60, len(train_data)):
        x_train.append(train_data[i-60:i, 0])
        y_train.append(train_data[i, 0])

    x_train, y_train = np.array(x_train), np.array(y_train)
    x_train = np.reshape(x_train, (x_train.shape[0], x_train.shape[1], 1))
    st.write("x_train shape:", x_train.shape)

    placeholder_3 = st.empty()
    
    # Add stop button
    stop_button_placeholder = st.empty()
    stop_button = stop_button_placeholder.button("Stop")
    
    if stop_button:
        st.session_state.stop_training = True
    
    if placeholder_3.button("predict"):
        start_time = time.time()
        
        model = Sequential()
        model.add(LSTM(100, return_sequences=True, input_shape=(x_train.shape[1], 1)))
        model.add(LSTM(100, return_sequences=True))
        model.add(LSTM(100, return_sequences=False))
        model.add(Dense(50))
        model.add(Dense(50))
        model.add(Dense(50))

        model.add(Dense(50))
        model.add(Dense(1))

        model.compile(optimizer='adam', loss='mean_squared_error')

        st.write("Training the model...")

        for epoch in range(epochs):
            if 'stop_training' in st.session_state and st.session_state.stop_training:
                st.write("Training stopped.")
                break
            model.fit(x_train, y_train, epochs=1, batch_size=batch_size, verbose=1)
        else:
            st.session_state.data = data

            st.write("Model trained")
            
        # Reset stop_training flag
        st.session_state.stop_training = False
        stop_button_placeholder.empty()
    

        end_time = time.time()
        training_duration = end_time - start_time
        st.write(f"Training time: {training_duration:.2f} seconds")

    # Prepare testing data
    test_data = scaled_data[training_data_len - 60:]
    x_test, y_test = [], dataset[training_data_len:]

    for i in range(60, len(test_data)):
        x_test.append(test_data[i-60:i, 0])

    x_test = np.array(x_test)
    x_test = np.reshape(x_test, (x_test.shape[0], x_test.shape[1], 1))

    start_time = time.time()

    # Get the model's predictions
    predictions = model.predict(x_test)
    predictions = scaler.inverse_transform(predictions)

    end_time = time.time()
    prediction_duration = end_time - start_time
    st.write(f"Prediction time: {prediction_duration:.2f} seconds")

    # Calculate RMSE
    rmse = np.sqrt(np.mean((predictions - y_test) ** 2))
    st.write("RMSE:", rmse)

    # Plot the data
    train = data[:training_data_len]
    valid = data[training_data_len:]
    valid['Predictions'] = predictions

    st.line_chart({
        'Train': train[predicted_data],
        'Validation': valid[predicted_data],
        'Predictions': valid['Predictions']
    })

        
if __name__ == "__main__":
    if 'authentication_status' not in st.session_state:
        st.session_state.authentication_status = False
        
    user = log.login_signup()
    if user is not None and st.session_state.authentication_status:
        st.session_state["username"] = user
        main()
    else:
        st.write("Invalid credentials")
