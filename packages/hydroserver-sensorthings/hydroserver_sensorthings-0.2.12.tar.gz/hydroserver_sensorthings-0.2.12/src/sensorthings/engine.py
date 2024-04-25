import re
from itertools import groupby
from abc import ABCMeta
from uuid import UUID
from datetime import datetime
from typing import Union, Tuple, List, Optional
from ninja.errors import HttpError
from django.http import HttpRequest
from django.urls.exceptions import Http404
from odata_query.grammar import ODataParser, ODataLexer
from odata_query.exceptions import ParsingException
from sensorthings import components as component_schemas
from sensorthings import settings
from sensorthings.utils import lookup_component
from sensorthings.schemas import ListQueryParams, EntityId
from sensorthings.components.things.engine import ThingBaseEngine
from sensorthings.components.locations.engine import LocationBaseEngine
from sensorthings.components.historicallocations.engine import HistoricalLocationBaseEngine
from sensorthings.components.datastreams.engine import DatastreamBaseEngine
from sensorthings.components.sensors.engine import SensorBaseEngine
from sensorthings.components.observedproperties.engine import ObservedPropertyBaseEngine
from sensorthings.components.featuresofinterest.engine import FeatureOfInterestBaseEngine
from sensorthings.components.observations.engine import ObservationBaseEngine
from sensorthings.components.observations.schemas import ObservationPostBody, ObservationDataArrayFields, \
     ObservationDataArray, ObservationParams


