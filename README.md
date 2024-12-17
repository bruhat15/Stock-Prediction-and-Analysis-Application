The system combines Long Short-Term Memory (LSTM) neural networks for time series prediction, Streamlit for an intuitive frontend interface, and Yahoo Finance (yfinance) for fetching real-time stock data.

Key Features:
1.	Dashboard for Stock Monitoring:
o	Displays real-time prices of popular stocks.
o	Supports both Scatter Plot and Area Plot visualizations for comparative price analysis.
o	Individual Candlestick Charts are available for detailed stock performance insights.

3.	Data Input Flexibility:
o	Download Data: Fetches stock data based on user-specified stock symbols (e.g., AAPL, GOOG) and a custom date range starting from January 1, 2024, to the current date.
o	Upload CSV: Users can upload custom stock datasets for analysis and prediction.

4.	Data Preprocessing and Customization:
o	Handles missing values by user-defined methods: mean, median, or custom input.
o	Enables feature scaling for selected numerical columns to improve graph accuracy.

![image](https://github.com/user-attachments/assets/6587e3e5-b470-4682-bf40-00bd66ca1db2)

6.	Interactive Analysis and Visualization:
o	Users can select columns for x-axis and y-axis visualization, providing flexibility in analyzing data trends.
o	Predicts stock trends using an LSTM-based model, with user-defined epochs for optimized results.

8.	Machine Learning Predictions:
o	LSTM model predicts future prices and validates predictions using metrics such as Root Mean Square Error (RMSE).
o	Provides clear visualizations for training, validation, and predictions for easy comparison.

9.	Integrated Stock Chatbot:
o	A chatbot powered by Google Gemini AI provides answers to stock-related queries, enhancing user experience and decision-making capabilities.

10.	User Authentication and Security:
o	Includes a secure login/signup system with email verification and password encryption.
o	Ensures data privacy and personalized user sessions.
