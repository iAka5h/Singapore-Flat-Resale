import pandas as pd
import numpy as np
import pickle
import streamlit as st
from streamlit_option_menu import option_menu
from PIL import Image
import base64
from scipy.stats import skew, kurtosis
import matplotlib.pyplot as plt
import seaborn as sns 

def file():
    data=pd.read_csv('H:/Python/Singapore/ResaleFlatPrices/file1.csv')
    return data


def prediction():
    st.subheader("Let's Predict!")
    st.write(':orange[Fill the form]')

    #Creating dictionary for mapping string to integer
    town_dic={'SENGKANG':20, 'WOODLANDS':24, 'PUNGGOL':17, 'JURONG WEST':13, 'TAMPINES':22, 'YISHUN':25, 'BEDOK':1, 'HOUGANG':11, 'CHOA CHU KANG':8, 'ANG MO KIO':0, 'BUKIT BATOK':3, 'BUKIT MERAH':4, 'BUKIT PANJANG':5, 'TOA PAYOH':23, 'KALLANG/WHAMPOA':14, 'PASIR RIS':16, 'SEMBAWANG':19, 'QUEENSTOWN':18, 'GEYLANG':10, 'CLEMENTI':9, 'JURONG EAST':12, 'SERANGOON':21, 'BISHAN':2, 'CENTRAL AREA':7, 'MARINE PARADE':15, 'BUKIT TIMAH':6}
    flat_type_dic={'4 ROOM':3.0, '5 ROOM':4.0, '3 ROOM':2.0, 'EXECUTIVE':5.0, '2 ROOM':1.0, 'MULTI-GENERATION':6.0, '1 ROOM':0.0}
    flat_model_dic={'Model A':8.0, 'Improved':5.0, 'New Generation':12.0, 'Premium Apartment':13.0, 'Simplified':16.0, 'Apartment':3.0, 'Maisonette':7.0, 'Standard':17.0, 'DBSS':4.0, 'Model A2':10.0, 'Type S1':19.0, 'Model A-Maisonette':9.0, 'Adjoined flat':2.0, 'Type S2':20.0, 'Terrace':18.0, '2-room':0.0, 'Premium Apartment Loft':14.0, 'Multi Generation':11.0, '3Gen':1.0, 'Improved-Maisonette':6.0, 'Premium Maisonette':15.0}

    #dropdown for categorical features
    town_options=['ANG MO KIO', 'BEDOK', 'BISHAN', 'BUKIT BATOK', 'BUKIT MERAH','BUKIT TIMAH', 'CENTRAL AREA', 'CHOA CHU KANG', 'CLEMENTI',
        'GEYLANG', 'HOUGANG', 'JURONG EAST', 'JURONG WEST','KALLANG/WHAMPOA', 'MARINE PARADE', 'QUEENSTOWN', 'SENGKANG',
        'SERANGOON', 'TAMPINES', 'TOA PAYOH', 'WOODLANDS', 'YISHUN','LIM CHU KANG', 'SEMBAWANG', 'BUKIT PANJANG', 'PASIR RIS',
        'PUNGGOL']
    flat_type_options=['1 ROOM', '3 ROOM', '4 ROOM', '5 ROOM', '2 ROOM', 'EXECUTIVE','MULTI GENERATION']
    flat_model_options=['IMPROVED', 'NEW GENERATION', 'MODEL A', 'STANDARD', 'SIMPLIFIED','MODEL A-MAISONETTE', 'APARTMENT', 'MAISONETTE', 'TERRACE',
        '2-ROOM', 'MULTI GENERATION', 'PREMIUM APARTMENT', 'Adjoined flat','Premium Maisonette', 'Model A2', 'DBSS', 'Type S1', 'Type S2',
        'Premium Apartment Loft', '3Gen']
    

    with st.form('resale price'):
        
        col1, col2, col3 =st.columns(3)
        with col1:
            town=st.selectbox('**Select the Town**', options=town_options)
            flat_type=st.selectbox('**Select the Flat Type**', options=flat_type_options)
            flat_model=st.selectbox('**Select the Flat Model**', options=flat_model_options)
            floor_area_sqm=st.number_input('**Enter the Floor Area sqm (range 34 to 158)**', min_value=34, max_value=158)
            lease_commence_year=st.selectbox('**Select the Lease Commence Year**', [str(i) for i in range(1966, 2020)])

        with col3:
            sale_year=st.selectbox('**Sale Year**', [str(i) for i in range(2015, 2024)])
            floors_start=st.selectbox('**Enter the Floor start value**', [str(i) for i in range(1, 40)])
            floors_end=st.selectbox('**Enter the Floor end value**', [str(i) for i in range(1, 42)])
            remaining_lease_years=st.selectbox('**Remaining Lease Years**', [str(i) for i in range(41, 97)])

            st.write('')
            st.write('')
            Button=st.form_submit_button(label='**:orange[SUBMIT]**')

        if Button:
            with open('H:/Python/Singapore/ResaleFlatPrices/Regression_model.pkl', 'rb') as file:
                reg_model=pickle.load(file)    

            #convert the dic features to the corresponding integers
            town_int=town_dic.get(town)
            flat_type_int=flat_type_dic.get(flat_type)
            flat_model_int=flat_model_dic.get(flat_model)

            user=reg_model.predict(np.array([[sale_year, town_int, flat_type_int, floor_area_sqm, flat_model_int, np.log(float(floors_start)), np.log(float(floors_end)), lease_commence_year, remaining_lease_years]]))
            resale_price=np.exp(user[0])
            resale_price=round(resale_price, 2)

            st.header(f':green[Predicted Resale Price : S$ {resale_price}]')
            st.caption(body='All Price in S$ (SGD)')


