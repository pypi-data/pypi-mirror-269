from typing import Optional

from gwproto.data_classes.component import Component
from gwproto.types.web_server_gt import WebServerGt


class WebServerComponent(Component):
    web_server_gt: WebServerGt

    def __init__(
        self,
        component_id: str,
        component_attribute_class_id: str,
        web_server_gt: WebServerGt,
        display_name: Optional[str] = None,
        hw_uid: Optional[str] = None,
    ):
        self.web_server_gt = web_server_gt
        super().__init__(
            component_id=component_id,
            component_attribute_class_id=component_attribute_class_id,
            display_name=display_name,
            hw_uid=hw_uid,
        )
