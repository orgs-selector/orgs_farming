#/==================================================================\#
# farming.py                                          (c) Mtvy, 2022 #
#\==================================================================/#
#                                                                    #
# Copyright (c) 2022. Mtvy (Matvei Prudnikov, m.d.prudnik@gmail.com) #
#                                                                    #
#\==================================================================/#

#/-----------------------------/ Libs \-----------------------------\#
from requests     import get as _get
from typing       import Any, Callable, Dict, List, Literal, Tuple, Set
from sys          import argv as _dvars
from progress.bar import Bar

from utility   import logging, saveLogs 
from database  import get_db, insert_db
from vars      import *
#\------------------------------------------------------------------/#

CPASS = (0, 500, 1000)

#\------------------------------------------------------------------/#
@logging(saveLogs)
def __run_farm(tb='orgs_tb', ks='ids_tb', **_) -> None:
    
    def __req(txt : str) -> Dict | Literal[False] | List:
        try:
            req = _get(txt).json()
        except:
            return []

        return False if 'features' not in req.keys() else req['features']


    def __proc_req(_ids : List[str], txt : str, _tb : str, _ks : str, _pass : Tuple[int]=CPASS) -> Tuple[List[int], Dict[str, bool]]:

        _st = {'added' : False, 'error' : False, 'over' : False}
        
        for skip in _pass:

            data = __req(f'{txt}&skip={skip}')
                
            if data:
                _ids = __add_items(data, _ids, _tb, _ks)

            elif len(data) and skip:
                _st['over'] = True; break
           
            if len(data) < 400:
                break
        
        _st['added'] = not (_st['error'] or _st['over'])

        return (_ids, _st)


    def __turn_tuple(_item : Dict[str, str | Any]) -> Tuple:
        """
        return [0, id, name, description, ctg, addr, phone, hours, crdnts]
        """
        prop = _item['properties']

        _buf : Dict | str = prop['CompanyMetaData']

        return [
            0, int(_buf['id']), prop['name'].replace("'", "''"),

            prop['description'].replace("'", "''"),
            
            [cat['name'] for cat in _buf['Categories']],
            
            _buf[ 'address' ].replace("'", "''"),
            
            [it['formatted'] for it in _buf['Phones']] \
                if 'Phones' in _buf.keys() else [''],

            _buf['Hours']['text'] \
                if 'Hours' in _buf.keys() \
                    and 'text' in _buf['Hours'].keys() else None,
            
            _item['geometry']['coordinates'] 
        ]


    def __add_items(_its : List, _ids : List, _tb : str, _ks : str) -> List[int]:

        txt_tb = ''
        txt_ks = ''

        for _it in _its:

            _item = __turn_tuple(_it)
            
            if _item[1] not in _ids:

                txt_tb += f"('{_item[1]}',      '{_item[2]}'," \
                          f" '{_item[3]}', ARRAY {_item[4]} ," \
                          f" '{_item[5]}', ARRAY {_item[6]} ," \
                          f" '{_item[7]}', ARRAY {_item[8]}),"
                txt_ks += f"('{_item[1]}'),"

                _ids.append(int(_item[1]))
                
        if txt_tb:
            insert_db(f'{INS_ORGS_TB} {txt_tb[:-1]}; {DBRESP} {_tb};')
            insert_db(f'{INS_IDS_TB} {txt_ks[:-1]}; {DBRESP} {_ks};')

        return _ids

    ids_set = [int(i[1]) for i in get_db(ks)]; cat_added = []

    with Bar('Farming', max=len(MAINCAT_CONST)) as bar:
        for api_key in API_KEY_SET:
            
            for ctg in MAINCAT_CONST:
                if ctg not in cat_added:

                    txt = f'{SEARCH_URL}?text={ctg}&type=biz&lang=ru_RU'\
                        f'&results={RESULT_LIM}&apikey={api_key}'

                    ids_set, st = __proc_req(ids_set, txt, tb, ks)

                    if st['added']:
                        cat_added.append(ctg); bar.next()
                    if st['over']:
                        break
            
            if len(cat_added) == len(MAINCAT_CONST):
                break
#\------------------------------------------------------------------/#         


#\------------------------------------------------------------------/#
def __is_eq(_write : Callable[[str], None], _tb='orgs_tb', _ks='ids_tb', **_) -> None:


    def __walk(data : List, keys : Set, tb) -> bool:
        with Bar('Scaning', max=len(data)) as bar:
            for it in data:
                bar.next()
                if it[1] not in keys:
                    keys |= {it[1]}
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