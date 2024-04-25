import sensorthings
import sensorthings.components as component_schemas
from django.utils.deprecation import MiddlewareMixin
from django.urls import resolve
from django.urls.exceptions import Http404
from django.http import HttpRequest
from sensorthings.engine import SensorThingsRequest
from sensorthings.utils import lookup_component
from sensorthings import settings


id_qualifier = settings.ST_API_ID_QUALIFIER


class SensorThingsMiddleware(MiddlewareMixin):

    @staticmethod
    def process_request(request: HttpRequest) -> None:
        """
        Middleware for resolving nested components in SensorThings URLs.

        The SensorThings specification requires the server to handle nested resource paths and addresses to table
        properties (including values and reference links for the properties). This middleware checks the request URLs
        for these special cases, extracts any extra parameters from these URLs and attaches them to the request, and
        links the request to the correct view function by updating the request's path_info attribute.

        Parameters
        ----------
        request : HttpRequest
            A Django HttpRequest object.

        Returns
        -------
        None
        """

        try:
            resolved_path = resolve(request.path_info)
            if resolved_path.url_name != 'st_complex_handler':
                # Check if path is part of a SensorThings API and determine the component.
                st_api = getattr(getattr(resolved_path.func, '__self__', None), 'api', None)
                if isinstance(st_api, sensorthings.SensorThingsAPI):
                    component_str = request.path_info.split('/')[-1].split('(')[0]
                    if component_str == 'CreateObservations':
                        request.component = 'Observation'
                    else:
                        request.component = lookup_component(
                            input_value=request.path_info.split('/')[-1].split('(')[0],
                            input_type='camel_plural',
                            output_type='camel_singular'
                        )
                    request.nested_resources = []
                return None
        except StopIteration:
            # Path is not part of the SensorThings app. Proceed normally.
            return None

        if request.method != 'GET':
            # Nested components are only allowed on GET requests.
            raise Http404

        route_length = len(resolved_path.route.split('/'))
        path_components = request.path_info.split('/')[route_length:]
        path_prefix = '/'.join(request.path_info.split('/')[:route_length])
        component = None
        nested_resources = []
        primary_component = None
        previous_component = None
        endpoint = None

        request.component_path = '/'.join(path_components)

        for i, raw_component in enumerate(path_components):
            path_info = f'{path_prefix}/{raw_component}'
            field_name = None

            try:
                resolved_path = resolve(path_info)
                if resolved_path.url_name == 'st_complex_handler':
                    # Sub-path may contain field names, or implicit links to related entities.
                    raise Http404
                if resolved_path.url_name.startswith('list'):
                    # This sub-path represents a collection of entities.
                    component = lookup_component(
                        input_value=resolved_path.url_name.replace('list_', ''),
                        input_type='snake_plural',
                        output_type='camel_singular'
                    )
                    field_name = lookup_component(
                        input_value=component,
                        input_type='camel_singular',
                        output_type='snake_plural'
                    )
                    primary_component = component
                    endpoint = f'{path_prefix}/{raw_component}'
                elif resolved_path.url_name.startswith('get'):
                    # This sub-path explicitly represents a single entity.
                    component = lookup_component(
                        input_value=resolved_path.url_name.replace('get_', ''),
                        input_type='snake_singular',
                        output_type='camel_singular'
                    )
                    field_name = lookup_component(
                        input_value=component,
                        input_type='camel_singular',
                        output_type='snake_singular'
                    )
                    primary_component = component
                    endpoint = f'{path_prefix}/{raw_component}'
                    nested_resources.append((component, resolved_path.kwargs.get(f'{field_name}_id')))
            except Http404:
                try:
                    # This sub-path may be an implicit relation and needs to be converted to an explicit path.
                    component_plural = lookup_component(
                        input_value=raw_component,
                        input_type='camel_singular',
                        output_type='camel_plural'
                    )
                    field_name = lookup_component(
                        input_value=raw_component,
                        input_type='camel_singular',
                        output_type='snake_singular'
                    )
                    if not field_name:
                        raise StopIteration
                    primary_component = raw_component
                    endpoint = f'{path_prefix}/{component_plural}({id_qualifier}temp_id{id_qualifier})'
                    nested_resources.append((raw_component, f'temp_id'))
                    component = raw_component
                except StopIteration:
                    # This sub-path may be a field name, $value, or $ref.
                    nested_resources = nested_resources[:-1]
                    component = raw_component
                    field_name = raw_component
                    query_dict = request.GET.copy()
                    query_dict['$select'] = field_name
                    request.GET = query_dict
            if previous_component in [c['SINGULAR_NAME'] for c in settings.ST_CAPABILITIES]:
                # Check that this component is a valid child of the previous part of the path.
                if field_name == '$ref':
                    query_dict = request.GET.copy()
                    query_dict['$select'] = 'self_link'
                    request.GET = query_dict
                elif field_name not in getattr(component_schemas, previous_component).__fields__:
                    raise Http404
            elif previous_component in ['$value', '$ref']:
                # $value/$ref must be the last components of a path.
                raise Http404
            elif component == '$value':
                if resolve(endpoint).url_name.startswith('list') or lookup_component(
                    input_value=previous_component,
                    input_type='camel_singular',
                    output_type='snake_singular'
                ) is not None or previous_component not in getattr(
                    component_schemas, primary_component
                ).__fields__.keys():
                    # $value can only be used on individual non-relational component fields.
                    raise Http404
                request.value_only = True
                query_dict = request.GET.copy()
                query_dict['$select'] = previous_component
                request.GET = query_dict
            elif component == '$ref':
                # $ref should be handled in a previous step.
                raise Http404

            previous_component = component

        request.nested_resources = nested_resources
        if endpoint:
            request.path_info = endpoint
        if primary_component in [c['SINGULAR_NAME'] for c in settings.ST_CAPABILITIES]:
            request.component = primary_component

    @staticmethod
    def process_view(request: SensorThingsRequest, view_func, view_args, view_kwargs) -> None:
        """
        Middleware for initializing a datastore engine for the request.

        This middleware generates a SensorThings engine object and attaches it to the request instance. The engine
        should include a connection to the associated database and methods for performing basic CRUD operations on that
        database and information model.

        Parameters
        ----------
        request : SensorThingsRequest
            A SensorThingsRequest object.
        view_func : Callable
            The view function associated with this request.
        view_args : list
            The arguments that will be passed to the view function.
        view_kwargs : dict
            The keyword arguments that will be passed to the view function.

        Returns
        -------
        None
        """

        if hasattr(getattr(view_func, '__self__', None), 'api'):
            st_api = view_func.__self__.api
            if isinstance(st_api, sensorthings.SensorThingsAPI):
                request.engine = st_api.engine(
                    host=request.get_host(),
                    scheme=request.scheme,
                    path=getattr(request, 'component_path', request.path.split('/')[-1]),
                    version=st_api.version,
                    component=getattr(request, 'component', None)
                )

                if hasattr(request, 'nested_resources'):
                    try:
                        replacement_id, filter_id_string = request.engine.resolve_nested_resource_path(
                            request.nested_resources
                        )

                        if replacement_id:
                            request.path_info = request.path_info.replace('temp_id', str(replacement_id))
                            for key in view_kwargs.keys():
                                view_kwargs[key] = view_kwargs[key].replace('temp_id', str(replacement_id))

                        if filter_id_string:
                            query_dict = request.GET.copy()
                            if not query_dict.get('$filter'):
                                query_dict['$filter'] = filter_id_string
                            else:
                                query_dict['$filter'] += f' and {filter_id_string}'
                            request.GET = query_dict

                    except Http404:
                        request.engine.component = None
