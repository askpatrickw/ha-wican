"""Adding the WiCAN integration with a device to HomeAssistant."""

import logging
from typing import Any
from homeassistant import config_entries
from homeassistant.const import CONF_IP_ADDRESS
import voluptuous as vol
from .const import DOMAIN
from .wican import WiCan

DATA_SCHEMA = vol.Schema(
    {
        vol.Required(CONF_IP_ADDRESS): str,
    }
)
_LOGGER = logging.getLogger(__name__)


class WiCanConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """WiCan Configuration flow.

    Parameters
    ----------
    domain: str
        Constant containing WiCAN domain.

    """

    VERSION = 1
    CONNECTION_CLASS = config_entries.CONN_CLASS_CLOUD_POLL

    async def async_step_user(self, user_input: dict[str, Any] | None = None):
        """Check creation WiCan device in HomeAssistant based on user-input.

        Parameters
        ----------
        user_input : dict
            Configuration data for the WiCan device (e.g. IP-Address).

        Returns
        -------
        async_create_entry: method:
            Calls function to create the WiCan device.
            If device cannot be created, exception is logged and error added to dict of errors.

        """
        errors = {}
        if user_input is not None:
            ip = user_input[CONF_IP_ADDRESS]
            try:
                wican = WiCan(ip)
                info = await wican.test()

                if info:
                    return self.async_create_entry(title="WiCAN", data=user_input)
                else:
                    errors[CONF_IP_ADDRESS] = (
                        "Failed validation, double check the IP, as well as check if you have protocol set to auto_pid"
                    )
            except ConnectionError:
                _LOGGER.exception("Connection Error")
                errors[CONF_IP_ADDRESS] = (
                    "WiCAN Connection error, are you sure the IP is correct?"
                )
            except Exception:
                _LOGGER.exception("Unexpected exception")
                errors[CONF_IP_ADDRESS] = "WiCAN not validated, unknown error"

        return self.async_show_form(
            step_id="user", data_schema=DATA_SCHEMA, errors=errors
        )
