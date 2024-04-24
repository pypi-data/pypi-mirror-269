"""
Spacer.py
"""

from typing import Any

from .Element import Element


class Spacer(Element):
    def __init__(self, skeleton_obj: Any) -> None:
        """
        Adds a blank line to the financial statement with nothing on it.
        :param skeleton_obj: The skeleton to implement the element into.
        """
        super().__init__(skeleton_obj)
        self.space_needed: int = (self.skel.calcd_width + self.skel.margin)
        self.output = f"|{" " * self.space_needed}|"
