# coding: utf-8

from pathlib import Path
import streamlit as st
import matplotlib.pyplot as plt

import plot

st.title("Matplotlib Style Configurator")
st.write("""[GitHub repository](https://github.com/dhaitz/matplotlib-style-configurator) -
            [Plotting code](https://matplotlib.org/gallery/style_sheets/style_sheets_reference.html) - 
            [Matplotlib style gallery ](https://tonysyu.github.io/raw_content/matplotlib-style-gallery/gallery.html) - 
            [mplcyberpunk](https://github.com/dhaitz/mplcyberpunk) - 
            [MPL stylesheets](https://github.com/dhaitz/matplotlib-stylesheets)""")

base_styles = ['default'] + [style for style in plt.style.available if not style.startswith('_')] + [
    "cyberpunk",
    "https://raw.githubusercontent.com/dhaitz/matplotlib-stylesheets/master/pitayasmoothie-dark.mplstyle",
    "https://raw.githubusercontent.com/dhaitz/matplotlib-stylesheets/master/pacoty.mplstyle",
    "https://raw.githubusercontent.com/dhaitz/matplotlib-stylesheets/master/pitayasmoothie-light.mplstyle",
]
style = st.selectbox("Choose base style:", base_styles)
plt.style.use(style)

# Set up sidebar with parameter customization widgets
st.sidebar.title("Customize")
params = Path('parameters.txt').read_text().splitlines()
for param in params:
    widget_type = st.sidebar.checkbox if (type(plt.rcParams[param]) == bool) else st.sidebar.text_input

    if type(plt.rcParams[param]) == list:  # can't put lists in text boxes -> use only first item
        plt.rcParams[param] = [widget_type(param, value=plt.rcParams[param][0])]
    else:
        plt.rcParams[param] = widget_type(param, value=plt.rcParams[param])

# Draw plot
n_columns = st.selectbox("Number of columns", [1, 2, 3, 6], index=2)
fig = plot.plot_figure(style_label=style, n_columns=n_columns)
st.pyplot(fig=fig)

# Generate stylesheet
if st.button("Generate stylesheet text"):
    for param in params:
        if plt.rcParamsDefault[param] != plt.rcParams[param]:
            st.write(f"{param}: {plt.rcParams[param]}".replace('#', ''))  # no hash symbol in stylefile?
      
