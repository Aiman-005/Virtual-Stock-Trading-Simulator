import re
from hash_map import HashMap
from password_utils import PasswordUtils

class UserNode:
    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.password = password
        self.dummy_balance = 10000  # Starting balance for dummy trading
        self.dummy_portfolio = HashMap()  # Manual HashMap for storing stocks
        self.undo_stack = None      # Will be initialized by DummyTrader
        self.redo_stack = None      # Will be initialized by DummyTrader
        self.next = None


class UserLinkedList:
    
    def __init__(self):
        self.head = None
        self.pwd_utils = PasswordUtils()
    
    def add_user(self, username, email, password):     
        # Check if username already exists
        if self.find_user(username):
            return False
        
        # Hash the password before storing
        hashed_password = self.pwd_utils.hash_password(password)
        
        # Create new user node with hashed password
        new_node = UserNode(username, email, hashed_password)
        
        # Add at beginning
        new_node.next = self.head
        self.head = new_node
        return True
    
    def find_user(self, username):
        current = self.head
        while current:
            if current.username == username:
                return current
            current = current.next
        return None
    
    def authenticate(self, username, password):
        user = self.find_user(username)
        if user:
            # Verify hashed password
            if self.pwd_utils.verify_password(password, user.password):
                return user
        return None

def is_valid_email(email):
   
    pattern = r'^[a-zA-Z0-9._%+-]+@gmail\.com$'
    return re.match(pattern, email) is not None


def is_valid_username(username):
    
    if not username or len(username) < 3:
        return False
    if not username[0].isalpha():
        return False
    if not all(c.isalnum() or c == '_' for c in username):
        return False
    return True

def signup(user_list, storage):
    
    print("\n" + "="*60)
    print("📝 SIGN UP - CREATE NEW ACCOUNT")
    print("="*60)
    
    pwd_utils = PasswordUtils()
    
    # Email validation
    for attempt in range(3):
        email = input("Enter your Gmail address: ")
        if is_valid_email(email):
            break
        print(f"❌ Invalid email. Attempt {attempt + 1}/3")
        if attempt == 2:
            print("⚠️  Maximum attempts reached.")
            return None
    
    # Username validation
    for attempt in range(3):
        username = input("Enter username (min 3 chars, start with letter): ")
        if is_valid_username(username):
            # Check in memory AND in file
            if not user_list.find_user(username) and not storage.user_exists(username):
                break
            else:
                print(f"❌ Username already exists!")
        else:
            print(f"❌ Invalid username. Attempt {attempt + 1}/3")
        
        if attempt == 2:
            print("⚠️  Maximum attempts reached.")
            return None
    
    # Password validation with masking
    for attempt in range(3):
        password = pwd_utils.get_password_masked("Enter password: ")
        confirm = pwd_utils.get_password_masked("Confirm password: ")
        if password == confirm:
            break
        print(f"❌ Passwords don't match. Attempt {attempt + 1}/3")
        if attempt == 2:
            print("⚠️  Maximum attempts reached.")
            return None
    
    # Creationn
    if user_list.add_user(username, email, password):
        user_node = user_list.find_user(username)
        
        # Save to file
        storage.save_user(user_node)
        
        print(f"\n✅ Account created successfully!")
        print(f"🎉 Welcome aboard, {username}!")
        return user_node
    else:
        print("❌ Failed to create account.")
        return None


def login(user_list):
    """Login existing user"""
    print("\n" + "="*60)
    print("🔐 LOGIN TO YOUR ACCOUNT")
    print("="*60)
    
    pwd_utils = PasswordUtils()
    
    for attempt in range(3):
        username = input("Username: ")
        password = pwd_utils.get_password_masked("Password: ")
        
        user = user_list.authenticate(username, password)
        if user:
            print(f"\n✅ Welcome back, {username}!")
            return user
        
        print(f"❌ Invalid credentials. Attempt {attempt + 1}/3")
        if attempt == 2:
            print("⚠️  Maximum login attempts reached.")
            return None
    
    return None