#/==================================================================\#
# database.py                                          (c) Mtvy, 2022 #
#\==================================================================/#
#                                                                    #
# Copyright (c) 2022. Mtvy (Matvei Prudnikov, m.d.prudnik@gmail.com) #
#                                                                    #
#\==================================================================/#

#/-----------------------------/ Libs \-----------------------------\#
from utility import logging, Any, Callable, List, Tuple

from vars import CONN_ADRGS, IDS_TB_CR, INS_ORGS_TB, DBRESP, ORGS_TB_CR, INS_IDS_TB
#\------------------------------------------------------------------/#


#\------------------------------------------------------------------/#
TEST_INSERT = (
    f'   {INS_ORGS_TB}                                     '
    f'   {8888                                           }  , '
    f' \'{"Grace SPA"                                    }\', '
    f' \'{"Онежская ул., 9/4кА, Москва, Россия"          }\', '
    f' ARRAY {["Зоомагазин", "Ветеринарная аптека"]      }  , '
    f' \'{"Россия, Москва, Онежская улица, 9/4кА"        }\', '
    f' ARRAY {["8 (800) 511-04-30", "+7 (929) 527-29-84"]}  , '
    f' \'{"ежедневно, 09:00–22:00"                       }\', '
    f' \'{"09:00:00 to 22:00:00 Everyday True"           }\'  '
     ');                                                      '
    f'{DBRESP} orgs_tb;                                     '
)
#\------------------------------------------------------------------/#


#\------------------------------------------------------------------/#
from psycopg2 import connect as connect_db

@logging()
def __connect() -> Tuple[Any, Any]:
    """This definition returns connection to database."""
    con = connect_db(**CONN_ADRGS); return con, con.cursor()
#\------------------------------------------------------------------/#


#\------------------------------------------------------------------/#
@logging()
def __push_msg(msg : str) -> Any | bool:
    """This definition sends message to database."""
    con, cur = __connect()

    if con and cur:
        cur.execute(msg); con.commit()
        return cur.fetchall()

    return False
#\------------------------------------------------------------------/#


#\------------------------------------------------------------------/#
def get_db(_tb : str) -> str | bool:
    return __push_msg(f'SELECT * FROM {_tb};')
#\------------------------------------------------------------------/#


#\------------------------------------------------------------------/#
def insert_db(msg : str) -> str | bool:
    return __push_msg(f'{msg};')
#\------------------------------------------------------------------/#


#\------------------------------------------------------------------/#
def delete_db(_tb : str, msg : str) -> str | bool:
    return __push_msg(f'DELETE FROM {_tb} WHERE {msg}; {DBRESP} orgs_tb;')
#\------------------------------------------------------------------/#


#\------------------------------------------------------------------/#
@logging()
def __test_database(_write : Callable[[str], None], _tb : str, _tst : str, **_) -> None:

    __push_msg(ORGS_TB_CR)

    test = bool(insert_db(TEST_INSERT))
    _write(f'[DB_INSERT] [{test}] <- insert_db({TEST_INSERT})\n\n')

    test = bool(get_db(_tb))
    _write(f'[DB_GET]    [{test}] <- get_db({_tb})\n\n')

    test = bool(delete_db(_tb, _tst))
    _write(f'[DB_DELETE] [{test}]   <- delete_db({_tb}, {_tst})\n\n')
#\------------------------------------------------------------------/#


#\------------------------------------------------------------------/#
@logging()
def __dump_tables(_write : Callable[[str], None], _tb : str, _fl : str, **_) -> None:
    from json import dump as _dump
    _dump(get_db(_tb), open(_fl, 'w')); _write(f'[DUMP][True]\n')
#\------------------------------------------------------------------/#    


#\------------------------------------------------------------------/#
@logging()
def __load_tables(_write : Callable[[str], None], _tb : str, _fl : str, **_) -> None:

    from json import load as _load
    orgs : List[List[str | Any]] = _load(open(_fl))

    from progress.bar import IncrementalBar as _Bar
    bar = _Bar('Loading', max=len(orgs))

    for org in orgs: 
        bar.next(); brt = "'"

        txt = f" {INS_ORGS_TB} '{org[1]}'     , " \
              f"'{org[2].replace(brt, brt*2)}', " \
              f"'{org[3].replace(brt, brt*2)}', ARRAY {org[4]}, " \
              f"'{org[5].replace(brt, brt*2)}', ARRAY {org[6]}, " \
              f"'{org[7]}', '{org[8]}'); {DBRESP} {_tb};        "
              
        if not insert_db(txt): 
            _write('[LOAD][False]\n'); return
        
        txt = f'{INS_IDS_TB} \'{org[1]}\'); {DBRESP} {_tb};'

        if not insert_db(txt):
            _write('[LOAD][False]\n'); return
            
    bar.finish(); _write(f'[LOAD][True]')
#\------------------------------------------------------------------/# 


#\------------------------------------------------------------------/# 
def __help_msg(_write : Callable[[str], None], **_) -> None:
    _write(f"-t Database testing\n"
           f"-s Get database tables json\n"
           f"-l Load tables into clear database (json needed)\n"
           f"-c Create database tables\n"
           f"-h Get help message\n"
           f"-f Run organisations farming\n"
           f"-e Fing equal variables\n")
#\------------------------------------------------------------------/# 


#\------------------------------------------------------------------/# 
@logging
def __cr_tables(_write : Callable, _tbs : str, **_) -> None:
    for _tb in _tbs: _write(f'[{_tb.__name__}][{__push_msg(_tb)}]\n')
#\------------------------------------------------------------------/#


#\==================================================================/#
from sys import argv as _dvars

if __name__ == "__main__":

    DB_CNTRL = {
        '-t' : __test_database,
        '-s' : __dump_tables,
        '-l' : __load_tables,
        '-c' : __cr_tables,
        '-h' : __help_msg
    }
    _args = {
        '_write' : print,
        '_tb'    : 'orgs_tb',
        '_tst'   : 'name = \'Grace SPA\'',
        '_fl'    : 'orgs_tb.json',
        '_tbs'   : [ORGS_TB_CR, IDS_TB_CR]
    }
    (DB_CNTRL[_dvar](_args) for _dvar in _dvars if _dvar in DB_CNTRL)
#\==================================================================/#