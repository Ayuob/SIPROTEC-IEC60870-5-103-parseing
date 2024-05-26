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
    import sys
    for line in sys.stdin:
        # Split the line into two-character groups and convert to integers
        frame = [int(line[i:i+2], 16) for i in range(0, len(line.strip()), 2)]
        if check_frame_checksum(frame):
            print("Checksum is valid for frame:", line.strip())
        else:
            print("Invalid checksum for frame:", line.strip())

if __name__ == "__main__":
    main()
