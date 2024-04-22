import pytest

from nlp_tir import datasets


@pytest.fixture
def mock_datasets_folder(monkeypatch):
    monkeypatch.setattr(datasets, "datasets_dir", "/tmp")


def test_get_dataset_reuter_50_50(mock_datasets_folder):
    r50_50 = datasets.get_dataset_reuter_50_50()
    df_train, df_test = r50_50["train"], r50_50["test"]

    assert len(df_train) == 2500
    assert len(df_test) == 2500
