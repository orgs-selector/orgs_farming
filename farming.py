#/==================================================================\#
# farming.py                                          (c) Mtvy, 2022 #
#\==================================================================/#
#                                                                    #
# Copyright (c) 2022. Mtvy (Matvei Prudnikov, m.d.prudnik@gmail.com) #
#                                                                    #
#\==================================================================/#

#/-----------------------------/ Libs \-----------------------------\#
from typing       import Dict, List, Literal, Tuple
from traceback    import format_exc
from sys          import argv as _dvars

from utility   import c_logging, saveLogs
#\------------------------------------------------------------------/#


def __run_farm() -> None:

    from requests  import get as _get
    from variables import API_KEY_SET, RESULT_LIM , SEARCH_URL
    
    def __req(txt     : str, 
              res     : int, 
              skip    : int, 
              api_key : str) -> Dict | Literal[False] | List:
        try:
            req = _get(
                f'{SEARCH_URL}?text={txt}&type=biz&lang=ru_RU'
                f'&results={res}&skip={skip}&apikey={api_key}'
            ).json()
        except:
            return []

        return False if 'features' not in req.keys() else req['features']

    def __proc_req(category : str, 
                   api_key  : str, 
                   _ids     : List[str],
                   passes   : Tuple[int] = (0, 500, 1000), 
                   result   : int = RESULT_LIM):

        _st = {'added' : False, 'error' : False, 'over' : False}
        for skip in passes:
            data = __req(category, result, skip, api_key)

            if data:
                _ids = __add_items(data, _ids)

            elif data == [] and skip == 0:
                _st['over'] = True
                break
           
            if len(data) < 400:
                break
        
        if not _st['error'] and not _st['over']:
            _st['added'] = True

        return (_ids, _st)


    def __turn_tuple(_item : Dict) -> Tuple:

        buffer = _item['properties']['CompanyMetaData']

        _name        = _item['properties'][   'name'    ].replace("'", "''")
        _description = _item['properties']['description'].replace("'", "''")

        _id          = int(buffer['id'])

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
                    f'    {INSERT_ORGS_TB}    '
                    f'     \'{_item[1]}\'   , '
                    f'     \'{_item[2]}\'   , '
                    f'     \'{_item[3]}\'   , '
                    f' ARRAY {_item[4]}     , '
                    f'     \'{_item[5]}\'   , '
                    f' ARRAY {_item[6]}     , '
                    f'     \'{_item[7]}\'   , '
                    f'     \'{_item[8]}\'     '
                     ');                      '
                    f'{COUNT_DB} orgs_tb     ;'
                )
                insert_db(
                    f'{INSERT_IDS_TB} \'{_item[1]}\'); '
                    f'{COUNT_DB} orgs_tb     ;         '
                )
                _ids.append(int(_item[1]))

        return _ids


    __push_msg(ORGS_TB_CREATE)

    __push_msg(IDS_TB_CREATE)

    tup_ids = get_db('ids_tb')

    ids_set = [int(i[1]) for i in tup_ids]

    cat_added = []

    from variables import MAINCAT_CONST

    for api_key in API_KEY_SET:
        st = {'added' : False, 'error' : False, 'over' : False}
        
        for ctg in MAINCAT_CONST:
            if ctg not in cat_added:
                try:
                    ids_set, st = __proc_req(ctg, api_key, ids_set)

                    if st['added']:
                        cat_added.append(ctg)
                    if st['over']:
                        break
                except:
                    saveLogs(f'[__run_farm]-->{format_exc()}')
        
            st = {'added' : False, 'error' : False, 'over' : False}
         

def __is_eq() -> None:
    _f = False
    test = get_db('orgs_tb')

    ids = []

    for i in test:
        if i[1] not in ids:
            ids.append(i[1])
        else:
            saveLogs(f'[] [{i[1]}]\n\n')
            _f = True
    
    _ids = get_db('ids_tb')

    eq_ids = []

    for i in _ids:
        if i[1] not in eq_ids:
            eq_ids.append(i[1])
        else:
            saveLogs(f'[] [{i[1]}]\n\n')
            _f = True
    
    print(f'[EQ][{_f}]\n')
            

def __help_msg():
    print(f"'-t' Database testing\n"
          f"'-s' Get database tables json\n"
          f"'-l' Load tables into clear database (json needed)\n"
          f"'-c' Create database tables\n"
          f"'-h' Get help message\n"
          f"'-f' Run organisations farming\n"
          f"'-e' Fing equal variables\n")

#\------------------------------------------------------------------/#


#\==================================================================/#
if __name__ == "__main__":

    DB_CONTROL_METHODS = {
        '-h' : __help_msg,
        '-f' : __run_farm,
        '-e' : __is_eq
    }

    for _dvar in _dvars:
        if _dvar in DB_CONTROL_METHODS:
            DB_CONTROL_METHODS[_dvar]()
#\==================================================================/#