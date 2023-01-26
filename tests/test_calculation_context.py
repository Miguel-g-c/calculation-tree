from calculation_tree.services.calculation_context import CalculationContext


def test_nodes_iterator():
    with CalculationContext() as ctx:
        var = ctx.variables.create("var", 1)
        ds = ctx.data_sources.create("ds", "", 2020)
        op = ctx.operations.create("op")
        assert set(ctx.nodes) == {var, ds, op}


def test_final_result():
    with CalculationContext() as ctx:
        var1 = ctx.variables.create("var1", 1)
        var2 = ctx.variables.create("var2", 2)
        var3 = var1 + var2
        assert ctx.final_result == var3
