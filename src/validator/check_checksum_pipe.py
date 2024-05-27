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

def main():
    for line in sys.stdin:
        # Split the line into two-character groups and convert to integers
        frame = [int(line[i:i+2], 16) for i in range(0, len(line.strip()), 2)]
        if check_frame_checksum(frame):
            # If checksum is valid, return true (status code 0)
            sys.exit(0)
        else:
            # If checksum is invalid, return false (status code 1)
            sys.exit(1)

if __name__ == "__main__":
    main()
