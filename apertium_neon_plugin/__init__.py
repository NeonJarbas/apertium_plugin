from ovos_plugin_manager.templates.language import LanguageTranslator
from ovos_utils.log import LOG
import requests


class ApertiumTranslator(LanguageTranslator):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # host it yourself https://github.com/apertium/apertium
        self.url = self.config.get("apertium_host") or \
                   "https://www.apertium.org/apy/translate"

    def translate(self, text, target=None, source=None, url=None):
        if self.boost and not source:
            source = self.default_language
        target = target or self.internal_language
        lang_pair = target
        if source:
            lang_pair = source + "|" + target
        r = requests.get(self.url,
                         params={"q": text, "langpair": lang_pair,
                                 "markUnknown": "no"}).json()
        if r.get("status", "") == "error":
            LOG.error(r["explanation"])
            return None
        return r["responseData"]["translatedText"]
