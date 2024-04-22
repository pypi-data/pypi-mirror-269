"""Vdsc Rong Viet provider concrete class."""

from vietfin.abstract.interface import IDerivativesFutures
from vietfin.abstract.vfobject import VfObject
# from vietfin.providers.vdsc.utils.derivatives_futures_quote import quote
    

class DerivativesFuturesVdsc(IDerivativesFutures):
    """The concrete implementation of Derivatives.Futures component with Vdsc Rong Viet as provider."""

    def historical(self, symbol: str, start_date: str, end_date: str) -> VfObject:
        """Derivatives Futures Historical. Load historical price data for a specific futures contract."""

        raise NotImplementedError("derivatives.futures.historical() command is not implemented for Vdsc Rong Viet provider.")
    
    def quote(self, symbol: str, limit: int) -> VfObject:
        """Derivatives Futures Quote. Load quote data for a specific futures contract."""

        raise NotImplementedError("derivatives.futures.quote() command is currently disabled for Vdsc Rong Viet provider.")

    def search(self, symbol: str) -> VfObject:
        """Derivatives Futures Search. Search for a specific futures contract."""

        raise NotImplementedError("derivatives.futures.search() command is not implemented for Vdsc Rong Viet provider.")