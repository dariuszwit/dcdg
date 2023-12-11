import os
import shutil

def generate_html_start(combined_html, directory):
    # Create the path to the "style.css" file in the source directory
    style_source_path = 'css/style.css'

    # Create the target path to the "css" folder in the output directory
    style_target_directory = os.path.join(directory, 'css')

    # Create the "css" folder in the output directory if it doesn't exist
    os.makedirs(style_target_directory, exist_ok=True)

    # Create the target path for the "style.css" file in the "css" folder
    style_target_path = os.path.join(style_target_directory, 'style.css')

    # Copy the "style.css" file to the "css" folder in the output directory
    shutil.copy(style_source_path, style_target_path)

    # Write the HTML starting tags and link the stylesheet
    combined_html.write(f"""
    <html>
    <head>
        <title>Combined Content</title>
        <link rel="stylesheet" type="text/css" href="{os.path.join('css', 'style.css')}">
    </head>
    <body>
    <div class='container'>
    """)

def generate_html_end(combined_html):
    # Write the HTML ending tags
    combined_html.write("""
    </div></body></html>
    """)
