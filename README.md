# TP200-tools
Scripts to automate Toast TP200/TP200W printer functions on a mass scale. Reboots, status checks, etc.

- Only tested on TP200 receipt printers, ticket printers such as the TKP300 have not been tested and are not supported.

# Install / Configuration
- Install python
- Download script and setup venv: https://docs.python.org/3/library/venv.html
- Run `pip install scapy requests`
- Set the subnet being used for the POS network in each Python file, in this case `subnet` and `exempt_ips` in the main function of each file.
- If using the status script, it may be helpful to include the known MAC addresses of each printer and the names in the format shown at the top of the Python file. If you choose not to add them, they will appear as IP addresses.

# Run
- Make sure your device is connected to the POS network before running, and disconnect after running.
- Run via root, for example on Linux: `sudo venv/bin/python3 reboot-TP200W.py`
- You may also use the script `run.sh` as an easier interface for each function. However, the network being scanned will still have to be set manually in each Python file.

## reboot-TP200.py
- Reboots all printers that are already on and available on the specified network.

## status-TP200.py
- Scans all available printers on the specified network and reports any issues each printer may have detected, i.e. end of paper, door open, etc.
- Has some configurable options as far as output to the console.

## test-TP200.py
- Should print the test sheet to all available printers on the specified network. This script is has *not* been tested to see if it works and is just a slight modification of the reboot script.

## print-TP200.py
- Print custom text to a single printer. Not designed for mass use.

## Future Roadmap
- Would like to make it easier to install and run
- Consolidation of subnet settings into one file?
- GUI????
