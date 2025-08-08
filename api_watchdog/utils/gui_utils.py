from tkinter import ttk


def api_selector(frame, values_dict):
    """Create and place an API selector combobox in the given frame.

    Args:
        frame: The tkinter frame where the combobox should be placed.
        values_dict: A dictionary containing API types as keys.

    Returns:
        A ttk.Combobox widget for selecting an API type.
    """
    api_type_label = ttk.Label(frame, text="Select API")
    api_type_label.grid(column=0, row=1)
    api_type = ttk.Combobox(frame, values=list(values_dict.keys()))
    api_type.grid(column=1, row=1)
    return api_type


def interval_selector(frame):
    """Create and place an interval selector combobox in the given frame.

    Args:
        frame: The tkinter frame where the combobox should be placed.

    Returns:
        A ttk.Combobox widget for selecting an interval.
    """
    interval_label = ttk.Label(frame, text="Select Interval")
    interval_label.grid(column=0, row=2)
    interval = ttk.Combobox(
        frame,
        values=[
            "5",
            "10",
            "15",
            "20",
            "25",
            "30",
            "60",
            "120",
            "300",
            "600",
            "1200",
            "1800",
            "3600",
        ],
    )
    interval.grid(column=1, row=2)
    return interval


def log_file_selector(frame):
    """Create and place a log file entry widget in the given frame.

    Args:
        frame: The tkinter frame where the entry widget should be placed.

    Returns:
        A ttk.Entry widget for entering a log file name.
    """
    log_file_label = ttk.Label(frame, text="Select Log File")
    log_file_label.grid(column=0, row=3)
    log_file = ttk.Entry(frame)
    log_file.grid(column=1, row=3)
    return log_file


def select_api_args(frame, api_type, values_dict):
    """Create and place API argument entry widgets in the given frame.

    Args:
        frame: The tkinter frame where the entry widgets should be placed.
        api_type: The type of API to select arguments for.
        values_dict: A dictionary containing API types as keys and their corresponding values.

    Returns:
        A list of ttk.Entry widgets for entering API arguments.
    """
    # Get the list of API class names
    api_class = [x for x in values_dict.keys()]
    # Get the corresponding class variables
    api_var = []
    # Initialize an empty list for the API arguments
    args = []
    # Iterate over the API class names
    for x in api_class:
        # Check if the current API class name matches the given API type
        if x == api_type:
            # If it does, add the corresponding class variable to the list
            api_var.append(values_dict[x].var)
    # Iterate over the class variables
    for x in api_var:
        # Create a label for the API argument
        ttk.Label(frame, text=x).grid(column=0, row=5)
        # Create an entry widget for the API argument
        args.append(ttk.Entry(frame))
        # Place the entry widget at the correct position in the frame
        args[-1].grid(column=1, row=5)
    # Return the list of API argument entry widgets
    return args


def stop_button(frame, command):
    """Create and place a stop button in the given frame.

    Args:
        frame: The tkinter frame where the button should be placed.
        command: The function to be called when the button is clicked.

    Returns:
        A ttk.Button widget for stopping the API monitoring.
    """
    return ttk.Button(frame, text="Stop", command=command).grid(
        column=0, row=7, columnspan=2, pady=5
    )
