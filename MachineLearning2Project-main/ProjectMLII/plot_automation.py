'''
This .py file is to contain all the functions that were created
in the execution of the EDA (automating graphic creation)
'''
#For the visualizations
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.express as px
import squarify

#For the dendrogram creation
from scipy.cluster.hierarchy import dendrogram

#For the clustering
from sklearn.cluster import KMeans, AgglomerativeClustering, DBSCAN, MeanShift
'''
We defined a global color code that will be used thoughout 
the exploration of the datasets
'''
col_code = ['#66d4db',
            '#caf0f2',
            '#969ea7',
            '#d9dde2', 
            '#66b3b8',
            '#66888b', 
            '#66a4a9', 
            '#7dadb0', 
            '#008992']

##################################

#creating a function that will automate the creation of piecharts
def auto_pie(
        series: pd.DataFrame, 
        title: str, 
        legend_title: str, 
        label_top: str, 
        label_bottom: str):
    
    '''
    This function creates a Pie-Chart displaying
    the percentage correspondent to every slice

    Arguments:
  - series(pd.DataFrame): more specifically the variable that
will be analyzed.
  - title(str): The title to display above the chart.
  - legent_title(str): The title to display on top of the
  legend
  - label_top(str): the label of the category to be displayed on top
  - label_bottom(str): the label of the category to be displayed in the bottom
  **Note**: This function is only applicable for variables with
            binary distribution
    
    '''

    # setting the color palette that will be used
    colours = col_code
    
    # creating the pie chart
    fig, ax = plt.subplots()
    ax.pie(series.value_counts(), 
    labels=series.value_counts().index, 
    colors=colours, 
    autopct='%1.2f%%', 
    textprops={'fontsize': 16})
    
    # setting the title and legend
    ax.set_title(title, fontsize=16)
    ax.legend(title=legend_title,
              labels=[label_top, label_bottom],
    loc='upper right')
    
    # removing the y-label
    ax.set_ylabel('')
    
    # displaying the chart
    plt.show()

##################################

#creating a function to automate the creation of bar charts
def auto_bar(series: pd.Series,
             title: str,
             x_axis_label: str,
             y_axis_label: str):

    '''
    This function creates a Pie-Chart displaying
    the percentage correspondent to every slice

    Arguments:
  - series(pd.DataFrame): more specifically the variable that
will be analyzed.
  - title(str): The title to display above the chart.
  - x_axis_label(str): The label to be displayed on the x-axis
  - y_axis_label(str): The label to be displayed on the y-axis

  **Note**: This function is only applicable for variables with
            binary distribution
    
    '''

    # Calculating the value counts for each unique value in the series
    value_counts = series.value_counts()

    # Creating the bar chart
    plt.bar(value_counts.index,
            value_counts.values,
            color='#caf0f2', 
            edgecolor='black',
            linewidth=1.2)

    # Setting the title and axis labels
    plt.title(title, fontsize=16)
    plt.xlabel(x_axis_label, fontsize=12)
    plt.ylabel(y_axis_label, fontsize=12)

    # Displaying the created chart
    plt.show()
    
##########################

def auto_subplots_v1(dataframe,
                     column_names: list):
    
    '''
    This function creates n bar charts
    to display the variation of different variables using subplots
    Arguments:
    - dataframe: more specifically the dataframe where then variables
    to be analyzed arev.
    - column_names(list): A list containing the variables from the 
    above mentioned dataframethat will be analyzed.

    '''

    num_subplots = len(column_names)
    fig, axs = plt.subplots(1, num_subplots)

    # Iterate over column_names to create subplots and bar charts
    for i, column in enumerate(column_names):
        axs[i].bar(dataframe[column].value_counts().index,
                    dataframe[column].value_counts().values,
                    edgecolor='black',
                    color='#caf0f2')
        
        # Set x-axis label, y-axis label, and title for each subplot
        axs[i].set_xlabel(column)
        axs[i].set_ylabel('Frequency')
        axs[i].set_title(f'Distribution of {column}')

    # Adjust the spacing between subplots
    plt.tight_layout()

    # Show the plot
    plt.show()

##########################

def auto_subplots_v2(dataframe):
    '''
    This function creates histograms for each lifetime_spend variable using subplots.

    Arguments:
        - dataframe: The DataFrame where the lifetime_spend variables are.
    '''

    # Storing all lifetime_spend columns in a single list
    lifetime_spend_columns = [col for col in dataframe.columns if col.startswith('lifetime_spend')]

    num_subplots = len(lifetime_spend_columns)
    fig, axs = plt.subplots(3, 3)

    # Flatten the subplots array for easier iteration
    axs = axs.flatten()

    # Create histograms for each subplot
    for i, (col, ax) in enumerate(zip(lifetime_spend_columns, axs)):
        # Get the data for the current column
        column_data = dataframe[col]

        # Create the histogram
        ax.hist(column_data,
                bins='auto',
                alpha=0.5,
                edgecolor='black',
                color='#66d4db')

        # Set subplot title as column name (excluding 'lifetime_spend' prefix)
        ax.set_title(col[15:])

        # Remove the x and y axis labels
        ax.set_xlabel('')
        ax.set_ylabel('')

    # Add a main title to the plot
    fig.suptitle('Lifetime expenditure per category', fontsize=16)

    # Adjust the spacing between subplots
    fig.tight_layout()

    # Show the plot
    plt.show()

