import sys
import struct

def hex_to_float(hex_str):
    # Convert hexadecimal string to float
    return struct.unpack('!f', bytes.fromhex(hex_str))[0]

def main():
    if len(sys.argv) != 2:
        print("Usage: python script.py <float_value>")
        sys.exit(1)

    try:
        float_value = float(sys.argv[1])
    except ValueError:
        print("Error: Invalid float value")
        sys.exit(1)

    # Read hexadecimal lines from standard input
    for line in sys.stdin:
        hex_str = line.strip()
        for i in range(len(hex_str)):
            for j in range(i + 1, len(hex_str) + 1):
                substr = hex_str[i:j]
                try:
                    if hex_to_float(substr) == float_value:
                        print(hex_str)
                        break
                except struct.error:
                    # Ignore substrings that are not valid hexadecimal
                    pass

if __name__ == "__main__":
    main()
