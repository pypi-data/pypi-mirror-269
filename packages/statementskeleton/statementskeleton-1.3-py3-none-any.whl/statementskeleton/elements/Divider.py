"""
Divider.py
"""

from typing import Any

from .Element import Element


class Divider(Element):
    def __init__(self, skeleton_obj: Any, border: bool = False) -> None:
        """
        Creates a divider. Useful for making sections more apparent.
        :param skeleton_obj:  The skeleton to implement the element into.
        :param border: If the divider is on the top or bottom. Changes its visual appearance.
        """
        super().__init__(skeleton_obj)

        if border:
            self.output = f"+{"-" * (self.skel.calcd_width + self.skel.margin)}+"
        else:
            self.output = f"|{"-" * (self.skel.calcd_width + self.skel.margin)}|"
