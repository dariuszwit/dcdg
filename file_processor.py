import os
import html
import re

def create_html_content(file_path, relative_path, content, html_file_id, file_size):
    # Escape HTML special characters in the content to prevent rendering issues
    safe_content = html.escape(content)

    # Format the file content as HTML
    return f"""
    <div class='file-content' id='{html_file_id}'>
        <h2><a href='#{html_file_id}'>{relative_path} ({file_size} bytes)</a></h2>
        <button class='copy-button' onclick='copyToClipboard(`{html_file_id}`)'>📋</button>
        <pre><code>{safe_content}</code></pre>
    </div>
    """

def process_file(file_path, relative_path, combined_txt, combined_html, mode):
    # Try to open and read file content with utf-8 encoding
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
    # If utf-8 decoding fails, try ISO-8859-1 encoding
    except UnicodeDecodeError:
        with open(file_path, 'r', encoding='ISO-8859-1') as file:
            content = file.read()

    # Get the size of the file
    file_size = os.path.getsize(file_path)

    # Generate a unique HTML ID for each file
    html_file_id = relative_path.replace(os.sep, "_").replace('.', '_')

    # Write file details and content to the combined text file
    combined_txt.write(f"----- {relative_path} ({file_size} bytes) -----\n{content if mode != 'size_only' else ''}\n\n")

    # Write the formatted HTML content
    combined_html.write(create_html_content(file_path, relative_path, content, html_file_id, file_size))
