from typing import NamedTuple

from common.Contract.Asset import Asset


class ShadowStock(NamedTuple):
    main_asset: Asset
    shadow_assets: list[Asset]

    def is_shadow(self, asset: Asset) -> bool:
        return asset in self.shadow_assets or asset == self.main_asset

    def __eq__(self, other):
        if isinstance(other, ShadowStock):
            return self.main_asset == other.main_asset and set(self.shadow_assets) == set(other.shadow_assets)
        return False
