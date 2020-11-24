
from ..v1.schemas import SchemasV1
from .messages import messageReplySchema, messageHeaderSchema, messageSchema, messageBodySchema
from .products import productBodySchema, productMessageSchema
from .events import eventBodySchema, eventActionsSchema, eventMessageSchema
from .variables import variablesBodySchema, variableDataSchema, variablesMessageSchema, variableTranslationSchema
from .products import productBodySchema
from .measurements import measurementDataSchema
from .jobs import jobBodySchema, jobMessageSchema

import copy

class SchemasV2(SchemasV1):

    version = "v2"


    messageBodySchema = messageBodySchema
    messageReplySchema = messageReplySchema
    messageHeaderSchema = messageHeaderSchema
    messageSchema = messageSchema

    productBodySchema = productBodySchema
    productMessageSchema = productMessageSchema

    eventActionsSchema = eventActionsSchema
    eventBodySchema = eventBodySchema
    eventMessageSchema = eventMessageSchema

    variableTranslationSchema = variableTranslationSchema
    variableDataSchema = variableDataSchema
    variablesBodySchema = variablesBodySchema
    variablesMessageSchema = variablesMessageSchema

    measurementDataSchema = measurementDataSchema

    jobBodySchema = jobBodySchema
    jobMessageSchema = jobMessageSchema



    @classmethod
    def getSchemaForMessageType(schemas, messageType):
        if messageType == "event":
            return schemas.eventMessageSchema
        elif messageType == "variables":
            return schemas.variablesMessageSchema
        elif messageType == "product":
            return schemas.productMessageSchema
        elif messageType == "job":
            return schemas.jobMessageSchema
        elif messageType == "message":
            return schemas.messageSchema
        else:
            raise Exception("Unknown message type '{}' for schemas '{}'".format(messageType, schemas))


    @classmethod
    def lift(cls, msg, logger=None):

        msgVersion = msg["message_header"].get("message_version", "v1")

        if msgVersion == "v2":
            if logger:
                logger.info("No need to lift, message is already v2")
            return msg

        if msgVersion == "v1":
            return SchemasV2.__liftFromV1(msg, logger=logger)
        else:
            if logger:
                logger.info("No rule to lift {} -> v2".format(msgVersion))
            return msg

    @classmethod
    def __liftFromV1(cls, msg, logger=None):

        msgType = msg["message_header"]["message_type"]

        if msgType == "event":
            if logger:
                logger.info("Lifting message={} v1 -> v2".format(msgType))
            return SchemasV2.__liftEventFromV1(msg)
        else:
            if logger:
                logger.info("No rule to lift message={} v1 -> v2".format(msgType))



    @classmethod
    def __liftEventFromV1(cls, msg_c):

        msg = copy.deepcopy(msg_c)

        msg["message_header"]["message_version"] = "v2"

        msg["message_body"]["event"]["measurement_data"] = msg["message_body"].get("measurements", [])
        if msg["message_body"].get("measurements"):
            del msg["message_body"]["measurements"]

        return msg

