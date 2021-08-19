import os


def media(request):
    if 'CLOUDINARY_URL' in os.environ:
        MEDIA_URL = 'https://res.cloudinary.com/hg2mvjxam/image/upload/v1629394929/media/'
    else:
        MEDIA_URL = '/media/'

    return {'MEDIA_URL': MEDIA_URL}
