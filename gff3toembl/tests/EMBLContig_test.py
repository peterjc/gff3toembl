import unittest
from mock import MagicMock, patch
from gff3toembl.EMBLContig import EMBLContig, EMBLHeader, EMBLFeature, EMBLSequence


class TestEMBLContig(unittest.TestCase):

  def create_blank_bit_of_contig(self):
    contig_mock = MagicMock()
    contig_mock.format.return_value = ""
    return contig_mock

  def test_format(self):
    contig = EMBLContig()
    header_mock = MagicMock()
    feature_mock_1 = MagicMock()
    feature_mock_2 = MagicMock()
    sequence_mock = MagicMock()
    header_mock.format.return_value = "Header\n"
    feature_mock_1.format.return_value = "Feature 1\n"
    feature_mock_1.start = 0
    feature_mock_2.format.return_value = "Feature 2\n"
    feature_mock_2.start = 100
    sequence_mock.format.return_value = "Sequence\n"
    contig.header = header_mock
    contig.features = {1: feature_mock_1, 2: feature_mock_2}
    contig.sequence = sequence_mock
    calculated_string = contig.format()
    expected_string = """\
Header
Feature 1
Feature 2
Sequence
"""
    self.assertEqual(calculated_string, expected_string)

  def test_add_feature(self):
    contig = EMBLContig()
    contig.add_feature(
        sequence_id = 1,
        feature_type = 'tRNA',
        start = 100,
        end = 200,
        strand = '+',
        feature_attributes =  {'some_attribute': 'ABC' }
    )
    self.assertEqual(len(contig.features), 1)

  def test_add_duplicate_feature(self):
    contig = EMBLContig()
    contig.add_feature(
        sequence_id = 1,
        feature_type = 'tRNA',
        start = 100,
        end = 200,
        strand = '+',
        feature_attributes =  {'some_attribute': 'ABC' }
    )
    contig.add_feature(
        sequence_id = 1,
        feature_type = 'tRNA',
        start = 100,
        end = 200,
        strand = '+',
        feature_attributes =  {'some_attribute': 'ABC' }
    )
    self.assertEqual(len(contig.features), 1)

  @patch('gff3toembl.EMBLContig.EMBLFeature')
  def test_add_ignored_feature(self, feature_mock):
    contig = EMBLContig()
    feature_mock.return_value.format.side_effect = lambda: None 
    contig.add_feature(
        sequence_id = 1,
        feature_type = 'tRNA',
        start = 100,
        end = 200,
        strand = '+',
        feature_attributes =  {'some_attribute': 'ABC' }
    )
    self.assertEquals(contig.features, {})

  def test_format_no_features(self):
    contig = EMBLContig()
    contig.header = self.create_blank_bit_of_contig()
    contig.sequence = self.create_blank_bit_of_contig()
    self.assertEquals(contig.format(), '')

  def test_get_sorted_features(self):
    # Must be able to get a list of features sorted by (start, end) irrespective of strand
    contig = EMBLContig()
    feature_1 = MagicMock()
    feature_1.start = 100
    feature_1.end = 200
    feature_2 = MagicMock()
    feature_2.start = 1100
    feature_2.end = 1200

    contig.features = {1: feature_1, 2: feature_2}
    expected_features = [feature_1, feature_2]
    self.assertEquals(contig.sorted_features(), expected_features)

    contig.features = {2: feature_2, 1: feature_1}
    expected_features = [feature_1, feature_2]
    self.assertEquals(contig.sorted_features(), expected_features)

    contig.features = {2: feature_1, 1: feature_2}
    expected_features = [feature_1, feature_2]
    self.assertEquals(contig.sorted_features(), expected_features)

  def test_get_sorted_features_2(self):
    # Must be able to get a list of features sorted by (start, end) irrespective of strand
    contig = EMBLContig()
    feature_1 = MagicMock()
    feature_1.start = 100
    feature_1.end = 2000
    feature_2 = MagicMock()
    feature_2.start = 1100
    feature_2.end = 1200

    contig.features = {1: feature_1, 2: feature_2}
    expected_features = [feature_1, feature_2]
    self.assertEquals(contig.sorted_features(), expected_features)

    contig.features = {2: feature_2, 1: feature_1}
    expected_features = [feature_1, feature_2]
    self.assertEquals(contig.sorted_features(), expected_features)

    contig.features = {2: feature_1, 1: feature_2}
    expected_features = [feature_1, feature_2]
    self.assertEquals(contig.sorted_features(), expected_features)

  def test_get_sorted_features_3(self):
    # Must be able to get a list of features sorted by (start, end) irrespective of strand
    contig = EMBLContig()
    feature_1 = MagicMock()
    feature_1.start = 100
    feature_1.end = 1500
    feature_2 = MagicMock()
    feature_2.start = 1100
    feature_2.end = 2000

    contig.features = {1: feature_1, 2: feature_2}
    expected_features = [feature_1, feature_2]
    self.assertEquals(contig.sorted_features(), expected_features)

    contig.features = {2: feature_2, 1: feature_1}
    expected_features = [feature_1, feature_2]
    self.assertEquals(contig.sorted_features(), expected_features)

    contig.features = {2: feature_1, 1: feature_2}
    expected_features = [feature_1, feature_2]
    self.assertEquals(contig.sorted_features(), expected_features)

  def test_add_sequence(self):
    contig = EMBLContig()
    contig.header = self.create_blank_bit_of_contig()
    contig.features['feature_1'] = self.create_blank_bit_of_contig()
    contig.add_sequence('AAAACCCGGTNN')
    self.assertIsInstance(contig.sequence, EMBLSequence)
    self.assertRaises(ValueError, contig.add_sequence, 'AAAACCCGGTNN')

  def test_format_no_sequence(self):
    contig = EMBLContig()
    contig.header = self.create_blank_bit_of_contig()
    contig.features['feature_1'] = self.create_blank_bit_of_contig()
    self.assertEqual(contig.sequence, None)
    self.assertRaises(ValueError, contig.format)

  def test_add_header(self):
    contig = EMBLContig()
    contig.features['feature_1'] = self.create_blank_bit_of_contig()
    contig.sequence = self.create_blank_bit_of_contig()
    header_details = {
      "authors": "John Doe",
      "classification": "UNC",
      "genome_type": "circular",
      "organism": "My organism",
      "project": "PRJ1234",
      "publication": "Unpublished",
      "sequence_identifier": "**contig123",
      "sequence_length": 8,
      "sequence_name": "chromX",
      "taxon_id": 5678,
      "title": "My title"
    }
    contig.add_header(**header_details)
    self.assertIsInstance(contig.header, EMBLHeader)
    with self.assertRaises(ValueError):
      contig.add_header(**header_details)

  def test_format_no_header(self):
    contig = EMBLContig()
    contig.features['feature_1'] = self.create_blank_bit_of_contig()
    contig.sequence = self.create_blank_bit_of_contig()
    self.assertEqual(contig.header, None)
    self.assertRaises(ValueError, contig.format)

