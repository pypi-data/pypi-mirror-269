import yaml
import csv
from usdm_excel import USDMExcel
from usdm_db import USDMDb
from uuid import UUID

SAVE_ALL = False

def to_int(value):
  try:
    return int(value)
  except:
    return None

def read_error_csv(file):
  reader = csv.DictReader(file)
  items = list(reader)
  for item in items:
    item['row'] = to_int(item['row'])
    item['column'] = to_int(item['column'])
  return items

def run_test(filename, mocker, save=False):
  fake_uuids = (UUID(f'00000000-0000-4000-8000-{i:012}', version=4) for i in range(10000))
  mocker.patch("usdm_db.neo4j_dict.uuid4", side_effect=fake_uuids)
  usdm = USDMDb()
  usdm.from_excel(f"tests/integration_test_files/{filename}.xlsx")
  result = usdm.to_neo4j_dict()

  # Useful if you want to see the results.
  if save or SAVE_ALL:
    with open(f"tests/integration_test_files/{filename}_neo4j_dict.yaml", 'w') as f:
      f.write(yaml.dump(result))
  
  with open(f"tests/integration_test_files/{filename}_neo4j_dict.yaml", 'r') as f:
    expected = yaml.safe_load(f) 
  assert result == expected

def test_simple_1(mocker, globals):
  run_test('simple_1', mocker)

def test_full_1(mocker, globals):
  run_test('full_1', mocker)

def test_full_2(mocker, globals):
  run_test('full_2', mocker)

def test_full_3(mocker, globals):
  run_test('full_3', mocker)
