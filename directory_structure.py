import os
from tqdm import tqdm
from pattern_utils import should_process

def create_directory_structure(directory, ignore_patterns, only_patterns, mode, combined_html, combined_txt):
    tree = {}
    base_directory = os.path.abspath(directory)

    # Traverse the directory structure
    for root, dirs, files in tqdm(os.walk(directory), desc="Processing Files"):
        # Filter directories and files according to specified patterns
        dirs[:] = [d for d in dirs if should_process(os.path.join(root, d), ignore_patterns, only_patterns, mode, base_directory)]
        files = [f for f in files if should_process(os.path.join(root, f), ignore_patterns, only_patterns, mode, base_directory)]

        # Add filtered directories and files to the tree
        tree[root] = {'dirs': dirs, 'files': files}

    def create_text_tree_html(path, node, prefix=''):
        # Generate the HTML representation of the directory tree
        html = ''
        for dir in sorted(node['dirs']):
            dir_path = os.path.join(path, dir)
            html += f"{prefix}{dir}/\n"
            if dir_path in tree:
                html += create_text_tree_html(dir_path, tree[dir_path], prefix + '    ')
        for file in sorted(node['files']):
            file_path = os.path.join(path, file)
            file_size_bytes = os.path.getsize(file_path)
            file_size_mb = bytes_to_mb(file_size_bytes)
            html += f"{prefix}{file} ({file_size_mb:.2f} MB)\n"
        return html

    def bytes_to_mb(size_in_bytes):
        # Convert bytes to megabytes
        return size_in_bytes / (1024 * 1024)

    def create_table_of_contents_html(tree, base_directory):
        # Create HTML table of contents
        html = '<div id="table-of-contents" class="content-block file-content">\n'
        html += '<h2>Table of Contents</h2>\n'
        html += '<button class="copy-button" onclick="copyToClipboard(\'teble-of-contents\')">&#128203;</button>\n'
        html += '<pre id="teble-of-contents">\n<code>\n'
        for path, content in tree.items():
            rel_path = os.path.relpath(path, base_directory)
            for file in sorted(content['files']):
                file_id = file.replace('.', '_')  # Create unique ID
                html += f"<li><a href='#{file_id}'>{rel_path}/{file}</a></li>\n"
        html += '\n</code>\n</pre>\n</div>\n'
        return html
        
    # Add JavaScript script for copying text
    copy_script = """
    <script>
    function copyToClipboard(elementId) {
        var copyText = document.getElementById(elementId);
        var textArea = document.createElement("textarea");
        textArea.value = copyText.textContent;
        document.body.appendChild(textArea);
        textArea.select();
        document.execCommand("Copy");
        textArea.remove();
    }
    </script>
    """

    # Create HTML structure and write to file
    combined_html.write('<div class="content">\n')
    combined_html.write(create_table_of_contents_html(tree, base_directory))
    combined_html.write('</div>\n')

    # Create HTML tree of files and write to file
    combined_html.write('<div class="directory-tree content-block file-content">\n')
    combined_html.write('<h2>Tree of Files</h2>\n')
    combined_html.write('<button class="copy-button" onclick="copyToClipboard(\'tree-content\')">&#128203;</button>\n')
    combined_html.write('<pre id="tree-content" class="file-content">\n')  
    # Apply the same class as the file code sections
    combined_html.write('<code>\n')
    combined_html.write(create_text_tree_html(directory, tree[directory], ''))
    combined_html.write('</code>\n')
    combined_html.write('</pre>\n')
    combined_html.write('</div>\n')
    combined_html.write(copy_script)

    # Write the directory structure to a TXT file
    combined_txt.write("Directory Tree:\n")
    combined_txt.write(create_text_tree_html(directory, tree[directory], ''))
    combined_txt.write("\n\n")

# Sample invocation (ensure it fits your code in main.py)
if __name__ == "__main__":
    # Example of opening files before calling the function
    with open('combined.html', 'w') as combined_html, open('combined.txt', 'w') as combined_txt:
        create_directory_structure('./', ignore_patterns, only_patterns, 'all', combined_html, combined_txt)