class TestEMBLHeader(unittest.TestCase):

  def test_initialize_header_object(self):
    header = EMBLHeader(
      authors="John Doe",
      classification="UNC",
      genome_type="circular",
      organism="My organism",
      project="PRJ1234",
      publication="Unpublished",
      sequence_identifier="**contig123",
      sequence_length=8,
      sequence_name="chromX",
      taxon_id=5678,
      title="My title"
    )

    self.assertEqual(header.authors, "John Doe")
    self.assertEqual(header.classification, "UNC")
    self.assertEqual(header.genome_type, "circular")
    self.assertEqual(header.organism, "My organism")
    self.assertEqual(header.project, "PRJ1234")
    self.assertEqual(header.publication, "Unpublished")
    self.assertEqual(header.sequence_identifier, "contig123") # Removed non-word characters
    self.assertEqual(header.sequence_length, 8)
    self.assertEqual(header.sequence_name, "chromX")
    self.assertEqual(header.taxon_id, 5678)
    self.assertEqual(header.title, "My title")
    self.assertIsInstance(header.source_feature, EMBLFeature)

  def test_remove_non_word_characters(self):
    header = EMBLHeader()
    test_cases = [
      ('foo', 'foo'),
      ('#foo', 'foo'),
      ('#fo!o', 'foo'),
      ('fo#o', 'foo'),
      ('foo##', 'foo'),
      ("*!#foo", 'foo')
    ]
    for test_string, expected_result in test_cases:
      self.assertEqual(header.remove_non_word_characters(test_string), expected_result)

  def test_format(self):
    header = EMBLHeader()

    header.authors="John Doe"
    header.classification="UNC"
    header.genome_type="circular"
    header.organism="My organism"
    header.project="PRJ1234"
    header.publication="Unpublished"
    header.sequence_identifier="contig123"
    header.sequence_length=1234
    header.sequence_name="chromX"
    header.taxon_id=5678
    header.title="My title"
    source_attributes = {"organism": "My organism", "db_xref": "taxon:5678", "note": "chromX"}
    header.source_feature = EMBLFeature('source', 1, 1234, '+', source_attributes)

    expected_header = """\
ID   XXX; XXX; circular; genomic DNA; STD; UNC; 1234 BP.
XX
AC   XXX;
XX
AC * _contig123
XX
PR   Project:PRJ1234;
XX
DE   XXX;
XX
RN   [1]
RA   John Doe;
RT   "My title";
RL   Unpublished.
XX
FH   Key             Location/Qualifiers
FH
FT   source          1..1234
FT                   /organism="My organism"
FT                   /mol_type="genomic DNA"
FT                   /db_xref="taxon:5678"
FT                   /note="chromX"
"""
    calculated_header = header.format()
    for calculated_line,expected_line in zip(calculated_header.split('\n'), expected_header.split('\n')):
      self.assertEqual(calculated_line, expected_line)
    self.assertEqual(len(calculated_header), len(expected_header))
    
    


  def test_format_long_organism_name(self):
    header = EMBLHeader()

    header.authors="John Doe"
    header.classification="UNC"
    header.genome_type="circular"
    header.organism="reeeeeeeeeeeeeeaaaaaaaaaaaaaallllllllllyyyyyyyyyyyyyyyyyyyy_long_name"
    header.project="PRJ1234"
    header.publication="Unpublished"
    header.sequence_identifier="contig123"
    header.sequence_length=1234
    header.sequence_name="chromX"
    header.taxon_id=5678
    header.title="My title"
    source_attributes = {"organism": header.organism, "db_xref": "taxon:5678", "note": "chromX"}
    header.source_feature = EMBLFeature('source', 1, 1234, '+', source_attributes)

    expected_header = """\
ID   XXX; XXX; circular; genomic DNA; STD; UNC; 1234 BP.
XX
AC   XXX;
XX
AC * _contig123
XX
PR   Project:PRJ1234;
XX
DE   XXX;
XX
RN   [1]
RA   John Doe;
RT   "My title";
RL   Unpublished.
XX
FH   Key             Location/Qualifiers
FH
FT   source          1..1234
FT                   /organism="reeeeeeeeeeeeeeaaaaaaaaaaaaaallllllllllyyyyyyyyy
FT                   yyyyyyyyyyy_long_name"
FT                   /mol_type="genomic DNA"
FT                   /db_xref="taxon:5678"
FT                   /note="chromX"
"""

    calculated_header = header.format()
    for calculated_line,expected_line in zip(calculated_header.split('\n'), expected_header.split('\n')):
      self.assertEqual(calculated_line, expected_line)
    self.assertEqual(len(calculated_header), len(expected_header))
    
    
  def test_format_long_publication(self):
    header = EMBLHeader()

    header.authors="Jagger M., Richards K., Watts C., Wood R., Jones B., Stewart I., Wyman B., Taylor M."
    header.classification="UNC"
    header.genome_type="circular"
    header.organism="organism"
    header.project="PRJ1234"
    header.publication="The Rolling Stones, 12 X 5, The Rolling Stones No. 2, Out of Our Heads, Aftermath, Between the Buttons, Their Satanic Majesties Request, Beggars Banquet"
    header.sequence_identifier="contig123"
    header.sequence_length=1234
    header.sequence_name="chromX"
    header.taxon_id=5678
    header.title="Let It Bleed, Sticky Fingers, Exile on Main St., Goats Head Soup, It's Only Rock 'n Roll, Black and Blue, Some Girls, Emotional Rescue, Tattoo You, Undercover"
    source_attributes = {"organism": header.organism, "db_xref": "taxon:5678", "note": "chromX"}
    header.source_feature = EMBLFeature('source', 1, 1234, '+', source_attributes)

    expected_header = """\
ID   XXX; XXX; circular; genomic DNA; STD; UNC; 1234 BP.
XX
AC   XXX;
XX
AC * _contig123
XX
PR   Project:PRJ1234;
XX
DE   XXX;
XX
RN   [1]
RA   Jagger M., Richards K., Watts C., Wood R., Jones B., Stewart I., Wyman B.,
RA   Taylor M.;
RT   "Let It Bleed, Sticky Fingers, Exile on Main St., Goats Head Soup, It's
RT   Only Rock 'n Roll, Black and Blue, Some Girls, Emotional Rescue, Tattoo
RT   You, Undercover";
RL   The Rolling Stones, 12 X 5, The Rolling Stones No. 2, Out of Our Heads,
RL   Aftermath, Between the Buttons, Their Satanic Majesties Request, Beggars
RL   Banquet.
XX
FH   Key             Location/Qualifiers
FH
FT   source          1..1234
FT                   /organism="organism"
FT                   /mol_type="genomic DNA"
FT                   /db_xref="taxon:5678"
FT                   /note="chromX"
"""

    calculated_header = header.format()
    for calculated_line,expected_line in zip(calculated_header.split('\n'), expected_header.split('\n')):
      self.assertEqual(calculated_line, expected_line)
    self.assertEqual(len(calculated_header), len(expected_header))

  def test_build_source_attributes(self):
    header = EMBLHeader()
    calculated_attributes=header.build_source_attributes(organism="an organism", taxon_id="TAX_ID", sequence_name="sequence_name")
    expected_attributes = {"organism": "an organism", "db_xref": "taxon:TAX_ID", "note": "sequence_name"}
    self.assertEqual(calculated_attributes, expected_attributes)


