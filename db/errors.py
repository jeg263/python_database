class Error(Exception):
    pass

class SQLInputError(Error):
    pass

class DuplicateFK(Error):
    pass


class DuplicateIndex(Error):
    pass


class DuplicateAttribute(Error):
    pass


class DuplicateRelation(Error):
    pass


class IndexesError(Error):
    pass


class ForeignKeyError(Error):
    pass