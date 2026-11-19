import re


class OCRNormalizer:
    @staticmethod
    def normalize_text(raw_text: str) -> str:
        """Cleans typical OCR transcription noise and standardizes currency symbols."""
        text = raw_text.replace("\r\n", "\n").replace("\r", "\n")
        # Standardize common currency symbols
        text = text.replace("US$", "$").replace("USD ", "$")
        # Clean double spaces
        text = re.sub(r"[ \t]+", " ", text)
        # Clean repetitive empty lines
        text = re.sub(r"\n{3,}", "\n\n", text)
        return text.strip()

