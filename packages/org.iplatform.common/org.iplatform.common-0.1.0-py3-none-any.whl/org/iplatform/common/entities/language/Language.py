from org.iplatform.common.entities.language.LanguageType import LanguageType
class Language():
    """
    The language of any
    """
    def __init__(self, code: str = 'en', language: str = 'Default', description: str = '') -> None:
        """
        The language code of language
        """
        self.code = code
        self.language = language
        self.description = description