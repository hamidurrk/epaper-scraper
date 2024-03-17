# Epaper Scraper

This is a Python-based web scraper for extracting data from online newspapers. Tested on [Jugantor Newspaper](https://epaper.jugantor.com/) from 2012 to 2024 in a Windows 11 machine.

## Installation

### Prerequisites

Before installing the scraper, ensure you have the following prerequisites:

- A Windows machine (Tested on Windows 11)
- [Python 3.12.0](https://www.python.org/downloads/release/python-3120/) installed on your system 
- [Firefox](https://www.mozilla.org/en-US/firefox/new/) installed as your browser. Make sure to install it in `C:\Program Files\Mozilla Firefox\`.

### Installation Steps

1. Download the Tesseract OCR executable from [here](https://github.com/UB-Mannheim/tesseract/wiki).

2. Install Tesseract OCR by following the installation instructions provided in the repository. Make sure to install it in `C:\Program Files (x86)\Tesseract-OCR`.

3. Open a command prompt or Anaconda prompt.

4. Navigate to the directory where you have cloned or downloaded the epaper-scraper repository.

5. Create and activate a virtual environment (optional but recommended):

    ```bash
    python -m venv venv
    ```

    - On Windows:

    ```bash
    venv\Scripts\activate
    ```

6. Install the required Python packages using pip:

    ```bash
    pip install -r requirements.txt
    ```

7. Test if Tesseract OCR is installed correctly by opening a Python prompt and running:

    ```python
    import pytesseract
    print(pytesseract)
    ```

    If you don't encounter any errors, Tesseract OCR is installed successfully.

## Usage

To use the epaper-scraper, follow these steps:

1. Click and run `start_firefox.bat` file. Alternatively run the commands from `cmd.txt`. This will initilize a firefox browser instance. 

1. Adjust parameters of the function in `main.py` and run:

    ```bash
    python main.py
    ```

3. The scraper will start extracting data from the specified newspaper website and save it to the specified output directory.


<!-- Download tesseract exe from https://github.com/UB-Mannheim/tesseract/wiki.

Install this exe in C:\Program Files (x86)\Tesseract-OCR

Open virtual machine command prompt in windows or anaconda prompt.

Run pip install pytesseract

To test if tesseract is installed type in python prompt:

import pytesseract

print(pytesseract) -->