import numpy as np
import pandas as pd
import plotly.graph_objects as go
from docplex.mp.model import Model
from geopy.distance import geodesic
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def get_cartesian(lat, long):
    """
    Convert latitude and longitude coordinates to Cartesian coordinates.

    Parameters:
    - lat (float): Latitude.
    - long (float): Longitude.

    Returns:
    tuple: Cartesian coordinates (x, y).
    """
    EARTH_RADIUS = 3958.8
    x = EARTH_RADIUS * np.cos(np.deg2rad(lat)) * np.cos(np.deg2rad(long))
    y = EARTH_RADIUS * np.cos(np.deg2rad(lat)) * np.sin(np.deg2rad(long))
    return x, y


def cartesian_distance(elem1, elem2):
    """
    Calculate the Cartesian distance between two points.

    Parameters:
    - elem1 (tuple): Cartesian coordinates of the first point (x1, y1).
    - elem2 (tuple): Cartesian coordinates of the second point (x2, y2).

    Returns:
    float: Cartesian distance between the points.
    """
    x1, y1 = elem1[0], elem1[1]
    x2, y2 = elem2[0], elem2[1]
    distance = ((x1 - x2) ** 2 + (y1 - y2) ** 2) ** 0.5
    return distance


def add_cartesian_coordinates(data):
    """
    Add Cartesian coordinates (X, Y) to a DataFrame based on latitude and longitude.

    Parameters:
    - data (DataFrame): Input DataFrame containing 'Lat' and 'Long' columns.

    Returns:
    DataFrame: Modified DataFrame with 'X' and 'Y' columns added.
    """
    data['X'], data['Y'] = get_cartesian(data['Lat'], data['Long'])
    return data


def create_distance_table(data):
    """
    Create a distance table between elements based on their Cartesian coordinates.

    Parameters:
    - data (DataFrame): Input DataFrame containing 'Name', 'X', and 'Y' columns.

    Returns:
    ndarray: Distance table between elements.
    """
    distances_table = pd.DataFrame(index=data['Name'], columns=data['Name'])
    for i in range(len(data)):
        for j in range(i + 1, len(data)):
            elem1 = data.iloc[i]['Name']
            elem2 = data.iloc[j]['Name']
            coords_elem1 = [data.iloc[i]['X'], data.iloc[i]['Y']]
            coords_elem2 = [data.iloc[j]['X'], data.iloc[j]['Y']]
            distance = cartesian_distance(coords_elem1, coords_elem2)
            distances_table.at[elem1, elem2] = distance
            distances_table.at[elem2, elem1] = distance

    distances_table = distances_table.fillna(0).infer_objects(copy=False).to_numpy()
    return distances_table


def create_binary_var_dict(model, number_elements, number_of_groups):
    """
    Create a dictionary of binary decision variables for group assignments.

    Parameters:
    - model (docplex.mp.model.Model): Optimization model.
    - number_elements (int): Number of elements.
    - number_of_groups (int): Number of groups.

    Returns:
    dict: Dictionary containing binary decision variables.
    """
    return model.binary_var_dict(
        [(i, j) for i in range(1, number_elements + 1) for j in range(1, number_of_groups + 1)], name="X")


def create_continuous_var_dict(model, number_elements):
    """
    Create a dictionary of continuous decision variables.

    Parameters:
    - model (docplex.mp.model.Model): Optimization model.
    - number_elements (int): Number of elements.

    Returns:
    dict: Dictionary containing continuous decision variables.
    """
    return model.continuous_var_dict(
        [(i, i_prime) for i in range(1, number_elements + 1) for i_prime in range(1, number_elements + 1)],
        name="U")


def create_objective_function(model, number_elements, continuous_var_dict, distance_table):
    """
    Create the objective function for the optimization model.

    Parameters:
    - model (docplex.mp.model.Model): Optimization model.
    - number_elements (int): Number of elements.
    - continuous_var_dict (dict): Dictionary containing continuous decision variables.
    - distance_table (ndarray): Distance table between elements.

    Returns:
    docplex.mp.LinearExpr: Objective function.
    """
    return model.sum(continuous_var_dict[(i, i_prime)] * distance_table[i - 1][i_prime - 1] for i in
                     range(1, number_elements + 1) for i_prime in
                     range(1, number_elements + 1)) / 2


def create_results_dict(number_elements, number_of_groups, binary_var_dict):
    """
    Create a dictionary of results from binary decision variables.

    Parameters:
    - number_elements (int): Number of elements.
    - number_of_groups (int): Number of groups.
    - binary_var_dict (dict): Dictionary containing binary decision variables.

    Returns:
    dict: Dictionary containing results.
    """
    results = {}
    for i in range(1, number_elements + 1):
        for j in range(1, number_of_groups + 1):
            results[(i, j)] = binary_var_dict[(i, j)].solution_value
    return results


