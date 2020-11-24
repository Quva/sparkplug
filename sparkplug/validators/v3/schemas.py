from ..v2.schemas import SchemasV2

from .process import processMetaDatas, processMeasurements, processMeasurementMessageSchema, processMetaDataMessageSchema
from .events import eventMetaDatas, eventMeasurements, eventMeasurementMessageSchema, eventMetaDataMessageSchema


class SchemasV3(SchemasV2):
    version = "v3"

    processMetaDatas = processMetaDatas
    processMetaDataMessageSchema = processMetaDataMessageSchema

    processMeasurements = processMeasurements
    processMeasurementMessageSchema = processMeasurementMessageSchema

    eventMetaDatas = eventMetaDatas
    eventMetaDataMessageSchema = eventMetaDataMessageSchema

    eventMeasurements = eventMeasurements
    eventMeasurementMessageSchema = eventMeasurementMessageSchema

    # TODO
    # Add recipe end points
