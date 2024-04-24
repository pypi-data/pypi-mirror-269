"""
Header.py
"""

from typing import Any

from .Element import Element


class Header(Element):
    def __init__(self, skeleton_obj: Any, header_type: str, header_name: str = "") -> None:
        """
        Displays information centered in the middle of the financial statement:\n
        "company" = Displays the name of the company.\n
        "fs" = Displays the name of the financial statement.\n
        "date" = Displays the name of the date.\n
        Any other input will display the custom header name.
        :param skeleton_obj: The skeleton to implement the element into.
        :param header_type: The information for the header to display taken from Skeleton.
        :param header_name: If using a custom header, the customer information for the header to display.
        """
        super().__init__(skeleton_obj)

        self.header_name: str = ""

        if header_type.lower() == "company":
            self.header_name = self.skel.company

        elif header_type.lower() == "fs":
            self.header_name = self.skel.fs_name

        elif header_type.lower() == "date":
            self.header_name = self.skel.f_date

        else:
            # Allows a custom header title with proper formatting.
            self.skel.add_text(header_name)
            self.header_name = header_name

        self.space_needed: int = (self.skel.calcd_width + self.skel.margin - len(self.header_name))
        self.l_space_needed: int = 0
        self.r_space_needed: int = 0

        if self.space_needed % 2 != 0:
            self.l_space_needed = int((self.space_needed / 2) - 0.5)
            self.r_space_needed = int((self.space_needed / 2) + 0.5)

        else:
            self.l_space_needed = self.r_space_needed = self.space_needed // 2

        self.output = f"|{" " * self.l_space_needed}{self.header_name}{" " * self.r_space_needed}|"
