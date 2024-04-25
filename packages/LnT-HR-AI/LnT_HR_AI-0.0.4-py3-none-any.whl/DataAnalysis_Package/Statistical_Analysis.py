def data_analysis():
    # Library for Data Manipulation
    import numpy as np
    import pandas as pd

    # Library for Data Visualization
    import matplotlib.pyplot as plt
    import seaborn as sns
    sns.set(style="white",font_scale=1.5)
    sns.set(rc={"axes.facecolor":"#FFFAF0","figure.facecolor":"#FFFAF0"})
    sns.set_context("poster",font_scale = .7)

    # Library to perform Statistical Analysis.
    from scipy import stats
    from scipy.stats import chi2
    from scipy.stats import chi2_contingency
    import tkinter as tk
    from tkinter import filedialog
    
    # Library for Ignore the warnings
    import warnings
    warnings.filterwarnings('always')
    warnings.filterwarnings('ignore')
    print("Select the file IBM-HR-Analytics-Employee-Attrition-and-Performance-Revised.csv")
    root = tk.Tk()
    root.withdraw() # Hide the root window
    
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

    employee_data = pd.read_csv(address)

    # Print top 5 rows in the dataframe.
    employee_data.head().style.set_properties(**{'background-color': '#E9F6E2','color': 'black','border-color': '#8b8c8c'})

    # Print bottom 5 rows in the dataframe.
    employee_data.tail().style.set_properties(**{'background-color': '#E9F6E2','color': 'black','border-color': '#8b8c8c'})

    # Print the shape of the DataFrame
    print("The shape of data frame:", employee_data.shape)
    # Print the length (number of rows) of the DataFrame
    print("Number of Rows in the dataframe:", len(employee_data))
    # Print the number of columns in the DataFrame
    print("Number of Columns in the dataframe:", len(employee_data.columns))



    num_cols = employee_data.select_dtypes(np.number).columns

    new_df = employee_data.copy()

    new_df["Attrition"] = new_df["Attrition"].replace({"No":0,"Yes":1})

    f_scores = {}
    p_values = {}

    for column in num_cols:
        f_score, p_value = stats.f_oneway(new_df[column],new_df["Attrition"])
        
        f_scores[column] = f_score
        p_values[column] = p_value


    plt.figure(figsize=(15,6))
    keys = list(f_scores.keys())
    values = list(f_scores.values())

    sns.barplot(x=keys, y=values)
    plt.title("Anova-Test F_scores Comparison",fontweight="black",size=20,pad=15)
    plt.xticks(rotation=90)

    for index,value in enumerate(values):
        plt.text(index,value,int(value), ha="center", va="bottom",fontweight="black",size=15)
    plt.show()

    ## <span style='color:blue'> 3] COMPARING F_SCORE AND P_VALUE OF ANOVA TEST. </span>

    test_df = pd.DataFrame({"Features":keys,"F_Score":values})
    test_df["P_value"] = [format(p, '.20f') for p in list(p_values.values())]

    test_df

    ## <font color=red>Inference:</font>


    cat_cols = employee_data.select_dtypes(include="object").columns.tolist()
    cat_cols.remove("Attrition")

    chi2_statistic = {}
    p_values = {}

    # Perform chi-square test for each column
    for col in cat_cols:
        contingency_table = pd.crosstab(employee_data[col], employee_data['Attrition'])
        chi2, p_value, _, _ = chi2_contingency(contingency_table)
        chi2_statistic[col] = chi2
        p_values[col] = p_value

    ## <span style='color:blue'> 5] VISUALIZE THE CHI-SQUARE STATISTICS VALUES </span>

    columns = list(chi2_statistic.keys())
    values = list(chi2_statistic.values())

    plt.figure(figsize=(16,6))
    sns.barplot(x=columns, y=values)
    plt.xticks(rotation=90)
    plt.title("Chi2 Statistic Value of each Categorical Columns",fontweight="black",size=20,pad=15)
    for index,value in enumerate(values):
        plt.text(index,value,round(value,2),ha="center",va="bottom",fontweight="black",size=15)

    plt.show()

    ## <span style='color:blue'> 6] COMPARING CHI^2_STATISTICS AND P_VALUE OF CHI^2 TEST. </span>

    test_df = pd.DataFrame({"Features":columns,"Chi_2 Statistic":values})
    test_df["P_value"] =  [format(p, '.20f') for p in list(p_values.values())]

    
    ## <span style='color:blue'> 7] DESCRIPTIVE ANALYSIS ON CATEGORICAL ATTRIBUTES </span>

    ## <font color=red>Inference:</font>

