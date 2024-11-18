import matplotlib.pyplot as plt
from plot_automation import col_code
import pandas as pd
import numpy as np
from mlxtend.preprocessing import TransactionEncoder
from mlxtend.frequent_patterns import apriori, association_rules
import multiprocessing as mp
from sklearn.model_selection import train_test_split
from sklearn.metrics import silhouette_score, confusion_matrix
from sklearn.cluster import AgglomerativeClustering


### Customer Segmentation utils

def combine_cluster_results(cluster1, cluster2, cluster1_name='K-means', cluster2_name='Hierarchical'):
    # Create the confusion matrix
    confusion = confusion_matrix(cluster1, cluster2)

    # Determine the range for the columns based on the cluster with the highest number of unique values
    max_unique_values = max(len(np.unique(cluster1)), len(np.unique(cluster2)))

    # Create the index and column labels based on the maximum number of unique values
    index_labels = ['{} {}'.format(cluster1_name, i) for i in range(max_unique_values)]
    column_labels = ['{} {}'.format(cluster2_name, i) for i in range(max_unique_values)]

    # Create a DataFrame with the confusion matrix, specifying the index and column labels
    confusion_df = pd.DataFrame(confusion, index=index_labels, columns=column_labels)

    # Filter out rows and columns filled with zeros
    confusion_df = confusion_df.loc[(confusion_df != 0).any(axis=1), (confusion_df != 0).any(axis=0)]

    return confusion_df


# Grid search for the parameters of algorithms in Customer Segmentation
def find_best_params(run_loops, algorithm, param_values, **kwargs):
    best_silhouette = -1
    best_params = {}

    if run_loops:
        for params in param_values:
            # Create clustering instance with current parameter values
            clustering = algorithm(**params, **kwargs)

            # Fit the clustering model to the data
            clustering.fit(customer_info_pca)

            # Check if the model created any clusters
            n_clusters = len(set(clustering.labels_)) - (1 if -1 in clustering.labels_ else 0)
            if n_clusters > 1:
                # Calculate the silhouette score
                current_silhouette_score = silhouette_score(customer_info_pca, clustering.labels_)

                # Check if the current parameter combination yields a better silhouette score
                if current_silhouette_score > best_silhouette:
                    best_silhouette = current_silhouette_score
                    best_params = params

        # Print the best parameter combination
        print("Best parameter combination:", best_params)


def run_clustering(linkage_methods: list, n_clusters_range, data: pd.DataFrame, run_loops=True):
    """
    Run Agglomerative Clustering with different linkage methods and number of clusters.

    Args:
        linkage_methods (list): List of linkage methods to test.
        n_clusters_range (range): Range of number of clusters to test.
        data (pd.DataFrame): PCA data for clustering.
        run_loops (bool, optional): Whether to run the clustering and result printing loops. Default is True.
    """
    results = {}

    if run_loops:
        for linkage_method in linkage_methods:
            for n_clusters in n_clusters_range:
                model = AgglomerativeClustering(n_clusters=n_clusters, linkage=linkage_method)
                model.fit(data)
                score = silhouette_score(data, model.labels_)

                if linkage_method not in results:
                    results[linkage_method] = {}
                results[linkage_method][n_clusters] = score

        for linkage_method in linkage_methods:
            print(f"Results for linkage method '{linkage_method}':")
            for n_clusters in n_clusters_range:
                score = results[linkage_method][n_clusters]
                print(f"\t{n_clusters} clusters: silhouette score = {score:.4f}")


#################
### Association Rules utils


def cluster_train_test_split(data, clustering='cluster_hdbscan', test_size=0.3, random_state=None):
    """
    Split clustered data into training and testing sets, ensuring even distribution across clusters.

    Parameters:
        data (pd.DataFrame): The data to be split.
        clustering (string): Name of the cluster column.
        test_size (float or int, optional): The desired ratio or absolute number of samples for the testing set.
            Defaults to 0.3 (30% of the data).
        random_state (int or RandomState, optional): Seed or random number generator state for reproducible output.
            Defaults to 0.

    Returns:
        X_train (pd.Dataframe): The training set.
        X_test (pd.Dataframe): The testing set.
    """
    print('Splitting data into training and testing sets...')
    cluster_names = data[clustering].unique()

    # Initialise empty arrays for training and testing sets
    X_train = pd.DataFrame()
    X_test = pd.DataFrame()

    # Iterate over each cluster
    for cluster in cluster_names:
        # Get the indices of samples belonging to the current cluster
        clustered_data = data[data[clustering] == cluster]

        # Perform train-test split for the current cluster
        X_cluster_train, X_cluster_test = train_test_split(clustered_data, test_size=test_size,
                                                           random_state=random_state)

        # Add the split data to the training and testing sets
        X_train = pd.concat([X_train, X_cluster_train])
        X_test = pd.concat([X_test, X_cluster_test])

    print('Done!')
    return X_train, X_test


