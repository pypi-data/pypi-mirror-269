"""
Subtotal.py
"""

from typing import Any

from .Account import Account


class Subtotal(Account):
    def __init__(self, skeleton_obj: Any, subtotal_name: str, subtotal_bal: float | int) -> None:
        """
        Adds a subtotal line. Similar to the Total class except it indents the line like the Account class does.
        :param skeleton_obj: The skeleton to implement the element into.
        :param subtotal_name: The name of the subtotal to display.
        :param subtotal_bal: The balance of the subtotal to display.
        """
        super().__init__(skeleton_obj, subtotal_name, subtotal_bal)

        self.output: str = (f"|{" " * self.skel.indent}{subtotal_name}{" " * self.central_spacer}"
                            f"{self.account_bal:{self.fdecimal}}{" "}|")
