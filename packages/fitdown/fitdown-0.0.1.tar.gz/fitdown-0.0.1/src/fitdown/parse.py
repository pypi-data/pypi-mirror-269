import re
from datetime import datetime

def parse_date(date: str):
    """
    Parses a date string in the format "Month day, year" and returns it in the format "mm/dd/yyyy".

    Args:
        date (str): The date string to be parsed.

    Returns:
        str: The parsed date string in the format "mm/dd/yyyy".

    Raises:
        ValueError: If the date format is not supported. The supported format is 'Month Day, Year' (e.g., 'January 1, 2024').

    Examples:
        >>> parse_date('January 1, 2024')
        '01/01/2024'
    """
    try:
        # TODO: Handle other date formats
        # Attempt to parse the date in the format "Month day, year"
        return datetime.strptime(date, "%B %d, %Y").strftime("%m/%d/%Y")
    except ValueError:
        # Inform the user about the supported date format
        raise ValueError("Date format not supported. Please use the format 'Month Day, Year' (e.g., 'January 1, 2024').")

def parse_exercise(exercise: str):
    """
    Parses the given exercise string and returns it in lowercase.

    Args:
        exercise (str): The exercise string to be parsed.

    Returns:
        str: The parsed exercise string in lowercase.
    """
    return exercise.lower()

def parse_single_line_exercise(line: str, current_date: str):
    """
    Parses a single line exercise and returns a list of exercise sets.

    Args:
        line (str): The input line containing the exercise information.
        current_date (str): The current date.

    Returns:
        list: A list of dictionaries representing each exercise set. Each dictionary contains the following keys:
            - 'date' (str): The date of the workout in the format 'mm/dd/yyyy'.
            - 'exercise' (str): The name of the exercise.
            - 'reps' (int): The number of repetitions.
            - 'weight' (float): The weight lifted.
            - 'unit' (str): The unit of weight ('lb' or 'kg').
            - 'notes' (str): Any additional notes or comments for the exercise set.
    """
    # Match single line exercises
    single_line_match = re.match(r'^([\d]+(?:x\d+)?\s*@\s*[\d.]+\s*(lb|kg)?)\s*([\w\s-]+)$', line)
    if single_line_match:
        sets_reps_weight = single_line_match.group(1)
        unit = single_line_match.group(2)
        exercise = single_line_match.group(3).strip().lower()

        if "x" in sets_reps_weight:
            sets_reps = sets_reps_weight.split("@")[0].strip()
            sets, reps = map(int, sets_reps.split("x"))
        else:
            sets = 1
            reps = int(sets_reps_weight.split("@")[0].strip())

        weight = float(
            sets_reps_weight.split("@")[1].split(unit)[0].strip()
        )

        exercise_set = {
            "date": current_date,
            "exercise": exercise,
            "reps": reps,
            "weight": weight,
            "unit": unit,
            "notes": "",
        }
        return [exercise_set] * int(sets)
    return []


def parse_sets(line: str, current_date: str, current_exercise: str):    
    """
    Parses a line of text representing sets, repetitions, and weight for an exercise.

    Args:
        line (str): The line of text to parse.
        current_date (str): The current date.
        current_exercise (str): The current exercise.

    Returns:
        list: A list of dictionaries representing each exercise set. Each dictionary contains the following keys:
            - 'date' (str): The date of the workout in the format 'mm/dd/yyyy'.
            - 'exercise' (str): The name of the exercise.
            - 'reps' (int): The number of repetitions.
            - 'weight' (float): The weight lifted.
            - 'unit' (str): The unit of weight ('lb' or 'kg').
            - 'notes' (str): Any additional notes or comments for the exercise set.

    Example:
        parse_sets("3x10 @ 100lb Some notes", "2024-01-01", "Squats")
        Output: [{'date': '2024-01-01', 'exercise': 'Squats', 'reps': 10, 'weight': 100.0, 'unit': 'lb', 'notes': 'Some notes'},
                 {'date': '2024-01-01', 'exercise': 'Squats', 'reps': 10, 'weight': 100.0, 'unit': 'lb', 'notes': 'Some notes'},
                 {'date': '2024-01-01', 'exercise': 'Squats', 'reps': 10, 'weight': 100.0, 'unit': 'lb', 'notes': 'Some notes'}]
    """
    
    # Match sets, repetitions, and weight
    set_match = re.match(
        r"^(\d+(?:x\d+)?)\s*@\s*([\d.]+)\s*(lb|kg)\s*(.*)$", line
    )
    if set_match:
        sets_reps = set_match.group(1)
        weight = set_match.group(2)
        unit = set_match.group(3)
        notes = set_match.group(4).strip()

        # Handle 'x' notation for sets and repetitions
        if "x" in sets_reps:
            sets, reps = map(int, sets_reps.split("x"))
        else:
            sets = 1
            reps = int(sets_reps)

        # Append the extracted information to the total_sets list
        exercise_set = {
            "date": current_date,
            "exercise": current_exercise,
            "reps": reps,
            "weight": float(weight),
            "unit": unit,
            "notes": notes,
        }

        return [exercise_set] * int(sets)
    return []

def parse(workout_text):
    """
    Parses the given workout text and extracts the sets, reps, weight, and other information for each exercise.

    Args:
        workout_text (str): The raw text of the workout.

    Returns:
        list: A list of dictionaries representing each exercise set. Each dictionary contains the following keys:
            - 'date' (str): The date of the workout in the format 'mm/dd/yyyy'.
            - 'exercise' (str): The name of the exercise.
            - 'reps' (int): The number of repetitions.
            - 'weight' (float): The weight lifted.
            - 'unit' (str): The unit of weight ('lb' or 'kg').
            - 'notes' (str): Any additional notes or comments for the exercise set.
    """
    total_sets = []
    current_date = None
    current_exercise = None

    # split raw text by on newlines
    for line in workout_text.split("\n"):
        # remove leading and trailing white space
        line = line.strip()
        # skip empty lines
        if not line:
            current_exercise = None
            continue

        # Match workout date
        date_match = re.match(r"^Workout (\w+ \d{1,2}, \d{4})$", line)
        if date_match:
            date_str = date_match.group(1)
            current_date = parse_date(date_str)
            continue

        # Match exercise name
        exercise_match = re.match(r'^(\w[\w\s-]+)$', line)
        # If the line matches the exercise name pattern and there's a current date
        if exercise_match and current_date:
            exercise_str = exercise_match.group(1)
            current_exercise = parse_exercise(exercise_str)
            continue
        
        # Match sets, repetitions, notes, and single line exercises
        if "@" in line and current_date:
            if current_exercise:
                exercise_sets = parse_sets(line, current_date, current_exercise)
            else:
                exercise_sets = parse_single_line_exercise(line, current_date)
            
            total_sets.extend(exercise_sets)

    return total_sets


def main():
    import json

    # Path to the example_workout.md file
    workout_file = "example_workout.md"

    # Read the workout file
    with open(workout_file, "r") as file:
        workout_content = file.read()

    # Parse the workout file
    workout_data = parse(workout_content)

    # Print the parsed workout data
    print(json.dumps(workout_data, indent=4, sort_keys=True))


if __name__ == "__main__":
    main()
