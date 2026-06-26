# Unity Localization Master

A desktop tool for translating and managing Unity Localization XML files with an intuitive graphical interface.

Unity Localization Master helps developers and translators automate the localization workflow by translating XML localization entries, editing translations, and exporting updated localization files without manually copying text between tools.

---

## Features

- Modern desktop interface built with Python and Tkinter
- Import Unity Localization XML files
- Automatic translation of localization entries
- Support for multiple target languages
- Preserve XML structure and formatting
- Batch translation workflow
- Save and reload project settings
- Logging and error reporting
- Designed for game localization projects

---

## Why Use Unity Localization Master?

Managing localization files manually can become time-consuming when working with hundreds or thousands of text entries.

Unity Localization Master helps by:

- Reducing repetitive translation work
- Speeding up localization updates
- Keeping XML files organized
- Simplifying multilingual project management
- Providing a user-friendly interface instead of editing XML manually

---

# Installation

## Option 1: Download Prebuilt Release (Recommended)

1. Open the Releases page.
2. Download the latest executable.
3. Run the application.

No Python installation is required.

---

## Option 2: Run From Source

### Requirements

- Python 3.10 or newer
- Windows 10/11

### Clone the Repository

```bash
git clone https://github.com/PVMRK/UnityLocalizationMaster.git
cd UnityLocalizationMaster
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Start the Application

```bash
python unity_localization_master.py
```

---

# Building an Executable

## Using Nuitka

Install Nuitka:

```bash
pip install nuitka ordered-set zstandard
```

Build:

```bash
python -m nuitka ^
  --standalone ^
  --onefile ^
  --windows-console-mode=disable ^
  --enable-plugin=tk-inter ^
  --include-package=deep_translator ^
  unity_localization_master.py
```

The compiled executable will be generated automatically.

---

# Quick Start Guide

## Step 1 — Launch the Application

Start Unity Localization Master.

The main window will open and display the available translation options.

---

## Step 2 — Select an XML File

Choose your Unity localization XML file.

The application will load and parse all localization entries.

---

## Step 3 — Configure Translation

Select:

- Source language
- Target language

Review the settings before starting the translation process.

---

## Step 4 — Start Translation

Press the translation button.

The application will:

1. Read localization entries
2. Translate text automatically
3. Preserve XML formatting
4. Generate updated localization content

Depending on file size, this process may take some time.

---

## Step 5 — Review Results

After translation completes:

- Check translated entries
- Verify special characters
- Review context-sensitive phrases

Automatic translation may occasionally require manual corrections.

---

## Step 6 — Save the Output

Export the translated XML file.

The generated file can then be imported back into your Unity project.

---

# Project Structure

```text
UnityLocalizationMaster/
│
├── unity_localization_master.py
├── requirements.txt
├── README.md
├── LICENSE
└── .gitignore
```

---

# Notes About Antivirus Software

Some antivirus engines may flag freshly built Python executables as suspicious.

This can happen because:

- The executable is newly created
- Python applications are packaged into a single binary
- Heuristic or AI-based detection systems generate false positives

The complete source code is publicly available in this repository and can be independently reviewed or built from source.

---

# Troubleshooting

## Translation Does Not Start

Make sure:

- Internet connection is available
- Dependencies are installed correctly
- The XML file is valid

---

## XML File Cannot Be Loaded

Verify:

- The file exists
- The XML structure is not corrupted
- The file is encoded correctly

---

## Build Errors

Update dependencies:

```bash
pip install -U pip
pip install -r requirements.txt
```

---

# Contributing

Contributions, bug reports, feature requests, and pull requests are welcome.

If you discover an issue, please open an Issue on GitHub and include:

- Steps to reproduce
- Screenshots (if applicable)
- Error messages
- Application version

---

# License

This project is distributed under the MIT License.

See the LICENSE file for details.

---

# Thank You

Thank you for using Unity Localization Master.

I hope this tool saves you time and makes the localization process easier for your projects.

If the project helped you and you'd like to support future development, you can make a donation here:

👉 👉 **[Support the project](https://www.donationalerts.com/r/pvmrk)**

Your support is greatly appreciated and helps maintain and improve the project.

Happy developing and good luck with your game projects!
