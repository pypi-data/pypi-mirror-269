"""
test_Skeleton.py

The only thing this file is for is to make sure the output looks correct. It won't verify anything else.
"""

from src.statementskeleton.skeletons.Skeleton import Skeleton

test_fs: dict[str:dict[str:dict[str:str | float]]] = {
    "Assets": {
        "Cash": {
            "d/c": "debit",
            "bal": 400.0,
            "term": "current"
        },

        "Accounts Receivable": {
            "d/c": "debit",
            "bal": 1_000.0,
            "term": "current"
        }
    },

    "Liabilities": {
        "Accounts Payable": {
            "d/c": "credit",
            "bal": 200.0,
            "term": "current"
        }
    },

    "Stockholders' Equity": {
        "Common Stock": {
            "d/c": "credit",
            "bal": 200
        },

        "Retained Earnings": {
            "d/c": "credit",
            "bal": 1_000
        }
    }
}

test_skeleton: Skeleton = Skeleton(test_fs, "Test Company", "Financial Statement",
                                   "12/31/20XX", decimals=False)

test_skeleton.print_output()
print(test_skeleton.return_output())