class SensorThingsBaseEngine(
    ThingBaseEngine,
    LocationBaseEngine,
    HistoricalLocationBaseEngine,
    DatastreamBaseEngine,
    SensorBaseEngine,
    ObservedPropertyBaseEngine,
    FeatureOfInterestBaseEngine,
    ObservationBaseEngine,
    metaclass=ABCMeta
):
    """
    Abstract base class for a SensorThings engine.

    A SensorThings API must be linked to a SensorThings engine to perform database operations. This class defines all
    required methods for an engine class and should be inherited by any SensorThings engine used by an API.
    """

    def __init__(
            self,
            host,
            scheme,
            path,
            version,
            component
    ):
        self.request = None
        self.host = host
        self.scheme = scheme
        self.path = path
        self.version = version
        self.component = component
        self.id_qualifier = settings.ST_API_ID_QUALIFIER

    def list_entities(self, request, query_params, component=None, join_ids=None, drop_related_links=False, root=True):
        """"""

        self.request = request

        if not self.component:
            raise HttpError(404, 'Entity not found.')

        if not join_ids:
            join_ids = {}

        entities, count = getattr(self, 'get_' + lookup_component(
            component if component else self.component, 'camel_singular', 'snake_plural'
        ))(
            filters=self.get_filters(query_params.get('filters')) if query_params.get('filters') else None,
            pagination=self.get_pagination(query_params),
            ordering=self.get_ordering(query_params),
            expanded=not root,
            get_count=True if query_params.get('count') is True else False,
            **join_ids
        )

        next_link = self.build_next_link(
            query_params=query_params,
            length=len(entities),
            count=count
        )

        if query_params.get('result_format') != 'dataArray':
            entities = self.build_selects_links_and_nested_components(
                request=request,
                component=component if component else self.component,
                values=entities,
                expand=query_params.get('expand'),
                select=query_params.get('select'),
                drop_related_links=drop_related_links
            )

        response = {
            'value': entities
        }

        if query_params.get('count') is True:
            response['count'] = count

        if next_link:
            response['next_link'] = next_link
        if query_params.get('result_format') == 'dataArray' and \
                (component is None and self.component == 'Observation' or component == 'Observation'):
            response = self.convert_to_data_array(
                response=response,
                select=query_params.get('select')
            )

        return response

    def get_entity(self, request, entity_id, query_params):

        self.request = request

        if not self.component:
            raise HttpError(404, 'Entity not found.')

        entities, count = getattr(self, 'get_' + lookup_component(
            self.component, 'camel_singular', 'snake_plural'
        ))(
            filters=self.get_filters(f"id eq '{entity_id}'"),
            get_count=False
        )

        entities = self.build_selects_links_and_nested_components(
            request=request,
            component=self.component,
            values=entities,
            expand=query_params.get('expand'),
            select=query_params.get('select')
        )

        entity = next(iter(entities), None)

        if not entity:
            raise HttpError(404, 'Record not found.')

        if getattr(request, 'value_only', False) is True:
            request.response_string = entity[query_params['select']]

        return entity

    def create_entity(self, request, response, entity_body):
        """"""

        self.request = request

        entity_id = getattr(self, 'create_' + lookup_component(
            self.component, 'camel_singular', 'snake_singular'
        ))(
            entity_body
        )

        response['Location'] = self.get_ref(self.component, entity_id)

    def create_entity_bulk(self, request, entity_body):
        """"""

        self.request = request
        grouped_entity_body = {}

        if request.component == 'Observation':
            for group in entity_body:
                grouped_entity_body[group.datastream.id] = grouped_entity_body.get(
                    group.datastream.id, []
                )
                mapped_fields = {
                    group.components.index(meta.alias) if meta.alias in group.components else None: field
                    for field, meta in ObservationPostBody.__fields__.items()
                }
                grouped_entity_body[group.datastream.id].extend([
                    ObservationPostBody(
                        datastream=EntityId(id=group.datastream.id),
                        **{
                            mapped_fields[i]: value for i, value in enumerate(entity)
                        }
                    ) for entity in group.data_array
                ])

        entity_ids = getattr(self, 'create_' + lookup_component(
            self.component, 'camel_singular', 'snake_singular'
        ) + '_bulk')(
            grouped_entity_body
        )

        return [
            self.get_ref(self.component, entity_id)
            for entity_id in entity_ids
        ]

    def update_entity(self, request, entity_id, entity_body, component=None):
        """"""

        self.request = request

        getattr(self, 'update_' + lookup_component(
            component if component else self.component, 'camel_singular', 'snake_singular'
        ))(
            entity_id,
            entity_body
        )

    def delete_entity(self, request, entity_id):
        self.request = request

        getattr(self, 'delete_' + lookup_component(
            self.component, 'camel_singular', 'snake_singular'
        ))(
            entity_id,
        )

    def get_ref(
            self,
            component: Optional[str] = None,
            entity_id: Optional[str] = None,
            related_component: Optional[str] = None,
            is_collection: Optional[bool] = False
    ) -> str:
        """
        Builds a reference URL for a given entity.

        Parameters
        ----------
        component : str
            The value to use as the base component in the URL.
        entity_id : str
            The ID of the entity if there is one.
        related_component : str
            The related component to be appended to the ref URL.
        is_collection : bool
            Sets whether the related component is a collection or not.

        Returns
        -------
        str
            The entity's reference URL.
        """

        base_url = settings.PROXY_BASE_URL if settings.PROXY_BASE_URL is not None else f'{self.scheme}://{self.host}'
        base_url = f'{base_url}/{settings.ST_API_PREFIX}/v{self.version}'

        url_component = lookup_component(component if component else self.component, 'camel_singular', 'camel_plural')

        ref_url = f'{base_url}/{url_component}'

        if entity_id is not None:
            ref_url = f'{ref_url}({self.id_qualifier}{entity_id}{self.id_qualifier})'

        if related_component is not None:
            if is_collection is True:
                related_component = lookup_component(related_component, 'camel_singular', 'camel_plural')
            ref_url = f'{ref_url}/{related_component}'

        return ref_url

    def resolve_nested_resource_path(self, nested_resources):
        """"""

        entity = None
        replacement_id = None
        filter_id_string = None
        for nested_resource in nested_resources:
            if nested_resource[1] is not None:
                component = lookup_component(nested_resource[0], 'camel_singular', 'snake_singular')
                if 'temp_id' not in nested_resource[1]:
                    lookup_id = nested_resource[1].replace(self.id_qualifier, '')
                else:
                    lookup_id = entity[f'{component}_id']
                    replacement_id = lookup_id

                entity = next(iter(getattr(
                    self, f'get_{lookup_component(component, "snake_singular", "snake_plural")}'
                )(
                    expanded=True,
                    **{f'{component}_ids': [lookup_id]}
                )[0]), None)

                if not entity:
                    raise Http404

                filter_id_string = f'{nested_resource[0]}/id eq \'{lookup_id}\''

            else:
                filter_id_string = None

        return replacement_id, filter_id_string

    @staticmethod
    def get_filters(filter_string: str):
        """"""

        lexer = ODataLexer()
        parser = ODataParser()

        try:
            return parser.parse(lexer.tokenize(filter_string))
        except ParsingException:
            raise HttpError(422, 'Failed to parse filter parameter.')

    @staticmethod
    def get_ordering(query_params: dict):
        """"""

        order_by_string = query_params.get('order_by')

        if not order_by_string:
            order_by_string = ''

        ordering = [
            {
                'field': order_field.strip().split(' ')[0],
                'direction': 'desc' if order_field.strip().endswith('desc') else 'asc'
            } for order_field in order_by_string.split(',')
        ] if order_by_string != '' else []

        return ordering

    @staticmethod
    def get_pagination(query_params):
        """"""

        return {
            'skip': query_params['skip'] if query_params['skip'] is not None else 0,
            'top': query_params['top'] if query_params['top'] is not None else 100,
            'count': query_params['count'] if query_params['count'] is not None else False
        }

    def build_next_link(
            self,
            query_params: dict,
            length: int,
            count: Optional[int] = None
    ):
        """"""

        top = query_params.pop('top', None)
        skip = query_params.pop('skip', None)

        if top is None:
            top = 100

        if skip is None:
            skip = 0

        if count is not None and top + skip < count or count is None and top == length:
            query_string = ObservationParams(
                top=top,
                skip=top + skip,
                **query_params
            ).get_query_string()

            return f'{self.get_ref()}{query_string}'
        else:
            return None

    def build_selects_links_and_nested_components(
            self,
            request,
            component,
            values,
            expand,
            select=None,
            data_array=False,
            drop_related_links=False
    ):
        """
        The build_selects_links_and_nested_components function is used to build the self_link, related_component_links,
        and nested components for a given component. The function takes in the following parameters:

        :param self: Refer to the current object
        :param request: Get the query parameters from the request
        :param component: Determine which component is being queried
        :param values: Pass in the values that are returned from the list_entities function
        :param expand: Expand nested components
        :param select: Specify which fields should be returned in the response
        :param data_array: Determine whether the data should be returned in a dataarray format
        :param drop_related_links: Drop the related links from the response
        :return: A list of dictionaries
        """

        related_components = self.get_related_components(component)
        expand_properties = self.parse_expand_parameter(component, expand)
        unselect_components = self.parse_select_parameter(component, select)

        for value in values:
            value['uid'] = value['id']

            if select == 'self_link' or (len(unselect_components) == 0 and data_array is False):
                value['self_link'] = self.get_ref(
                    component=component,
                    entity_id=value['uid']
                )

            for unselect_component in unselect_components:
                value.pop(unselect_component, None)

            if data_array is False:
                for related_component, component_meta in related_components.items():
                    if related_component in expand_properties:
                        expand_properties[related_component]['join_ids'].append(
                            value[expand_properties[related_component]['join_field']]
                        )
                    elif related_component not in unselect_components:
                        value[f'{related_component}_link'] = self.get_ref(
                            component=component,
                            entity_id=value['uid'],
                            related_component=component_meta['component'],
                            is_collection=component_meta['is_collection']
                        ) if not drop_related_links else None

        if data_array is False:
            for expand_property_name, expand_property_meta in expand_properties.items():
                if len(expand_property_meta['join_ids']) > 0:
                    if expand_property_meta['join_field'] == 'uid':
                        join_field = lookup_component(
                            component, 'camel_singular', 'snake_singular'
                        ) + '_ids'
                    else:
                        join_field = expand_property_meta['join_field'] + 's'

                    apply_data_array = expand_property_meta['query_params'].get('result_format') == 'dataArray'

                    related_entities = {
                        entity.get('uid') if not apply_data_array else entity.get('datastream_id'): entity
                        for entity in self.list_entities(
                            request=request,
                            query_params=expand_property_meta['query_params'],
                            component=expand_property_meta['component'],
                            join_ids={
                                join_field: expand_property_meta['join_ids']
                            },
                            drop_related_links=True,
                            root=False
                        ).get('value')
                    }

                    for value in values:
                        if related_components[expand_property_name]['is_many_to_many']:
                            value[f'{expand_property_name}_rel'] = [
                                getattr(
                                    component_schemas, f'{expand_property_meta["component"]}GetResponse'
                                )(**related_entity).dict(
                                    by_alias=True,
                                    exclude_none=True
                                ) for related_entity in related_entities.values()
                                if value['uid'] in related_entity[join_field]
                            ]
                        elif related_components[expand_property_name]['is_collection']:
                            if apply_data_array:
                                del related_entities[value['uid']]['datastream']
                            value[f'{expand_property_name}_rel'] = [
                                getattr(
                                    component_schemas, f'{expand_property_meta["component"]}GetResponse'
                                )(**related_entity).dict(
                                    by_alias=True,
                                    exclude_unset=True
                                ) for related_entity in related_entities.values()
                                if related_entity[join_field[:-1]] == value['uid']
                            ] if not apply_data_array else ObservationDataArray(
                                **related_entities.get(value['uid'])
                            ).dict(
                                by_alias=True,
                                exclude_unset=True
                            )
                        else:
                            value[f'{expand_property_name}_rel'] = getattr(
                                component_schemas, f'{expand_property_meta["component"]}GetResponse'
                            )(**related_entities[
                                value[expand_property_meta['join_field']]
                            ]).dict(
                                by_alias=True,
                                exclude_none=True
                            )

        return values

    @staticmethod
    def get_related_components(component):
        """
        The get_related_components function returns a dictionary of related components for the given component.

        :param component: Get the related components of a specific component
        :return: A dict of related components
        """

        many_to_many_relations = {
            'Thing': ['Location'],
            'Location': ['Thing', 'HistoricalLocation'],
            'HistoricalLocation': ['Location']
        }

        return {
            name: {
                'component': field.type_.__name__,
                'is_collection': True if lookup_component(name, 'snake_singular', 'camel_singular') is None else False,
                'is_many_to_many': True if field.type_.__name__ in many_to_many_relations.get(component, []) else False
            } for name, field in getattr(component_schemas, f'{component}Relations').__fields__.items()
        }

    @staticmethod
    def parse_select_parameter(component, select_parameter):
        """
        The parse_select_parameter function takes in a component and a select_parameter.
        If the select_parameter is not None, it splits the parameter into an array of strings.
        It then creates an unselect_components list that contains all fields from the component's schema except for
        those that are in the select parameter (if any). If there are no fields specified in the select parameter, or if
        'id' is not included as one of them, it adds 'id' to this list as well.

        :param component: Determine which component schema to use
        :param select_parameter: Determine which fields are returned in the response
        :return: A list of components that should be unselected
        """

        if not select_parameter:
            return []

        select_parameter = select_parameter.split(',')

        unselect_components = [
            field[0] for field in getattr(component_schemas, component).__fields__.items()
            if field[1].alias not in select_parameter
        ]

        if len(select_parameter) > 0 and 'id' not in select_parameter:
            unselect_components.append('id')

        return unselect_components

    def parse_expand_parameter(self, component, expand_parameter):
        """
        The parse_expand_parameter function takes a component and an expand_parameter as input.
        The function returns a dictionary of related components that are to be expanded, with the following keys:
            - component: The name of the related component (e.g., 'Observation')
            - join_field: The field in the current table that is used to join with this related table (e.g., 'id' or
                          'observation_id')
            - query_params: A dictionary containing all query parameters for this specific nested request, including any
                            $expand parameters for further nesting.

        :param self: Represent the instance of the class
        :param component: Get the related components of a component
        :param expand_parameter: Expand the results of a query
        :return: A dictionary of the form:
        """

        if not expand_parameter:
            expand_parameter = ''
        expand_properties = {}
        expand_components = re.split(r',(?![^(]*\))', expand_parameter)
        related_components = self.get_related_components(component)

        for expand_component in expand_components:
            component_name = re.sub(r'(?<!^)(?=[A-Z])', '_', expand_component.split('/')[0].split('(')[0]).lower()
            if component_name not in related_components:
                continue

            nested_query_params = re.search(r'\(.*?\)', expand_component.split('/')[0])
            nested_query_params = nested_query_params.group(0)[1:-1] if nested_query_params else ''
            nested_query_params = {
                nested_query_param.split('=')[0]: nested_query_param.split('=')[1]
                for nested_query_param in nested_query_params.split('&') if nested_query_param
            }

            if component_name not in expand_properties:
                expand_properties[component_name] = {
                    'component': related_components[component_name]['component'],
                    'join_field': 'uid' if related_components[component_name]['is_collection'] else
                    lookup_component(
                        related_components[component_name]['component'], 'camel_singular', 'snake_singular'
                    ) + '_id',
                    'join_ids': [],
                    'query_params': nested_query_params
                }

            if len(expand_component.split('/')) > 1:
                expand_properties[component_name]['query_params']['$expand'] = ','.join(
                    (
                        *expand_properties[component_name]['query_params']['$expand'].split(','),
                        expand_component.split('/')[1],
                    )
                ) if '$expand' in expand_properties[component_name]['query_params'] else expand_component.split('/')[1]

        for expand_property in expand_properties.values():
            if expand_property['component'] == 'Observation':
                expand_property['query_params'] = ObservationParams(**expand_property['query_params']).dict()
            else:
                expand_property['query_params'] = ListQueryParams(**expand_property['query_params']).dict()

        return expand_properties

    @staticmethod
    def get_field_index(components, field):
        """
        The get_field_index function takes two arguments:
            1. components - a list of strings representing the fields in a CSV file
            2. field - the name of one of those fields

        :param components: Store the list of components in a row
        :param field: Find the index of a field in the components list
        :return: The index of the field in the components list
        """

        try:
            return components.index(field)
        except ValueError:
            return None

    def convert_to_data_array(
            self,
            response: dict,
            select: Union[str, None] = None
    ):
        """
        The convert_to_data_array function takes a response from the Observation entity and converts it to an array of
        observations. The function is called by the get_many method in the Observation class, which is used when
        querying multiple observations at once. The convert_to_data_array function groups all observations by their
        datastream id, and then creates a list of dictionaries containing each observation's phenomenon time (time) and
        result value (value). It also adds a 'datastream' key with its corresponding datastream id.

        :param self: Make the method belong to the class
        :param response: dict: Pass the response from the get_observations function
        :param select: Union[str: Select the fields that will be returned in the response
        :return: A dictionary with the following keys:
        """

        if select:
            selected_fields = [
                field[0] for field in ObservationDataArrayFields.__fields__.items()
                if field[1].alias in select.split(',')
            ]
        else:
            selected_fields = [
                field for field in ObservationDataArrayFields.__fields__ if field in ['phenomenon_time', 'result']
            ]

        response['value'] = [
            {
                'datastream_id': datastream_id,
                'datastream': self.get_ref('Datastream', datastream_id),
                'components': [
                    ObservationDataArrayFields.__fields__[field].alias for field in selected_fields
                ],
                'data_array': [
                    [
                        value for field, value in ObservationDataArrayFields(**observation).dict().items()
                        if field in selected_fields
                    ] for observation in observations
                ]
            } for datastream_id, observations in groupby(response['value'], key=lambda x: x['datastream_id'])
        ]

        return response

    @staticmethod
    def iso_time_interval(start_time: Optional[datetime], end_time: Optional[datetime]):
        """
        The iso_time_interval function takes two datetime objects as input and returns a string in the format
            start_time/end_time, where both times are formatted according to ISO 8601. If either of the inputs is None,
            then that time will be omitted from the output string.

        :param start_time: Optional[datetime]: Specify that the start_time parameter is optional
        :param end_time: Optional[datetime]: Specify that the end_time parameter is optional
        :return: A string that represents the time interval between two datetime objects
        """

        if start_time and end_time:
            return start_time.isoformat(timespec='seconds') + '/' + end_time.isoformat(timespec='seconds')
        elif start_time and not end_time:
            return start_time.isoformat(timespec='seconds')
        elif end_time and not start_time:
            return end_time.isoformat(timespec='seconds')
        else:
            return None


class SensorThingsRequest(HttpRequest):
    """
    The SensorThings request class.

    This class extends Django's HttpRequest class to include an engine class, component name, component path, and an
    entity_chain tuple. These attributes should be added to the request in the SensorThings middleware before calling a
    view function.
    """

    engine: SensorThingsBaseEngine
    auth: str
    component: str
    component_path: List[str]
    entity_chain: List[Tuple[str, Union[UUID, int, str]]]
    value_only: bool
