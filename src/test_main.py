import unittest
import os
import tempfile
from main import extract_title, copy_content, generate_page

class TestGeneratePage(unittest.TestCase):
    def test_copy_content_copies_assets_to_selected_destination(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            source_dir = os.path.join(temp_dir, "static")
            destination_dir = os.path.join(temp_dir, "docs")
            os.makedirs(os.path.join(source_dir, "images"))
            os.makedirs(destination_dir)

            with open(os.path.join(source_dir, "images", "logo.png"), "wb") as asset:
                asset.write(b"image data")
            with open(os.path.join(destination_dir, "stale.txt"), "w") as stale_file:
                stale_file.write("stale")

            copy_content(source_dir, destination_dir)

            copied_asset = os.path.join(destination_dir, "images", "logo.png")
            self.assertTrue(os.path.isfile(copied_asset))
            with open(copied_asset, "rb") as asset:
                self.assertEqual(asset.read(), b"image data")
            self.assertFalse(os.path.exists(os.path.join(destination_dir, "stale.txt")))

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

    def test_generate_page_prefixes_root_relative_assets_with_basepath(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            markdown_path = os.path.join(temp_dir, "index.md")
            template_path = os.path.join(temp_dir, "template.html")
            destination_path = os.path.join(temp_dir, "public", "index.html")

            with open(markdown_path, "w", encoding="utf-8") as markdown_file:
                markdown_file.write("# Title")
            with open(template_path, "w", encoding="utf-8") as template_file:
                template_file.write(
                    '<link href="/index.css"><img src="/images/logo.png">'
                )

            generate_page(markdown_path, template_path, destination_path, "/project/")

            with open(destination_path, "r", encoding="utf-8") as output_file:
                generated_html = output_file.read()

        self.assertIn('href="/project/index.css"', generated_html)
        self.assertIn('src="/project/images/logo.png"', generated_html)