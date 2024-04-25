def data_visual():               
        

        import tkinter as tk
        from tkinter import filedialog
        
        print("select the folder where you want to save the jpg and csv files")

        root = tk.Tk()
        root.withdraw() # Hide the root window
        print("Select the file IBM-HR-Analytics-Employee-Attrition-and-Performance-Revised.csv")

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
    
        # Create a Tk root window and hide it
        root = tk.Tk()
        root.withdraw()
        
        # Open the directory selection dialog
        address = filedialog.askdirectory()
        
        # Print the selected folder path
        

        import numpy as np
        import pandas as pd

        #Library for Data Visualization.
        import seaborn as sns
        import matplotlib.pyplot as plt
        sns.set(style="white",font_scale=1.5)
        sns.set(rc={"axes.facecolor":"#FFFAF0","figure.facecolor":"#FFFAF0"})
        sns.set_context("poster",font_scale = .7)

        # Library to Display whole Dataset.
        pd.set_option("display.max.columns",None)
        pd.set_option("display.max.rows",None)

        # Ignore  the warnings
        import warnings
        warnings.filterwarnings('always')
        warnings.filterwarnings('ignore')

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

        ## <span style='color:red'> 1] VISUALIZING THE EMPLOYEE ATTRITION RATE. </span>

        #Visualization to show Employee Attrition in Counts.
        plt.figure(figsize=(17,6))
        plt.subplot(1,2,1)
        attrition_rate = employee_data["Attrition"].value_counts()
        sns.barplot(x=attrition_rate.index,y=attrition_rate.values,palette=["#1d7874","#8B0000"])
        plt.title("Employee Attrition Counts",fontweight="black",size=20,pad=20)
        for i, v in enumerate(attrition_rate.values):
                plt.text(i, v, v,ha="center", fontweight='black', fontsize=18)

        #Visualization to show Employee Attrition in Percentage.
        plt.subplot(1,2,2)
        plt.pie(attrition_rate, labels=["No","Yes"], autopct="%.2f%%", textprops={"fontweight":"black","size":15},
                colors = ["#1d7874","#AC1F29"],explode=[0,0.1],startangle=90)
        center_circle = plt.Circle((0, 0), 0.3, fc='white')
        fig = plt.gcf()
        fig.gca().add_artist(center_circle)
        plt.title("Employee Attrition Rate",fontweight="black",size=20,pad=10)
        
        plt.savefig(f"{address}/employee_attrition_counts.jpg", format='jpg', dpi=300)

        ### <font color=green>Inference:</font>

        ## <span style='color:red'> 2] ANALYZING EMPLOYEE ATTRITION BY GENDER. </span>

        #Visualization to show Total Employees by Gender.
        plt.figure(figsize=(14,6))
        plt.subplot(1,2,1)
        gender_attrition = employee_data["Gender"].value_counts()
        plt.title("Employees Distribution by Gender",fontweight="black",size=20)
        plt.pie(gender_attrition, autopct="%.0f%%",labels=gender_attrition.index,textprops=({"fontweight":"black","size":20}),
                explode=[0,0.1],startangle=90,colors= ["#ffb563","#FFC0CB"])

        #Visualization to show Employee Attrition by Gender.
        plt.subplot(1,2,2)
        new_df = employee_data[employee_data["Attrition"]=="Yes"]
        value_1 = employee_data["Gender"].value_counts()
        value_2 = new_df["Gender"].value_counts()
        attrition_rate = np.floor((value_2/value_1)*100).values
        sns.barplot(x=value_2.index, y=value_2.values,palette=["#D4A1E7","#E7A1A1"])
        plt.title("Employee Attrition Rate by Gender",fontweight="black",size=20,pad=20)
        for index,value in enumerate(value_2):
                plt.text(index,value,str(value)+" ("+str(int(attrition_rate[index]))+"% )",ha="center",va="bottom",
                size=15,fontweight="black")
        plt.tight_layout()
        plt.savefig(f"{address}/employee_attrition_Gender.jpg", format='jpg', dpi=300)
        
        ### <font color=green>Inference:</font>
        ## <span style='color:red'> 3] ANALYZING EMPLOYEE ATTRITION BY AGE. </span>

        #Visualization to show Employee Distribution by Age.
        plt.figure(figsize=(13.5,6))
        plt.subplot(1,2,1)
        sns.histplot(x="Age",hue="Attrition",data=employee_data,kde=True,palette=["#11264e","#6faea4"])
        plt.title("Employee Distribution by Age",fontweight="black",size=20,pad=10)

        #Visualization to show Employee Distribution by Age & Attrition.
        plt.subplot(1,2,2)
        sns.boxplot(x="Attrition",y="Age",data=employee_data,palette=["#D4A1E7","#6faea4"])
        plt.title("Employee Distribution by Age & Attrition",fontweight="black",size=20,pad=10)
        plt.tight_layout()
        
        plt.savefig(f"{address}/employee_attrition_Age.jpg", format='jpg', dpi=300)

        ### <font color=green>Inference:</font>

        ## <span style='color:red'> 4] ANALYZING EMPLOYEE ATTRITION BY BUSINESS TRAVEL. </span>

        #Visualization to show Total Employees by Businees Travel.
        plt.figure(figsize=(14,6))
        plt.subplot(1,2,1)
        value_1 = employee_data["BusinessTravel"].value_counts()
        plt.title("Employees by Business Travel", fontweight="black", size=20, pad=20)
        plt.pie(value_1.values, labels=value_1.index, autopct="%.1f%%",pctdistance=0.75,startangle=90,
                colors=['#E84040', '#E96060', '#E88181'],textprops={"fontweight":"black","size":15})
        center_circle = plt.Circle((0, 0), 0.4, fc='white')
        fig = plt.gcf()
        fig.gca().add_artist(center_circle)

        #Visualization to show Attrition Rate by Businees Travel.
        plt.subplot(1,2,2)
        new_df = employee_data[employee_data["Attrition"]=="Yes"]
        value_2 = new_df["BusinessTravel"].value_counts()
        attrition_rate = np.floor((value_2/value_1)*100).values
        sns.barplot(x=value_2.index,y=value_2.values,palette=["#11264e","#6faea4","#FEE08B"])
        plt.title("Attrition Rate by Businees Travel",fontweight="black",size=20,pad=20)
        for index,value in enumerate(value_2):
            plt.text(index,value,str(value)+" ("+str(int(attrition_rate[index]))+"% )",ha="center",va="bottom",
                size=15,fontweight="black")
        plt.tight_layout()
        
        plt.savefig(f"{address}/employee_attrition_BusinessTravel.jpg", format='jpg', dpi=300)

        ### <font color=green>Inference:</font>


        ## <span style='color:red'> 5] ANALYZING EMPLOYEE ATTRITION BY DEPARTMENT. </span>

        #Visualization to show Total Employees by Department.
        plt.figure(figsize=(14,6))
        plt.subplot(1,2,1)
        value_1 = employee_data["Department"].value_counts()
        sns.barplot(x=value_1.index, y=value_1.values,palette = ["#FFA07A", "#D4A1E7", "#FFC0CB"])
        plt.title("Employees by Department",fontweight="black",size=20,pad=20)
        for index,value in enumerate(value_1.values):
             plt.text(index,value,value,ha="center",va="bottom",fontweight="black",size=15,)

        #Visualization to show Employee Attrition Rate by Department.
        plt.subplot(1,2,2)
        new_df = employee_data[employee_data["Attrition"]=="Yes"]
        value_2 = new_df["Department"].value_counts()
        attrition_rate = np.floor((value_2/value_1)*100).values
        sns.barplot(x=value_2.index, y=value_2.values,palette=["#11264e","#6faea4","#FEE08B"])
        plt.title("Attrition Rate by Department",fontweight="black",size=20,pad=20)
        for index,value in enumerate(value_2):
          plt.text(index,value,str(value)+" ("+str(attrition_rate[index])+"% )",ha="center",va="bottom",
                size=15,fontweight="black")
        plt.tight_layout()
        
        ## <span style='color:red'> 6] ANALYZING EMPLOYEE ATTRITION BY DAILY RATE. </span>
        plt.savefig(f"{address}/employee_attrition_Department.jpg", format='jpg', dpi=300)

        employee_data["DailyRate"].describe().to_frame().T

        # Define the bin edges for the groups
        bin_edges = [0, 500, 1000, 1500]

        # Define the labels for the groups
        bin_labels = ['Low DailyRate', 'Average DailyRate', 'High DailyRate']

        # Cut the DailyRate column into groups
        employee_data['DailyRateGroup'] = pd.cut(employee_data['DailyRate'], bins=bin_edges, labels=bin_labels)

        ##Visualization to show Total Employees by DailyRateGroup.
        plt.figure(figsize=(13,6))
        plt.subplot(1,2,1)
        value_1 = employee_data["DailyRateGroup"].value_counts()
        plt.pie(value_1.values, labels=value_1.index,autopct="%.2f%%",textprops={"fontweight":"black","size":15},
                explode=[0,0.1,0.1],colors= ['#FF8000', '#FF9933', '#FFB366', '#FFCC99'])
        plt.title("Employees by DailyRateGroup",fontweight="black",pad=15,size=18)

        #Visualization to show Attrition Rate by DailyRateGroup.
        plt.subplot(1,2,2)
        new_df = employee_data[employee_data["Attrition"]=="Yes"]
        value_2 = new_df["DailyRateGroup"].value_counts()
        attrition_rate = np.floor((value_2/value_1)*100).values
        sns.barplot(x=value_2.index.tolist(),y= value_2.values,palette=["#11264e","#6faea4","#FEE08B"])
        plt.title("Employee Attrition Rate by DailyRateGroup",fontweight="black",pad=15,size=18)
        for index,value in enumerate(value_2.values):
            plt.text(index,value, str(value)+" ("+str(attrition_rate[index])+"%)",ha="center",va="bottom",fontweight="black",size=15)

        plt.tight_layout()

        plt.savefig(f"{address}/employee_attrition_DailyRateGroup.jpg", format='jpg', dpi=300)

        ## <span style='color:red'> 7] ANALYZING EMPLOYEE ATTRITION BY DISTANCE FROM HOME. </span>

        print("Total Unique Values in Attribute is =>",employee_data["DistanceFromHome"].nunique())

        employee_data["DistanceFromHome"].describe().to_frame().T

        # Define the bin edges for the groups
        bin_edges = [0,2,5,10,30]

        # Define the labels for the groups
        bin_labels = ['0-2 kms', '3-5 kms', '6-10 kms',"10+ kms"]

        # Cuttinf the DistaanceFromHome column into groups
        employee_data['DistanceGroup'] = pd.cut(employee_data['DistanceFromHome'], bins=bin_edges, labels=bin_labels)

        ##Visualization to show Total Employees by DistnaceFromHome.
        plt.figure(figsize=(14,6))
        plt.subplot(1,2,1)
        value_1 = employee_data["DistanceGroup"].value_counts()
        sns.barplot(x=value_1.index.tolist(), y=value_1.values,palette = ["#FFA07A", "#D4A1E7", "#FFC0CB","#87CEFA"])
        plt.title("Employees by Distance From Home",fontweight="black",pad=15,size=18)
        for index, value in enumerate(value_1.values):
                plt.text(index,value,value,ha="center",va="bottom",fontweight="black",size=15)
        
        #Visualization to show Attrition Rate by DistanceFromHome.
        plt.subplot(1,2,2)
        new_df = employee_data[employee_data["Attrition"]=="Yes"]
        value_2 = new_df["DistanceGroup"].value_counts()
        attrition_rate = np.floor((value_2/value_1)*100).values
        sns.barplot(x=value_2.index.tolist(),y= value_2.values,palette=["#11264e","#6faea4","#FEE08B","#D4A1E7","#E7A1A1"])
        plt.title("Attrition Rate by DistanceFromHome",fontweight="black",pad=15,size=18)
        for index,value in enumerate(value_2.values):
              plt.text(index,value, str(value)+" ("+str(attrition_rate[index])+"%)",ha="center",va="bottom",fontweight="black",size=15)

        plt.tight_layout()
        
        plt.savefig(f"{address}/employee_attrition_DistanceGroup.jpg", format='jpg', dpi=300)


        ## <span style='color:red'> 8] ANALYZING EMPLOYEE ATTRITION BY EDUCATION. </span>

        #Visualization to show Total Employees by Education.
        plt.figure(figsize=(13.5,6))
        plt.subplot(1,2,1)
        value_1 = employee_data["Education"].value_counts()
        sns.barplot(x=value_1.index,y=value_1.values,order=value_1.index,palette = ["#FFA07A", "#D4A1E7", "#FFC0CB","#87CEFA"])
        plt.title("Employees Distribution by Education",fontweight="black",size=20,pad=15)
        for index,value in enumerate(value_1.values):
            plt.text(index,value,value,ha="center",va="bottom",fontweight="black",size=15)
        
        #Visualization to show Employee Attrition by Education.
        plt.subplot(1,2,2)
        value_2 = new_df["Education"].value_counts()
        attrition_rate = np.floor((value_2/value_1)*100).values
        sns.barplot(x=value_2.index,y=value_2.values,order=value_2.index,palette=["#11264e","#6faea4","#FEE08B","#D4A1E7","#E7A1A1"])
        plt.title("Employee Attrition by Education",fontweight="black",size=18,pad=15)
        for index,value in enumerate(value_2.values):
             plt.text(index,value,str(value)+" ("+str(attrition_rate[index])+"%)",ha="center",va="bottom",
                fontweight="black",size=13)
        plt.tight_layout()
        
        plt.savefig(f"{address}/employee_attrition_Education.jpg", format='jpg', dpi=300)

        ### <font color=green>Inference:</font>

        ## <span style='color:red'> 9] ANALYZING EMPLOYEE ATTRITION BY EDUCATION FIELD. </span>

        #Visualization to show Total Employees by Education Field.
        plt.figure(figsize=(13.5,8))
        plt.subplot(1,2,1)
        value_1 = employee_data["EducationField"].value_counts()
        sns.barplot(x=value_1.index, y=value_1.values,order=value_1.index,palette = ["#FFA07A", "#D4A1E7", "#FFC0CB","#87CEFA"])
        plt.title("Employees by Education Field",fontweight="black",size=20,pad=15)
        for index,value in enumerate(value_1.values):
           plt.text(index,value,value,ha="center",va="bottom",fontweight="black",size=15)
        plt.xticks(rotation=90)

        #Visualization to show Employee Attrition by Education Field.
        plt.subplot(1,2,2)
        value_2 = new_df["EducationField"].value_counts()
        attrition_rate = np.floor((value_2/value_1)*100).values
        sns.barplot(x=value_2.index,y=value_2.values,order=value_2.index,palette=["#11264e","#6faea4","#FEE08B","#D4A1E7"])
        plt.title("Employee Attrition by Education Field",fontweight="black",size=18,pad=15)
        for index,value in enumerate(value_2.values):
           plt.text(index,value,str(value)+" ("+str(attrition_rate[index])+"%)",ha="center",va="bottom",
                fontweight="black",size=13)
        plt.xticks(rotation=90)
        plt.tight_layout()
        
        plt.savefig(f"{address}/employee_attrition_EducationField.jpg", format='jpg', dpi=300)

        ### <font color=green>Inference:</font>
        ## <span style='color:red'> 10] ANALYZING EMPLOYEE ATTRITION BY ENVIRONMENT SATISFACTION. </span>

        #Visualization to show Total Employees by EnvironmentSatisfaction.
        plt.figure(figsize=(14,6))
        plt.subplot(1,2,1)
        value_1 = employee_data["EnvironmentSatisfaction"].value_counts()
        plt.title("Employees by EnvironmentSatisfaction", fontweight="black", size=20, pad=20)
        plt.pie(value_1.values, labels=value_1.index, autopct="%.1f%%",pctdistance=0.75,startangle=90,
                colors=['#E84040', '#E96060', '#E88181'],textprops={"fontweight":"black","size":15})
        center_circle = plt.Circle((0, 0), 0.4, fc='white')
        fig = plt.gcf()
        fig.gca().add_artist(center_circle)

        #Visualization to show Attrition Rate by EnvironmentSatisfaction.
        plt.subplot(1,2,2)
        new_df = employee_data[employee_data["Attrition"]=="Yes"]
        value_2 = new_df["EnvironmentSatisfaction"].value_counts()
        attrition_rate = np.floor((value_2/value_1)*100).values
        sns.barplot(x=value_2.index,y=value_2.values,order=value_2.index,palette=["#11264e","#6faea4","#FEE08B","#D4A1E7","#E7A1A1"])
        plt.title("Attrition Rate by Environment Satisfaction",fontweight="black",size=20,pad=20)
        for index,value in enumerate(value_2):
                plt.text(index,value,str(value)+" ("+str(attrition_rate[index])+"% )",ha="center",va="bottom",
                size=15,fontweight="black")
        plt.tight_layout()


        plt.savefig(f"{address}/employee_attrition_EnvironmentSatisfaction.jpg", format='jpg', dpi=300)

        ## <span style='color:red'> 11] ANALYZING EMPLOYEE ATTRITION BY JOB ROLES. </span>

        #percentage seems to be wrong 



        ##Visualization to show Total Employees by JobRole.
        plt.figure(figsize=(13,8))
        plt.subplot(1,2,1)
        value_1 = employee_data["JobRole"].value_counts()
        sns.barplot(x=value_1.index.tolist(), y=value_1.values,palette = ["#FFA07A", "#D4A1E7", "#FFC0CB","#87CEFA"])
        plt.title("Employees by Job Role",fontweight="black",pad=15,size=18)
        plt.xticks(rotation=90)
        for index, value in enumerate(value_1.values):
               plt.text(index,value,value,ha="center",va="bottom",fontweight="black",size=15)
        
        #Visualization to show Attrition Rate by JobRole.
        plt.subplot(1,2,2)
        new_df = employee_data[employee_data["Attrition"]=="Yes"]
        value_2 = new_df["JobRole"].value_counts()
        attrition_rate = np.floor((value_2/value_1)*100).values
        sns.barplot(x=value_2.index.tolist(), y=value_2.values,palette=["#11264e","#6faea4","#FEE08B","#D4A1E7","#E7A1A1"])
        plt.title("Employee Attrition Rate by JobRole",fontweight="black",pad=15,size=18)
        plt.xticks(rotation=90)
        for index,value in enumerate(value_2.values):
            plt.text(index,value, str(value)+" ("+str(int(attrition_rate[index]))+"%)",ha="center",va="bottom",
                fontweight="black",size=10)
        plt.tight_layout()

        plt.savefig(f"{address}/employee_attrition_JobRole.jpg", format='jpg', dpi=300)

        ## <span style='color:red'> 12] ANALYZING EMPLOYEE ATTRITION BY JOB LEVEL. </span>

        #Visualization to show Total Employees by Job Level.
        plt.figure(figsize=(14,6))
        plt.subplot(1,2,1)
        value_1 = employee_data["JobLevel"].value_counts()
        plt.title("Employees by Job Level", fontweight="black", size=20, pad=20)
        plt.pie(value_1.values, labels=value_1.index, autopct="%.1f%%",pctdistance=0.8,startangle=90,
                colors=['#FF6D8C', '#FF8C94', '#FFAC9B', '#FFCBA4',"#FFD8B1"],textprops={"fontweight":"black","size":15})
        center_circle = plt.Circle((0, 0), 0.4, fc='white')
        fig = plt.gcf()
        fig.gca().add_artist(center_circle)
        
        #Visualization to show Attrition Rate by JobLevel.
        plt.subplot(1,2,2)
        new_df = employee_data[employee_data["Attrition"]=="Yes"]
        value_2 = new_df["JobLevel"].value_counts()
        attrition_rate = np.floor((value_2/value_1)*100).values
        sns.barplot(x=value_2.index,y=value_2.values,order=value_2.index,palette=["#11264e","#6faea4","#FEE08B","#D4A1E7","#E7A1A1"])
        plt.title("Attrition Rate by Job Level",fontweight="black",size=20,pad=20)
        for index,value in enumerate(value_2):
              plt.text(index,value,str(value)+" ("+str(attrition_rate[index])+"% )",ha="center",va="bottom",
                size=15,fontweight="black")
        plt.tight_layout()

        plt.savefig(f"{address}/employee_attrition_JobLevel.jpg", format='jpg', dpi=300)

        ## <span style='color:red'> 13] ANALYZING EMPLOYEE ATTRITION BY JOB SATISFACTION. </span>

        #Visualization to show Total Employees by Job Satisfaction.
        plt.figure(figsize=(14,6))
        plt.subplot(1,2,1)
        value_1 = employee_data["JobSatisfaction"].value_counts()
        plt.title("Employees by Job Satisfaction", fontweight="black", size=20, pad=20)
        plt.pie(value_1.values, labels=value_1.index, autopct="%.1f%%",pctdistance=0.8,startangle=90,
                colors=['#FFB300', '#FFC300', '#FFD700', '#FFFF00'],textprops={"fontweight":"black","size":15})
        center_circle = plt.Circle((0, 0), 0.4, fc='white')
        fig = plt.gcf()
        fig.gca().add_artist(center_circle)
        
        #Visualization to show Attrition Rate by Job Satisfaction.
        plt.subplot(1,2,2)
        new_df = employee_data[employee_data["Attrition"]=="Yes"]
        value_2 = new_df["JobSatisfaction"].value_counts()
        attrition_rate = np.floor((value_2/value_1)*100).values
        sns.barplot(x=value_2.index,y=value_2.values,order=value_2.index,palette=["#11264e","#6faea4","#FEE08B","#D4A1E7","#E7A1A1"])
        plt.title("Attrition Rate by Job Satisfaction",fontweight="black",size=20,pad=20)
        for index,value in enumerate(value_2):
               plt.text(index,value,str(value)+" ("+str(attrition_rate[index])+"% )",ha="center",va="bottom",
                size=15,fontweight="black")
        plt.tight_layout()
        
        plt.savefig(f"{address}/employee_attrition_JobSatisfaction.jpg", format='jpg', dpi=300)

        ### <font color=green>Inference:</font>
        ## <span style='color:red'> 14] ANALYZING EMPLOYEE ATTRITION BY MARTIAL STATUS. </span>

        #Visualization to show Total Employees by MaritalStatus.
        plt.figure(figsize=(14,6))
        plt.subplot(1,2,1)
        value_1 = employee_data["MaritalStatus"].value_counts()
        plt.title("Employees by MaritalStatus", fontweight="black", size=20, pad=20)
        plt.pie(value_1.values, labels=value_1.index, autopct="%.1f%%",pctdistance=0.75,startangle=90,
                colors=['#E84040', '#E96060', '#E88181', '#E7A1A1'],textprops={"fontweight":"black","size":15})
        center_circle = plt.Circle((0, 0), 0.4, fc='white')
        fig = plt.gcf()
        fig.gca().add_artist(center_circle)
        
        #Visualization to show Attrition Rate by MaritalStatus.
        plt.subplot(1,2,2)
        new_df = employee_data[employee_data["Attrition"]=="Yes"]
        value_2 = new_df["MaritalStatus"].value_counts()
        attrition_rate = np.floor((value_2/value_1)*100).values
        sns.barplot(x=value_2.index, y=value_2.values,palette=["#11264e","#6faea4","#FEE08B","#D4A1E7","#E7A1A1"])
        plt.title("Attrition Rate by MaritalStatus",
                fontweight="black",
                size=20,pad=20)
        for index,value in enumerate(value_2):
           plt.text(index,value,str(value)+" ("+str(attrition_rate[index])+"% )",ha="center",va="bottom",
                size=15,fontweight="black")
        plt.tight_layout()
        plt.savefig(f"{address}/employee_attrition_MaritalStatus.jpg", format='jpg', dpi=300)

        ### <font color=green>Inference:</font>


        ## <span style='color:red'> 15] ANALYZING EMPLOYEE ATTRITION BY MONTHLY INCOME. </span>

        #Visualization to show Employee Distribution by MonthlyIncome.
        plt.figure(figsize=(13,6))
        plt.subplot(1,2,1)
        sns.histplot(x="MonthlyIncome", hue="Attrition", kde=True ,data=employee_data,palette=["#11264e","#6faea4"])
        plt.title("Employee Attrition by Monthly Income",fontweight="black",size=20,pad=15)

        #Visualization to show Employee Attrition by Monthly Income.
        plt.subplot(1,2,2)
        sns.boxplot(x="Attrition",y="MonthlyIncome",data=employee_data,palette=["#D4A1E7","#6faea4"])
        plt.title("Employee Attrition by Monthly Income",fontweight="black",size=20,pad=15)
        plt.tight_layout()
        
        plt.savefig(f"{address}/employee_attrition_MonthlyIncome.jpg", format='jpg', dpi=300)

        ### <font color=green>Inference:</font>

        ## <span style='color:red'> 16] ANALYZING EMPLOYEE ATTRITION BY WORK EXPERIENCE. </span>

        employee_data["NumCompaniesWorked"].describe().to_frame().T

        # Define the bin edges for the groups
        bin_edges = [0, 1, 3, 5, 10]

        # Define the labels for the groups
        bin_labels = ['0-1 Companies', '2-3 companies', '4-5 companies', "5+ companies"]

        # Cut the DailyRate column into groups
        employee_data["NumCompaniesWorkedGroup"] = pd.cut(employee_data['NumCompaniesWorked'], bins=bin_edges, labels=bin_labels)

        #Visualization to show Total Employees by NumCompaniesWorked.
        plt.figure(figsize=(13,6))
        plt.subplot(1,2,1)
        value_1 = employee_data["NumCompaniesWorkedGroup"].value_counts()
        plt.title("Employees by Companies Worked", fontweight="black", size=20, pad=20)
        plt.pie(value_1.values, labels=value_1.index, autopct="%.1f%%",pctdistance=0.75,startangle=90,
                colors=['#FF6D8C', '#FF8C94', '#FFAC9B', '#FFCBA4'],textprops={"fontweight":"black","size":15})
        center_circle = plt.Circle((0, 0), 0.4, fc='white')
        fig = plt.gcf()
        fig.gca().add_artist(center_circle)
        
        #Visualization to show Attrition Rate by NumCompaniesWorked.
        plt.subplot(1,2,2)
        new_df = employee_data[employee_data["Attrition"]=="Yes"]
        value_2 = new_df["NumCompaniesWorkedGroup"].value_counts()
        attrition_rate = np.floor((value_2/value_1)*100).values
        sns.barplot(x=value_2.index.tolist(), y=value_2.values,palette=["#11264e","#6faea4","#FEE08B","#D4A1E7","#E7A1A1"])
        plt.title("Attrition Rate by Companies Worked",fontweight="black",size=20,pad=20)
        for index,value in enumerate(value_2):
               plt.text(index,value,str(value)+" ("+str(int(attrition_rate[index]))+"%)",ha="center",va="bottom",
                size=15,fontweight="black")
        plt.xticks(size=12)
        plt.tight_layout()
        
        plt.savefig(f"{address}/employee_attrition_NumCompaniesWorkedGroup.jpg", format='jpg', dpi=300)

        ### <font color=green>Inference:</font>
        ## <span style='color:red'> 17] ANALYZING EMPLOYEE ATTRITION BY OVERTIME. </span>

        #Visualization to show Total Employees by OverTime.
        plt.figure(figsize=(15,6))
        plt.subplot(1,2,1)
        value_1 = employee_data["OverTime"].value_counts()
        plt.title("Employees by OverTime", fontweight="black", size=20, pad=20)
        plt.pie(value_1.values, labels=value_1.index, autopct="%.1f%%",pctdistance=0.75,startangle=90,
                colors=["#ffb563","#FFC0CB"],textprops={"fontweight":"black","size":15})
        center_circle = plt.Circle((0, 0), 0.4, fc='white')
        fig = plt.gcf()
        fig.gca().add_artist(center_circle)

        
        #Visualization to show Attrition Rate by OverTime.
        plt.subplot(1,2,2)
        new_df = employee_data[employee_data["Attrition"]=="Yes"]
        value_2 = new_df["OverTime"].value_counts()
        attrition_rate = np.floor((value_2/value_1)*100).values
        sns.barplot(x=value_2.index.tolist(), y=value_2.values,palette=["#D4A1E7","#E7A1A1"])
        plt.title("Attrition Rate by OverTime",fontweight="black",size=20,pad=20)
        for index,value in enumerate(value_2):
             plt.text(index,value,str(value)+" ("+str(int(attrition_rate[index]))+"%)",ha="center",va="bottom",
                size=15,fontweight="black")
        plt.xticks(size=13)
        plt.tight_layout()
        
        plt.savefig(f"{address}/employee_attrition_OverTime.jpg", format='jpg', dpi=300)

        ### <font color=green>Inference:</font>

        ## <span style='color:red'> 18] ANALYZING EMPLOYEE ATTRITION BY SALARY HIKE. </span>

        #Visualization to show Employee Distribution by Percentage Salary Hike.
        plt.figure(figsize=(16,6))
        sns.countplot(x="PercentSalaryHike", hue="Attrition", data=employee_data, palette=["#1d7874","#AC1F29"])
        plt.title("Employee Attrition By PercentSalaryHike",fontweight="black",size=20,pad=15)
        
        plt.savefig(f"{address}/employee_attrition_counts.jpg", format='jpg', dpi=300)

        ### <font color=green>Inference:</font>

        ## <span style='color:red'> 19] ANALYZING EMPLOYEE ATTRITION BY PERFORMANCE RATING. </span>

        #Visualization to show Total Employees by PerformanceRating.
        plt.figure(figsize=(14,6))
        plt.subplot(1,2,1)
        value_1 = employee_data["PerformanceRating"].value_counts()
        plt.title("Employees by PerformanceRating", fontweight="black", size=20, pad=20)
        plt.pie(value_1.values, labels=value_1.index, autopct="%.1f%%",pctdistance=0.75,startangle=90,
                colors=["#ffb563","#FFC0CB"],textprops={"fontweight":"black","size":15})
        center_circle = plt.Circle((0, 0), 0.4, fc='white')
        fig = plt.gcf()
        fig.gca().add_artist(center_circle)
        
        #Visualization to show Attrition Rate by PerformanceRating.
        plt.subplot(1,2,2)
        new_df = employee_data[employee_data["Attrition"]=="Yes"]
        value_2 = new_df["PerformanceRating"].value_counts()
        attrition_rate = np.floor((value_2/value_1)*100).values
        sns.barplot(x=value_2.index.tolist(),y= value_2.values,palette=["#D4A1E7","#E7A1A1"])
        plt.title("Attrition Rate by PerformanceRating",fontweight="black",size=20,pad=20)
        for index,value in enumerate(value_2):
             plt.text(index,value,str(value)+" ("+str(int(attrition_rate[index]))+"%)",ha="center",va="bottom",
                size=15,fontweight="black")
        plt.tight_layout()
        
        plt.savefig(f"{address}/employee_attrition_PerformanceRating.jpg", format='jpg', dpi=300)

        ### <font color=green>Inference:</font>


        ## <span style='color:red'> 20] ANALYZING EMPLOYEE ATTRITION BY RELATIONSHIP SATISFACTION. </span>

        #Visualization to show Total Employees by RelationshipSatisfaction.
        plt.figure(figsize=(13,6))
        plt.subplot(1,2,1)
        value_1 = employee_data["RelationshipSatisfaction"].value_counts()
        plt.title("Employees by RelationshipSatisfaction", fontweight="black", size=20, pad=20)
        plt.pie(value_1.values, labels=value_1.index, autopct="%.1f%%",pctdistance=0.75,startangle=90,
                colors=['#6495ED', '#87CEEB', '#00BFFF', '#1E90FF'],textprops={"fontweight":"black","size":15})
        center_circle = plt.Circle((0, 0), 0.4, fc='white')
        fig = plt.gcf()
        fig.gca().add_artist(center_circle)
        
        #Visualization to show Attrition Rate by RelationshipSatisfaction.
        plt.subplot(1,2,2)
        new_df = employee_data[employee_data["Attrition"]=="Yes"]
        value_2 = new_df["RelationshipSatisfaction"].value_counts()
        attrition_rate = np.floor((value_2/value_1)*100).values
        sns.barplot(x=value_2.index, y=value_2.values,order=value_2.index,palette=["#11264e","#6faea4","#FEE08B","#D4A1E7","#E7A1A1"])
        plt.title("Attrition Rate by RelationshipSatisfaction",fontweight="black",size=20,pad=20)
        for index,value in enumerate(value_2):
             plt.text(index,value,str(value)+" ("+str(int(attrition_rate[index]))+"%)",ha="center",va="bottom",
                size=15,fontweight="black")
        plt.tight_layout()
        
        plt.savefig(f"{address}/employee_attrition_RelationshipSatisfaction.jpg", format='jpg', dpi=300)

        ### <font color=green>Inference:</font>


        ## <span style='color:red'> 21] ANALYZING EMPLOYEE ATTRITION BY WORK LIFE BALANCE. </span>

        ##Visualization to show Total Employees by WorkLifeBalance.
        plt.figure(figsize=(14.5,6))
        plt.subplot(1,2,1)
        value_1 = employee_data["WorkLifeBalance"].value_counts()
        plt.title("Employees by WorkLifeBalance", fontweight="black", size=20, pad=20)
        plt.pie(value_1.values, labels=value_1.index, autopct="%.1f%%",pctdistance=0.75,startangle=90,
                colors= ['#FF8000', '#FF9933', '#FFB366', '#FFCC99'],textprops={"fontweight":"black","size":15})
        center_circle = plt.Circle((0, 0), 0.4, fc='white')
        fig = plt.gcf()
        fig.gca().add_artist(center_circle)

        #Visualization to show Attrition Rate by WorkLifeBalance.
        plt.subplot(1,2,2)
        new_df = employee_data[employee_data["Attrition"]=="Yes"]
        value_2 = new_df["WorkLifeBalance"].value_counts()
        attrition_rate = np.floor((value_2/value_1)*100).values
        sns.barplot(x=value_2.index, y=value_2.values,order=value_2.index,palette=["#11264e","#6faea4","#FEE08B","#D4A1E7","#E7A1A1"])
        plt.title("Employee Attrition Rate by WorkLifeBalance",fontweight="black",pad=15,size=18)
        for index,value in enumerate(value_2.values):
            plt.text(index,value, str(value)+" ("+str(attrition_rate[index])+"%)",ha="center",va="bottom",
                fontweight="black",size=15)
        plt.tight_layout()
        
        plt.savefig(f"{address}/employee_attrition_WorkLifeBalance.jpg", format='jpg', dpi=300)

        ### <font color=green>Inference:</font>


        ## <span style='color:red'> 22] ANALYZING EMPLOYEE ATTRITION BY TOTAL WORKING EXPERIENCE. </span>

        # Define the bin edges for the groups
        bin_edges = [0, 5, 10, 20, 50]

        # Define the labels for the groups
        bin_labels = ['0-5 years', '5-10 years', '10-20 years', "20+ years"]

        # Cut the DailyRate column into groups
        employee_data["TotalWorkingYearsGroup"] = pd.cut(employee_data['TotalWorkingYears'], bins=bin_edges, labels=bin_labels)

        #Visualization to show Total Employees by TotalWorkingYearsGroup.
        plt.figure(figsize=(14,6))
        plt.subplot(1,2,1)
        value_1 = employee_data["TotalWorkingYearsGroup"].value_counts()
        plt.title("Employees by TotalWorkingYears", fontweight="black", size=20, pad=20)
        plt.pie(value_1.values, labels=value_1.index, autopct="%.1f%%",pctdistance=0.75,startangle=90,
                colors=['#E84040', '#E96060', '#E88181', '#E7A1A1'],textprops={"fontweight":"black","size":15})
        center_circle = plt.Circle((0, 0), 0.4, fc='white')
        fig = plt.gcf()
        fig.gca().add_artist(center_circle)
        
        #Visualization to show Attrition Rate by TotalWorkingYearsGroup.
        plt.subplot(1,2,2)
        new_df = employee_data[employee_data["Attrition"]=="Yes"]
        value_2 = new_df["TotalWorkingYearsGroup"].value_counts()
        attrition_rate = np.floor((value_2/value_1)*100).values
        sns.barplot(x=value_2.index.tolist(), y=value_2.values,palette=["#11264e","#6faea4","#FEE08B","#D4A1E7","#E7A1A1"])
        plt.title("Attrition Rate by TotalWorkingYears",fontweight="black",size=20,pad=20)
        for index,value in enumerate(value_2):
            plt.text(index,value,str(value)+" ("+str(int(attrition_rate[index]))+"%)",ha="center",va="bottom",
                size=15,fontweight="black")
        plt.tight_layout()
        
        plt.savefig(f"{address}/employee_attrition_TotalWorkingYears.jpg", format='jpg', dpi=300)

        ### <font color=green>Inference:</font>


        ## <span style='color:red'> 23] ANALYZING EMPLOYEE ATTRITION BY YEARS AT COMPANY. </span>

        # Define the bin edges for the groups
        bin_edges = [0, 1, 5, 10, 20]

        # Define the labels for the groups
        bin_labels = ['0-1 years', '2-5 years', '5-10 years', "10+ years"]

        # Cut the DailyRate column into groups
        employee_data["YearsAtCompanyGroup"] = pd.cut(employee_data['YearsAtCompany'], bins=bin_edges, labels=bin_labels)

        #Visualization to show Total Employees by YearsAtCompanyGroup.
        plt.figure(figsize=(14,6))
        plt.subplot(1,2,1)
        value_1 = employee_data["YearsAtCompanyGroup"].value_counts()
        plt.title("Employees by YearsAtCompany", fontweight="black", size=20, pad=20)
        plt.pie(value_1.values, labels=value_1.index, autopct="%.1f%%",pctdistance=0.75,startangle=90,
                colors=['#FFB300', '#FFC300', '#FFD700', '#FFFF00'],textprops={"fontweight":"black","size":15})
        center_circle = plt.Circle((0, 0), 0.4, fc='white')
        fig = plt.gcf()
        fig.gca().add_artist(center_circle)

        #Visualization to show Attrition Rate by YearsAtCompanyGroup.
        plt.subplot(1,2,2)
        new_df = employee_data[employee_data["Attrition"]=="Yes"]
        value_2 = new_df["YearsAtCompanyGroup"].value_counts()
        attrition_rate = np.floor((value_2/value_1)*100).values
        sns.barplot(x=value_2.index.tolist(), y=value_2.values,palette=["#11264e","#6faea4","#FEE08B","#D4A1E7","#E7A1A1"])
        plt.title("Attrition Rate by YearsAtCompany",fontweight="black",size=20,pad=20)
        for index,value in enumerate(value_2):
             plt.text(index,value,str(value)+" ("+str(int(attrition_rate[index]))+"%)",ha="center",va="bottom",
                size=15,fontweight="black")
        plt.tight_layout()
        
        plt.savefig(f"{address}/employee_attrition_YearsAtCompany.jpg", format='jpg', dpi=300)

        ### <font color=green>Inference:</font>


        ## <span style='color:red'> 24] ANALYZING EMPLOYEE ATTRITION BY YEARS IN CURRENT ROLE. </span>

        # Define the bin edges for the groups
        bin_edges = [0, 1, 5, 10, 20]

        # Define the labels for the groups
        bin_labels = ['0-1 years', '2-5 years', '5-10 years', "10+ years"]

        # Cut the DailyRate column into groups
        employee_data["YearsInCurrentRoleGroup"] = pd.cut(employee_data['YearsInCurrentRole'], bins=bin_edges, labels=bin_labels)

        #Visualization to show Total Employees by YearsInCurrentRoleGroup.
        plt.figure(figsize=(14,6))
        plt.subplot(1,2,1)
        value_1 = employee_data["YearsInCurrentRoleGroup"].value_counts()
        plt.title("Employees by YearsInCurrentRole", fontweight="black", size=20, pad=20)
        plt.pie(value_1.values, labels=value_1.index, autopct="%.1f%%",pctdistance=0.75,startangle=90,
                colors=['#6495ED', '#87CEEB', '#00BFFF', '#1E90FF'],textprops={"fontweight":"black","size":15,"color":"black"})
        center_circle = plt.Circle((0, 0), 0.4, fc='white')
        fig = plt.gcf()
        fig.gca().add_artist(center_circle)
        
        #Visualization to show Attrition Rate by YearsInCurrentRoleGroup.
        plt.subplot(1,2,2)
        new_df = employee_data[employee_data["Attrition"]=="Yes"]
        value_2 = new_df["YearsInCurrentRoleGroup"].value_counts()
        attrition_rate = np.floor((value_2/value_1)*100).values
        sns.barplot(x=value_2.index.tolist(), y=value_2.values,palette= ["#11264e","#6faea4","#FEE08B","#D4A1E7","#E7A1A1"])
        plt.title("Attrition Rate by YearsInCurrentRole",fontweight="black",size=20,pad=20)
        for index,value in enumerate(value_2):
           plt.text(index,value,str(value)+" ("+str(int(attrition_rate[index]))+"%)",ha="center",va="bottom",
                size=15,fontweight="black")
        plt.tight_layout()
        
        plt.savefig(f"{address}/employee_attrition_YearsInCurrentRole.jpg", format='jpg', dpi=300)

        ### <font color=green>Inference:</font>

        ## <span style='color:red'> 25] ANALYZING EMPLOYEE ATTRITION BY YEARS SINCE LAST PROMOTION. </span>

        # Define the bin edges for the groups
        bin_edges = [0, 1, 5, 10, 20]

        # Define the labels for the groups
        bin_labels = ['0-1 years', '2-5 years', '5-10 years', "10+ years"]

        # Cut the DailyRate column into groups
        employee_data["YearsSinceLastPromotionGroup"] = pd.cut(employee_data['YearsSinceLastPromotion'], bins=bin_edges, labels=bin_labels)

        #Visualization to show Total Employees by YearsSinceLastPromotionGroup.
        plt.figure(figsize=(14,6))
        plt.subplot(1,2,1)
        value_1 = employee_data["YearsSinceLastPromotionGroup"].value_counts()
        plt.title("Employees by YearsSinceLastPromotion", fontweight="black", size=20, pad=20)
        plt.pie(value_1.values, labels=value_1.index, autopct="%.1f%%",pctdistance=0.75,startangle=90,
                colors=['#FF6D8C', '#FF8C94', '#FFAC9B', '#FFCBA4'],textprops={"fontweight":"black","size":15})
        center_circle = plt.Circle((0, 0), 0.4, fc='white')
        fig = plt.gcf()
        fig.gca().add_artist(center_circle)
        
        #Visualization to show Attrition Rate by YearsSinceLastPromotionGroup.
        plt.subplot(1,2,2)
        new_df = employee_data[employee_data["Attrition"]=="Yes"]
        value_2 = new_df["YearsSinceLastPromotionGroup"].value_counts()
        attrition_rate = np.floor((value_2/value_1)*100).values
        sns.barplot(x=value_2.index.tolist(), y=value_2.values,palette=["#11264e","#6faea4","#FEE08B","#D4A1E7","#E7A1A1"])

        plt.title("Attrition Rate by YearsSinceLastPromotion",fontweight="black",size=20,pad=20)
        for index,value in enumerate(value_2):
           plt.text(index,value,str(value)+" ("+str(int(attrition_rate[index]))+"%)",ha="center",va="bottom",
                size=15,fontweight="black")
        plt.tight_layout()
        
        plt.savefig(f"{address}/employee_attrition_yearsincelastpromotion.jpg", format='jpg', dpi=300)

        ### <font color=green>Inference:</font>


        ## <span style='color:red'> 26] ANALYZING EMPLOYEE ATTRITION BY YEARS WITH CURRENT MANAGER. </span>

        # Define the bin edges for the groups
        bin_edges = [0, 1, 5, 10, 20]

        # Define the labels for the groups
        bin_labels = ['0-1 years', '2-5 years', '5-10 years', "10+ years"]

        # Cut the DailyRate column into groups
        employee_data["YearsWithCurrManagerGroup"] = pd.cut(employee_data['YearsWithCurrManager'], bins=bin_edges, labels=bin_labels)

        #Visualization to show Total Employees by YearsWithCurrManagerGroup.
        plt.figure(figsize=(14,6))
        plt.subplot(1,2,1)
        value_1 = employee_data["YearsWithCurrManagerGroup"].value_counts()
        plt.title("Employees by YearsWithCurrManager", fontweight="black", size=20, pad=20)
        plt.pie(value_1.values, labels=value_1.index, autopct="%.1f%%",pctdistance=0.75,startangle=90,
                colors= ['#FF8000', '#FF9933', '#FFB366', '#FFCC99'],textprops={"fontweight":"black","size":15})
        center_circle = plt.Circle((0, 0), 0.4, fc='white')
        fig = plt.gcf()
        fig.gca().add_artist(center_circle)

        #Visualization to show Attrition Rate by YearsWithCurrManagerGroup.
        plt.subplot(1,2,2)
        new_df = employee_data[employee_data["Attrition"]=="Yes"]
        value_2 = new_df["YearsWithCurrManagerGroup"].value_counts()
        attrition_rate = np.floor((value_2/value_1)*100).values
        sns.barplot(x=value_2.index.tolist(), y=value_2.values,palette=["#11264e","#6faea4","#FEE08B","#D4A1E7","#E7A1A1"])
        plt.title("Attrition Rate by YearsWithCurrManager",fontweight="black",size=20,pad=20)
        for index,value in enumerate(value_2):
            plt.text(index,value,str(value)+" ("+str(int(attrition_rate[index]))+"%)",ha="center",va="bottom",
                size=15,fontweight="black")
        plt.tight_layout()

        plt.savefig(f"{address}/employee_attrition_YearswithManager.jpg", format='jpg', dpi=300)





        ### <font color=green>Inference:</font>

        employee_data["PerformanceRating"].value_counts()

        employee_data["JobRole"].value_counts()

        employee_data["EducationField"].value_counts()

        fil_df=employee_data[employee_data['JobRole']=="Sales Executive"]

        value_1 = employee_data["Infield"].value_counts()
        value_1


        plt.figure(figsize=(14,6))
        plt.subplot(1,2,1)
        value_1 = employee_data["Infield"].value_counts()
        plt.title("Employees by Infield", fontweight="black", size=20, pad=20)
        plt.pie(value_1.values, labels=value_1.index, autopct="%.1f%%",pctdistance=0.75,startangle=90,
                colors=["#ffb563","#FFC0CB"],textprops={"fontweight":"black","size":15})
        center_circle = plt.Circle((0, 0), 0.4, fc='white')
        fig = plt.gcf()
        fig.gca().add_artist(center_circle)
        
        #Visualization to show Attrition Rate by PerformanceRating.
        plt.subplot(1,2,2)
        new_df = employee_data[employee_data["Attrition"]=="Yes"]
        value_2 = new_df["Infield"].value_counts()
        attrition_rate = np.floor((value_2/value_1)*100).values
        sns.barplot(x=value_2.index.tolist(),y= value_2.values,palette=["#D4A1E7","#E7A1A1"])
        plt.title("Attrition Rate by Infield",fontweight="black",size=20,pad=20)
        for index,value in enumerate(value_2):
             plt.text(index,value,str(value)+" ("+str(int(attrition_rate[index]))+"%)",ha="center",va="bottom",
                size=15,fontweight="black")
        plt.tight_layout()
        
        plt.savefig(f"{address}/employee_attrition_infield.jpg", format='jpg', dpi=300)

