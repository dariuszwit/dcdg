import os
import re

def should_process(file_path, ignore_patterns, only_patterns, mode, base_directory):
    def match_pattern(file_path, patterns):
        for pattern_obj in patterns:
            pattern = pattern_obj["pattern"]
            is_regex = pattern_obj["is_regex"]
            if is_regex:
                # Check if the file path matches the regex pattern
                if re.search(pattern, file_path):
                    return True
            else:
                # Create a relative path from the base directory
                relative_path = os.path.relpath(file_path, base_directory)
                # Check if the pattern exists in the relative path
                if pattern in relative_path:
                    return True
        return False

    # If mode is 'all' or 'ignore', process the file unless it matches ignore patterns
    if mode in ["all", "ignore"]:
        return not match_pattern(file_path, ignore_patterns)
    # If mode is 'only', process the file only if it matches only patterns
    elif mode == "only":
        return match_pattern(file_path, only_patterns)
    # For other modes, do not process the file
    return False
