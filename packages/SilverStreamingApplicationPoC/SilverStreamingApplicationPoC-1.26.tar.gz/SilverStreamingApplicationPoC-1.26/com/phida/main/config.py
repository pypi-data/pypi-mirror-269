# Define a dictionary to store global configurations
global_config = {}

# Function to set a configuration variable
def set_config(key, value):
    global global_config
    global_config[key] = value

# Function to get a configuration variable
def get_config(key):
    global global_config
    return global_config.get(key)
