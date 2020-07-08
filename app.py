# coding: utf-8

from pathlib import Path
import streamlit as st
import matplotlib.pyplot as plt

import plot
import base64


# Title
st.title("Matplotlib Style Configurator")
st.markdown("""[GitHub repository](https://github.com/dhaitz/matplotlib-style-configurator) -
            [Plotting code](https://matplotlib.org/gallery/style_sheets/style_sheets_reference.html) -
            [Matplotlib style gallery ](https://tonysyu.github.io/raw_content/matplotlib-style-gallery/gallery.html) -
            [mplcyberpunk](https://github.com/dhaitz/mplcyberpunk) -
            [MPL stylesheets](https://github.com/dhaitz/matplotlib-stylesheets)""")


# Sidebar: basic config selectors
base_styles = ['default'] + [style for style in plt.style.available if not style.startswith('_')] + [
    "cyberpunk",
    "https://raw.githubusercontent.com/dhaitz/matplotlib-stylesheets/master/pitayasmoothie-dark.mplstyle",
    "https://raw.githubusercontent.com/dhaitz/matplotlib-stylesheets/master/pacoty.mplstyle",
    "https://raw.githubusercontent.com/dhaitz/matplotlib-stylesheets/master/pitayasmoothie-light.mplstyle",
]
style = st.sidebar.selectbox("Choose base style:", base_styles)
plt.style.use(style)

n_columns = st.sidebar.selectbox("Number of columns", [1, 2, 3, 6], index=2)


# Sidebar: parameter customization widgets
st.sidebar.header("Customize style:")
st.sidebar.text("(Parameter list is non-exhaustive)")
params = Path('parameters.txt').read_text().splitlines()
for param in params:
    widget_type = st.sidebar.checkbox if (type(plt.rcParams[param]) == bool) else st.sidebar.text_input

    if type(plt.rcParams[param]) == list:  # can't put lists in text boxes -> use only first item
        plt.rcParams[param] = [widget_type(param, value=plt.rcParams[param][0])]
    else:
        plt.rcParams[param] = widget_type(param, value=plt.rcParams[param])


# Draw plot
fig = plot.plot_figure(style_label=style, n_columns=n_columns)
st.pyplot(fig=fig)
plt.close(fig)

# Link to download stylesheet
def get_stylesheet_download_link(params, filename="my_style.mplstyle"):
    """Generates a download link for a stylesheet file. https://discuss.streamlit.io/t/heres-a-download-function-that-works-for-dataframes-and-txt/4052"""

    stylesheet_lines = []
    for param in params:
        if plt.rcParamsDefault[param] != plt.rcParams[param]:  # only store parameters which were changed from the defaults.
            if type(plt.rcParams[param]) == list:
                value = ', '.join(plt.rcParams[param])
            else:
                value = plt.rcParams[param]
            stylesheet_lines.append(f"{param}: {value}".replace('#', ''))

    stylesheet_text = '\n'.join(stylesheet_lines)
    b64 = base64.b64encode(stylesheet_text.encode()).decode()
    return f'<a href="data:file/text;base64,{b64}" download={filename}>Download stylesheet</a> (<a href="https://matplotlib.org/tutorials/introductory/customizing.html">Installation instructions</a>)'

st.markdown(get_stylesheet_download_link(params), unsafe_allow_html=True)


# workaround to open in wide mode (https://github.com/streamlit/streamlit/issues/314#issuecomment-579274365)
max_width_str = f"max-width: 1000px;"
st.markdown(f"""<style>.reportview-container .main .block-container{{ {max_width_str} }}</style>""", unsafe_allow_html=True)
