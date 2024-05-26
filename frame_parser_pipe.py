import sys

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
    asdu['Type Identification'] = hex(frame[index])
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

    # # Information Object Address (IOA)
    # ioa = (frame[index] << 8) + frame[index + 1]
    # asdu['Information Object Address (IOA)'] = ioa
    # index += 2

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
    for line in sys.stdin:

        buffer = ""

        # Remove empty lines
        line = line.strip()
        if not line:
            continue

        buffer += line
        
        # Check if the buffer ends with 0x16
        if buffer[-2:] != "16":
            continue

        # Split the buffer into two-character groups and convert to integers
        frame = [int(buffer[i:i+2], 16) for i in range(0, len(buffer), 2)]
            
        # Split the line into two-character groups and convert to integers
        # frame = [int(line[i:i+2], 16) for i in range(0, len(line.strip()), 2)]

        # Drop fixed length frames starting with 0x10
        if frame[0] == 0x10:
            buffer = ""
            continue
        

        # frame = [int(x, 16) for x in line.strip().split()]
        parsed_frame = parse_iec103_frame(frame)
        print_frame(parsed_frame)
        print()

if __name__ == "__main__":
    main()