class TestEMBLFeature(unittest.TestCase):

  def create_uninitialized_feature(self):
    # In most cases I don't want tests to run the __init__
    # This creates an otherwise identical EMBLFeature object
    return EMBLFeature.__new__(EMBLFeature)

  def test_initializer(self):
    feature = EMBLFeature(
        feature_type='tRNA',
        start = 100,
        end = 200,
        strand = '+',
        feature_attributes =  {'some_attribute': 'ABC' }
    )
    self.assertEqual(feature.feature_type, 'tRNA')
    self.assertEqual(feature.start, 100)
    self.assertEqual(feature.end, 200)
    self.assertEqual(feature.strand, '+')
    self.assertEqual(feature.locus_tag, None)
    self.assertEqual(feature.translation_table, 11)

    expected_attributes = [('some_attribute', 'ABC')]
    self.assertItemsEqual(feature.attributes, expected_attributes)

  def test_initializer_for_ignored_features(self):
    feature = EMBLFeature(
        feature_type='ncRNA',
        start = 100,
        end = 200,
        strand = '+',
        feature_attributes =  {'some_attribute': 'ABC' }
    )
    self.assertEqual(feature.format(), None)

  def test_format(self):
    feature = self.create_uninitialized_feature()
    feature.feature_type = "feature_type"
    feature.start = 1
    feature.end = 10
    feature.strand = ''
    feature.attributes = [
      ("attributeA", "foo"),
      ("attributeB", 'bar'),
      ("attributeB", 'baz')
    ]
    calculated_string = feature.format()
    expected_string = """\
FT   feature_type    1..10
FT                   /attributeA="foo"
FT                   /attributeB="bar"
FT                   /attributeB="baz"
"""

    for calculated_line,expected_line in zip(calculated_string.split('\n'), expected_string.split('\n')):
      self.assertEqual(calculated_line, expected_line)
    self.assertEqual(len(calculated_string), len(expected_string))

  def test_pick_feature_builder(self):
    feature = self.create_uninitialized_feature()
    self.assertEqual(feature.pick_feature_builder('CDS'), feature.create_CDS_feature)
    self.assertEqual(feature.pick_feature_builder('source'), feature.create_source_feature)
    self.assertEqual(feature.pick_feature_builder('ncRNA'), feature.create_empty_feature)
    self.assertEqual(feature.pick_feature_builder('other'), feature.create_default_feature)

  def test_create_empty_feature(self):
    feature = self.create_uninitialized_feature()
    feature.create_empty_feature(
        feature_type='ncRNA',
        start = 100,
        end = 200,
        strand = '+',
        feature_attributes =  {'some_attribute': 'ABC' },
        locus_tag = None,
        translation_table = 11
    )
    self.assertEqual(feature.format(), None)

  def test_create_default_feature(self):
    feature = self.create_uninitialized_feature()
    feature.create_default_feature(
        feature_type='tRNA',
        start = 100,
        end = 200,
        strand = '+',
        feature_attributes =  {'some_attribute': 'ABC' },
        locus_tag = None,
        translation_table = 11
    )
    self.assertEqual(feature.feature_type, 'tRNA')
    self.assertEqual(feature.start, 100)
    self.assertEqual(feature.end, 200)
    self.assertEqual(feature.strand, '+')
    self.assertEqual(feature.locus_tag, None)
    self.assertEqual(feature.translation_table, 11)

    expected_attributes = [('some_attribute', 'ABC')]
    self.assertItemsEqual(feature.attributes, expected_attributes)

  def test_create_default_feature_with_locus_tag(self):
    feature = self.create_uninitialized_feature()
    feature.create_default_feature(
        feature_type='tRNA',
        start = 100,
        end = 200,
        strand = '+',
        feature_attributes =  {'some_attribute': 'ABC', 'locus_tag': 'XYZ_123'},
        locus_tag = 'A_LOCUS_TAG',
        translation_table = 11
    )
    self.assertEqual(feature.feature_type, 'tRNA')
    self.assertEqual(feature.start, 100)
    self.assertEqual(feature.end, 200)
    self.assertEqual(feature.strand, '+')
    self.assertEqual(feature.locus_tag, 'A_LOCUS_TAG')
    self.assertEqual(feature.translation_table, 11)

    expected_attributes = [('some_attribute', 'ABC'), ('locus_tag', 'A_LOCUS_TAG_123')]
    self.assertItemsEqual(feature.attributes, expected_attributes)

  def test_create_CDS_feature(self):
    feature = self.create_uninitialized_feature()
    feature.create_CDS_feature(
        feature_type='tRNA',
        start = 100,
        end = 200,
        strand = '+',
        feature_attributes =  {'some_attribute': 'ABC' },
        locus_tag = None,
        translation_table = 11
    )
    self.assertEqual(feature.feature_type, 'tRNA')
    self.assertEqual(feature.start, 100)
    self.assertEqual(feature.end, 200)
    self.assertEqual(feature.strand, '+')
    self.assertEqual(feature.locus_tag, None)
    self.assertEqual(feature.translation_table, 11)

    expected_attributes = [('some_attribute', 'ABC'), ('transl_table', 11)]
    self.assertItemsEqual(feature.attributes, expected_attributes)
    
  def test_create_feature_with_quotes(self):
    feature = self.create_uninitialized_feature()
    feature.create_CDS_feature(
        feature_type='CDS',
        start = 100,
        end = 200,
        strand = '+',
        feature_attributes =  {'gene': '"dnaA"', 'codon_start': '"1"','colour': '"9"', 'locus_tag': '"ABC_001"' },
        locus_tag = None,
        translation_table = 11
    )
    expected_attributes = [('gene', 'dnaA'),('codon_start', 1), ('locus_tag', 'ABC_001'), ('transl_table', 11)]
    self.assertItemsEqual(feature.attributes, expected_attributes)

  def test_create_source_feature(self):
    feature = self.create_uninitialized_feature()
    feature.create_source_feature(
        feature_type='source',
        start = 1,
        end = 1234,
        strand = '+',
        feature_attributes = {"organism": "My organism", "db_xref": "taxon:5678", "note": "chromX"},
        locus_tag = None,
        translation_table = 11
    )
    self.assertEqual(feature.feature_type, 'source')
    self.assertEqual(feature.start, 1)
    self.assertEqual(feature.end, 1234)
    self.assertEqual(feature.strand, '+')
    self.assertEqual(feature.locus_tag, None)
    self.assertEqual(feature.translation_table, 11)

    # Source attributes should have their attributes in this order.  We therefore use assertEqual not assertItemsEqual
    expected_attributes = [("organism", "My organism"), ("mol_type", "genomic DNA"), ("db_xref", "taxon:5678"), ("note", "chromX")]
    self.assertEqual(feature.attributes, expected_attributes)

  def test_format_attribute(self):
    feature = self.create_uninitialized_feature()
    calculated_string = feature.format_attribute('attributeA', 'foo')
    expected_string = 'FT                   /attributeA="foo"'
    self.assertEqual(calculated_string, expected_string)

    calculated_string = feature.format_attribute('transl_table', 11)
    expected_string = 'FT                   /transl_table=11'
    self.assertEqual(calculated_string, expected_string)

  def test_lookup_attribute_formatter(self):
    feature = self.create_uninitialized_feature()
    formatter = feature.lookup_attribute_formatter('attributeA')
    self.assertEqual(formatter, feature.default_attribute_formatter)

    feature = self.create_uninitialized_feature()
    formatter = feature.lookup_attribute_formatter('transl_table')
    self.assertEqual(formatter, feature.number_attribute_formatter)

  def test_number_attribute_formatter(self):
    feature = self.create_uninitialized_feature()
    calculated_string = feature.number_attribute_formatter('transl_table', 11)
    expected_string = 'FT                   /transl_table=11'
    self.assertEqual(calculated_string, expected_string)

  def test_format_multiline_attribute(self):
    feature = self.create_uninitialized_feature()
    long_attribute = 'abc efg hij klm nop qrs tuvw xyz abc efg hij klm nop qrs tuvw xyz'
    calculated_string = feature.format_attribute('product', long_attribute)
    expected_string = """\
FT                   /product="abc efg hij klm nop qrs tuvw xyz abc efg hij klm
FT                   nop qrs tuvw xyz"\
"""
    self.assertEqual(calculated_string, expected_string)

    long_attribute = """\
abc efg hij klm nop qrs tuvw xyz abc efg hij klm nop qrs tuvw xyz \
abc efg hij klm nop qrs tuvw xyz abc_efg hij klm nop qrs tuvw xyz\
"""
    calculated_string = feature.format_attribute('product', long_attribute)
    expected_string = """\
FT                   /product="abc efg hij klm nop qrs tuvw xyz abc efg hij klm
FT                   nop qrs tuvw xyz abc efg hij klm nop qrs tuvw xyz abc_efg
FT                   hij klm nop qrs tuvw xyz"\
"""
    self.assertEqual(calculated_string, expected_string)

  def test_lookup_attribute_creator(self):
    feature = self.create_uninitialized_feature()
    self.assertEqual(feature.lookup_attribute_creator('some_key'),
                     feature.create_default_attributes)
    self.assertEqual(feature.lookup_attribute_creator('product'),
                     feature.create_product_attributes)
    self.assertEqual(feature.lookup_attribute_creator('locus_tag'),
                     feature.create_locus_tag_attributes)
    self.assertEqual(feature.lookup_attribute_creator('eC_number'),
                     feature.create_EC_number_attributes)
    self.assertEqual(feature.lookup_attribute_creator('inference'),
                     feature.create_inference_attributes)
    self.assertEqual(feature.lookup_attribute_creator('protein_id'),
                     feature.ignore_attributes)
    self.assertEqual(feature.lookup_attribute_creator('ID'),
                     feature.ignore_attributes)


  def test_create_product_attributes(self):
    feature = self.create_uninitialized_feature()
    test_cases = [
      ('""', [('product', "Uncharacterised protein")]),
      ('abc,efg,hij', [('product', "abc")]),
      ('hypothetical protein,efg,hij', [('product', "efg")]),
      ('efg,hypothetical protein,hij', [('product', "efg")]),
      ('hypothetical protein,hypothetical protein,hij', [('product', "hij")]),
      ('hypothetical protein', [('product', "Uncharacterised protein")]),
      ('conserved hypothetical protein', [('product', "Uncharacterised protein")]),
      ('hypothetical protein,Unknown protein abc', [('product', "Uncharacterised protein abc")]),
      ('hypothetical protein,unknown protein abc', [('product', "uncharacterised protein abc")]),
      ('Hypothetical protein abc', [('product', "Uncharacterised protein")])
      
    ]
    for test_case, expected_result in test_cases:
      calculated_result = feature.create_product_attributes('product', test_case)
      self.assertEqual(calculated_result, expected_result)

  def test_create_locus_tag_attributes(self):
    feature = self.create_uninitialized_feature()
    feature.locus_tag = None

    calculated_attributes = feature.create_locus_tag_attributes('locus_tag', 'ABC123')
    expected_attributes = [('locus_tag', 'ABC123')]
    self.assertEqual(calculated_attributes, expected_attributes)

    calculated_attributes = feature.create_locus_tag_attributes('locus_tag', 'ABC123_XYZ')
    expected_attributes = [('locus_tag', 'ABC123_XYZ')]
    self.assertEqual(calculated_attributes, expected_attributes)

    calculated_attributes = feature.create_locus_tag_attributes('locus_tag', 'ABC_123_XYZ')
    expected_attributes = [('locus_tag', 'ABC_123_XYZ')]
    self.assertEqual(calculated_attributes, expected_attributes)

    feature.locus_tag = "some_other_tag"

    calculated_attributes = feature.create_locus_tag_attributes('locus_tag', 'ABC123')
    expected_attributes = [('locus_tag', 'some_other_tag_ABC123')]
    self.assertEqual(calculated_attributes, expected_attributes)

    calculated_attributes = feature.create_locus_tag_attributes('locus_tag', 'ABC123_XYZ')
    expected_attributes = [('locus_tag', 'some_other_tag_XYZ')]
    self.assertEqual(calculated_attributes, expected_attributes)

    calculated_attributes = feature.create_locus_tag_attributes('locus_tag', 'ABC_123_XYZ')
    expected_attributes = [('locus_tag', 'some_other_tag_XYZ')]
    self.assertEqual(calculated_attributes, expected_attributes)

  def test_create_EC_number_attributes(self):
    feature = self.create_uninitialized_feature()
    calculated_attributes = feature.create_EC_number_attributes('eC_number', '1.2.3.4')
    expected_attributes = [('EC_number', '1.2.3.4')]
    self.assertEqual(calculated_attributes, expected_attributes)

    calculated_attributes = feature.create_EC_number_attributes('eC_number', '1.2.3.4,1.2.3.-')
    expected_attributes = [('EC_number', '1.2.3.-'), ('EC_number', '1.2.3.4')]
    self.assertEqual(calculated_attributes, expected_attributes)

    calculated_attributes = feature.create_EC_number_attributes('eC_number', '1.2.3.4,1.2.3.4')
    expected_attributes = [('EC_number', '1.2.3.4')]
    self.assertEqual(calculated_attributes, expected_attributes)

    calculated_attributes = feature.create_EC_number_attributes('eC_number', '1.2.3.4,1.2.3.-,1.2.3.4')
    expected_attributes = [('EC_number', '1.2.3.-'), ('EC_number', '1.2.3.4')]
    self.assertEqual(calculated_attributes, expected_attributes)
    
    calculated_attributes = feature.create_EC_number_attributes('eC_number', '2.1.1.-),2.1.1.173')
    expected_attributes = [ ('EC_number', '2.1.1.173')]
    self.assertEqual(calculated_attributes, expected_attributes)
    
    calculated_attributes = feature.create_EC_number_attributes('eC_number', '2.7.7.58%2CIrp5,6.3.2.-')
    expected_attributes = [ ('EC_number', '6.3.2.-')]
    self.assertEqual(calculated_attributes, expected_attributes)
    
    calculated_attributes = feature.create_EC_number_attributes('eC_number', '1.2.3.4,1.2.3.-,1.2.3.-')
    expected_attributes = [('EC_number', '1.2.3.-'), ('EC_number', '1.2.3.4')]
    self.assertEqual(calculated_attributes, expected_attributes)

  def test_create_inference_attributes(self):
    feature = self.create_uninitialized_feature()
    calculated_attributes = feature.create_inference_attributes('inference', '123')
    expected_attributes = [('inference', '123')]
    self.assertEqual(calculated_attributes, expected_attributes)

    calculated_attributes = feature.create_inference_attributes('inference', '123,ABC')
    expected_attributes = [('inference', '123'), ('inference', 'ABC')]
    self.assertEqual(calculated_attributes, expected_attributes)

    calculated_attributes = feature.create_inference_attributes('inference', '123,123')
    expected_attributes = [('inference', '123'), ('inference', '123')]
    self.assertEqual(calculated_attributes, expected_attributes)

    calculated_attributes = feature.create_inference_attributes('inference', '123,ABC,123')
    expected_attributes = [('inference', '123'), ('inference', 'ABC'), ('inference', '123')]
    self.assertEqual(calculated_attributes, expected_attributes)

    calculated_attributes = feature.create_inference_attributes('inference', 'B,A,A')
    expected_attributes = [('inference', 'B'), ('inference', 'A'), ('inference', 'A')]
    self.assertEqual(calculated_attributes, expected_attributes)

    calculated_attributes = feature.create_inference_attributes('inference', 'B,A,B')
    expected_attributes = [('inference', 'B'), ('inference', 'A'), ('inference', 'B')]
    self.assertEqual(calculated_attributes, expected_attributes)

    calculated_attributes = feature.create_inference_attributes('inference', '123,similar to AA sequence:UniProtKB:Q2G282')
    expected_attributes = [('inference', '123'), ('db_xref', "UniProtKB/Swiss-Prot:Q2G282")]
    self.assertEqual(calculated_attributes, expected_attributes)

  def test_ignore_attributes(self):
    feature = self.create_uninitialized_feature()
    calculated_attributes = feature.ignore_attributes('ID', '123')
    expected_attributes = []
    self.assertEqual(calculated_attributes, expected_attributes)

  def test_should_convert_to_db_xref(self):
    feature = self.create_uninitialized_feature()
    self.assertTrue(feature.should_convert_to_db_xref('similar to AA sequence:UniProtKB:Q2G282'))
    self.assertTrue(feature.should_convert_to_db_xref('protein motif:Pfam:PF01475.13'))
    self.assertTrue(feature.should_convert_to_db_xref('protein motif:CLUSTERS:PRK09462'))
    self.assertTrue(feature.should_convert_to_db_xref('protein motif:TIGRFAMs:TIGR01327'))
    self.assertTrue(feature.should_convert_to_db_xref('protein motif:Cdd:COG1932'))
    self.assertTrue(feature.should_convert_to_db_xref('SOME_PREFIX protein motif:Cdd:COG1932'))
    self.assertTrue(feature.should_convert_to_db_xref('protein motif:Cdd:COG1932i SOME_SUFFIX'))
    self.assertTrue(feature.should_convert_to_db_xref('SOME_PREFIX protein motif:Cdd:COG1932i SOME_SUFFIX'))
    self.assertFalse(feature.should_convert_to_db_xref('protein'))
    self.assertFalse(feature.should_convert_to_db_xref('something else'))
    self.assertFalse(feature.should_convert_to_db_xref('motif:Cdd:COG1932i'))

  def test_convert_to_db_xref(self):
    feature = self.create_uninitialized_feature()
    test_cases = [
      ('similar to AA sequence:UniProtKB:Q2G282', "UniProtKB/Swiss-Prot:Q2G282"),
      ('protein motif:Pfam:PF01475.13', "PFAM:PF01475.13"),
      ('protein motif:CLUSTERS:PRK09462', "CDD:PRK09462"),
      ('protein motif:TIGRFAMs:TIGR01327', "TIGRFAM:TIGR01327"),
      ('protein motif:Cdd:COG1932', "CDD:COG1932"),
      ('SOME_PREFIX protein motif:Cdd:COG1932', "SOME_PREFIX CDD:COG1932"),
      ('protein motif:Cdd:COG1932 SOME_SUFFIX', "CDD:COG1932 SOME_SUFFIX"),
      ('SOME_PREFIX protein motif:Cdd:COG1932 SOME_SUFFIX', "SOME_PREFIX CDD:COG1932 SOME_SUFFIX")
    ]
    for test_input, expected_output in test_cases:
      self.assertEqual(feature.convert_to_db_xref(test_input), expected_output)
    for test_input in ['protein', 'something else', 'motif:Cdd:COG1932i']:
      self.assertRaises(ValueError, feature.convert_to_db_xref, test_input)

  def test_create_translation_table_attribute(self):
    feature = self.create_uninitialized_feature()
    calculated_attributes = feature.create_translation_table_attributes('transl_table', '11')
    expected_attributes = [('transl_table', '11')]
    self.assertEqual(calculated_attributes, expected_attributes)

    calculated_attributes = feature.create_translation_table_attributes('transl_table', 'something_else')
    expected_attributes = [('transl_table', 'something_else')]
    self.assertEqual(calculated_attributes, expected_attributes)

  def test_create_default_attributes(self):
    feature = self.create_uninitialized_feature()
    calculated_attributes = feature.create_default_attributes('some_value', 'A')
    expected_attributes = [('some_value', 'A')]
    self.assertEqual(calculated_attributes, expected_attributes)

    calculated_attributes = feature.create_default_attributes('some_value', 'A,B')
    expected_attributes = [('some_value', 'A')]
    self.assertEqual(calculated_attributes, expected_attributes)

    calculated_attributes = feature.create_default_attributes('some_value', 'B,A')
    expected_attributes = [('some_value', 'B')]
    self.assertEqual(calculated_attributes, expected_attributes)

    calculated_attributes = feature.create_default_attributes('some_value', 'A,A')
    expected_attributes = [('some_value', 'A')]
    self.assertEqual(calculated_attributes, expected_attributes)

    calculated_attributes = feature.create_default_attributes('some_value', 'A,A,B')
    expected_attributes = [('some_value', 'A')]
    self.assertEqual(calculated_attributes, expected_attributes)

  def test_format_coordinates(self):
    feature = self.create_uninitialized_feature()
    calculated_coordinates = feature.format_coordinates(1, 10, '')
    expected_coordinates = '1..10'
    self.assertEqual(calculated_coordinates, expected_coordinates)

    calculated_coordinates = feature.format_coordinates(1, 10, '-')
    expected_coordinates = 'complement(1..10)'
    self.assertEqual(calculated_coordinates, expected_coordinates)

    calculated_coordinates = feature.format_coordinates(1, 10, '***NONSENCE***')
    expected_coordinates = '1..10'
    self.assertEqual(calculated_coordinates, expected_coordinates)

  def test_no_wrap_at_length_79(self):
    source_attributes = {"organism": 'abc', "db_xref": "taxon:5678", "note": "chromX"}
    feature = EMBLFeature('source', 1, 1234, '+', source_attributes)

    formatted_product = feature.product_attribute_formatter('product','Anthranilate 1,2-dioxygenase ferredoxin subunit')
    expected_product = 'FT                   /product="Anthranilate 1,2-dioxygenase ferredoxin subunit"'
    assert len(expected_product) == 79
    self.assertEqual(formatted_product, expected_product)

  def test_no_wrap_at_length_80(self):
    source_attributes = {"organism": 'abc', "db_xref": "taxon:5678", "note": "chromX"}
    feature = EMBLFeature('source', 1, 1234, '+', source_attributes)

    formatted_product = feature.product_attribute_formatter('product','1,4-dihydroxy-2-naphthoate octaprenyltransferase')
    expected_product = 'FT                   /product="1,4-dihydroxy-2-naphthoate octaprenyltransferase"'
    assert len(expected_product) == 80
    self.assertEqual(formatted_product, expected_product)

  def test_wrap_with_space_at_80(self):
    source_attributes = {"organism": 'abc', "db_xref": "taxon:5678", "note": "chromX"}
    feature = EMBLFeature('source', 1, 1234, '+', source_attributes)

    formatted_product = feature.product_attribute_formatter('product','Permease for cytosine/purines, uracil, thiamine, allantoin')
    expected_product = 'FT                   /product="Permease for cytosine/purines, uracil, thiamine,\n' + \
                       'FT                   allantoin"'
    self.assertEqual(formatted_product, expected_product)

  def test_split_product_attribute_on_hyphen(self):
    source_attributes = {"organism": 'abc', "db_xref": "taxon:5678", "note": "chromX"}
    feature = EMBLFeature('source', 1, 1234, '+', source_attributes)
    # TODO: This test currently 'passes' but shows the undesirable
    # behaviour of splitting up a long word.
    formatted_product = feature.product_attribute_formatter('product','2-succinyl-6-hydroxy-2,4-cyclohexadiene-1-carboxylate synthase')
    expected_product = 'FT                   /product="2-succinyl-6-hydroxy-2,4-cyclohexadiene-1-carboxy\n' + \
                       'FT                   late synthase"'
    self.assertEqual(formatted_product, expected_product)


