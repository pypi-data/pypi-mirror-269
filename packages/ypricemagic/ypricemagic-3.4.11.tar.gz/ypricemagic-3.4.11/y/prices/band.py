import asyncio
from typing import Optional

import a_sync
from a_sync.property import HiddenMethodDescriptor
from brownie import chain
from brownie.exceptions import VirtualMachineError
from typing_extensions import Self

from y import Contract
from y.classes.common import ERC20
from y.datatypes import Address, AddressOrContract, Block
from y.exceptions import UnsupportedNetwork
from y.networks import Network

addresses = {
    # https://docs.fantom.foundation/tutorials/band-protocol-standard-dataset
    Network.Fantom: '0x56E2898E0ceFF0D1222827759B56B28Ad812f92F'
}

supported_assets = {
    # https://docs.fantom.foundation/tutorials/band-protocol-standard-dataset#supported-tokens
    Network.Fantom: [
        "0xaf319E5789945197e365E7f7fbFc56B130523B33", # FRAX
        "0x04068DA6C83AFCFA0e13ba15A6696662335D5B75", # USDC
        "0x0E1694483eBB3b74d3054E383840C6cf011e518e", # sUSD
        "0x6a07A792ab2965C72a5B8088d3a069A7aC3a993B", # AAVE
        "0x46E7628E8b4350b2716ab470eE0bA1fa9e76c6C5", # BAND
        "0xD67de0e0a0Fd7b15dC8348Bb9BE742F3c5850454", # BNB
        "0x321162Cd933E2Be498Cd2267a90534A804051b11", # BTC
        "0xB01E8419d842beebf1b70A7b5f7142abbaf7159D", # COVER
        "0x657A1861c15A3deD9AF0B6799a195a249ebdCbc6", # CREAM
        "0x1E4F97b9f9F913c46F1632781732927B9019C68b", # CRV
        "0x74b23882a30290451A17c44f4F05243b6b58C76d", # ETH
        "0x44B26E839eB3572c5E959F994804A5De66600349", # HEGIC
        "0x2A5062D22adCFaAfbd5C541d4dA82E4B450d4212", # KP3R
        "0xb3654dc3D10Ea7645f8319668E8F54d2574FBdC8", # LINK
        "0x924828a9Fb17d47D0eb64b57271D10706699Ff11", # SFI
        "0x56ee926bD8c72B2d5fa1aF4d9E4Cbb515a1E3Adc", # SNX
        "0xae75A438b2E0cB8Bb01Ec1E1e376De11D44477CC", # SUSHI
        "0x29b0Da86e484E1C0029B56e817912d778aC0EC69", # YFI
    ]
}

class Band(a_sync.ASyncGenericSingleton):
    def __init__(self, asynchronous: bool = False) -> None:
        if chain.id not in addresses:
            raise UnsupportedNetwork('band is not supported on this network')
        self.asynchronous = asynchronous
        super().__init__()

    def __contains__(self, asset: AddressOrContract) -> bool:
        return chain.id in addresses and asset in supported_assets[chain.id]
    
    @a_sync.aka.property
    async def oracle(self) -> Contract:
        return await Contract.coroutine(addresses[chain.id])
    __oracle__: HiddenMethodDescriptor[Self, Contract]

    async def get_price(self, asset: Address, block: Optional[Block] = None) -> Optional[float]:
        oracle, asset_symbol = await asyncio.gather(
            self.__oracle__,
            ERC20(asset, asynchronous=True).symbol,
        )
        try:
            reference_data = await oracle.getReferenceData.coroutine(asset_symbol, 'USDC', block_identifier=block)
            return reference_data[0] / 1e18
        except ValueError:
            return None
        except VirtualMachineError:
            return None


try:
    band = Band(asynchronous=True)
except UnsupportedNetwork:
    band = set()
