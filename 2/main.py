import numpy as np

from utils.basic_operations import load_image, save_image, prepare_image, initialize_directories
from methods.clustering import kmeans
from methods.block_processing import block_processing, METHODS
from methods.scale import scale_NN

CHUNK_SIZE = 8
CLUSTERS = 16

def main():
    initialize_directories()

    file_name = "test.jpg"

    image = prepare_image(load_image(file_name))

    height, width, _ = image.shape

    image = scale_NN(image, scale=0.2)

    image = kmeans(image, CLUSTERS, 20)

    image = scale_NN(image, size=(width, height))

    save_image(image, file_name)

    print("Done!")
    

if __name__ == "__main__":
    main()