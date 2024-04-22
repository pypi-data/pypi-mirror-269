from .base import CardanoToken


class HoskyToken(CardanoToken):
    def __init__(self, dexhunter_partner_code: str):
        super().__init__(
            asset_id="a0028f350aaabe0545fdcb56b039bfb08e4bb4d8c4d7c3c7d481c235484f534b59",
            asset_name="484f534b59",
            fingerprint="asset17q7r59zlc3dgw0venc80pdv566q6yguw03f0d9",
            policy_id="a0028f350aaabe0545fdcb56b039bfb08e4bb4d8c4d7c3c7d481c235",
            symbol="HOSKY",
            decimals=0,
            dexhunter_partner_code=dexhunter_partner_code,
        )

    @property
    def ada(self) -> float:
        return 0.0

    @property
    def usd(self) -> float:
        return 0.0
