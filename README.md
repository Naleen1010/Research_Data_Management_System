# Experimental Data Management System

## Overview
This Python-based project provides a modular application for managing and analyzing experimental data. The system allows users to add, update, delete, and analyze experimental records with various statistical measures including average, standard deviation, and correlation analysis.

## Features
- **Data Management**
  - Add new experiment entries
  - Update existing entries
  - Delete existing entries
- **Statistical Analysis**
  - Calculate averages
  - Compute standard deviations
  - Perform correlation analysis
- **Modular Design**
  - Separate scripts for different functionalities
  - Enhanced maintainability and testability
- **Error Handling**
  - Graceful error management
  - Meaningful error messages

## File Structure
The project consists of the following Python scripts:

- `main1.py`: Core functionality and user interactions
- `main2.py`: Additional data processing features
- `main3.py`: Advanced analysis capabilities
- `main4.py`: Extended functionalities
- `unit_test.py`: Contains unit tests for verifying the functionality of all main scripts

## Prerequisites
- Python 3.x or higher
- Required libraries (install using pip):
  ```
  pip install -r requirements.txt
  ```

## Installation
1. Clone or download this repository
2. Navigate to the project directory
3. Install required dependencies:
   ```
   pip install -r requirements.txt
   ```

## Usage
Each script can be run independently based on the functionality required:

```bash
python main1.py  # For core functionality
python main2.py  # For data processing features
python main3.py  # For analysis capabilities
python main4.py  # For extended features
```

## Testing
To run the unit tests and verify the functionality of the scripts:

```bash
python -m unittest unit_test.py
```

Test results will be displayed in the console, showing which tests passed or failed.

## Design Considerations
- **Modularity**: The project is divided into multiple scripts to enhance maintainability and testability.
- **Code Structure**: Functions and classes are designed to encapsulate specific behaviors.
- **Error Handling**: The code includes comprehensive error handling to ensure robust operation.
- **Documentation**: In-line comments and docstrings are used throughout to explain functionality.

## Future Development
- **Extensibility**: The modular design allows for easy addition of new features.
- **Performance Optimization**: Certain areas of the code can be optimized for better performance.

## Author
- **Name**: H.A.Naleen Nimantha
- **Student ID**: 20232835
- **University of Westminster ID**: w2082272
- **Institution**: Informatics Institute of Technology
- **Course**: BSc (Hons) Computer Science
