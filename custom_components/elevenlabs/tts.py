import logging
from http.client import HTTPException

import requests
from homeassistant.components.tts import Provider

CONF_VOICE = "voice"
_LOGGER = logging.getLogger(__name__)


class ElevenLabsProvider(Provider):
    """The ElevenLabs speech API provider."""

    def __init__(
            self, apikey, voice
    ):
        """Init ElevenLabs TTS service."""
        self._apikey = apikey
        self._voice = voice
        self.name = "ElevenLabs"

    # @property
    # def default_language(self):
    #     """Return the default language."""
    #     return self._lang

    # @property
    # def supported_languages(self):
    #     """Return list of supported languages."""
    #     return SUPPORTED_LANGUAGES

    # @property
    # def supported_options(self):
    #     """Return list of supported options like voice, emotion."""
    #     return [CONF_VOICE]

    # @property
    # def default_options(self):
    #     """Return a dict include default options."""
    #     return {CONF_VOICE: self._voice}

    def get_tts_audio(self, message, language, options=None):
        """Load TTS from ElevenLabs."""
        # if options['voice'] is None:
        #     language = self._lang

        try:
            # trans = pycsspeechtts.TTSTranslator(self._apikey, self._region)
            # data = trans.speak(
            #     language=language,
            #     gender=options[CONF_GENDER],
            #     voiceType=options[CONF_TYPE],
            #     output=self._output,
            #     rate=self._rate,
            #     volume=self._volume,
            #     pitch=self._pitch,
            #     contour=self._contour,
            #     text=message,
            # )

            url = f"https://api.elevenlabs.io/v1/text-to-speech/{self._voice}"

            data = {
                "text": message
            }

            headers = {
                "xi-api-key": self._apikey
            }

            response = requests.post(url, data=data, headers=headers)

            if response.status_code == requests.codes.ok:
                _LOGGER.debug("Text synthesis OK")

                return "mp3", response.content

        except HTTPException as ex:
            _LOGGER.error("Error occurred for ElevenLabs TTS: %s", ex)

        return None, None
