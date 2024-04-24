"""
Account.py
"""

from typing import Any

from .Element import Element


class Account(Element):
    def __init__(self, skeleton_obj: Any, account_name: str, account_bal: float | int) -> None:
        """
        Adds an individual account and its balance to the skeleton.
        :param skeleton_obj: The skeleton to implement the element into.
        :param account_name: The name of the account to display.
        :param account_bal: The balance of the account to display.
        """
        super().__init__(skeleton_obj)

        self.central_spacer: int = -1
        self.account_bal: float | int = 0.0
        self.fdecimal: str = ","

        if self.skel.decimals:
            self.account_bal = float(round(account_bal, 2))
            self.fdecimal = ",.2f"

        else:
            self.account_bal = int(round(account_bal))

        self.central_spacer += (self.skel.calcd_width - len(account_name) + self.skel.margin - self.skel.indent -
                                len(f"{self.account_bal:{self.fdecimal}}"))

        self.central_spacer = max(self.central_spacer, self.skel.column_space)

        self.output: str = (f"|{" " * self.skel.indent}{account_name}{"·" * self.central_spacer}"
                            f"{self.account_bal:{self.fdecimal}}{" "}|")
