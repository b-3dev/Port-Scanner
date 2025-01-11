# Port Scanner Tool

A simple, multithreaded port scanner designed to scan a range of ports on a specified IP address or domain. This tool is capable of quickly scanning a wide range of ports to check whether they are open or closed, and it displays detailed process and system information during the scan.

## Features
- Multithreaded scanning to improve speed.
- Port range validation to ensure correct input.
- IP address or domain validation before starting the scan.
- Progress bar to show scanning status.
- Memory and process information display after scan completion.
- Auto installation of required libraries (`colorama`, `psutil`) if they are not found.
- Colorful output for better readability.

## Installation

1. Clone the repository or download the script to your local machine.

2. Run the script using Python:

   ```bash
   python src/script.py
   ```

## Usage

1. **Launch the script**:  
   Once you run the script, it will display the logo and information about the tool.

2. **Enter the target**:  
   You will be prompted to input either an IP address or a domain name. The tool will validate this input to ensure it is correct.

3. **Define the port range**:  
   You will need to enter a start port and an end port. The tool will scan all ports in this range. The valid port range is from 1 to 65535.

4. **Start the scan**:  
   After entering the target and port range, the scan will begin. The tool will display the scanning progress as a progress bar and will output the results in real-time.

5. **Review the results**:  
   After the scan completes, the tool will display the following:
   - A list of open ports, if any.
   - The number of open and closed ports.
   - Detailed system and process information, such as memory usage and scan duration.

## Functions

### `print_logo()`
Displays the logo and metadata about the tool.

### `scan_port(ip, port)`
Scans a single port on the given IP address and updates the results.

### `threader(queue, ip, total_ports, semaphore)`
Worker thread that processes ports from the queue and scans them.

### `print_progress(remaining_ports, total_ports)`
Displays a progress bar based on the number of remaining ports.

### `scan(ip, start_port, end_port)`
Scans a range of ports on the provided IP address. It uses multiple threads to improve speed.

### `is_valid_ip_or_domain(ip)`
Validates if the provided input is a valid IP address or domain name.

### `validate_port_input(prompt)`
Validates port input from the user to ensure it is a number between 1 and 65535.

### `validate_ip_or_domain_input()`
Prompts the user to input a valid IP address or domain name.

### `print_system_info(start_time, num_open_ports, num_ports_scanned)`
Displays system and process information, including memory usage, process ID, thread count, and scan details.

### `main()`
The main function that runs the tool, handles user input, and initiates the scan.

## Notes
- The tool uses the `socket` library for network communication and port scanning.
- It utilizes `psutil` to fetch system information like memory usage and process details.
- `colorama` is used to color the output for better readability in the terminal.

## Troubleshooting

- **"Library not found"**: If the tool reports that a library is missing, it will attempt to install the library automatically. Ensure you have a stable internet connection.
- **Invalid input**: The tool validates both IP/domain and port input. If you encounter issues, ensure that the values you provide are valid.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Need Help?

If you encounter any issues or have questions about this project, feel free to open an issue in the [GitHub repository](https://github.com/b-3dev/Port-Scanner/issues). I'll be happy to assist you!