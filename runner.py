import sys
from antlr4 import *
from antlr4.tree.Tree import TerminalNodeImpl
from parser.SQLiteLexer import SQLiteLexer
from parser.SQLiteParser import SQLiteParser
from parser.SQLiteListener import SQLiteListener
from db.db import DBParser
from db.errors import *


def main(argv):
    db = DBParser()

    # for i in range(1, 101):
    #     db.insert_tuple(db.select("A"),
    #                     [{"attribute": "id", "value": str(i)}, {"attribute": "value", "value": str(i)}])
    #     db.insert_tuple(db.select("C"),
    #                 [{"attribute": "id", "value": str(i)}, {"attribute": "value", "value": 1}])
    # for i in range(1, 1001):
    #     db.insert_tuple(db.select("B"),
    #                     [{"attribute": "id", "value": str(i)}, {"attribute": "value", "value": str(i)}])
    # for i in range(1, 1001):
    #     db.insert_tuple(db.select("D"),
    #                     [{"attribute": "id", "value": str(i)}, {"attribute": "value", "value": 1}])
    # for i in range(1, 101):
    #     db.insert_tuple(db.select("Q"),
    #                     [{"attribute": "id", "value": str(i)}, {"attribute": "value", "value": str(i)}])
    # for i in range(1, 101):
    #     db.insert_tuple(db.select("Z"),
    #                     [{"attribute": "id", "value": str(i)}, {"attribute": "value", "value": str(i)}])
    while True:
        try:
            y = input()

            if y == 'x':
                break
            else:
                input_val = InputStream(y)
                lexer = SQLiteLexer(input_val)
                stream = CommonTokenStream(lexer)
                parser = SQLiteParser(stream)
                tree = parser.sql_stmt_list()
                # parsertree = parser.parse()
                # print(parsertree)
                # print(parser.ruleNames)
                # print(tree.toStringTree())

                # traverse(tree, parser.ruleNames)
            printer = SQLiteListener(db)
            walker = ParseTreeWalker()
            walker.walk(printer, tree)
        except SQLInputError as err:
            print("SQL Input Error: " + str(err.args[0]))



def traverse(tree, rule_names, indent = 0):
    if tree.getText() == "<EOF>":
        return
    elif isinstance(tree, TerminalNodeImpl):
        print("{0}TOKEN='{1}'".format(" " * indent, tree.getText()))

    else:
        print("{0}{1}".format("  " * indent, rule_names[tree.getRuleIndex()]))



        for child in tree.children:
            traverse(child, rule_names, indent + 1)


if __name__ == '__main__':
    main(sys.argv)