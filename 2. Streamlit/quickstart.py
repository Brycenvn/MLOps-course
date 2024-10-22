import streamlit as st 
# Set the app title 
st.title('My First Streamlit App') 
# Create a text input 
user_input = st.text_input('Enter a Your name:', 'BrycenVN') 
# Display the customized message 
st.write('Hello,' + user_input)