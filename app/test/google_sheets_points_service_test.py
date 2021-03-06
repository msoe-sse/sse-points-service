import unittest
from app.main.points.google_sheets_points_service import parse_first_row, parse_students

class GoogleSheetsPointsServiceTest(unittest.TestCase):
    def test_parse_first_row(self):
        """
        Tests to make sure that the meeting names are parsed correctly
        """
        #Arrange
        cell_values = [["", "General Meeting 1", "General Meeting 2", "General Meeting 3", "TOTALS"]]

        #Act
        result = parse_first_row(cell_values)

        #Assert
        self.assertCountEqual(["General Meeting 1", "General Meeting 2", "General Meeting 3"], result)

    def test_parse_students_basic(self):
        """
        Basic test case for parse students which parses one student
        """
        #Arrange
        cell_values = [["", "General Meeting 1", "General Meeting 2", "General Meeting 3", "TOTALS"],
                       ["Student 1", "1", "1", "1", "3"]]

        #Act
        result = parse_students(cell_values, ["General Meeting 1", "General Meeting 2", "General Meeting 3"])

        #Assert
        self.assertEqual(1, len(result))
        self._assert_student("Student 1", [1, 1, 1], 3, result[0])

    def test_parse_students_sorting(self):
        """
        Test case to make sure that the students are being sorted descending by point total
        """
         #Arrange
        cell_values = [["", "General Meeting 1", "General Meeting 2", "General Meeting 3", "TOTALS"],
                       ["Student 1", "1", "1", "", "2"],
                       ["Student 2", "1", "", "", "1"],
                       ["Student 3", "1", "1", "1", "3"]]

        #Act
        result = parse_students(cell_values, ["General Meeting 1", "General Meeting 2", "General Meeting 3"])

        #Assert
        self.assertEqual(3, len(result))
        self._assert_student("Student 3", [1, 1, 1], 3, result[0])
        self._assert_student("Student 1", [1, 1, 0], 2, result[1])
        self._assert_student("Student 2", [1, 0, 0], 1, result[2])
    
    def test_parse_students_zero_point_total(self):
        #Arrange
        cell_values = [["", "General Meeting 1", "General Meeting 2", "General Meeting 3", "TOTALS"],
                       ["Student 1", "1", "", "", "1"],
                       ["Student 2", "", "", "", "0"],
                       ["Student 3", "", "", "", "0"],
                       ["Student 4", "1", "", "1", "2"]]
        
        #Act
        result = parse_students(cell_values, ["General Meeting 1", "General Meeting 2", "General Meeting 3"])

        #Assert
        self.assertEqual(2, len(result))
        self._assert_student("Student 4", [1, 0, 1], 2, result[0])
        self._assert_student("Student 1", [1, 0, 0], 1, result[1])
    
    def _assert_student(self, name, point_breakdown, point_total, student):
        self.assertEqual(name, student["name"])
        self.assertCountEqual(point_breakdown, student["pointBreakdown"])
        self.assertEqual(point_total, student["pointTotal"])

if __name__ == '__main__':
    unittest.main()