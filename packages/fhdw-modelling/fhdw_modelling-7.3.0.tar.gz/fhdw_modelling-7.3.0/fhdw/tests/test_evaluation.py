"""Test evaluation resources."""

import pandas as pd

from fhdw.modelling.evaluation import get_regression_metrics
from fhdw.modelling.evaluation import plot_estimates
from fhdw.modelling.evaluation import plot_estimates_multiple_models
from fhdw.modelling.evaluation import plot_identity
from fhdw.modelling.evaluation import plot_identity_multiple_models
from fhdw.modelling.evaluation import plot_residuals
from fhdw.modelling.evaluation import plot_train_test_target_distribution


def test_get_regression_metrics_positive():
    """Test regression metrics calculation for positive values."""
    y_true = pd.Series([1, 2, 3, 4, 5])
    y_pred = pd.Series([1.1, 2.2, 2.9, 4.2, 5.1])

    metrics = get_regression_metrics(y_true=y_true, y_pred=y_pred)

    assert len(metrics) == 5
    assert metrics["RMSLE"] is not None


def test_get_regression_metrics_negative():
    """Test regression metrics calculation with negative values."""
    y_true = pd.Series([1, 2, 3, 4, 5])
    y_pred = pd.Series([1.1, -2.2, 2.9, 4.2, 5.1])

    metrics = get_regression_metrics(y_true=y_true, y_pred=y_pred)

    assert len(metrics) == 5
    assert metrics["RMSLE"] is None

    y_true = pd.Series([1, 2, -3, 4, 5])
    y_pred = pd.Series([1.1, 2.2, 2.9, 4.2, 5.1])

    metrics = get_regression_metrics(y_true=y_true, y_pred=y_pred)

    assert len(metrics) == 5
    assert metrics["RMSLE"] is None

    y_true = pd.Series([-1, 2, 3, 4, 5])
    y_pred = pd.Series([1.1, -2.2, 2.9, 4.2, 5.1])

    metrics = get_regression_metrics(y_true=y_true, y_pred=y_pred)

    assert len(metrics) == 5
    assert metrics["RMSLE"] is None


def test_plot_estimates_single_model_variant():
    """Test vs-plot properties after generating the plot."""
    # Mock data for testing
    y_true = pd.Series([1, 2, 3, 4, 5])
    y_pred = pd.Series([1.1, 2.2, 2.8, 3.7, 4.9])
    title = "Test Target"

    # generate the plot
    figure = plot_estimates(y_true, y_pred, title)

    figure_dict = figure.to_dict()
    assert figure_dict["layout"]["title"]["text"] == title
    assert figure_dict["layout"]["xaxis"]["title"]["text"] == "index"
    assert figure_dict["layout"]["yaxis"]["title"]["text"] == title

    # Check if the data in the plot matches the input data
    assert figure.data[0].x.tolist() == list(range(len(y_true)))  # type: ignore
    assert figure.data[0].y.tolist() == y_pred.tolist()  # type: ignore
    assert figure.data[2].y.tolist() == y_true.tolist()  # type: ignore
    assert len(figure.data) == 4  # type: ignore


def test_plot_estimates_multiple_models_variant():
    """Test estimate plot in the multiple model variant."""
    # Mock data for testing
    y_true = pd.Series([1, 2, 3, 4, 5])
    model1 = pd.Series([1.1, 2.2, 2.8, 3.7, 4.9])
    model2 = pd.Series([1, 3, 4, 2.0, 6])
    title = "Test Target"

    data = pd.DataFrame({"y_true": y_true, "model1": model1, "model2": model2})

    # generate the plot
    figure = plot_estimates_multiple_models(data, title)

    figure_dict = figure.to_dict()
    assert figure_dict["layout"]["title"]["text"] == title
    assert len(figure.data) == 6  # type: ignore


def test_plot_identity_single_model_variant():
    """Test identity-plot properties after generating the plot."""
    y_true = pd.Series([1, 2, 3, 4, 5])
    y_pred = pd.Series([1.1, 2.2, 2.9, 4.2, 5.1])
    title = "Test Plot"

    figure = plot_identity(y_true, y_pred, title)

    figure_dict = figure.to_dict()
    assert figure_dict["layout"]["title"]["text"] == title
    assert figure_dict["layout"]["xaxis"]["title"]["text"] == "ground truth"
    assert figure_dict["layout"]["yaxis"]["title"]["text"] == "prediction"
    assert len(figure_dict["layout"]["shapes"]) == 1
    assert figure_dict["layout"]["shapes"][0]["type"] == "line"


def test_plot_identity_multiple_models_variant():
    """Test estimate plot in the multiple model variant."""
    # Mock data for testing
    y_true = pd.Series([1, 2, 3, 4, 5])
    model1 = pd.Series([1.1, 2.2, 2.8, 3.7, 4.9])
    model2 = pd.Series([1, 3, 4, 2.0, 6])
    title = "Test Target"

    data = pd.DataFrame({"y_true": y_true, "model1": model1, "model2": model2})

    # generate the plot
    figure = plot_identity_multiple_models(data, title)

    figure_dict = figure.to_dict()
    assert figure_dict["layout"]["title"]["text"] == title
    assert len(figure.data) == 4  # type: ignore


# Test with sample data
def test_plot_with_sample_data():
    """Test basic functionality distribution plot."""
    y_train = pd.Series([1, 2, 2, 3])
    y_test = pd.Series([2, 3, 4])
    target = "example_target"

    fig = plot_train_test_target_distribution(target, y_train, y_test)

    # Assert expected plot properties
    expected_title = "Train vs. Test Distribution for target 'example_target'."
    assert fig.layout.title.text == expected_title

    # Data for train and test per trace (dist + box = 4)
    assert len(fig.data) == 4  # type: ignore


def test_plot_residuals_basic():
    """Test basic functionality of residual plot."""
    y_train = pd.Series([1, 2, 3])
    pred_train = pd.Series([4, 5, 6])
    y_test = pd.Series([7, 8, 9])
    pred_test = pd.Series([10, 11, 12])
    title = "Residual Plot"
    fig = plot_residuals(y_train, pred_train, y_test, pred_test, title)
    assert fig.layout.title.text == title
    assert len(fig.data) == 6  # type: ignore