def statistics(): 
    st.header('INSIGHTS & STATISTICS')
    df3=file()

    st.subheader('Methodology')
    st.markdown('##### :orange[1. Data Exploration and Preprocessing]')
    st.markdown("""
                - **Conduct exploratory data analysis (EDA) to uncover patterns, correlations, and anomalies.**
                - **Address skewness and noise through techniques such as log transformation and data normalization.**
                - **Detect and handle outliers to ensure data quality and model reliability.**
                """)
    st.markdown('##### :orange[2. Regression Model Development]')
    st.markdown("""
                - **Implement a machine learning regression model using algorithms robust to skewed and noisy data, such as Random Forest and mulitple regression models.**
                - **Optimize model techniques like GridSearchCV, Scalings are not required, Since my RF model has already achieved good accuracy scores.**
                """)
    st.markdown('##### :orange[3. Streamlit Dashboard Implementation]')
    st.markdown("""
                - **Design an intuitive Streamlit interface to facilitate user interaction and data input.**
                - **Integrate predictive models into the dashboard to provide real-time insights and predictions.**
                """)
    
    st.markdown('-----------------------------------------------------------------------------------------------')


    col1, col2, col3=st.columns(3)
    with col1:
        st.subheader('Outlier detections')
        data={'Outliers':['Total number of outliers', 'Percentage of Outlier'], 'Values':[8633, 3.86]}
        st.dataframe(data)

        st.subheader('Model Evaluation')
        metrics={'Metrics':['R2 Score', 'Mean Absolute error', 'Mean Squared error', 'Root Mean Squared error'], 'Values':[0.9562712698389672, 0.050822770651348846, 0.0048399577587047524, 0.06956980493507764]}
        st.dataframe(metrics)

        st.subheader('Average number of Flats')
        st.markdown('**:blue[Singapore Average Number of Flats in each Street : 23]**')

    
    with col3:
        st.subheader('Features Sknewness and Kurtosis values')

        skewness=df3.apply(skew)
        kurtosis1=df3.apply(kurtosis)

        st.dataframe({
            'Skewness': skewness,
            'Kurtosis': kurtosis1
        })

    st.subheader('This is a RandomForest Regressor model that achieves 96% accuracy')    


def home():
    st.title('Singapore Resale Flat Prediction')
    
    col1, col2 = st.columns(2)
    with col1:
        st.image('https://skipsolabs-padang.s3.amazonaws.com/froala/uploadedContent/tenant/7/uploads/DD_HDB.png',use_column_width=True)
        
    with col2:
        st.subheader(':orange[Overview]')
        st.markdown('**The primary goal of this project is to develop a sophisticated machine learning model to predict the resale prices of flats in Singapore. The model will be integrated into a user-friendly web application, designed to assist potential buyers and sellers in estimating the resale value of flats. By leveraging historical transaction data, the application will provide accurate and actionable price predictions.**')
        st.markdown('**:blue[Domine:] Real Estate**')
        

    c1,c2,c3,c4=st.columns(4)     
    with c1:
        st.image('https://upload.wikimedia.org/wikipedia/commons/5/58/Bishan_HDB.JPG',use_column_width=True)
    with c2:
        st.image('https://upload.wikimedia.org/wikipedia/commons/thumb/7/77/JurongwestHDB.JPG/220px-JurongwestHDB.JPG',use_column_width=True)
    with c3:
        st.image('https://media2.malaymail.com/uploads/articles/2020/2020-07/20200725_Singapore-HDB.jpg', use_column_width=True)
    with c4:
        st.image('https://storage.googleapis.com/realtyplusmag-news-photo/news-photo/105760.Housing-and-Development-Board-(HDB).jpg',
         )# use_column_width=True)

    st.link_button(label='Official Website',url='https://www.hdb.gov.sg/cs/infoweb/homepage',use_container_width=True)

    st.subheader(':orange[Features and Goals ]') 
    st.markdown("""
                - **:green[Data Exploration] : Analyze the dataset for skewness and outliers.**
                - **:green[Data Transformation] : Clean and preprocess the data for modeling.**
                - **:green[Regression Modeling] : Predict the `Resale Flat Price` using machine learning models.**
                - **:green[Interactive Dashboard] : Use Streamlit for dynamic data exploration and predictions.**

                """)
    st.write('')
    st.markdown("**:orange[Technologies Used :] Pandas, Numpy, Scikit-learn, Seaborn, Matplotlib and Streamlit**")
    st.write('')
    st.markdown("**:blue[Github link - ] https://github.com/iAka5h**")




#Main Program
st.set_page_config(layout="wide")

user=option_menu(None, options= ['Home', 'Prediction', 'Statistics'], 
                 icons=["house", "graph-up", "book"], menu_icon="cast", orientation='horizontal',
                 styles={"container": {"padding": "5px","border": "2px ridge ", "background-color": "#002b36"},
                               "icon": {"color": "white", "font-size": "24px"},
                               "nav-link": {"font-size": "24px", "text-align": "center", "margin": "-2px"},
                               "nav-link-selected": {"background-color": "#247579"}}
                        )

if user=='Home':
    home()

elif user=='Prediction':
    prediction()

elif user=='Statistics':
    statistics()    
    
