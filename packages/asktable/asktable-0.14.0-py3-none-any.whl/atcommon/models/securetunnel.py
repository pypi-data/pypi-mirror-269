from atcommon.models.base import BaseCoreModel


class SecureTunnelCore(BaseCoreModel):
    __properties_init__ = ['tenant_id', 'id', 'atst_server_host', 'atst_server_port',
                           'links_count', 'status', 'created_at', 'modified_at', ]

    def __repr__(self):
        return f"<ATST {self.id}>"


class SecureTunnelLinkCore(BaseCoreModel):
    __properties_init__ = ['securetunnel_id', 'id', 'created_at',
                           'modified_at', 'target_host', 'target_port',
                           'proxy_port', 'status', 'datasource_ids',]

    def __repr__(self):
        return f"<STLink {self.id}>"