import difflib
import re


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
        # Разбиваем тексты на слова, сохраняя пробелы и знаки препинания
        user_words = re.findall(r'\S+|\s+', user_text)
        model_words = re.findall(r'\S+|\s+', model_text)

        differ = difflib.Differ()
        diff = list(differ.compare(user_words, model_words))

        marked_text = []
        i = 0

        while i < len(diff):
            line = diff[i]
            
            # Пропускаем строки с '?'
            if line[0] == "?":
                i += 1
                continue

            code, word = line[0], line[2:]
            
            # Собираем последовательности слов для замены
            if code == "-" and i + 1 < len(diff) and diff[i + 1][0] == "+":
                # Собираем все удаленные слова
                deleted_words = []
                while i < len(diff) and diff[i][0] == "-":
                    deleted_words.append(diff[i][2:])
                    i += 1
                    # Пропускаем строки с '?'
                    while i < len(diff) and diff[i][0] == "?":
                        i += 1
                
                # Собираем все добавленные слова
                added_words = []
                while i < len(diff) and diff[i][0] == "+":
                    added_words.append(diff[i][2:])
                    i += 1
                    # Пропускаем строки с '?'
                    while i < len(diff) and diff[i][0] == "?":
                        i += 1
                
                # Объединяем слова в строки
                deleted_text = "".join(deleted_words)
                added_text = "".join(added_words)
                
                if deleted_text.strip() or added_text.strip():
                    marked_text.append(f"<replace new='{added_text}'>{deleted_text}</replace>")
                continue
            
            elif code == "-":
                # Собираем все удаленные слова
                deleted_words = []
                while i < len(diff) and diff[i][0] == "-":
                    deleted_words.append(diff[i][2:])
                    i += 1
                    # Пропускаем строки с '?'
                    while i < len(diff) and diff[i][0] == "?":
                        i += 1
                
                deleted_text = "".join(deleted_words)
                if deleted_text.strip():
                    marked_text.append(f"<del>{deleted_text}</del>")
                continue
            
            elif code == "+":
                # Собираем все добавленные слова
                added_words = []
                while i < len(diff) and diff[i][0] == "+":
                    added_words.append(diff[i][2:])
                    i += 1
                    # Пропускаем строки с '?'
                    while i < len(diff) and diff[i][0] == "?":
                        i += 1
                
                added_text = "".join(added_words)
                if added_text.strip():
                    marked_text.append(f"<ins>{added_text}</ins>")
                continue
            
            elif code == " ":
                marked_text.append(word)
            
            i += 1

        return "".join(marked_text)
