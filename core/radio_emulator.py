import re


class VirtualFT991A:
    def __init__(self):
        # Default state of our virtual rig
        self.vfo_a_freq = 14074000  # 14.074 MHz (in Hz)
        self.mode = "12"  # Yaesu code '12' stands for USB-DATA (FT8)
        self.power = 50  # 50 Watts

    def process_command(self, command_str):
        """Processes a raw Yaesu CAT string and returns the rig response."""
        command_str = command_str.strip()
        if not command_str.endswith(';'):
            return ""

        # Extract the 2-letter instruction code
        code = command_str[:2]

        # 1. Frequency Read/Write (FA)
        if code == "FA":
            if len(command_str) > 3:  # Writing a new frequency e.g., FA014074000;
                digits = re.findall(r'\d+', command_str)
                if digits:
                    self.vfo_a_freq = int(digits[0])
                return ""  # Set commands don't reply
            else:  # Reading frequency e.g., FA;
                return f"FA{self.vfo_a_freq:09d};"

        # 2. Operating Mode Read/Write (MD)
        elif code == "MD":
            if len(command_str) > 3:  # Writing mode e.g., MD12;
                self.mode = command_str[2:4]
                return ""
            else:  # Reading mode e.g., MD;
                return f"MD{self.mode};"

        # 3. Transmit/Receive State (TX / RX)
        elif code == "TX":
            print("Virtual Rig: Transmitting PTT Active!")
            return ""
        elif code == "RX":
            print("Virtual Rig: Receiving/Idle State!")
            return ""

        # Unknown commands fallback with an empty response
        return ""
