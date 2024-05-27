import sys

TYPE_IDENTIFICATION_MAP = {
    0x01: "Measured Values",
    0x09: "Min/Max Values",
    0x0B: "Demand Values",
    0x0D: "Status Information"
}

MEASURED_VALUES_MAP = {
    0: "Ia (current phase A)",
    1: "Ib (current phase B)",
    2: "Ic (current phase C)",
    3: "In (neutral current)",
    4: "I1 (positive sequence current)",
    5: "I2 (negative sequence current)",
    6: "3Io (zero sequence current)",
    7: "Va (voltage phase A)",
    8: "Vb (voltage phase B)",
    9: "Vc (voltage phase C)",
    10: "V1 (positive sequence voltage)",
    11: "V2 (negative sequence voltage)",
    12: "VN (neutral voltage)",
    13: "P (active power)",
    14: "Q (reactive power)",
    15: "S (apparent power)",
    16: "f (frequency)",
    17: "PF (power factor)"
}

def type_identification_description(type_id):
    return TYPE_IDENTIFICATION_MAP.get(type_id, f"Unknown Type ({type_id})")

def measured_value_description(index):
    return MEASURED_VALUES_MAP.get(index, f"Unknown Measurement ({index})")

def parse_iec103_frame(frame):
    frame_dict = {}
    index = 0

    # Start Byte
    frame_dict['Start'] = hex(frame[index])
    index += 1

    # Length
    frame_dict['Length1'] = frame[index]
    index += 1
    frame_dict['Length2'] = frame[index]
    index += 1

    # Start Byte again
    frame_dict['Start (again)'] = hex(frame[index])
    index += 1

    # Control Field
    frame_dict['Control'] = hex(frame[index])
    index += 1

    # Address Field
    frame_dict['Address'] = frame[index]
    index += 1

    # ASDU
    asdu = {}
    type_id = frame[index]
    asdu['Type Identification'] = type_identification_description(type_id)
    index += 1
    asdu['Variable Structure Qualifier (VSQ)'] = hex(frame[index])
    index += 1
    asdu['Cause of Transmission (COT)'] = hex(frame[index])
    index += 1
    asdu['Common Address'] = frame[index]
    index += 1
    asdu['Function type'] = frame[index]
    index += 1
    asdu['Information number'] = frame[index]
    index += 1

    # Information elements Value
    info_elements_value = []
    while index < len(frame) - 2:  # Assuming the last 2 bytes are Checksum and End Byte
        iov = (frame[index] << 8) + frame[index + 1]
        if type_id == 0x01:  # Measured Values
            info_elements_value.append(f"{measured_value_description(len(info_elements_value))}: {iov}")
        else:
            info_elements_value.append(iov)
        index += 2
    asdu['Information elements Value'] = info_elements_value

    # Checksum
    frame_dict['Checksum'] = hex(frame[index])
    index += 1

    # End Byte
    frame_dict['End'] = hex(frame[index])

    frame_dict['ASDU'] = asdu
    return frame_dict

def print_frame(frame_dict):
    for key, value in frame_dict.items():
        if isinstance(value, dict):
            print(f"{key}:")
            for sub_key, sub_value in value.items():
                print(f"  {sub_key}: {sub_value}")
        else:
            print(f"{key}: {value}")

def main():
    buffer = ""

    for line in sys.stdin:
        # Remove empty lines
        line = line.strip()
        if not line:
            continue

        buffer += line

        # Check if the buffer ends with 0x16
        if buffer[-2:] != "16":
            continue

        try:
            # Split the buffer into two-character groups and convert to integers
            frame = [int(buffer[i:i+2], 16) for i in range(0, len(buffer), 2)]
            # Drop fixed length frames starting with 0x10
            if frame[0] == 0x10:
                buffer = ""
                continue

            parsed_frame = parse_iec103_frame(frame)
            print_frame(parsed_frame)
            print()
        except Exception as e:
            print(f"Error processing frame: {buffer} - {e}", file=sys.stderr)

        buffer = ""

if __name__ == "__main__":
    if '--help' in sys.argv:
        help_text = """
Usage: python parse_iec103.py [options]

Options:
  --help      Show this help message and exit.

Description:
  This script reads IEC 60870-5-103 frames from standard input, checks their checksum, and parses the frame content.

  The frame should be provided as a continuous sequence of hexadecimal digits without spaces.

  The script can be used in pipelines to validate frames on the fly.

Examples:
  grep -v '^$' frames.txt | cut -d' ' -f2- | python parse_iec103.py
  echo "680C0C6873010901060100010F5816" | python parse_iec103.py
"""
        print(help_text, file=sys.stderr)
        sys.exit(0)
    main()
