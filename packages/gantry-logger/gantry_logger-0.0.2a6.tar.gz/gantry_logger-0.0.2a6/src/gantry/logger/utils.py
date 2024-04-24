import os
from typing import Optional

from gantry.sdk import Gantry


def _init_gantry(api_key: Optional[str] = None) -> Gantry:
    api_key = api_key or os.environ.get("GANTRY_API_KEY")
    if not api_key:
        raise ValueError(
            "You must provide an API key to use this feature. "
            "You can provide one as an argument or "
            "set the GANTRY_API_KEY environment variable."
        )
    return Gantry(
        api_key_auth=api_key,
        server_url=os.environ.get("GANTRY_LOGS_LOCATION"),  # type: ignore
    )
