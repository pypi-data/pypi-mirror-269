from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split
from sklearn import datasets

# Load Iris dataset
iris = datasets.load_iris()
X = iris.data
y = iris.target
# Split dataset into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.5, random_state=42)
# Artificial Immune System (AIS) Classifier
class AISClassifier:
    def __init__(self, n_neighbors=10):
        self.knn = KNeighborsClassifier(n_neighbors=n_neighbors)
    def fit(self, X_train, y_train):
        self.knn.fit(X_train, y_train)
    def predict(self, X_test):
        return self.knn.predict(X_test)
# Train AIS classifier
ais_clf = AISClassifier(n_neighbors=10)
ais_clf.fit(X_train, y_train)
# Make predictions
y_pred = ais_clf.predict(X_test)
# Calculate accuracy
accuracy = accuracy_score(y_test, y_pred)
print("Accuracy:", accuracy)
