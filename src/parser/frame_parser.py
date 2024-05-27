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
    asdu['Type Identification'] = (frame[index])
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

    # IOA used in iec60780-5-101 version of protcole
    # Information Object Address (IOA) 
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

    frame_dict['ASDU'] = asdu

    # Checksum
    frame_dict['Checksum'] = hex(frame[index])
    index += 1

    # End Byte
    frame_dict['End'] = hex(frame[index])

    return frame_dict

def print_frame(frame_dict):
    for key, value in frame_dict.items():
        if isinstance(value, dict):
            print(f"{key}:")
            for sub_key, sub_value in value.items():
                print(f"  {sub_key}: {sub_value}")
        else:
            print(f"{key}: {value}")

# Example frame in hexadecimal representation
# frame = [0x68, 0x0C, 0x0C, 0x68, 0x73, 0x01, 0x09, 0x01, 0x06, 0x01, 0x00, 0x01, 0x0F, 0x58, 0x16]
frame = [0x68,0x16,0x16,0x68,0x73,0x01,0xa0,0x81,0xa0,0x01,0x6f,0x00,0x04,0x05,0x00,0x03,0x00,0x00,0x42,0x6a,0x00,0x0e,0x02,0xc8,0xb2,0xc4,0xab,0x16]
parsed_frame = parse_iec103_frame(frame)
print_frame(parsed_frame)

