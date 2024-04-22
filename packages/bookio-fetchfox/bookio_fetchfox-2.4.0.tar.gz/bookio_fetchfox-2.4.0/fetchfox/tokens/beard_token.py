from fetchfox.constants.beard import (
    BEARD_TOKEN_ASSET_ID,
    BEARD_TOKEN_ASSET_NAME,
    BEARD_TOKEN_POLICY_ID,
    BEARD_TOKEN_FINGERPRINT,
)
from fetchfox.constants.currencies import BEARD

from .base import CardanoToken


class BeardToken(CardanoToken):
    def __init__(self, dexhunter_partner_code: str):
        super().__init__(
            asset_id=BEARD_TOKEN_ASSET_ID,
            asset_name=BEARD_TOKEN_ASSET_NAME,
            fingerprint=BEARD_TOKEN_FINGERPRINT,
            policy_id=BEARD_TOKEN_POLICY_ID,
            symbol=BEARD,
            dexhunter_partner_code=dexhunter_partner_code,
        )
