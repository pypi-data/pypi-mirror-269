from sys import stderr
from antlr4.error.ErrorListener import ConsoleErrorListener


class ErrorListener(ConsoleErrorListener):
    def __init__(self, filepath):
        self.filepath = filepath

    def syntaxError(self, recognizer, offendingSymbol, line, column, msg, e):
        stderr.write(f"{self.filepath}:{line}:{column}: {msg}\n")
