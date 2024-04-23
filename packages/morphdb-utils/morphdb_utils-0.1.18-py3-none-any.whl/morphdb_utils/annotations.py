import io
import base64
from typing import Literal

import pandas as pd  # type: ignore
import matplotlib.figure  # type: ignore


def _get_html_from_mpl_image(fig: matplotlib.figure.Figure) -> str:
    buf = io.BytesIO()
    fig.savefig(buf, format="png")
    buf.seek(0)
    return (
        f'<img src="data:image/png;base64,{base64.b64encode(buf.read()).decode()}" />'
    )


# TODO: type annotation ommitted because plotly should not be in dependencies of morphdb_utils
def _get_html_from_plotly_image(fig) -> str:
    buf = io.StringIO()
    fig.write_html(
        buf,
        include_plotlyjs="cdn",
        full_html=False,
        config={
            "modeBarButtonsToRemove": [
                "zoom",
                "pan",
                "select",
                "zoomIn",
                "zoomOut",
                "autoScale",
                "resetScale",
                "lasso2d",
            ],
            "displaylogo": False,
        },
    )
    buf.seek(0)
    return buf.getvalue()


def transform(func):
    """decorator for main functions of morph's Python Cell.
    This decorator basically does nothing but indicates that the function perform some tabluar transformation
    and returns pandas DataFrame.
    """

    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        assert isinstance(result, pd.DataFrame)
        return result

    return wrapper


def visualize(library: Literal["matplotlib", "pyplot"]):
    """decorator for main functions of morph's Python Cell.
    This decorator indicates that the function perform some visualization and returns Figure object.
    the Figure object will be converted to HTML string and returned.

    Args:
        library (Literal["matplotlib", "pyplot"]): library used for visualization. either "matplotlib" or "pyplot"
    """

    def decorator(func):
        def wrapper(*args, **kwargs):
            result = func(*args, **kwargs)
            if library == "matplotlib":
                assert isinstance(result, matplotlib.figure.Figure)
                return _get_html_from_mpl_image(result)
            else:
                # TODO: assertion skipeed because plotly should not be in dependencies of morphdb_utils
                # assert isinstance(result, plotly.graph_objs._figure.Figure)
                return _get_html_from_plotly_image(result)

        return wrapper

    return decorator