class TestEMBLSequence(unittest.TestCase):

  def create_uninitialized_sequence(self):
    # In most cases I don't want tests to run the __init__
    # This creates an otherwise identical EMBLFeature object
    return EMBLSequence.__new__(EMBLSequence)

  def test_init(self):
    sequence = EMBLSequence('AAAACCCGGTNN')
    expected_header = "SQ   Sequence 12 BP; 4 A; 3 C; 2 G; 1 T; 2 other;"
    expected_body = '     aaaacccggt nn                                                            12\n'
    self.assertEqual(sequence.header, expected_header)
    self.assertEqual(sequence.body, expected_body)
    self.assertEqual(sequence.length, 12)

  def test_format(self):
    sequence = self.create_uninitialized_sequence()
    sequence.header = "SQ   Sequence 12 BP; 4 A; 3 C; 2 G; 1 T; 2 other;"
    sequence.body = '     aaaacccggt nn                                                            12\n'
    calculated_string = sequence.format()
    expected_string = """\
SQ   Sequence 12 BP; 4 A; 3 C; 2 G; 1 T; 2 other;
     aaaacccggt nn                                                            12
"""
    self.assertEqual(calculated_string, expected_string)

  def test_calculate_neucleotide_counts(self):
    sequence = self.create_uninitialized_sequence()
    calculated_counts = sequence.calculate_nucleotide_counts('AAAACCCGGTNN')
    expected_counts = {'a': 4, 'c': 3, 'g': 2, 't': 1, 'other': 2}
    self.assertEqual(calculated_counts, expected_counts)

    calculated_counts = sequence.calculate_nucleotide_counts('AAAAaaaaAAAA')
    expected_counts = {'a': 12, 'c': 0, 'g': 0, 't': 0, 'other': 0}
    self.assertEqual(calculated_counts, expected_counts)

    calculated_counts = sequence.calculate_nucleotide_counts('------------')
    expected_counts = {'a': 0, 'c': 0, 'g': 0, 't': 0, 'other': 12}
    self.assertEqual(calculated_counts, expected_counts)

    calculated_counts = sequence.calculate_nucleotide_counts('acgtACGTtttT')
    expected_counts = {'a': 2, 'c': 2, 'g': 2, 't': 6, 'other': 0}
    self.assertEqual(calculated_counts, expected_counts)

  def test_format_header(self):
    sequence = self.create_uninitialized_sequence()
    neucleotide_counts = {'a': 4, 'c': 3, 'g': 2, 't': 1, 'other': 2}
    calculated_header = sequence.format_header(neucleotide_counts)
    expected_header = "SQ   Sequence 12 BP; 4 A; 3 C; 2 G; 1 T; 2 other;"

    neucleotide_counts = {'a': 12, 'c': 0, 'g': 0, 't': 0, 'other': 0}
    calculated_header = sequence.format_header(neucleotide_counts)
    expected_header = "SQ   Sequence 12 BP; 12 A; 0 C; 0 G; 0 T; 0 other;"

    neucleotide_counts = {'a': 0, 'c': 0, 'g': 0, 't': 0, 'other': 12}
    calculated_header = sequence.format_header(neucleotide_counts)
    expected_header = "SQ   Sequence 12 BP; 0 A; 0 C; 0 G; 0 T; 12 other;"

    neucleotide_counts = {'a': 2, 'c': 2, 'g': 2, 't': 6, 'other': 0}
    calculated_header = sequence.format_header(neucleotide_counts)
    expected_header = "SQ   Sequence 12 BP; 2 A; 2 C; 2 G; 6 T; 0 other;"

  def test_split_line_of_sequence(self):
    sequence = self.create_uninitialized_sequence()
    line_of_sequence = "123"
    calculated_split = sequence.split_line_of_sequence(line_of_sequence)
    expected_split = ["123", '', '', '', '', '']
    self.assertEqual(calculated_split, expected_split)

    line_of_sequence = "123456789"
    calculated_split = sequence.split_line_of_sequence(line_of_sequence)
    expected_split = ["123456789", '', '', '', '', '']
    self.assertEqual(calculated_split, expected_split)

    line_of_sequence = "1234567890"
    calculated_split = sequence.split_line_of_sequence(line_of_sequence)
    expected_split = ["1234567890", '', '', '', '', '']
    self.assertEqual(calculated_split, expected_split)

    line_of_sequence = "12345678901"
    calculated_split = sequence.split_line_of_sequence(line_of_sequence)
    expected_split = ["1234567890", "1", '', '', '', '']
    self.assertEqual(calculated_split, expected_split)

    line_of_sequence = "1234567890123"
    calculated_split = sequence.split_line_of_sequence(line_of_sequence)
    expected_split = ["1234567890", "123", '', '', '', '']
    self.assertEqual(calculated_split, expected_split)

    line_of_sequence = "12345678901234567890"
    calculated_split = sequence.split_line_of_sequence(line_of_sequence)
    expected_split = ["1234567890", "1234567890", '', '', '', '']
    self.assertEqual(calculated_split, expected_split)

    line_of_sequence = "1234567890123456789012345"
    calculated_split = sequence.split_line_of_sequence(line_of_sequence)
    expected_split = ["1234567890", "1234567890", "12345", '', '', '']
    self.assertEqual(calculated_split, expected_split)

  def test_split_sequence(self):
    sequence = self.create_uninitialized_sequence()
    sequence_string = "tctgacaatcgctttctt"
    calculated_split = sequence.split_sequence(sequence_string)
    expected_split = [ (['tctgacaatc', 'gctttctt', '', '', '', ''], 18) ]
    self.assertEqual(calculated_split, expected_split)

    sequence_string = "tttaaaaccccgggtttcccgggaaa"
    calculated_split = sequence.split_sequence(sequence_string)
    expected_split = [ (['tttaaaaccc', 'cgggtttccc', 'gggaaa', '', '', ''], 26) ]
    self.assertEqual(calculated_split, expected_split)

    sequence_string = "tctgacaatcgctttctttaaaaagaaactattgtcgagaatttgcattagcaatatcactttgtcaaaaagatgtttgaatgttaaataaacattcaaaactgaatacaatatgtca"
    calculated_split = sequence.split_sequence(sequence_string)
    expected_split = [ (["tctgacaatc", "gctttcttta", "aaaagaaact", "attgtcgaga", "atttgcatta", "gcaatatcac"], 60),
                       (["tttgtcaaaa", "agatgtttga", "atgttaaata", "aacattcaaa", "actgaataca", "atatgtca"],   118) ]
    self.assertEqual(calculated_split, expected_split)

    sequence_string = "tctgacaatcgctttctttaaaaagaaactattgtcgagaatttgcattagcaatatcactttgtcaaaaagatgtttgaatgttaaataaacattcaaaactgaatacaatatgtcac"
    calculated_split = sequence.split_sequence(sequence_string)
    expected_split = [ (["tctgacaatc", "gctttcttta", "aaaagaaact", "attgtcgaga", "atttgcatta", "gcaatatcac"], 60),
                       (["tttgtcaaaa", "agatgtttga", "atgttaaata", "aacattcaaa", "actgaataca", "atatgtcac"],  119) ]
    self.assertEqual(calculated_split, expected_split)

    sequence_string = "tctgacaatcgctttctttaaaaagaaactattgtcgagaatttgcattagcaatatcactttgtcaaaaagatgtttgaatgttaaataaacattcaaaactgaatacaatatgtcaca"
    calculated_split = sequence.split_sequence(sequence_string)
    expected_split = [ (["tctgacaatc", "gctttcttta", "aaaagaaact", "attgtcgaga", "atttgcatta", "gcaatatcac"], 60),
                       (["tttgtcaaaa", "agatgtttga", "atgttaaata", "aacattcaaa", "actgaataca", "atatgtcaca"], 120) ]
    self.assertEqual(calculated_split, expected_split)

  def test_format_sequence_body(self):
    sequence = self.create_uninitialized_sequence()
    sequence_string="tctgacaatcgctttctt"
    expected_string = """\
     tctgacaatc gctttctt                                                      18
"""
    calculated_string = sequence.format_sequence_body(sequence_string)
    self.assertEqual(calculated_string, expected_string)

    sequence_string="TTTAAAACCCCGGGtttcccgggaaa"
    expected_string = """\
     tttaaaaccc cgggtttccc gggaaa                                             26
"""
    calculated_string = sequence.format_sequence_body(sequence_string)
    self.assertEqual(calculated_string, expected_string)

    sequence_string="tctgacaatcgctttctttaaaaagaaactattgtcgagaatttgcattagcaatatcactttgtcaaaaagatgtttgaatgttaaataaacattcaaaactgaatacaatatgtca"
    expected_string = """\
     tctgacaatc gctttcttta aaaagaaact attgtcgaga atttgcatta gcaatatcac        60
     tttgtcaaaa agatgtttga atgttaaata aacattcaaa actgaataca atatgtca         118
"""
    calculated_string = sequence.format_sequence_body(sequence_string)
    self.assertEqual(calculated_string, expected_string)

    sequence_string="tctgacaatcgctttctttaaaaagaaactattgtcgagaatttgcattagcaatatcactttgtcaaaaagatgtttgaatgttaaataaacattcaaaactgaatacaatatgtcac"
    expected_string = """\
     tctgacaatc gctttcttta aaaagaaact attgtcgaga atttgcatta gcaatatcac        60
     tttgtcaaaa agatgtttga atgttaaata aacattcaaa actgaataca atatgtcac        119
"""
    calculated_string = sequence.format_sequence_body(sequence_string)
    self.assertEqual(calculated_string, expected_string)

    sequence_string="tctgacaatcgctttctttaaaaagaaactattgtcgagaatttgcattagcaatatcactttgtcaaaaagatgtttgaatgttaaataaacattcaaaactgaatacaatatgtcaca"
    expected_string = """\
     tctgacaatc gctttcttta aaaagaaact attgtcgaga atttgcatta gcaatatcac        60
     tttgtcaaaa agatgtttga atgttaaata aacattcaaa actgaataca atatgtcaca       120
"""
    calculated_string = sequence.format_sequence_body(sequence_string)
    self.assertEqual(calculated_string, expected_string)
