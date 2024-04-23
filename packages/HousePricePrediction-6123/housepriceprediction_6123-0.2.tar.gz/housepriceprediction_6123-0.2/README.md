# Median housing value prediction

The housing data can be downloaded from https://raw.githubusercontent.com/ageron/handson-ml/master/. The script has codes to download the data. We have modelled the median house value on given housing data.

The following techniques have been used:

 - Linear regression
 - Decision Tree
 - Random Forest

## Steps performed

1. **Data Preparation**: The housing data is cleaned and prepared. Missing values are checked and imputed.

2. **Feature Engineering**: Features are generated, and variables are checked for correlation.

3. **Modeling**: Multiple sampling techniques are evaluated. The dataset is split into training and testing sets. Various modeling techniques, including linear regression, decision trees, and random forest, are tried and evaluated. The mean squared error (MSE) is used as the evaluation metric.


### Follow these steps to run the code:

## How to Run the Code

Follow these steps to run the code:
1. create the environment
    ```conda env create --name mle-dev --file env.yml```
    or
    ```conda env create -f env.yml```

2. Activate the Conda environment:

   ```conda activate mle-dev```


## Execute the Scripts
### Run the following scripts sequentially:
````python ingest_data.py```
```python train.py train.csv```
```python src/score.py test.csv```

This README provides detailed instructions for setting up the environment, running the code, generating data and models, installing and configuring packages. Adjust paths and commands as needed based on your project setup.
