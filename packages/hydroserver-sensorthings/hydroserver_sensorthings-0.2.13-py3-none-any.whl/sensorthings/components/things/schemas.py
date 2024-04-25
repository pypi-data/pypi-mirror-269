from typing import TYPE_CHECKING, Union, List, Optional
from pydantic import Field, AnyHttpUrl
from ninja import Schema
from sensorthings.schemas import BaseListResponse, BaseGetResponse, BasePostBody, BasePatchBody, EntityId, NestedEntity
from sensorthings.validators import allow_partial

if TYPE_CHECKING:
    from sensorthings.components.locations.schemas import Location
    from sensorthings.components.historicallocations.schemas import HistoricalLocation
    from sensorthings.components.datastreams.schemas import Datastream


class ThingFields(Schema):
    name: str
    description: str
    properties: Optional[dict] = None

    class Config:
        allow_population_by_field_name = True


class ThingRelations(Schema):
    locations: List['Location'] = []
    historical_locations: List['HistoricalLocation'] = []
    datastreams: List['Datastream'] = []


class Thing(ThingFields, ThingRelations):
    pass


class ThingPostBody(BasePostBody, ThingFields):
    locations: List[Union[EntityId, NestedEntity]] = Field(
        [], alias='Locations', nested_class='LocationPostBody'
    )
    historical_locations: List[NestedEntity] = Field(
        [], alias='HistoricalLocations', nested_class='HistoricalLocationPostBody'
    )
    datastreams: List[NestedEntity] = Field(
        [], alias='Datastreams', nested_class='DatastreamPostBody'
    )


@allow_partial
class ThingPatchBody(BasePatchBody, ThingFields):
    locations: List[EntityId] = Field([], alias='Locations')


@allow_partial
class ThingGetResponse(ThingFields, BaseGetResponse):
    locations_link: AnyHttpUrl = Field(None, alias='Locations@iot.navigationLink')
    locations_rel: List[NestedEntity] = Field(None, alias='Locations', nested_class='LocationGetResponse')
    historical_locations_link: AnyHttpUrl = Field(None, alias='HistoricalLocations@iot.navigationLink')
    historical_locations_rel: List[NestedEntity] = Field(
        None,
        alias='HistoricalLocations',
        nested_class='HistoricalLocationGetResponse'
    )
    datastreams_link: AnyHttpUrl = Field(None, alias='Datastreams@iot.navigationLink')
    datastreams_rel: List[NestedEntity] = Field(None, alias='Datastreams', nested_class='DatastreamGetResponse')


class ThingListResponse(BaseListResponse):
    value: List[ThingGetResponse]


class ThingGetResponseODM(ThingGetResponse):
    properties: str
