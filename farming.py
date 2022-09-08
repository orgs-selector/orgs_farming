#/==================================================================\#
# farming.py                                          (c) Mtvy, 2022 #
#\==================================================================/#
#                                                                    #
# Copyright (c) 2022. Mtvy (Matvei Prudnikov, m.d.prudnik@gmail.com) #
#                                                                    #
#\==================================================================/#

#/-----------------------------/ Libs \-----------------------------\#
from traceback    import format_exc
from typing import Any


from utility   import logging, saveLogs, Callable, Dict, List, Literal, Tuple, Set
from vars import IDS_TB_CR, INS_ORGS_TB, DBRESP, ORGS_TB_CR, INS_IDS_TB
from database import get_db, insert_db, push_msg
#\------------------------------------------------------------------/#

CPASS =(0, 500, 1000)

#\------------------------------------------------------------------/#
def __run_farm() -> None:

    from requests import get as _get
    from vars import API_KEY_SET, RESULT_LIM, SEARCH_URL
    
    
    def __req(txt : str) -> Dict | Literal[False] | List:
        try:
            req = _get(txt).json()
        except:
            return []

        return False if 'features' not in req.keys() else req['features']


    def __proc_req(_ids : List[str], txt : str, _pass : Tuple[int]=CPASS) -> None:

        _st = {'added' : False, 'error' : False, 'over' : False}
        
        for skip in _pass:
            data = __req(txt)
                
            if data:
                _ids = __add_items(data, _ids)

            elif len(data) and skip:
                _st['over'] = True; break
           
            if len(data) < 400:
                break
        
        _st['added'] = not (_st['error'] | _st['over'])

        return (_ids, _st)


    def __turn_tuple(_item : Dict[str, str | Any]) -> Tuple:

        prop = _item['properties']; buffer = prop['CompanyMetaData']

        _name, _description, _id = (
            prop[   'name'    ].replace("'", "''"), 
            prop['description'].replace("'", "''"),
            int(buffer['id'])
        )

        _address     = buffer['address'   ].replace("'", "''")
        _categories  = []
        _phones      = ['']
        
        for cat in buffer['Categories']:
            _categories.append(cat['name'])

        _available = _hours = None

        if 'Hours' in buffer.keys():
            if 'text' in buffer['Hours'].keys():
                _hours = buffer['Hours']['text']
            
        if 'Phones' in buffer.keys():
            for phone in buffer['Phones']:
                _phones.append(phone['formatted'])

        del buffer

        return [0, _id         , _name      ,
                   _description, _categories,
                   _address    , _phones    , 
                   _hours      , _available ]


    def __add_items(_its : List, _ids : List) -> List[int]:

        for _it in _its:
            _item = __turn_tuple(_it)
            if _item[1] not in _ids:
                insert_db(
                    f'    {INS_ORGS_TB}    '
                    f'     \'{_item[1]}\'   , '
                    f'     \'{_item[2]}\'   , '
                    f'     \'{_item[3]}\'   , '
                    f' ARRAY {_item[4]}     , '
                    f'     \'{_item[5]}\'   , '
                    f' ARRAY {_item[6]}     , '
                    f'     \'{_item[7]}\'   , '
                    f'     \'{_item[8]}\'     '
                     ');                      '
                    f'{DBRESP} orgs_tb     ;'
                )
                insert_db(
                    f'{INS_IDS_TB} \'{_item[1]}\'); '
                    f'{DBRESP} orgs_tb     ;         '
                )
                _ids.append(int(_item[1]))

        return _ids


    push_msg(ORGS_TB_CR)

    push_msg(IDS_TB_CR)

    tup_ids = get_db('ids_tb')

    ids_set = [int(i[1]) for i in tup_ids]

    cat_added = []

    from vars import MAINCAT_CONST

    for api_key in API_KEY_SET:
        st = {'added' : False, 'error' : False, 'over' : False}
        
        for ctg in MAINCAT_CONST:
            if ctg not in cat_added:
                try:
                    #f'{SEARCH_URL}?text={ctg}&type=biz&lang=ru_RU'
                    #f'&results={result}&skip={skip}&apikey={api}'
                    ids_set, st = __proc_req(ctg, api_key, ids_set)

                    if st['added']:
                        cat_added.append(ctg)
                    if st['over']:
                        break
                except:
                    saveLogs(f'[__run_farm]-->{format_exc()}')
        
            st = {'added' : False, 'error' : False, 'over' : False}
#\------------------------------------------------------------------/#         


#\------------------------------------------------------------------/#
def __is_eq(_write : Callable[[str], None], _tb='orgs_tb', _ks='ids_tb') -> None:


    def __walk(data : List, keys : Set, tb) -> bool:
        for it in data:
            if it[1] not in keys:
                keys += it[1]
            else:
                _write(f'[{tb}][EQ!] [{it[1]}]\n\n')
    

    data = get_db(_tb); __walk(data, set(), _tb)
    
    data = get_db(_ks); __walk(data, set(), _ks)
    
    print(f'[EQ][END]\n')
#\------------------------------------------------------------------/#
       

#\------------------------------------------------------------------/#
def __help_msg(_write : Callable[[str], None], **_) -> None:
    _write("'-h' Get help message         \n"
           "'-f' Run organisations farming\n"
           "'-e' Fing equal variables     \n")
#\------------------------------------------------------------------/#


#\==================================================================/#
from sys import argv as _dvars

if __name__ == "__main__":

    DB_CNTRL = {
        '-h' : __help_msg,
        '-f' : __run_farm,
        '-e' : __is_eq
    }

    _args = {
        '_write' : print,
        '_tb'    : 'orgs_tb',
        '_tst'   : 'name = \'Grace SPA\'',
        '_fl'    : 'orgs_tb.json',
        '_tbs'   : [ORGS_TB_CR, IDS_TB_CR]
    }

    for _dvar in _dvars: 
        if _dvar in DB_CNTRL: 
            DB_CNTRL[_dvar](**_args)
#\==================================================================/#