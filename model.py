import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error
from sklearn.model_selection import train_test_split, RandomizedSearchCV
from sklearn.model_selection import GridSearchCV

import data_prepare
from scipy.stats import randint

# Local new df
new_df = data_prepare.prepare_data()

# Perform one-hot encoding for categorical variables
categorical_columns = ["author", "medium"]
encoded_df = pd.get_dummies(new_df, columns=categorical_columns)

# Separate the features (X) and the target variable (y)
X = encoded_df.drop("hammer_price", axis=1)
y = encoded_df["hammer_price"]

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=11)

print(X_train.iloc[0])

# Initialize and train the Random Forest regression model
rf_model = RandomForestRegressor(random_state=420)
# Grid search >
# Define the parameter grid for grid search
# Define the parameter distribution for random search
param_dist = {
    'n_estimators': randint(100, 500),
    'max_depth': [None, 5, 10, 20],
    'min_samples_split': randint(2, 10),
    'min_samples_leaf': randint(1, 5)
}


# Perform random search with cross-validation
random_search = RandomizedSearchCV(rf_model, param_dist, n_iter=4, cv=5, scoring='neg_mean_squared_error')
random_search.fit(X_train, y_train)

# Print the best hyperparameters and best score
print("Best Hyperparameters:", random_search.best_params_)
print("Best Score (Negative MSE):", random_search.best_score_)
# < Grid search
# rf_model.fit(X_train, y_train)
rf_model = random_search

# Make predictions on the training set
y_train_pred = rf_model.predict(X_train)

# Calculate the mean squared error on the training set
mse_train = mean_squared_error(y_train, y_train_pred)
print("Mean Squared Error (Training):", mse_train)

# Make predictions on the test set
y_test_pred = rf_model.predict(X_test)

# Calculate the mean squared error on the test set
mse_test = mean_squared_error(y_test, y_test_pred)
print("Mean Squared Error (Testing):", mse_test)

# Define the parameters for the new artwork
new_artwork = {
    'author_Igor Mitoraj': 1,
    'medium_lithography/paper': 1,
    'width': 64.0,
    'height': 48.0
}

# Create a DataFrame for the new artwork
new_artwork_df = pd.DataFrame([new_artwork])

# Perform one-hot encoding for the categorical variables
new_artwork_encoded = pd.get_dummies(new_artwork_df)

# Align the columns of the new artwork data with the training data columns
new_artwork_encoded = new_artwork_encoded.reindex(columns=X_train.columns, fill_value=0)

# Make the prediction using the trained model
predicted_price = rf_model.predict(new_artwork_encoded)

# Print the predicted hammer price
print("Predicted Hammer Price:", predicted_price[0])