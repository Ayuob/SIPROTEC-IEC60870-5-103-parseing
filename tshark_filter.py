import sys
import pyshark
import subprocess

def extract_usb_data_with_tshark(file_path):
    cmd = ['tshark', '-r', file_path, '-Y', 'usb.capdata', '-T', 'fields', '-e', 'usb.capdata']
    process = subprocess.run(cmd, capture_output=True, text=True)
    print(process.stdout)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python script.py <path_to_file.pcapng>")
        sys.exit(1)

    file_path = sys.argv[1]
    extract_usb_data_with_tshark(file_path)