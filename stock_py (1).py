
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import yfinance as yf

#import yfinance as yf
ticker='SBIN.NS'
start='2010-01-01'
end='2022-12-31'

df = yf.download(ticker,start,end)
df.columns = df.columns.droplevel(1)
df.reset_index(inplace=True)

df.head()

plt.plot(df.Close)
plt.legend(['Close'])

ma100=df.Close.rolling(100).mean()
ma100

plt.figure(figsize=(12,6))
plt.plot(df.Close)
plt.plot(ma100,'r')
plt.legend(['Close','MovingAvg100'])

ma200=df.Close.rolling(200).mean()
ma200

plt.figure(figsize=(12,6))
plt.plot(df.Close)
plt.plot(ma100,'r')
plt.plot(ma200,'g')
plt.legend(['Close Price','MovingAvg100','MovingAvg200'])

df.shape

#Spliting Data into Training And Testing

data_training=pd.DataFrame(df['Close'][0:int(len(df)*0.70)]) #70% data for training
data_testing=pd.DataFrame(df['Close'][int(len(df)*0.70):int(len(df))]) #30% data for testing

print(data_training.shape)
print(data_testing.shape)

data_training.head()

data_testing.head()

#scale down train data using minmax_scaler
from sklearn.preprocessing import MinMaxScaler
scaler=MinMaxScaler(feature_range=(0,1))

data_training_array=scaler.fit_transform(data_training)
data_training_array

x_train=[] #price array
y_train=[] #predicting price

for i in range(100,data_training_array.shape[0]):
  x_train.append(data_training_array[i-100: i])
  y_train.append(data_training_array[i,0])

x_train,y_train=np.array(x_train),np.array(y_train)

#ML Model
from keras.layers import Dense,Dropout,LSTM
from keras.models import Sequential

model=Sequential()
model.add(LSTM(units=50, activation='relu', return_sequences=True,
               input_shape=(x_train.shape[1],1)))
model.add(Dropout(0.2))


model.add(LSTM(units=60,activation='relu', return_sequences=True))
model.add(Dropout(0.3))

model.add(LSTM(units=80,activation='relu', return_sequences=True))
model.add(Dropout(0.4))

model.add(LSTM(units=120,activation='relu'))
model.add(Dropout(0.5))


model.add(Dense(units=1))

model.summary()

model.compile(optimizer = 'adam',loss = 'mean_squared_error')
model.fit(x_train, y_train, epochs = 50)

model.save('keras_model.h5')
#/*from google.colab import files
#files.download('keras_model.h5')*/

data_testing.head()

past_100_days=data_training.tail(100)

final_df=pd.concat([past_100_days, data_testing], ignore_index=True)

final_df.head()

input_data = scaler.fit_transform(final_df)
input_data

input_data.shape

x_test=[]
y_test=[]

for i in range(100,input_data.shape[0]):
  x_test.append(input_data[i-100:i])
  y_test.append(input_data[i,0])

x_test,y_test=np.array(x_test),np.array(y_test)
print(x_test.shape)
print(y_test.shape)

#model preciction
y_predicted=model.predict(x_test)

y_predicted.shape

y_test

y_predicted

scaler.scale_

#scaling back the value to it's original form
scale_factor=1/0.00714127
y_predicted=y_predicted * scale_factor
y_test=y_test* scale_factor

plt.figure(figsize=(12,6))
plt.plot(y_test,'b',label='Original Price')
plt.plot(y_predicted,'r',label='Predicted Price')
plt.xlabel('Time')
plt.ylabel('Price')
plt.legend()
plt.show()
