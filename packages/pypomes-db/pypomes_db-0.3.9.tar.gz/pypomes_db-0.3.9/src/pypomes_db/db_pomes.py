from logging import Logger
from typing import Any

from .db_common import DB_ENGINE

match DB_ENGINE:
    case "oracle":
        from . import oracle_pomes
    case "postgres":
        from . import postgres_pomes
    case "sqlserver":
        from . import sqlserver_pomes


def db_connect(errors: list[str] | None,
               logger: Logger = None) -> Any:
    """
    Obtain and return a connection to the database, or *None* if the connection cannot be obtained.

    :param errors: incidental error messages
    :param logger: optional logger
    :return: the connection to the database
    """
    result: Any = None
    match DB_ENGINE:
        case "postgres":
            result = postgres_pomes.db_connect(errors, logger)
        case "sqlserver":
            result = sqlserver_pomes.db_connect(errors, logger)

    return result


def db_exists(errors: list[str],
              table: str,
              where_attrs: list[str],
              where_vals: tuple,
              logger: Logger = None) -> bool:
    """
    Determine whether the table *table* in the database contains at least one tuple.

    For this determination, *where_attrs* are made equal to *where_values* in the query, respectively.
    If more than one, the attributes are concatenated by the *AND* logical connector.

    :param errors: incidental error messages
    :param table: the table to be searched
    :param where_attrs: the search attributes
    :param where_vals: the values for the search attributes
    :param logger: optional logger
    :return: True if at least one tuple was found
    """
    # noinspection PyDataSource
    sel_stmt: str = "SELECT * FROM " + table
    if len(where_attrs) > 0:
        sel_stmt += " WHERE " + "".join(f"{attr} = %s AND " for attr in where_attrs)[0:-5]
    rec: tuple = db_select_one(errors=errors,
                               sel_stmt=sel_stmt,
                               where_vals=where_vals,
                               require_nonempty=False,
                               logger=logger)
    result: bool = None if len(errors) > 0 else rec is not None

    return result


def db_select_one(errors: list[str] | None,
                  sel_stmt: str,
                  where_vals: tuple,
                  require_nonempty: bool = False,
                  logger: Logger = None) -> tuple:
    """
    Search the database and return the first tuple that satisfies the *sel_stmt* search command.

    The command can optionally contain search criteria, with respective values given
    in *where_vals*. The list of values for an attribute with the *IN* clause must be contained
    in a specific tuple. In case of error, or if the search is empty, *None* is returned.

    :param errors: incidental error messages
    :param sel_stmt: SELECT command for the search
    :param where_vals: values to be associated with the search criteria
    :param require_nonempty: defines whether an empty search should be considered an error
    :param logger: optional logger
    :return: tuple containing the search result, or None if there was an error, or if the search was empty
    """
    require_min: int = 1 if require_nonempty else None
    reply: list[tuple] = db_select_all(errors=errors,
                                       sel_stmt=sel_stmt,
                                       where_vals=where_vals,
                                       require_min=require_min,
                                       require_max=1,
                                       logger=logger)

    return reply[0] if reply else None


def db_select_all(errors: list[str] | None,
                  sel_stmt: str,
                  where_vals: tuple = None,
                  require_min: int = None,
                  require_max: int = None,
                  logger: Logger = None) -> list[tuple]:
    """
    Search the database and return all tuples that satisfy the *sel_stmt* search command.

    The command can optionally contain search criteria, with respective values given
    in *where_vals*. The list of values for an attribute with the *IN* clause must be contained
    in a specific tuple. If not positive integers, *require_min* and *require_max* are ignored.
    If the search is empty, an empty list is returned.

    :param errors: incidental error messages
    :param sel_stmt: SELECT command for the search
    :param where_vals: the values to be associated with the search criteria
    :param require_min: optionally defines the minimum number of tuples to be returned
    :param require_max: optionally defines the maximum number of tuples to be returned
    :param logger: optional logger
    :return: list of tuples containing the search result, or [] if the search is empty
    """
    result: list[tuple] | None = None
    match DB_ENGINE:
        case "oracle":
            result = oracle_pomes.db_select_all(errors, sel_stmt, where_vals, require_min, require_max,  logger)
        case "postgres":
            result = postgres_pomes.db_select_all(errors, sel_stmt, where_vals, require_min, require_max,  logger)
        case "sqlserver":
            result = sqlserver_pomes.db_select_all(errors, sel_stmt, where_vals, require_min, require_max, logger)

    return result


