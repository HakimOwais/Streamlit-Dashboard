import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import warnings
warnings.filterwarnings('ignore')

st.set_page_config(page_title="Data Analysis", page_icon=":bar_chart:",layout="wide")

st.title(" :bar_chart: Data Analysis Dashboard ")
st.markdown('<style>div.block-container{padding-top:1rem;}</style>',unsafe_allow_html=True)

# App title
# st.subheader("Upload your dataset")

# Upload file
uploaded_file = st.file_uploader("Upload your dataset", type=["csv","txt","xlsx","xls"])

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    
    if st.button('Click here to load examples'):
        st.write(df.head())
    
    # Exploratory Data Analysis (EDA)
    if st.button("Describe dataset"):
        st.write(df.describe())
    if st.button("Check Missing Values"):
        st.write(df.isna().sum())

    # Data Cleaning
    # df1 =df.copy()
    # Fill numeric rows with the median
    st.subheader("Fill missing values with median")
    for label, content in df.items():
        if pd.api.types.is_numeric_dtype(content):
            if pd.isnull(content).sum():
                # Adding binary column which tells us if the data was missing or not #
                df[label+"_is_missing"]= pd.isnull(content)
                # fill missing values with median 
                df[label] = content.fillna(content.median())
                    
            # Check for columns which are not numeric
    for label, content in df.items():
        if not pd.api.types.is_numeric_dtype(content):
            print(label)

    for label, content in df.items():
        if not pd.api.types.is_numeric_dtype(content):
            # Adding binary column which tells us if the data was missing or not
            df[label+"_is_missing"]= pd.isnull(content)
            # fill missing values with median
            df[label] = pd.Categorical(content).codes +1
   
    cleaned_df = df.copy()  # Placeholder for outlier-removed DataFrame
    # Display cleaned DataFrame
    if st.button("Cleaned DataFrame Using Median:"):
        st.write(cleaned_df)
    
    columns_to_delete = st.multiselect('Select columns to delete:', cleaned_df.columns)
    if st.button('Delete Columns'):
        if columns_to_delete:
            cleaned_df = cleaned_df.drop(columns=columns_to_delete)
            st.write('DataFrame after column deletion:')
            st.write(cleaned_df)
        else:
            st.warning('Please select at least one column to delete.')
       
    # Provide download link for cleaned dataset
    st.subheader("Download Cleaned Dataset")
    csv = cleaned_df.to_csv(index=False)
    st.download_button("Download CSV", data=csv, file_name='cleaned_data.csv')

    # Plots section
    st.subheader("Create Plots")

    # Column selection for x-axis
    x_column = st.selectbox("Select X-axis Column:", cleaned_df.columns)

    # Column selection for y-axis
    y_column = st.selectbox("Select Y-axis Column:", cleaned_df.columns)

    # Plot type selection
    plot_type = st.selectbox("Select Plot Type:", ["scatter", "bar", "line"])

    # Create the plot
    if plot_type == "scatter":
        fig = px.scatter(cleaned_df, x=x_column, y=y_column, title="Scatter Plot")
    elif plot_type == "bar":
        fig = px.bar(cleaned_df, x=x_column, y=y_column, title="Bar Plot")
    elif plot_type == "line":
        fig = px.line(cleaned_df, x=x_column, y=y_column, title="Line Plot")

    st.plotly_chart(fig)