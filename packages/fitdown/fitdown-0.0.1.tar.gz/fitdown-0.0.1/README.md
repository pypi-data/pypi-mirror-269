# fitdown-py
Markup language and parser for fitness logs, mainly weightlifting. A superset of [Markdown](https://en.wikipedia.org/wiki/Markdown).

Based off of [fitdown](https://github.com/datavis-tech/fitdown)

The idea is to be able to derive structured data from concise workout notes taken on a smartphone.

## Workout Date
Triggers on the term "Workout" and requires 'Month Day, Year' date format (e.g., 'January 1, 2024'). All exercises that follow a workout date line have that date associated with it.
Example:
```
Workout January 1, 2024'
```

## Exercises with Sets & Reps
Parse a specific exercise and its sets and reps (repititions) with weights using a few different formats. Pounds (`lb`) and kilograms (`kg`) are supported and each exercise should be separated by a blank line.

Formats:
1. Single Line Exercises
2. Multi-line Exercises
3. Exercises with Multiplied Sets & Reps

A parsed exercise is a dictionary with the following keys:
- `date`: The date of the workout in `MM/DD/YYYY` format.
- `exercise`: The name of the exercise.
- `reps`: The number of repetitions.
- `weight`: The weight lifted.
- `unit` (Optional): The unit of weight, either `lb` or `kg`.
- `notes` (Optional): Any notes associated with the exercise.

## Single Line Exercises
Can define an entire exercise on a single line. Notes are not supported in this format. 

`{sets}x{reps}@{weight}{lb|kg} {exercise}`

Example:
```
5@185 Deadlift

5@185lb Deadlift

2x5 @ 35 Squat

2x5 @ 35kg Squat
```

## Multi-line Exercises
Define an exercise and its sets and reps on multiple lines. Notes are supported in this format as shown in the example below, where the second Deadlift set is marked as 'TOUGH'.

```
{exercise}
{sets}x{reps}@{weight}{lb|kg} {notes}
```

Example:
```
Deadlift
5@185

Deadlift
5@185lb

Squat
2x5 @ 35

Squat
5@35kg
5@35kg TOUGH
```

## Example
Here's an example of a workout log in the Fitdown format:

```
Workout February 26, 2024

5@185lb Deadlift

3x5 @ 35kg Squat

Crunches
3x20 @ 20lb 

Hammer Curl
10 @ 45.5lb each
10 @ 45.5lb each

Bench Press
10 @ 90lb 
10 @ 90lb 
10 @ 120lb TOUGH
```

The following elements are parsed:

```
[
    {
        "date": "02/26/2024",
        "exercise": "deadlift",
        "notes": "",
        "reps": 5,
        "unit": "lb",
        "weight": 185.0
    },
    {
        "date": "02/26/2024",
        "exercise": "squat",
        "notes": "",
        "reps": 5,
        "unit": "kg",
        "weight": 35.0
    },
    {
        "date": "02/26/2024",
        "exercise": "squat",
        "notes": "",
        "reps": 5,
        "unit": "kg",
        "weight": 35.0
    },
    {
        "date": "02/26/2024",
        "exercise": "crunches",
        "notes": "",
        "reps": 20,
        "unit": "lb",
        "weight": 20.0
    },
    {
        "date": "02/26/2024",
        "exercise": "crunches",
        "notes": "",
        "reps": 20,
        "unit": "lb",
        "weight": 20.0
    },
    {
        "date": "02/26/2024",
        "exercise": "hammer curl",
        "notes": "each",
        "reps": 10,
        "unit": "lb",
        "weight": 45.5
    },
    {
        "date": "02/26/2024",
        "exercise": "hammer curl",
        "notes": "each",
        "reps": 10,
        "unit": "lb",
        "weight": 45.5
    },
    {
        "date": "02/26/2024",
        "exercise": "bench press",
        "notes": "",
        "reps": 10,
        "unit": "lb",
        "weight": 90.0
    },
    {
        "date": "02/26/2024",
        "exercise": "bench press",
        "notes": "",
        "reps": 10,
        "unit": "lb",
        "weight": 90.0
    },
    {
        "date": "02/26/2024",
        "exercise": "bench press",
        "notes": "TOUGH",
        "reps": 10,
        "unit": "lb",
        "weight": 120.0
    }
]
```

## Acknowledgements

Many thanks to [Datavis Tech INC](https://github.com/datavis-tech) and [curran](https://github.com/curran) for building it in JavaScript and paving the way for me to now use this in my own notes!