##################################

def auto_boxplot(dataframe, x_column, y_column, x_labels=None):
    '''
    This function creates a boxplot for the specified columns of a DataFrame.

    Arguments:
        - dataframe: The DataFrame containing the data to be plotted.
        - x_column: The column name to be used for grouping on the x-axis.
        - y_column: The column name to be used for the y-axis.
        - x_labels (optional): Labels to be used for the x-axis tick marks.
    '''

    # Creating the boxplot
    dataframe[[y_column, x_column]].boxplot(by=x_column)
    
    # Removing the gridlines from the boxplot
    plt.grid(visible=None)

    # Setting the title for the boxplot
    plt.title(f"{y_column} per {x_column}")

    # Setting the label for the x-axis
    plt.xlabel(x_column, fontsize=12)

    # Setting the label for the y-axis
    plt.ylabel(y_column, fontsize=12)

    # Setting x-axis tick labels if provided
    if x_labels:
        plt.xticks(np.arange(len(x_labels)) + 1, labels=x_labels)

    # Displaying the boxplot
    plt.show()

##################################

def plot_total_spends(dataframe):

    '''
      This function creates a treemap comparing
      various categories of a dataframe

       Arguments:
    - dataframe: more specifically the dataframe that
    contains the categories that will be analyzed.
    '''

    # Create the dictionary with category names and corresponding totals
    all_spends = {
        'Groceries': dataframe['lifetime_spend_groceries'].sum(),
        'Vegetables': dataframe['lifetime_spend_vegetables'].sum(),
        'Non-Alcoholic Drinks': dataframe['lifetime_spend_nonalcohol_drinks'].sum(),
        'Alcoholic Drinks': dataframe['lifetime_spend_alcohol_drinks'].sum(),
        'Meat': dataframe['lifetime_spend_meat'].sum(),
        'Fish': dataframe['lifetime_spend_fish'].sum(),
        'Hygiene': dataframe['lifetime_spend_hygiene'].sum(),
        'Tech': dataframe['lifetime_spend_tech'].sum()
    }

    # Create a list of labels with values and percentages
    labels = [f"{k} \n ({v:,} € - {100*v/sum(all_spends.values()):.2f}%)" for k, v in all_spends.items()]

    # Plot the treemap using Squarify
    squarify.plot(sizes=all_spends.values(), label=labels, color=col_code, text_kwargs={'fontsize': 10}, edgecolor='black')

    # Remove the axis
    plt.axis('off')
    # Add a title
    plt.title('Total Money Spent per Category')
    # Display the plot
    plt.show()


##################################
#creating a function to automate the creation of line plots
def auto_lineplot(series: pd.Series):

    '''
      This function creates a Line Plot
      to display the hourly variation of a variable

      Arguments:
      - series(pd.DataFrame): more specifically the variable that
      will be analyzed.
      
    '''

    # Calculate the hourly variation of customers
    hourly_counts = series.value_counts().sort_index()

    # Plot the hourly variation using a line plot
    plt.plot(hourly_counts.index, hourly_counts.values, marker='o', color='#66d4db')

    # Fill the area below the line plot
    plt.fill_between(hourly_counts.index, hourly_counts.values, color='#66d4db', alpha=0.25)

    # Add a title to the graph
    plt.title('Customer Count per Hour')

    # Label the x and y axes
    plt.xlabel('Hour')
    plt.ylabel('Count')

    # Set the x-axis tick labels to match the hourly values
    plt.xticks(hourly_counts.index)

    # Add dotted lines connecting each data point to the x-axis
    for hour, count in zip(hourly_counts.index, hourly_counts.values):
        plt.plot([hour, hour], [0, count], color='gray', linestyle=(0, (1, 5)))

    # Display the plot
    plt.show()


##################################

