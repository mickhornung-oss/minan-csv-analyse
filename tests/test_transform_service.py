"""Tests fuer den Transform-Service."""

from minan_v1.domain.models import FilterCondition, FilterOperator, SortState
from minan_v1.services.transform_service import (
    apply_filter,
    apply_filters,
    apply_sort,
    drop_column,
    focus_duplicate_rows,
    focus_missing_rows,
    focus_outlier_candidates,
    mark_duplicates,
    mark_missing,
    rename_column,
)


class TestTransformService:
    """Testklasse fuer Daten-Transformationen auf der Arbeitskopie."""

    def test_rename_column_success(self, sample_df):
        result = rename_column(sample_df.copy(), "Name", "NeuerName")
        assert result.success is True
        assert "NeuerName" in result.df.columns
        assert "Name" not in result.df.columns
        assert "Name" in sample_df.columns

    def test_rename_column_not_exists(self, sample_df):
        result = rename_column(sample_df.copy(), "NichtVorhanden", "NeuerName")
        assert result.success is False
        assert "nicht gefunden" in result.message.lower()

    def test_rename_column_already_exists(self, sample_df):
        result = rename_column(sample_df.copy(), "Name", "Alter")
        assert result.success is False
        assert "existiert bereits" in result.message.lower()

    def test_drop_column_success(self, sample_df):
        result = drop_column(sample_df.copy(), "Name")
        assert result.success is True
        assert "Name" not in result.df.columns
        assert "Name" in sample_df.columns

    def test_drop_column_not_exists(self, sample_df):
        result = drop_column(sample_df.copy(), "NichtVorhanden")
        assert result.success is False
        assert "nicht gefunden" in result.message.lower()

    def test_filter_equal(self, sample_df):
        condition = FilterCondition(column="Alter", operator=FilterOperator.EQUAL, value="30")
        result = apply_filter(sample_df, condition)
        assert result.success is True
        assert len(result.df) == 1

    def test_filter_greater_than(self, sample_df):
        condition = FilterCondition(column="Alter", operator=FilterOperator.GREATER_THAN, value="30")
        result = apply_filter(sample_df, condition)
        assert result.success is True
        assert len(result.df) == 2

    def test_filter_between(self, sample_df):
        condition = FilterCondition(
            column="Alter",
            operator=FilterOperator.BETWEEN,
            value="30",
            value2="40",
        )
        result = apply_filter(sample_df, condition)
        assert result.success is True
        assert len(result.df) == 2

    def test_filter_contains(self, sample_df):
        condition = FilterCondition(column="Stadt", operator=FilterOperator.CONTAINS, value="er")
        result = apply_filter(sample_df, condition)
        assert result.success is True
        assert len(result.df) == 3

    def test_filter_is_empty(self, sample_df):
        condition = FilterCondition(column="Name", operator=FilterOperator.IS_EMPTY)
        result = apply_filter(sample_df, condition)
        assert result.success is True
        assert len(result.df) == 1

    def test_filter_not_empty(self, sample_df):
        condition = FilterCondition(column="Name", operator=FilterOperator.IS_NOT_EMPTY)
        result = apply_filter(sample_df, condition)
        assert result.success is True
        assert len(result.df) == 4

    def test_filter_column_not_exists(self, sample_df):
        condition = FilterCondition(column="NichtVorhanden", operator=FilterOperator.EQUAL, value="Test")
        result = apply_filter(sample_df, condition)
        assert result.success is False
        assert "nicht gefunden" in result.message.lower()

    def test_apply_multiple_filters(self, sample_df):
        conditions = [
            FilterCondition(column="Stadt", operator=FilterOperator.EQUAL, value="Berlin"),
            FilterCondition(column="Alter", operator=FilterOperator.GREATER_THAN, value="30"),
        ]
        result = apply_filters(sample_df, conditions)
        assert result.success is True
        assert result.row_count == 2
        assert set(result.df["Name"].tolist()) == {"Charlie", "Eve"}

    def test_sort_ascending(self, sample_df):
        result = apply_sort(sample_df.copy(), SortState(column="Alter", ascending=True))
        assert result.success is True
        assert result.df["Alter"].tolist() == sorted(sample_df["Alter"].tolist())

    def test_sort_descending(self, sample_df):
        result = apply_sort(sample_df.copy(), SortState(column="Alter", ascending=False))
        assert result.success is True
        assert result.df["Alter"].tolist() == sorted(sample_df["Alter"].tolist(), reverse=True)

    def test_sort_column_not_exists(self, sample_df):
        result = apply_sort(sample_df.copy(), SortState(column="NichtVorhanden", ascending=True))
        assert result.success is False
        assert "nicht gefunden" in result.message.lower()

    def test_mark_duplicates(self, df_with_duplicates):
        result = mark_duplicates(df_with_duplicates)
        assert len(result.marked_rows) == 4
        assert "dubletten" in result.message.lower()

    def test_mark_missing(self, sample_df):
        result = mark_missing(sample_df)
        assert len(result.marked_columns) == 2
        assert len(result.marked_cells) == 2
        assert "fehlende" in result.message.lower()

    def test_focus_missing_rows(self, sample_df):
        result = focus_missing_rows(sample_df)
        assert result.success is True
        assert result.row_count == 1
        assert result.df.iloc[0]["ID"] == 4

    def test_focus_duplicate_rows(self, df_with_duplicates):
        result = focus_duplicate_rows(df_with_duplicates)
        assert result.success is True
        assert result.row_count == 4

    def test_focus_outlier_candidates(self, df_with_outliers):
        result = focus_outlier_candidates(df_with_outliers)
        assert result.success is True
        assert result.row_count == 1
        assert result.df.iloc[0]["Wert"] == 200
