import pickle
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score, classification_report

class RedBlue:
    def __init__(self):
        self.red = None
        self.blue = None
        self.model = SVC(kernel="rbf")

    def add_red(self, features):
        if self.red is None:
            self.red = features
        else:
            self.red = np.vstack((self.red, features))

    def add_blue(self, features):
        if self.blue is None:
            self.blue = features
        else:
            self.blue = np.vstack((self.blue, features))

    def save(self, name):
        model_path = f"models/{name}.pkl"
        with open(model_path, "wb") as file:
            pickle.dump(self.model, file)

        return model_path

    def train(self):
        # Combine the feature vectors
        X = np.vstack((self.red, self.blue))

        # Create labels (0 for the first set, 1 for the second set)
        y = np.array([0] * len(self.red) + [1] * len(self.blue))

        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.1, random_state=42
        )

        print("Train:", X_train.shape)


        # Train the SVM model
        self.model.fit(X_train, y_train)

        # Predict labels for the test set
        y_pred = self.model.predict(X_test)

        # Calculate the accuracy
        accuracy = accuracy_score(y_test, y_pred)
        print(f"Accuracy: {accuracy:.2f}")

        # Detailed classification report
        print(classification_report(y_test, y_pred))

        # feature_map = features.all()
        # # Predict the class for each pixel's feature vector
        # predictions = model.predict(feature_map)

        # # Reshape the predictions back to the original image shape
        # # Assume `original_image_shape` is a tuple with the shape of the original image (height, width)
        # (w, h) = features.flat_shape()
        # classification_image = predictions.reshape((h, w))

        # # For visualization, scale the classification image to full 8-bit range if it's binary
        # # This step is optional and depends on how you want to visualize the result
        # classification_image_scaled = (classification_image * 255).astype(np.uint8)

        # # Save or display the classification image
        # cv2.imwrite('classification_image.png', classification_image_scaled)
        # dpg.set_value(mask_id, mask_to_data(classification_image))

        print("Done")
        return self.model

        # # To load the model
        # with open('svc_model.pkl', 'rb') as file:
        #     model = pickle.load(file)

