# import libraries

import pandas as pd 
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor  
from sklearn.pipeline import Pipeline 
from sklearn.metrics import mean_squared_error

# read laptop csv file
df = pd.read_csv('D:\Harsha\DS\Harsha_S8318_LaptopPricePrediction\csv\laptop.csv', na_values=['?'])

# drop unnessery columns
df.drop(columns = ['Unnamed: 0.1',	'Unnamed: 0'], inplace = True)

# df.info() 
# print(df.isnull().sum())

# catgorical and numeric columns
cat_data = df.select_dtypes(include = 'object')
cat_columns = cat_data.columns
numeric_data = df.select_dtypes(exclude = 'object')
numeric_columns = numeric_data.columns
# cat_columns
# numeric_columns



# Missing value Imputation
si_cat = SimpleImputer(strategy= 'most_frequent')
si_num = SimpleImputer(strategy='median')
df[cat_columns] = si_cat.fit_transform(df[cat_columns])
df[numeric_columns] = si_num.fit_transform(df[numeric_columns])

# Handling outliers for Inches
q1 = df['Inches'].describe()['25%']
q3 = df['Inches'].describe()['75%']
IQR = q3 - q1 
lower_limit = q1 - 1.5*IQR
upper_limit = q3 + 1.5*IQR
df['Inches'] = df['Inches'].clip(lower_limit, upper_limit)

# Handling outliers for Price 
q1_p = df['Price'].describe()['25%']
q3_p = df['Price'].describe()['75%']
IQR_p = q3_p - q1_p
lower_limit_p = q1_p - 1.5 * IQR_p
upper_limit_p = q3_p + 1.5 * IQR_p
df['Price'] = df['Price'].clip(lower_limit_p, upper_limit_p)

# OneHotEncoding
preprocessing = ColumnTransformer(transformers=[
    ('nominal_Encoder', OneHotEncoder(handle_unknown='ignore'), cat_columns)  
], remainder='passthrough')


#Inches feature is not needed 
df.drop(columns='Inches', inplace=True)

# dependent and independent variables
X = df.drop(columns = 'Price')
y = df['Price']

# splitting data - 80% for training and 20% for testing 
x_train, x_test, y_train, y_test = train_test_split(X, y, test_size = 0.2, random_state=42) 



# creating pipeline
model = Pipeline(steps = [
    ('preprocesor', preprocessing),
    ('Regrosser', RandomForestRegressor())
])

# model training 
model.fit(x_train, y_train)

# model teting
ypred_RFT = model.predict(x_test)

# checking RMSE value
mse_RFT = mean_squared_error(y_test, ypred_RFT)
# print(mse_RFT ** 0.5)

# function to predict laptop price
def laptop_price_pred(Company, TypeName, ScreenResolution, Cpu, Ram, Memory, Gpu, OpSys, Weight):
  inputs = pd.DataFrame([[Company, TypeName, ScreenResolution, Cpu, Ram, Memory, Gpu, OpSys, Weight]], columns = ['Company', 'TypeName', 'ScreenResolution', 'Cpu', 'Ram', 'Memory', 'Gpu', 'OpSys', 'Weight'])
  return model.predict(inputs)[0]


# res = laptop_price_pred('Apple',	'Ultrabook',	13.3, 'IPS Panel Retina Display 2560x1600',	'Intel Core i5 2.3GHz',	'8GB',	'128GB SSD',	'Intel Iris Plus Graphics 640',	'macOS',	'1.37kg')
# print(res)

# function to get all unique row from all the columns 
col_unq_data = {}
def unique_data():
    for i in X.columns:
        col_unq_data[i] = list(df[i].unique())
    
    return col_unq_data
