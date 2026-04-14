from tkinter import *
from tkinter import messagebox
import numpy as np
import pandas as pd
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import accuracy_score

# Define symptoms and skin diseases
l1 = ['itching', 'skin_rash', 'nodal_skin_eruptions', 'continuous_sneezing', 'shivering', 'chills',  'watering_from_eyes']
skin_diseases = ['Fungal infection', 'Allergy']

# Initialize the symptom vector
l2 = [0] * len(l1)

# Load and preprocess the datasets
tr = pd.read_csv("Testing.csv")
df = pd.read_csv("Training.csv")

# Replace prognosis labels with numeric values for skin diseases
replace_dict = {skin_diseases[i]: i for i in range(len(skin_diseases))}
tr.replace({'prognosis': replace_dict}, inplace=True)
df.replace({'prognosis': replace_dict}, inplace=True)

# Filter the datasets to include only relevant skin diseases
tr = tr[tr['prognosis'].isin(replace_dict.values())]
df = df[df['prognosis'].isin(replace_dict.values())]

# Ensure the symptom column names are correct
missing_columns = [col for col in l1 if col not in df.columns]
if missing_columns:
    raise KeyError(f"Columns missing from the dataset: {missing_columns}")

# Prepare the training and testing data
X_test = tr[l1]
y_test = tr["prognosis"]
X = df[l1]
y = df["prognosis"]

# GUI functions
def message():
    if Symptom1.get() == "None" and Symptom2.get() == "None" and Symptom3.get() == "None":
        messagebox.showinfo("OPPS!!", "ENTER SYMPTOMS PLEASE")
    else:
        KNN()

def KNN():
    knn = KNeighborsClassifier(n_neighbors=3)
    knn.fit(X, y)
    y_pred = knn.predict(X_test)
    print("Accuracy:", accuracy_score(y_test, y_pred))

    psymptoms = [Symptom1.get(), Symptom2.get(), Symptom3.get()]
    l2 = [1 if symptom in psymptoms else 0 for symptom in l1]

    inputtest = [l2]
    predict = knn.predict(inputtest)[0]
    result = "No Disease" if predict >= len(skin_diseases) else skin_diseases[predict]
    
    t3.delete("1.0", END)
    t3.insert(END, result)

# GUI setup
root = Tk()
root.title("Skin Disease Prediction From Symptoms")

w2 = Label(root, text="Skin Disease Prediction From Symptoms", font=("Elephant", 30))
w2.grid(row=1, column=0, columnspan=2, padx=100)

Symptom1 = StringVar(value="None")
Symptom2 = StringVar(value="None")
Symptom3 = StringVar(value="None")

Label(root, text="Symptom 1", font=("Elephant", 15)).grid(row=7, column=1, pady=10, sticky=W)
Label(root, text="Symptom 2", font=("Elephant", 15)).grid(row=8, column=1, pady=10, sticky=W)
Label(root, text="Symptom 3", font=("Elephant", 15)).grid(row=9, column=1, pady=10, sticky=W)

OPTIONS = sorted(l1)
OptionMenu(root, Symptom1, *OPTIONS).grid(row=7, column=2)
OptionMenu(root, Symptom2, *OPTIONS).grid(row=8, column=2)
OptionMenu(root, Symptom3, *OPTIONS).grid(row=9, column=2)

Button(root, text="Predict", height=2, width=20, command=message, font=("Elephant", 15)).grid(row=15, column=1, pady=20)

t3 = Text(root, height=2, width=30, font=("Elephant", 20))
t3.grid(row=20, column=1, padx=10)

root.mainloop()
