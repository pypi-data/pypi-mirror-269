"""
pyodide-mkdocs-theme
Copyleft GNU GPLv3 🄯 2024 Frédéric Zinelli

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.
If not, see <https://www.gnu.org/licenses/>.
"""


from typing import Any
from mkdocs.config import config_options as C


from .pyodide_logger import logger



def typ_deprecated_with_custom_msg(prop:str, typ:Any):
    return C.Deprecated(
        message=f"Macros using {prop} may not work anymore and will be removed in the future. "
                "Please contact the author of the theme if you need this macro/tool.",
        option_type = C.Optional(C.Type(typ)),
    )


def deprecation_warning(that:str):
    logger.warning(that)
