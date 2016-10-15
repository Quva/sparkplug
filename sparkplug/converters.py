from uuid import uuid1
import dateparser
import pytz

fieldMapping = {
    'event_property_date_key': 'Time_material_produced',
    'event_property_similarity_key': 'Product_global_code',
    'event_property_source_key': 'Prod_machine',
    'measurement_property_max_threshold_key': 'tolerance_max',
    'measurement_property_min_threshold_key': 'tolerance_min'
}

def convertMessageInPlace(message):
    
    messageType = message["message_header"]["message_type"]
    
    if messageType == "event":
        
        body = message["message_body"]["event"]
        eventID = body["event_id"]
        
        props = body.get("event_properties", {})
        
        # If event_produced_time is not present in the current message body,
        # and if it is found in the properties, we'll lift it into a regular field in the body
        eventProducedTimeVal_props = props.get(fieldMapping["event_property_date_key"], None)
        if ( eventProducedTimeVal_props is not None and
             body.get("event_produced_time", None) is None):
            body["event_produced_time"] = convertTime(eventProducedTimeVal_props)
            
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

def convertTime(ds):
    return dateparser.parse(ds).replace(tzinfo=pytz.UTC).strftime("%Y-%m-%d %H:%M:%S%z")
            
def convertMeasurementRow(measRow, eventID):

    if measRow.get("variable_id", None) is None:
        measRow["variable_id"] = "{}:{}".format(measRow["variable_source_id"],
                                                measRow["variable_name"])
        
        del measRow["variable_source_id"]
        del measRow["variable_name"]

    if measRow.get("event_id", None) is None:
        measRow["event_id"] = eventID
    
    measRow["measurement_time"] = convertTime(measRow["measurement_time"])

    if measRow.get("measurement_timeuuid", None) is None:
        measRow["measurement_timeuuid"] = str(uuid1())
    
    if measRow.get("measurement_threshold_min", None) is not None:
        measThresholdMin_props = props.get(fieldMapping["measurement_property_threshold_min_key"], None)
        if measThresholdMin_props is not None:
            measRow["measurement_threshold_min"] = measThresholdMin_props
            
    if measRow.get("measurement_threshold_max", None) is not None:
        measThresholdMax_props = props.get(fieldMapping["measurement_property_threshold_max_key"], None)
        if measThresholdMax_props is not None:
            measRow["measurement_threshold_max"] = measThresholdMax_props
                
    if measRow.get("measurement_target", None) is not None:
        measTarget_props = props.get(fieldMapping["measurement_property_target_key"], None)
        if measTarget_props is not None:
            measRow["measurement_target"] = measTarget_props
                    
    return measRow
                
