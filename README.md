
Table of Contents
=================

 * [Quva Flow Technical Documentation](#quva-flow-technical-documentation)
   * [Sparkplug](#sparkplug)
     * [Installation](#installation)
     * [Usage](#usage)
   * [REST API](#rest-api)
     * [Message Header](#message-header)
     * [Message Reply Field](#message-reply-field)
     * [Variables Message](#variables-message)
     * [Event Message](#event-message)
     * [Feedback Message](#feedback-message)
   * [User Interface](#user-interface)

Quva® Flow Technical Documentation
==================================
Quva Flow is an engine that consists of services running data transfer, storage, analytics, and user interface. 

Sparkplug
---------
Sparkplug is an adapter program, licensed under [Apache License 2.0](https://github.com/Quva/sparkplug/blob/master/LICENSE.txt) for communicating with [Quva Flow](http://quva.fi/en/services/process-industry) REST API. Sparkplug currently supports sending messages as JSON and XML objects to our REST API. Sparkplug features a full suite of routines for validating the contents of the messages prior to sending them.


### Installation
Obtain sparkplug from the GitHub repository:
```
git clone https://github.com/Quva/sparkplug.git
```

Install prerequisites using pip:
```
pip install -r requirements.txt
```
after which go ahead and install sparkplug:
```
make clean build install
```
or, if you are missing `make`, call `setup.py` directly:
```
python setup.py clean build install
```


### Usage
Sending the message can be done using your favorite method that supports POST commands to REST API. However, sparkplug is the recommended one since it does input validation for all the messages, among other things.

To use Sparkplug, you specify the message to send; URL pointing to the ImportQueue of the service; sender ID as recognized by Quva Flow; and separate credentials for the REST API: 
```
sparkplug \
	  --payload message.json \
	  --url https://flow.quva.fi/<path>/<to>/<application>/api/ImportQueue?senderID=<mysenderid> \
	  --username $USERNAME \
	  --password $PASSWORD
```
If one is only interested in input validation, a.k.a dryrun, the following will do:
```
sparkplug \
	  --payload message.json \
	  --isDryrun
```

The XML message is sent similarly (sparkplug infers the format of the message with the suffix):
```
sparkplug \
	  --payload message.xml \
	  --url https://flow.quva.fi/<path>/<to>/<application>/api/ImportQueue?senderID=<mysenderid> \
	  --username $USERNAME \
	  --password $PASSWORD
```

In case you are wondering what the contents of the message is, read on!


REST API
--------
For now, there are two types of messages: Variables and Event. The former is used for declaring variables and their meta data, and the latter is used for declaring events. Both message types are currently supported by the Quva analytics service, but more will be added when needed.

### Message Container
Each message is enclosed in a container, the Message Container. The Message Container has the following fields:

 
| key            | type   | required  | comment               |
|----------------|--------|-----------|-----------------------|
| message_header | Object | YES       | Header of the message |
| message_body   | Object | YES       | Body of the message   |


The Message Container in JSON is expressed as:
```
{
  "message_header": {
    ...
  },
  "message_body": {
    ...
  }
}
```
In XML the Message Container is expressed as:
```
<message>
  <message_header>
    ...
  </message_header>
  <message_body>
    ...
  </message_body>
</message>
```

### Message Header
Every Message Container contains Message Header with the following fields:


| key                  | type   | required  | comment                                                                            |
|----------------------|--------|-----------|------------------------------------------------------------------------------------|
| message_type         | Enum   | YES       | Indicates which message it is. Supported types currently are: "variables", "event" |
| message_sender_id    | String | YES       | An ID that identifies the sender                                                   |
| message_recipient_id | String | YES       | An ID that identifies recipient (Quva)                                             |
| message_id           | String | NO        | An ID that uniquely identifies the message                                         |
| message_version      | String | YES       | Message version. Use "v2" for now.                                                 |

The Message Header takes the following form as JSON:
```
{
  "message_header": {
    "message_type": "<myevent>",
    "message_sender_id": "<mysenderid>",
    "message_recipient_id": "Quva",
    "message_id": "<myuniquemessageid>",
    "message_version": "v2"
  },
  "message_body": {
    ...
  }
}
```

### Variables Message
Variables Message is contained inside the message body of the container that has type "variables" like so:
```
{
  "message_header": {
    "message_type": "variables",
    "message_sender_id": "<mysenderid>",
    "message_recipient_id": "Quva",
    "message_id": "<myuniquemessageid>",
    "message_version": "v2"
  },
  "message_body": {
    "variables": [...]
  }
}
```
The list inside the "variables" field contains a list of objects with the following fields:

|               key    | type    | required  | comment                                                |
|----------------------|---------|-----------|--------------------------------------------------------|
| variable_source_id   | String  | YES       | Source identifier. |
| variable_name        | String  | YES       | Human-readable name for the variable. Does not have to be unique, i.e. multiple sources can share the same variable names. |
| variable_unit        | String  | NO        | Scientific unit (for example SI) for the variable      |
| variable_is_txt      | Boolean | YES       | Flag to denote whether the the variable should be treated as text or number. |
| variable_description | String  | YES       | A human-readable description, which is used in the UI. |
| variable_properties  | Map     | NO        | map of properties listed per variable, such as: origin table, site id, machine id, sensor id, etc. Can store at most 100 keys. |

Variables Message should be sent just once to the service so as to register them. Without registering the variables they are not stored in the database and thus cannot be surfaced in the frontend nor used by analytics applications. The message contains all the meta data for all the variables that are of interest regarding analysis. Below is an example how the JSON containing the aforementioned fields should be formatted:

```
{
  "message_header": {
    "message_type": "variables",
    "message_sender_id": "<mysenderid>",
    "message_recipient_id": "Quva",
    "message_id": "<myuniquemessageid>",
    "message_version": "v2"
  },
  "message_body": {
    "variables": [
      {
        "variable_unit": "m/s",
        "variable_is_txt": false,
        "variable_source_id": "factory_X",
        "variable_name": "tagABC"
        "variable_description": "Machine Speed"
        "variable_properties": {
          "source_table_field": "<fieldname>",
          "source_table": "<tablename>"
        }, 
      },
      {
      ...
      }
    ]
  }
}
```

Variable identifier consists of two pieces of information: the name (`variable_name`) and source (`variable_source_id`). A variable that has a specific name can come from multiple sources. This convention makes it possible to pool together data for a single variable coming from different sources, which may be beneficial for analytics.

The current interface supports at most 1 million variables.

### Event Message
Event Message is contained inside the message body of the container that has type "event" like so:
```
{
  "message_header": {
    "message_type": "event",
    "message_sender_id": "<mysenderid>",
    "message_recipient_id": "Quva",
    "message_id": "<myuniquemessageid>",
    "message_version": "v2"
  },
  "message_body": {
    "event": {...},
    "measurements": [...]
  }
}
```
Event Messages are sent when a new event happens, or an old one gets updated. The service can identify whether the event is new or re-entered based on `event_id`. General event information is stored in the field `event` and has the following fields in it: 

| key              | type   | required  | comment                                                      |
|------------------|--------|-----------|--------------------------------------------------------------|
| event_id         | String | YES       | Unique string for every event                                |
| event_type       | String | YES       | Groups similar events together                               |
| event_start_time | Date   | NO       | What is the start time of the event                          |
| event_stop_time  | Date   | NO       | What is the stop time of the event                           |
| event_properties | Map    | NO        | Map of properties for the event. Can store at most 100 keys. |

Along with the event information comes the measurements, given in a separate field `measurements`. Inside `measurements` there is a list of objects with the following fields:

| key                    | type   | required | comment                                  |
|------------------------|--------|----------|------------------------------------------|
| variable_name          | String | YES      | What is the name of the variable         |
| variable_source_id     | String | YES      | What is the source of the variable       |
| measurement_time       | Date   | YES      | When was the measurement taken           |
| measurement_num_value  | Double | NO       | What was the measured value. Needs to be set if variable_is_txt is False. |
| measurement_txt_value  | String | NO       | What was the measured value. Needs to be set if variable_is_txt is True. |
| measurement_properties | Map    | NO       | Map of the properties of the measurement. Can store at most 10 keys. |

Of these, `measurement_num_value` and `measurement_txt_value` are mutually exclusive and should be used according to how the variables are set in the Variables message (see `variable_is_txt` flag). Below is an example Event message in JSON format:

```
{
  "message_header": {
    "message_type": "event",
    "message_sender_id": "<mysenderid>",
    "message_recipient_id": "Quva",
    "message_id": "<myuniquemessageid>",
    "message_version": "v2"
  },
  "message_body": {
    "measurements": [
      {
        "measurement_time": "2014-12-30 00:00:00+0200",
        "variable_source_id": "<country>/<site>/<unit>", 
        "measurement_txt_value": "YES", 
        "variable_name": "Is sensor active?"
      }, 
      {
      ...
      }
    ],
    "event": {
      "event_id": "<myeventid>", 
      "event_stop_time": "yyyy-mm-dd HH:MM:SS+ZZZZ", 
      "event_start_time": "yyyy-mm-dd HH:MM:SS+ZZZZ", 
      "event_type": "<myeventtype>",
      "event_properties": {
        ...
      }
    }
  }
}
```
