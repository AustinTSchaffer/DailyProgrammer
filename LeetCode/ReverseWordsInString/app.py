class Solution:
    def reverseWords(self, s: str) -> str:
        output = []

        current_word = ""
        for char in s:
            if char == " ":
                if current_word:
                    output.insert(0, current_word)
                    current_word = ""
            else:
                current_word += char

        if current_word:
            output.insert(0, current_word)

        return " ".join(output)
