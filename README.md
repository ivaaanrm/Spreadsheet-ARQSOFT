# Spreadsheet-ARQSOFT

### Requirements
```sh
pip install -r requirements.txt
````
**Note**: The program uses the `pandas` package to show in terminal the Spreadsheet formatted in columns.

## 1. Instructions for running the program

- For running the program using the command interface:
```sh
python main.py
```
- For running the program using the UI interface:
```sh
python main.py --ui
```
### How to use the graphic interface
- Select the cell to edit
- Insert on the top bar the content of the cell and `Enter`.

## 2. Instructions to run the tests. `TestsRunner.py`

1. Set the working directory to the `markerrun` directory. To be able of import all packages of the project correctly.

```cd PythonProjectAutomaticMarkerForGroupsOf2/SpreadsheetMarkerForStudents/markerrun```

```sh
python TestsRunner.py
```

## 3. DCD Tree project

```
Spreadsheet-ARQSOFT
├─ Domain
│  ├─ Data
│  │  ├─ Formula
│  │  │  ├─ __init__.py
│  │  │  ├─ formula.py
│  │  │  └─ tokenizer.py
│  │  ├─ __init__.py
│  │  ├─ cell.py
│  │  ├─ content.py
│  │  └─ coordinate.py
│  ├─ Exception
│  │  ├─ __init__.py
│  │  └─ exceptions.py
│  ├─ FileHandler
│  │  ├─ __init__.py
│  │  ├─ fileParser.py
│  │  └─ fileSaver.py
│  ├─ __init__.py
│  └─ spreadsheet.py
├─ Interfaces
│  ├─ CommandInterface.py
│  ├─ UIInterface.py
│  └─ __init__.py
├─ LICENSE
├─ README.md
├─ SpreadsheetController.py
├─ main.py
└─ requirements.txt

```