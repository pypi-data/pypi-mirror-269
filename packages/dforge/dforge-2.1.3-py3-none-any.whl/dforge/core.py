import pandas as pd
import numpy as np
import random
import math
from tabulate import tabulate
from dforge.plotData import CustomPlot
from sklearn.model_selection import StratifiedKFold

class PDBuilder:
    """  A class used to create a Pandas DataFrame with the possibility of reading from a file.
    
    This class provides a convenient way to create Pandas DataFrames by specifying columns and values,
    with the additional feature of automatically recognizing the file extension for reading data from files.
    
    Attributes:
        dataframe (pandas.DataFrame): A Pandas DataFrame containing the data read from file or specified with columns and values.
        
    Methods:
        __init__(filename=None, columns=None, values=None, **kwargs):
            Creates dataframe based on the provided input parameters: filename, columns or values.
            **kwargs are used for passing aditional arguments corresponding to read_file_extention (example: read_csv) to the pandas dataframe function

        generate_id_column(id_type="numeric"):
            Creates id column and populate it with values numeric or hexa.

        show_data(head=None)
            Show first lines of the database corresponding to head number

        add_data(new_data, regenerate_id=False)
            Adds data to the dataframe

        show_columns_name()
            Shows the names of the columns from database
        
        show_columns(columns_name)
            Shows the desired columns corresponding to the given columns_name
        
    Example usage:
        # CreateDataPD object with columns and values
        creator = CreateDataPD(columns=['Name', 'Age'], values=[['Alice', 30], ['Bob', 25]])

        # CreateDataPD object to read data from file
        creator = CreateDataPD(filename='data.csv')

        # Display the Pandas DataFrame
        creator.show_data(head=10) # Shows the first 10 elements of dataframe
        
    """
    def __init__(self, filename=None, columns=None, values=None, **kwargs):
        """
        Initializes the CreateDataPD object with optional parameters.

        Args:
            filename (str): The name of the file to read data from (optional).
            columns (list): A list of column names for the DataFrame (optional).
            values (list of lists): A list of lists representing the values for each row of the DataFrame (optional).
            **kwargs: Used for passing aditional arguments corresponding to read_file_extention (example: read_csv) to the pandas dataframe function
        """

        self.dataframe = None

        if filename:
            self.read_file(filename, **kwargs)
        elif values is not None and columns is not None:
                self.create_dataframe(values, columns, **kwargs)
        else:
            raise ValueError("Either provide a filename to read data from a file, or provide both columns and values to create DataFrame.")

    def read_file(self, filename, **kwargs):
        """ Method for reading file unsing pandas with automatically recognizing the file extension

        Args:
            filename (str): Contains the path and the filename of the database
            **kwargs: Arguments corresponding the specific function to read (example: for read_csv() one argument can be index_col=False)
        """
        file_extension = filename.split('.')[-1].lower()
        supported_extensions = ['csv', 'xlsx', 'xls', 'json', 'parquet', 'feather', 'pickle']
        
        if file_extension in supported_extensions:
            file_extension = 'excel' if file_extension == 'xlsx' or file_extension == 'xls' else file_extension
            read_function = getattr(pd, f"read_{file_extension}")
            self.dataframe = read_function(filename, **kwargs)
        else:
            raise ValueError("Unsupported file extension. Supported extensions are: {}".format(', '.join(supported_extensions)))

    def create_dataframe(self, data, columns, **kwargs):
        """ Method for creating dataframe from specified columns and values given to the constructor.

        Args:
            data (list of lists): A list of lists representing the values for each row of the DataFrame
        """
        if data.any():
            data_dict = {col: [row[i] for row in data] for i, col in enumerate(columns)}
            self.dataframe = pd.DataFrame(data_dict, columns=columns, **kwargs)
        else:
            raise ValueError("Data is empty.")

    def generate_id_column(self, id_type="numeric"):
        """ Method for generating unique id values for data

        Args:
            id_type (str): type of id to generate. Takes as values "numeric" or "hexa"
        """
        if not self.check_id_column():
            self.dataframe.insert(0, "id", None)
        self.generate_id(gen_type=id_type)

    def check_id_column(self, column_name="id"):
        """ Method for checking if id column exists in dataframe

        Args:
            column_name (str): Usually is the "id" column
        """
        return column_name in self.dataframe.columns

    def generate_id(self, gen_type="numeric"):
        """ Method for generating unique identifiers for id column

        Args:
            gen_type (str): The type of identifiers to be generated, numeric or hexa
        """
        if gen_type == "hexa":
            length_required = max(8, math.ceil(math.log(len(self.dataframe), 16)) + 1)
            self.dataframe.loc[self.dataframe["id"].isna(), "id"] = self.generate_unique_hexa_ids(length_required)
        elif gen_type == "numeric":
            length_required = max(7, math.ceil(math.log10(len(self.dataframe))))
            self.dataframe.loc[self.dataframe["id"].isna(), "id"] = self.generate_unique_numeric_ids(length_required)
        else:
            raise AttributeError("Unknown generation id type")

    def generate_unique_numeric_ids(self, length):
        """ Method for generating numeric unique identifiers.

        Args:
            length (int): the length of the identifier based on the number of data from database
        """
        return np.random.randint(10 ** (length - 1), (10 ** length) - 1, size=len(self.dataframe))

    def generate_unique_hexa_ids(self, length):
        """ Method for generating hexadecimal unique identifiers.

        Args:
            length (int): the length of the identifier based on the number of data from database
        """
        return [hex(random.getrandbits(length * 4))[2:] for _ in range(len(self.dataframe))]

    def show_data(self, head=None):
        """ Method for printing the first given (by the head attribute) number of elements in database.

        Args:
            head (int): Number of elements prom the database to be printed
        """
        if head:
            print(self.dataframe.head(head))
        else:
            print(self.dataframe)

    def add_data(self, new_data, regenerate_id=False):
        """ Method for adding new values to the created dataframe.

        Args: 
            new_data (list or list of lists): values to be added
            regenerate_id (bool): regenrate the unique identifiers for the elements in database (Optional)
        """
        new_dataframe = pd.DataFrame(new_data, columns=self.dataframe.columns)
        self.dataframe = pd.concat([self.dataframe, new_dataframe], ignore_index=True)
        if regenerate_id:
            self.dataframe["id"] = None
            self.complete_id_column()

    def show_columns_name(self):
        """ Method for printing the columns names
        """
        print("Columns:", self.dataframe.columns.tolist())

    def show_columns(self, columns_name):
        """ Method for printing the specified columns

        Args: 
            columns_name (str or list of str): Column names to be showing
        """
        print(self.dataframe[columns_name])
    
    def save_data(self, filename, file_extension='csv', **kwargs):
        """ Method for saving dataframe on supported formats.

        Args:
            filename (str): The filename for the saved dataframe.
            file_extention (str): The desired file extension. Supported files: ['csv', 'xlsx', 'xls', 'json', 'parquet', 'feather', 'pickle'].
                Optional. Default = 'csv'
        """
        supported_extensions = ['csv', 'xlsx', 'xls', 'json', 'parquet', 'feather', 'pickle']
        
        if file_extension in supported_extensions:
            file_extension = 'excel' if file_extension == 'xlsx' or file_extension == 'xls' else file_extension
            save_function = getattr(self.dataframe, f"to_{file_extension}")
            save_function(filename, **kwargs)
        else:
            raise ValueError("Unsupported file extension. Supported extensions are: {}".format(', '.join(supported_extensions)))


