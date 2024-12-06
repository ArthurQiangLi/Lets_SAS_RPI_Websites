import matplotlib.pyplot as plt
import os
from csv import reader, DictWriter
from datetime import datetime


def filter_a10_data(file_path, output_dir="logged_data"):
    """
    Filters a10 data by validating rows and ensuring 'arm_clock' is within [600, 1400].
    Saves the filtered data to a new CSV file.

    Args:
        file_path (str): Path to the original a10 CSV file.
        output_dir (str): Directory to save the filtered CSV file. Defaults to "logged_data".

    Returns:
        str: Path to the filtered CSV file.
    """
    # Load the original file and validate rows
    try:
        with open(file_path, "r") as f:
            csv_reader = reader(f)
            headers = next(csv_reader)  # First row as headers
            rows = []
            for row in csv_reader:
                if len(row) == len(headers):  # Validate row length
                    rows.append(row)
    except Exception as e:
        print(f"Error reading file: {e}")
        return None

    # Convert rows to a list of dictionaries for processing
    data = [dict(zip(headers, row)) for row in rows]

    # Filter rows with arm_clock in range [600, 1400]
    filtered_data = []
    for row in data:
        try:
            arm_clock = float(row.get("arm_clock", 0))
            if 600 <= arm_clock <= 1400:
                filtered_data.append(row)
        except ValueError:
            continue  # Skip rows with invalid arm_clock values

    # Save filtered data to a new CSV file
    base_name = os.path.basename(file_path).replace(".csv", "_filtered_conditioned.csv")
    os.makedirs(output_dir, exist_ok=True)
    filtered_file_path = os.path.join(output_dir, base_name)

    with open(filtered_file_path, "w", newline="") as f:
        writer = DictWriter(f, fieldnames=headers)
        writer.writeheader()
        writer.writerows(filtered_data)

    print(f"Filtered data saved to {filtered_file_path}")
    return filtered_file_path


def plot_a10_data(file_path, parameter_groups):
    """
    Plots a10 data based on parameter groups.

    Args:
        file_path (str): Path to the filtered a10 CSV file.
        parameter_groups (dict): Groups of parameters to plot. Example:
            {"plot1": ["cpu", "memory"], "plot2": ["arm_clock"]}.
    """
    # Load the filtered data
    try:
        with open(file_path, "r") as f:
            csv_reader = reader(f)
            headers = next(csv_reader)  # First row as headers
            rows = [dict(zip(headers, row)) for row in csv_reader]
    except Exception as e:
        print(f"Error reading file: {e}")
        return

    # Prepare data for plotting
    timestamps = [datetime.strptime(row["Timestamp"], "%Y-%m-%d %H:%M:%S") for row in rows]
    plot_data = {key: [float(row[key]) for row in rows if key in row] for group in parameter_groups.values() for key in group}

    # Create plots
    num_plots = len(parameter_groups)
    fig, axes = plt.subplots(nrows=num_plots, ncols=1, figsize=(10, 5 * num_plots), sharex=True)
    fig.tight_layout(pad=4.0)

    # Handle single plot case
    if num_plots == 1:
        axes = [axes]

    for idx, (group, params) in enumerate(parameter_groups.items()):
        ax = axes[idx]
        for param in params:
            if param in plot_data:
                ax.plot(timestamps, plot_data[param], label=param)
            else:
                print(f"Warning: '{param}' not found in the data.")

        ax.set_title(group)
        ax.legend()
        ax.grid()

    plt.show()

def plot_a10_data_arrays(filtered_file, parameter_groups2, height=3, width=5):
    """
    Plots a10 data in subplots organized by rows.

    Args:
        filtered_file (str): Path to the filtered a10 CSV file.
        parameter_groups2 (list of lists): Parameters to plot, each sublist corresponds to a row of subplots.
        height (int): Height of each subplot in inches. Defaults to 3.
        width (int): Width of each subplot in inches. Defaults to 5.
    """
    try:
        # Load the filtered data
        with open(filtered_file, "r") as f:
            csv_reader = reader(f)
            headers = next(csv_reader)  # First row as headers
            rows = [dict(zip(headers, row)) for row in csv_reader]
    except Exception as e:
        print(f"Error reading file: {e}")
        return

    # Prepare data for plotting
    timestamps = [datetime.strptime(row["Timestamp"], "%Y-%m-%d %H:%M:%S") for row in rows]
    plot_data = {key: [(row[key]) for row in rows if key in row] for group in parameter_groups2 for key in group}

    # Calculate total number of rows for subplots
    num_rows = len(parameter_groups2)
    fig, axes = plt.subplots(nrows=num_rows, ncols=1, figsize=(width, height * num_rows), sharex=True)
    fig.tight_layout(pad=4.0)

    # Handle single row case (axes becomes a single object, not a list)
    if num_rows == 1:
        axes = [axes]

    # Plot each row of parameters
    for row_idx, params in enumerate(parameter_groups2):
        ax = axes[row_idx]
        for param in params:
            if param in plot_data:
                ax.plot(timestamps, plot_data[param], label=param)
            else:
                print(f"Warning: '{param}' not found in the data.")

        # Set titles and labels
        ax.set_title(f"Row {row_idx + 1} Plot")
        ax.set_ylabel("Values")
        ax.legend()
        ax.grid()

    # Set common x-label for all rows
    axes[-1].set_xlabel("Timestamp")

    plt.show()


