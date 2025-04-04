import os
import csv
import random
from sklearn import linear_model
from sklearn import metrics
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


def extract_features(data, feature_conditions):
    # return pd.Series(True, index=data.index)
    return data[feature_conditions]


def compute_vector(data, feature_conditions=None):
    if feature_conditions:
        mask = pd.Series(True, index=data.index)

        for feature_cond in feature_conditions:
            mask &= data.eval(feature_cond)

        return mask.astype(int)


def load_data(data_path, write_file=False, write_path=None):
    features_array = []
    data = []
    if os.path.isfile(data_path):
        with open(data_path, 'r') as f:
            reader = csv.reader(f)

            i = 0
            for row in reader:
                if i == 0:
                    features_array = row
                    print(f"features: {features_array}")
                else:
                    data.append(row)
                    print(f"data row: {row}")

                i += 1

            features_array = np.array(features_array)
            data = np.array(data)

            if write_file and write_path:
                np.save(write_path + "/data.npy", data)
                np.save(write_path + "/feature_names.npy", features_array)

            return features_array, data

    else:
        raise FileNotFoundError("csv file not found")


def get_selected_features(data_path, features_arr, write_file=False, write_path=None):
    data = []
    print(f"features chosen: {features_arr}")

    if os.path.isfile(data_path):
        print(f"choosing columns: {data_path}")
        df = pd.read_csv(data_path, usecols=features_arr)
        data = df.to_numpy()

        if write_file and write_path:

            np.save(write_path + "/selected_data.npy", data)

    return data


def separate_sets(data_arr, seed=42):
    random.seed(42)
    random.shuffle(data_arr)

    split_idx = int(len(data_arr) * 0.80)
    training_arr = data_arr[ :split_idx]
    testing_arr = data_arr[split_idx: ]
    print(f"training size: {len(training_arr)}, testing size: {len(testing_arr)}")

    return training_arr, testing_arr


def train_lr_model(x_train, y_train):
    model = linear_model.LinearRegression()
    model.fit(x_train, y_train)
    return model


def test_lr_model(model, x_test, y_test):
    y_predictions = model.predict(x_test)
    mse_error = metrics.mean_squared_error(y_test, y_predictions)

    if x_test.shape[1] != 1:
        print("Cannot plot: More than one feature in x_test.")
        return mse_error

    # Reshape to 1D for plotting
    x_flat = x_test[:, 0]

    # Sort by x for smooth line
    sort_idx = np.argsort(x_flat)
    x_sorted = x_flat[sort_idx]
    y_sorted = y_predictions[sort_idx]

    # Plot
    plt.scatter(x_flat, y_test, label='True Data', color='blue')
    plt.plot(x_sorted, y_sorted, label='Regression Line', color='red')
    plt.xlabel('x')
    plt.ylabel('y')
    plt.legend()
    plt.title('Linear Regression')
    plt.show()

    return mse_error





