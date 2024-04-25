from atcommon.models.base import BaseCoreModel


class SecureTunnelCore(BaseCoreModel):
    __properties_init__ = ['tenant_id', 'id', 'name', 'atst_server_host', 'atst_server_port',
                           'links_count', 'status', 'created_at', 'modified_at', 'info']

    def __repr__(self):
        return f"<ATST {self.id}>"


class SecureTunnelLinkCore(BaseCoreModel):
    # remove proxy_host because it is configured in configfile
    __properties_init__ = ['securetunnel_id', 'id', 'created_at',
                           'modified_at', 'target_host', 'target_port',
                           'proxy_port', 'status', 'datasource_ids',]

    def __repr__(self):
        return (f"<STLink {self.id}({self.securetunnel_id}) [proxy]:{self.proxy_port}->"
                f"{self.target_host}:{self.target_port}>")