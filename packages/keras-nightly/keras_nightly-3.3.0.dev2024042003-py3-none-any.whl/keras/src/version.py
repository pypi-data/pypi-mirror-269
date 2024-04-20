from keras.src.api_export import keras_export

# Unique source of truth for the version number.
__version__ = "3.3.0.dev2024042003"


@keras_export("keras.version")
def version():
    return __version__
