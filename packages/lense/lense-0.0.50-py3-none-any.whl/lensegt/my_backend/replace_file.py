import pandas as pd
import numpy as np
import warnings
warnings.filterwarnings('ignore')
def fix_errors(data):


    def coerce_to_correct_dtype(data):
        numeric_cols = []
        categorical_cols = []
        
        for col in data.columns:
            col_data = data[col]
            numeric_count = pd.to_numeric(col_data, errors='coerce').notna().sum()
            total_count = col_data.count()
            if numeric_count > total_count / 2:
                try:
                    data[col] = pd.to_numeric(col_data, errors='coerce')
                    numeric_cols.append(col)
                except ValueError:
                    pass
            else:
                categorical_cols.append(col)
        
        return numeric_cols, categorical_cols

    def fillna_with_mean_median_mode(data):
        data.replace(['none', 'N.A.', 'nan'], np.nan, inplace=True)
        data.replace(to_replace='[%]', value='', regex=True, inplace=True)
        numeric_cols, categorical_cols = coerce_to_correct_dtype(data)
        
        # Handle numerical columns
        if len(numeric_cols) > 0:
            print("Numerical columns")
            choice = input("For numerical columns, press 1 to fill with mean, 2 for custom value: ")
            if choice == '1':
                try:
                    fill_value = data[numeric_cols].mean()
                except TypeError as e:
                    print("Error computing mean for numerical columns. Likely due to non-numeric values.")
                    print("Please review the following columns for non-numeric values:")
                    print(numeric_cols)
                    return
            elif choice == '2':
                custom_value = input("Enter custom value for numerical columns: ")
                while True:
                    try:
                        fill_value = float(custom_value)
                        break
                    except ValueError:
                        print("Invalid input. Please enter a numerical value.")
                        custom_value = input("Enter custom value for numerical columns: ")
            else:
                print("Invalid choice. Using mean value to fill.")
                fill_value = data[numeric_cols].mean()
            
            # Fill numerical columns with the chosen value
            data[numeric_cols] = data[numeric_cols].fillna(fill_value)
        
        # Handle categorical columns
        if len(categorical_cols) > 0:
            print("Categorical columns")
            choice = input("For categorical columns, press 1 to fill with mode, 2 for custom value: ")
            if choice == '1':
                fill_value = data[categorical_cols].mode().iloc[0]
            elif choice == '2':
                custom_value = input("Enter custom value for categorical columns: ")
                fill_value = custom_value
            else:
                print("Invalid choice. Using mode value to fill.")
                fill_value = data[categorical_cols].mode().iloc[0]
            
            # Fill categorical columns with the chosen value
            data[categorical_cols] = data[categorical_cols].fillna(fill_value)

    fillna_with_mean_median_mode(data)
    data.to_csv("output_population.csv", index=False)
    return data