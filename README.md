![Logo](resources/icons/app_icon.ico)

<h1 style="margin-top: 0; padding-top: 0">SilentGuardian</h1>

[![Version](https://img.shields.io/badge/version-1.0.0-blue.svg)](https://semver.org/) [![License](https://img.shields.io/badge/license-GPL--3.0-informational)](https://semver.org/)<br>
SilentGuardian is a Python application built using the PyQt6 library, designed for sound analysis and automatic volume adjustments of selected application on your computer. With advanced sound processing algorithms, our tool allows users to monitor sound levels and react to them automatically and in a configurable manner.

## Table of Contents
- [Key Features](#key-features)
  - [Sound Analysis](#sound-analysis)
  - [Automatic Volume Adjustments](#automatic-volume-adjustments)
  - [Intuitive User Interface](#intuitive-user-interface)
  - [Configurability](#configurability)
- [Installation](#installation)
  - [System Requirements](#system-requirements)
  - [Installation Steps](#installation-steps)
  - [Additional Setup](#additional-setup)
- [Usage](#usage)
- [Example Uses](#example-uses)
- [Project Structure](#structure-of-the-project)
- [Contributing](#contributing)
- [License](#license)
- [Acknowledgements](#acknowledgements)

## Key Features

### Sound Analysis:
- Continuous monitoring of sound from a selected audio source on the computer.
- Utilizes advanced sound processing techniques to determine sound volume and characteristics.

### Automatic Volume Adjustments:
- Automatically adjusts the volume of selected application or process on the computer upon reaching a specified volume threshold.
- Users can configure which application is affected and set preferred volume levels.
- Offers selectable cutoff modes to customize the behavior of automatic volume adjustments.

### Intuitive User Interface:
- Simple and intuitive user interface created using the PyQt6 library.
- Allows easy configuration of sound analysis parameters and management of application volume settings.

### Configurability:
- Flexible customization to individual user preferences and needs.

## Installation

### System Requirements:
- Python >= 3.11
- PyQt6 library

### Installation Steps:
1. Install Python from the official Python website: [python.org](https://www.python.org/).
2. Install the dependencies listed in `requirements.txt` by running: 
   ```bash
   pip install -r requirements.txt
   ```

### Additional Setup:
1. Install VB-CABLE Virtual Audio Device from the official website: [VB-CABLE Virtual Audio Device](https://vb-audio.com/Cable/).
2. Configure the audio settings on your operating system to use VB-CABLE Virtual Audio Device for listening.

## Usage
1. Open the applications that generate the sound you want to analyze.
2. In the sound settings of each application, select VB-CABLE as the output device.
3. Run the SilentGuardian application: ```python main.py```

## Example Uses
#### 1. Discord Conversations
Enhance your Discord experience by listening to music at a higher volume during quiet moments. SilentGuardian automatically mutes or lowers the volume of your music when someone starts speaking, ensuring you never miss a word.

#### 2. Online Meetings
Improve your productivity during online meetings by applying the same principle. Enjoy background music at a comfortable volume, and let SilentGuardian automatically lower the music volume when someone speaks, allowing you to focus on the conversation without manual adjustments.

#### 3. Watching Movies with Interspersed Music
Enjoy watching movies while occasionally listening to music. SilentGuardian can lower or mute the music when movie audio is detected, providing an uninterrupted viewing experience while still enjoying your favorite tunes.

## Structure of the Project

```
silent_guardian/
│
├── backend/ # Modules containing the application logic
│ ├── __init__.py
│ ├── actions.py
│ ├── audio_core.py
│ ├── binds.py
│ ├── config.py
│ ├── core.py
│ ├── cutoff.py
│ ├── global_state_manager.py
│ ├── logger.py 
│ └── settings.py
│
├── gui/ # Modules containing the user interface
│ ├── __init__.py
│ ├── animated_stacked_widget.py
│ ├── apps.py
│ ├── apps_settings.py
│ ├── bind_create.py
│ ├── bind_remove.py
│ ├── binds.py
│ ├── binds_clear.py
│ ├── custom_messagebox.py
│ ├── custom_titlebar.py
│ ├── cutoff_modes.py
│ ├── inputs.py
│ ├── inputs_settings.py
│ ├── main_window.py
│ ├── menu.py
│ ├── settings.py
│ ├── svg_color_widget.py
│ └── tray.py
│
├── resources/ # Application resources
│ ├── fonts/
| │ └── Poppins
│ ├── icons/
│ ├── resources.py
│ └── resources.qrc
│
├── README.md
├── requirements.txt
├── config.json
├── version.py
└── main.py
```

## Contributing
Pull requests are welcome. For minor changes, please open an issue first to discuss what you would like to change.

## License
This project is licensed under the GNU General Public License v3.0. You can view the full text of the license in the [LICENSE](LICENSE) file. This license ensures that any derivative work is also distributed under the same terms, promoting open-source development and collaboration.

## Acknowledgements
Icons used in this project are sourced from SVG Repo, primarily under the MIT License.
