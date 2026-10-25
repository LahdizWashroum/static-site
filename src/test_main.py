import unittest
import os
import tempfile
from main import extract_title, copy_content, generate_page

class TestGeneratePage(unittest.TestCase):
    def test_extract_title(self):
        markdown = """
        # My Title

        This is some content.
        """
        title = extract_title(markdown)
        self.assertEqual(title, "My Title")

    def test_generate_page_separates_html_blocks(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            markdown_path = os.path.join(temp_dir, "index.md")
            template_path = os.path.join(temp_dir, "template.html")
            destination_path = os.path.join(temp_dir, "public", "index.html")

            with open(markdown_path, "w", encoding="utf-8") as markdown_file:
                markdown_file.write("# Title\n\nFirst paragraph.\n\nSecond paragraph.")
            with open(template_path, "w", encoding="utf-8") as template_file:
                template_file.write("<article>\n      {{ Content }}\n    </article>")

            generate_page(markdown_path, template_path, destination_path)

            with open(destination_path, "r", encoding="utf-8") as output_file:
                generated_html = output_file.read()

        self.assertIn(
            "<article>\n      <h1>Title</h1>\n      <p>First paragraph.</p>\n"
            "      <p>Second paragraph.</p>\n    </article>",
            generated_html,
        )