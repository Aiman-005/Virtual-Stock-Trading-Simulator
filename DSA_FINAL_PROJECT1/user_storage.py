import os
import json


class UserStorage:
    """Handle saving and loading user data to/from files"""
    
    def __init__(self):
        self.users_dir = "users_data"
        self.credentials_file = "users_data/credentials.txt"
        self.initialize()
    
    def initialize(self):
        """Create users_data directory if it doesn't exist"""
        if not os.path.exists(self.users_dir):
            os.makedirs(self.users_dir)
            print(f"✅ Created {self.users_dir} directory")
        
        if not os.path.exists(self.credentials_file):
            with open(self.credentials_file, 'w') as f:
                f.write("")  # Create empty file
            print(f"✅ Created credentials file")
    
    def _hashmap_to_dict(self, hashmap):
        """Helper: Convert HashMap to Python dict for JSON serialization"""
        result = {}
        if hasattr(hashmap, 'items'):
            items = hashmap.items()
            for i in range(len(items)):
                key, value = items[i]
                result[key] = value
        return result
    
    def _dict_to_hashmap(self, data_dict, hashmap):
        """Helper: Load dict data into HashMap"""
        for key, value in data_dict.items():
            hashmap.put(key, value)
    
    def save_user(self, user_node):
        """
        Save user data to file
        Creates: users_data/{username}.txt with all user info
        Updates: users_data/credentials.txt with username:email:hashed_password
        """
        # Save to credentials file (append) - password is already hashed
        with open(self.credentials_file, 'a') as f:
            f.write(f"{user_node.username}:{user_node.email}:{user_node.password}\n")
        
        # Save user's personal file
        user_file = os.path.join(self.users_dir, f"{user_node.username}.txt")
        
        # Convert portfolio HashMap to dict ONLY for JSON serialization
        portfolio_dict = self._hashmap_to_dict(user_node.dummy_portfolio)
        
        # We must use dict here for JSON.dump() - but only temporarily
        user_data = {
            "username": user_node.username,
            "email": user_node.email,
            "password": user_node.password,  # Already hashed
            "balance": user_node.dummy_balance,
            "portfolio": portfolio_dict
        }
        
        with open(user_file, 'w') as f:
            json.dump(user_data, f, indent=4)
        
        print(f"✅ User data saved (password hashed)")

    
    def load_all_users(self, user_list):
        """
        Load all users from credentials file into UserLinkedList
        Returns: number of users loaded
        Note: Passwords are already hashed in files
        """
        if not os.path.exists(self.credentials_file):
            return 0
        
        count = 0
        with open(self.credentials_file, 'r') as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                
                parts = line.split(':')
                if len(parts) == 3:
                    username, email, hashed_password = parts
                    
                    # Load user's personal data
                    user_file = os.path.join(self.users_dir, f"{username}.txt")
                    
                    if os.path.exists(user_file):
                        with open(user_file, 'r') as uf:
                            # JSON loading gives us a dict, but we minimize its use
                            user_data = json.load(uf)
                        
                        # Create user node directly (password already hashed)
                        from authentication import UserNode
                        user_node = UserNode(username, email, hashed_password)
                        
                        # Add to linked list manually
                        user_node.next = user_list.head
                        user_list.head = user_node
                        
                        # Restore balance
                        user_node.dummy_balance = user_data.get("balance", 10000)
                        
                        # Restore portfolio - convert dict back to HashMap
                        portfolio_data = user_data.get("portfolio", {})
                        self._dict_to_hashmap(portfolio_data, user_node.dummy_portfolio)
                        
                        count += 1
        
        return count
    
    def update_user(self, user_node):
        """Update existing user's data file (password already hashed)"""
        user_file = os.path.join(self.users_dir, f"{user_node.username}.txt")
        
        # Convert portfolio HashMap to dict ONLY for JSON serialization
        portfolio_dict = self._hashmap_to_dict(user_node.dummy_portfolio)
        
        # Must use dict temporarily for JSON.dump()
        user_data = {
            "username": user_node.username,
            "email": user_node.email,
            "password": user_node.password,  # Already hashed
            "balance": user_node.dummy_balance,
            "portfolio": portfolio_dict
        }
        
        with open(user_file, 'w') as f:
            json.dump(user_data, f, indent=4)
    
    def user_exists(self, username):
        """Check if username already exists in credentials file"""
        if not os.path.exists(self.credentials_file):
            return False
        
        with open(self.credentials_file, 'r') as f:
            for line in f:
                parts = line.split(':')
                if len(parts) >= 1 and parts[0] == username:
                    return True
        
        return False