def plot_a10_data_4(filtered_file, parameter_groups2, height=3, width=5, title_fontsize=12):
    """
    Plots a10 data in a grid with subplots organized by rows and columns.

    Args:
        filtered_file (str): Path to the filtered a10 CSV file.
        parameter_groups2 (list of lists): Parameters to plot, organized in a grid.
        height (int): Height of each subplot in inches. Defaults to 3.
        width (int): Width of each subplot in inches. Defaults to 5.
    """
    try:
        # Load the filtered data
        with open(filtered_file, "r") as f:
            csv_reader = reader(f)
            headers = next(csv_reader)  # First row as headers
            rows = [dict(zip(headers, row)) for row in csv_reader]
    except Exception as e:
        print(f"Error reading file: {e}")
        return

    # Prepare data for plotting
    timestamps = [datetime.strptime(row["Timestamp"], "%Y-%m-%d %H:%M:%S") for row in rows]
    plot_data = {key: [float(row[key]) for row in rows if key in row] for group in parameter_groups2 for key in group}

    # Calculate grid size
    num_rows = len(parameter_groups2)
    num_cols = len(parameter_groups2[0])

    fig, axes = plt.subplots(nrows=num_rows, ncols=num_cols, figsize=(width * num_cols, height * num_rows), sharex=True)
    fig.tight_layout(pad=4.0)

    # Handle case for single-row or single-column subplots
    if num_rows == 1:
        axes = [axes]
    if num_cols == 1:
        axes = [[ax] for ax in axes]

    # Plot each parameter in its corresponding grid cell
    for row_idx, params_row in enumerate(parameter_groups2):
        for col_idx, param in enumerate(params_row):
            ax = axes[row_idx][col_idx]
            if param in plot_data:
                ax.plot(timestamps, plot_data[param], label=param)
                ax.set_title(param)
                ax.grid()
            else:
                print(f"Warning: '{param}' not found in the data.")
                ax.set_title(f"{param} (Missing)", fontsize=title_fontsize)

    # Set shared x-axis label
    for ax in axes[-1]:  # Last row
        ax.set_xlabel("Timestamp")

    plt.show()

#############################################################################################################################
# Example Usage
DO_WHAT = 4
file_path = "logged_data/2024-12-05_23-08-21_a10.csv"  # Replace with your actual file path
filtered_file = "logged_data/2024-12-05_23-08-21_a10_filtered_conditioned.csv"  # Replace with your actual file path

    # Step 1: Filter data and save it
if (DO_WHAT==1):
    filtered_file = filter_a10_data(file_path)

if (DO_WHAT==2):
    # Step 2: Plot the filtered data (multiple times if needed)
    parameter_groups1 = {
        "plot1": ["cpu", "memory"],
        "plot2": ["arm_clock"],
        "plot3": ["humidity", "cpu_temperature", "total_cpu"],
    }

    if filtered_file:
        plot_a10_data(filtered_file, parameter_groups1)

if (DO_WHAT==3):
    parameter_groups2 = [
        # ["cpu", "total_cpu", "apache2metrics_TotalkBytes"],
        # ["cpu_temperature", "apache2metrics_Load1", "apache2metrics_TotalAccesses"],
        # ["memory", "apache2metrics_Load5", "apache2metrics_DurationPerReq"]
        ["health", "performance"],
        ["no"],
        ["clock"]
    ]

    plot_a10_data_arrays(filtered_file, parameter_groups2, height=3, width=5)

if (DO_WHAT==4):
    parameter_groups2 = [
        ["cpu", "total_cpu", "apache2metrics_TotalkBytes"],
        ["cpu_temperature", "apache2metrics_Load1", "apache2metrics_TotalAccesses"],
        ["memory", "apache2metrics_Load5", "apache2metrics_DurationPerReq"]
    ]

    plot_a10_data_4(filtered_file, parameter_groups2, height=3, width=5, title_fontsize=30)
#############################################################################################################################



