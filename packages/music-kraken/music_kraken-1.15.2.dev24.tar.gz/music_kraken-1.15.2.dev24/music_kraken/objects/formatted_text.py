import mistune
from markdownify import markdownify as md


def plain_to_markdown(plain: str) -> str:
    return plain.replace("\n", "  \n")


class FormattedText:    
    html = ""

    def __init__(
            self,
            markdown: str = None,
            html: str = None,
            plain: str = None,
    ) -> None:
        if html is not None:
            self.html = html
        elif markdown is not None:
            self.html = mistune.markdown(markdown)
        elif plain is not None:
            self.html = mistune.markdown(plain_to_markdown(plain))

    @property
    def is_empty(self) -> bool:
        return self.html == ""

    def __eq__(self, other) -> False:
        if type(other) != type(self):
            return False
        if self.is_empty and other.is_empty:
            return True

        return self.doc == other.doc

    @property
    def markdown(self) -> str:
        return md(self.html).strip()

    def __str__(self) -> str:
        return self.markdown

    plaintext = markdown
    
