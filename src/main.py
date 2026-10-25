from textnode import TextNode
from textnode import TextType
from htmlnode import LeafNode, ParentNode, HTMLNode
from block import markdown_to_html_nodes
import os
import sys

def main():
    # Use sys.argv to get the first CLI as the basepath. If none is provided, default to /
    basepath = sys.argv[1] if len(sys.argv) > 1 else "/"
    text_node = TextNode("Hello, World!", TextType.PLAIN, None)
    print(text_node)
    copy_content(destination_dir="docs")
    generate_pages_recursive("content", "template.html", "docs", basepath)

def copy_content(source_dir="static", destination_dir="public"):
    # Copy all files and subdirectories, replacing any existing destination contents.
    
    # Delete all contents of the destination directory
    if os.path.exists(destination_dir):
        for root, dirs, files in os.walk(destination_dir, topdown=False):
            for name in files:
                os.remove(os.path.join(root, name))
            for name in dirs:
                os.rmdir(os.path.join(root, name))
    
    # Copy all contents from source to destination
    for root, dirs, files in os.walk(source_dir):
        for name in files:
            source_file = os.path.join(root, name)
            relative_path = os.path.relpath(source_file, source_dir)
            destination_file = os.path.join(destination_dir, relative_path)

            # Create destination directory if it doesn't exist
            os.makedirs(os.path.dirname(destination_file), exist_ok=True)

            # Copy the file
            with open(source_file, 'rb') as src_file:
                with open(destination_file, 'wb') as dest_file:
                    dest_file.write(src_file.read())
    
def extract_title(markdown: str) -> str:
    # Extract the title from the markdown content. The title is defined as the first line that starts with a '#' character.
    lines = markdown.splitlines()
    for line in lines:
        stripped_line = line.strip()
        if stripped_line.startswith('#'):
            return stripped_line.lstrip('#').strip()
    return "Untitled"

def generate_page(from_path, template_path, dest_path, basepath="/") -> None:
    #Print a message like "Generating page from from_path to dest_path using template_path".
    #Read the markdown file at from_path and store the contents in a variable.
    #Read the template file at template_path and store the contents in a variable.
    #Use your markdown_to_html_node function and .to_html() method to convert the markdown file to an HTML string.
    #Use the extract_title function to grab the title of the page.
    #Replace the {{ Title }} and {{ Content }} placeholders in the template with the HTML and title you generated.
    #Write the new full HTML page to a file at dest_path. Be sure to create any necessary directories if they don't exist.

    print(f"Generating page from {from_path} using template {template_path} to {dest_path}")
    # Read the markdown file
    with open(from_path, 'r', encoding='utf-8') as f:
        markdown_content = f.read()
    
    # Read the template file
    with open(template_path, 'r', encoding='utf-8') as f:
        template_content = f.read()

    # Convert markdown to HTML
    html_nodes = markdown_to_html_nodes(markdown_content)
    html_content = "\n      ".join(node.to_html() for _, node in html_nodes)
    
    # Extract the title
    title = extract_title(markdown_content)

    # Replace placeholders in the template
    final_html = template_content.replace("{{ Title }}", title).replace("{{ Content }}", html_content)
    final_html = final_html.replace('href="/', f'href="{basepath}').replace(
        'src="/', f'src="{basepath}'
    )

    # Write the final HTML to the destination file
    os.makedirs(os.path.dirname(dest_path), exist_ok=True)
    with open(dest_path, 'w', encoding='utf-8') as f:
        f.write(final_html)

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path, basepath="/"):
    # Recursively generate pages for all markdown files in the content directory.
    # For each markdown file, generate a corresponding HTML file in the destination directory.
    # Maintain the same directory structure in the destination directory as in the content directory.

    for root, dirs, files in os.walk(dir_path_content):
        for file in files:
            if file.endswith('.md'):
                # Construct full paths
                from_path = os.path.join(root, file)
                relative_path = os.path.relpath(from_path, dir_path_content)
                dest_path = os.path.join(dest_dir_path, os.path.splitext(relative_path)[0] + '.html')

                # Generate the page
                generate_page(from_path, template_path, dest_path, basepath)

if __name__ == "__main__":
    main()