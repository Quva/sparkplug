from ..v2.schemas import SchemasV2, liftFromV1toV2

from .process import processMeasurementMessageSchema, processMetadataMessageSchema
from .events import eventMeasurementMessageSchema, eventMetadataMessageSchema


class SchemasV3(SchemasV2):
    version = "v3"

    processMetadataMessageSchema = processMetadataMessageSchema

    processMeasurementMessageSchema = processMeasurementMessageSchema

    eventMetadataMessageSchema = eventMetadataMessageSchema

    eventMeasurementMessageSchema = eventMeasurementMessageSchema

    # TODO
    # Add recipe end points

    @classmethod
    def getSchemaForMessageType(cls, messageType):
        if messageType == "event":
            return cls.eventMessageSchema
        elif messageType == "variables":
            return cls.variablesMessageSchema
        elif messageType == "product":
            return cls.productMessageSchema
        elif messageType == "job":
            return cls.jobMessageSchema
        elif messageType == "message":
            return cls.messageSchema

        elif messageType == "process_measurements":
            return cls.processMeasurementMessageSchema
        elif messageType == "process_metadata":
            return cls.processMetadataMessageSchema
        elif messageType == "event_measurements":
            return cls.eventMeasurementMessageSchema
        elif messageType == "event_metadata":
            return cls.eventMetadataMessageSchema
        else:
            raise Exception("Unknown message type '{}' for schemas '{}'".format(messageType, cls))
            
    @classmethod
    def lift(cls, msg, logger=None):

        msgVersion = msg["message_header"].get("message_version", "v1")
        if msgVersion == "v3":
            if logger:
                logger.info("No need to lift, message is already v3")
            return msg

        if msgVersion == "v2":
            if logger:
                logger.info("No need to lift, message is already v3 is backwards compatible")
            return msg

        if msgVersion == "v1":
            return liftFromV1toV2(msg, logger=logger)
        else:
            if logger:
                logger.info("No rule to lift {} -> v2".format(msgVersion))
            return msg