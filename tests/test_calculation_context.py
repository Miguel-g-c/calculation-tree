from calculation_tree.model import DataSource
from calculation_tree.services.calculation_context import CalculationContext


def test_nodes_iterator():
    with CalculationContext() as ctx:
        var1 = ctx.variables.create("var1", 1)
        ef = ctx.emission_factors.get("0904eaa8-c828-4f20-bb7c-cf9d7556feb3")
        ppi = ctx.price_indices.get("35fe5f8b-88bc-46b2-a6cb-f77bbf4f454c")
        assert set(ctx.nodes) == {var1, ef, ppi}


def test_final_result():
    with CalculationContext() as ctx:
        var1 = ctx.variables.create("var1", 1)
        var2 = ctx.variables.create("var2", 2)
        var3 = var1 + var2
        assert ctx.final_result == var3


def test_traverse():
    with CalculationContext() as ctx:
        var1 = ctx.variables.create("var1", 1)
        var2 = ctx.variables.create("var2", 2)
        var3 = var1 + var2
        op = var3.parents[0]
        acc = []
        ctx.traverse(lambda n: acc.append(n))
        assert acc == [var3, op, var1, var2]


def test_render_tree():
    # TODO: implement test and better rendering
    pass


def test_to_dict():
    with CalculationContext() as ctx:
        ds = DataSource("IEA", "", 2020)
        var1 = ctx.variables.create("var1", 1, parents=[ds])
        var3 = -var1
        var2 = ctx.variables.create("var2", 2)
        var4 = var3 + var2
        assert ctx.to_dict() == {
            "id": var4.id,
            "type": "Variable",
            "name": "-var1 + var2",
            "value": 1.0,
            "parents": [
                {
                    "id": var4.parents[0].id,
                    "type": "Operation",
                    "name": "add",
                    "parents": [
                        {
                            "id": var3.id,
                            "type": "Variable",
                            "name": "-var1",
                            "value": -1.0,
                            "parents": [
                                {
                                    "id": var3.parents[0].id,
                                    "type": "Operation",
                                    "name": "neg",
                                    "parents": [
                                        {
                                            "id": var1.id,
                                            "type": "Variable",
                                            "name": "var1",
                                            "value": 1.0,
                                            "parents": [
                                                {
                                                    "id": ds.id,
                                                    "type": "DataSource",
                                                    "name": "IEA",
                                                    "description": "",
                                                    "year": 2020,
                                                    "parents": [],
                                                }
                                            ],
                                        }
                                    ],
                                }
                            ],
                        },
                        {
                            "id": var2.id,
                            "type": "Variable",
                            "name": "var2",
                            "value": 2.0,
                            "parents": [],
                        },
                    ],
                }
            ],
        }
