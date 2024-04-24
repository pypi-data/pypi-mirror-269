# Type stubs for simular-evm

Fully documented type annotations for `PyEvm` and `PyAbi` in [simular-evm](https://pypi.org/project/simular-evm)

## Contents

```python
from typing import Optional, Tuple

class DynSolTypeWrapper:
    """Decode output from function"""

class PyEvm:
    """An in-memory EVM"""

    def __new__() -> PyEvm:
        """Create an in-memory EVM"""

    def call(
        self,
        fn_name: str,
        args: str,
        to: str,
        abi: PyAbi,
    ):
        """
        Transaction (read) operation to a contract at the given address `to`.
        This will NOT change state in the EVM.
        """

    def simulate(
        self,
        fn_name: str,
        args: str,
        caller: str,
        to: str,
        value: int,
        abi: PyAbi,
    ) -> object:
        """
        Transaction operation to a contract at the given address `to`.
        This can simulate a transact/call operation, but will NOT change state in the EVM.
        """

    def deploy(self, args: str, caller: str, value: int, abi: PyAbi) -> str:
        """Deploy a contract"""

    def transact(
        self,
        fn_name: str,
        args: str,
        caller: str,
        to: str,
        value: int,
        abi: PyAbi,
    ) -> object:  # TODO: figure out the return type, and the "py: Python<'_>" argument
        """
        Transaction (write) operation to a contract at the given address `to`.
        This will change state in the EVM.
        """

    @staticmethod
    def from_fork(url: str, blocknumber: Optional[int] = None) -> PyEvm:
        """Create a fork EVM"""

    @staticmethod
    def from_snapshot(snapshot: str) -> PyEvm:
        """Create an in-memory EVM from a `SnapShot`"""

    def create_snapshot(self) -> str:
        """Create a `SnapShot` of the current EVM state"""

    def create_account(self, address: str, balance: Optional[int] = None) -> None:
        """Create account with an initial balance"""

    def get_balance(self, address: str) -> int:
        """Get the balance of the given user"""

    def transfer(self, caller: str, to: str, amount: int) -> None:
        """Transfer the amount of value from `caller` to the given recipient `to`."""

class PyAbi:
    """
    Can load and parse ABI information.
    Used in `Contract.py` to process function calls.
    """

    def bytecode(self) -> list[int]:
        """Return the contract bytecode"""

    def encode_constructor(self, args: str) -> Tuple[list[int], bool]:
        """
        Encode constructor arguments.
        Returns the encoded args, and whether the constructor is payable
        """

    def encode_function(
        self, name: str, args: str
    ) -> Tuple[list[int], bool, DynSolTypeWrapper]:
        """
        Encode the arguments for a specific function.
        Returns:
        - `encoded args`
        - `is the function payable?`
        - `DynSolType` to decode output from function
        """

    @staticmethod
    def from_abi_bytecode(abi: str, bytes: Optional[bytes]) -> PyAbi:
        """Load from the un-parsed json `abi` and optionally `bytecode`"""

    @staticmethod
    def from_full_json(abi: str) -> PyAbi:
        """
        Load a complete ABI file from a compiled Solidity contract.
        This is a raw un-parsed json file that includes both `abi` and `bytecode`.
        """

    @staticmethod
    def from_human_readable(values: list[str]) -> PyAbi:
        """
        Create an ABI by providing shortened definitions of the functions of interest.

        ## Example:

        `["function hello() (uint256)"]` creates the function `hello` that can be encoded/decoded for calls to the Evm.
        """

    def has_fallback(self) -> bool:
        """Does the Contract have a fallback function?"""

    def has_function(self, name: str) -> bool:
        """Does the ABI contain the function `name`?"""

    def has_receive(self) -> bool:
        """Does the contract have a receive function?"""
```