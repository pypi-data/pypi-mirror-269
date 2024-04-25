from django.apps import apps as django_apps
from django.core.exceptions import ImproperlyConfigured

from dj_tenants.conf import settings
from dj_tenants.context import (
    get_current_tenant,
    tenant_context,
    tenant_context_disabled,
)

__all__ = [
    "get_current_tenant",
    "tenant_context",
    "tenant_context_disabled"
]


def get_tenant_model():
    try:
        return django_apps.get_model(settings.DJ_TENANTS_TENANT_MODEL, require_ready=False)
    except ValueError:
        raise ImproperlyConfigured(
            "DJ_TENANTS_TENANT_MODEL must be of the form 'app_label.model_name'"
        )
    except LookupError:
        raise ImproperlyConfigured(
            "DJ_TENANTS_TENANT_MODEL refers to model '%s' that has not been installed"
            % settings.DJ_TENANTS_TENANT_MODEL
        )
