import os

# ✅ Get the virtual serial port path from the environment variable
SERIAL_PORT = os.getenv("VIRTUAL_SERIAL_PORT", "/tmp/ttyUSB0")

def send_iridium_message(message):
    """Simulates sending a message via a virtual Iridium serial device."""
    try:
        print(f"📡 Simulating Iridium Message: {message}")

        # ✅ Ensure the virtual serial device exists before using it
        if os.path.exists(SERIAL_PORT):
            print(f"✅ Virtual Serial Port ({SERIAL_PORT}) detected.")
            return True
        else:
            raise FileNotFoundError(f"❌ Virtual Serial Port ({SERIAL_PORT}) not found!")

    except Exception as e:
        print(f"❌ Error in simulated Iridium messaging: {e}")
        return False