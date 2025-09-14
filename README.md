# Operating-System-using-Python-for-the-Windows-CLI
🖥️ Fam Word Operating System (FWOS)
👨‍💻 Author: Fatehali Abbasali Moknojiya
FWOS is a Python-based Operating System Shell with a Graphical Interface (GUI) built using tkinter. It simulates an OS terminal with commands like ls, cd, cat, grep, touch, vi, etc. It runs as a Python application (not a real kernel) and is designed for learning and fun 🚀.
📦 Requirements
🐍 Python 3.8+
💻 Works on Linux, Windows, macOS
📚 Pre-installed modules: os, sys, shlex, shutil, subprocess, glob, time, re, datetime, tkinter
▶️ How to Run (Source Code)
1️⃣ Clone or copy the FWOS project into a folder.
2️⃣ Make sure you have Python installed: python3 --version
3️⃣ Run the system: python3 fwos.py
🛠️ Supported Commands
•	man - 📖 Show help for commands
•	pwd - 📂 Print working directory
•	cd DIR - 📂 Change directory
•	ls - 📋 List files and folders
•	mkdir D - 📁 Create directory
•	rmdir D - 🗑️ Remove empty directory
•	cp A B - 📄➡️ Copy file
•	mv A B - 📦➡️ Move file
•	rm F - ❌ Remove file
•	cat F - 📜 Show file contents
•	more F - 📜➡️ Show file contents with paging
•	chmod M F - 🔑 Change file permissions
•	diff A B - 🔍 Compare two files
•	grep P F - 🔎 Search text in file(s)
•	wc F - 🧮 Count lines, words, chars
•	ps - ⚙️ Show running processes
•	kill PID - 💀 Kill process
•	nice +N CMD - ⭐ Run with priority
•	sleep N - ⏳ Wait N seconds
•	batch S - 📜 Run script in background
•	at TIME CMD - 🕒 Run command at scheduled time
•	touch F - 🖊️ Create empty file / update timestamp
•	vi F - 📝 GUI editor to edit a file (Save = Ctrl+S, Cancel = Ctrl+Q)
•	clear - 🧹 Clear terminal screen
•	exit - 🚪 Exit FWOS
✨ Features
💻 Custom GUI terminal built with tkinter
📝 Interactive vi editor in GUI window
🌍 Cross-platform: Linux, Windows, macOS
⚡ Real commands simulated with Python
🏁 Windows EXE Build (No Python Needed)
You can convert fwos.py into a standalone Windows .exe using PyInstaller:
1️⃣ Install PyInstaller: pip install pyinstaller
2️⃣ Build EXE: pyinstaller --noconsole --onefile fwos.py
3️⃣ Find EXE in dist/ folder, run fwos.exe on any Windows PC 🎉
📜 License
This project is for educational purposes only.
Created by Fatehali Abbasali Moknojiya.