def distance_between_elements(data, elemA, elemB):
    """
    Calculate the distance between two elements based on their geographical coordinates.

    Parameters:
    - data (DataFrame): DataFrame containing geographical coordinates.
    - elemA (str): Name of the first element.
    - elemB (str): Name of the second element.

    Returns:
    float: Distance between the elements in kilometers.
    """
    elemA_coordinates = (
        data.loc[data['Name'] == elemA, 'Lat'].values[0], data.loc[data['Name'] == elemA, 'Long'].values[0])
    elemB_coordinates = (
        data.loc[data['Name'] == elemB, 'Lat'].values[0], data.loc[data['Name'] == elemB, 'Long'].values[0])
    return round(geodesic(elemA_coordinates, elemB_coordinates).kilometers)


def binary_variable(data, var):
    """
    Convert categorical variable to binary variables.

    Parameters:
    - data (DataFrame): Input DataFrame containing the variable.
    - var (str): Name of the variable.

    Returns:
    ndarray: Array of binary variables.
    """
    columns_to_remove = data.columns.tolist()
    columns_to_remove.remove(var)

    df_var = data.drop(columns=columns_to_remove)

    unique_values = data[var].unique().tolist()
    unique_values.sort()  # Sorting the unique values to ensure consistent ordering

    for value in unique_values:
        df_var[str(value)] = (df_var[var] == value).astype(int)

    df_var.drop(columns=[var], inplace=True)

    return df_var.to_numpy()


def plot_worldmap_with_groups(data, save=False):
    """
    Plot a world map with elements colored by group.

    Parameters:
    - data (DataFrame): DataFrame containing geographical coordinates and group assignments.
    - save (bool): Whether to save the plot as an image.

    Returns:
    None
    """
    fig = go.Figure(go.Scattergeo(
        lat=data['Lat'],
        lon=data['Long'],
        text=data['Name'],
        mode='markers',
        marker_color=data['Group'],
        marker_size=10))

    fig.update_layout(title='Optimized Groups by distance minimization')
    fig.show()

    if save:
        fig.write_image("optimized_groups.png")

    return


def key_performance_indicators(initial_data, data_with_groups):
    """
    Calculate key performance indicators before and after optimization.

    Parameters:
    - initial_data (DataFrame): Initial data before optimization.
    - data_with_groups (DataFrame): Data with group assignments after optimization.

    Returns:
    tuple: Tuple containing KPIs (average_distance_before, average_distance_after, decrease_percentage).
    """
    total_distance_before = 0
    total_distance_after = 0
    total_games_before = 0
    total_games_after = 0
    elements = initial_data['Name'].tolist()

    for i in elements:
        temporary_elements = initial_data['Name'].tolist()
        temporary_elements.pop(elements.index(i))
        for j in temporary_elements:
            if initial_data.loc[initial_data['Name'] == j, 'Group'].values[0] == \
                    initial_data.loc[initial_data['Name'] == i, 'Group'].values[0]:
                total_games_before += 1
                total_distance_before += distance_between_elements(initial_data, i, j) // 2
            if data_with_groups.loc[data_with_groups['Name'] == j, 'Group'].values[0] == \
                    data_with_groups.loc[data_with_groups['Name'] == i, 'Group'].values[0]:
                total_games_after += 1
                total_distance_after += distance_between_elements(data_with_groups, i, j) // 2

    average_distance_before = round(total_distance_before / total_games_before, 2)
    average_distance_after = round(total_distance_after / total_games_after, 2)
    decrease = round(((average_distance_after - average_distance_before) / average_distance_before) * 100, 2)

    return 'Before optimization, the average distance was ', average_distance_before, "After optimization, the average distance would be ", average_distance_after, "This represents an average distance reduction of ", decrease


def read_file(file_path):
    """
    Read a file into a DataFrame based on its format.

    Parameters:
    - file_path (str): Path to the file.

    Returns:
    DataFrame: DataFrame containing the data from the file.

    Raises:
    ValueError: If the file format is not supported.
    """
    file_extension = file_path.split('.')[-1].lower()

    if file_extension == 'csv':
        return pd.read_csv(file_path)
    elif file_extension == 'json':
        return pd.read_json(file_path)
    elif file_extension == 'xml':
        return pd.read_xml(file_path)
    elif file_extension == 'xls' or file_extension == 'xlsx':
        return pd.read_excel(file_path)

    else:
        raise ValueError("Unsupported file format. Only CSV, JSON and Excel formats are currently supported.")


