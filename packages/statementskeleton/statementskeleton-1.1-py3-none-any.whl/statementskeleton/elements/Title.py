"""
Title.py
"""

from typing import Any

from .Element import Element


class Title(Element):
    def __init__(self, skeleton_obj: Any, title_name: str) -> None:
        """
        An account category title. Used to group accounts into larger categories (assets, liabilities, equity, etc.).
        :param skeleton_obj: The skeleton to implement the element into.
        :param title_name: The title for the element to display.
        """
        super().__init__(skeleton_obj)

        self.space_needed: int = (self.skel.calcd_width + self.skel.margin - len(title_name))
        self.output = f"| {title_name}{" " * (self.space_needed - 1)}|"
