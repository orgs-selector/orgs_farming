from os.path import join as get_path;

LOG_FILE = get_path('bot.txt')

CONN_ADRGS = {
    'database' : 'orgs' ,
    'password' : 'orgs' ,
    'user'     : 'orgs' ,
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
     '   crdnts   TEXT[]                              '
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
    '                     crdnts   '    
    ') VALUES                      '
)

INS_IDS_TB = 'INSERT INTO ids_tb (spcl_id) VALUES '

IDS_TB_CR = (
    'CREATE TABLE ids_tb(                           '
     '   id serial primary key, spcl_id VARCHAR(255)'
     ');                                            '
    f'{DBRESP} orgs_tb;                           '
)


MAINCAT_CONST = ['автомойка Москва', 'Автоуслуги Москва', 'Автошколы Москва', 'Аквааэробика Москва', 'Аквапарки Москва', 'Антикафе Москва', 'Ателье Москва', 'Аэробика Москва', 'Аэрография Москва', 'Аэройога Москва', 'Бани на дровах Москва', 'Банкетные залы Москва', 'Баня и сауна Москва', 'Бассейны Москва', 'Больницы Москва', 'Боулинг Москва', 'Бургерные Москва', 'Бытовые услуги Москва', 'Вакцинация Москва', 'Ветаптеки Москва', 'Где сделать пирсинг Москва', 'Гипермаркеты Москва', 'Детские развлекательные центры Москва', 'Детский сад Москва', 'Диспансер Москва', 'Еда и напитки Москва', 'Женская консультация Москва', 'Замена масла Москва', 'Зоопарки Москва', 'Зумба Москва', 'Капсульная эндоскопия Москва', 'Караоке-бары Москва', 'Катки Москва', 'Кафе-кондитерские Москва', 'Книжные магазины Москва', 'Комиссионные магазины Москва', 'Компьютерная томография Москва', 'Компьютерные клубы Москва', 'Кофейни Москва', 'Кроссфит Москва', 'Круглосуточные автосервисы Москва', 'Круглосуточные ветеринарные клиники Москва', 'Круглосуточные ночные клубы Москва', 'Круглосуточные одежда и обувь Москва', 'Круглосуточные рестораны Москва', 'Круглосуточные салоны красоты и спа Москва', 'Круглосуточные торговые центры Москва', 'Круглосуточные фитнес клубы Москва', 'Курсы английского языка Москва', 'Курсы повышения квалификации Москва', 'Магазины нижнего белья Москва', 'Магазины обуви Москва', 'Магазины одежды Москва', 'Магазины пряжи Москва', 'Магазины спортивной одежды Москва', 'Магазины сумок Москва', 'Магазины тканей Москва', 'Магазины цветов Москва', 'Магазины часов Москва', 'Медицина Москва', 'Наращивание ногтей Москва', 'Наращивание ресниц Москва', 'Недорогие фитнес-клубы Москва', 'Ночные клубы с танцами Москва', 'Образование Москва', 'Общественные бани Москва', 'Общий анализ крови Москва', 'Окрашивание волос Москва', 'Отели и дома отдыха Москва', 'Пабы Москва', 'Пекарни Москва', 'Цигун Москва', 'Цирки Москва', 'Чайханы Москва', 'Шашлычные Москва', 'Шугаринг Москва']

API_KEY_SET = [
    'f49ce4e7-2f3f-46ba-b33e-da64cfbe94d7',
    '604bc3ff-6e7a-4400-bf1d-0b5a10ff24b8',
    '0871411f-8076-46ab-aed4-9e24468043a5',
    'bbb8456c-2daa-44b7-af44-5159b2e07cae',
    'e617b2ba-26f0-4733-a9fa-04134b38a2f1',
    '8e3a7ddd-374f-44e7-8bc7-37dd7dc2d568',
    '082ec27b-41d8-441d-ab37-92ab31ef5ae3'
]

RESULT_LIM = 500

SEARCH_URL = 'https://search-maps.yandex.ru/v1/'

