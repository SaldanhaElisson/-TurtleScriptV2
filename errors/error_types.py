from enum import Enum


class ErrorType(Enum):
  LEXICAL = "Lexical"
  SYNTACTIC = "Syntactic"
  SEMANTIC = "Semantic"