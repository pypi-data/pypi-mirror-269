"""
Total.py
"""

from typing import Any

from .Account import Account


class Total(Account):
    def __init__(self, skeleton_obj: Any, total_name: str, total_bal: float | int) -> None:
        """
        Displays the total of all accounts. Useful to summarize a section. The total must be calculated manually, this
        simply provides a unique formatting option.
        :param skeleton_obj: The skeleton to implement the element into.
        :param total_name: The name of the total.
        :param total_bal: The balance of the total.
        """
        super().__init__(skeleton_obj, total_name, total_bal)

        # I have no idea why I need to subtract 2 here, but I do. This whole self.space_needed calculation has gotten
        # super messy.
        self.central_spacer -= 2
        self.central_spacer = max(self.central_spacer, self.skel.column_space)
        self.output: str = (f"| Total {total_name}{" " * (self.central_spacer - 1)}{self.account_bal:{self.fdecimal}}"
                            f"{" "}|")
