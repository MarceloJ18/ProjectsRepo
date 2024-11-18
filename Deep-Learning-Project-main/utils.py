import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.impute import KNNImputer
from sklearn.cluster import KMeans, AgglomerativeClustering
from sklearn.model_selection import train_test_split
from sklearn.metrics import silhouette_score, confusion_matrix
import cv2


def percentage_calculus(numerator, data):
    denominator = len(data)
    return 100 * numerator/denominator


def train_percentage(data, train, decimal_places=2):
    length_train = len(train)
    percentage = percentage_calculus(length_train, data)
    print('Train represents {}%'.format(round(percentage, decimal_places)))


def missing_values_percentage(data, column, decimal_places=2):
    count = data[column].isna().sum()
    percentage = percentage_calculus(count, data)
    print('Percentage of "{}" missing values: {}%'.format(column, round(percentage, decimal_places)))


def set_plot_properties(ax, x_label, y_label, y_lim=[]):
    """
    Set properties of a plot axis.

    Args:
        ax (matplotlib.axes.Axes): The axis object of the plot.
        x_label (str): The label for the x-axis.
        y_label (str): The label for the y-axis.
        y_lim (list, optional): The limits for the y-axis. Defaults to [].

    Returns:
        None
    """
    ax.set_xlabel(x_label)  # Set the label for the x-axis
    ax.set_ylabel(y_label)  # Set the label for the y-axis
    if len(y_lim) != 0:
        ax.set_ylim(y_lim)  # Set the limits for the y-axis if provided


def plot_bar_chart(ax, data, variable, x_label, y_label='Count', y_lim=[], legend=[], color='cadetblue', annotate=False, top=None):
    """
    Plot a bar chart based on the values of a variable in the given data.

    Args:
        ax (matplotlib.axes.Axes): The axis object of the plot.
        data (pandas.DataFrame): The input data containing the variable.
        variable (str): The name of the variable to plot.
        x_label (str): The label for the x-axis.
        y_label (str, optional): The label for the y-axis. Defaults to 'Count'.
        y_lim (list, optional): The limits for the y-axis. Defaults to [].
        legend (list, optional): The legend labels. Defaults to [].
        color (str, optional): The color of the bars. Defaults to 'cadetblue'.
        annotate (bool, optional): Flag to annotate the bars with their values. Defaults to False.
        top (int or None, optional): The top value for plotting. Defaults to None.

    Returns:
        None
    """
    counts = data[variable].value_counts()[:top] if top else data[variable].value_counts()  # Count the occurrences of each value in the variable
    x = counts.index
    y = counts.values

    ax.bar(x, y, color=color)  # Plot the bar chart with specified color
    ax.set_xticks(x)  # Set the x-axis tick positions
    if len(legend) != 0:
        ax.set_xticklabels(legend)  # Set the x-axis tick labels if provided

    if annotate:
        for i, v in enumerate(y):
            ax.text(i, v, str(v), ha='center', va='bottom', fontsize=12)  # Annotate the bars with their values

    set_plot_properties(ax, x_label, y_label, y_lim)  # Set plot properties using helper function


def knn_imputer_best_k(data, k_min, k_max, weights='distance'):
    """
    Find the best value of K for KNN imputation by evaluating the average silhouette score.

    Args:
        data (pandas.DataFrame): The input data for KNN imputation and clustering.
        k_min (int): The minimum value of K to evaluate.
        k_max (int): The maximum value of K to evaluate.
        weights (str, optional): The weight function used in KNN imputation. Defaults to 'distance'.

    Returns:
        None
    """
    # Define the range of K values to evaluate
    k_values = range(k_min, k_max + 1)

    # Initialize an empty list to store the average silhouette scores
    avg_silhouette_scores = []

    # Iterate over each K value
    for k in k_values:
        # Create the KNN imputer with the current K value
        knn_imputer = KNNImputer(n_neighbors=k, weights=weights)

        # Perform KNN imputation and clustering for each fold in cross-validation
        silhouette_scores = []
        for fold in range(5):  # Adjust the number of folds as needed
            # Split your data into training and test sets
            # Replace the following lines with your actual data splitting code
            X_train, X_test = train_test_split(data, train_size=0.9)

            # Perform KNN imputation on the training and test sets
            X_train_imputed = knn_imputer.fit_transform(X_train)
            X_test_imputed = knn_imputer.transform(X_test)

            # Cluster the imputed data using KMeans or other clustering algorithm
            kmeans = KMeans(n_clusters=k)
            kmeans.fit(X_train_imputed)

            # Evaluate the clustering performance using silhouette score
            labels = kmeans.predict(X_test_imputed)
            silhouette = silhouette_score(X_test_imputed, labels)
            silhouette_scores.append(silhouette)

        # Calculate the average silhouette score for the current K value
        avg_silhouette_score = np.mean(silhouette_scores)
        avg_silhouette_scores.append(avg_silhouette_score)

    # Find the index of the K value with the highest average silhouette score
    best_k_index = np.argmax(avg_silhouette_scores)
    best_k = k_values[best_k_index]

    print('Best K value:', best_k)


# def get_image_dimensions(image_list):
#     """
#     This function prints the largest and smallest dimensions of the images in the list
#     Args:
#         image_list: list of images
#     """
    
#     # List for storing image dimensions
#     largest_width, largest_height = 0, 0
#     smallest_width, smallest_height = float('inf'), float('inf')
    
#     for image in image_list:
#         # Get the width and height of the image
#         height, width, _ = image.shape
    
#         # Update largest and smallest dimensions if necessary
#         largest_width = max(largest_width, width)
#         largest_height = max(largest_height, height)
#         smallest_width = min(smallest_width, width)
#         smallest_height = min(smallest_height, height)
        
#     print("Largest Image : {}x{}".format(largest_width, largest_height))
#     print("Smallest Image : {}x{}".format(smallest_width, smallest_height))


def apply_contrast_enhancement(images_data, size=(45, 60), alpha=1.3, beta=0.5, display=False):
    """
    This function applies contrast enhancement to the images in a dataset.
    Args:
        images_data: list of images
        size: size to which the images should be resized
        alpha: contrast control (1.0 means no change)
        beta: brightness control (0 means no change)
        display: whether to display the images before and after the contrast enhancement
    Returns:
        images_data_processed: numpy array of processed images
    """

    # Lists to store the processed images
    images_data_processed = []

    # Apply contrast enhancement to each image
    for img in images_data:
        # Resize it
        img = cv2.resize(img, size)

        # Apply contrast enhancement
        enhanced_img = cv2.convertScaleAbs(img, alpha=alpha, beta=beta)

        # Append the processed image to the list
        images_data_processed.append(enhanced_img)

    # Convert the processed lists to numpy arrays
    images_data_processed = np.array(images_data_processed)

    # Display first 6 images and compare them with the original images
    if display:
        fig, ax = plt.subplots(1, 6, figsize=(15, 15))
        for i in range(6):
            ax[i].imshow(images_data[i])
            ax[i].set_title("Original Image")
        plt.show()

        fig, ax = plt.subplots(1, 6, figsize=(15, 15))
        for i in range(6):
            ax[i].imshow(images_data_processed[i])
            ax[i].set_title("Contrast Enhanced Image")
        plt.show()

    return images_data_processed
