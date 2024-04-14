import base64
from io import BytesIO
from pathlib import Path
from typing import List

import fitz
import numpy as np
import requests
from fitz import Pixmap
from PIL import Image


class PDFHandler:
    def __init__(self, api_key, single_query=False) -> None:
        self.api_key = api_key
        self.single_query = single_query

    def _pixmap_to_image(self, pixmap: Pixmap) -> np.ndarray:
        raw_data = pixmap.samples
        image = np.frombuffer(raw_data, dtype=np.uint8)
        image = image.reshape((pixmap.height, pixmap.width, 3))
        return image

    def _request(self, messages):
        payload = {
            "model": "gpt-4-turbo",
            "messages": messages,
            "max_tokens": 300,
        }
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}",
        }
        response = requests.post(
            "https://api.openai.com/v1/chat/completions", headers=headers, json=payload
        )
        # print(json.dumps(messages, indent=4))
        if response.status_code == 200:
            result = response.json()
        else:
            print("Error:", response.status_code, response.text)
            result = None
        return result

    def _summarize_image(self, images: List[np.ndarray]) -> str:
        def to_b64(image: np.ndarray) -> str:
            # Convert the numpy array to a Pillow image
            image_pil = Image.fromarray(image.astype("uint8"))

            # Convert the image to a base64 string
            with BytesIO() as buffer:
                image_pil.save(buffer, format="JPEG")
                img_str = base64.b64encode(buffer.getvalue()).decode("utf-8")
                return img_str

        images_b64 = [to_b64(image) for image in images]
        if self.single_query:
            prompt = {
                "type": "text",
                "text": """
                        You're a judge in a hackathon looking at images of slides from the final presentation of the demos.
                        Summarize the slide content concisely, such that you can user it later on with the text and summarizations
                        from the other slides.
                        """,
            }
            content = [
                {
                    "type": "image_url",
                    "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"},
                }
                for base64_image in images_b64
            ]
            content.insert(0, prompt)
            result = self._request(
                messages=[
                    {
                        "role": "user",
                        "content": content,
                    }
                ]
            )
            results = [result] * len(images_b64)  # TODO: hacky
        else:
            prompt = {
                "type": "text",
                "text": """
                        You're a judge in a hackathon looking at an image of a slide from the final presentation of the demos.
                        Summarize the slide content concisely, such that you can user it later on with the text and summarizations
                        from the other slides.
                        """,
            }
            results = []
            for base64_image in images_b64:
                messages = [
                    {
                        "role": "user",
                        "content": [
                            prompt,
                            {
                                "type": "image_url",
                                "image_url": {
                                    "url": f"data:image/jpeg;base64,{base64_image}"
                                },
                            },
                        ],
                    }
                ]
                result = self._request(messages)
                results.append(result)
        return results

    def extract_information_from_pdf(self, pdf_path):
        pdf_document = fitz.open(pdf_path)
        contents = {}
        for page_number in range(pdf_document.page_count):
            page = pdf_document.load_page(page_number)
            text = page.get_text()
            if not bool(text.strip()):  # no text on page
                image = self._pixmap_to_image(page.get_pixmap())
                # cv2.imwrite(f"{page_number}.jpg", image)
                contents[page_number] = image
            else:  # some text on page
                contents[page_number] = text
        pdf_document.close()

        images = [image for image in contents.values() if isinstance(image, np.ndarray)]
        image_summaries = self._summarize_image(images)
        for page_number, content in contents.items():
            if isinstance(content, np.ndarray):
                contents[page_number] = image_summaries.pop(0)
        return contents


if __name__ == "__main__":
    # pdf_path = 'misc/samples/pitchdeck.pdf'
    input_folder = Path("misc/samples")
    pdfs = list(input_folder.glob("*.pdf"))
    print(pdfs)
    handler = PDFHandler("", single_query=False)
    contents = handler.extract_information_from_pdf(pdfs[0])
    for i, text in contents.items():
        print(i, text[:20])
