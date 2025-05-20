import unittest
from unittest.mock import patch, mock_open
import io
import avro.schema
from main3 import ResearchDataManager


class TestResearchDataManager(unittest.TestCase):

    def setUp(self):
        # Initialize a ResearchDataManager instance for each test
        self.manager = ResearchDataManager()
        self.manager.set_schema(avro.schema.parse(open("research_data_schema.avsc", "r").read()))

    def test_add_entry(self):
        with patch('builtins.input', side_effect=["Experiment 1", "2024-01-01", "Naleen", "1.2 2.3 3.4"]):
            self.manager.add_entry()
        
        self.assertEqual(len(self.manager.get_entries()), 1)
        entry = self.manager.get_entries()[0]
        self.assertEqual(entry['experiment_name'], "Experiment 1")
        self.assertEqual(entry['date'], "2024-01-01")
        self.assertEqual(entry['researcher'], "Naleen")
        self.assertEqual(entry['data_points'], [1.2, 2.3, 3.4])

    def test_view_entries(self):
        with patch('builtins.input', side_effect=["Experiment 1", "2024-01-01", "Naleen", "1.2 2.3 3.4"]):
            self.manager.add_entry()

        with patch('sys.stdout', new=io.StringIO()) as fake_out:
            self.manager.view_entries()
            output = fake_out.getvalue().strip()
            self.assertIn("Experiment Name: Experiment 1", output)
            self.assertIn("Date: 2024-01-01", output)
            self.assertIn("Researcher: Naleen", output)
            self.assertIn("Data Points: 1.2, 2.3, 3.4", output)

    def test_save_and_load_entries(self):
        entry = {
            'experiment_name': "Experiment 1",
            'date': "2024-01-01",
            'researcher': "Naleen",
            'data_points': [1.2, 2.3, 3.4]
        }
        self.manager.set_entries([entry])

        # Mock open to simulate file operations
        mock_file = mock_open()
        with patch('builtins.open', mock_file):
            self.manager.save_entries_to_file()

        self.manager.set_entries([])  # Clear entries

        # Mock open for loading entries
        encoded_entry = self.manager._ResearchDataManager__encode_base64(b'test_data')
        mock_file = mock_open(read_data=f"{encoded_entry}\n")
        with patch('builtins.open', mock_file):
            with patch('avro.io.DatumReader.read', return_value=entry):
                self.manager.load_entries_from_file()

        self.assertEqual(len(self.manager.get_entries()), 1)
        self.assertEqual(self.manager.get_entries()[0], entry)

    def test_analyze_data(self):
        entry = {
            'experiment_name': "Experiment 1",
            'date': "2024-01-01",
            'researcher': "Naleen",
            'data_points': [1.2, 2.3, 3.4]
        }
        self.manager.set_entries([entry])

        with patch('builtins.input', side_effect=["1"]):
            with patch('sys.stdout', new=io.StringIO()) as fake_out:
                self.manager.analyze_data()
                output = fake_out.getvalue().strip()
                self.assertIn("Average: 2.30", output)
                self.assertIn("Median: 2.30", output)
                self.assertIn("Standard Deviation: 1.10", output)

    def test_delete_entry(self):
        entry = {
            'experiment_name': "Experiment 1",
            'date': "2024-01-01",
            'researcher': "Naleen",
            'data_points': [1.2, 2.3, 3.4]
        }
        self.manager.set_entries([entry])

        with patch('builtins.input', side_effect=["1", "yes"]):
            self.manager.delete_entry()

        self.assertEqual(len(self.manager.get_entries()), 0)

    def test_update_entry(self):
        entry = {
            'experiment_name': "Experiment 1",
            'date': "2024-01-01",
            'researcher': "Naleen",
            'data_points': [1.2, 2.3, 3.4]
        }
        self.manager.set_entries([entry])

        with patch('builtins.input', side_effect=["1", "Experiment 2", "2024-01-02", "Naleen", "4.5 5.6"]):
            self.manager.update_entry()

        updated_entry = self.manager.get_entries()[0]
        self.assertEqual(updated_entry['experiment_name'], "Experiment 2")
        self.assertEqual(updated_entry['date'], "2024-01-02")
        self.assertEqual(updated_entry['researcher'], "Jane Doe")
        self.assertEqual(updated_entry['data_points'], [4.5, 5.6])

if __name__ == '__main__':
    unittest.main()
