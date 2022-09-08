from os.path import join as get_path;

LOG_FILE = get_path('bot.txt')

CONN_ADRGS = {
    'database' : 'map' ,
    'password' : 'map' ,
    'user'     : 'map' ,
    'host'     : 'localhost',
    'port'     : '5432'     
}

DBRESP = 'SELECT COUNT(1) FROM'

ORGS_TB_CR = (
     'CREATE TABLE orgs_tb(                           '
     '   id serial primary key, spcl_id VARCHAR(255), '
     '   name     VARCHAR(255), discr   VARCHAR(255), '
     '   catg     TEXT[]      , addr    VARCHAR(255), '
     '   phone    TEXT[]      , hours   VARCHAR(255), '
     '   avlb     VARCHAR(255)                        '
     ');                                              '
    f'{DBRESP} orgs_tb;                               '
)

INS_ORGS_TB = (
    'INSERT INTO orgs_tb (spcl_id, '
    '                     name   , '
    '                     discr  , '
    '                     catg   , '
    '                     addr   , '
    '                     phone  , '
    '                     hours  , '
    '                     avlb     '    
    ') VALUES (                    '
)

INS_IDS_TB = 'INSERT INTO ids_tb (spcl_id) VALUES (';

IDS_TB_CR = (
    'CREATE TABLE ids_tb(                           '
     '   id serial primary key, spcl_id VARCHAR(255)'
     ');                                            '
    f'{DBRESP} orgs_tb;                           '
)


MAINCAT_CONST = ...
API_KEY_SET   = ... 
RESULT_LIM    = ... 
SEARCH_URL    = ...
