import unittest
from fitdown.parse import (
    parse_date,
    parse_exercise,
    parse_single_line_exercise,
    parse_sets,
    parse,
)


class TestFitdownParser(unittest.TestCase):

    def test_parse_date_valid_format(self):
        line = "January 1, 2024"
        expected_date = "01/01/2024"
        self.assertEqual(parse_date(line), expected_date)

    def test_parse_date_invalid_format(self):
        line = "Jan 1, 2024"
        with self.assertRaises(ValueError):
            parse_date(line)
    
    def test_parse_date_invalid_format2(self):
        line = "2024-01-01"
        with self.assertRaises(ValueError):
            parse_date(line)
            
    def test_parse_date_no_match(self):
        line = "This is not a workout date"
        with self.assertRaises(ValueError):
            parse_date(line)

    def test_parse_exercise_valid_line(self):
        line = "Push-ups"
        expected_exercise = "push-ups"
        self.assertEqual(parse_exercise(line), expected_exercise)

    def test_parse_single_line_exercise_valid_format(self):
        line = "3x10 @ 50 lb Squat"
        current_date = "01/01/2024"
        expected_result = [
            {
                "date": "01/01/2024",
                "exercise": "squat",
                "reps": 10,
                "weight": 50.0,
                "unit": "lb",
                "notes": "",
            },
            {
                "date": "01/01/2024",
                "exercise": "squat",
                "reps": 10,
                "weight": 50.0,
                "unit": "lb",
                "notes": "",
            },
            {
                "date": "01/01/2024",
                "exercise": "squat",
                "reps": 10,
                "weight": 50.0,
                "unit": "lb",
                "notes": "",
            },
        ]
        self.assertEqual(
            parse_single_line_exercise(line, current_date), expected_result
        )

    def test_parse_single_line_exercise_invalid_format(self):
        line = "Invalid exercise format"
        current_date = "01/01/2024"
        self.assertEqual(parse_single_line_exercise(line, current_date), [])

    def test_parse_sets_valid_format(self):
        line = "3x10 @ 50lb"
        current_date = "01/01/2024"
        current_exercise = "squat"
        expected_result = [
            {
                "date": "01/01/2024",
                "exercise": "squat",
                "reps": 10,
                "weight": 50.0,
                "unit": "lb",
                "notes": "",
            },
            {
                "date": "01/01/2024",
                "exercise": "squat",
                "reps": 10,
                "weight": 50.0,
                "unit": "lb",
                "notes": "",
            },
            {
                "date": "01/01/2024",
                "exercise": "squat",
                "reps": 10,
                "weight": 50.0,
                "unit": "lb",
                "notes": "",
            },
        ]
        self.assertEqual(
            parse_sets(line, current_date, current_exercise), expected_result
        )

    def test_parse_sets_invalid_format(self):
        line = "Invalid set format"
        current_date = "01/01/2024"
        current_exercise = "squat"
        self.assertEqual(parse_sets(line, current_date, current_exercise), [])

    def test_parse_valid_workout_text(self):
        workout_text = "Workout February 26, 2024\n\n5@185lb Deadlift\n\n3x5 @ 35kg Squat\n\nCrunches\n3x20 @ 20lb\n\nHammer Curl\n10 @ 45.5lb each\n10 @ 45.5lb each\n\nBench Press\n10 @ 90lb\n10 @ 90lb\n10 @ 120lb TOUGH"

        expected_result = [
            {
                "date": "02/26/2024",
                "exercise": "deadlift",
                "notes": "",
                "reps": 5,
                "unit": "lb",
                "weight": 185.0,
            },
            {
                "date": "02/26/2024",
                "exercise": "squat",
                "notes": "",
                "reps": 5,
                "unit": "kg",
                "weight": 35.0,
            },
            {
                "date": "02/26/2024",
                "exercise": "squat",
                "notes": "",
                "reps": 5,
                "unit": "kg",
                "weight": 35.0,
            },
            {
                "date": "02/26/2024",
                "exercise": "squat",
                "notes": "",
                "reps": 5,
                "unit": "kg",
                "weight": 35.0,
            },
            {
                "date": "02/26/2024",
                "exercise": "crunches",
                "notes": "",
                "reps": 20,
                "unit": "lb",
                "weight": 20.0,
            },
            {
                "date": "02/26/2024",
                "exercise": "crunches",
                "notes": "",
                "reps": 20,
                "unit": "lb",
                "weight": 20.0,
            },
            {
                "date": "02/26/2024",
                "exercise": "crunches",
                "notes": "",
                "reps": 20,
                "unit": "lb",
                "weight": 20.0,
            },
            {
                "date": "02/26/2024",
                "exercise": "hammer curl",
                "notes": "each",
                "reps": 10,
                "unit": "lb",
                "weight": 45.5,
            },
            {
                "date": "02/26/2024",
                "exercise": "hammer curl",
                "notes": "each",
                "reps": 10,
                "unit": "lb",
                "weight": 45.5,
            },
            {
                "date": "02/26/2024",
                "exercise": "bench press",
                "notes": "",
                "reps": 10,
                "unit": "lb",
                "weight": 90.0,
            },
            {
                "date": "02/26/2024",
                "exercise": "bench press",
                "notes": "",
                "reps": 10,
                "unit": "lb",
                "weight": 90.0,
            },
            {
                "date": "02/26/2024",
                "exercise": "bench press",
                "notes": "TOUGH",
                "reps": 10,
                "unit": "lb",
                "weight": 120.0,
            },
        ]
        self.assertEqual(parse(workout_text), expected_result)

    def test_parse_empty_workout_text(self):
        workout_text = ""
        expected_result = []
        self.assertEqual(parse(workout_text), expected_result)

    def test_parse_workout_text_with_invalid_lines(self):
        workout_text = "Workout January 1, 2024\n\nInvalid line\n\n3x10 @ 50lb Squat\n\nInvalid line"
        expected_result = [
            {
                "date": "01/01/2024",
                "exercise": "squat",
                "reps": 10,
                "weight": 50.0,
                "unit": "lb",
                "notes": "",
            },
            {
                "date": "01/01/2024",
                "exercise": "squat",
                "reps": 10,
                "weight": 50.0,
                "unit": "lb",
                "notes": "",
            },
            {
                "date": "01/01/2024",
                "exercise": "squat",
                "reps": 10,
                "weight": 50.0,
                "unit": "lb",
                "notes": "",
            },
        ]
        self.assertEqual(parse(workout_text), expected_result)


if __name__ == "__main__":
    unittest.main()
