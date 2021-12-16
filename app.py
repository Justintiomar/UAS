import pandas as pd
import streamlit as st
import plotly.express as px

st.set_page_config(page_title='Grafik produksi minyak mentah')
st.title('Grafik Produksi Minyak Mentah')

csv_file = 'produksi_minyak_mentah.csv'
json_file = 'kode_negara_lengkap.json'

#open json file
df_json_ori = pd.read_json(json_file)
df_json_ori.dropna(inplace = True)

#open csv file
df_csv_ori = pd.read_csv(csv_file,usecols=['kode_negara','tahun','produksi'])

#cleaning data
df1 = df_json_ori.rename({'alpha-3':'country_code','sub-region': 'sub_region'},axis='columns')
df2 = df1.country_code.isin(df_csv_ori['kode_negara'])
df_json = df1[df2]
df3 = df_csv_ori.kode_negara.isin(df_json['country_code'])
df_csv = df_csv_ori[df3]

#Grafik negara terhadap tahun
st.header('Grafik Produksi Minyak Mentah Terhadap Waktu')
country_list = df_json['name'].unique().tolist()
year = df_csv['tahun'].unique().tolist()
option = st.selectbox('Negara: ', country_list)
country_name = df_json.loc[df_json['name']== option,'country_code'].iloc[0]
option_filter = df_csv.kode_negara.isin([country_name])
filetered_country = df_csv[option_filter]
fixed_column_name = filetered_country.rename({'tahun':'Tahun','produksi':'Produksi'},axis = 'columns')

bar_chart = px.bar(fixed_column_name, 
                     x='Tahun',
                     y='Produksi',                     
                     text ='Produksi',
                     color_discrete_sequence = ['#000957'],
                     template= 'plotly_white' )
st.plotly_chart(bar_chart)

#Grafik B-besar negara dengan jumlah produksi terbesar pada tahun T
st.header('Negara dengan Jumlah Produksi Terbesar pada Tahun T')
T = st.slider("T: ",min(year), max(year))
B = st.slider("B: ",1,137)
filter_year = df_csv.tahun.isin([T])
sorted_list = df_csv[filter_year].sort_values(by=['produksi'],ascending=False)
display = sorted_list.iloc[0:B]

produksi2 = list(display['produksi'])
kode_negara2 = list(display['kode_negara'])
negara2 = []
for item in kode_negara2:
    neg2 = df_json[df_json['country_code']==item]['name'].iloc[0]
    negara2.append(neg2)
list_of_tuples = list(zip(negara2,produksi2))
df_2 = pd.DataFrame(list_of_tuples,columns = ['Negara','Produksi'])

bar_chart2 = px.bar(df_2, 
                     x='Negara',
                     y='Produksi',                     
                     text ='Produksi',
                     color_discrete_sequence = ['#F63366'],
                     template= 'plotly_white' )
st.plotly_chart(bar_chart2)

#Grafik B-besar negara dengan jumlah produksi terbesar secara kumulatif
st.header('Negara dengan Jumlah Produksi Minyak Terbesar Secara Kumulatif')
Number = st.slider("B:  ",1,137)
kode_negara_unik = list(df_csv['kode_negara'].unique())
total_produksi = []
list1 = []

for kode_negara in kode_negara_unik:
    jumlah_produksi = df_csv[df_csv['kode_negara']==kode_negara]['produksi']
    total_produksi.append(jumlah_produksi.sum())
    list1.append([jumlah_produksi.sum(),kode_negara])
total_produksi.sort(reverse=True)
list_kode_negara = []
produksi=[]
for i in range(Number):
    produksi.append(total_produksi[i])
    for j in range(len(list1)):
        if(list1[j][0]==total_produksi[i]):
            list_kode_negara.append(list1[j][1])
negara = []
for item in list_kode_negara:
    nama_negara = df_json[df_json['country_code']==item]['name'].iloc[0]
    negara.append(nama_negara)

list_of_tuples = list(zip(negara,produksi))
df = pd.DataFrame(list_of_tuples,columns = ['Negara','Total produksi'])

bar_chart3 = px.bar(df, 
                     x='Negara',
                     y='Total produksi',                     
                     text ='Total produksi',
                     color_discrete_sequence = ['#22577A'],
                     template= 'plotly_white' )
st.plotly_chart(bar_chart3)

#Summary
st.header("Informasi Negara")
get_year = st.slider("Tahun:  ",min(year),max(year))
filter_year4 = df_csv.tahun.isin([get_year])
col1, col2= st.columns(2)
with col1 :
    #negara dengan jumlah produksi trebesar pada tahun T
    sorted_list4 = df_csv[filter_year4].sort_values(by=['produksi'],ascending=False)

    produksi4 = list(sorted_list4['produksi'])
    kode_negara4 = list(sorted_list4['kode_negara'])
    produksi_terbesar  =  produksi4[0]
    kode_negara41 = kode_negara4[0] 

    st.subheader("Negara dengan Jumlah Produksi Terbesar pada Tahun T")
    nama_negara = df_json[df_json['country_code']==kode_negara41]['name'].iloc[0]
    st.write("Nama Lengkap Negara   : ", nama_negara)
    st.write("Kode Negara           : ", kode_negara41)
    region41 = df_json[df_json['country_code']==kode_negara41]['region'].iloc[0]
    st.write("Region                : ", region41)
    sub_region41 = df_json[df_json['country_code']==kode_negara41]['sub_region'].iloc[0]
    st.write("Sub-region            : ", sub_region41)
    st.write("Jumlah produksi       : ", produksi_terbesar)

    #negara dengan jumlah produksi terbesar keseluruhan tahun
    st.subheader("Negara dengan Produksi Terbesar pada Keseluruhan Tahun")
    sorted_list = df_csv.sort_values(by=['produksi'],ascending=False)
    to_dataframe = pd.DataFrame(sorted_list)
    list_kode_negara = list(to_dataframe['kode_negara'])
    list_tahun = list(to_dataframe['tahun'])
    list_produksi = list(to_dataframe['produksi'])
    produksi_terbesar = list_produksi[0]
    kode_negara42 = list_kode_negara[0]
    tahun42 = list_tahun[0]
    nama_negara = df_json[df_json['country_code']==kode_negara42]['name'].iloc[0]
    st.write("Nama Lengkap Negara   : ", nama_negara)
    st.write("Kode Negara           : ", kode_negara42)
    region41 = df_json[df_json['country_code']==kode_negara42]['region'].iloc[0]
    st.write("Region                : ", region41)
    sub_region42 = df_json[df_json['country_code']==kode_negara42]['sub_region'].iloc[0]
    st.write("Sub-region            : ", sub_region42)
    st.write("Jumlah produksi       : ", produksi_terbesar)

