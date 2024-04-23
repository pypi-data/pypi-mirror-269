import os
import numpy as np
import re
import librosa
import tensorflow as tf
from tensorflow.keras.applications import VGG16
from tensorflow.keras.layers import Input, Flatten, Dense
from tensorflow.keras.models import Model
from sklearn.metrics import classification_report, accuracy_score, f1_score
from sklearn.model_selection import KFold
import argparse

def load_data(data_path, sr=44100):
    X = []
    y = []

    folders = os.listdir(data_path)

    for folder in folders:
        folder_path = os.path.join(data_path, folder)
        if os.path.isdir(folder_path):
            for filename in os.listdir(folder_path):
                if filename.endswith('.wav') or filename.endswith('.mp3'):
                    file_path = os.path.join(folder_path, filename)
                    audio, _ = librosa.load(file_path, sr=sr)

                    label = int(filename.split('-')[-1].split('.')[0])  # ESC

                    # Calculate the spectrogram from the audio
                    #spectrogram = librosa.feature.melspectrogram(y=audio, sr=sr)
                    #spectrogram = librosa.power_to_db(spectrogram, ref=np.max)
                    
                    spectrogram = np.abs(librosa.stft(audio, n_fft=2048))
                    spectrogram = np.mean(spectrogram, axis=1)

                    X.append(spectrogram)
                    y.append(label)

    X = np.array(X)
    y = np.array(y)

    # Print the number of unique labels
    num_unique_labels = len(np.unique(y))
    print('Number of Unique Labels:', num_unique_labels)

    return X, y

def build_model(input_shape, num_classes):
    # Load the VGG16 model with pretrained weights
    vgg16_model = VGG16(weights='imagenet', include_top=False, input_shape=input_shape)

    # Freeze the layers in the VGG16 base
    for layer in vgg16_model.layers:
        layer.trainable = False

    # Flatten the output of VGG16
    flatten_layer = Flatten()(vgg16_model.output)

    # Add a custom output layer for your specific classification task
    output_layer = Dense(num_classes, activation='softmax')(flatten_layer)

    # Create a new model with VGG16 base and custom output
    model = Model(inputs=vgg16_model.input, outputs=output_layer)

    # Compile the model
    model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])

    return model

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--data_path", type=str, required=True, help="Path to the data folder")
    args = parser.parse_args()

    X, y = load_data(args.data_path)
    num_classes = len(np.unique(y))

    # Define the number of cross-validation folds
    num_folds = 5
    kf = KFold(n_splits=num_folds, shuffle=True, random_state=42)

    accuracy_scores = []
    f1_scores = []

    for train_indices, test_indices in kf.split(X):
        X_train, X_test = X[train_indices], X[test_indices]
        y_train, y_test = y[train_indices], y[test_indices]

        # Build the VGG16-based model
        input_shape = X_train.shape[1:]  # Input shape is the shape of the spectrogram
        model = build_model(input_shape, num_classes)

        # Train the model
        model.fit(X_train, y_train, epochs=10, batch_size=32, validation_split=0.15, verbose=1)

        # Evaluate the model
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

    print("Cross-Validation Results:")
    print(f"Average Accuracy: {avg_accuracy}")
    print(f"Average F1 Score: {avg_f1}")
