import json

def load_patterns(config_file):
    # Open and read the configuration file
    with open(config_file, 'r') as file:
        config = json.load(file)
    
    # Retrieve the 'ignore_patterns' from the configuration, defaulting to an empty list if not found
    patterns = config.get('ignore_patterns', [])
    processed_patterns = []

    # Process each pattern object in the 'ignore_patterns' list
    for pattern_obj in patterns:
        # Get the pattern string, defaulting to an empty string if not found
        pattern = pattern_obj.get("pattern", "")
        # Check if the pattern is a regular expression, defaulting to False if not found
        is_regex = pattern_obj.get("is_regex", False)
        # Add the processed pattern to the list
        processed_patterns.append({"pattern": pattern, "is_regex": is_regex})
    
    # Return the processed ignore patterns and the 'only_patterns' from the configuration
    return processed_patterns, config.get('only_patterns', [])
