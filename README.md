# Aura Video-Analyser
Software developed by Egon Spengler to aid research into the visualisation and interpretation of the human aura and emotional response. The Aura Video-Analyser is a machine which interprets the brain's spectra-neuronal, psycho-electrical frequencies (associated with the variation of luminescense in the aura, as response to changes in the subject's emotional condition), through electrodes adhered to the subject's left and right temples. The raw psycho-electrical impulses are fed into algorithms that convert these signals into usable data. The machine interprets the data and outputs to video.

A real-time video thermal-imaging filter which recolours, pixelates, and replaces background. The effect replicates the screen shown in Ghostbusters when Dana is being interviewed.


## Setup
#### 1. Install dependencies (must be Python 3.11)

```bash
# Linux
sudo apt-get install python3.11 python3-pip python3.11-venv

# Windows
winget install Python.Python.3.11
winget install --id Git.Git -e --source winget # Install Git if not already installed
```

#### 2. Clone the repo

```bash
git clone https://github.com/jae-vh/Aura-Video-Analyser
cd Aura-Video-Analyser
```

#### 3. Create virtual environment and activate

```bash
# Linux 
python3.11 -m venv venv
. venv/bin/activate

# Windows
py -3.11 -m venv venv
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope Process
.\venv\Scripts\activate
```

#### 4. Install Python dependencies

```bash
pip install -r requirements.txt
```

#### 5. Execute Aura Video-Analyser

```bash
# Linux
python3.11 aura-video-analyser.py

# Windows
python aura-video-analyser.py
```

#### 6. Provide camera device index

```bash
# Example:
{0: 'EasyCamera', 1: 'Webcam C170', 2: 'OBS Virtual Camera'}
Enter camera index:
1
```
#### 7. To close, click Video-Analyser window and press 'q'

## Notes
- Software has only been tested on one camera so far, so your mileage may vary!
- Ensure subject is well-lit (colour mapping depends heavily on lighting)

## Contributing

Bug reports, feature requests, and pull requests are more than welcome :)

## Acknowledgements

The Aura Video-Analyser is based on the following project: [https://github.com/noorkhokhar99/Creating-fake-thermal-images-using-Python](https://github.com/noorkhokhar99/Creating-fake-thermal-images-using-Python)
