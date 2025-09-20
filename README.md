# Python drawing application in PyQt5

Version: 0.1.2

![Screenshot of the application](https://i.ibb.co/Nd34dwDm/image.png)

## Installation

This section is about setting up a virtual environment if you have Python installed already. If not, [install Python](https://www.python.org/downloads/) first.

 1. Download the source code, or clone the repository: `https://github.com/Broyler/py-drawing-app`
 2. Create a virtual environment: `python3 -m venv .venv`
 3. Activate the virtual environment:
				- On Linux/macOS: `source .venv/bin/activate`
				- On Windows: `.venv\Scripts\activate.bat` 
4. Install the dependencies: `pip install -r requirements.txt`

Once you have everything set up, you can run the project.

### Running the app

Simply execute `python3 src/main.py` from the root of the project - you should be in the same folder as files `README.md`, `pyproject.toml`, `requirements.txt`, etc. 

## Features

This project is still very much in the early development. As per version 0.1.0, the following features exist:

#### Tools:
 - Bucket fill tool (flood fill)
 - Pencil tool
 - Eraser tool
 - Clear screen tool
 
 ### Features:
 
 - File operations such as opening, creating, and saving images.
 - Color selection from a predetermined color palette.
 - Thickness selection.
 - Dynamic window resizing

### Work in progress

 - Line, rectangle and circle tools (<0.2.0).
 - Custom color selection menu (<0.2.0).
 - Scaling settings (<0.2.5).
 - Recent files menu (<0.3.0).
 - Undo and redo commands (<0.3.0).
 - Selection (<0.4.0).

And more...

