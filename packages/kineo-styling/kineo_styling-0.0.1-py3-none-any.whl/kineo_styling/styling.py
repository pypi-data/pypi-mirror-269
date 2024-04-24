from plotly.graph_objects import Figure
from typing import Any, Dict
from colors import kineo_colors_full
from functools import wraps


def style_fig_for_presentation(
    fig: Figure,
    update_layout_kwargs: Dict[Any, Any] = {},
    update_traces_kwargs: Dict[Any, Any] = {},
    patch_colors: bool = True,
    dark_mode: bool = False,
):
    """Export an plotly figure as a PNG image

    Args:
        fig (Figure): The plotly figure to export
        update_layout_kwargs (dict, optional): Update layout arguments. Defaults to {}.
        update_traces_kwargs (dict, optional): Update traces arguments. Defaults to {}.
        patch_colors (bool, optional): Whether to use the Kineo color palette. Defaults to True.
        dark_mode (bool, optional): Whether the image will be used in dark mode. Defaults to False.

    Returns:
        Figure: The updated figure
    """

    if dark_mode:
        gridcolor = "#C3C3C3"
        font_color = "white"
    else:
        gridcolor = "#434343"
        font_color = "black"

    _update_layout_kwargs = dict(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font_color=font_color,
        title=None,
    )
    _update_layout_kwargs.update(update_layout_kwargs)
    fig.update_layout(**_update_layout_kwargs)

    new_color_mapping = {}
    rows, cols = fig._get_subplot_rows_columns()
    for r in rows:
        for c in cols:
            fig.update_xaxes(
                showgrid=True,
                gridwidth=1,
                gridcolor=gridcolor,
                row=r,
                col=c,
            )
            fig.update_yaxes(
                showgrid=True,
                gridwidth=1,
                gridcolor=gridcolor,
                row=r,
                col=c,
            )

    if patch_colors:
        # update colors seen
        for trace_data in fig.data:
            current_color = trace_data.marker.color
            if current_color and current_color not in new_color_mapping:
                new_color_mapping[current_color] = kineo_colors_full[
                    len(new_color_mapping) % len(kineo_colors_full)
                ]
            if hasattr(trace_data, "line") and trace_data.line:
                current_color = trace_data.line.color
                if current_color and current_color not in new_color_mapping:
                    new_color_mapping[current_color] = kineo_colors_full[
                        len(new_color_mapping) % len(kineo_colors_full)
                    ]

    # update colors
    for old, new in new_color_mapping.items():
        fig.update_traces(marker_color=new, selector=dict(marker_color=old))
        fig.update_traces(line_color=new, selector=dict(line_color=old))

    # remove annotations
    fig.layout.annotations = ()
    fig.update_traces(**update_traces_kwargs)
    return fig


def patch_to_light_mode(view_func):
    @wraps(view_func)
    def _wrapped_view(*args, **kwargs):
        fig = view_func(*args, **kwargs)
        if fig is None:
            return None
        if not isinstance(fig, Figure):
            raise ValueError(
                "This decorator only works on functions that return a Figure object"
            )
        fig = style_fig_for_presentation(fig, dark_mode=False)
        return fig

    return _wrapped_view


def patch_to_dark_mode(view_func):
    @wraps(view_func)
    def _wrapped_view(*args, **kwargs):
        fig = view_func(*args, **kwargs)
        if fig is None:
            return None
        if not isinstance(fig, Figure):
            raise ValueError(
                "This decorator only works on functions that return a Figure object"
            )
        fig = style_fig_for_presentation(fig, dark_mode=True)
        return fig

    return _wrapped_view
