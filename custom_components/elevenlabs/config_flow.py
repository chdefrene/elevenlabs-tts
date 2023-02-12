"""Config flow for ElevenLabs integration."""
import logging

import voluptuous as vol
from homeassistant import config_entries
from homeassistant.const import CONF_API_KEY

from .tts import CONF_VOICE

_LOGGER = logging.getLogger(__name__)

DATA_SCHEMA = vol.Schema(
    {
        vol.Required(CONF_API_KEY): str,
        vol.Required(CONF_VOICE): str,
    }
)


class ConfigFlow(config_entries.ConfigFlow, domain="elevenlabs"):
    """Example config flow."""
    # The schema version of the entries that it creates
    # Home Assistant will call your migrate method if the version changes
    VERSION = 1
    CONNECTION_CLASS = config_entries.CONN_CLASS_CLOUD_PUSH

    async def async_step_user(self, user_input=None):
        """Handle the initial step."""
        errors = {}

        if not getattr(user_input, CONF_API_KEY, None):
            errors[CONF_API_KEY] = "Need API key"

        elif not getattr(user_input, CONF_VOICE, None):
            errors[CONF_VOICE] = "Need to select a voice"

        else:
            try:
                return self.async_create_entry(title="ElevenLabs", data=user_input)
            except Exception as err:
                _LOGGER.exception(err)
                errors["base"] = "An unknown error occurred."

        # If there is no user input or there were errors, show the form again,
        # including any errors that were found with the input.
        return self.async_show_form(
            step_id="user", data_schema=DATA_SCHEMA, errors=errors
        )
