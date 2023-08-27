# Python-PLC Communication via TCP  
  
This project establishes communication between a Python application and a Programmable Logic Controller (PLC) using the TCP/IP protocol. The Python script acts as a client that connects to the PLC server, enabling data exchange between the two systems. This can be useful for monitoring, data logging, or control applications in industrial automation systems.  
  
## Motivation  
  
The motivation behind this project is to improve quality control within a manufacturing process. In a production line where items are being assembled or manufactured, there's a camera system and various sensors monitoring the process. The Python program, equipped with machine learning algorithms or AI, can analyze the information from these sensors and cameras to perform real-time quality assessment.  
  
Two threads play a role in this scenario:  
  
1. **Transmitting Thread:** One thread controls the transmission speed of the information. This is important because you want to ensure that the data from the sensors and cameras is sent to the Python program in a timely manner. Depending on the processing capacity of the Python program and the data rate from the sensors, you might need to adjust the transmission speed to avoid overwhelming the system.  
  
2. **Bit Toggling Thread:** The other thread that toggles bit 0 of the communication could be used as a synchronization or trigger mechanism. For instance, when a new item arrives at a particular point on the production line, the bit could be toggled to notify the Python program that a new inspection cycle should begin. This ensures that the machine learning algorithms or AI analyze the relevant data for each item at the right time.  
  
The Python program could use machine learning algorithms to analyze images from the camera system to detect defects or anomalies in the products being manufactured. It could also process data from various sensors to monitor parameters such as temperature, pressure, vibration, etc., to ensure that the manufacturing process is operating within specified tolerances. If any issues are detected, the system could trigger alerts, stop the production line, or take corrective actions.  
  
In this way, the combination of Python, machine learning algorithms, sensors, cameras, and PLC communication creates an intelligent quality control system that enhances manufacturing efficiency and product quality. 
 
## Table of Contents  
  
- [Installation](#installation)  
- [Usage](#usage)  
- [Configuration](#configuration)  
- [Dependencies](#dependencies)  
- [Contributing](#contributing)  
- [License](#license)  
  
## Installation  
  
To install and set up this project, follow these steps:  
  
1. Clone the repository:  
git clone https://github.com/yourusername/yourproject.git

2. Navigate to the project directory:  
cd TCPcom/src

3. Install any dependencies, if applicable (e.g., using `pip` for Python projects):  
pip install -r requirements.txt

4. Provide any additional steps necessary to set up the project.  
  
## Usage  
  
To use this project, run the main Python script, which will connect to the PLC server and initiate communication:  
  
python main.py

  
Ensure that the PLC server is running and properly configured to accept incoming TCP connections.  
  
## Configuration  
  
This project uses a `config.py` file to manage global variables for the TCP/IP connection. The available settings and their purposes are:  
  
- `LENGTH`: The length of the data to be sent (default: 32)  
- `PORT`: The port number to use for connecting to the PLC server (default: 5050)  
- `FORMAT`: The encoding format for sent data (default: 'utf-8')  
- `SERVER`: The PLC server's IP address (default: "192.168.17.100")  
- `ADDR`: The server's address, a tuple containing the `SERVER` and `PORT` (default: (SERVER, PORT))  
  
Make sure to update these settings as needed to match the configuration of your PLC server.  
  
## Dependencies  
  
List any third-party libraries or tools that your project relies on. Include the version numbers and links to the respective project pages.  
  
For example:  
  
- [Python](https://www.python.org/) 3.7 or later  
  
## Contributing  
  
To contribute to this project:  
  
1. Fork the repository.  
2. Create a new branch (`git checkout -b my-feature-branch`).  
3. Commit your changes (`git commit -am 'Add some feature'`).  
4. Push to the branch (`git push origin my-feature-branch`).  
5. Create a new Pull Request.  
  
Please follow established coding standards and include tests for any new features or bug fixes.  
  
## License  
  
Include information about your project's license, if applicable. You can link to the full license text in a separate `LICENSE` file.  
  
---  