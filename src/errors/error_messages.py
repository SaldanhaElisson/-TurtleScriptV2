from enum import Enum


class ErrorMessages(Enum):
    UNKNOWN_SYMBOL = "Symbol not known to the compiler."
    IGNORE_LINE = "Ignore this line."
    FIRST_SYMBOL = "ID INVALID: You can't start with number or invalid symbol."
    ID_WRONG_FORMATTED = "Mal formatted ID: Must be in Snake_Case (lowercase letters, numbers and underrscores only)."
    TEXT_OR_CHAR_NOT_CLOSED = "Text or char not closed."
    DELIMITER_CLOSED_ERROR = "Delimiter was closed without being opened."
    DELIMITER_NOT_CLOSED_ERROR = "Delimiter was opened but was not closed."
    DELIMITER_ERROR = "The following delimmiters were not closed."
    DELIMITER_NOT_FOUND_ERROR = "Delimiter is not part of our set of symbols."
    DELIMITER_OPENED_ERROR = "Delimiter was opened and was not closed."

