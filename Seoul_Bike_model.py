
from tensorflow.keras import Input, Sequential
from tensorflow.keras.layers import Dense, Dropout
import os
import pickle
import numpy as np
import tensorflow as tf
file_path = os.getcwd()+"\\utils"
model=None
scaler=None

def create_model():
    global model
    file_str = file_path+"\\seoul_bike_model.weights.h5"

    model = Sequential()
    model.add(Input((15,)))  # 들어올 문제파일의 모양, 갯수는 의미 없음
    model.add(Dense(256, activation="relu"))  # 256*15개의 파라미터를 갖는다.
    model.add(Dropout(0.4))  # 0.4=40%
    # model.add(Dense(128,activation="relu"))#128*15개의 파라미터를 갖는다.
    model.add(Dense(32, activation="relu"))  # 32*15개의 파라미터를 갖는다.
    model.add(Dropout(0.4))
    # model.add(Dense(32,activation="relu"))
    model.add(Dense(8, activation="relu"))  # 8*15개의 파라미터를 갖는다.
    model.add(Dropout(0.4))
    # Dense와 Dropout를 줄여서 간격을 줄여나감
    model.add(Dense(1))
    model.load_weights(file_str)
    model.compile(loss="mse", optimizer="adam", metrics=["mae"])

def create_prescaler():
    global scaler
    file_str = file_path+"\\prenormal.pre"
    print(os.path.exists(file_str))

    with open(file_str, 'rb') as fp:
        scaler = pickle.load(fp);

def preprocessor_data(t_data,t_sub):#호출1. t_data 스케일링 가능 데이터 t_sub 원핫인코딩 데이터
    if not scaler:
        create_prescaler()
    t_data = np.array([t_data])
    t_sub = np.array(t_sub)
    t_data=scaler.transform(t_data)
    print("스케일링된데이터:",t_data)
    oh_seas = [0, 0, 0, 0]
    oh_holis = [0, 0]
    seas = ['Autumn', 'Spring', 'Summer', 'Winter']
    holis = ['Holiday', 'No Holiday']
    seas_ix = seas.index(t_sub[0])
    oh_seas[seas_ix] = 1
    holis_ix = holis.index(t_sub[1])
    oh_holis[holis_ix] = 1
    t_sub= [oh_seas, oh_holis]
    print("원핫인코딩 데이터: ",t_sub)
    return np.concatenate([t_data, np.array([t_sub[0]]), np.array([t_sub[1]])], axis=1)
#호출 예제 predict_data(preprocessor_data(user_data,user_sub))
def predict_data(x_data): #호출2. 모델 인출과 예측 리턴
    global model
    if not model:
        create_model()
    return model.predict(x_data)
def common_fun(user_data,user_sub):
    pre_data = preprocessor_data(user_data,user_sub)
    y_pred=predict_data(pre_data)
    return y_pred[0][0]

if "__main__" == __name__:
    # print(create_model())
    # Hour 시간대0  Temperature 온도1 Humidity 습도2  Wind speed 풍속 3
    # Visibility 가시거리 4 Dew point tmeperature 안개 5 Solar Radiation 일사량 6
    # Rainfall 강수량 7 Snowfall (cm) 적설량8
    # Seasons 계절 11, # Holiday 휴일 여부
    user_data=[8,12,40,2.5,1500,-10,0.8,0,0]
    user_sub=["Winter","No Holiday"]
    pre_data=preprocessor_data(user_data,user_sub)
    print(pre_data.shape)
    print(pre_data)
    y_pred=predict_data(pre_data)
    print(y_pred[0][0])