def db_insert(errors: list[str] | None,
              insert_stmt: str,
              insert_vals: tuple,
              logger: Logger = None) -> int:
    """
    Insert a tuple, with values defined in *insert_vals*, into the database.

    :param errors: incidental error messages
    :param insert_stmt: the INSERT command
    :param insert_vals: the values to be inserted
    :param logger: optional logger
    :return: the number of inserted tuples (0 ou 1), or None if an error occurred
    """
    result: int | None = None
    match DB_ENGINE:
        case "oracle":
            result = oracle_pomes.db_modify(errors, insert_stmt, insert_vals, logger)
        case "postgres":
            result = postgres_pomes.db_modify(errors, insert_stmt, insert_vals, logger)
        case "sqlserver":
            result = sqlserver_pomes.db_modify(errors, insert_stmt, insert_vals, logger)

    return result


def db_update(errors: list[str] | None,
              update_stmt: str,
              update_vals: tuple,
              where_vals: tuple,
              logger: Logger = None) -> int:
    """
    Update one or more tuples in the database, as defined by the command *update_stmt*.

    The values for this update are in *update_vals*.
    The values for selecting the tuples to be updated are in *where_vals*.

    :param errors: incidental error messages
    :param update_stmt: the UPDATE command
    :param update_vals: the values for the update operation
    :param where_vals: the values to be associated with the search criteria
    :param logger: optional logger
    :return: the number of updated tuples, or None if an error occurred
    """
    result: int | None = None
    values: tuple = update_vals + where_vals
    match DB_ENGINE:
        case "oracle":
            result = oracle_pomes.db_modify(errors, update_stmt, values, logger)
        case "postgres":
            result = postgres_pomes.db_modify(errors, update_stmt, values, logger)
        case "sqlserver":
            result = sqlserver_pomes.db_modify(errors, update_stmt, values, logger)

    return result


def db_delete(errors: list[str] | None,
              delete_stmt: str,
              where_vals: tuple,
              logger: Logger = None) -> int:
    """
    Delete one or more tuples in the database, as defined by the *delete_stmt* command.

    The values for selecting the tuples to be deleted are in *where_vals*.

    :param errors: incidental error messages
    :param delete_stmt: the DELETE command
    :param where_vals: the values to be associated with the search criteria
    :param logger: optional logger
    :return: the number of deleted tuples, or None if an error occurred
    """
    result: int | None = None
    match DB_ENGINE:
        case "oracle":
            result = oracle_pomes.db_modify(errors, delete_stmt, where_vals, logger)
        case "postgres":
            result = postgres_pomes.db_modify(errors, delete_stmt, where_vals, logger)
        case "sqlserver":
            result = sqlserver_pomes.db_modify(errors, delete_stmt, where_vals, logger)

    return result


def db_bulk_insert(errors: list[str] | None,
                   insert_stmt: str,
                   insert_vals: list[tuple],
                   logger: Logger = None) -> int:
    """
    Insert the tuples, with values defined in *insert_vals*, into the database.

    :param errors: incidental error messages
    :param insert_stmt: the INSERT command
    :param insert_vals: the list of values to be inserted
    :param logger: optional logger
    :return: the number of inserted tuples, or None if an error occurred
    """
    result: int | None = None
    match DB_ENGINE:
        case "postgres":
            result = postgres_pomes.db_bulk_insert(errors, insert_stmt, insert_vals, logger)
        case "sqlserver":
            result = sqlserver_pomes.db_bulk_insert(errors, insert_stmt, insert_vals, logger)

    return result


def db_call_function(errors: list[str] | None,
                     func_name: str,
                     func_vals: tuple,
                     logger: Logger = None) -> list[tuple]:
    """
    Execute the stored function *func_name* in the database, with the parameters given in *func_vals*.

    :param errors: incidental error messages
    :param func_name: name of the stored function
    :param func_vals: parameters for the stored function
    :param logger: optional logger
    :return: the data returned by the function
    """
    result: Any = None
    match DB_ENGINE:
        case "oracle":
            result = oracle_pomes.db_call_function(errors, func_name, func_vals, logger)
        case "postgres":
            result = postgres_pomes.db_call_procedure(errors, func_name, func_vals, logger)
        case "sqlserver":
            result = sqlserver_pomes.db_call_procedure(errors, func_name, func_vals, logger)

    return result


def db_call_procedure(errors: list[str] | None,
                      proc_name: str,
                      proc_vals: tuple,
                      logger: Logger = None) -> list[tuple]:
    """
    Execute the stored procedure *proc_name* in the database, with the parameters given in *proc_vals*.

    :param errors: incidental error messages
    :param proc_name: name of the stored procedure
    :param proc_vals: parameters for the stored procedure
    :param logger: optional logger
    :return: the data returned by the procedure
    """
    result: Any = None
    match DB_ENGINE:
        case "oracle":
            result = oracle_pomes.db_call_procedure(errors, proc_name, proc_vals, logger)
        case "postgres":
            result = postgres_pomes.db_call_procedure(errors, proc_name, proc_vals, logger)
        case "sqlserver":
            result = sqlserver_pomes.db_call_procedure(errors, proc_name, proc_vals, logger)

    return result