def print_groups(data_with_groups, number_of_groups, number_elements):
    """
    Generate a display of elements grouped by their assigned groups.

    Parameters:
    - data_with_groups (DataFrame): DataFrame containing group assignments for elements.
    - number_of_groups (int): Number of groups.
    - number_elements (int): Total number of elements.

    Returns:
    str: String representation of groups and their elements.
    """
    elements_per_group = number_elements // number_of_groups
    unique_groups = sorted(data_with_groups['Group'].unique())

    group_display = '___________' + '\n'

    for group in unique_groups:
        group_display += (f'  Group {group}  ' + '\n' + '___________' + '\n')
        elements = data_with_groups[data_with_groups['Group'] == group]['Name'].tolist()
        for i in range(0, elements_per_group):
            group_display += (f'{elements[i]}' + '\n')
        group_display += ('___________' + '\n')

    return group_display


def solve_problem(file, number_of_groups, list_var_equal_to_one=None, list_var_maximum_one=None, plot=False, save=False,
                  kpi=False):
    """
    Solve the optimization problem to assign elements to groups.

    Parameters:
    - file (str): Path to the file containing input data.
    - number_of_groups (int): Number of groups to divide the elements into.
    - list_var_equal_to_one (list): List of variables that must have exactly one occurrence in each group.
    - list_var_maximum_one (list): List of variables that must have at most one occurrence in each group.
    - plot (bool): Whether to plot the optimized groups on a world map.
    - save (bool): Whether to save the plot as an image.
    - kpi (bool): Whether to calculate key performance indicators.

    Returns:
    tuple: Tuple containing DataFrame with group assignments, string representation of groups, and KPIs (if calculated).
    """
    data = read_file(file)
    data = add_cartesian_coordinates(data)
    distance_table = create_distance_table(data)
    all_var = list_var_equal_to_one + list_var_maximum_one
    number_elements = data.shape[0]
    initial_dataset = data.copy()

    if number_elements % number_of_groups != 0:
        raise ValueError("The number of elements is not divisible by the number of groups. "
                         "Unable to construct the specified number of groups with the given number of elements.")

    logger.info("Initialization...")

    variable_tables = {}
    for i in range(0, len(all_var)):
        variable_tables[all_var[i]] = binary_variable(data, all_var[i])

    model = Model(name="Optimization by distance minimization")

    binary_var_dict = create_binary_var_dict(model, number_elements, number_of_groups)
    continuous_var_dict = create_continuous_var_dict(model, number_elements)

    objective_function = create_objective_function(model, number_elements, continuous_var_dict, distance_table)
    model.minimize(objective_function)

    if list_var_equal_to_one:
        for i in list_var_equal_to_one:
            for j in range(1, data[i].nunique() + 1):
                for h in range(1, number_of_groups + 1):
                    model.add_constraint(
                        model.sum(binary_var_dict[(k, h)] * variable_tables[i][k - 1][j - 1] for k in
                                  range(1, number_elements + 1)) == 1)

    if list_var_maximum_one:
        for i in list_var_maximum_one:
            for j in range(1, data[i].nunique() + 1):
                for h in range(1, number_of_groups + 1):
                    model.add_constraint(
                        model.sum(binary_var_dict[(k, h)] * variable_tables[i][k - 1][j - 1] for k in
                                  range(1, number_elements + 1)) <= 1)

    for j in range(1, number_of_groups + 1):
        model.add_constraint(model.sum(binary_var_dict[(i, j)] for i in range(1, number_elements + 1)) == 4)

    for i in range(1, number_elements + 1):
        model.add_constraint(model.sum(binary_var_dict[(i, j)] for j in range(1, 9)) == 1)

        for i_prime in range(1, number_elements + 1):
            for j in range(1, number_of_groups + 1):
                model.add_constraint(
                    continuous_var_dict[(i, i_prime)] >= binary_var_dict[(i, j)] + binary_var_dict[(i_prime, j)] - 1)

    logger.info("Model optimization...")
    model.solve()

    elements = data['Name'].tolist()
    results = create_results_dict(number_elements, number_of_groups, binary_var_dict)

    data_with_groups = {'Element': elements, 'Group': [0] * len(elements)}
    for i in range(1, number_elements + 1):
        for j in range(1, number_of_groups + 1):
            if results[(i, j)] == 1:
                data_with_groups['Group'][i - 1] = j

    data_with_groups = pd.DataFrame(data_with_groups)
    data["Group"] = data_with_groups["Group"]

    group_display = print_groups(data_with_groups, number_of_groups, number_elements)

    if plot:
        if save:
            plot_worldmap_with_groups(data, True)
        plot_worldmap_with_groups(data, False)

    if kpi:
        kpis = key_performance_indicators(initial_dataset, data)
        return data_with_groups, group_display, kpis

    return data_with_groups, group_display

