#############################
#       Variables
#############################
variable "aws_access_key" {}
variable "aws_secret_key" {}

#############################
#       Provider
#############################

provider "aws" {
  access_key = "${var.aws_access_key}"
  secret_key = "${var.aws_secret_key}"
  region = "us-east-1"
}


#############################
#       Data
#############################

data "archive_file" "get_status_zip" {
  type        = "zip"
  source_file = "${path.module}/../lambda/get_garage_status.py"
  output_path = "${path.module}/artifacts/get_garage_status.zip"
}

data "archive_file" "publish_open_sesame_zip" {
  type        = "zip"
  source_file = "${path.module}/../lambda/publish_open_sesame.py"
  output_path = "${path.module}/artifacts/publish_open_sesame.zip"
}

data "archive_file" "write_latest_status_trigger_zip" {
  type        = "zip"
  source_file = "${path.module}/../lambda/write_latest_status_trigger.py"
  output_path = "${path.module}/artifacts/write_latest_status_trigger.zip"
}

data "archive_file" "subscribe_write_to_dynamo_zip" {
  type        = "zip"
  source_file = "${path.module}/../lambda/subscribe_write_to_dynamo.py"
  output_path = "${path.module}/artifacts/subscribe_write_to_dynamo.zip"
}


#############################
#       Resources
#############################

########## IAM
resource "aws_iam_role" "garage_lambda_role" {
  name = "garage_lambda_role"
  assume_role_policy = <<EOF
{
"Version": "2012-10-17",
"Statement": [
    {
    "Action": "sts:AssumeRole",
    "Principal": {
        "Service": "lambda.amazonaws.com"
    },
    "Effect": "Allow",
    "Sid": ""
    }
]
}
EOF
}
resource "aws_iam_role_policy_attachment" "attach_dynamo" {
  role       = "${aws_iam_role.garage_lambda_role.name}"
  policy_arn = "arn:aws:iam::aws:policy/AmazonDynamoDBFullAccess"
}

resource "aws_iam_role_policy_attachment" "attach_apigateway" {
  role       = "${aws_iam_role.garage_lambda_role.name}"
  policy_arn = "arn:aws:iam::aws:policy/AmazonAPIGatewayInvokeFullAccess"
}

resource "aws_iam_role_policy_attachment" "attach_basic_lambda" {
  role       = "${aws_iam_role.garage_lambda_role.name}"
  policy_arn = "arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole"
}

resource "aws_iam_role_policy_attachment" "attach_iot" {
  role       = "${aws_iam_role.garage_lambda_role.name}"
  policy_arn = "arn:aws:iam::aws:policy/AWSIoTFullAccess"
}


########## Lambda
resource "aws_lambda_function" "get_garage_status" {
    filename = "${path.module}/artifacts/get_garage_status.zip"
    function_name = "get_garage_status"
    role = "${aws_iam_role.garage_lambda_role.arn}"
    handler = "lambda_handler"
    //Need to figure out why this function call fails
    //source_code_hash = "${filebase64sha256("${path.module}/artifacts/get_garage_status.zip")}"
    runtime = "python3.7"
}

resource "aws_lambda_function" "publish_open_sesame" {
    filename = "${path.module}/artifacts/publish_open_sesame.zip"
    function_name = "publish_open_sesame"
    role = "${aws_iam_role.garage_lambda_role.arn}"
    handler = "lambda_handler"
    runtime = "python3.7"
}

resource "aws_lambda_function" "write_latest_status_trigger" {
    filename = "${path.module}/artifacts/write_latest_status_trigger.zip"
    function_name = "write_latest_status_trigger"
    role = "${aws_iam_role.garage_lambda_role.arn}"
    handler = "lambda_handler"
    runtime = "python3.7"
}

resource "aws_lambda_function" "subscribe_write_to_dynamo" {
    filename = "${path.module}/artifacts/subscribe_write_to_dynamo.zip"
    function_name = "subscribe_write_to_dynamo"
    role = "${aws_iam_role.garage_lambda_role.arn}"
    handler = "lambda_handler"
    runtime = "python3.7"
}