def auto_map(dataframe):

  '''
    This function creates a map to display
    thge geographical distribution of observations

    Arguments:
    - dataframe: more specifically the dataframe that
    contains the observations that will be analyzed.
      
    '''
  
  #Set the Mapbox access token
  px.set_mapbox_access_token('pk.eyJ1IjoiZGFuaWVsa3J1ayIsImEiOiJjbGhydTR0ZmcwaXlkM2lvYXF6NTF3d3BsIn0.TPV8oY0m4z7Cucv-Dun7-g')

  #Create a scatter mapbox chart
  fig = px.scatter_mapbox(dataframe,
                          lat=dataframe['latitude'],  # Specify the latitude column for locations
                          lon=dataframe['longitude'],  # Specify the longitude column for locations
                          color='customer_type',  # Color the markers based on customer_type column
                          color_discrete_map={'Supermarket': '#66d4db', 'Human Client': 'purple'},  # Assign custom colors for each variant
                          hover_data=['customer_name'],  # Display customer_name on hover
                          zoom=9.5)  # Set the initial zoom level

  #Update the layout to remove margins
  fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})

  #Display the chart
  fig.show()

  import matplotlib.pyplot as plt

def plot_total_amounts_bars(dataframe):

    '''
      This function creates a bar chart comparing
      various categories of a dataframe

       Arguments:
    - dataframe: more specifically the dataframe that
    contains the observations that will be analyzed.
    '''

    # Calculate the totals for each category
    total_groceries = dataframe['lifetime_spend_groceries'].sum()
    total_electronics = dataframe['lifetime_spend_electronics'].sum()
    total_vegetables = dataframe['lifetime_spend_vegetables'].sum()
    total_non_alcohol_drinks = dataframe['lifetime_spend_nonalcohol_drinks'].sum()
    total_alcohol_drinks = dataframe['lifetime_spend_alcohol_drinks'].sum()
    total_meat = dataframe['lifetime_spend_meat'].sum()
    total_fish = dataframe['lifetime_spend_fish'].sum()
    total_hygiene = dataframe['lifetime_spend_hygiene'].sum()

    # Create a list of variable names and their corresponding totals
    variables = ['Groceries',
                 'Electronics',
                 'Vegetables',
                 'Non-Alcohol Drinks',
                 'Alcohol Drinks',
                 'Meat',
                 'Fish',
                 'Hygiene']

    totals = [total_groceries,
              total_electronics,
              total_vegetables,
              total_non_alcohol_drinks,
              total_alcohol_drinks,
              total_meat,
              total_fish,
              total_hygiene]

    # Create a bar chart
    plt.bar(variables,
            totals,
            color=col_code,
            edgecolor='black',
            linewidth=1.2)

    plt.xlabel('Variables')
    plt.ylabel('Total Amount (Log Scale)')
    plt.yscale('log')  # Set the y-axis scale to logarithmic
    plt.title('Total Amount Spent per Category by the Supermarkets')

    # Display the chart
    plt.show()

##################################

def auto_umap(cluster: list,
              umap_rep: object):
  '''
  Automatically does the UMAP representation with the cluster label chosen
  Parameters:
    - cluster (list): the list with the labels of the clusters
    - umap_rep (object): indicates which umap is to be utilized
  '''
  plt.scatter(umap_rep[:, 0], umap_rep[:, 1], 
            c=cluster, cmap=plt.cm.tab10)
  plt.colorbar(label='Cluster')

  plt.show()

##################################

def plot_dendrogram(model, **kwargs):
    # Create linkage matrix and then plot the dendrogram

    # create the counts of samples under each node
    counts = np.zeros(model.children_.shape[0])
    n_samples = len(model.labels_)
    for i, merge in enumerate(model.children_):
        current_count = 0
        for child_idx in merge:
            if child_idx < n_samples:
                current_count += 1  # leaf node
            else:
                current_count += counts[child_idx - n_samples]
        counts[i] = current_count

    linkage_matrix = np.column_stack(
        [model.children_, model.distances_, counts]
    ).astype(float)

    # Plot the corresponding dendrogram
    dendrogram(linkage_matrix, **kwargs)

##################################

def plot_hierarchical_dendrogram(linkage, distance_threshold, n_clusters=None, title='Dendogram', truncate_mode=None, p=None, line=None):
    """
    Plot a hierarchical clustering dendrogram with optional line.

    Args:
        linkage (str): The linkage criterion for the hierarchical clustering.
        distance_threshold (float): The distance threshold for forming flat clusters.
        n_clusters (int or None, optional): The number of clusters to find. If None, flat clusters are formed.
        title (str): The title of the dendrogram plot.
        truncate_mode (str or None, optional): The truncation mode for the dendrogram plot. Default is None.
        p (int or None, optional): The number of levels to show in the dendrogram plot when truncate_mode='level'. Default is None.
        line (float or None, optional): The y-coordinate for drawing a horizontal line on the dendrogram plot. Default is None.
    """
    hierarchical_solution = AgglomerativeClustering(
        linkage=linkage, distance_threshold=distance_threshold, n_clusters=n_clusters
    ).fit(customer_info_pca)

    fig, ax = plt.subplots()
    plt.title(title)
    plot_dendrogram(hierarchical_solution, truncate_mode=truncate_mode, p=p)
    if line is not None:
        plt.axhline(y=line, color='r', linestyle='-')
    plt.show()

