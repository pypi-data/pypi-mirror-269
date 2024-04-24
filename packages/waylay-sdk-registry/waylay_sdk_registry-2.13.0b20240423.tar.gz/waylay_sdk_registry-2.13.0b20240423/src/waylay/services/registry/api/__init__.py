"""Waylay Function Registry: apis."""

# import apis into api package
from .about_api import AboutApi
from .jobs_api import JobsApi
from .models_api import ModelsApi
from .plugs_api import PlugsApi
from .runtimes_api import RuntimesApi
from .schemas_api import SchemasApi
from .webscripts_api import WebscriptsApi

__all__ = [
    "AboutApi",
    "JobsApi",
    "ModelsApi",
    "PlugsApi",
    "RuntimesApi",
    "SchemasApi",
    "WebscriptsApi",
]
