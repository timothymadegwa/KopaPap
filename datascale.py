import pandas as pd
import sklearn.datasets as datasets
from sklearn.preprocessing import MinMaxScaler
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
import numpy as np

X, y = datasets.make_classification(scale=None)
X_int = X.astype(int)
y_int = y.astype(int)

# split the dataset in training and test
SPLIT = 70
X_train = X_int[0:SPLIT-1]
X_test = X_int[SPLIT:]
#X_train, X_test, y_train, y_test = train_test_split(X_int,y_int,test_size=0.3,random_state=122)

# can repeat the procedure for MinMaxScaler, StandardScaler etc.
MIN = 5
MAX = 85
mms = MinMaxScaler(feature_range=(MIN, MAX))

# Fit on training set only. Fit and transform performed in the same step
# Fit saves the parameters 'mean' and 'standard deviation' for further use
# X_scaled = (X - mean)/std_deviation
X_train_mms = mms.fit_transform(X_train)

print('Scaling with MinMaxScaler')
# Apply scaling on test set
X_test_mms = mms.transform(X_test)
print('Scalar fit on train dataset of {}%'.format(SPLIT))

# show as an example the last row
print(X_test_mms[-1])

# Transform the whole set, with fitting and transformation in one step
print('Scaling applied to whole dataset')
mmsa = MinMaxScaler(feature_range=(1, 99))
mmsa.fit_transform(X_int)
X_all_mms = mmsa.transform(X_int)
# display as an example the last row
print(X_all_mms[-1])

print('% Percentage difference between trained and whole dataset scaler')
X_diff = X_all_mms[-1] - X_test_mms[-1]
X_diff_perc = (100/(MAX-MIN+1)) * X_diff
print(X_diff_perc.astype(int))

# Consider a new row to the whole dataset and scale it
X_row = np.random.uniform(low=5, high=95, size=(20,))
print('New observation:')
print(X_row)
print('New observation scaled:')
X_row_norm = mms.transform([X_row])
print(X_row_norm[0])