class PDNumPro(PDBuilder):
    """
    A class for performing numeric analysis on Pandas DataFrames.

    This class extends the functionality of CreateDataPD class and provides additional methods 
    for numeric analysis, data transformation, and visualization.

    Attributes:
        dataframe (pandas.DataFrame): A Pandas DataFrame containing the data to be analyzed.
        dtypes (pandas.DataFrame): A DataFrame containing the data types of each column in the DataFrame.
        minimum_on_columns (dict): A dictionary to store the minimum value for each column. Is generated ony for numeric data. 
        self.maximum_on_columns (dict): A dictionary to store the maximum value for each column. Is generated ony for numeric data. 
        self.dictionary_discretized_data (dict):  A dictionary to store mappings for non-numeric columns to numeric values.

    Methods:
        __init__(*args, **kwargs):
            Initializes the PDNumericAnalysis object with optional parameters.
        
        column_statistics(column_name, **kwargs):
            Computes statistics for a specified column in the DataFrame.
        
        plot_histogram(column_name, **kwargs):
            Plots a histogram for a specified column in the DataFrame.
        
        data_balance(label_column="labels", **kwargs):
            Visualizes the balance of classes in the DataFrame based on a specified label column.
        
        column_standardisation(column_name, range=[0, 1], overwrite=True):
            Standardizes the values of a numeric column to a specified range.
        
        data_standardisation(columns_name, range=[0, 1], overwrite=True):
            Standardizes the values of multiple numeric columns to a specified range.
        
        column_reconstruct(column_name, range=[0, 1], overwrite=True):
            Reconstructs the values of a column from a standardized range to the original range.
        
        data_reconstruction(columns_name, range=[0, 1], overwrite=True):
            Reconstructs the values of multiple columns from standardized ranges to the original ranges.
        
        column_to_numeric_values(column_name, overwrite=True):
            Converts the values of a non-numeric column to numeric values.
        
        non_numeric_columns_to_numeric(overwrite=True):
            Converts all non-numeric columns in the DataFrame to numeric values.
        
        find_non_numeric_columns():
            Finds all non-numeric columns in the DataFrame.
        
        find_numeric_columns():
            Finds all numeric columns in the DataFrame.
        
        extract_numeric_data():
            Extracts numeric data from the DataFrame.
        
        delete_column(columns_name):
            Deletes specified columns from the DataFrame.
        
        create_folds(nr_folds=5, label_column="label"):
            Creates folds for cross-validation based on a specified label column.

    Example usage:
        # Create PDNumericAnalysis object with DataFrame
        analysis = PDNumericAnalysis(dataframe=df)

        # Compute statistics for a column
        stats = analysis.column_statistics(column_name='Age')

        # Plot histogram for a column
        analysis.plot_histogram(column_name='Age')

        # Visualize class balance
        analysis.data_balance(label_column='Class')

        # Standardize numeric columns
        analysis.data_standardisation(columns_name=['Age', 'Height'])

        # Convert non-numeric columns to numeric
        analysis.non_numeric_columns_to_numeric()

        # Delete a column
        analysis.delete_column(columns_name='Weight')

        # Create folds for cross-validation
        analysis.create_folds(nr_folds=5, label_column='Class')
    """
    def __init__(self, filename=None, columns=None, values=None, **kwargs):
        """
        Initializes the PDNumericAnalysis object with optional parameters.

        Args:
            filename (str): The name of the file to read data from (optional).
            columns (list): A list of column names for the DataFrame (optional).
            values (list of lists): A list of lists representing the values for each row of the DataFrame (optional).
            **kwargs: Used for passing aditional arguments corresponding to read_file_extention (example: read_csv) to the pandas dataframe function
        """
        super().__init__(filename=filename, columns=columns, values=values, **kwargs)
        self.dtypes = self.dataframe.dtypes.to_dict()
        self.minimum_on_columns = {}
        self.maximum_on_columns = {}
        self.dictionary_discretized_data = {}

    def column_statistics(self, column_name, **kwargs):
        """ Method for computing statistics of the database on column.

        Args:
            column_name (str): Column for which the statistics are computed
            **kwargs: 
        """
        if not pd.api.types.is_numeric_dtype(self.dataframe[column_name]):
            counts = self.dataframe[column_name].value_counts().to_dict()
            stats_dict = {
                'histogram': {'categories': counts.keys(), 'frequency': counts.values()}
            }
        else:
            bins = kwargs.get("bins", 10)
            hist, bins = np.histogram(self.dataframe[column_name], bins=bins)
            stats_dict = {
                'mean': self.dataframe[column_name].mean(),
                'std': self.dataframe[column_name].std(),
                'minim': self.dataframe[column_name].min(),
                'maxim': self.dataframe[column_name].max(),
                'unique_values': self.dataframe[column_name].unique(),
                'histogram': {'hist': hist, 'bins': bins},
                'None_values': {'nr_values': self.dataframe[column_name].isna().sum(),
                                'idxs': pd.Index(self.dataframe[column_name]).get_indexer_for(self.dataframe[column_name][self.dataframe[column_name].isna()])}
            }
        return stats_dict
    
    def show_numeric_columns_statistics(self, column_names='Numeric'):
        """ Method computing columns statistics and show it in table.

        Args:
            column_names (str or list of str): Default is 'Numeric' and is computing the
                statistics for all numeric columns and show in a table. Can be computed for
                a column as string or for multiple columns as list of strings. If the column
                given is not a numeric one, a warrning will be shown.
        """
        if column_names == 'Numeric':
            column_names = self.find_numeric_columns()  

        statistics = []
        if isinstance(column_names, str):
            column_names = [column_names] 

        if isinstance(column_names, list):
            for column in column_names:
                if pd.api.types.is_numeric_dtype(self.dataframe[column]):
                    columns_statistics = self.column_statistics(column)
                    statistics.append([column, round(columns_statistics['mean'], 2),
                                    round(columns_statistics['std'], 2), 
                                    round(columns_statistics['minim'], 2),
                                    round(columns_statistics['maxim'], 2)])
                else:
                    print(f"\033[93mWarrning: The column '{column}' contains non-numeric data and statistics cannot be computed.\033[0m")
        else:
            raise TypeError("column_names must be either string or list")

        table_header = ['MEAN', 'STD', 'MIN', 'MAX']
        print(tabulate(statistics, headers=table_header, tablefmt='fancy_grid', numalign='right'))

    def plot_histogram(self, column_name, **kwargs):
        """ Method for plotting the histogram of a column

        Args:
            column_name (str): The name of the column to plot hystogram
        """
        plot = CustomPlot(title="Histogram", xlabel="Bins", ylabel="Counts")
        plot.histogram_plot(self.dataframe[column_name], **kwargs)
        plot.show_plot()

    def data_balance(self, label_column="Class", chart_type="pie", **kwargs):
        """ Method for showing the data balance of the classes

        Args:
            label_column (str): The column of dataframe containing the class labels
            chart_type (str): Type of the chart, pie or bar
            **kwargs: Extra arguments for matplotlib.pyplot bar or pie functions and extra arguments for CustomPlot:
                - show_numbers=False (bool): Show values at the top of bar or on pie chart. 
                - map_max_space=1 (float - [0, 1]): Set space for color map.
                - cmap='winter' (str): Color map.
                - percentage=False (bool): Set if given values are percentage. Can be used only if show_numbers=True.
        """
        labels_distribution = self.dataframe[label_column].value_counts(sort=False)
        data_nr = len(self.dataframe[label_column])
        # labels = self.dataframe[label_column].nunique()

        plot = CustomPlot("Class distribution", "", "")
        if chart_type == "bar":
            plot.plot_bar(labels_distribution, label=labels_distribution.index, **kwargs)
        elif chart_type == "pie":
            plot.plot_pie(labels_distribution.values, labels_distribution.index, **kwargs)
        else:
            raise ValueError("Unknown chart type")
        plot.show_plot()

    def column_standardisation(self, column_name, range=[0, 1], overwrite=True):
        """ Method for normalize data in a specified range for a given column.

        Args:
            column_name (str): The column to be standardized
            range (list): The range desired for standardized (Optional)
            overwite (bool): Specifies if the column will be overwrite or will be created a new column coresponding to [column_name]_normalized (Optional)
        """
        minim, maxim = self.dataframe[column_name].min(), self.dataframe[column_name].max()
        if overwrite:
            self.dataframe[column_name] = [(x - minim) * (range[1] - range[0]) / (maxim - minim) + range[0] for x in self.dataframe[column_name]]
        else:
            self.dataframe[f"{column_name}_normalized"] = [(x - minim) * (range[1] - range[0]) / (maxim - minim) + range[0] for x in self.dataframe[column_name]]

        self.minimum_on_columns[column_name] = minim
        self.maximum_on_columns[column_name] = maxim
        return minim, maxim

    def data_standardisation(self, columns_name='All', range=[0,1], overwrite=True):
        """ Method for multiple columns standardisation. Only numeric columns can be standardized.

        Args:
            colums_name (list of str): The names of the column to be standardized
            range (list): The range desired for standatdisation (Optional)
            overwrite (bool): Specifies if the columns will be overwrite or will be created a new column coresponding to [column_name]_normalized (Optional)
        """

        if columns_name == 'All':
            for column_name in self.dataframe.columns:
                if self.is_numeric_column(column_name):
                    self.column_standardisation(column_name, range=range, overwrite=overwrite)
                else:
                    print(f"\033[93mWarrning: The column '{column_name}' contains non-numeric data and cannot be standardized.\033[0m")
        elif columns_name == 'Numeric':
            for column_name in self.find_numeric_columns():
                if self.is_numeric_column(column_name):
                    self.column_standardisation(column_name, range=range, overwrite=overwrite)
                else:
                    print(f"\033[93mWarrning: The column '{column_name}' contains non-numeric data and cannot be standardized.\033[0m")
        else:
            for column_name in columns_name:
                if self.is_numeric_column(column_name):
                    self.column_standardisation(column_name, range=range, overwrite=overwrite)
                else:
                    print(f"\033[93mWarrning: The column '{column_name}' contains non-numeric data and cannot be standardized.\033[0m")

    def column_reconstruct(self, column_name, range=[0,1], overwrite=True):
        """ Method for reconstructing the data after standardization. Only numeric data can be reconstructed.
        If this method is called, miinimum per columns and maximum per columns will be saved for further reconstruction.

        Args:
            column_name (str): Column name to be reconstructed
            range (list): The range desired for standardization (Optional)
            overwite (bool): Specifies if the column will be overwrite or will be created a new column coresponding to [column_name]_reconstructed (Optional)
        """
        if overwrite:
            self.dataframe[column_name] = [(x - range[0]) * (self.maximum_on_columns[column_name] - self.minimum_on_columns[column_name]) / (range[1] - range[0]) + self.minimum_on_columns[column_name] for x in self.dataframe[column_name]]
        else:
            self.dataframe[f"{column_name}_reconstructed"] = [(x - range[0]) * (self.maximum_on_columns[column_name] - self.minimum_on_columns[column_name]) / (range[1] - range[0]) + self.minimum_on_columns[column_name] for x in self.dataframe[column_name]]

    def data_reconstruction(self, columns_name='All', range=[0,1], overwrite=True):
        """ Method for multiple columns reconstruction. Only numeric data can be reconstructed.

        Args:
            colums_name (list of str): The columns to be reconstructed
            range (list): The range of normalized data (Optional)
            overwite (bool): Specifies if the columns will be overwrite or will be created a new column coresponding to [column_name]_reconstructed (Optional)
        """
        if columns_name == 'All':
            for column_name in self.dataframe.columns:
                if self.is_numeric_column(column_name):
                    self.column_reconstruct(column_name, range=range, overwrite=overwrite)
                else:
                    print(f"\033[93mWarrning: The column '{column_name}' contains non-numeric data and cannot be standardized.\033[0m")
        elif columns_name == 'Numeric':
            for column_name in self.find_numeric_columns():
                if self.is_numeric_column(column_name):
                    self.column_reconstruct(column_name, range=range, overwrite=overwrite)
                else:
                    print(f"\033[93mWarrning: The column '{column_name}' contains non-numeric data and cannot be standardized.\033[0m")
        else:
            for column_name in columns_name:
                if self.is_numeric_column(column_name):
                    self.column_reconstruct(column_name, range=range, overwrite=overwrite)
                else:
                    print(f"\033[93mWarrning: The column '{column_name}' contains non-numeric data and cannot be reconstructed.\033[0m")

    def column_to_numeric_values(self, column_name, overwrite=True):
        """ Method for changing nnon-numeric values to numeric values.
        If this method is called, the dictionary will be populated with changes that were made for the column.

        Args:
            column_name (str): The name of the column to be changed to numeric
            overwrite (bool): If True, the column will be overwrite, otherwise, a new column will be creaded with {column_name}_numeric. (Optional)
        """
        unique_values = self.dataframe[column_name].unique()
        self.dictionary_discretized_data[column_name] = {"values": unique_values, "number_values": list(range(len(unique_values)))}
        mapping = {value: index for index, value in enumerate(unique_values)}
        self.dataframe[column_name] = self.dataframe[column_name].map(mapping) if overwrite else self.dataframe[f"{column_name}_numeric"]

    def non_numeric_columns_to_numeric(self, overwrite=True):
        """ Method for changing all the non-numeric columns to numeric ones.

        Args:
            overwrite (bool): If True, the column will be overwrite, otherwise, a new column will be creaded with {column_name}_numeric. (Optional)
        """
        non_numeric_columns = self.find_non_numeric_columns()
        for column in non_numeric_columns:
            self.column_to_numeric_values(column, overwrite=overwrite)

    def find_non_numeric_columns(self):
        """ Method for finding all non-numeric columns from dataframe.
        """
        return [column for column in self.dataframe.columns if not pd.api.types.is_numeric_dtype(self.dataframe[column]) or self.dataframe[column].dtype == bool]

    def find_numeric_columns(self):
        """ Method for finding all numeric columns from dataframe.
        """
        return [column for column in self.dataframe.columns if pd.api.types.is_numeric_dtype(self.dataframe[column]) and self.dataframe[column].dtype != bool]
    
    def is_numeric_column(self, column_name):
        """ Method for testing if a column is numeric.

        Args:
            column_name (str): column name to be tested
        """
        return pd.api.types.is_numeric_dtype(self.dataframe[column_name])

    def extract_numeric_data(self):
        """ Extract all numeric data columns into a numpy array.
        """
        return self.dataframe[self.find_numeric_columns()]

    def delete_column(self, columns_name):
        """ Method for deleting columns.

        Args:
            columns_name (list of strings): The columns name to be deleted.
        """
        self.dataframe.drop(columns_name, axis=1, inplace=True)

    def create_folds(self, nr_folds=5, label_column="label"):
        """ Method for creating folds of database. This method will add a new column to teh dataframe with name 'fold', containing the fold numbers for each element.

        Args:
            nr_folds (int): Number of folds.
            label_column (str): The name of label columns for creating the folds.
        """
        skf = StratifiedKFold(n_splits=nr_folds, shuffle=True, random_state=42) 
        self.dataframe["fold"] = -1  
        for fold, (train_idx, val_idx) in enumerate(skf.split(self.dataframe, self.dataframe[label_column])):
            self.dataframe.loc[val_idx, 'fold'] = fold

        