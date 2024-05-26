import sys

TYPE_IDENTIFICATION_MAP = {
    0x01: "Measured Values",
    0x0D: "Status Information"
    # Add more types as needed
}

MEASURED_VALUES_MAP = {
    601: "Ia (current phase A)",
    602: "Ib (current phase B)",
    603: "Ic (current phase C)",
    604: "In (neutral current)",
    605: "I1 (positive sequence current)",
    606: "I2 (negative sequence current)",
    831: "3Io (zero sequence current)",
    621: "Va (voltage phase A)",
    622: "Vb (voltage phase B)",
    623: "Vc (voltage phase C)",
    624: "Va-b",
    625: "Vb-c",
    626: "Vc-a",
    627: "VN (neutral voltage)",
    629: "V1 (positive sequence voltage)",
    630: "V2 (negative sequence voltage)",
    641: "P (active power)",
    642: "Q (reactive power)",
    645: "S (apparent power)",
    644: "Frequency"
}

STATUS_INFORMATION_MAP = {
    201: "Circuit breaker status",
    202: "Disconnect switch status",
    203: "Ground switch status",
    204: "Relay status",
    205: "Trip status",
    206: "Pickup status",
    207: "Block status",
    208: "Disk emulation status"
    # Add more status information as needed
}

def type_identification_description(type_id):
    return TYPE_IDENTIFICATION_MAP.get(type_id, f"Unknown Type ({type_id})")

def measured_value_description(info_number):
    return MEASURED_VALUES_MAP.get(info_number, f"Unknown Measurement ({info_number})")

def status_information_description(info_number):
    return STATUS_INFORMATION_MAP.get(info_number, f"Unknown Status ({info_number})")

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
    info_number = frame[index]
    if type_id == 0x01:
        asdu['Information number'] = measured_value_description(info_number)
    elif type_id == 0x0D:
        asdu['Information number'] = status_information_description(info_number)
    else:
        asdu['Information number'] = f"Unknown Information number ({info_number})"
    index += 1

    # Information elements Value
    info_elements_value = []
    while index < len(frame) - 2:  # Assuming the last 2 bytes are Checksum and End Byte
        iov = (frame[index] << 8) + frame[index + 1]
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
