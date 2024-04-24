# you can run this test from project root folder as: python -m unittest tests.test_presentation_processor
# or set pythonpath and then run this test from inside tests folder as: python -m unittest test_presentation_processor

import json
import logging

class PresentationProcessor:
    def __init__(self):#, file_path):
        #self.file_path = file_path
        pass

    def text_to_json(self, text):
        """
        Converts a structured text representation of slides into a JSON format.

        This method parses each line of the given text, constructing a dictionary
        for each slide with details about the slide's title, content, and associated images.
        Each slide is detected by lines marked with '**' at the start and end of the title.
        Additional details such as image paths and captions are handled by `parse_line`.

        Args:
            text (str): A string containing the structured text of slides, where each slide's
                        title is enclosed in double asterisks '**', and content and images
                        are listed under the title with '-' at the beginning of each line.

        Returns:
            str: A string in JSON format representing the list of slides, where each slide is
                a dictionary containing the title, content, and a list of images with their
                paths and optional captions. For example:
    
        Notes:
            - The method assumes that each slide's content follows immediately after its title and that each new slide starts with a title line marked by '**'.
            - Images and captions are expected to follow a specific format with '-' indicating new items.
            - The last slide is appended after the loop if it contains content or images.
        """
        slides, current_slide, current_images = [], None, []
        for line in text.split('\n'):
            line = line.strip()
            if not line:
                continue
            if '**' in line:  # Starting new slide
                if current_slide:  # Save the current slide before starting a new one
                    if current_images:
                        current_slide['images'] = current_images
                    slides.append(current_slide)
                title = line.split('**')[1]
                current_slide = {'title': title, 'content': ''}
                current_images = []  # Reset images for the new slide
            else:
                self.parse_line(line, current_slide, current_images)
        if current_slide:  # Don't forget to save the last slide
            if current_images:
                current_slide['images'] = current_images
            slides.append(current_slide)
        return json.dumps({'slides': slides}, indent=4)

    def parse_line(self, line, current_slide, current_images):
        """
        Parses a single line of text to update the current slide or images list.

        This method handles the content of the slide based on prefixes in the line:
        - Lines starting with '-' are considered as content.
        - Lines containing 'Image:' initiate a new image object.
        - Lines containing 'Caption:' add a caption to the last image in the list.
        - Lines containing 'ImageLayout:' specify the layout of images on the slide.

        Args:
            line (str): The line of text to be parsed.
            current_slide (dict): The dictionary representing the current slide being processed.
            current_images (list): A list of image dictionaries associated with the current slide.

        Side Effects:
            - Modifies current_slide by adding content directly.
            - Modifies current_images by adding new images or updating existing ones with captions or layouts.
        """
        line = line.strip()
        if line.startswith('-'):
            content = line[1:].strip()
            if 'Image:' in content and not any(img['path'] == content.split('Image:')[1].strip() for img in current_images):
                self.handle_image(content, current_images)
            elif 'Caption:' in content and current_images:
                if current_images[-1].get('caption') is None:
                    self.handle_caption(content, current_images)
            elif 'ImageLayout:' in content:
                self.handle_layout(content, current_slide)
            else:
                current_slide['content'] += content + '\n'
    
    def handle_image(self, content, current_images):
        """
        Extracts the image path from the content and appends a new image dictionary to current_images.

        Args:
            content (str): The content string containing the image path.
            current_images (list): The list of images currently associated with the slide.

        Side Effects:
            - Appends a new dictionary with the image path to the current_images list.
        """
        image_info = {'path': content.split('Image:')[1].strip()}
        current_images.append(image_info)


    def handle_caption(self, content, current_images):
        """
        Adds a caption to the last image in the current_images list, if any images exist.

        Args:
            content (str): The content string containing the caption.
            current_images (list): The list of images currently associated with the slide.

        Side Effects:
            - Modifies the last dictionary in current_images by adding a caption key-value pair.
        """
        if current_images and 'caption' not in current_images[-1]:
            current_images[-1]['caption'] = content.split('Caption:')[1].strip()

    def handle_layout(self, content, current_slide):
        """
        Sets the image layout for the current slide based on the specified layout content.

        Args:
            content (str): The content string containing layout specifications.
            current_slide (dict): The dictionary representing the current slide being processed.

        Side Effects:
            - Modifies current_slide by adding or updating the 'imagelayout' key with the specified layout.
        """
        layout = list(map(int, content.split('ImageLayout:')[1].strip().split(',')))
        current_slide['imagelayout'] = layout

    def json_to_text(self, json_input):
        """
        Convert JSON representation of slides back to a structured text format.
        
        Args:
            json_input (str): JSON string of slides data.
        
        Returns:
            str: Structured text representation of the JSON data.
        """
        try:
            data = json.loads(json_input)
        except json.JSONDecodeError as e:
            logging.error("Invalid JSON provided: %s", e)
            return "Invalid JSON"

        slides_text = []
        for idx, slide in enumerate(data['slides'], 1):
            slides_text.append(f"{idx}. **{slide['title']}**:")
            if slide['content'].strip():
                slides_text.extend([f"   - {line.strip()}" for line in slide['content'].strip().split('\n')])
            for image in slide.get('images', []):
                slides_text.append(f"   - Image: {image['path']}")
                if 'caption' in image:
                    slides_text.append(f"   - Caption: {image['caption']}")
            if 'imagelayout' in slide:
                layout = ','.join(map(str, slide['imagelayout']))
                slides_text.append(f"   - ImageLayout: {layout}")
            slides_text.append("")

        return '\n'.join(slides_text).strip()

    def read_text_from_file(self, file_path):
        """
        Read text from a file specified by the file_path attribute.

        Args:
            file_path (str): Path of text file.
    
        Returns:
            str: The content of the file as a string.
        Raises:
            FileNotFoundError: If the file does not exist.
            IOError: If an I/O error occurs when opening the file.
        """
        try:
            with open(file_path, 'r') as file:
                return file.read()
        except FileNotFoundError:
            logging.error(f"The file '{file_path}' does not exist.")
            raise
        except IOError as e:
            logging.error(f"Error reading file {file_path}: {e}")
            raise


    def save_to_file(self, data, filename):
        try:
            with open(filename, 'w') as file:
                file.write(data)
            logging.info(f"Data successfully saved to {filename}")
            return True  # Explicitly return True on success
        except IOError as e:
            logging.error(f"Failed to save data to {filename}: {e}")
            return False  # Explicitly return False on failure

# # This setup ensures each image and its caption are treated as separate and linked only if they are correctly sequential in the text. This avoids overwriting or duplicating the image or caption fields.
# # Example usage
# processor = PresentationProcessor('presentation.txt')
# text_content = processor.read_text_from_file()
# if text_content:
#     # Generate JSON from the text content
#     presentation_json = processor.text_to_json(text_content)
#     # Save the generated JSON to a file
#     if processor.save_to_file(presentation_json, 'presentation.json'):
#         print("JSON saved successfully.")

#     # Convert JSON back to original text format
#     original_text = processor.json_to_text(presentation_json)
#     # Save the original text to a file
#     if processor.save_to_file(original_text, "restored_presentation.txt"):
#         print("Text file also saved successfully.")
# else:
#     print("No content to process.")
