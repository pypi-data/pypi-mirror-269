from django.db.models.sql import compiler

from dj_tenants import get_current_tenant
from dj_tenants.context import get_dj_state


class SQLCompiler(compiler.SQLCompiler):
    def as_sql(self, *args, **kwargs):
        has_tenant_id = any(field.column == 'tenant_id' for field in self.query.model._meta.fields)
        dj_state = get_dj_state()
        if has_tenant_id and dj_state.get('enabled', True):
            self.query.add_filter("tenant_id", get_current_tenant().id)

        return super().as_sql(*args, **kwargs)


class SQLInsertCompiler(compiler.SQLInsertCompiler, SQLCompiler):
    def field_as_sql(self, field, val):
        res = super().field_as_sql(field, val)
        dj_state = get_dj_state()
        if field.column == 'tenant_id' and dj_state.get('enabled', True):
            return '%s', [str(get_current_tenant().id)]
        return res


class SQLDeleteCompiler(compiler.SQLDeleteCompiler, SQLCompiler):
    def as_sql(self, *args, **kwargs):
        return super().as_sql(*args, **kwargs)


class SQLUpdateCompiler(compiler.SQLUpdateCompiler, SQLCompiler):
    def as_sql(self, *args, **kwargs):
        dj_state = get_dj_state()
        has_tenant_id = any(field.column == 'tenant_id' for field in self.query.model._meta.fields)
        if has_tenant_id and dj_state.get('enabled', True):
            self.query.add_filter("tenant_id", get_current_tenant().id)
        return super().as_sql(*args, **kwargs)


class SQLAggregateCompiler(compiler.SQLAggregateCompiler, SQLCompiler):
    def as_sql(self, *args, **kwargs):
        return super().as_sql(*args, **kwargs)
