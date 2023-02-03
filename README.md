# ml-gui
Creating a simple Machine Learning graphical user interface that will provide output. 

## Example Windows install and run
![windows install and run example](20230203125037.gif)

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

## Create a new branch based on develop and tag the release
- `git checkout -b release-#.#.# develop` where `#.#.#`, is the new version e.g. `0.0.1`
- `git add .`
- `git commit -m "Version bump to #.#.#"`
- `git tag -a v#.#.# -m "Tagging version #.#.# as v#.#.#"`
- `git push origin --tags`
    - This will create a tag with the version and push the local tags to remote (this will trigger the `release.yml` github action)
- `git push origin release-#.#.#`

## Troubleshooting
- `brew install python-tk` (possible issue with tkinter on macOS)

## Windows app run commands
- `conda create -n mlgui_env python=3.10`
- `conda activate mlgui_env`
- `pip install -r requirements.txt`
- `python mlgui.py`