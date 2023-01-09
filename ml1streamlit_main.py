# import library
import streamlit as st
import pandas as pd
import numpy as np
import pickle #untuk menyimpan atau membaca data .pkl
import base64 #untuk membuka file .gif di streamlit

# @st.cache adalah meningkatkan performa web
@st.cache(suppress_st_warning = True)
def get_fvalue(val) :
    feature_dict = {"No":1, "Yes":2}
    for key, value in feature_dict.items() :
        if val == key :
            return value
        
def get_value(val, my_dict) :
    for key, value in my_dict.items() :
        if val == key :
            return value

# sidebar
#st.sidebar.header('MENU')
app_mode = st.sidebar.selectbox('MENU', ['Home', 'Prediksi']) #2Halaman

# sidebar pemilihan halaman
if app_mode == 'Home' :
    st.title('Aplikasi Prediksi Peminjaman')
    st.image('assets/loan_image.jpg')
    st.write('\n')
    st.write('\n')
    st.markdown('Dataset :')
    #st.header('Dataset :')
    
    data = pd.read_csv('loan_dataset.csv')
    st.write(data.head())
    
#     s1 = dict(selector='th', props=[('text-align', 'center')])
#     s2 = dict(selector='td', props=[('text-align', 'center')])
#     # you can include more styling paramteres, check the pandas docs
#     table = data.style.set_table_styles([s1,s2]).hide(axis=0).to_html()     
#     st.write(f'{table}', unsafe_allow_html=True)
    
    st.write('\n')
    st.write('\n')
    st.markdown('Pendapatan Pemohon Hutang (Applicant Income) vs Jumlah Pinjaman (Loan Amount)')
    #st.header('Pendapatan Pemohon Hutang vs Jumlah Pinjaman :')
    st.bar_chart(data[['ApplicantIncome','LoanAmount']].head(20))
    
elif app_mode == 'Prediksi' :
    st.image('assets/slider-short-3.jpg')
    st.subheader('Kamu perlu mengisi semua informasi yang diperlukan untuk mendapatkan balasan atas permintaan pinjaman Anda!')
    st.sidebar.subheader('')
    st.sidebar.subheader('Informasi Client :')
    
    gender_dict = {'Male':1, 'Female':2}
    feature_dict = {"No":1, "Yes":2}
    edu = {'Graduate':1, 'Not Graduate':2}
    prop = {'Rural':1, 'Urban':2, 'Semiurban':3}
    
    ApplicantIncome = st.sidebar.slider('ApplicantIncome', 0, 10000, 0)
    CoapplicantIncome = st.sidebar.slider('CoapplicantIncome', 0, 10000, 0) #pendapatan rekan calonpeminjam
    LoanAmount = st.sidebar.slider('LoanAmount in K$', 9.0, 700.0, 200.0)
    
    Loan_Amount_Term = st.sidebar.selectbox('Loan_Amount_Term', (12.0, 36.0, 60.0, 84.0, 120.0, 180.0, 240.0, 300.0, 360.0))
    
    st.write('<style>div.row-widget.stRadio > div{flex-direction:row;}</style>', unsafe_allow_html=True) #makehorizontalradio
    Credit_History = st.sidebar.radio('Credit_History', (0.0, 1.0))
    Gender = st.sidebar.radio('Gender', tuple(gender_dict.keys()))
    Married = st.sidebar.radio('Married', tuple(feature_dict.keys()))
    Self_Employed = st.sidebar.radio('Self Employed', tuple(feature_dict.keys())) #bisnis / usaha pribadi (wirausaha)
    Dependents = st.sidebar.radio('Dependents', options = ['0', '1', '2', '3+'])
    Education = st.sidebar.radio('Education', tuple(edu.keys()))
    Property_Area = st.sidebar.radio('Property_Area', tuple(prop.keys()))
    
    #one-hot encoding dependents
    class_0, class_3, class_1, class_2 = 0, 0, 0, 0
    if Dependents == '0' :
        class_0 = 1
    elif Dependents == '1' :
        class_1 = 1
    elif Dependents == '2' :
        class_2 = 1
    else :
        class_3 = 1
    
    #one-hot encoding property area
    Rural, Urban, Semiurban = 0, 0, 0
    if Property_Area == 'Urban' :
        Urban = 1
    elif Property_Area == 'Semiurban' :
        Semiurban = 1
    else :
        Rural = 1
    
    #mengumpulkan dan menyimpan data
    data1 = {
        'Gender' : Gender,
        'Married' : Married,
        'Dependents' : [class_0, class_1, class_2, class_3],
        'Education' : Education,
        'ApplicantIncome' : ApplicantIncome,
        'CoapplicantIncome' : CoapplicantIncome,
        'Self Employed' : Self_Employed,
        'LoanAmount' : LoanAmount,
        'Loan_Amount_Term' : Loan_Amount_Term,
        'Credit_History' : Credit_History,
        'Property_Area' : [Rural, Urban, Semiurban],
    }
    
    #inputan
    feature_list = [ApplicantIncome, CoapplicantIncome, LoanAmount, Loan_Amount_Term, Credit_History, 
                    get_value(Gender, gender_dict), get_fvalue(Married), 
                    data1['Dependents'][0], data1['Dependents'][1], data1['Dependents'][2], data1['Dependents'][3],
                    get_value(Education, edu), get_fvalue(Self_Employed), 
                    data1['Property_Area'][0], data1['Property_Area'][1], data1['Property_Area'][2]]
    
    #mengubah menjadi tipe data array
    single_sample = np.array(feature_list).reshape(1, -1)
    
    #memuat model Random Forest Classifier pada loaded_model, prediksinya 0 atau 1 dalam prediksi (dalam menentukan gagal atau sukses)
    if st.button('Klik untuk Prediksi') :
        file_ = open("assets/6m-rain.gif", "rb")
        contents = file_.read()
        data_url = base64.b64encode(contents).decode("utf-8")
        file_.close()
        
        file = open('assets/green-cola-no.gif', 'rb')
        contents = file.read()
        data_url_no = base64.b64encode(contents).decode('utf-8')
        file.close()
        
        loaded_model = pickle.load(open('Random_Forest.sav', 'rb'))
        prediction = loaded_model.predict(single_sample)
        if prediction[0] == 0 :
            st.error('Berdasarkan pada perhitungan kami, Anda tidak dapat melakukan pinjaman melalui Bank')
            st.markdown(f' <img src="data:image/gif;base64,{data_url_no}" alt="cat gif">', unsafe_allow_html = True)
        elif prediction[0] == 1 :
            st.success('Selamat, Anda dapat melakukan peminjaman melalui Bank')
            st.markdown(f'<img src="data:image/gif;base64,{data_url}" alt="cat gif">', unsafe_allow_html = True)
    
    st.sidebar.write('')
    st.sidebar.write('')
    st.sidebar.write('')
    st.sidebar.write('')
    st.sidebar.write('')
    st.sidebar.write('')
    
    
#menghilangkan burger dan made with streamlit
hide_streamlit_style = """
 <style>
  #MainMenu {visibility: hidden;}
  footer {visibility: hidden;}
 </style>
"""
st.markdown(hide_streamlit_style, unsafe_allow_html=True)