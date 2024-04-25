
def Run_MLModels():
    
    import tkinter as tk
    from tkinter import filedialog
    import csv
    # Create a Tk root window and hide it
    print("select the folder where you want to save the jpg and csv files")
    root = tk.Tk()
    root.withdraw()
        
        # Open the directory selection dialog
    address = filedialog.askdirectory()
        
    # Library for Data Manipulation
    import numpy as np
    import pandas as pd

    #Library for Data Visualization.
    import seaborn as sns
    import matplotlib.pyplot as plt
    import hvplot
    sns.set_style("whitegrid")
    plt.style.use("fivethirtyeight")

    # Library for Statistical Modelling
    from sklearn.preprocessing import LabelEncoder
    from sklearn.preprocessing import StandardScaler
    from sklearn.metrics import confusion_matrix, accuracy_score, classification_report, roc_auc_score, precision_recall_curve, roc_curve
    from sklearn.model_selection import train_test_split, GridSearchCV
    from sklearn.linear_model import LogisticRegression
    from sklearn.ensemble import RandomForestClassifier
    from sklearn.svm import SVC
    from xgboost import XGBClassifier
    from lightgbm import LGBMClassifier
    from catboost import CatBoostClassifier
    from sklearn.ensemble import AdaBoostClassifier

    print("==================== Packages Loaded ======================")

    # Library for Ignore the warnings
    import warnings
    warnings.filterwarnings('always')
    warnings.filterwarnings('ignore')
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


    # Convert categorical variables into numerical form. 
    label = LabelEncoder()
    employee_data["Attrition"] = label.fit_transform(employee_data.Attrition)

    employee_data.info()


    # Transform categorical data into dummies
    dummy_col = [column for column in employee_data.drop('Attrition', axis=1).columns if employee_data[column].nunique() < 20]
    data = pd.get_dummies(employee_data, columns=dummy_col, drop_first=True, dtype='uint8')
    data.info()

    print(data.shape)

    # Remove duplicate Features
    data = data.T.drop_duplicates()
    data = data.T

    # Remove Duplicate Rows
    data.drop_duplicates(inplace=True)

    print(data.shape)

    data.drop('Attrition', axis=1).corrwith(data.Attrition).sort_values().plot(kind='barh', figsize=(10, 30))

    feature_correlation = data.drop('Attrition', axis=1).corrwith(data.Attrition).sort_values()
    model_col = feature_correlation[np.abs(feature_correlation) > 0.02].index
    len(model_col)

    X = data.drop('Attrition', axis=1)
    y = data.Attrition

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42,
                                                        stratify=y)

    scaler = StandardScaler()
    X_train_std = scaler.fit_transform(X_train)
    X_test_std = scaler.transform(X_test)
    X_std = scaler.transform(X)

    def feature_imp(df, model):
        fi = pd.DataFrame()
        fi["feature"] = df.columns
        fi["importance"] = model.feature_importances_
        return fi.sort_values(by="importance", ascending=False)

    y_test.value_counts()[0] / y_test.shape[0]

    stay = (y_train.value_counts()[0] / y_train.shape)[0]
    leave = (y_train.value_counts()[1] / y_train.shape)[0]

    print("===============TRAIN=================")
    print(f"Staying Rate: {stay * 100:.2f}%")
    print(f"Leaving Rate: {leave * 100 :.2f}%")

    stay = (y_test.value_counts()[0] / y_test.shape)[0]
    leave = (y_test.value_counts()[1] / y_test.shape)[0]

    print("===============TEST=================")
    print(f"Staying Rate: {stay * 100:.2f}%")
    print(f"Leaving Rate: {leave * 100 :.2f}%")

    #The rows are Training accuracy, Testing accuracy, ROC, AUC
        
    ml_model_comparsion = {
        'Support Vector Machinegrid':[],
        'Random Forestgrid':[],
        'Random Forest':[] , 
        'XGBoost': [], 
        'Logistic Regression':[] ,
        'Support Vector Machine':[] ,
        'LightGBM':[] ,
        'CatBoost':[] ,
        'AdaBoost':[] 
    }

    def evaluate(model, X_train, X_test, y_train, y_test,model_name):

        y_test_pred = model.predict(X_test)
        y_train_pred = model.predict(X_train)

        print("TRAINIG RESULTS: \n===============================")
        clf_report = pd.DataFrame(classification_report(y_train, y_train_pred, output_dict=True))
        print(f"CONFUSION MATRIX:\n{confusion_matrix(y_train, y_train_pred)}")
        print(f"ACCURACY SCORE:\n{accuracy_score(y_train, y_train_pred):.4f}")
        print(f"CLASSIFICATION REPORT:\n{clf_report}")
        ml_model_comparsion[model_name].append(accuracy_score(y_train, y_train_pred))

        print("TESTING RESULTS: \n===============================")
        clf_report = pd.DataFrame(classification_report(y_test, y_test_pred, output_dict=True))
        print(f"CONFUSION MATRIX:\n{confusion_matrix(y_test, y_test_pred)}")
        print(f"ACCURACY SCORE:\n{accuracy_score(y_test, y_test_pred):.4f}")
        print(f"CLASSIFICATION REPORT:\n{clf_report}")
        ml_model_comparsion[model_name].append(accuracy_score(y_test, y_test_pred)) 


    lr_clf = LogisticRegression(solver='liblinear', penalty='l1')
    lr_clf.fit(X_train_std, y_train)

    evaluate(lr_clf, X_train_std, X_test_std, y_train, y_test,'Logistic Regression')

    def plot_precision_recall_vs_threshold(precisions, recalls, thresholds,name):
        plt.plot(thresholds, precisions[:-1], "b--", label="Precision")
        plt.plot(thresholds, recalls[:-1], "g--", label="Recall")
        plt.xlabel("Threshold")
        plt.legend(loc="upper left")
        plt.title("Precision/Recall Tradeoff")
        plt.savefig(f"{address}/PR_{name}.jpg", format='jpg', dpi=300)

        

    def plot_roc_curve(fpr, tpr,name1, label=None):
        plt.plot(fpr, tpr, linewidth=2, label=label)
        plt.plot([0, 1], [0, 1], "k--")
        plt.axis([0, 1, 0, 1])
        plt.xlabel('False Positive Rate')
        plt.ylabel('True Positive Rate')
        plt.title('ROC Curve')
        plt.savefig(f"{address}/ROC_{name1}.jpg", format='jpg', dpi=300)
        
        
    precisions, recalls, thresholds = precision_recall_curve(y_test, lr_clf.predict(X_test_std))
    plt.figure(figsize=(14, 25))
    plt.subplot(4, 2, 1)
    plot_precision_recall_vs_threshold(precisions, recalls, thresholds,"Logistic Regression")

    plt.subplot(4, 2, 2)
    plt.plot(precisions, recalls)
    plt.xlabel("Precision")
    plt.ylabel("Recall")
    plt.title("PR Curve: precisions/recalls tradeoff LogisticRegression")
    plt.savefig(f"{address}/PR CurveLR.jpg", format='jpg', dpi=300)


    plt.subplot(4, 2, 3)
    fpr, tpr, thresholds = roc_curve(y_test, lr_clf.predict(X_test_std))
    plot_roc_curve(fpr, tpr,"Logistic Regression")

    scores_dict = {
        'Logistic Regression': {
            'Train': roc_auc_score(y_train, lr_clf.predict(X_train)),
            'Test': roc_auc_score(y_test, lr_clf.predict(X_test)),
        },
    }


    rf_clf = RandomForestClassifier(n_estimators=100, bootstrap=False,
    #                                      class_weight={0:stay, 1:leave}
                                        )
    rf_clf.fit(X_train, y_train)
    evaluate(rf_clf, X_train, X_test, y_train, y_test,'Random Forest')

    param_grid = dict(
        n_estimators= [100, 500, 900], 
        max_features= ['auto', 'sqrt'],
        max_depth= [2, 3, 5, 10, 15, None], 
        min_samples_split= [2, 5, 10],
        min_samples_leaf= [1, 2, 4], 
        bootstrap= [True, False]
    )

    rf_clf = RandomForestClassifier(random_state=42)
    search = GridSearchCV(rf_clf, param_grid=param_grid, scoring='roc_auc', cv=5, verbose=1, n_jobs=-1)
    search.fit(X_train, y_train)

    rf_clf = RandomForestClassifier(**search.best_params_, random_state=42)
    rf_clf.fit(X_train, y_train)
    evaluate(rf_clf, X_train, X_test, y_train, y_test,'Random Forestgrid')

    precisions, recalls, thresholds = precision_recall_curve(y_test, rf_clf.predict(X_test))
    plt.figure(figsize=(14, 25))
    plt.subplot(4, 2, 1)
    plot_precision_recall_vs_threshold(precisions, recalls, thresholds,"Random Forestgrid")

    plt.subplot(4, 2, 2)    
    plt.plot(precisions, recalls)
    plt.xlabel("Precision")
    plt.ylabel("Recall")
    plt.title("PR Curve: precisions/recalls tradeoff RandomForest")
    plt.savefig(f"{address}/PR CurveRF.jpg", format='jpg', dpi=300)

    plt.subplot(4, 2, 3)
    fpr, tpr, thresholds = roc_curve(y_test, rf_clf.predict(X_test))
    plot_roc_curve(fpr, tpr,"RandomForest")

    scores_dict['Random Forest'] = {
            'Train': roc_auc_score(y_train, rf_clf.predict(X_train)),
            'Test': roc_auc_score(y_test, rf_clf.predict(X_test)),
        }

    df = feature_imp(X, rf_clf)[:40]
    df.set_index('feature', inplace=True)
    df.plot(kind='barh', figsize=(10, 10))
    plt.title('Feature Importance according to Random Forest')
    plt.savefig(f"{address}/Feature Importance according to Random Forest.jpg", format='jpg', dpi=300)


    svm_clf = SVC(kernel='linear')
    svm_clf.fit(X_train_std, y_train)

    evaluate(svm_clf, X_train_std, X_test_std, y_train, y_test,'Support Vector Machine')

    svm_clf = SVC(random_state=42)

    param_grid = [
        {'C': [1, 10, 100, 1000], 'kernel': ['linear']},
        {'C': [1, 10, 100, 1000], 'gamma': [0.001, 0.0001], 'kernel': ['rbf']}
    ]

    search = GridSearchCV(svm_clf, param_grid=param_grid, scoring='roc_auc', cv=3, refit=True, verbose=1)
    search.fit(X_train_std, y_train)
    svm_clf = SVC(**search.best_params_)
    svm_clf.fit(X_train_std, y_train)

    evaluate(svm_clf, X_train_std, X_test_std, y_train, y_test,'Support Vector Machinegrid')


    precisions, recalls, thresholds = precision_recall_curve(y_test, svm_clf.predict(X_test_std))
    plt.figure(figsize=(14, 25))
    plt.subplot(4, 2, 1)
    plot_precision_recall_vs_threshold(precisions, recalls, thresholds,"Support Vector Machinegrid")

    plt.subplot(4, 2, 2)
    plt.plot(precisions, recalls)
    plt.xlabel("Precision")
    plt.ylabel("Recall")
    plt.title("PR Curve: precisions/recalls tradeoff for SVM")
    plt.savefig(f"{address}/employee_attrition_counts.jpg", format='jpg', dpi=300)

    plt.subplot(4, 2, 3)
    fpr, tpr, thresholds = roc_curve(y_test, svm_clf.predict(X_test_std))
    plot_roc_curve(fpr, tpr,"Support vector machine")

    scores_dict['Support Vector Machine'] = {
            'Train': roc_auc_score(y_train, svm_clf.predict(X_train_std)),
            'Test': roc_auc_score(y_test, svm_clf.predict(X_test_std)),
        }


    xgb_clf = XGBClassifier()
    xgb_clf.fit(X_train, y_train)

    evaluate(xgb_clf, X_train, X_test, y_train, y_test,'XGBoost')

    scores_dict['XGBoost'] = {
            'Train': roc_auc_score(y_train, xgb_clf.predict(X_train)),
            'Test': roc_auc_score(y_test, xgb_clf.predict(X_test)),
        }

    precisions, recalls, thresholds = precision_recall_curve(y_test, xgb_clf.predict(X_test))
    plt.figure(figsize=(14, 25))
    plt.subplot(4, 2, 1)
    plot_precision_recall_vs_threshold(precisions, recalls, thresholds,"XGB")

    plt.subplot(4, 2, 2)
    plt.plot(precisions, recalls)
    plt.xlabel("Precision")
    plt.ylabel("Recall")
    plt.title("PR Curve: precisions/recalls tradeoff for XGBoost")
    plt.savefig(f"{address}/recalls tradeoff for XGBoost", format='jpg', dpi=300)

    plt.subplot(4, 2, 3)
    fpr, tpr, thresholds = roc_curve(y_test, xgb_clf.predict(X_test))
    plot_roc_curve(fpr, tpr,"XGBoost")

    df = feature_imp(X, xgb_clf)[:35]
    df.set_index('feature', inplace=True)
    df.plot(kind='barh', figsize=(10, 8))
    plt.title('Feature Importance according to XGBoost')
    plt.savefig(f"{address}/Feature Importance according to XGBoost.jpg", format='jpg', dpi=300)

    lgb_clf = LGBMClassifier()
    lgb_clf.fit(X_train, y_train)

    evaluate(lgb_clf, X_train, X_test, y_train, y_test,'LightGBM')

    precisions, recalls, thresholds = precision_recall_curve(y_test, lgb_clf.predict(X_test))
    plt.figure(figsize=(14, 25))
    plt.subplot(4, 2, 1)
    plot_precision_recall_vs_threshold(precisions, recalls, thresholds,"LightGBM")

    plt.subplot(4, 2, 2)
    plt.plot(precisions, recalls)
    plt.xlabel("Precision")
    plt.ylabel("Recall")
    plt.title("PR Curve: precisions/recalls tradeoff for LightGBM")
    plt.savefig(f"{address}/PR Curve tradeoff for LightGBM.jpg", format='jpg', dpi=300)

    plt.subplot(4, 2, 3)
    fpr, tpr, thresholds = roc_curve(y_test, lgb_clf.predict(X_test))
    plot_roc_curve(fpr, tpr,"LGBM")

    scores_dict['LightGBM'] = {
            'Train': roc_auc_score(y_train, lgb_clf.predict(X_train)),
            'Test': roc_auc_score(y_test, lgb_clf.predict(X_test)),
        }


    cb_clf = CatBoostClassifier()
    cb_clf.fit(X_train, y_train, verbose=0)

    evaluate(cb_clf, X_train, X_test, y_train, y_test,'CatBoost')

    precisions, recalls, thresholds = precision_recall_curve(y_test, cb_clf.predict(X_test))
    plt.figure(figsize=(14, 25))
    plt.subplot(4, 2, 1)
    plot_precision_recall_vs_threshold(precisions, recalls, thresholds,"CatBoost")

    plt.subplot(4, 2, 2)
    plt.plot(precisions, recalls)
    plt.xlabel("Precision")
    plt.ylabel("Recall")
    plt.title("PR Curve: precisions/recalls tradeoff for CatBoost")
    plt.savefig(f"{address}/PR Curve tradeoff for CatBoost.jpg", format='jpg', dpi=300)

    plt.subplot(4, 2, 3)
    fpr, tpr, thresholds = roc_curve(y_test, cb_clf.predict(X_test))
    plot_roc_curve(fpr, tpr,"Catboost")

    scores_dict['CatBoost'] = {
            'Train': roc_auc_score(y_train, cb_clf.predict(X_train)),
            'Test': roc_auc_score(y_test, cb_clf.predict(X_test)),
        }


    ab_clf = AdaBoostClassifier()
    ab_clf.fit(X_train, y_train)

    evaluate(ab_clf, X_train, X_test, y_train, y_test,'AdaBoost')

    precisions, recalls, thresholds = precision_recall_curve(y_test, ab_clf.predict(X_test))
    plt.figure(figsize=(14, 25))
    plt.subplot(4, 2, 1)
    plot_precision_recall_vs_threshold(precisions, recalls, thresholds,"AdaBoost")

    plt.subplot(4, 2, 2)
    plt.plot(precisions, recalls)
    plt.xlabel("Precision")
    plt.ylabel("Recall")
    plt.title("PR Curve: precisions/recalls tradeoff for Adaboost")
    plt.savefig(f"{address}/PR Curve tradeoff for Adaboost.jpg", format='jpg', dpi=300)

    plt.subplot(4, 2, 3)
    fpr, tpr, thresholds = roc_curve(y_test, ab_clf.predict(X_test))
    plot_roc_curve(fpr, tpr,"Adaboost")

    scores_dict['AdaBoost'] = {
            'Train': roc_auc_score(y_train, ab_clf.predict(X_train)),
            'Test': roc_auc_score(y_test, ab_clf.predict(X_test)),
        }


    ml_models = {
        'Support Vector Machinegrid':svm_clf,
        'Random Forestgrid':rf_clf,
        
        'Random Forest':rf_clf,
        'XGBoost': xgb_clf, 
        'Logistic Regression': lr_clf,
        'Support Vector Machine': svm_clf,
        'LightGBM': lgb_clf,
        'CatBoost': cb_clf,
        'AdaBoost': ab_clf
    }

    for model in ml_models:
        ml_model_comparsion[model].append(roc_auc_score(y_test, ml_models[model].predict(X_test)))

    plt.figure(figsize=(10, 8))

    # Iterate through each model
    for model_name, model in ml_models.items():
        if hasattr(model, "predict_proba"):  # Check if the model has predict_proba method
            # Predict probabilities for positive class
            y_pred_prob = model.predict_proba(X_test)[:, 1]
        else:
            # For models without predict_proba, use decision_function or predict
            y_pred_prob = model.decision_function(X_test) if hasattr(model, "decision_function") else model.predict(X_test)
        
        # Compute ROC curve
        fpr, tpr, _ = roc_curve(y_test, y_pred_prob)
        
        # Compute AUC score
        auc_score = roc_auc_score(y_test, y_pred_prob)
        ml_model_comparsion[model_name].append(auc_score)
        # Plot ROC curve
        plt.plot(fpr, tpr, label=f'{model_name} (AUC = {auc_score:.3f})')

    plt.plot([0, 1], [0, 1], 'k--')  # Diagonal line for random guessing
    plt.xlabel('False Positive Rate')
    plt.ylabel('True Positive Rate')
    plt.title('Receiver Operating Characteristic (ROC) Curves')
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(f"{address}/ROC.jpg", format='jpg', dpi=300)
    
    print(ml_model_comparsion)
    df = pd.DataFrame.from_dict(ml_model_comparsion)
    print(df)
    new_data = ['Training accuracy', 'Testing accuracy', 'ROC', 'AUC']
    df.insert(loc=0, column='//', value=new_data)

    df.to_csv(f"{address}/Result.csv")




