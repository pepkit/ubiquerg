from ubiquerg import parse_registry_path


def test_parse_reg():
	pvars = parse_registry_path("abc")
	assert(pvars['item'] == 'abc')

	assert(parse_registry_path("http://big.databio.org/bulker/bulker/demo.yaml") == None)

