'''
Helper functions for setting up the page and page formatting.
'''
import base64
import streamlit as st
from importlib.resources import files


def page_logo():
    '''
    Create logo to go above the pages in the sidebar
    '''
    # Set up logo for display in markdown, which we use instead of st.image()
    # to allow inline display and alt_text
    img_path = str(files('kailo_beewell_dashboard')
                   .joinpath('images/kailo_beewell_logo_padded.png'))
    file = open(img_path, 'rb')
    contents = file.read()
    url = base64.b64encode(contents).decode('utf-8')
    file.close()

    # Display logo
    st.markdown(f'''
<style>
    [data-testid='stSidebarNav'] {{
        background-image: url('data:image/png;base64,{url}');
        background-repeat: no-repeat;
        padding-top: 110px; /* Move page names down */
        background-position: 0px 50px; /* Move image down */
        background-size: 240px;
    }}
</style>
''', unsafe_allow_html=True)


def page_setup(type):
    '''
    Set up page to standard conditions, with layout as specified

    Parameters
    ----------
    type : string
        Survey type - 'standard', 'symbol', or 'public'
    '''
    # Set up streamlit page parameters
    st.set_page_config(
        page_title='#BeeWell School Dashboard',
        page_icon='🐝',
        initial_sidebar_state='expanded',
        layout='centered',
        menu_items={'About': f'''
{type.capitalize()} #BeeWell survey dashboard for North Devon and Torridge in
2023/24 as part of Kailo.'''})

    # Import CSS style
    css_path = str(files('kailo_beewell_dashboard').joinpath('css/style.css'))
    with open(css_path) as css:
        st.markdown(f'<style>{css.read()}</style>', unsafe_allow_html=True)

    # Add page logo
    page_logo()


def blank_lines(n):
    '''
    Create blank lines on the page of the dashboard

    Parameters
    ----------
    n : int
        Number of blank lines to create
    '''
    counter = 0
    while counter < n:
        st.text('')
        counter += 1


def page_footer(school):
    '''
    Create a footer for each page

    Parameters
    ----------
    school : string
        Name of the chosen school for this dashboard
    '''
    blank_lines(2)
    st.divider()
    st.markdown(f'''
<p style='font-size: 12px;'>
This dashboard shows results for pupils at {school}. If you have any
questions, you can get in touch with the Kailo team by emailing
kailobeewell@dartington.org.uk.''', unsafe_allow_html=True)
