import sys
import os

class PasswordUtils:
    
    def __init__(self):
        pass
    
    def hash_password(self, password):
        
        # Convert password to bytes if string
        if isinstance(password, str):
            password_bytes = [ord(c) for c in password]
        else:
            password_bytes = password
        
        # Constants for hashing
        prime = 31
        mod = 2**32
        
        # First pass: polynomial hash
        hash1 = 0
        for i, byte in enumerate(password_bytes):
            hash1 = (hash1 * prime + byte) % mod
        
        # Second pass: reverse polynomial hash
        hash2 = 0
        for i, byte in enumerate(reversed(password_bytes)):
            hash2 = (hash2 * prime + byte) % mod
        
        # Third pass: XOR with position-based weights
        hash3 = 0
        for i, byte in enumerate(password_bytes):
            hash3 ^= (byte << (i % 8)) | (byte >> (8 - i % 8))
            hash3 = hash3 % mod
        
        # Combine all three hashes
        combined = (hash1 ^ hash2 ^ hash3) % mod
        
        # Multiple rounds of mixing for better distribution
        for round_num in range(5):
            combined = self._mix_bits(combined, round_num)
        
        # Extend hash to make it longer (more secure-looking)
        extended_hash = ""
        for i in range(8):
            segment = combined
            for j in range(i):
                segment = self._mix_bits(segment, j)
            extended_hash += hex(segment)[2:].zfill(8)
        
        return extended_hash[:64]  # Return 64-character hash
    
    def _mix_bits(self, value, round_num):
        """
        Mix bits for better distribution
        Uses bit rotation and XOR operations
        """
        mod = 2**32
        
        # Rotate bits
        rotated = ((value << 7) | (value >> 25)) & (mod - 1)
        
        # XOR with round constant
        round_constant = (round_num * 0x9e3779b9) % mod
        mixed = rotated ^ round_constant
        
        # Additional mixing
        mixed = (mixed * 0x85ebca6b) % mod
        mixed = mixed ^ (mixed >> 13)
        mixed = (mixed * 0xc2b2ae35) % mod
        mixed = mixed ^ (mixed >> 16)
        
        return mixed % mod
    
    def verify_password(self, input_password, stored_hash):
      
        input_hash = self.hash_password(input_password)
        return input_hash == stored_hash
    
    def get_password_masked(self, prompt="Password: "):
       
        print(prompt, end='', flush=True)
        password = ""
        
        # Detect operating system
        if os.name == 'nt':  # Windows
            try:
                import msvcrt
                while True:
                    char = msvcrt.getch()
                    
                    # Enter key pressed (Windows: \r or \n)
                    if char in (b'\r', b'\n'):
                        print()  # New line after password
                        break
                    
                    # Backspace pressed
                    elif char == b'\x08':
                        if len(password) > 0:
                            password = password[:-1]
                            # Erase the asterisk: move back, print space, move back again
                            sys.stdout.write('\b \b')
                            sys.stdout.flush()
                    
                    # Ctrl+C pressed
                    elif char == b'\x03':
                        print()
                        raise KeyboardInterrupt
                    
                    # Normal character
                    else:
                        try:
                            decoded = char.decode('utf-8')
                            password += decoded
                            sys.stdout.write('*')  # Print asterisk
                            sys.stdout.flush()
                        except UnicodeDecodeError:
                            pass  # Ignore non-UTF8 characters
                
                return password
                
            except ImportError:
                # msvcrt not available, fallback to basic input
                import getpass
                return getpass.getpass("")
        
       
