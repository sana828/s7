import pandas as pd
import pickle

# Load the trained model from the pickle file
with open('rf.pkl', 'rb') as f:
    clf = pickle.load(f)

# Read the test data
test_data = pd.read_csv('data_out_5.csv')
testt=test_data[0:1]
##print()
# Assuming test data has the same features as training data (excluding the target column)
X_test = test_data

# Predict the labels for the test data
predictions = clf.predict(testt)[0]
print(predictions)
### Append the predicted output colum to the test data
##test_data['predicted_output'] = predictions
##
### Now, you need to manually enter the target output in a column, let's call it 'target_output'.
### You can do this in Excel or any other spreadsheet software.
##
### Save the test data with predicted and target output as output.csv
##test-data.to_csv('output_1.csv', index=False)