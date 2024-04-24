name = 'edurpa_google'
from .Classroom import Classroom
from .CustomOAuth import CustomOAuth
from .Form import Form
from .Utils import Utils
from robotlibcore import DynamicCore

class Google(DynamicCore):
    def __init__(
        self
    ):
        # Register keyword libraries to LibCore
        libraries = [
            Classroom(),
            Form(),
            CustomOAuth(),
            Utils()
        ]
        super().__init__(libraries)