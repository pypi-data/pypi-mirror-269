import os
import numpy as np
import re
from sklearn.model_selection import KFold
from sklearn.preprocessing import StandardScaler
import librosa
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout
from tensorflow.keras.optimizers import Adam
from sklearn.metrics import classification_report, accuracy_score, f1_score  # Add this line
import argparse

from tensorflow.keras.layers import Dense, Dropout, BatchNormalization, Add, Input
from tensorflow.keras.models import Model
from tensorflow.keras.regularizers import l2

#label = int(re.search(r'\d+(?=\.\w+$)', filename).group()) # ESC
  
  #mfccs = librosa.feature.mfcc(y=audio, sr=sr, n_mfcc=13)
  #feature = np.mean(mfccs, axis=1)


def load_data(data_path):
    X = []
    y = []

    folders = os.listdir(data_path)

    for folder in folders:
        folder_path = os.path.join(data_path, folder)
        if os.path.isdir(folder_path):
            for filename in os.listdir(folder_path):
                if filename.endswith('.wav') or filename.endswith('.mp3'):
                    file_path = os.path.join(folder_path, filename)
                    audio, sr = librosa.load(file_path, sr=44100)

                    
                    
                    
                    label = int(filename.split('-')[-1].split('.')[0]) #ESC
                    
                    
                    #label = int(filename.split('_')[-1].split('.')[0]) #MUSIC
                    
                    
                    #label= int(filename.split('-')[-5])-1 #RAVDESS
                    

                    spectrogram = np.abs(librosa.stft(audio, n_fft=2048))
                    feature = np.mean(spectrogram, axis=1)


                    X.append(feature)
                    y.append(label)
                    
                    
                    

    X = np.array(X)
    y = np.array(y)
    print('xxxxx',len(X))
    print('yyyyyy',len(y))
    
    
        # Print the number of unique labels
    num_unique_labels = len(np.unique(y))
    print('Number of Unique Labels:', num_unique_labels)

    return X, y

def build_model(input_dim, num_classes, learning_rate, weight_decay):
    # Define the model architecture and include regularization terms using l2 weight decay.
    inp = Input(shape=input_dim)

    initializer = 'glorot_normal'

    y = Dense(512, activation='relu', kernel_initializer=initializer, kernel_regularizer=l2(weight_decay))(inp)
    y = Dropout(0.4)(y)
    y = BatchNormalization()(y)

    y = Dense(256, activation='relu', kernel_initializer=initializer, kernel_regularizer=l2(weight_decay))(y)
    y = Dropout(0.4)(y)
    y = BatchNormalization()(y)

    residual = Dense(256)(inp)      
    y = Add()([y, residual])        
    y = Dense(128, activation='relu', kernel_initializer=initializer, kernel_regularizer=l2(weight_decay))(y)
    y = Dropout(0.4)(y)
    y = BatchNormalization()(y)

    y = Dense(num_classes, activation='softmax')(y)

    m = Model(inputs=inp, outputs=y)
    optimizer = Adam(learning_rate=learning_rate)
    m.compile(loss='sparse_categorical_crossentropy', optimizer=optimizer, metrics=['accuracy'])
    return m

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--data_path", type=str, required=True, help="Path to the data folder")
    args = parser.parse_args()

    X, y = load_data(args.data_path)
    num_classes = len(np.unique(y))

    # Define a grid of learning rates and weight decay factors to search
    learning_rates = [1e-4, 1e-3, 1e-2,1e-5]
    weight_decay_factors = [1e-5, 1e-4, 1e-3]

    best_accuracy = 0
    best_f1 = 0
    best_lr = None
    best_weight_decay = None

    for learning_rate in learning_rates:
        for weight_decay in weight_decay_factors:
            print(f"Learning Rate: {learning_rate}, Weight Decay: {weight_decay}")

            model = build_model(X.shape[1:], num_classes, learning_rate, weight_decay)
            kf = KFold(n_splits=5, shuffle=True, random_state=40)

            accuracy_scores = []
            f1_scores = []

            for train_index, test_index in kf.split(X):
                X_train, X_test = X[train_index], X[test_index]
                y_train, y_test = y[train_index], y[test_index]

                model.fit(X_train, y_train, epochs=70, batch_size=64, validation_split=0.15, verbose=0)

                y_pred = model.predict(X_test)
                y_pred_classes = np.argmax(y_pred, axis=1)

                accuracy = accuracy_score(y_test, y_pred_classes)
                f1 = f1_score(y_test, y_pred_classes, average='weighted')

                accuracy_scores.append(accuracy)
                f1_scores.append(f1)

                print(f"Fold Accuracy: {accuracy}, F1 Score: {f1}")

            avg_accuracy = np.mean(accuracy_scores)
            avg_f1 = np.mean(f1_scores)

            print(f"Average Accuracy: {avg_accuracy}")
            print(f"Average F1 Score: {avg_f1}")

            if avg_accuracy > best_accuracy and avg_f1 > best_f1:
                best_accuracy = avg_accuracy
                best_f1 = avg_f1
                best_lr = learning_rate
                best_weight_decay = weight_decay

    print(f"Best Accuracy: {best_accuracy} (Learning Rate: {best_lr}, Weight Decay: {best_weight_decay})")
    print(f"Best F1 Score: {best_f1} (Learning Rate: {best_lr}, Weight Decay: {best_weight_decay})")