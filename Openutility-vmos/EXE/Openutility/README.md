# Openutility Operating System

Openutility is a lightweight operating system simulation built using Python and Tkinter. It provides a graphical user interface that mimics a desktop environment, allowing users to interact with various applications and system components.

## Features

- **Boot Animation**: A visually appealing boot animation that simulates the startup process of the operating system.
- **System Applications**: Includes a calculator, file explorer, web browser, calendar, clock, note-taking app, settings, application store, and video player.
- **Taskbar**: A taskbar that provides quick access to system applications and displays the current time and battery status.
- **Lock Screen**: A security feature that locks the screen after a period of inactivity, requiring a password to unlock.

## File Structure

- `Openutility.py`: Main entry point of the application, initializes the OS interface and manages system components.
- `ZeroClocks.py`: Implements clock functionalities for displaying the current time.
- `FileExplorer.py`: Provides file management capabilities for browsing and managing files.
- `Browser.py`: A simple web browser for navigating the internet.
- `zero_calendar.py`: Calendar functionalities for managing dates and events.
- `caogaoben.py`: Note-taking application for creating and managing notes.
- `zerostore.py`: Application store for browsing and installing third-party applications.
- `Videos.py`: Video player for playing video files.
- `requirements.txt`: Lists third-party libraries required for the project.

## Installation

To run the Openutility OS, ensure you have Python installed on your machine. Then, install the required libraries by running:

```
pip install -r requirements.txt
```

## Usage

To start the Openutility OS, run the following command:

```
python Openutility.py
```

This will launch the operating system interface, where you can interact with the various applications and features provided.

## Contributing

Contributions are welcome! If you would like to contribute to the project, please fork the repository and submit a pull request.

## License

This project is licensed under the MIT License. See the LICENSE file for more details.