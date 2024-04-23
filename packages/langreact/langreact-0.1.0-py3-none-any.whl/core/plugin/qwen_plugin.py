"""
File Created: Thursday, 18th April 2024 11:04:20 pm
Author: zhangli.max (zhangli.max@bigo.com)
-----
Last Modified: Thursday, 18th April 2024 11:05:34 pm
Modified By: zhangli.max (zhangli.max@bigo.com)
"""

from core.application import Application, QwenLMApplication
from core.plugin.plugins import ApplicationPlugin


class QwenTurboPlugin(ApplicationPlugin):
    def __init__(self):
        super().__init__("qwen", "0.1")

    def create_new_application(
        self, local_context, configure, reflection=False
    ) -> Application:
        return QwenLMApplication("turbo", configure)
