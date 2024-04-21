import inspect
from typing import Any

from greyhorse.result import Result
from greyhorse.utils.injectors import ParamsInjector

from ..utils.registry import ReadonlyRegistry
from ..entities.providers import ProviderFactoryRegistry, ProviderKey
from ..entities.operator import OperatorFactoryRegistry, OperatorKey
from ..errors import ModuleFunctionError
from ..schemas.components import DepsPolicy, ResourceConf


class ResourceBuilder[K, R]:
    def __init__(
        self,
        deps_registry: ReadonlyRegistry[Any, Any],
        providers_registry: ProviderFactoryRegistry,
        operators_registry: OperatorFactoryRegistry,
        mapping  #: ResFactoryMapping[K, R],
    ):
        self._mapping = mapping
        self._deps_registry = deps_registry
        self._provider_factories = providers_registry
        self._operator_factories = operators_registry

    def _filter_deps(self, deps_filters: list[DepsPolicy], registry: ReadonlyRegistry) -> dict:
        result = {}

        for deps_filter in deps_filters:
            if deps_filter.name_pattern is not None:
                for name in registry.get_names(deps_filter.key):
                    if deps_filter.name_pattern.match(name):
                        result[deps_filter.key] = registry.get(deps_filter.key, name)
                        break
            elif dep := registry.get(deps_filter.key):
                result[deps_filter.key] = dep

            if deps_filter.key not in result:
                pass  # TODO error operator should provide "deps_filter.key"

        return result

    def __call__(self, conf: ResourceConf[K], **kwargs) -> Result[R]:
        if not conf.enabled:
            return Result.from_ok()  # TODO

        injector = ParamsInjector()

        values = {'name': conf.name, **conf.args}
        values.update(kwargs)

        for key, value in self._filter_deps(conf.deps, self._deps_registry).items():
            if inspect.isclass(key):
                injector.add_type_provider(key, value)
            else:
                values[key] = value

        for deps_conf, registry in (
            (conf.providers_deps, self._provider_factories),
            (conf.operators_deps, self._operator_factories),
        ):
            for key, factory in self._filter_deps(deps_conf, registry).items():
                res = factory()
                if not res.success:
                    return res
                injector.add_type_provider(key, res.result)

        if factory := self._mapping.get(conf.key):
            injected_args = injector(factory, values=values)
            res = factory(*injected_args.args, **injected_args.kwargs)
            if not res.success:
                return res
            instance = res.result
        else:
            return Result.from_error(None)  # TODO

        return Result.from_ok(instance)