def visualise_cluster(dataframe, cluster_column, x_column=None):
    """
    Visualise either the count values of the cluster column or the values of a specific column (X)
    grouped by the cluster column.

    Args:
        dataframe (pandas.DataFrame): The input DataFrame containing the data.
        cluster_column (str): The name of the column representing the clusters.
        x_column (str, optional): The name of the column for which values are calculated.
            If None, the function will plot the count values of the cluster column.
            If specified, the function will count the number of X values per cluster. Default is None.

    Returns:
        None (displays a bar plot)

    Raises:
        ValueError: If either the cluster_column or x_column does not exist in the dataframe.
    """
    if x_column is None:
        # Calculate cluster sizes
        cluster_sizes = dataframe[cluster_column].value_counts()

        # Create a bar plot to visualize cluster sizes
        plt.figure(figsize=(10, 6))
        ax = cluster_sizes.plot(kind='bar',
                                color=[col_code[i % len(col_code)] for i in range(len(cluster_sizes.index))])
        plt.xlabel('Cluster')
        plt.ylabel('Cluster Size')
        plt.title('Cluster Sizes')

        # Add values to the bar plot
        for i, v in enumerate(cluster_sizes):
            ax.text(i, v, str(v), ha='center', va='bottom')

        # Remove grid
        plt.grid(False)

        plt.show()

    else:
        # Count the number of x_column values per cluster
        x_count = dataframe.groupby(cluster_column)[x_column].nunique()

        # Create a bar plot to visualize x_column counts
        plt.figure(figsize=(10, 6))
        ax = x_count.plot(kind='bar', color=[col_code[i % len(col_code)] for i in range(len(x_count.index))])
        plt.xlabel('Cluster')
        plt.ylabel(f'{x_column} Count')
        plt.title(f'{x_column} Counts per Cluster')

        # Add values to the bar plot
        for i, v in enumerate(x_count):
            ax.text(i, v, str(v), ha='center', va='bottom')

        # Remove grid
        plt.grid(False)
        plt.show()


def analyse_clusters(X_train, X_test=None, timeout=20):
    """
    Analyses clusters and calculates the average difference in lift between X_train and X_test (if provided).

    Parameters:
        X_train (pd.DataFrame): Training data.
        X_test (pd.DataFrame, optional): Test data. Defaults to None.
        timeout (int): Timeout in seconds for calculating the average difference in lift. Defaults to 20.

    """
    print('Analysing clusters...')
    # Find the number of clusters and cluster names
    clustering = 'cluster_hdbscan'
    cluster_names = X_train[clustering].unique()

    # Iterate over each cluster
    for cluster_idx in range(len(cluster_names)):
        # Extract the name of the current cluster
        cluster = cluster_names[cluster_idx]

        print(f"\nAnalysing cluster {cluster}...")
        # Extract the transactions for the current cluster
        cluster_transactions_train = X_train[X_train[clustering] == cluster]['list_of_goods']

        # Encoding the training transactions for the current cluster
        te = TransactionEncoder()
        te_ary = te.fit(cluster_transactions_train).transform(cluster_transactions_train)
        df_train = pd.DataFrame(te_ary, columns=te.columns_)

        # Applying Apriori algorithm to find frequent itemsets for the current cluster
        frequent_itemsets = apriori(df_train, min_support=0.01, use_colnames=True)

        # Generating association rules for the current cluster
        rules = association_rules(frequent_itemsets, metric="lift", min_threshold=1.1)

        # Filter rules based on additional criteria
        valid_rules = rules[
            (rules['confidence'] >= 0.5)
        ]

        # Print or process the association rules for the current cluster
        print(f"Cluster {cluster} Association Rules:")
        display(valid_rules.sort_values(by='lift', ascending=False))

        if X_test is not None:
            print(f"Calculating average difference in lift for cluster {cluster}...")
            # Extract the transactions for the current cluster
            cluster_transactions_test = X_test[X_test[clustering] == cluster]['list_of_goods']

            # Encoding the test transactions for the current cluster
            te_test = te.fit(cluster_transactions_test).transform(cluster_transactions_test)
            df_test = pd.DataFrame(te_test, columns=te.columns_)

            if timeout is None:
                # Calculate the average difference in lift without timeout
                average_difference = calculate_difference(df_test, valid_rules)
            else:
                # Calculate the average difference in lift with timeout
                pool = mp.Pool(processes=1)
                result = pool.apply_async(calculate_difference, args=(df_test, valid_rules))
                try:
                    average_difference = result.get(timeout)
                except mp.TimeoutError:
                    average_difference = "Took too long"

            print('Average difference in lift:', average_difference)


def calculate_difference(X_test, valid_rules):
    # Applying Apriori algorithm to find frequent itemsets for the current cluster
    frequent_itemsets_test = apriori(X_test, min_support=0.01, use_colnames=True)

    # Generating association rules for the current cluster
    rules_test = association_rules(frequent_itemsets_test, metric="lift", min_threshold=1.1)

    # Filter rules based on additional criteria
    valid_rules_test = rules_test[
        (rules_test['confidence'] >= 0.5)
    ]

    valid_rules_test = valid_rules_test[['antecedents', 'consequents', 'lift']]
    valid_rules_test.columns = ['antecedents', 'consequents', 'lift_test']

    evaluation = valid_rules.merge(
        valid_rules_test,
        on=['antecedents', 'consequents']
    )
    return round(np.abs(evaluation['lift'] - evaluation['lift_test']).mean(), 2)
