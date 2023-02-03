# ml-gui
Creating a simple Machine Learning graphical user interface that will provide output. 

## App build command
- `pyinstaller --onefile --windowed mlgui.py` or 
- `pyinstaller --noconfirm --clean mlgui.spec` (this is preferred)

## App run command
- `./dist/mlgui`

## App run commands without building
- `python3 -m venv venv`
- `source venv/bin/activate`
- `pip install -r requirements.txt`
- `python mlgui.py`

## Troubleshooting
- `brew install python-tk` (possible issue with tkinter on macOS)