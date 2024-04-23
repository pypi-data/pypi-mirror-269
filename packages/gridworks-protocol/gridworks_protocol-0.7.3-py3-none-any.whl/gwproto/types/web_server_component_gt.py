import typing
from typing import Literal

from gwproto.data_classes.component import Component
from gwproto.data_classes.components.web_server_component import WebServerComponent
from gwproto.types.component_gt import ComponentGt
from gwproto.types.web_server_gt import WebServerGt


class WebServerComponentGt(ComponentGt):
    WebServer: WebServerGt
    TypeName: Literal["web.server.component.gt"] = "web.server.component.gt"
    Version: Literal["000"] = "000"

    def __hash__(self):
        return hash((type(self),) + tuple(self.__dict__.values()))  # noqa

    @classmethod
    def from_data_class(cls, component: WebServerComponent) -> "WebServerComponentGt":
        return WebServerComponentGt(
            ComponentId=component.component_id,
            ComponentAttributeClassId=component.component_attribute_class_id,
            WebServer=component.web_server_gt,
            DisplayName=component.display_name,
            HwUid=component.hw_uid,
        )

    def to_data_class(self) -> WebServerComponent:
        component = Component.by_id.get(self.ComponentId, None)
        if component is not None:
            return typing.cast(WebServerComponent, component)
        return WebServerComponent(
            component_id=self.ComponentId,
            component_attribute_class_id=self.ComponentAttributeClassId,
            web_server_gt=self.WebServer,
            display_name=self.DisplayName,
            hw_uid=self.HwUid,
        )
