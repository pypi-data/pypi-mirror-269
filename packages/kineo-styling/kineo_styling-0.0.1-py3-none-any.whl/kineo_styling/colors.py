import pandas as pd
import plotly.express as px

kineo_pink = {
    "base_color": "#E6007E",
    "shaded": ["#E6007E", "#EB3398", "#F066B2", "#F599CB"],
}
kineo_purple = {
    "base_color": "#5D72C2",
    "shaded": ["#5D72C2", "#7D8ECE", "#9EAADA", "#BEC7E7"],
}
kineo_purple_light = {
    "base_color": "#94A5F8",
    "shaded": ["#94A5F8", "#A9B7F9", "#BFC9FB", "#D4DBFC"],
}
kineo_aquamarine = {
    "base_color": "#1ABEBA",
    "shaded": ["#1ABEBA", "#48CBC8", "#76D8D6", "#A3E5E3"],
}
kineo_mohair = {
    "base_color": "#CDC8BA",
    "shaded": ["#CDC8B7", "#D7D3C5", "#E1DED4", "#EBE9E2"],
}
kineo_mauve = {
    "base_color": "#352F7B",
    "shaded": ["#352F7B", "#5D5995", "#8682B0", "#AEACCA"],
}
kineo_fuschia = {
    "base_color": "#C50E92",
    "shaded": ["#C50E92", "#D13EA8", "#DC6FBD", "#E89FD3"],
}
kineo_unicorn = {
    "base_color": "#B070F0",
    "shaded": ["#B070F0", "#C08DF3", "#D0A9F6", "#DFC6F6"],
}
kineo_marine_grey = {
    "base_color": "#696969",
    "shaded": ["#696969", "#878787", "#A5A5A5", "#C3C3C3"],
}
kineo_burned_yellow = {
    "base_color": "#F3BA27",
    "shaded": ["#F3BA27", "#F6C853", "#F8D67E", "#FAE4A9"],
}
kineo_azure_blue = {
    "base_color": "#3E65E4",
    "shaded": ["#3E65E4", "#6584E9", "#8BA3EF", "#B2C1F4"],
}

kineo_primary = kineo_pink["base_color"]
kineo_secondary = kineo_purple["base_color"]

kineo_colors_2 = [kineo_pink["base_color"], kineo_purple["base_color"]]
kineo_colors_3 = [
    kineo_pink["base_color"],
    kineo_purple["base_color"],
    kineo_aquamarine["base_color"],
]
kineo_colors_5 = [
    kineo_pink["base_color"],
    kineo_purple["base_color"],
    kineo_aquamarine["base_color"],
    kineo_burned_yellow["base_color"],
    kineo_azure_blue["base_color"],
]
kineo_colors_full = [
    kineo_pink["base_color"],
    kineo_purple["base_color"],
    kineo_aquamarine["base_color"],
    kineo_burned_yellow["base_color"],
    kineo_purple_light["base_color"],
    kineo_azure_blue["base_color"],
    kineo_unicorn["base_color"],
    kineo_mauve["base_color"],
    kineo_fuschia["base_color"],
    kineo_marine_grey["base_color"],
    kineo_mohair["base_color"],
]


def show_colors():
    """Show the colors avaliable in the Kineo color palette"""
    show_shades = []
    for c, cn in [
        (kineo_pink, "kineo_pink"),
        (kineo_purple, "kineo_purple"),
        (kineo_aquamarine, "kineo_aquamarine"),
        (kineo_burned_yellow, "kineo_burned_yellow"),
        (kineo_purple_light, "kineo_purple_light"),
        (kineo_azure_blue, "kineo_azure_blue"),
        (kineo_unicorn, "kineo_unicorn"),
        (kineo_mauve, "kineo_mauve"),
        (kineo_fuschia, "kineo_fuschia"),
        (kineo_marine_grey, "kineo_marine_grey"),
        (kineo_mohair, "kineo_mohair"),
    ]:
        for i, cs in enumerate(c["shaded"]):
            show_shades.append(
                {
                    "base": cn,
                    "color": cs,
                    "shade": f"{cn.replace('kineo_', '')}_{i}",
                    "val": 1,
                }
            )
    show_shades = pd.DataFrame(show_shades)
    fig = px.bar(
        show_shades,
        x="base",
        y="val",
        color="shade",
        text="color",
        color_discrete_map=show_shades.set_index("shade")["color"].to_dict(),
    )
    fig.update_layout(
        showlegend=False,
        yaxis={"visible": False},
        xaxis={"visible": False},
        margin={"l": 0, "r": 0, "t": 0, "b": 0},
    )
    fig.show()
