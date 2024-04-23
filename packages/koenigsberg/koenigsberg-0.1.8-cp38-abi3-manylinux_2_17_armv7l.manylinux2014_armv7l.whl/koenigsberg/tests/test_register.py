from __future__ import annotations

from pathlib import Path

import koenigsberg as kg
import pytest
from pytest import param


@pytest.mark.parametrize(
    ("fname", "in_table_name", "out_table_name"),
    [
        param("functional_alltypes.parquet", "funk_all", "funk_all", id="basename"),
    ],
)
def test_register_parquet(data_dir, fname, in_table_name, out_table_name):
    fname = Path(fname)
    con = kg.con()
    table = con.register(data_dir / "parquet" / fname.name, table_name=in_table_name)

    assert any(out_table_name in t for t in con.list_tables())
    assert table.count() > 0
