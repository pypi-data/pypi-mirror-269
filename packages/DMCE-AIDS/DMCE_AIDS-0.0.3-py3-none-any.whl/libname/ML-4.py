import pandas as pd
from sklearn.datasets import load_breast_cancer
from sklearn.model_selection import train_test_split
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report
import seaborn as sns
import matplotlib.pyplot as plt


cancer = load_breast_cancer()
data = pd.DataFrame(cancer.data, columns=cancer.feature_names)
data['diagnosis'] = cancer.target
data.head()
#Output 1
X = data.drop('diagnosis', axis=1)
y = data['diagnosis']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
model = SVC(kernel='linear')
model.fit(X_train, y_train)
y_pred = model.predict(X_test)

print(classification_report(y_test, y_pred))
print(confusion_matrix(y_test, y_pred))
print('Accuracy:', accuracy_score(y_test, y_pred))
#Output 2
cm = confusion_matrix(y_test, y_pred)
sns.set(font_scale =1.5)
def plot_conf_mat (cm) :
    fig,ax = plt.subplots(figsize =(10,6))
    ax = sns.heatmap(cm,annot=True,fmt='d',cbar=False)
    plt.xlabel("True label")
    plt.ylabel("Predicteed label")
    plt.show()
plot_conf_mat(cm)