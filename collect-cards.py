import sqlite3
import pathlib
import json
import os

import qrcode
from barcode import EAN13, Code39
from barcode.writer import ImageWriter

ROOT_DIR = pathlib.Path(__file__).parent

db = sqlite3.connect(ROOT_DIR / 'sync_db')
res = db.execute('SELECT id,content FROM synced_resources WHERE collection GLOB "/users/*/loyalty-cards/"').fetchall()

os.makedirs(ROOT_DIR / 'cards', exist_ok=True)
for (id,data) in res:

    os.makedirs(ROOT_DIR / 'cards' / id)
    with open(ROOT_DIR / 'cards' / id / 'data.json', 'wb') as f:
        f.write(data)

    data = json.loads(data.decode())
    provider_id = data['input_provider_reference']['identifier']
    provider_logo = db.execute(f'SELECT content FROM synced_resources WHERE collection = "{provider_id}/" AND id = "logo"').fetchone()[0]
    with open(ROOT_DIR / 'cards' / id / 'logo.png', 'wb') as f:
        f.write(provider_logo)

    code_format = data['input_barcode_format']
    if code_format == 'EAN_13':
        code = EAN13(data['input_id'])
        code.writer = ImageWriter()
        code.save(ROOT_DIR / 'cards' / id / 'barcode')
    elif code_format == 'CODE_39':
        code = Code39(data['input_id'])
        code.writer = ImageWriter()
        code.save(ROOT_DIR / 'cards' / id / 'barcode')
    elif code_format == 'QR_CODE':
        qrcode.make(data['input_id']).save(ROOT_DIR / 'cards' / id / 'barcode.png')

db.close()