import base64
import re

from PIL import Image

from django.template.defaultfilters import register
from django.contrib.staticfiles.finders import find as find_static_file
from django.utils.safestring import mark_safe

ESCAPE_TABLE = {
    '#': '%23',
    '%': '%25',
    ':': '%3A',
    '<': '%3C',
    '>': '%3E',
    '"': "'",
}
escape_re = re.compile('|'.join(ESCAPE_TABLE.keys()))


def prepare_svg(svg: str):
    svg = re.sub(r'\s+', ' ', svg).strip()
    svg = re.sub(r'> <', '><', svg)
    svg = escape_re.sub(lambda x: ESCAPE_TABLE[x.group()], svg)
    return svg


@register.simple_tag
def raw_media_file(url: str):
    """
    a template tag that returns a raw staticfile
    Usage::
        {% raw_media_file url %}
    Examples::
        <style>{% raw_media_file path/to/style.css %}</style>
    """
    path = get_media_url_path(url)
    return get_file_data(path)


@register.simple_tag
def encode_media_file(url: str, encoding='base64', file_type='image'):
    """
    a template tag that returns a encoded string representation of a staticfile
    Usage::
        {% encode_media_file url [encoding] %}
    Examples::
        <img src="{% encode_media_file 'path/to/img.png' %}">

    Example of media urls (they should be presented w/o `/media/` prefix:
    - `/media/samples/thumb.png` -> `samples/thumb.png`
    """
    ext = get_file_extension(url)
    file_data = raw_media_file(url)
    file_data = base64.b64encode(file_data)
    encoded_data = encode_file_data(file_data, ext, encoding, file_type)
    return encoded_data
    # return 'data:{0}/{1};{2},{3}'.format(file_type, ext, encoding, file_data)


@register.simple_tag
def lqip_media_img_tag(url, thumb, id='', className='', encoding='base64', file_type='image'):
    """
    a template tag that returns an image with lqip encoded thumbnail
    Usage::
        {% encode_media_file url thumb [encoding] %}
    Examples::
        <img src="{% encode_media_file 'path/to/thumb.png' 'path/to/img.png' %}">

    Example of media urls (they should be presented w/o `/media/` prefix:
    - `/media/samples/thumb.png` -> `samples/thumb.png`
    """
    ext = get_file_extension(url)
    thumbPath = get_media_url_path(thumb)
    file_data = raw_media_file(thumbPath)
    file_data = base64.b64encode(file_data)
    origPath = get_media_url_path(url)
    im = Image.open(origPath)
    width, height = im.size
    encoded_data = encode_file_data(file_data, ext, encoding, file_type)
    svg_data = (
        r'<svg xmlns="http://www.w3.org/2000/svg"'
        r' xmlns:xlink="http://www.w3.org/1999/xlink"'
        f' viewBox="0 0 {width} {height}">'
        r'<filter id="b" color-interpolation-filters="sRGB">'
        r'<feGaussianBlur stdDeviation=".5"></feGaussianBlur>'
        r'<feComponentTransfer>'
        r'<feFuncA type="discrete" tableValues="1 1"></feFuncA>'
        r'</feComponentTransfer>'
        r'</filter>'
        r'<image filter="url(#b)" preserveAspectRatio="none"'
        r' height="100%" width="100%"'
        f' xlink:href="{encoded_data}">'
        r'</image>'
        r'</svg>'
    )
    escaped_svg_data = prepare_svg(svg_data)
    URI = f'data:image/svg+xml;charset=utf-8,{escaped_svg_data}'
    styleCode = f'background-size: cover; background-image: url("{URI}");'
    quotedStyleCode = re.sub(r'"', '&quot;', styleCode)
    return mark_safe(
        r'<img'
        f' id="{id}"'
        f' class="{className}"'
        f' src="{url}"'
        f' style="{quotedStyleCode}"'
        f' width="{width}"'
        f' height="{height}"'
        r' loading="lazy"'
        r' />'
    )


def get_file_extension(path: str):
    return path.split('.')[-1].lower()


def encode_file_data(file_data: bytes, ext='', encoding='base64', file_type='image'):
    return 'data:{0}/{1};{2},{3}'.format(file_type, ext, encoding, file_data.decode('utf-8'))


def get_media_url_path(url: str):
    path = get_following_url_part(url, '/media/')
    path = find_static_file(path)
    return path


def get_following_url_part(path: str, find_needle: str):
    # Try to find an url part
    pos = path.find(find_needle)
    if pos != -1:
        start_pos = pos + len(find_needle)
        path = path[start_pos:]
    return path


def get_file_data(path):
    with open(path, 'rb') as f:
        data = f.read()
        f.close()
        return data
