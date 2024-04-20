
from yattag import Doc
from usdm_model.eligibility_criterion import EligibilityCriterion
from usdm_model.narrative_content import NarrativeContent
from usdm_db.document.document import Document
from tests.test_factory import Factory

def create_criteria(factory):
  INCLUSION = factory.cdisc_code('C25532', 'Inc')
  EXCLUSION = factory.cdisc_code('C25370', 'Exc')
  item_list = [
    {'name': 'IE1', 'label': '', 'description': '', 'text': 'Only perform at baseline', 
     'dictionaryId': None, 'category': INCLUSION, 'identifier': '01', 'nextId': None, 'previousId': None, 'contextId': None
    },
    {'name': 'IE2', 'label': '', 'description': '', 'text': '<p>Only perform on males</p>', 
    'dictionaryId': None, 'category': INCLUSION, 'identifier': '02', 'nextId': None, 'previousId': None, 'contextId': None
    },
  ]
  results = factory.set(EligibilityCriterion, item_list)
  return results

def test_create(mocker, globals, minimal, factory):
  minimal.population.criteria = create_criteria(factory)
  doc = Doc()
  document = Document("xxx", minimal.study, globals.errors_and_logging)
  content = factory.item(NarrativeContent, {'name': "C1", 'sectionNumber': '1.1.1', 'sectionTitle': 'Section Title', 'text': '<usdm:macro id="section" name="inclusion"/>', 'childIds': []})
  document._content_to_html(content, doc)
  result = doc.getvalue()
  expected = '<div class=""><h3 id="section-1.1.1">1.1.1 Section Title</h3><usdm:macro id="section" name="inclusion"></usdm:macro></div>'
  assert result == expected
