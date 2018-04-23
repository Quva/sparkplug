
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
Variables Message is contained inside the message body of the container like so:
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
    "variables": {
      "variable_data": [...]
    }
  }
}
```
The "variable_data" field contains a list of objects with the following fields:

|               key    | type    | required  | comment                                                |
|----------------------|---------|-----------|--------------------------------------------------------|
| variable_source_id   | String  | YES       | Source identifier. For example machine or factory ID. |
| variable_group       | String  | YES       | Variable group. Usually "PROCESS" or "QUALITY" |
| variable_name        | String  | YES       | Variable name or ID, corresponding to sensor ID in an automation system, for example. Does not have to be unique, i.e. multiple sources can share the same variable names. |
| variable_name_alias  | String  | NO        | Alternative variable name |
| variable_unit        | String  | NO        | Scientific unit (for example SI) for the variable      |
| variable_is_txt      | Boolean | YES       | Flag to denote whether the the variable should be treated as text or number. |
| variable_description | String  | YES       | A human-readable description, which is used in the UI. |
| variable_properties  | Map     | NO        | Map of additional, freely selected properties listed per variable, such as: source_table, site_id, machine_id, sensor_id, etc. Can store at most 100 keys. |

Variable identifier consists of two pieces of information: the source (`variable_source`) and name (`variable_name`). A variable that has a specific name can come from multiple sources. This convention makes it possible to pool together data for a single variable coming from different sources, which may be beneficial for analytics.

Each Variables Message should contain all the variable definitions related to one or more source (identified by `variable_source_id`). Variables for different sources can be sent in separate messages, but each message must contain all variables for that source. The API replaces old variables with new ones for all sources specified in `variable_source_id` fields in the message.

Variables should be sent at least once, when initially registering them to the system, and whenever they need to be added, removed or modified. The current interface supports at most 1 million variables.

Below is an example how the JSON containing the aforementioned fields should be formatted:

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
    "variables": {
      "variable_data": [
        {
          "variable_source_id": "<country>/<site>/<unit>",
          "variable_group": "PROCESS",
          "variable_name": "tag_1001",
          "variable_unit": "m/s",
          "variable_is_txt": false,
          "variable_description": "Machine Speed",
          "variable_properties": {
            "source_field": "tag_1001_avg_1min",
            "source_table": "historian_current"
          }
        },
        {
        ...
        }
      ]
    }
  }
}
```

### Event Message
Event Message is contained inside the message body of the container like so:
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
    "event": {
      "event_id": "<myeventid>",
      "event_type": "<myeventtype>",
      "event_properties": {...},
      "measurement_data": [...],
      "actions": {...}
    }
  }
}
```
Event Messages are sent when a new event happens, or an old one gets updated. The service can identify whether the event is new or re-entered based on `event_id`, which could correspond to a manufactured item, for example. If the process is continuous, lacking separable units, `event_id` could be a timestamp (such as "201804221815") that is simply used for labeling and transmitting a bunch of measurements within a time frame.

The `event` object of an Event Message contains following fields: 

| key              | type   | required  | comment                                                      |
|------------------|--------|-----------|--------------------------------------------------------------|
| event_id         | String | YES       | Unique string for every event                    |
| event_type       | String | YES       | Identifier for grouping similar events together  |
| event_start_time | Date   | NO        | Start time of the event                          |
| event_stop_time  | Date   | NO        | Stop time of the event                           |
| event_properties | Map    | NO        | Map of properties for the event. Can store at most 100 keys. |

Measurements are transmitted along with the event metadata, in a separate field `measurement_data`. Inside `measurement_data` there is a list of objects with the following fields:

| key                    | type   | required | comment                                  |
|------------------------|--------|----------|------------------------------------------|
| variable_source_id     | String | YES      | Variable source identifier       |
| variable_name          | String | YES      | Variable name                    |
| measurement_time       | Date   | YES      | Measurement time. ISO 8601 format with timezone field. |
| measurement_num_value  | Double | NO       | Measured value if `variable_is_txt` for the corresponding variable is False. |
| measurement_txt_value  | String | NO       | Measured value if `variable_is_txt` for the corresponding variable is True. |
| measurement_properties | Map    | NO       | Map of measurement properties. Can store at most 10 keys. |

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
    "event": {
      "event_id": "<myeventid>",
      "event_stop_time": "yyyy-mm-dd HH:MM:SS+ZZZZ",
      "event_start_time": "yyyy-mm-dd HH:MM:SS+ZZZZ",
      "event_type": "NEW_EVENT",
      "event_properties": {
        ...
      },
      "measurement_data": [{
        "measurement_time": "2014-12-30 00:00:00+0200",
        "variable_source_id": "<country>/<site>/<unit>",
        "variable_name": "tag_1001",
        "measurement_num_value": 13.856900
      },{
        "measurement_time": "2014-12-30 00:00:00+0200",
        "variable_source_id": "<country>/<site>/<unit>",
        "variable_name": "tag_1002",
        "measurement_num_value": null
      },{
        ...
      }],
      "actions": {
        "preclean_variable_groups": ["PROCESS"]
      }
    }
  }
}
```

The example above also contains an `actions` object, which is used for transmitting control commands to the API. Currently supported actions are:

 * `preclean_variable_groups`: Clear previously sent measurement data from the event. Should be used when retransmitting overlapping data -- even if the timestamps match exactly.

 * `request_analysis`: Run SPC analysis on the event. Other analyses and online prediction may be configured to run continuously without explicit requests.

 * `request_analysis_feedback`: Set to `true` to have the system send feedback message after finished SPC analysis.

