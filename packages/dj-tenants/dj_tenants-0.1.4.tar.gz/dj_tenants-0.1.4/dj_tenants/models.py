from django.db import models

from dj_tenants.conf import settings
from dj_tenants.context import get_current_tenant, get_dj_state

tenant_field_name = settings.DJ_TENANTS_TENANT_FIELD


class TenantManager(models.Manager):
    def bulk_create(self, objs, *args, **kwargs):
        state = get_dj_state()
        if state.get("enabled", True):
            tenant_id = get_current_tenant().id
            for obj in objs:
                setattr(obj, 'tenant_id', tenant_id)
        return super().bulk_create(objs, *args, **kwargs)

    def bulk_update(self, objs, fields, *args, **kwargs):
        state = get_dj_state()
        if state.get("enabled", True):
            tenant_id = get_current_tenant().id
            for obj in objs:
                setattr(obj, 'tenant_id', tenant_id)
            return super().bulk_update(objs, fields, *args, **kwargs)


class TenantAware(models.Model):
    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        setattr(self, tenant_field_name, get_current_tenant())
        super().save(*args, **kwargs)

    def get_tenant_instance(self):
        return getattr(self, tenant_field_name)
