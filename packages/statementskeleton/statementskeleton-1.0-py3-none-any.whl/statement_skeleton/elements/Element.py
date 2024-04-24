"""
Element.py
"""

from typing import override, Any


class Element:
    def __init__(self, skeleton_obj: Any) -> None:
        """
        Creates an element to be implemented inside a statement skeleton.
        :param skeleton_obj: The skeleton to implement the element into.
        """
        self.skel: Any = skeleton_obj
        self.output: str = ""

    @override
    def __str__(self) -> str:
        return self.output

