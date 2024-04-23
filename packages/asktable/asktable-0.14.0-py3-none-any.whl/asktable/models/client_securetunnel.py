
from asktable.models.client_base import convert_to_object, BaseResourceList
from atcommon.models.securetunnel import SecureTunnelCore, SecureTunnelLinkCore



class SecureTunnelLinkList(BaseResourceList):
    __do_not_print_properties__ = ['created_at']

    @convert_to_object(cls=SecureTunnelLinkCore)
    def _get_all_resources(self):
        return self._get_all_resources_request()


class SecureTunnel(SecureTunnelCore):
    def delete(self):
        return self.api.send(endpoint=f"/securetunnels/{self.id}", method="DELETE")

    @property
    def links(self):
        return SecureTunnelLinkList(self.api, endpoint=f"/securetunnels/{self.id}/links")


class SecureTunnelList(BaseResourceList):
    __do_not_print_properties__ = ['tenant_id', 'created_at']

    @convert_to_object(cls=SecureTunnel)
    def create(self):
        return self.api.send(endpoint=self.endpoint, method="POST")

    @convert_to_object(cls=SecureTunnel)
    def _get_all_resources(self):
        return self._get_all_resources_request()

    @convert_to_object(cls=SecureTunnel)
    def get(self, id):
        return self.api.send(endpoint=f"{self.endpoint}/{id}", method="GET")
