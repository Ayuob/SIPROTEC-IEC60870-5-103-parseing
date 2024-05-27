# IEC 60870-5-103 Frame Parser

This repository contains a Python script for parsing IEC 60870-5-103 frames, providing a human-readable description of each field, including the type identification and information elements. This script is useful for validating frames and understanding the data communicated in SCADA systems.

## Features

- Parses IEC 60870-5-103 frames from standard input.
- Provides human-readable descriptions for each field.
- Checks the checksum of the frames.
- Handles various types of information, including measured values, status information, relay actions, and general interrogation.

## Information Object Structure

The Information Object in the IEC 60870-5-103 protocol typically consists of:

1. **Information Object Address (IOA)**: A unique address for each information object.
2. **Information Elements (IE)**: The actual data points associated with the information object, which can include various types of measured values, status information, or commands.

## Information Element Data Types

Information elements can have different data types, including:

- **Single-point information**: Represents binary information such as the status of a switch (on/off).
- **Double-point information**: Used to represent a status with more than two states.
- **Measured values**: Can be normalized values, scaled values, or short floating-point numbers.
- **Integrated totals**: Typically counter values representing quantities over time.
- **Step position information**: Represents the position of a control element in discrete steps.
- **Packed output**: Used for events of protection equipment, typically with a timestamp.

## ASDU Structure

The ASDU (Application Service Data Unit) consists of:

1. **Data Unit Identifier**:
   - **Type identification**: Indicates the type of the ASDU.
   - **Variable structure qualifier (VSQ)**: Indicates whether the ASDU contains a sequence of information elements or information objects.
   - **Cause of transmission (COT)**: Indicates why the ASDU is being sent.
   - **Common address of ASDU**: Identifies the ASDU's destination within the network.

2. **Information Object**:
   - **Information Object Address (IOA)**: The address of the information object.
   - **Information Elements**: The data associated with the information object.
   - **Time tag** (if used): A timestamp indicating when the data was collected.

## Usage

1. Save the script to a file, e.g., `parse_iec103.py`.
2. Run the script and pipe data into it:
   ```sh
   grep -v '^$' frames.txt | cut -d' ' -f2- | python parse_iec103.py
   echo "680C0C6873010901060100010F5816" | python parse_iec103.py
