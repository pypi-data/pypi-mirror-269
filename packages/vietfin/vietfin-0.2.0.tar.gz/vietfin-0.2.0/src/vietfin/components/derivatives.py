"""VietFin Derivatives class."""

from typing import Literal

from vietfin.abstract.vfobject import VfObject
from vietfin.abstract.factory import (
    DerivativesFuturesFactory,
    DerivativesCoveredWarrantFactory,
)
from vietfin.abstract.interface import (
    IDerivativesFutures,
    IDerivativesCoveredWarrant,
)


class Derivatives:
    """VietFin Derivatives related group of commands."""

    def __init__(self) -> None:
        self.futures = DerivativesFutures()
        self.cw = DerivativesCoveredWarrant()


class DerivativesFutures:
    """VietFin Derivatives.Futures-related group of commands."""

    # list of implemented providers
    PROVIDERS = Literal["tcbs", "ssi"]

    @staticmethod
    def _get_provider(provider: PROVIDERS) -> IDerivativesFutures:
        provider_name = provider.lower()
        return DerivativesFuturesFactory().get_provider(provider_name)

    def historical(
        self,
        symbol: str,
        start_date: str | None = None,
        end_date: str | None = None,
        provider: PROVIDERS = "tcbs",
    ) -> VfObject:
        """Futures Historical price. Load Futures Historical data for a specific futures contract."""

        provider_instance = self._get_provider(provider)
        return provider_instance.historical(
            symbol=symbol,
            start_date=start_date,  # type: ignore
            end_date=end_date,  # type: ignore
        )

    def quote(
        self,
        symbol: str,
        limit: int = 100,
        provider: PROVIDERS = "ssi",
    ) -> VfObject:
        """Futures Quote. Load Futures quote for a specific futures contract."""

        provider_instance = self._get_provider(provider)
        return provider_instance.quote(
            symbol=symbol,
            limit=limit,
        )

    def search(self, symbol: str = "", provider: PROVIDERS = "ssi") -> VfObject:
        """Derivatives Futures Search. Search for a specific futures contract."""

        provider_instance = self._get_provider(provider)
        return provider_instance.search(symbol=symbol)


class DerivativesCoveredWarrant:
    """VietFin Derivatives.CoveredWarrant-related group of commands."""

    # list of implemented providers
    PROVIDERS = Literal["ssi"]

    @staticmethod
    def _get_provider(provider: PROVIDERS) -> IDerivativesCoveredWarrant:
        provider_name = provider.lower()
        return DerivativesCoveredWarrantFactory().get_provider(provider_name)

    def search(self, symbol: str = "", provider: PROVIDERS = "ssi") -> VfObject:
        """Derivatives Covered Warrant Search. Search for a specific covered warrant."""

        provider_instance = self._get_provider(provider)
        return provider_instance.search(symbol=symbol)
