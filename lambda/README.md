# lambda Functions

## Publishing to the MQTT | publish_lambda.py
A lambda function is used to publish messages to the MQTT that the pi is subscribed to. It will send either a "close" or "open" command for the pi to process. The pi will then process the payload and respond with an appropriate message, which the lambda function will also return.

## Writing logs/results to Dynamo | write_to_dynamo.py
A lambda function is used to write logs and the current status of the garage to Dynamo. This lambda should be configured to trigger (via lambda rules) when the Pi publishes to the MQTT. So, when the garage door succesfully opens or closes, the pi will publish to the queue, and the lambda will trigger to update the state of the garage in Dynamo. The function returns the response from the Dynamo put action.

## Getting the status of the garage | getStatus.py
A lambda function is used to get the last known good state of the garage by querying the Dynamo table. This will be used by the UI of the application as well as the Alexa skill. It returns a json object representing the state of the garage.
