import sys

def calculate_checksum(frame):
    # Calculate checksum as the sum of all bytes from the 5th byte to the last byte before checksum
    checksum = sum(frame[4:-2]) % 256
    return checksum

def check_frame_checksum(frame):
    # Extract checksum from the frame
    received_checksum = frame[-2]
    # Calculate expected checksum
    expected_checksum = calculate_checksum(frame)
    # Compare and return result
    return received_checksum == expected_checksum

def print_help():
    help_text = """
Usage: python check_checksum.py [options]

Options:
  --help      Show this help message and exit.

Description:
  This script reads IEC 60870-5-103 frames from standard input, checks their checksum, and returns an exit status indicating whether the checksum is valid.

  The frame should be provided as a continuous sequence of hexadecimal digits without spaces.

  The script can be used in pipelines to validate frames on the fly. It exits with status code 0 if the checksum is valid and status code 1 if it is not.

Examples:
  cat frames.txt | python check_checksum.py
  echo "680C0C6873010901060100010F5816" | python check_checksum.py
"""
    print(help_text)

def main():
    if '--help' in sys.argv:
        print_help()
        sys.exit(0)

    for line in sys.stdin:
        try:
            # Split the line into two-character groups and convert to integers
            frame = [int(line[i:i+2], 16) for i in range(0, len(line.strip()), 2)]
            if check_frame_checksum(frame):
                # If checksum is valid, return true (status code 0)
                sys.exit(0)
            else:
                # If checksum is invalid, return false (status code 1)
                sys.exit(1)
        except Exception as e:
            print(f"Error processing frame: {line.strip()} - {e}", file=sys.stderr)
            sys.exit(1)

if __name__ == "__main__":
    main()
