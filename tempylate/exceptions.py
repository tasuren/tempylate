# tempylate - Exceptions


__all__ = ("TempylateError", "LoadBlockError")


class TempylateError(Exception):
    "Tempylate error base error."


class LoadBlockError(TempylateError):
    "This error occurs when Tempylate fails to load a block."