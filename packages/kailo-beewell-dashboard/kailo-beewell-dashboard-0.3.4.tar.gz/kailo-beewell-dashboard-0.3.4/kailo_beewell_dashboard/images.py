'''
Helper functions for working with image files
'''
from tempfile import NamedTemporaryFile
import base64
from importlib.resources import files


def convert_fig_to_html(fig, alt_text):
    '''
    Convert plotly fig to HTML by saving it as a temporary PNG file, and then
    importing that and converting it to HTML which can produce the figure.

    Parameters
    ----------
    fig : plotly figure object
        Figure to be converted
    alt_text : string
        Alternative text for the figure

    Returns
    -------
    img_tag : string
        HTML to generate image
    '''
    # Adjust the layout so the figure proportions fit in the PDF report and are
    # similar to streamlit, with automargin to ensure labels aren't cut off
    fig.update_layout(
        height=411,
        width=600,
        xaxis=dict(automargin=True),
        yaxis=dict(automargin=True))

    # Write image to a temporary file, then open again and convert to HTML
    with NamedTemporaryFile(suffix='.png') as temp:
        fig.write_image(temp)
        temp.seek(0)
        data_uri = base64.b64encode(
            open(temp.name, 'rb').read()).decode('utf-8')

    # Generate the image tag, inserting the HTML for the figure
    img_tag = f'''
<img src='data:image/png;base64,{data_uri}' alt='{alt_text}'>'''

    return img_tag


def get_image_path(filename):
    '''
    Get path for image in the kailo-beewell-dashboard package

    Parameters
    ----------
    filename: string
        Name of the image file within the package (e.g. 'image.png')

    Returns
    -------
    img_path : string
        Path to image within the package
    '''
    img_path = str(files('kailo_beewell_dashboard')
                   .joinpath(f'images/{filename}'))
    return img_path
