GOAL: Automate the model creation.

Description:
    This project expecting the train data and target column. Based on the test data and target column can clean, encode, split, and fit a model 
    based on four algorithms(decissiontree, random forest, linear regression, gradient boosting). It will calculate the r2_score. Based on the r2 
    score it will finalize the model to this train data. Can pass your real data to this model for prediction.

Limitations:
    1) It will work for regression problems only not for classification problems.
    2) As a part of cleaning process using mode for categorical, median for numbers to fill the null values.
    3) considering r2_score only to finalize the model.
