from calculation_tree.model import DataSource


def test_data_source_print():
    data_source = DataSource("data_source", "", 2020)
    assert str(data_source) == "data_source (2020)"
