# Aura Video-Analyser
Fundamental software developed by Egon Spengler to aid research into the visualisation and interpretation of the human aura. The Aura Video-Analyser is a machine which interprets the brain's spectra-neuronal, psycho-electrical frequencies, (associated with the variation of luminescense in the aura, as response to changes in the subject's emotional condition) through electrodes adhered to the subject's left and right temples. The psycho-electrical impulses are fed into algorithms that convert these signals into usable data. The machine interprets the data and outputs to video.

## Setup
#### 1. Install dependencies (must be Python 3.11)
```bash
# Linux
sudo apt-get install python3.11 python3.11-pip python3.11-venv

# Windows
winget install Python.Python.3.11
```

#### 2. Within the repo directory, create virtual environment and activate

```bash
# Linux 
python3.11 -m venv venv
. venv/bin/activate

# Windows
py -3.11 -m venv venv
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope Process
.\venv\Scripts\activate
```

#### 3. Install Python dependencies

```bash
pip install -r requirements.txt
```

#### 4. Execute Aura Video-Analyser

```bash
# Linux
python3.11 aura-video-analyser.py

# Windows
python aura-video-analyser.py
```

#### 5. Provide camera device index

```
# Example:
{0: 'EasyCamera', 1: 'Webcam C170', 2: 'OBS Virtual Camera'}
Enter camera index:
1
```
#### 6. To close, click OpenCV window and press 'q'


## Acknowledgements

The Aura Video-Analyser is based on the following project: [https://github.com/noorkhokhar99/Creating-fake-thermal-images-using-Python](https://github.com/noorkhokhar99/Creating-fake-thermal-images-using-Python)
