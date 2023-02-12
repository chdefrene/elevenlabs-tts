import logging
from http.client import HTTPException

import homeassistant.helpers.config_validation as cv
import requests
import voluptuous as vol
from homeassistant.components.tts import PLATFORM_SCHEMA, Provider
from homeassistant.const import CONF_API_KEY

CONF_VOICE = "voice"
_LOGGER = logging.getLogger(__name__)

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend(
    {
        vol.Required(CONF_API_KEY): cv.string,
        vol.Required(CONF_VOICE): cv.string,
    }
)


def get_engine(hass, config, discovery_info=None):
    """Set up ElevenLabs speech component."""
    return ElevenLabsProvider(
        config[CONF_API_KEY],
        config[CONF_VOICE],
    )


class ElevenLabsProvider(Provider):
    """The ElevenLabs speech API provider."""

    def __init__(
            self, apikey, voice
    ):
        """Init ElevenLabs TTS service."""
        self._apikey = apikey
        self._voice = voice
        self.name = "ElevenLabs"

    @property
    def default_language(self):
        """Return the default language."""
        return "en"

    @property
    def supported_languages(self):
        """Return list of supported languages."""
        return ["en"]

    @property
    def supported_options(self):
        """Return list of supported options like voice, emotion."""
        return []

    @property
    def default_options(self):
        """Return a dict include default options."""
        return {}

    def get_tts_audio(self, message, language, options=None):
        """Load TTS from ElevenLabs."""
        if language is None:
            language = "en"

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
