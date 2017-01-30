import dateutil.parser
import logging
import pytz
from uuid import uuid1

fieldMapping = {
    'event_property_date_key': 'Time_material_produced',
    'event_property_similarity_key': 'Product_global_code',
    'event_property_source_key': 'Prod_machine',
    'measurement_property_threshold_min_key': 'tolerance_min',
    'measurement_property_threshold_max_key': 'tolerance_max',
    'measurement_property_target_key': 'target',
    'variable_property_group_key' : 'variable_group'
}

def convertMessageInPlace(message):

    messageType = message["message_header"]["message_type"]
    
    if messageType == "event":
        
        body = message["message_body"]["event"]
        eventID = body["event_id"]
        
        props = body.get("event_properties", {})
        
        # Convert event_produced_time if defined
        eventProducedTimeVal_body = body.get("event_produced_time", None)
        if (eventProducedTimeVal_body is not None):
            body["event_produced_time"] = convertTime(eventProducedTimeVal_body)

        # If event_produced_time is not present in the current message body,
        # and if it is found in the properties, we'll lift it into a regular field in the body
        eventProducedTimeVal_props = props.get(fieldMapping["event_property_date_key"], None)
        if (eventProducedTimeVal_props is not None):
            # First convert the props field
            eventProducedTimeVal_props = convertTime(eventProducedTimeVal_props)
            props[fieldMapping["event_property_date_key"]] = eventProducedTimeVal_props
            # Set event_produced_time in the body if not yet defined
            if (eventProducedTimeVal_body is None):
                body["event_produced_time"] = eventProducedTimeVal_props

        # If product_id is not present in the current message body,
        # and if it is found in the properties, we'll lift it into a regular field in the body
        productID_props = props.get(fieldMapping["event_property_similarity_key"], None)
        if ( productID_props is not None and
             body.get("product_id", None) is None):
            body["product_id"] = productID_props
           
        # Convert measurements if measurements are defined and is a list:
        measurements = body.get("measurement_data", None)
        if measurements is not None and isinstance(measurements, list):
            body["measurement_data"] = list(map(lambda measRow: convertMeasurementRow(measRow,
                                                                                      eventID),
                                                measurements))

    elif messageType == "variables":

        body = message["message_body"]["variables"]

        # Convert measurements if measurements are defined and is a list:
        variables = body.get("variable_data", None)
        if variables is not None and isinstance(variables, list):
            body["variable_data"] = list(map(lambda varRow: convertVariableRow(varRow),
                                             variables))

def convertTime(ds):
    dt = dateutil.parser.parse(ds)
    # Default to UTC if timezone is not specified
    if dt.tzinfo is None or dt.tzinfo.utcoffset(dt) is None:
        logging.warning("Timezone not specified in timestamp '{}'. Defaulting to UTC"
                        .format(ds))
        dt = dt.replace(tzinfo=pytz.UTC)
    #logging.debug("Converted timestamp '{}' to '{}'".format(ds, dt))
    return dt.strftime("%Y-%m-%d %H:%M:%S%z")

def getVariableID(varSourceID, varName):
    return "{}:{}".format(varSourceID, varName)

def convertMeasurementRow(measRow, eventID):
    measRow["measurement_time"] = convertTime(measRow["measurement_time"])
    return measRow

def convertMeasurementRow_old(measRow, eventID):

    if measRow.get("variable_id", None) is None:
        measRow["variable_id"] = getVariableID(measRow["variable_source_id"],
                                               measRow["variable_name"])
        
        del measRow["variable_source_id"]
        del measRow["variable_name"]
    
    if measRow.get("event_id", None) is None:
        measRow["event_id"] = eventID
    
    measRow["measurement_time"] = convertTime(measRow["measurement_time"])

    if measRow.get("measurement_timeuuid", None) is None:
        measRow["measurement_timeuuid"] = str(uuid1())

    measProps = measRow.get("measurement_properties", {})
        
    if measRow.get("measurement_threshold_min", None) is None:
        measThresholdMin_props = measProps.get(fieldMapping["measurement_property_threshold_min_key"], None)
        if measThresholdMin_props is not None:
            measRow["measurement_threshold_min"] = float(measThresholdMin_props)
            
    if measRow.get("measurement_threshold_max", None) is None:
        measThresholdMax_props = measProps.get(fieldMapping["measurement_property_threshold_max_key"], None)
        if measThresholdMax_props is not None:
            measRow["measurement_threshold_max"] = float(measThresholdMax_props)
                
    if measRow.get("measurement_target", None) is None:
        measTarget_props = measProps.get(fieldMapping["measurement_property_target_key"], None)
        if measTarget_props is not None:
            measRow["measurement_target"] = float(measTarget_props)
                    
    return measRow
                
def convertVariableRow(varRow):
    
    if varRow.get("variable_id", None) is None:
        varRow["variable_id"] = getVariableID(varRow["variable_source_id"],
                                              varRow["variable_name"])

    if varRow.get("variable_group", None) is None:
        varGroup_prop = varRow.get("variable_properties", {})\
                              .get(fieldMapping["variable_property_group_key"], None)
        if varGroup_prop is not None:
            varRow["variable_group"] = varGroup_prop
        
    return varRow
