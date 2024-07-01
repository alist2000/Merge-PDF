# PDF Merger Application

This is a simple PDF merger application built with Python and PySide6. It allows users to select a directory containing PDF files, merge them, and optionally add page numbers to the merged PDF. The merged PDF is saved in the same directory where the script is run.

## Features

- Select a directory containing PDF files.
- Merge the PDFs in the selected directory.
- Optionally add page numbers to the merged PDF.
- Save the merged PDF in the current working directory.

## Installation

1. Clone the repository:

    ```sh
    git clone https://github.com/your-username/pdf-merger-app.git
    cd pdf-merger-app
    ```

2. Create and activate a virtual environment (optional but recommended):

    ```sh
    python -m venv venv
    source venv/bin/activate   # On Windows use `venv\Scripts\activate`
    ```

3. Install the required packages:

    ```sh
    pip install -r requirements.txt
    ```

## Usage

1. Run the application:

    ```sh
    python pdf_merger_app.py
    ```

2. Interact with the UI:
   - Click "Select Directory" to choose the directory containing the PDFs.
   - Check or uncheck "Add Page Numbers" based on your preference.
   - Click "Generate" to merge the PDFs and optionally add page numbers. The merged PDF will be saved in the current working directory where the script was executed. The status label will update to show the progress and final output file path.

## Requirements

- Python 3.6+
- PySide6
- PyPDF2
- reportlab

## Contributing

Contributions are welcome! Please fork the repository and submit a pull request for any improvements or bug fixes.

## License

This project is licensed under the MIT License.
