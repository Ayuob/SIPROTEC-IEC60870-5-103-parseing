import serial
import time

def send_lines_to_serial(file_path, com_port='COM3', baud_rate=38400):
    ser = None  # Initialize ser outside try for accessibility in finally
    try:
        ser = serial.Serial(com_port, baud_rate, timeout=1, parity=serial.PARITY_EVEN,
                            stopbits=serial.STOPBITS_ONE, bytesize=serial.EIGHTBITS)
        with open(file_path, 'r') as file:
            for line in file:
                line = line.strip()
                data = bytes.fromhex(line)
                ser.write(data)
                start_time = time.time()
                message = b''  # Initialize buffer for accumulating message parts
                
                while True:
                    byte = ser.read(1)
                    if byte:
                        message += byte  # Accumulate each byte into message
                        # Check if the entire message thus far contains the delimiter
                        if b'\x16' in message:  
                            # Split on delimiter, in case multiple messages are in the buffer
                            parts = message.split(b'\x16')
                            for part in parts[:-1]:  # Process all complete messages
                                print(f"Received message: {part.hex()}")
                            message = parts[-1]  # Keep any incomplete message part in the buffer
                            if parts[-1] == b'':
                                break  # If last part is empty, we finished on a delimiter

                    # Timeout check to avoid infinite loops
                    if time.time() - start_time > 5:  # Adjust timeout as needed
                        print("Timeout reached. Continuing to next line.")
                        break

    except serial.SerialException as e:
        print("Serial Port Error:", e)
    except FileNotFoundError:
        print("File not found:", file_path)
    finally:
        if ser:
            ser.close()

# Example usage:
send_lines_to_serial("usb_capdata_output.txt")
