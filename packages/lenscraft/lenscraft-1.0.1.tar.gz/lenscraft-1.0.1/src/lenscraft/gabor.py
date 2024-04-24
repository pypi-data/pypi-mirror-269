import cv2
import numpy as np
import shapely
from scipy.spatial.distance import cosine, euclidean
from sklearn.cluster import KMeans

class FeatureMap:
    def __init__(self, features):
        """Features (width x height x features)"""
        self.features = features
        self.normalized = self._normalize(features)
        self.F = features.shape[2]

        print("Create feature map: ", features.shape)

    def get_feature_vector_at(self, x, y):
        # Extract the feature vector for the given pixel
        f = self.normalized[y, x, :]
        
        return f
    
    def get_feature_area(self, x, y, padding=10):
        f = self.normalized[y-padding:y+padding, x-padding:x+padding, :]
        f = f.reshape(((padding*2)**2, self.F))
        return f
    
    def get_polygon_area(self, polygon, sample=None):
        features = []
        # Iterate over the pixels within the bounding box
        minx, miny, maxx, maxy = polygon.bounds
        for y in range(int(miny), int(maxy)):
            for x in range(int(minx), int(maxx)):
                point = shapely.Point(x, y)
                # Check if the point is within the polygon
                if polygon.contains(point):
                    features.append(self.get_feature_vector_at(x, y))
    
        result = np.array(features)
        if sample is not None:
            N = result.shape[0] # Number of features 
            M = min(sample, N) # Requested sample size
            random_indices = np.random.choice(N, M, replace=False)
            result = result[random_indices, :]

        return result

    def all(self):
        h, w = self.normalized.shape[0:2]
        return self.normalized.reshape((w*h, self.F))
    
    def flat_shape(self):
        h, w = self.normalized.shape[0:2]
        return (w, h)
    
    def _normalize(self, features):
        # Compute min and max for each feature across all pixels
        min_vals = np.min(features, axis=(0, 1))
        max_vals = np.max(features, axis=(0, 1))
        
        # Ensure we don't divide by zero if a feature has constant value by setting those to 1
        denom = np.where(max_vals - min_vals != 0, max_vals - min_vals, 1)
        
        # Normalize each feature separately
        normalized = (features - min_vals) / denom
    
        return normalized

class Gabor:
    def __init__(self):
        self.kernels = build_gabor_kernels()

    def apply_gabor_filters(self, img):
        return np.array([cv2.filter2D(img, cv2.CV_32F, k) for k in self.kernels])

    def load_features(self, image_path) -> FeatureMap:
        img = cv2.imread(image_path)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        return self.generate_features(img)

    def generate_features(self, img):
        features = self.apply_gabor_filters(img).transpose((1, 2, 0))

        # Add color info as a feature
        #features = np.concatenate((features, img), axis=0)
        grayscale_feature = np.expand_dims(img, axis=2)
        print("feature shape: ", grayscale_feature.shape, features.shape)
        all_features = np.concatenate((features, grayscale_feature), axis=2)

        return FeatureMap(all_features)


def build_gabor_kernels(ksize=41, sigmas=[11, 21], thetas=np.arange(0, np.pi, np.pi / 4), lambdas=[5, 10, 20], gamma=0.5, psi=0):
    kernels = []
    for theta in thetas:
        for sigma in sigmas:
            for lambd in lambdas:
                kernel = cv2.getGaborKernel((ksize, ksize), sigma, theta, lambd, gamma, psi, ktype=cv2.CV_32F)
                kernels.append(kernel)
    return kernels

def apply_gabor_filters(img, kernels):
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)  # Convert to grayscale if necessary
    feature_vectors = []
    for kernel in kernels:
        filtered = cv2.filter2D(img, cv2.CV_8UC3, kernel)
        feature_vectors.append(filtered.reshape(-1))
    return np.array(feature_vectors).T  # Transpose to make it (num_pixels, num_features)

def apply_gabor_filters(img, kernels):
    # Apply Gabor filters to the image
    feature_maps = np.array([cv2.filter2D(img, cv2.CV_32F, k) for k in kernels])
    return feature_maps

def extract_features(feature_maps, mask):
    # Use the mask to extract features from the ROI
    masked_features = feature_maps[:, mask > 0]  # Apply mask to each feature map
    # You can average (or otherwise pool) the features within the ROI if needed
    roi_features = np.mean(masked_features, axis=1)
    return roi_features

def calculate_cosine_distances(feature_maps, roi_features):
    h, w = feature_maps.shape[1:]  # Height and width of the feature maps
    distances = np.zeros((h, w))
    
    # Iterate over each pixel in the feature maps
    for i in range(h):
        for j in range(w):
            pixel_features = feature_maps[:, i, j]
            # Calculate cosine distance
            #distances[i, j] = cosine(roi_features, pixel_features)
            distances[i, j] = euclidean(roi_features, pixel_features)
    
    
    return distances / np.max(distances)

def gabor_features(image):
    kernels = build_gabor_kernels()
    features = apply_gabor_filters(image, kernels)

    # Add color info as a feature
    features = np.concatenate((features, image), axis=2)

    print(features.shape)
    return FeatureMap(np.transpose(features, (1, 2, 0)))

def hog_features(image):
    if len(image.shape) > 2:
        image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Parameters for HOG
    winSize = (64, 64)  # Size of the detection window
    blockSize = (16, 16)  # Size of a block
    blockStride = (8, 8)  # Block stride
    cellSize = (8, 8)  # Size of a cell
    nbins = 9  # Number of bins for the histograms

    # Create HOG Descriptor object
    hog = cv2.HOGDescriptor(winSize, blockSize, blockStride, cellSize, nbins)

    # Compute HOG features
    # Note: compute() function expects a different image size, so you might need to resize or crop your image accordingly
    hog_features = hog.compute(image)
    
    # Reshape the feature vector to a more manageable size
    features = hog_features.flatten()
    
    return features


def get_features(image, point):
    # Generate Gabor kernels and apply them
    kernels = build_gabor_kernels()
    features = apply_gabor_filters(image, kernels)

    return features[:, point[1], point[0]]

def process_image(image, mask):
    
    image = cv2.GaussianBlur(image, (5,5), 1)

    # Generate Gabor kernels and apply them
    kernels = build_gabor_kernels()
    features = apply_gabor_filters(image, kernels)
    
    # Extract the feature vector from the selected ROI
    roi_features = extract_features(features, mask)

    print(features.shape)
    
    # Calculate cosine distances between the ROI feature vector and all other pixels
    distances = calculate_cosine_distances(features, roi_features)
    print(distances.shape)

    
    return distances

def cluser_features(image, k=3):
    kernels = build_gabor_kernels()
    features = apply_gabor_filters(image, kernels)
    print(features.shape)

    feature_v = np.transpose(features, (1, 2, 0)).reshape((-1, 24))
    print(feature_v.shape)
    # Initialize and fit the K-means model
    kmeans = KMeans(n_clusters=k, random_state=42)
    cluster_labels = kmeans.fit_predict(feature_v)
    segmented_image = cluster_labels.reshape((features.shape[1], features.shape[2]))
    print(segmented_image.shape)
    return segmented_image / np.max(segmented_image)

if __name__ == "__main__":
    image = cv2.cvtColor(cv2.imread("images/spacer_top__3.png"), cv2.COLOR_BGR2GRAY)
    mask = cv2.cvtColor(cv2.imread("images/mask.png"), cv2.COLOR_BGR2GRAY)
    result = process_image(image, mask)

    cv2.imshow("output", result)
    cv2.waitKey()