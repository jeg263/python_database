# Generated from SQLite.g4 by ANTLR 4.7.1
from db.db import DB
from antlr4 import *
if __name__ is not None and "." in __name__:
    from parser.SQLiteParser import SQLiteParser
else:
    from parser.SQLiteParser import SQLiteParser

# This class defines a complete listener for a parse tree produced by SQLiteParser.
class SQLiteListener(ParseTreeListener):
    def __init__(self, db):
        ParseTreeListener.__init__(self)
        self._db = db

    # Enter a parse tree produced by SQLiteParser#parse.
    def enterParse(self, ctx:SQLiteParser.ParseContext):
        pass

    # Exit a parse tree produced by SQLiteParser#parse.
    def exitParse(self, ctx:SQLiteParser.ParseContext):
        pass


    # Enter a parse tree produced by SQLiteParser#error.
    def enterError(self, ctx:SQLiteParser.ErrorContext):
        pass

    # Exit a parse tree produced by SQLiteParser#error.
    def exitError(self, ctx:SQLiteParser.ErrorContext):
        pass


    # Enter a parse tree produced by SQLiteParser#sql_stmt_list.
    def enterSql_stmt_list(self, ctx:SQLiteParser.Sql_stmt_listContext):
        pass
        # table_names = []
        # columns = []
        # values = []
        # print(ctx.getText())
        # for i in range(len(ctx.children)):
        #     #print("hey")
        #
        #     if ctx.getChild(i).getText() == 'SELECT':
        #         i += 1
        #
        #     while ctx.getChild(i).getText() != 'FROM':
        #         if ctx.getChild(i).getText().isalpha():
        #             columns.append(ctx.getChild(i).getText())
        #     i += 1
        #     table_names.append(ctx.getChild(i).getText())
        #     i += 1
        #
        #     while ctx.getChild(i).getText() != '<EOF>':
        #         if ctx.getChild(i).getText().isalpha():
        #             values.append((ctx.getChild(i).getText()))
        #
        #
        #
        # print(table_names)
        # print(columns)
        # print(values)

    # Exit a parse tree produced by SQLiteParser#sql_stmt_list.
    def exitSql_stmt_list(self, ctx:SQLiteParser.Sql_stmt_listContext):
        pass


    # Enter a parse tree produced by SQLiteParser#sql_stmt.
    def enterSql_stmt(self, ctx:SQLiteParser.Sql_stmtContext):
        pass

    # Exit a parse tree produced by SQLiteParser#sql_stmt.
    def exitSql_stmt(self, ctx:SQLiteParser.Sql_stmtContext):
        #print(ctx.)
        pass


    # Enter a parse tree produced by SQLiteParser#alter_table_stmt.
    def enterAlter_table_stmt(self, ctx:SQLiteParser.Alter_table_stmtContext):
        foreign_keys = []
        relation_names = []

        if ctx.getChild(3).getText() == "ADD":
            relation_names.append(ctx.getChild(2).getText())

            i = 4
            foreign_key_start_pos = ctx.getChild(i).getText().find("(")
            token = ctx.getChild(i).getText()
            token = token[foreign_key_start_pos + 1:]
            foreign_key_end_pos = token.find(")")
            key_token = token[:foreign_key_end_pos]
            token = token[foreign_key_end_pos + 1:]
            references_start = token.find("REFERENCES")
            key_table_token_start = token.find("(")
            key_table_token_end = token.find(")")
            table_token = token[references_start + len("REFERENCES"):key_table_token_start]
            attribute_token = token[key_table_token_start + 1: key_table_token_end]
            foreign_keys.append([key_token, table_token, attribute_token])
            for fk in foreign_keys:
                self._db.create_fks(relation_names[0], [fk[0]], [fk[2]], [fk[1]])
        else:
            relation_names.append(ctx.getChild(2).getText())

            i = 4
            attribute = ctx.getChild(7).getText()
            self._db.drop_foreign_key(relation_names[0], attribute)
        pass

    # Exit a parse tree produced by SQLiteParser#alter_table_stmt.
    def exitAlter_table_stmt(self, ctx:SQLiteParser.Alter_table_stmtContext):
        pass


    # Enter a parse tree produced by SQLiteParser#analyze_stmt.
    def enterAnalyze_stmt(self, ctx:SQLiteParser.Analyze_stmtContext):
        pass

    # Exit a parse tree produced by SQLiteParser#analyze_stmt.
    def exitAnalyze_stmt(self, ctx:SQLiteParser.Analyze_stmtContext):
        pass


    # Enter a parse tree produced by SQLiteParser#attach_stmt.
    def enterAttach_stmt(self, ctx:SQLiteParser.Attach_stmtContext):
        pass

    # Exit a parse tree produced by SQLiteParser#attach_stmt.
    def exitAttach_stmt(self, ctx:SQLiteParser.Attach_stmtContext):
        pass


    # Enter a parse tree produced by SQLiteParser#begin_stmt.
    def enterBegin_stmt(self, ctx:SQLiteParser.Begin_stmtContext):
        pass

    # Exit a parse tree produced by SQLiteParser#begin_stmt.
    def exitBegin_stmt(self, ctx:SQLiteParser.Begin_stmtContext):
        pass


    # Enter a parse tree produced by SQLiteParser#commit_stmt.
    def enterCommit_stmt(self, ctx:SQLiteParser.Commit_stmtContext):
        pass

    # Exit a parse tree produced by SQLiteParser#commit_stmt.
    def exitCommit_stmt(self, ctx:SQLiteParser.Commit_stmtContext):
        pass


    # Enter a parse tree produced by SQLiteParser#compound_select_stmt.
    def enterCompound_select_stmt(self, ctx:SQLiteParser.Compound_select_stmtContext):
        pass

    # Exit a parse tree produced by SQLiteParser#compound_select_stmt.
    def exitCompound_select_stmt(self, ctx:SQLiteParser.Compound_select_stmtContext):
        pass


    # Enter a parse tree produced by SQLiteParser#create_index_stmt.
    def enterCreate_index_stmt(self, ctx:SQLiteParser.Create_index_stmtContext):
        index_names = []
        relation_names = []
        values = []

        index_names.append(ctx.getChild(2).getText())

        for i in range(len(ctx.children)):
            if ctx.getChild(i).getText() == 'ON':
                i = i + 1
                while ctx.getChild(i).getText() != '(':
                    if ctx.getChild(i).getText().isalnum():
                        relation_names.append(ctx.getChild(i).getText())
                    i += 1
            elif ctx.getChild(i).getText() == '(':
                i += 1
                while ctx.getChild(i).getText() != ')':
                    if ctx.getChild(i).getText() and ctx.getChild(i).getText() != "," \
                            and ctx.getChild(i).getText() != "(":
                        values.append(ctx.getChild(i).getText())
                    i += 1
                break
        types = []
        for val in values:
           types.append("type")

        self._db.create_indexes(relation_names[0], [values], [types], [index_names[0]])

    # Exit a parse tree produced by SQLiteParser#create_index_stmt.
    def exitCreate_index_stmt(self, ctx:SQLiteParser.Create_index_stmtContext):
        pass


    # Enter a parse tree produced by SQLiteParser#create_table_stmt.
    def enterCreate_table_stmt(self, ctx:SQLiteParser.Create_table_stmtContext):
        table_names = []
        attributes = []
        primary_keys = []
        domains = []
        foreign_keys = []

        table_names.append(ctx.getChild(2).getText())

        # CREATE TABLE Q (id1 int, id2 int, id3 int, professor string, PRIMARY KEY (id1, id2, id3), FOREIGN KEY (PersonID) REFERENCES Persons(PersonID));
        # CREATE TABLE Orders (OrderID int, OrderNumber int, PersonID int, PRIMARY KEY (OrderID, Another), FOREIGN KEY (PersonID) REFERENCES Persons(PersonID));

        for i in range(len(ctx.children)):
            if ctx.getChild(i).getText() == '(':
                i = i + 1
                token = ctx.getChild(i).getText()
                while token != ')' and token.find("PRIMARYKEY") == -1:
                    token = ctx.getChild(i).getText()
                    if ctx.getChild(i).getText().isalnum():
                        if token.find("int") != -1:
                            token = token[0:token.find("int")]
                            domains.append("integer")
                        elif token.find("string") != -1:
                            token = token[0:token.find("string")]
                            domains.append("string")
                        elif token.find("float") != -1:
                            token = token[0:token.find("float")]
                            domains.append("float")
                        attributes.append(token)
                    i += 1
            elif ctx.getChild(i).getText().find("PRIMARYKEY") != -1:
                primary_key_start_pos = ctx.getChild(i).getText().find("(")
                primary_key_end_pos = ctx.getChild(i).getText().find(")")
                token = ctx.getChild(i).getText()
                token = token[primary_key_start_pos + 1:primary_key_end_pos]
                tokens = token.split(",")
                primary_keys += tokens
            elif ctx.getChild(i).getText().find("FOREIGNKEY") != -1:
                foreign_key_start_pos = ctx.getChild(i).getText().find("(")
                token = ctx.getChild(i).getText()
                token = token[foreign_key_start_pos + 1:]
                foreign_key_end_pos = token.find(")")
                key_token = token[:foreign_key_end_pos]
                token = token[foreign_key_end_pos + 1:]
                references_start = token.find("REFERENCES")
                key_table_token_start = token.find("(")
                key_table_token_end = token.find(")")
                table_token = token[references_start + len("REFERENCES"):key_table_token_start]
                attribute_token = token[key_table_token_start + 1: key_table_token_end]
                foreign_keys.append([key_token, table_token, attribute_token])

        pk_domains = []
        location_to_delete = []
        i = 0
        for pk in primary_keys:
            for j in range(0, len(attributes)):
                if attributes[j] == pk:
                    pk_domains.append(domains[j])
                    location_to_delete.append(j)
        location_to_delete = sorted(location_to_delete, reverse=True)
        for loc in location_to_delete:
            domains.pop(loc)
            attributes.pop(loc)

        self._db.create_table(table_names[0], primary_keys, pk_domains, attributes, domains)
        for fk in foreign_keys:
            self._db.create_fks(table_names[0], [fk[0]], [fk[2]], [fk[1]])
        print("Relation created")

    # Exit a parse tree produced by SQLiteParser#create_table_stmt.
    def exitCreate_table_stmt(self, ctx:SQLiteParser.Create_table_stmtContext):
        pass


    # Enter a parse tree produced by SQLiteParser#create_trigger_stmt.
    def enterCreate_trigger_stmt(self, ctx:SQLiteParser.Create_trigger_stmtContext):
        pass

    # Exit a parse tree produced by SQLiteParser#create_trigger_stmt.
    def exitCreate_trigger_stmt(self, ctx:SQLiteParser.Create_trigger_stmtContext):
        pass


    # Enter a parse tree produced by SQLiteParser#create_view_stmt.
    def enterCreate_view_stmt(self, ctx:SQLiteParser.Create_view_stmtContext):
        pass

    # Exit a parse tree produced by SQLiteParser#create_view_stmt.
    def exitCreate_view_stmt(self, ctx:SQLiteParser.Create_view_stmtContext):
        pass


    # Enter a parse tree produced by SQLiteParser#create_virtual_table_stmt.
    def enterCreate_virtual_table_stmt(self, ctx:SQLiteParser.Create_virtual_table_stmtContext):
        pass

    # Exit a parse tree produced by SQLiteParser#create_virtual_table_stmt.
    def exitCreate_virtual_table_stmt(self, ctx:SQLiteParser.Create_virtual_table_stmtContext):
        pass


    # Enter a parse tree produced by SQLiteParser#delete_stmt.
    def enterDelete_stmt(self, ctx:SQLiteParser.Delete_stmtContext):
        table_name = []
        attributes = []
        values = []
        sec_op = []

        for i in range(len(ctx.children)):

            if ctx.getChild(i).getText() == 'DELETE':
                i += 2
                table_name.append(ctx.getChild(i).getText())
            i += 1

            if ctx.getChild(i).getText() == 'WHERE':
                i += 1
            words10 = ctx.getChild(i).getText().split("AND")
            for item in words10:
                if '=' in item:
                    if "<=" in item:
                        words11 = item.split('<=')
                        sec_op.append('<=')
                        attributes.append(words11[0])
                        values.append(words11[1])
                    elif ">=" in item:
                        words11 = item.split('>=')
                        sec_op.append('>=')
                        attributes.append(words11[0])
                        values.append(words11[1])
                    elif "!=" in item:
                        words11 = item.split('!=')
                        sec_op.append('!=')
                        attributes.append(words11[0])
                        values.append(words11[1])
                    else:
                        words11 = item.split('=')
                        sec_op.append('=')
                        attributes.append(words11[0])
                        values.append(words11[1])
                elif '<' in item:
                    words11 = item.split('<')
                    sec_op.append('<')
                    attributes.append(words11[0])
                    values.append(words11[1])
                elif '>' in item:
                    words11 = item.split('>')
                    sec_op.append('>')
                    attributes.append(words11[0])
                    values.append(words11[1])

                i += 1

            # print(len(ctx.children))
            values = [x.replace('"', '') for x in values]
            values = [x.replace("'", '') for x in values]

            where = []
            for i in range(0, len(attributes)):
                where.append({"attribute": attributes[i], "value": values[i], "operation": sec_op[i]})

            d = self._db.delete(self._db.select(table_name[0]), where)
            print("Tuples deleted")
            d.print()

            # print(table_name)
            # print(attributes)
            # print(sec_op)
            # print(values)

            break

    # Exit a parse tree produced by SQLiteParser#delete_stmt.
    def exitDelete_stmt(self, ctx:SQLiteParser.Delete_stmtContext):
        pass


    # Enter a parse tree produced by SQLiteParser#delete_stmt_limited.
    def enterDelete_stmt_limited(self, ctx:SQLiteParser.Delete_stmt_limitedContext):
        pass

    # Exit a parse tree produced by SQLiteParser#delete_stmt_limited.
    def exitDelete_stmt_limited(self, ctx:SQLiteParser.Delete_stmt_limitedContext):
        pass


    # Enter a parse tree produced by SQLiteParser#detach_stmt.
    def enterDetach_stmt(self, ctx:SQLiteParser.Detach_stmtContext):
        pass

    # Exit a parse tree produced by SQLiteParser#detach_stmt.
    def exitDetach_stmt(self, ctx:SQLiteParser.Detach_stmtContext):
        pass


    # Enter a parse tree produced by SQLiteParser#drop_index_stmt.
    def enterDrop_index_stmt(self, ctx:SQLiteParser.Drop_index_stmtContext):
        index_name = ctx.getChild(2).getText()

        self._db.drop_index(index_name)

    # Exit a parse tree produced by SQLiteParser#drop_index_stmt.
    def exitDrop_index_stmt(self, ctx:SQLiteParser.Drop_index_stmtContext):
        pass


    # Enter a parse tree produced by SQLiteParser#drop_table_stmt.
    def enterDrop_table_stmt(self, ctx:SQLiteParser.Drop_table_stmtContext):
        table_name = ctx.getChild(2).getText()

        self._db.drop_table(table_name)

    # Exit a parse tree produced by SQLiteParser#drop_table_stmt.
    def exitDrop_table_stmt(self, ctx:SQLiteParser.Drop_table_stmtContext):
        pass


    # Enter a parse tree produced by SQLiteParser#drop_trigger_stmt.
    def enterDrop_trigger_stmt(self, ctx:SQLiteParser.Drop_trigger_stmtContext):
        pass

    # Exit a parse tree produced by SQLiteParser#drop_trigger_stmt.
    def exitDrop_trigger_stmt(self, ctx:SQLiteParser.Drop_trigger_stmtContext):
        pass


    # Enter a parse tree produced by SQLiteParser#drop_view_stmt.
    def enterDrop_view_stmt(self, ctx:SQLiteParser.Drop_view_stmtContext):
        pass

    # Exit a parse tree produced by SQLiteParser#drop_view_stmt.
    def exitDrop_view_stmt(self, ctx:SQLiteParser.Drop_view_stmtContext):
        pass


    # Enter a parse tree produced by SQLiteParser#factored_select_stmt.
    def enterFactored_select_stmt(self, ctx:SQLiteParser.Factored_select_stmtContext):
        pass


    # Exit a parse tree produced by SQLiteParser#factored_select_stmt.
    def exitFactored_select_stmt(self, ctx:SQLiteParser.Factored_select_stmtContext):
        pass


    # Enter a parse tree produced by SQLiteParser#insert_stmt.
    def enterInsert_stmt(self, ctx:SQLiteParser.Insert_stmtContext):
        table_names = []
        columns = []
        values = []

        table_names.append(ctx.getChild(2).getText())

        for i in range(len(ctx.children)):
            if ctx.getChild(i).getText() == '(':
                i = i + 1
                while ctx.getChild(i).getText() != ')':
                    if ctx.getChild(i).getText().isalpha():
                        columns.append(ctx.getChild(i).getText())
                    i += 1
            elif ctx.getChild(i).getText() == 'values':
                i += 1
                while ctx.getChild(i).getText() != ')':
                    i += 1
                    if ctx.getChild(i).getText().isalpha() or ctx.getChild(i).getText().isdigit():
                        values.append(ctx.getChild(i).getText())
                    if ctx.getChild(i).getText() == '“':
                        i += 1
                        hold = ''
                        while ctx.getChild(i).getText() != '”':
                            hold += ctx.getChild(i).getText()
                            i += 1
                        values.append(hold)
                    i += 1
                break

        # # return table_names, columns, values
        # print(table_names)
        # print(columns)
        # print(values)
        values = [x.replace('"', '') for x in values]
        values = [x.replace("'", '') for x in values]

        self._db.insert(table_names, columns, values)

    # Exit a parse tree produced by SQLiteParser#insert_stmt.
    def exitInsert_stmt(self, ctx:SQLiteParser.Insert_stmtContext):
        pass


    # Enter a parse tree produced by SQLiteParser#pragma_stmt.
    def enterPragma_stmt(self, ctx:SQLiteParser.Pragma_stmtContext):
        pass

    # Exit a parse tree produced by SQLiteParser#pragma_stmt.
    def exitPragma_stmt(self, ctx:SQLiteParser.Pragma_stmtContext):
        pass


    # Enter a parse tree produced by SQLiteParser#reindex_stmt.
    def enterReindex_stmt(self, ctx:SQLiteParser.Reindex_stmtContext):
        pass

    # Exit a parse tree produced by SQLiteParser#reindex_stmt.
    def exitReindex_stmt(self, ctx:SQLiteParser.Reindex_stmtContext):
        pass


    # Enter a parse tree produced by SQLiteParser#release_stmt.
    def enterRelease_stmt(self, ctx:SQLiteParser.Release_stmtContext):
        pass

    # Exit a parse tree produced by SQLiteParser#release_stmt.
    def exitRelease_stmt(self, ctx:SQLiteParser.Release_stmtContext):
        pass


    # Enter a parse tree produced by SQLiteParser#rollback_stmt.
    def enterRollback_stmt(self, ctx:SQLiteParser.Rollback_stmtContext):
        pass

    # Exit a parse tree produced by SQLiteParser#rollback_stmt.
    def exitRollback_stmt(self, ctx:SQLiteParser.Rollback_stmtContext):
        pass


    # Enter a parse tree produced by SQLiteParser#savepoint_stmt.
    def enterSavepoint_stmt(self, ctx:SQLiteParser.Savepoint_stmtContext):
        pass

    # Exit a parse tree produced by SQLiteParser#savepoint_stmt.
    def exitSavepoint_stmt(self, ctx:SQLiteParser.Savepoint_stmtContext):
        pass


    # Enter a parse tree produced by SQLiteParser#simple_select_stmt.
    def enterSimple_select_stmt(self, ctx:SQLiteParser.Simple_select_stmtContext):
        pass

    # Exit a parse tree produced by SQLiteParser#simple_select_stmt.
    def exitSimple_select_stmt(self, ctx:SQLiteParser.Simple_select_stmtContext):
        pass


    # Enter a parse tree produced by SQLiteParser#select_stmt.
    def enterSelect_stmt(self, ctx:SQLiteParser.Select_stmtContext):
        pass

    # Exit a parse tree produced by SQLiteParser#select_stmt.
    def exitSelect_stmt(self, ctx:SQLiteParser.Select_stmtContext):
        pass


    # Enter a parse tree produced by SQLiteParser#select_or_values.
    def enterSelect_or_values(self, ctx:SQLiteParser.Select_or_valuesContext):
        pass

    # Exit a parse tree produced by SQLiteParser#select_or_values.
    def exitSelect_or_values(self, ctx:SQLiteParser.Select_or_valuesContext):
        pass


    # Enter a parse tree produced by SQLiteParser#update_stmt.
    def enterUpdate_stmt(self, ctx:SQLiteParser.Update_stmtContext):
        table_name = []
        columns = []
        col_val = []
        column_op = []
        attributes = []
        values = []
        sec_op = []

        for i in range(len(ctx.children)):

            if ctx.getChild(i).getText() == 'UPDATE':
                i += 1
                table_name.append(ctx.getChild(i).getText())
            i += 1

            if ctx.getChild(i).getText() == 'SET':
                i += 1

            while ctx.getChild(i).getText() != "WHERE":

                if ctx.getChild(i).getText() == ',':
                    i += 1

                columns.append(ctx.getChild(i).getText())
                i += 1
                column_op.append(ctx.getChild(i).getText())
                i += 1
                col_val.append(ctx.getChild(i).getText())
                i += 1

            i += 1

            words10 = ctx.getChild(i).getText().split("AND")
            for item in words10:
                if '=' in item:
                    if "<=" in item:
                        words11 = item.split('<=')
                        sec_op.append('<=')
                        attributes.append(words11[0])
                        values.append(words11[1])
                    elif ">=" in item:
                        words11 = item.split('>=')
                        sec_op.append('>=')
                        attributes.append(words11[0])
                        values.append(words11[1])
                    elif "!=" in item:
                        words11 = item.split('!=')
                        sec_op.append('!=')
                        attributes.append(words11[0])
                        values.append(words11[1])
                    else:
                        words11 = item.split('=')
                        sec_op.append('=')
                        attributes.append(words11[0])
                        values.append(words11[1])
                elif '<' in item:
                    words11 = item.split('<')
                    sec_op.append('<')
                    attributes.append(words11[0])
                    values.append(words11[1])
                elif '>' in item:
                    words11 = item.split('>')
                    sec_op.append('>')
                    attributes.append(words11[0])
                    values.append(words11[1])
                i += 1


            #print(len(ctx.children))
            # print(table_name)
            # print(columns)
            # print(col_val)
            # print(column_op)
            # print(attributes)
            # print(sec_op)
            # print(values)

            values = [x.replace('"', '') for x in values]
            values = [x.replace("'", '') for x in values]

            col_val = [x.replace('"', '') for x in col_val]
            col_val = [x.replace("'", '') for x in col_val]

            # rs = [x.replace('"', '') for x in rs]
            # rs = [x.replace("'", '') for x in rs]

            # update(self, relation, values, where):
            update_values = []
            for i in range(0, len(columns)):
                update_values.append({"attribute": columns[i], "value": col_val[i]})
            where_values = []
            for i in range(0, len(attributes)):
                where_values.append({"attribute": attributes[i], "value": values[i], "operation": sec_op[i]})

            u = self._db.update(self._db.select(table_name[0]), update_values, where_values)
            print("Relation updated")
            u.print()
            break

    # Exit a parse tree produced by SQLiteParser#update_stmt.
    def exitUpdate_stmt(self, ctx:SQLiteParser.Update_stmtContext):
        pass


    # Enter a parse tree produced by SQLiteParser#update_stmt_limited.
    def enterUpdate_stmt_limited(self, ctx:SQLiteParser.Update_stmt_limitedContext):
        pass

    # Exit a parse tree produced by SQLiteParser#update_stmt_limited.
    def exitUpdate_stmt_limited(self, ctx:SQLiteParser.Update_stmt_limitedContext):
        pass


    # Enter a parse tree produced by SQLiteParser#vacuum_stmt.
    def enterVacuum_stmt(self, ctx:SQLiteParser.Vacuum_stmtContext):
        pass

    # Exit a parse tree produced by SQLiteParser#vacuum_stmt.
    def exitVacuum_stmt(self, ctx:SQLiteParser.Vacuum_stmtContext):
        pass


    # Enter a parse tree produced by SQLiteParser#column_def.
    def enterColumn_def(self, ctx:SQLiteParser.Column_defContext):
        pass

    # Exit a parse tree produced by SQLiteParser#column_def.
    def exitColumn_def(self, ctx:SQLiteParser.Column_defContext):
        pass


    # Enter a parse tree produced by SQLiteParser#type_name.
    def enterType_name(self, ctx:SQLiteParser.Type_nameContext):
        pass

    # Exit a parse tree produced by SQLiteParser#type_name.
    def exitType_name(self, ctx:SQLiteParser.Type_nameContext):
        pass


    # Enter a parse tree produced by SQLiteParser#column_constraint.
    def enterColumn_constraint(self, ctx:SQLiteParser.Column_constraintContext):
        pass

    # Exit a parse tree produced by SQLiteParser#column_constraint.
    def exitColumn_constraint(self, ctx:SQLiteParser.Column_constraintContext):
        pass


    # Enter a parse tree produced by SQLiteParser#conflict_clause.
    def enterConflict_clause(self, ctx:SQLiteParser.Conflict_clauseContext):
        pass

    # Exit a parse tree produced by SQLiteParser#conflict_clause.
    def exitConflict_clause(self, ctx:SQLiteParser.Conflict_clauseContext):
        pass


    # Enter a parse tree produced by SQLiteParser#expr.
    def enterExpr(self, ctx:SQLiteParser.ExprContext):
        pass

    # Exit a parse tree produced by SQLiteParser#expr.
    def exitExpr(self, ctx:SQLiteParser.ExprContext):
        pass


    # Enter a parse tree produced by SQLiteParser#foreign_key_clause.
    def enterForeign_key_clause(self, ctx:SQLiteParser.Foreign_key_clauseContext):
        pass

    # Exit a parse tree produced by SQLiteParser#foreign_key_clause.
    def exitForeign_key_clause(self, ctx:SQLiteParser.Foreign_key_clauseContext):
        pass


    # Enter a parse tree produced by SQLiteParser#raise_function.
    def enterRaise_function(self, ctx:SQLiteParser.Raise_functionContext):
        pass

    # Exit a parse tree produced by SQLiteParser#raise_function.
    def exitRaise_function(self, ctx:SQLiteParser.Raise_functionContext):
        pass


    # Enter a parse tree produced by SQLiteParser#indexed_column.
    def enterIndexed_column(self, ctx:SQLiteParser.Indexed_columnContext):
        pass

    # Exit a parse tree produced by SQLiteParser#indexed_column.
    def exitIndexed_column(self, ctx:SQLiteParser.Indexed_columnContext):
        pass


    # Enter a parse tree produced by SQLiteParser#table_constraint.
    def enterTable_constraint(self, ctx:SQLiteParser.Table_constraintContext):
        pass

    # Exit a parse tree produced by SQLiteParser#table_constraint.
    def exitTable_constraint(self, ctx:SQLiteParser.Table_constraintContext):
        pass


    # Enter a parse tree produced by SQLiteParser#with_clause.
    def enterWith_clause(self, ctx:SQLiteParser.With_clauseContext):
        pass

    # Exit a parse tree produced by SQLiteParser#with_clause.
    def exitWith_clause(self, ctx:SQLiteParser.With_clauseContext):
        pass


    # Enter a parse tree produced by SQLiteParser#qualified_table_name.
    def enterQualified_table_name(self, ctx:SQLiteParser.Qualified_table_nameContext):
        pass

    # Exit a parse tree produced by SQLiteParser#qualified_table_name.
    def exitQualified_table_name(self, ctx:SQLiteParser.Qualified_table_nameContext):
        pass


    # Enter a parse tree produced by SQLiteParser#ordering_term.
    def enterOrdering_term(self, ctx:SQLiteParser.Ordering_termContext):
        pass

    # Exit a parse tree produced by SQLiteParser#ordering_term.
    def exitOrdering_term(self, ctx:SQLiteParser.Ordering_termContext):
        pass


    # Enter a parse tree produced by SQLiteParser#pragma_value.
    def enterPragma_value(self, ctx:SQLiteParser.Pragma_valueContext):
        pass

    # Exit a parse tree produced by SQLiteParser#pragma_value.
    def exitPragma_value(self, ctx:SQLiteParser.Pragma_valueContext):
        pass


    # Enter a parse tree produced by SQLiteParser#common_table_expression.
    def enterCommon_table_expression(self, ctx:SQLiteParser.Common_table_expressionContext):
        pass

    # Exit a parse tree produced by SQLiteParser#common_table_expression.
    def exitCommon_table_expression(self, ctx:SQLiteParser.Common_table_expressionContext):
        pass


    # Enter a parse tree produced by SQLiteParser#result_column.
    def enterResult_column(self, ctx:SQLiteParser.Result_columnContext):
        pass

    # Exit a parse tree produced by SQLiteParser#result_column.
    def exitResult_column(self, ctx:SQLiteParser.Result_columnContext):
        pass


    # Enter a parse tree produced by SQLiteParser#table_or_subquery.
    def enterTable_or_subquery(self, ctx:SQLiteParser.Table_or_subqueryContext):
        pass

    # Exit a parse tree produced by SQLiteParser#table_or_subquery.
    def exitTable_or_subquery(self, ctx:SQLiteParser.Table_or_subqueryContext):
        pass


    # Enter a parse tree produced by SQLiteParser#join_clause.
    def enterJoin_clause(self, ctx:SQLiteParser.Join_clauseContext):
        pass

    # Exit a parse tree produced by SQLiteParser#join_clause.
    def exitJoin_clause(self, ctx:SQLiteParser.Join_clauseContext):
        pass


    # Enter a parse tree produced by SQLiteParser#join_operator.
    def enterJoin_operator(self, ctx:SQLiteParser.Join_operatorContext):
        pass

    # Exit a parse tree produced by SQLiteParser#join_operator.
    def exitJoin_operator(self, ctx:SQLiteParser.Join_operatorContext):
        pass


    # Enter a parse tree produced by SQLiteParser#join_constraint.
    def enterJoin_constraint(self, ctx:SQLiteParser.Join_constraintContext):
        pass

    # Exit a parse tree produced by SQLiteParser#join_constraint.
    def exitJoin_constraint(self, ctx:SQLiteParser.Join_constraintContext):
        pass


    # Enter a parse tree produced by SQLiteParser#select_core.
    def enterSelect_core(self, ctx:SQLiteParser.Select_coreContext):
        print("Query parsed")

        table_names = []
        join_tables = []
        columns = []
        col_names = []
        ls = []
        rs = []
        operators = []
        on_left = []
        on_right = []
        on_op = []
        i = 0
        while i != len(ctx.children):
            if ctx.getChild(i) and ctx.getChild(i).getText() == 'SELECT':
                i += 1
            if not ctx.getChild(i):
                break

            while ctx.getChild(i).getText() != 'FROM':
                if 'AS' in ctx.getChild(i).getText():
                    # print("TRUEEEEE")
                    # print(ctx.getChild(i).getText())
                    words = ctx.getChild(i).getText().split('AS')
                    # print(words)
                    columns.append(words[0])
                    col_names.append(words[1])

                elif ctx.getChild(i).getText().isalpha() or ctx.getChild(i).getText() == '*':
                    columns.append(ctx.getChild(i).getText())

                elif "." in ctx.getChild(i).getText() and 'AS' not in ctx.getChild(i).getText():
                    columns.append(ctx.getChild(i).getText())
                    words2 = ctx.getChild(i).getText().split('.')
                    col_names.append(words2[1])

                else:
                    pass
                i += 1
            i += 1

            while 'INNERJOIN' in ctx.getChild(i).getText() == False or ctx.getChild(i).getText() != '<EOF>':
                if 'INNERJOIN' in ctx.getChild(i).getText():
                    break
                # print(ctx.getChild(i).getText())
                table_names.append(ctx.getChild(i).getText())
                # join_tables.append(ctx.getChild(i).getText())
                # print(ctx.getChild(i).getText())

                if ctx.getChild(i).getText() == ctx.getChild(-1).getText():
                    break

                if ',' in ctx.getChild(i + 1).getText():
                    i += 2
                    # table_names.append(ctx.getChild(i).getText())
                else:
                    i += 1

            # print("HEY", ctx.getChild(i).getText())

            if 'INNERJOIN' in ctx.getChild(i).getText():
                words4 = ctx.getChild(i).getText().split('INNERJOIN')
                # print("HEY", words4)
                join_tables.append(words4[0])
                second_table = words4[1]
                join_tables.append(second_table[0])

                if 'ON' in words4[1]:
                    words5 = words4[1].split('ON')
                    if '=' in words5[1]:
                        if '<=' in words5[1]:
                            words9 = words5[1].split('<=')
                            on_left.append(words9[0])
                            on_right.append(words9[1])
                            on_op.append('<=')
                        elif '>=' in words5[1]:
                            words9 = words5[1].split('>=')
                            on_left.append(words9[0])
                            on_right.append(words9[1])
                            on_op.append('>=')
                        elif '!=' in words5[1]:
                            words9 = words5[1].split('!=')
                            on_left.append(words9[0])
                            on_right.append(words9[1])
                            on_op.append('!=')
                        else:
                            words9 = words5[1].split('=')
                            on_left.append(words9[0])
                            on_right.append(words9[1])
                            on_op.append('=')
                    elif '<' in words5[1]:
                        words9 = words5[1].split('<')
                        on_left.append(words9[0])
                        on_right.append(words9[1])
                        on_op.append('<')
                    elif '>' in words5[1]:
                        words9 = words5[1].split('>')
                        on_left.append(words9[0])
                        on_right.append(words9[1])
                        on_op.append('>')
                    elif '>=' in words5[1]:
                        words9 = words5[1].split('>=')
                        on_left.append(words9[0])
                        on_right.append(words9[1])
                        on_op.append('>=')
                    elif '<=' in words5[1]:
                        words9 = item.split('<=')
                        on_left.append(words9[0])
                        on_right.append(words9[1])
                        on_op.append('<=')
                    elif '!=' in words5[1]:
                        words9 = item.split('!=')
                        on_left.append(words9[0])
                        on_right.append(words9[1])
                        on_op.append('!=')

                i += 2

            if ctx.getChild(i) and 'AND' in ctx.getChild(i).getText():
                words8 = ctx.getChild(i).getText().split('AND')
                for item in words8:
                    if '=' in item:
                        if '>=' in item:
                            words9 = item.split('>=')
                            ls.append(words9[0])
                            rs.append(words9[1])
                            operators.append('>=')
                        elif "<=" in item:
                            words9 = item.split('<=')
                            ls.append(words9[0])
                            rs.append(words9[1])
                            operators.append('<=')
                        elif "!=" in item:
                            words9 = item.split('!=')
                            ls.append(words9[0])
                            rs.append(words9[1])
                            operators.append('!=')
                        else:
                            words9 = item.split('=')
                            ls.append(words9[0])
                            rs.append(words9[1])
                            operators.append('=')
                    elif '<' in item:
                        words9 = item.split('<')
                        ls.append(words9[0])
                        rs.append(words9[1])
                        operators.append('<')
                    elif '>' in item:
                        words9 = item.split('>')
                        ls.append(words9[0])
                        rs.append(words9[1])
                        operators.append('>')

            elif ctx.getChild(i) and not "AND" in ctx.getChild(i).getText():
                print(ctx.getChild(i).getText())
                item = ctx.getChild(i).getText()
                if '=' in item:
                    if '<=' in item:
                        words9 = item.split('<=')
                        ls.append(words9[0])
                        rs.append(words9[1])
                        operators.append('<=')
                    elif '>=' in item:
                        words9 = item.split('>=')
                        ls.append(words9[0])
                        rs.append(words9[1])
                        operators.append('>=')
                    elif '!=' in item:
                        words9 = item.split('!=')
                        ls.append(words9[0])
                        rs.append(words9[1])
                        operators.append('!=')
                    else:
                        words9 = item.split('=')
                        ls.append(words9[0])
                        rs.append(words9[1])
                        operators.append('=')
                elif '<' in item:
                    words9 = item.split('<')
                    ls.append(words9[0])
                    rs.append(words9[1])
                    operators.append('<')
                elif '>' in item:
                    words9 = item.split('>')
                    ls.append(words9[0])
                    rs.append(words9[1])
                    operators.append('>')
                elif '>=' in item:
                    words9 = item.split('>=')
                    ls.append(words9[0])
                    rs.append(words9[1])
                    operators.append('>=')
                elif '<=' in item:
                    words9 = item.split('<=')
                    ls.append(words9[0])
                    rs.append(words9[1])
                    operators.append('<=')
                elif '!=' in item:
                    words9 = item.split('!=')
                    ls.append(words9[0])
                    rs.append(words9[1])
                    operators.append('!=')

            # print(i)
            # print(words4)
            # print(words5)
            i += 1

            if 'WHERE' in table_names:
                table_names.pop()
                table_names.pop()

        # print(table_names)
        # print(join_tables)
        # print(columns)
        # print(col_names)
        # print(on_left)
        # print(on_op)
        # print(on_right)
        # print(ls)
        # print(operators)
        # print(rs)
        # print(values)

        col_names = [x.replace('"', '') for x in col_names]
        col_names = [x.replace("'", '') for x in col_names]

        rs = [x.replace('"', '') for x in rs]
        rs = [x.replace("'", '') for x in rs]

        if len(join_tables) > 0:
            left_table = join_tables[0]
            right_table = join_tables[1]
            on_left_new = []
            for l_col in on_left:
                if l_col.find(join_tables[0] + ".") != -1:
                    on_left_new.append(l_col[l_col.find(join_tables[0] + ".") + len(join_tables[0] + "."):])
                else:
                    on_left_new.append(l_col)
            on_right_new = []
            for r_col in on_right:
                if r_col.find(join_tables[1] + ".") != -1:
                    on_right_new.append(r_col[r_col.find(join_tables[1] + ".") + len(join_tables[1] + "."):])
                else:
                    on_right_new.append(r_col)

            left_t_select_abutes = []
            righ_t_select_abutes = []
            i = 0
            for abute in ls:
                if abute.find(join_tables[0] + ".") != -1:
                    left_t_select_abutes.append(
                        {"attribute": abute[abute.find(join_tables[0] + ".") + len(join_tables[0] + "."):],
                         "value": rs[i], "operation": operators[i]})
                if abute.find(join_tables[1] + ".") != -1:
                    rhs_bute = abute[abute.find(join_tables[1] + ".") + len(join_tables[1] + "."):]
                    # rhs_bute = "right_side_" + rhs_bute
                    righ_t_select_abutes.append(
                        {"attribute": rhs_bute, "value": rs[i], "operation": operators[i]})
                i += 1

            if len(left_t_select_abutes) == 0:
                left_t_select_abutes = None
            if len(righ_t_select_abutes) == 0:
                righ_t_select_abutes = None
            lt = self._db.select(left_table, left_t_select_abutes)
            rt = self._db.select(right_table, righ_t_select_abutes)
            lt.print()
            rt.print()
            j = self._db.join(lt, rt, on_left_new, on_right_new, on_op)

            final_select_attributes = []
            i = 0
            for abute in ls:
                if abute.find(join_tables[0] + ".") != -1:
                    final_select_attributes.append({"attribute": abute[abute.find(join_tables[0] + ".") + len(join_tables[0] + "."):], "value": rs[i], "operation": operators[i]})
                elif abute.find(join_tables[1] + ".") != -1:
                    rhs_bute = abute[abute.find(join_tables[1] + ".") + len(join_tables[1] + "."):]
                    rhs_bute = "right_side_" + rhs_bute
                    final_select_attributes.append(
                        {"attribute": rhs_bute, "value": rs[i], "operation": operators[i]})
                else:
                    final_select_attributes.append({"attribute": abute, "value": rs[i], "operation": operators[i]})
                i += 1
            if len(final_select_attributes) == 0:
                final_select_attributes = None
            # SELECT C.id, B.value2 FROM C INNER JOIN B ON C.id = B.value WHERE B.value2 = 95
            s = self._db.select(j, final_select_attributes)

            if columns == ["*"]:
                s.print()
            else:
                final_projection_abutes = []
                for abute in columns:
                    if abute.find(join_tables[0] + ".") != -1:
                        final_projection_abutes.append(
                            abute[abute.find(join_tables[0] + ".") + len(join_tables[0] + "."):])
                    elif abute.find(join_tables[1] + ".") != -1:
                        rhs_bute = abute[abute.find(join_tables[1] + ".") + len(join_tables[1] + "."):]
                        rhs_bute = "right_side_" + rhs_bute
                        final_projection_abutes.append(rhs_bute)
                    else:
                        final_projection_abutes.append(abute)

                final_column_names = []
                for abute in col_names:
                    if abute.find(join_tables[0] + ".") != -1:
                        final_column_names.append(abute[abute.find(join_tables[0] + ".") + len(join_tables[0] + "."):])
                    elif abute.find(join_tables[1] + ".") != -1:
                        rhs_bute = abute[abute.find(join_tables[1] + ".") + len(join_tables[1] + "."):]
                        rhs_bute = "right_side_" + rhs_bute
                        final_column_names.append(rhs_bute)
                    else:
                        final_column_names.append(abute)
                self._db.project(s, final_projection_abutes, final_column_names, lose_rhs=True).print()
            # join_tables_dict = {}
            # for table in join_tables:
            #     join_tables_dict[table] = {"project": [], "select": []}
            # on_left_new = []
            # for l_col in on_left:
            #     if l_col.find(join_tables[0] + ".") == -1:
            #         on_left_new.append(join_tables[0] + "." + l_col)
            #     else:
            #         on_left_new.append(l_col)
            # for table in join_tables_dict.keys():
            #
            #
            #     columns_to_project = list(set(columns + on_left_new))
            #     names_to_project = []
            #     for i in range(0, len(columns_to_project)):
            #         for j in range(0, len(columns)):
            #             if columns_to_project[i] == columns[j]:
            #                 names_to_project.append(col_names[j])
            #         if j == len(columns) and i + 1 != len(names_to_project):
            #             names_to_project.append(columns_to_project[i])
            #
            #     i = 0
            #     for column in columns_to_project:
            #         if column.find(table + ".") != -1:
            #             column = column[column.find(table + ".") + len(table + "."):]
            #             print(join_tables_dict[table])
            #             join_tables_dict[table]["project"].append({"attribute": column, "as": col_names[i]})
            #         i += 1
        else:
            print("regular select")
            t = self._db.select(table_names[0])

            final_select_attributes = []
            i = 0
            for abute in ls:
                if abute.find(table_names[0] + ".") != -1:
                    final_select_attributes.append(
                        {"attribute": abute[abute.find(table_names[0] + ".") + len(table_names[0] + "."):],
                         "value": rs[i], "operation": operators[i]})
                else:
                    final_select_attributes.append({"attribute": abute, "value": rs[i], "operation": operators[i]})
                i += 1
            if len(final_select_attributes) == 0:
                final_select_attributes = None

            s = self._db.select(t, final_select_attributes).print()



    # Exit a parse tree produced by SQLiteParser#select_core.
    def exitSelect_core(self, ctx:SQLiteParser.Select_coreContext):
        pass


    # Enter a parse tree produced by SQLiteParser#compound_operator.
    def enterCompound_operator(self, ctx:SQLiteParser.Compound_operatorContext):
        pass

    # Exit a parse tree produced by SQLiteParser#compound_operator.
    def exitCompound_operator(self, ctx:SQLiteParser.Compound_operatorContext):
        pass


    # Enter a parse tree produced by SQLiteParser#cte_table_name.
    def enterCte_table_name(self, ctx:SQLiteParser.Cte_table_nameContext):
        pass

    # Exit a parse tree produced by SQLiteParser#cte_table_name.
    def exitCte_table_name(self, ctx:SQLiteParser.Cte_table_nameContext):
        pass


    # Enter a parse tree produced by SQLiteParser#signed_number.
    def enterSigned_number(self, ctx:SQLiteParser.Signed_numberContext):
        pass

    # Exit a parse tree produced by SQLiteParser#signed_number.
    def exitSigned_number(self, ctx:SQLiteParser.Signed_numberContext):
        pass


    # Enter a parse tree produced by SQLiteParser#literal_value.
    def enterLiteral_value(self, ctx:SQLiteParser.Literal_valueContext):
        pass

    # Exit a parse tree produced by SQLiteParser#literal_value.
    def exitLiteral_value(self, ctx:SQLiteParser.Literal_valueContext):
        pass


    # Enter a parse tree produced by SQLiteParser#unary_operator.
    def enterUnary_operator(self, ctx:SQLiteParser.Unary_operatorContext):
        pass

    # Exit a parse tree produced by SQLiteParser#unary_operator.
    def exitUnary_operator(self, ctx:SQLiteParser.Unary_operatorContext):
        pass


    # Enter a parse tree produced by SQLiteParser#error_message.
    def enterError_message(self, ctx:SQLiteParser.Error_messageContext):
        pass

    # Exit a parse tree produced by SQLiteParser#error_message.
    def exitError_message(self, ctx:SQLiteParser.Error_messageContext):
        pass


    # Enter a parse tree produced by SQLiteParser#module_argument.
    def enterModule_argument(self, ctx:SQLiteParser.Module_argumentContext):
        pass

    # Exit a parse tree produced by SQLiteParser#module_argument.
    def exitModule_argument(self, ctx:SQLiteParser.Module_argumentContext):
        pass


    # Enter a parse tree produced by SQLiteParser#column_alias.
    def enterColumn_alias(self, ctx:SQLiteParser.Column_aliasContext):
        pass

    # Exit a parse tree produced by SQLiteParser#column_alias.
    def exitColumn_alias(self, ctx:SQLiteParser.Column_aliasContext):
        pass


    # Enter a parse tree produced by SQLiteParser#keyword.
    def enterKeyword(self, ctx:SQLiteParser.KeywordContext):
        pass

    # Exit a parse tree produced by SQLiteParser#keyword.
    def exitKeyword(self, ctx:SQLiteParser.KeywordContext):
        pass


    # Enter a parse tree produced by SQLiteParser#name.
    def enterName(self, ctx:SQLiteParser.NameContext):
        pass

    # Exit a parse tree produced by SQLiteParser#name.
    def exitName(self, ctx:SQLiteParser.NameContext):
        pass


    # Enter a parse tree produced by SQLiteParser#function_name.
    def enterFunction_name(self, ctx:SQLiteParser.Function_nameContext):
        pass

    # Exit a parse tree produced by SQLiteParser#function_name.
    def exitFunction_name(self, ctx:SQLiteParser.Function_nameContext):
        pass


    # Enter a parse tree produced by SQLiteParser#database_name.
    def enterDatabase_name(self, ctx:SQLiteParser.Database_nameContext):
        pass

    # Exit a parse tree produced by SQLiteParser#database_name.
    def exitDatabase_name(self, ctx:SQLiteParser.Database_nameContext):
        pass


    # Enter a parse tree produced by SQLiteParser#table_name.
    def enterTable_name(self, ctx:SQLiteParser.Table_nameContext):
        pass

    # Exit a parse tree produced by SQLiteParser#table_name.
    def exitTable_name(self, ctx:SQLiteParser.Table_nameContext):
        pass


    # Enter a parse tree produced by SQLiteParser#table_or_index_name.
    def enterTable_or_index_name(self, ctx:SQLiteParser.Table_or_index_nameContext):
        pass

    # Exit a parse tree produced by SQLiteParser#table_or_index_name.
    def exitTable_or_index_name(self, ctx:SQLiteParser.Table_or_index_nameContext):
        pass


    # Enter a parse tree produced by SQLiteParser#new_table_name.
    def enterNew_table_name(self, ctx:SQLiteParser.New_table_nameContext):
        pass

    # Exit a parse tree produced by SQLiteParser#new_table_name.
    def exitNew_table_name(self, ctx:SQLiteParser.New_table_nameContext):
        pass


    # Enter a parse tree produced by SQLiteParser#column_name.
    def enterColumn_name(self, ctx:SQLiteParser.Column_nameContext):
        pass

    # Exit a parse tree produced by SQLiteParser#column_name.
    def exitColumn_name(self, ctx:SQLiteParser.Column_nameContext):
        pass


    # Enter a parse tree produced by SQLiteParser#collation_name.
    def enterCollation_name(self, ctx:SQLiteParser.Collation_nameContext):
        pass

    # Exit a parse tree produced by SQLiteParser#collation_name.
    def exitCollation_name(self, ctx:SQLiteParser.Collation_nameContext):
        pass


    # Enter a parse tree produced by SQLiteParser#foreign_table.
    def enterForeign_table(self, ctx:SQLiteParser.Foreign_tableContext):
        pass

    # Exit a parse tree produced by SQLiteParser#foreign_table.
    def exitForeign_table(self, ctx:SQLiteParser.Foreign_tableContext):
        pass


    # Enter a parse tree produced by SQLiteParser#index_name.
    def enterIndex_name(self, ctx:SQLiteParser.Index_nameContext):
        pass

    # Exit a parse tree produced by SQLiteParser#index_name.
    def exitIndex_name(self, ctx:SQLiteParser.Index_nameContext):
        pass


    # Enter a parse tree produced by SQLiteParser#trigger_name.
    def enterTrigger_name(self, ctx:SQLiteParser.Trigger_nameContext):
        pass

    # Exit a parse tree produced by SQLiteParser#trigger_name.
    def exitTrigger_name(self, ctx:SQLiteParser.Trigger_nameContext):
        pass


    # Enter a parse tree produced by SQLiteParser#view_name.
    def enterView_name(self, ctx:SQLiteParser.View_nameContext):
        pass

    # Exit a parse tree produced by SQLiteParser#view_name.
    def exitView_name(self, ctx:SQLiteParser.View_nameContext):
        pass


    # Enter a parse tree produced by SQLiteParser#module_name.
    def enterModule_name(self, ctx:SQLiteParser.Module_nameContext):
        pass

    # Exit a parse tree produced by SQLiteParser#module_name.
    def exitModule_name(self, ctx:SQLiteParser.Module_nameContext):
        pass


    # Enter a parse tree produced by SQLiteParser#pragma_name.
    def enterPragma_name(self, ctx:SQLiteParser.Pragma_nameContext):
        pass

    # Exit a parse tree produced by SQLiteParser#pragma_name.
    def exitPragma_name(self, ctx:SQLiteParser.Pragma_nameContext):
        pass


    # Enter a parse tree produced by SQLiteParser#savepoint_name.
    def enterSavepoint_name(self, ctx:SQLiteParser.Savepoint_nameContext):
        pass

    # Exit a parse tree produced by SQLiteParser#savepoint_name.
    def exitSavepoint_name(self, ctx:SQLiteParser.Savepoint_nameContext):
        pass


    # Enter a parse tree produced by SQLiteParser#table_alias.
    def enterTable_alias(self, ctx:SQLiteParser.Table_aliasContext):
        pass

    # Exit a parse tree produced by SQLiteParser#table_alias.
    def exitTable_alias(self, ctx:SQLiteParser.Table_aliasContext):
        pass


    # Enter a parse tree produced by SQLiteParser#transaction_name.
    def enterTransaction_name(self, ctx:SQLiteParser.Transaction_nameContext):
        pass

    # Exit a parse tree produced by SQLiteParser#transaction_name.
    def exitTransaction_name(self, ctx:SQLiteParser.Transaction_nameContext):
        pass


    # Enter a parse tree produced by SQLiteParser#any_name.
    def enterAny_name(self, ctx:SQLiteParser.Any_nameContext):
        pass

    # Exit a parse tree produced by SQLiteParser#any_name.
    def exitAny_name(self, ctx:SQLiteParser.Any_nameContext):
        pass


