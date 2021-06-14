#%%

from sklearn.preprocessing import MinMaxScaler
from sklearn.preprocessing import OneHotEncoder

import pandas as pd
import numpy as np

from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, GRU, Dropout, LSTM

import tensorflow.keras.losses as losses

import matplotlib.pyplot as plt
import tensorflow as tf
import tensorflow_docs.plots as plotting
from functools import reduce

import tensorflow_docs.plots as plotting





def create_train_window(input, label, group_size=6):
  x_train = []
  y_train = []
  x_test = []
  y_test = []
  for i in range(0, len(input)-group_size):
    if(i < (len(input)-group_size-1)*0.8):
      x_train.append(input[i:group_size+i])
      y_train.append(label[i+group_size-1])
    else:
      x_test.append(input[i:group_size+i])
      y_test.append(label[i+group_size-1])
  return np.array(x_train), np.array(y_train), np.array(x_test), np.array(y_test)



df = pd.read_csv('../../OnlineData/CategoricalVolume.csv')


# Adding to input One hot encoded Month and CP

CP_enc = OneHotEncoder(handle_unknown='ignore')
CP_enc.fit(np.array(df.iloc[:, 1]).reshape(-1, 1))
CP_OneHotEncoded = CP_enc.transform(np.array(df.iloc[:, 1]).reshape(-1, 1)).toarray()

month_serie = list(map(lambda x: x.split('-')[1], np.array(df.iloc[:, 0])))
Month_enc = OneHotEncoder(handle_unknown='ignore')
Month_enc.fit(np.array(month_serie).reshape(-1, 1))
Month_OneHotEncoded = Month_enc.transform(np.array(month_serie).reshape(-1, 1)).toarray()

cp_transformed_df = pd.DataFrame(data=CP_OneHotEncoded, columns=CP_enc.categories_)

categories_month = np.array(list(map(lambda x: f'M-{x}', Month_enc.categories_[0])))
month_transformed_df = pd.DataFrame(data=Month_OneHotEncoded, columns=categories_month)

#%%

# One hot encoding label
label_enc = OneHotEncoder(handle_unknown='ignore')
label_enc.fit(np.array(df.iloc[:, 20]).reshape(-1, 1))
label_OneHotEncoded = label_enc.transform(np.array(df.iloc[:, 20]).reshape(-1, 1)).toarray()

label_transformed_df =  pd.DataFrame(data=label_OneHotEncoded, columns=label_enc.categories_)



input = df.iloc[:, 2:20]
label_transformed = np.array(label_transformed_df)

input = cp_transformed_df.join(input)
input = input.join(month_transformed_df)

#%%

scaler_input = MinMaxScaler(feature_range=(0,1))

input_transformed = scaler_input.fit_transform(input)

df_transformed = pd.DataFrame(input_transformed)


group_size = 6

x_train = []
y_train = []
x_test = []
y_test = []
num_cps_unique = len(CP_OneHotEncoded[0])

for cp in range(0, num_cps_unique):
    input_t = np.array([])
    label_t = np.array([])
    for ind in range(0, len(input_transformed)):
        if input_transformed[ind][cp] == 1:
            input_t = np.append(input_t, input_transformed[ind])
            label_t = np.append(label_t, label_transformed[ind])
    input_t = input_t.reshape((-1, len(input_transformed[0])))
    label_t = label_t.reshape((-1, len(label_transformed[0])))

    x_train_t, y_train_t, x_test_t, y_test_t = create_train_window(input_t, label_t, group_size=group_size)

    x_train = np.append(x_train, x_train_t)
    y_train = np.append(y_train, y_train_t)
    x_test = np.append(x_test, x_test_t)
    y_test = np.append(y_test, y_test_t)

x_train = x_train.reshape(-1, group_size, len(input_transformed[0]))
y_train = y_train.reshape(-1, len(label_transformed[0]))
x_test = x_test.reshape(-1, group_size, len(input_transformed[0]))
y_test = y_test.reshape(-1, len(label_transformed[0]))

input_shape_w = np.shape(x_train[0])


# MODEL

calc_class_weight = lambda x: (1./x) * (3285 / 5.)
class_weight = {
    0: calc_class_weight(3065),
    1: calc_class_weight(127),
    2: calc_class_weight(58),
    3: calc_class_weight(23),
    4: calc_class_weight(12),
}

#%%
# Parametres
LR = 0.001
FACTOR_LR = LR / 5
MIN_LR = LR / 20


# Callbacks

early_stopping = tf.keras.callbacks.EarlyStopping(
    monitor="loss",
    min_delta=0,
    patience=50,
    verbose=0,
    mode="auto",
    baseline=None,
    restore_best_weights=False,
)

checkpoint = tf.keras.callbacks.ModelCheckpoint(
    'model',
    monitor="val_loss",
    verbose=0,
    save_best_only=True,
    save_weights_only=False,
    mode="auto",
    save_freq="epoch",
    options=None
)

reduce_lr = tf.keras.callbacks.ReduceLROnPlateau(
    monitor="loss",
    factor=FACTOR_LR,
    patience=10,
    verbose=0,
    mode="auto",
    min_delta=MIN_LR,
    cooldown=0,
    min_lr=0
)

# %%
GRU_SIZE = 128
DENSE_SIZE = 64
DROP_OUT = 0.2
res_exp = 4
experimentation_list = [[np.floor(gru), np.floor(dense), drop]
                                  for gru in np.linspace(32, 256, res_exp)
                                  for dense in np.linspace(16, 128, res_exp)
                                  for drop in np.linspace(0.1, 0.3, res_exp) if gru > dense ]
path_output = 'Experimentation'
for ID, arr in enumerate(experimentation_list):
    GRU_SIZE, DENSE_SIZE, DROP_OUT = arr
    # Creación MODELO
    model = Sequential()
    model.add(GRU(GRU_SIZE, input_shape=input_shape_w, return_sequences=False, dropout=DROP_OUT, recurrent_dropout=0.5))
    model.add(Dense(DENSE_SIZE, activation='relu'))
    model.add(Dropout(DROP_OUT))
    model.add(Dense(label_transformed_df.shape[1], activation='softmax'))
    model.compile(optimizer=tf.keras.optimizers.Adam(lr=LR), loss=losses.CategoricalCrossentropy(), metrics=['accuracy'])
    model.summary()



    history = model.fit(x_train, y_train, epochs=10000000 ,shuffle=True, batch_size=8,
                        callbacks=[early_stopping, reduce_lr], validation_data=(x_test, y_test),
                        class_weight=class_weight)

    hist_df = pd.DataFrame(history.history)

    # save to json:
    hist_json_file = 'history.json'
    with open(f'{path_output}/{ID}-hist', mode='w') as f:
        hist_df.to_json(f)
    model.save(f'{path_output}/{ID}-model')