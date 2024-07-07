#######################################
"""Kural Tabanli Siniflandirma ile 
Potansiyel Müşteri Getirisi Hesaplama"""
#######################################
"""With Rule Based Classification 
Potential Customer Yield Calculation"""
#######################################
#Business Problem:
#Given below project, project tasks and data:
#https://github.com/abdullahalakbarli/Data_Science_Python_Project/blob/main/Gezinomi_Kural_Taban%C4%B1.pdf
#Data:
#https://github.com/abdullahalakbarli/Data_Science_Python_Project/blob/main/miuul_gezinomi.xlsx
#######################################
#Görev 1: Aşağıdaki Soruları Yanıtlayınız
#Soru1 : miuul_gezinomi.xlsx dosyasını okutunuz ve veri seti ile ilgili genel bilgileri gösteriniz.
import pandas as pd

file_path = r"C:\Users\Abdullah\Downloads\proje\miuul_gezinomi.xlsx"

df = pd.read_excel(file_path, sheet_name="Sheet1")

pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)

print(df.head())
print(df.shape)
print(df.info)

#Soru 2:Kaç unique şehir vardır? Frekansları nedir?
print(df['SaleCityName'].nunique())
print(df['SaleCityName'].value_counts())

#Soru 3:Kaç unique Concept vardır?
print(df['ConceptName'].nunique())

#Soru 4: Hangi Concept’den kaçar tane satış gerçekleşmiş?
print(df['ConceptName'].value_counts())

#Soru5: Şehirlere göre satışlardan toplam ne kadar kazanılmış?
print(df.groupby('SaleCityName').agg({'Price' : 'sum'}))

#Soru6: Concept türlerine göre göre ne kadar kazanılmış?
print(df.groupby('ConceptName').agg({'Price' : 'sum'}))

#Soru7: Şehirlere göre PRICE ortalamaları nedir?
print(df.groupby('SaleCityName').agg({'Price' : 'mean'}))

#Soru 8: Conceptlere göre PRICE ortalamaları nedir?
print(df.groupby('ConceptName').agg({'Price' : 'mean'}))

#Soru 9: Şehir-Concept kırılımında PRICE ortalamaları nedir?
city_concept_list = ['SaleCityName', 'ConceptName']
print(df.groupby(city_concept_list).agg({'Price' : 'mean'}))

###########################################################################
#Görev 2: SaleCheckInDayDiff değişkenini kategorik bir değişkene çeviriniz.
###########################################################################

df['EB_score'] = df['SaleCheckInDayDiff'].apply(lambda x: 'Early Bookers' if x > 90 
                                                          else ('Planners' 
                                                                if (x < 90) & (x >= 30) 
                                                                else ('Potential Planners' if (x < 30) & (x >= 7) 
                                                                      else 'Last Minuters')))

###########################################################################
#Görev 3: Şehir-Concept-EB Score, Şehir-Concept- Sezon, Şehir-Concept-CInDay kırılımında ortalama ödenen ücret ve yapılan işlem sayısı cinsinden inceleyiniz ?
###########################################################################
"""I have a different approach to this task. I want to solve the task programmatically.
So I want to remove the unnecessary columns in this problem. Then I can continue 
to write a program to solve this task using other columns"""

unnecessary_columns = ['SaleId', 'SaleDate', 'CheckInDate', 'SaleCheckInDayDiff']
df.drop(unnecessary_columns, axis = 1).head()

def finding_average_num(dataframe , col):
    print(dataframe.groupby(['SaleCityName', 'ConceptName',col]).agg({'Price' : ['mean', 'count']}))

necessary_columns = ['EB_score', 'CInDay', 'Seasons']
for col in necessary_columns:
    finding_average_num(df, col)

###########################################################################
#Görev 4: City-Concept-Season kırılımının çıktısını PRICE'a göre sıralayınız
###########################################################################
print(df.groupby(['SaleCityName', 'ConceptName', 'Seasons']).agg({'Price' : 'mean'}).sort_values('Price', ascending = False))

###########################################################################
#Görev 5: Indekste yer alan isimleri değişken ismine çeviriniz
###########################################################################
agg_df = df.groupby(['SaleCityName', 'ConceptName', 'Seasons']).agg({'Price' : 'mean'}).sort_values('Price', ascending = False)
agg_df.reset_index(inplace = True)

agg_df.head(20)

###########################################################################
#Görev 6: Yeni seviye tabanlı müşterileri (persona) tanımlayınız
###########################################################################

df['sales_level_based'] = df[['SaleCityName', 'ConceptName', 'Seasons']].agg(lambda x: '_'.join(x).upper(), axis = 1)

###########################################################################
#Görev 7: Yeni müşterileri (personaları) segmentlere ayırınız.
###########################################################################
agg_df ['SEGMENTS'] = pd.cut(agg_df['Price'], 4, labels = ["D", "C", "B", "A"])
agg_df.head(10)
agg_df.groupby('SEGMENTS').agg({'Price' : ['max', 'mean', 'sum']})


###########################################################################
#Görev 8: Yeni gelen müşterileri sınıflandırıp, ne kadar gelir getirebileceklerini tahmin ediniz
###########################################################################
antalya_herşeydahil_high_season = agg_df[(agg_df['SaleCityName'] == 'Antalya') &
                                           (agg_df['ConceptName'] == 'Herşey Dahil') &
                                           (agg_df['Seasons'] == 'High')]
print(antalya_herşeydahil_high_season['Price'].mean())

girne_yarımpansiyon_low_season = agg_df[(agg_df['SaleCityName'] == 'Girne') &
                                        (agg_df['ConceptName'] == 'Herşey Dahil') &
                                        (agg_df['Seasons'] == 'High')]

print(girne_yarımpansiyon_low_season)
print(girne_yarımpansiyon_low_season['Price'].mean)

#As a programmer, I prefer to write this problem in a programmatic code :)
def average_income_from_cust(DataFrame, col):
    return DataFrame.groupby(col, observed = False).agg({'Price' : 'mean'}).sort_values('Price', ascending = False)

columns = ['SaleCityName', 'ConceptName', 'Seasons']

print(average_income_from_cust(df, columns))
