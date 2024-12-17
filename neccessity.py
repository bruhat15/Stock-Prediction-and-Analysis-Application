
import plotly.express as px
import streamlit as st
from sklearn.preprocessing import StandardScaler, LabelEncoder, MinMaxScaler
import pandas as pd
def plot_graph(data,graphs,x_axis,y_axis,g_type=None):
     for graph in graphs.values():
                if graph[0] == x_axis and graph[1] == y_axis:
                 graph_type = graph[2]
                
                # Check if columns exist in data
                 if x_axis in data.columns and y_axis in data.columns:
                    if graph_type == "Line" or graph_type==g_type:
                        fig = px.line(data, x=x_axis, y=y_axis, title=f'{y_axis} Over Time', labels={x_axis: x_axis, y_axis: y_axis})
                    elif graph_type == "Bar" or graph_type==g_type:
                        fig = px.bar(data, x=x_axis, y=y_axis, title=f'{y_axis} Over Time', labels={x_axis: x_axis, y_axis: y_axis})
                    elif graph_type == "Scatter" or graph_type==g_type:
                        fig = px.scatter(data, x=x_axis, y=y_axis, title=f'{y_axis} Over Time', labels={x_axis: x_axis, y_axis: y_axis})
                    elif graph_type == "Histogram" or graph_type==g_type:
                        fig = px.histogram(data, x=x_axis, y=y_axis, title=f'{y_axis} Over Time', labels={x_axis: x_axis, y_axis: y_axis})
                    elif graph_type == "Box" or graph_type==g_type:
                        fig = px.box(data, x=x_axis, y=y_axis, title=f'{y_axis} Over Time', labels={x_axis: x_axis, y_axis: y_axis})
                    elif graph_type == "Violin" or graph_type==g_type:
                        fig = px.violin(data, x=x_axis, y=y_axis, title=f'{y_axis} Over Time', labels={x_axis: x_axis, y_axis: y_axis})
                    elif graph_type == "Area" or graph_type==g_type:
                        fig = px.area(data, x=x_axis, y=y_axis, title=f'{y_axis} Over Time', labels={x_axis: x_axis, y_axis: y_axis})
                    elif graph_type == "Pie" or graph_type==g_type:
                        fig = px.pie(data, names=x_axis, values=y_axis, title=f'{y_axis} Over Time')
                    elif graph_type == "Treemap" or graph_type==g_type:
                        fig = px.treemap(data, path=[x_axis], values=y_axis, title=f'{y_axis} Over Time')
                    elif graph_type == "Sunburst" or graph_type==g_type:
                        fig = px.sunburst(data, path=[x_axis], values=y_axis, title=f'{y_axis} Over Time')
        
                    
                 if fig:
                      return fig,graph_type

def get_prompt(data):
    prompt=', '.join(data) + '''\nYou have a dataset with the following columns: column_names. 
            1. Identify which column is the target variable to be predicted. Provide this in one word. 
            2. For each of the remaining columns, specify how you would visualize the data using different types of graphs. Provide the graph details in the following format:
            x_axis, y_axis, graph_type \  
            x_axis, y_axis, graph_type \ 
            predicted data
            and so on for each graph type.but give the useful graph than just giving it
            For example:
            Date, Open, Line\ 
            Date, Volume, Bar\
            close
            do not mention entire columns details
            Output the graph details as a string with each entry separated by a backslash (`\`). At the end of the string, include the column name to be predicted in one word.
            give underscore for space
            Do not include any additional text other than this format.
            give only top 8 graphical info
            give exactly what i asked you to do
            '''   
    return prompt

def preprocess(data):
                # Convert index to 'Date' column if needed
                if 'Date' not in st.session_state.data.columns and isinstance(st.session_state.data.index, pd.DatetimeIndex):
                     data['Date'] = data.index
                if data.any:
                     st.markdown("nullity observed.how do you want to sort out?!.....")
                if st.checkbox("Drop rows with missing values"):
                    data = data.dropna()
                else:
                    fill_value = st.selectbox("Fill missing values with:", ["mean", "median", "custom"])
                    if fill_value == "mean":
                        data = data.fillna(data.mean())
                    elif fill_value == "median":
                        data = data.fillna(data.median())
                    elif fill_value == "custom":
                        custom_value = st.text_input("Custom value:")
                        data = data.fillna(custom_value)
                    
                categorical_cols = data.select_dtypes(include=['object']).columns
                if len(categorical_cols):
                    columns_to_encode = st.multiselect(
                        'Select columns to label encode',
                        options=categorical_cols,
                        default=[]
                    )
                    if columns_to_encode:
                        for col in columns_to_encode:
                            if col in categorical_cols:
                                le = LabelEncoder()
                                data[col] = le.fit_transform(data[col])

                # Feature Scaling
                numerical_cols = data.select_dtypes(include=['float64', 'int64']).columns
                if len(numerical_cols):
                    columns_to_scale = st.multiselect(
                        'Select columns to scale',
                        options=numerical_cols,
                        default=[]
                    )

                    scaler = StandardScaler()
                    
                    if columns_to_scale:
                        for col in columns_to_scale:
                            if col in numerical_cols:
                                data[col] = scaler.fit_transform(data[[col]])
                return data

def chat_bot(model):

                    for message in st.session_state.messages:
                        with st.chat_message(message["role"]):
                            st.markdown(message["content"])

                    # Collect user input
                    prompt = st.chat_input("What is up?")
                    
                    if prompt:
                        # Display the user message
                        with st.chat_message("user"):
                            st.markdown(prompt)
                        st.session_state.messages.append({"role": "user", "content": prompt})

                        # Generate response from Google Generative AI
                        with st.chat_message("assistant"):
                            
                            message_placeholder = st.empty()
                            full_response = ""
                            prompt='''This website predicts stock prices and includes the following main features:

User-Friendly Interface: Easy navigation for all user levels.
Real-Time Data: Live updates on stock prices and market trends.
Predictive Models: Advanced machine learning for future price predictions.
Technical Analysis Tools: Indicators like moving averages, RSI, and MACD.
Interactive Charts: Customizable and high-quality charts.
Custom Alerts: Notifications for significant market movements.
Educational Resources: Tutorials and articles on stock market basics.
Backtesting: Test strategies on historical data.
News Feed: Latest financial news and market analysis.
Portfolio Management: Track and analyze investments.
Security and Privacy: Strong measures to protect user data.
This platform aids investors in making informed trading decisions.this is my content imagine you are chat for stocks only and based on the content give me answer
,i am giving prompt, answer properly.give in small short words'''+prompt
                    
                        response = model.generate_content(prompt)
                        full_response = response.text
                        st.write(full_response)
                        message_placeholder.markdown(full_response)

                        st.session_state.messages.append({"role": "assistant", "content": full_response})