from sklearn.preprocessing import MinMaxScaler
from sklearn.preprocessing import OneHotEncoder

import pandas as pd
import numpy as np

from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, GRU, Dropout, LSTM

import tensorflow.keras.losses as losses
from sklearn.utils import class_weight

import tensorflow as tf


def create_train_window(input, label, group_size=6):
    x_train = []
    y_train = []
    x_test = []
    y_test = []
    for i in range(0, len(input) - group_size):
        week_volume = label[i:group_size + i]
        max_week_volume = np.max(week_volume)
        noVolume_prob = np.random.choice([True, False], p=[0.6, 0.4])

        if max_week_volume > 0 or noVolume_prob:
            if (i < (len(input) - group_size - 1) * 0.8):
                x_train.append(input[i:group_size + i])
                y_train.append(label[i + group_size - 1])
            else:
                x_test.append(input[i:group_size + i])
                y_test.append(label[i + group_size - 1])
    return np.array(x_train), np.array(y_train), np.array(x_test), np.array(y_test)


def filter_dataset(path_input, inp_cols, label):
    df = pd.read_csv(path_input)
    keepCols = inp_cols + [label] + ["TimOcurrencia", "DesCPOcurrencia"]
    dropCols = list(set(df.columns).difference(set(keepCols)))
    df = df.drop(dropCols, axis=1)
    return df


def exec_model(path_output, inp_cols=[], label='',
               path_input='../../../OnlineData/CategoricalVolume_8cpFinal.csv'):
    df = filter_dataset(path_input, inp_cols, label)

    # Adding to input One hot encoded Month and CP

    CP_enc = OneHotEncoder(handle_unknown='ignore')
    CP_enc.fit(np.array(df.iloc[:, 1]).reshape(-1, 1))
    CP_OneHotEncoded = CP_enc.transform(np.array(df.iloc[:, 1]).reshape(-1, 1)).toarray()

    month_serie = list(map(lambda x: x.split('/')[0], np.array(df['TimOcurrencia'])))
    Month_enc = OneHotEncoder(handle_unknown='ignore')
    Month_enc.fit(np.array(month_serie).reshape(-1, 1))
    Month_OneHotEncoded = Month_enc.transform(np.array(month_serie).reshape(-1, 1)).toarray()

    cp_transformed_df = pd.DataFrame(data=CP_OneHotEncoded, columns=CP_enc.categories_)

    categories_month = np.array(list(map(lambda x: f'M-{x}', Month_enc.categories_[0])))
    month_transformed_df = pd.DataFrame(data=Month_OneHotEncoded, columns=categories_month)

    # One hot encoding label
    label_enc = OneHotEncoder(handle_unknown='ignore')
    label_enc.fit(np.array(df[label]).reshape(-1, 1))
    label_OneHotEncoded = label_enc.transform(np.array(df.iloc[:, 20]).reshape(-1, 1)).toarray()

    label_transformed_df = pd.DataFrame(data=label_OneHotEncoded, columns=label_enc.categories_)

    input = df.drop([label, "TimOcurrencia", "DesCPOcurrencia"], axis=1)
    label_transformed = np.array(label_transformed_df)

    input = cp_transformed_df.join(input)
    input = input.join(month_transformed_df)

    scaler_input = MinMaxScaler(feature_range=(0, 1))

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

    y_train_class = list(map(np.argmax, y_train))
    class_weights = class_weight.compute_class_weight('balanced', np.unique(y_train_class), y_train_class)
    class_weights = {id: class_weights[id] for id in range(0, len(y_train[0]))}

    # Callbacks

    # Parametres
    LR = 0.001
    FACTOR_LR = 0.5
    MIN_LR = LR / 100

    early_stopping = tf.keras.callbacks.EarlyStopping(
        monitor="val_loss",
        min_delta=0,
        patience=70,
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
        factor=FACTOR_LR,
        min_lr=MIN_LR,
    )

    GRU_SIZE, DENSE_SIZE, DROP_OUT = [128, 32, 0.1]
    RECURRENT_DROP, DROP_OUT_GRU = [0, 0.1]
    # Creación MODELO
    model = Sequential()
    model.add(GRU(GRU_SIZE, input_shape=input_shape_w, return_sequences=True, recurrent_dropout=RECURRENT_DROP,
                  dropout=DROP_OUT_GRU))
    model.add(GRU(GRU_SIZE, recurrent_dropout=RECURRENT_DROP, dropout=DROP_OUT_GRU))
    model.add(Dense(DENSE_SIZE, activation='relu'))
    model.add(Dropout(DROP_OUT))
    model.add(Dense(label_transformed_df.shape[1], activation='softmax'))
    model.compile(optimizer=tf.keras.optimizers.Adam(learning_rate=LR), loss='binary_crossentropy',
                  metrics=['accuracy'])
    model.summary()

    history = model.fit(x_train, y_train, epochs=10000000, shuffle=True, batch_size=8,
                        callbacks=[reduce_lr, early_stopping], validation_data=(x_test, y_test),
                        class_weight=class_weights, verbose=1)

    hist_df = pd.DataFrame(history.history)

    # save to json:
    with open(f'{path_output}/hist.json', mode='w') as f:
        hist_df.to_json(f)
    model.save(f'{path_output}/model')


if __name__ == '__main__':
    exec_model()