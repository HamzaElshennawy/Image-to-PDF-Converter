# Image to PDF Converter

A lightweight Python script to convert multiple images into a single PDF file. This tool is designed to be easy to use from the command line or integrated into your operating system's context menu.

## Features

-   **Batch Conversion**: Converts multiple images or entire directories of images into a single PDF.
-   **Format Support**: Supports common image formats including `.jpg`, `.jpeg`, `.png`, `.bmp`, `.gif`, `.tiff`, and `.webp`.
-   **Automatic Sorting**: Images are automatically sorted by name before conversion.
-   **Logging**: Generates a log file for each conversion operation to help track progress and debug issues.
-   **Smart Output**: Automatically names the output PDF with a timestamp (e.g., `converted_20231025_143000.pdf`) and saves it in the directory of the first image.

## Prerequisites

-   Python 3.6 or higher
-   [Pillow](https://python-pillow.org/) library

## Installation

1.  **Clone or Download** this repository to your local machine.
2.  **Install Dependencies**:
    Open your terminal or command prompt and run:
    ```bash
    pip install Pillow
    ```

## Usage

Run the script from the command line by providing the paths to the images or directories you want to convert.

### Basic Usage

```bash
python script.py path/to/image1.jpg path/to/image2.png
```

### Convert Entire Directory

You can also pass a directory path, and the script will find all valid images inside it:

```bash
python script.py path/to/images_directory
```

### Mixing Files and Directories

You can mix individual files and directories:

```bash
python script.py path/to/image1.jpg path/to/folder_of_images
```

### Specify Output File

You can specify the name and location of the output PDF using the `-o` or `--output` flag:

```bash
python script.py -o my_document.pdf image1.jpg image2.png
```

### Using the GUI

A graphical interface is available for easier use.

1.  Run the GUI script:
    ```bash
    python gui.py
    ```
2.  **Add Images**: Click "Add Images..." to select files.
3.  **Reorder**: Use "Move Up" and "Move Down" buttons to arrange the page order.
4.  **Convert**: Click "Convert to PDF" and choose where to save the file.

## How it Works

1.  The script accepts a list of file or folder paths.
2.  It filters for supported image extensions.
3.  Images are sorted alphabetically.
4.  All images are converted to RGB mode (if necessary) and appended to a single PDF file.
5.  Expected output is `converted_YYYYMMDD_HHMMSS.pdf` located in the same folder as the first image.
6.  A log file (`convert_log_...txt`) is created nearby to record the process and any errors.

## Troubleshooting

-   **"No valid image files found"**: Ensure the files you are pointing to have one of the supported extensions.
-   **Permission Errors**: Make sure you have write permissions in the directory where the images are located, as the script attempts to save the PDF there.
