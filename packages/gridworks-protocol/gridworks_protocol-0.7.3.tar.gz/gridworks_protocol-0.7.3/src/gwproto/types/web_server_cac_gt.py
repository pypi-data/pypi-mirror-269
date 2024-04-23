import json
import typing
from typing import Literal

from gwproto.data_classes.cacs.web_server_cac import WebServerCac
from gwproto.data_classes.component_attribute_class import ComponentAttributeClass
from gwproto.types.component_attribute_class_gt import ComponentAttributeClassGt


class WebServerCacGt(ComponentAttributeClassGt):
    TypeName: Literal["hubitat.cac.gt"] = "web.server.cac.gt"
    Version: Literal["000"] = "000"

    @classmethod
    def from_data_class(cls, cac: WebServerCac) -> "WebServerCacGt":
        return WebServerCacGt(
            ComponentAttributeClassId=cac.component_attribute_class_id,
            DisplayName=cac.display_name,
        )

    def to_data_class(self) -> WebServerCac:
        cac = ComponentAttributeClass.by_id.get(self.ComponentAttributeClassId, None)
        if cac is not None:
            return typing.cast(WebServerCac, cac)
        return WebServerCac(
            component_attribute_class_id=self.ComponentAttributeClassId,
            display_name=self.DisplayName,
        )

    def __hash__(self):
        return hash((type(self),) + tuple(self.__dict__.values()))  # noqa
