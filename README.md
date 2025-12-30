# 📝 ZenNotes - Modern Writing Space

**ZenNotes** is a sleek, distraction-free desktop note-taking application built with Python. It features a modern dark-mode interface, real-time search, and a local SQLite database to keep your thoughts organized and private.

## ✨ Features

* **Modern UI**: Built with `CustomTkinter` for a high-performance, beautiful dark-themed experience.
* **Local Storage**: All notes are stored locally in a `notes.db` file. Your data never leaves your computer.
* **Instant Search**: Find your notes quickly with a real-time title search.
* **Management**: Create, rename, and delete notes with ease.
* **Auto-save**: Hit "Save Changes" to commit your writing to the database instantly.

---

## 🚀 How to Run (For Users)

You don't need to install Python to use ZenNotes. Just download the version for your Operating System:

1. Go to the **Actions** tab in this GitHub repository.
2. Select the latest successful "Build ZenNotes Executables" run.
3. Scroll down to **Artifacts** and download the zip file for your OS (**Windows, macOS, or Linux**).
4. **Important**: Place the executable in its own folder (e.g., `Documents/ZenNotes`).
5. Run the file:
* **Windows**: Double-click `notes_app.exe`.
* **Linux**: Right-click `notes_app` -> Properties -> Permissions -> **Allow executing file as program**, then run it.
* **macOS**: Double-click the app (you may need to allow it in Security settings).



> **Note**: On first run, a file named `notes.db` will be created in the folder. This file contains all your notes—**do not delete it** if you want to keep your data!

---

## 🛠️ Development & Manual Setup

If you want to run the source code or modify the app:

### Prerequisites

* Python 3.10 or higher
* `uv` (recommended) or `pip`

### Installation

1. Clone the repository:
```bash
git clone https://github.com/your-username/zennotes.git
cd zennotes

```


2. Set up a virtual environment and install dependencies:
```bash
uv venv
source .venv/bin/activate  # On Linux/Mac
# .venv\Scripts\activate   # On Windows
uv pip install -r requirements.txt

```


3. Run the app:
```bash
python notes_app.py

```



---

## 📦 Building Standalone Files

To package the app manually using PyInstaller:

**Linux:**

```bash
pyinstaller --noconsole --onefile \
--add-data "$(python -c 'import customtkinter, os; print(os.path.dirname(customtkinter.__file__))'):customtkinter/" \
notes_app.py

```

**Windows:**

```bash
pyinstaller --noconsole --onefile ^
--add-data "PATH_TO_CUSTOMTKINTER;customtkinter/" ^
notes_app.py

```

---


### **Final Checklist before you Push to GitHub:**

1. Ensure your main file is named `notes_app.py`.
2. Make sure your `.github/workflows/build.yml` file is exactly as we discussed.
3. Ensure your `requirements.txt` is the cleaned version.
