# Lambda Functions (λ)

## Publishing to the MQTT | publish_open_sesame.py
A lambda function is used to publish messages to the MQTT, that the pi is subscribed to. It will send either a "close" or "open" command for the pi to process. The pi will then process the payload and respond with an appropriate message, which the lambda function will also return.

It sends a message to `$aws/things/CarPen9000/door`


## Writing logs/results to Dynamo | subscribe_write_to_dynamo.py
A lambda function is used to write logs and the current status of the garage to Dynamo. This lambda should be configured to trigger (via lambda rules) when the Pi publishes to the MQTT. So, when the garage door successfully opens or closes, the pi will publish to the queue, and the lambda will trigger to update the state of the garage in Dynamo. The function returns the response from the Dynamo put action.

When defining the function under lambda, add an IoT trigger with custom rules.

```
  SELECT * FROM "$aws/things/CarPen9000/sensor"
```

## Getting the status of the garage | get_garage_status.py
A lambda function is used to get the last known good state of the garage by querying the Dynamo table. This will be used by the UI of the application as well as the Alexa skill. It returns a json object representing the state of the garage.

```
  SELECT * FROM "$aws/things/CarPen9000/askSensor"
```

## Getting the status of the garage | write_latest_status_trigger.py
A lambda function which acts as a trigger and updates the DynamoDB table with just the latest state in the record. Scan and query across lambda is not the most efficient, hence this lambda fetches the last state from the DB.