with col2 :
    #negara dengan jumlah produksi terkecil pada tahun T (!= 0)
    sorted_list5 = df_csv[filter_year4].sort_values(by=['produksi'],ascending=True)

    produksi5 = list(sorted_list5['produksi'])
    kode_negara5 = list(sorted_list5['kode_negara'])
    for item in produksi5:
        if (item>0) :
            produksi_terkecil = item
            break
    kode_negara51 = df_csv[df_csv['produksi']==produksi_terkecil]['kode_negara'].iloc[0]

    st.subheader("Negara dengan Jumlah Produksi Terkecil pada Tahun T")
    nama_negara = df_json[df_json['country_code']==kode_negara51]['name'].iloc[0]
    st.write("Nama Lengkap Negara   : ", nama_negara)
    st.write("Kode Negara           : ", kode_negara51)
    region51 = df_json[df_json['country_code']==kode_negara51]['region'].iloc[0]
    st.write("Region                : ", region51)
    sub_region51 = df_json[df_json['country_code']==kode_negara51]['sub_region'].iloc[0]
    st.write("Sub-region            : ", sub_region51)
    st.write("Jumlah produksi       : ", produksi_terkecil)

    #negara dengan jumlah produksi terkecil keseluruhan tahun (!= 0)
    st.subheader("Negara dengan Produksi Terkecil pada Keseluruhan Tahun")
    sorted_list = df_csv.sort_values(by=['produksi'],ascending=True)
    to_dataframe = pd.DataFrame(sorted_list)

    list_kode_negara = list(to_dataframe['kode_negara'])
    list_tahun = list(to_dataframe['tahun'])
    list_produksi = list(to_dataframe['produksi'])
    total_produksi.sort(reverse=False)
    for i in range (len(sorted_list)):
        if(list_produksi[i]>0):
            total_produksi_terkecil = list_produksi[i]
            kode_negara52 = list_kode_negara[i]
            break

    for j in range(len(list1)):
            if(list1[j][0]==total_produksi_terkecil):
                kode_negara52 = list1[j][1]

    nama_negara = df_json[df_json['country_code']==kode_negara52]['name'].iloc[0]
    st.write("Nama Lengkap Negara   : ", nama_negara)
    st.write("Kode Negara           : ", kode_negara52)
    region52 = df_json[df_json['country_code']==kode_negara52]['region'].iloc[0]
    st.write("Region                : ", region52)
    sub_region52 = df_json[df_json['country_code']==kode_negara52]['sub_region'].iloc[0]
    st.write("Sub-region            : ", sub_region52)
    st.write("Jumlah produksi        : ", total_produksi_terkecil)

col3,col4 = st.columns(2)
with col3: 
    #negara dengan jumlah produksi 0 pada tahun T
    st.subheader("Negara dengan Jumlah Produksi 0 pada Tahun T")
    B = st.slider("Banyak negara yang ingin ditampilkan: ",1,20)
    to_dataframe = pd.DataFrame(sorted_list4)
    filter_0 =to_dataframe.produksi.isin([0])
    filtered_produksi =to_dataframe[filter_0]
    kode_negara_0 = list(filtered_produksi['kode_negara'])

    for i in range(B): 
        st.write("Negara ", i+1) 
        nama_negara = df_json[df_json['country_code']==kode_negara_0[i]]['name'].iloc[0]
        st.write("Nama Lengkap Negara   : ", nama_negara)
        st.write("Kode Negara           : ", kode_negara_0[i])
        region0 = df_json[df_json['country_code']==kode_negara_0[i]]['region'].iloc[0]
        st.write("Region                : ", region0)
        sub_region0 = df_json[df_json['country_code']==kode_negara_0[i]]['sub_region'].iloc[0]
        st.write("Sub-region            : ", sub_region0)
        st.write()
with col4:
    #negara dengan jumlah produksi 0 pada keseluruhan tahun
    st.subheader("Negara dengan Jumlah Produksi 0 pada Keseluruhan Tahun")
    B = st.slider("Banyak negara yang ingin ditampilkan: ",1,41)
    list_0 = []
    for i in range(len(list1)):
        if(list1[i][0]==0):
            list_0.append(list1[i][1])

    for i in range(B): 
        st.write("Negara ", i+1) 
        nama_negara = df_json[df_json['country_code']==list_0[i]]['name'].iloc[0]
        st.write("Nama Lengkap Negara   : ", nama_negara)
        st.write("Kode Negara           : ", list_0[i])
        region0 = df_json[df_json['country_code']==list_0[i]]['region'].iloc[0]
        st.write("Region                : ", region0)
        sub_region0 = df_json[df_json['country_code']==list_0[i]]['sub_region'].iloc[0]
        st.write("Sub-region            : ", sub_region0)
        st.write()
