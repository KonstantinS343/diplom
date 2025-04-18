import difflib


class TranslationQualityService:
    """
    Service to handle translation quality checks.
    """

    async def highlight_differences(self, user_text: str, model_text: str) -> dict:
        """
        Highlight differences between user and model translations.
        """

        # Highlight differences
        highlighted_text = await self.add_difference_tokens(user_text, model_text)

        return {
            "user_text": user_text,
            "model_text": model_text,
            "highlighted_text": highlighted_text,
            "similarity": difflib.SequenceMatcher(None, user_text, model_text).ratio(),
        }

    async def add_difference_tokens(self, user_text: str, model_text: str) -> str:
        """
        Add special tokens to highlight differences between two texts.
        """
        user_words = user_text.strip().split()
        model_words = model_text.strip().split()

        differ = difflib.Differ()
        diff = list(differ.compare(user_words, model_words))

        marked_text = []
        i = 0

        while i < len(diff):
            line = diff[i]
            if line[0] == "?":
                i += 1
                continue

            code, word = line[0], line[2:].strip()
            if code == " ":
                marked_text.append(word)
            elif code == "-" and i + 1 < len(diff) and diff[i + 1][0] == "+":
                new_word = diff[i + 1][2:].strip()
                marked_text.append(f"<replace new='{new_word}'>{word}</replace>")
                i += 1
            elif code == "-":
                marked_text.append(f"<del>{word}</del>")
            elif code == "+":
                marked_text.append(f"<ins>{word}</ins>")
            i += 1

        return " ".join(marked_text)
