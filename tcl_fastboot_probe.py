"""Request MediaTek preloader FASTBOOT mode once; no DA or flash commands."""
import sys
import time
import serial

port = sys.argv[1] if len(sys.argv) > 1 else "COM8"
deadline = time.monotonic() + 45
print(f"Waiting up to 45 seconds for {port}. Connect the powered-off phone.", flush=True)
while time.monotonic() < deadline:
    try:
        s = serial.Serial(port, 115200, timeout=0.25, write_timeout=0.5)
    except (OSError, serial.SerialException):
        time.sleep(0.05)
        continue

    # Once a port opens, send only one mode request. Do not retry a write.
    try:
        print(f"Opened {port}; requesting FASTBOOT once.", flush=True)
        s.write(b"FASTBOOT")
        response = bytearray()
        end = time.monotonic() + 2
        while time.monotonic() < end:
            try:
                response.extend(s.read(64))
            except (OSError, serial.SerialException) as e:
                print(f"Port disconnected or read failed: {e}")
                break
            if b"TOOBTSAF" in response or b"READYTOO" in response or b"METAFORB" in response:
                break
        print("Response (ASCII):", repr(bytes(response)))
        print("Response (HEX):", response.hex(" "))
        if b"METAFORB" in response:
            print("Preloader returned a forbidden-mode response.")
        elif b"TOOBTSAF" in response or b"READYTOO" in response:
            print("Possible FASTBOOT acknowledgement. Verify with fastboot devices.")
        else:
            print("No recognized acknowledgement. Check the phone and fastboot devices.")
    except (OSError, serial.SerialException) as e:
        print(f"Mode request failed: {e}")
    finally:
        try:
            s.close()
        except (OSError, serial.SerialException):
            pass
    break
else:
    print(f"Timed out waiting for {port}; no command was sent.")
