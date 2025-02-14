import numpy as np

def initialize_centroids(flat_array: np.array, k: int) -> np.array:
    final_centroids = []
    while len(final_centroids) < k:
        centroid = flat_array[np.random.choice(flat_array.shape[0])]
        weights = np.linalg.norm(flat_array - centroid, axis=1) # For future me: np.linalg.norm is the same as np.sqrt(np.sum(np.array([test[j][x] ** 2 for x in range(3)])))- in this example...

        weights_sum = np.sum(weights)
        if weights_sum == 0:
            weights = np.ones_like(weights) / len(weights)
        else:
            weights = weights / weights_sum

        index = np.random.choice(flat_array.shape[0], p=weights)
        if not any(np.array_equal(flat_array[index], centroid) for centroid in final_centroids):
            final_centroids.append(flat_array[index])


    return final_centroids

def calculate_centroids(clusters: list) -> np.array:
    return np.array([np.mean(cluster, axis=0) for cluster in clusters])

def kmeans(image: np.array, k: int, max_iterations: int) -> np.array:
    width, height = image.shape[:2] # We need it to revert the image to its original shape later :)
    flat_image = image.reshape(-1, 3)

    centroids = initialize_centroids(flat_image, k)

    print(centroids)
    loop = 0
    converged = False
    while not converged and loop < max_iterations:
        print(f'Loop {loop}')
        loop += 1
        clusters = [[] for _ in range(k)]
        distances = np.linalg.norm(flat_image[:, np.newaxis, :] - centroids, axis=2)
        labels = np.argmin(distances, axis=1)
        clusters = [flat_image[labels == i] for i in range(len(centroids))]

        new_centroids = calculate_centroids(clusters)

        if np.array_equal(centroids, new_centroids):
            converged = True

        centroids = new_centroids
    
    # for i in range(flat_image.shape[0]):
    #     flat_image[i] = centroids[np.argmin(np.linalg.norm(flat_image[i] - centroids, axis=1))]
    flat_image = np.array([centroids[label] for label in labels])

    new_image = flat_image.reshape(width, height, 3)
    new_image = new_image.astype(np.uint8)

    return new_image