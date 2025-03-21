import re

# @see https://gist.github.com/rodrigoborgesdeoliveira/987683cfbfcc8d800192da1e73adc486
youtubeLinkPrefixRegex = re.compile(r'^https://(\w*\.)?(youtube\.com|youtu\.be)/')
linkPrefixRegex = re.compile(r'^https://')

__all__ = [
    'youtubeLinkPrefixRegex',
    'linkPrefixRegex',
]
