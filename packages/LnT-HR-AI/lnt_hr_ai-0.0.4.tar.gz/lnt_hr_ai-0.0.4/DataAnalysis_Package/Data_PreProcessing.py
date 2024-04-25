
def DataPreProcessing():
    # Library for Data Manipulation
    import numpy as np
    import pandas as pd
    # Library for Statistical Modelling
    from sklearn.preprocessing import LabelEncoder
    import tkinter as tk
    from tkinter import filedialog
    root = tk.Tk()
    root.withdraw() # Hide the root window
    print("Select the file IBM-HR-Analytics-Employee-Attrition-and-Performance.csv")

    # Open the file dialog and get the selected file path
    file_path = filedialog.askopenfilename()
    
    # Print the selected file path
    address=""
    for iterator in file_path:
        if iterator=="/" :
            address+="\\\\"
        else:
            address+=iterator

        
    # Close the application
    root.destroy()
    
    # Library for Ignore the warnings
    import warnings
    warnings.filterwarnings('always')
    warnings.filterwarnings('ignore')

    
    employee_data = pd.read_csv(address)

    # Print top 5 rows in the dataframe.

    employee_data["PerformanceRating"].value_counts()
    #employee_data.head().style.set_properties(**{'background-color': '#E9F6E2','color': 'black','border-color': '#8b8c8c'})

    # Print bottom 5 rows in the dataframe.
    employee_data.tail().style.set_properties(**{'background-color': '#E9F6E2','color': 'black','border-color': '#8b8c8c'})
    ## <span style='color:blue'> 1] COMPUTING SIZE OF DATASET </span>

    # Print the shape of the DataFrame
    print("The shape of data frame:", employee_data.shape)
    # Print the length (number of rows) of the DataFrame
    print("Number of Rows in the dataframe:", len(employee_data))
    # Print the number of columns in the DataFrame
    print("Number of Columns in the dataframe:", len(employee_data.columns))

    ## <span style='color:blue'> 2] ENLIST COLUMNS OF DATASET </span>

    print("Column labels in the dataset in column order:")
    for column in employee_data.columns:
        print(column)

    ## <span style='color:blue'> 3] GENERATING BASIC INFORMATION OF ATTRIBUTES </span>

    # Print the Long summary of the dataframe by setting verbose = True
    # Check for Non-Null or Nan Nalues in the dataset.
    print(employee_data.info(verbose = True))

    ### <font color=red>Inference:</font>

    ## <span style='color:blue'> 4] ENLISTING NUMERICAL FEATURES </span>

    employee_data.select_dtypes(np.number).sample(5).style.set_properties(**{'background-color': '#E9F6E2',
                                                                'color': 'black','border-color': '#8b8c8c'})

    ### <font color=red>Inference:</font>
    ### 4.1] Labelling Categories in Numerical Feature

    employee_data["Education"] = employee_data["Education"].replace({1:"Below College",2:"College",3:"Bachelor",4:"Master",5:"Doctor"})

    employee_data["EnvironmentSatisfaction"] = employee_data["EnvironmentSatisfaction"].replace({1:"Low",2:"Medium",3:"High",4:"Very High"})

    employee_data["JobInvolvement"] = employee_data["JobInvolvement"].replace({1:"Low",2:"Medium",3:"High",4:"Very High"})

    employee_data["JobLevel"] = employee_data["JobLevel"].replace({1:"Entry Level",2:"Junior Level",3:"Mid Level",4:"Senior Level",
                                            5:"Executive Level"})

    employee_data["JobSatisfaction"] = employee_data["JobSatisfaction"].replace({1:"Low",2:"Medium",3:"High",4:"Very High"})

    employee_data["PerformanceRating"] = employee_data["PerformanceRating"].replace({1:"Low",2:"Good",3:"Excellent",4:"Outstanding"})

    employee_data["RelationshipSatisfaction"] = employee_data["RelationshipSatisfaction"].replace({1:"Low",2:"Medium",3:"High",4:"Very High"})

    employee_data["WorkLifeBalance"] = employee_data["WorkLifeBalance"].replace({1:"Bad",2:"Good",3:"Better",4:"Best"})

    ## <span style='color:blue'> 5] ENLISTING CATEGORICAL FEATURES </span>

    employee_data.select_dtypes(include="O").sample(5).style.set_properties(**{'background-color': '#E9F6E2',
                                                                    'color': 'black','border-color': '#8b8c8c'})

    ## <span style='color:blue'> 6] CHECK FOR MISSING VALUES </span>

    x=0
    Infield=[]
    for j, i in zip(employee_data["JobRole"], employee_data["EducationField"]):
        
        if (j =="Sales Executive" or j=="Human Resources" or j=="Sales Representative") and (i =="Medical"or  i=="Technical Degree"):
            Infield.append(1)      
        else: 
            Infield.append(0)
            

    employee_data["Infield"]=Infield



    # Calculate the number of missing values in each column
        
    missing_df = employee_data.isnull().sum().to_frame().rename(columns={0:"Total No. of Missing Values"})
    missing_df["% of Missing Values"] = round((missing_df["Total No. of Missing Values"]/len(employee_data))*100,2)
    missing_df

    ### <font color=red>Inference:</font>

    ## <span style='color:blue'> 7] DESCRIPTIVE ANALYSIS ON NUMERICAL ATTRIBUTES </span>

    employee_data.describe().T

    ### <font color=red>Inference:</font>
    ## <span style='color:blue'> 8] DROP UNNECESSARY COLUMNS </span>

    employee_data.drop(['EmployeeCount', 'EmployeeNumber', 'Over18', 'StandardHours'], axis="columns", inplace=True)

    # Print top 5 rows in the dataframe.

    # Print the shape of the DataFrame
    print("The shape of data frame:", employee_data.shape)
    # Print the length (number of rows) of the DataFrame
    print("Number of Rows in the dataframe:", len(employee_data))
    # Print the number of columns in the DataFrame
    print("Number of Columns in the dataframe:", len(employee_data.columns))

    print("Column labels in the dataset in column order:")
    for column in employee_data.columns:
        print(column)

    ## <span style='color:blue'> 9] DESCRIPTIVE ANALYSIS ON CATEGORICAL ATTRIBUTES </span>

    employee_data.describe(include="O").T


    # Calculate the number of unique values in each column
    for column in employee_data.columns:
        print(f"{column} - Number of unique values : {employee_data[column].nunique()}")
        print("=============================================================")

    categorical_features = []
    for column in employee_data.columns:
        if employee_data[column].dtype == object and len(employee_data[column].unique()) <= 30:
            categorical_features.append(column)
            print(f"{column} : {employee_data[column].unique()}")
            print(employee_data[column].value_counts())
            print("====================================================================================")
    categorical_features.remove('Attrition')


    # Save DataFrame to CSV file
    employee_data.to_csv('IBM-HR-Analytics-Employee-Attrition-and-Performance-Revised.csv', index=False)
    import os

    # Assuming the file is saved in the current directory
    if 'IBM-HR-Analytics-Employee-Attrition-and-Performance-Revised.csv' in os.listdir('.'):
        print("File created successfully.")
    else:
        print("File not found.")
        import os

# Assuming 'file_path' is the path to your file
    file_path = 'IBM-HR-Analytics-Employee-Attrition-and-Performance-Revised.csv'

    # Get the absolute path of the file
    full_path = os.path.abspath(file_path)

    # Print the full path
    print(full_path)



DataPreProcessing()
































