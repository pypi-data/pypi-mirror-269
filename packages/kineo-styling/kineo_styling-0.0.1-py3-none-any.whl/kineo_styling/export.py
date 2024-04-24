from plotly.graph_objects import Figure
from typing import Any, Dict
from kineo_styling.styling import style_fig_for_presentation


def export_figure_as_png(
    fig: Figure,
    output_path: str,
    update_layout_kwargs: Dict[Any, Any] = {},
    update_traces_kwargs: Dict[Any, Any] = {},
    patch_colors: bool = True,
    dark_mode: bool = False,
):
    """Export an plotly figure as a PNG image

    Args:
        fig (Figure): The plotly figure to export
        output_path (str): The path to save the image
        update_layout_kwargs (dict, optional): Update layout arguments. Defaults to {}.
        update_traces_kwargs (dict, optional): Update traces arguments. Defaults to {}.
        patch_colors (bool, optional): Whether to use the Kineo color palette. Defaults to True.
        dark_mode (bool, optional): Whether the image will be used in dark mode. Defaults to False.

    Returns:
        Figure: The updated figure
    """
    fig = style_fig_for_presentation(
        fig=fig,
        update_layout_kwargs=update_layout_kwargs,
        update_traces_kwargs=update_traces_kwargs,
        patch_colors=patch_colors,
        dark_mode=dark_mode,
    )
    fig.write_image(output_path, scale=2)
    return fig


def export_figure_as_png_dark_mode(
    fig: Figure,
    output_path: str,
    update_layout_kwargs: Dict[Any, Any] = {},
    update_traces_kwargs: Dict[Any, Any] = {},
    patch_colors: bool = True,
):
    """Export an plotly figure as a PNG image for dark mode

    Args:
        fig (Figure): The plotly figure to export
        output_path (str): The path to save the image
        update_layout_kwargs (dict, optional): Update layout arguments. Defaults to {}.
        update_traces_kwargs (dict, optional): Update traces arguments. Defaults to {}.
        patch_colors (bool, optional): Whether to use the Kineo color palette. Defaults to True.

    Returns:
        Figure: The updated figure
    """

    return export_figure_as_png(
        fig,
        output_path,
        update_layout_kwargs=update_layout_kwargs,
        update_traces_kwargs=update_traces_kwargs,
        patch_colors=patch_colors,
        dark_mode=True,
    )


def export_figure_as_png_light_mode(
    fig: Figure,
    output_path: str,
    update_layout_kwargs: Dict[Any, Any] = {},
    update_traces_kwargs: Dict[Any, Any] = {},
    patch_colors: bool = True,
):
    """Export an plotly figure as a PNG image for light mode

    Args:
        fig (Figure): The plotly figure to export
        output_path (str): The path to save the image
        update_layout_kwargs (dict, optional): Update layout arguments. Defaults to {}.
        update_traces_kwargs (dict, optional): Update traces arguments. Defaults to {}.
        patch_colors: Whether to use the Kineo color palette. Defaults to True.

    Returns:
        Figure: The updated figure
    """

    return export_figure_as_png(
        fig,
        output_path,
        update_layout_kwargs=update_layout_kwargs,
        update_traces_kwargs=update_traces_kwargs,
        patch_colors=patch_colors,
        dark_mode=False,
    )
