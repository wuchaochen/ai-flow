# AI Flow

## Introduction

AI Flow is an open source framework that bridges big data and artificial intelligence. It manages the entire machine learning project lifecycle as a unified workflow, including feature engineering, model training, model evaluation, model service, model inference, monitoring, etc. Throughout the entire workflow, users can choose to use the computing engine like Python, Flink etc.

In addition to the capability of orchestrating a group of batch jobs, by leveraging an event-based scheduler(enhanced version of Airflow), AI Flow also supports workflows that contain streaming jobs. Such capability is quite useful for complicate real-time machine learning systems as well as other real-time workflows in general.

## Features

You can use AI Flow to do the following:

![](https://raw.githubusercontent.com/wiki/flink-extended/ai-flow/images/functions.png)

1. Define the machine learning workflow including batch/stream jobs.

2. Manage metadata(generated by the machine learning workflow) of date sets, models, artifacts, metrics, jobs etc.

3. Schedule and run the machine learning workflow.

4. Publish and subscribe events

To support online machine learning scenarios, notification service and event-based schedulers are introduced.

AI Flow's current components are:

1. SDK: It defines how to build a machine learning workflow and includes the api of the AI Flow.

2. Notification Service: It provides event listening and notification functions.

3. Meta Service: It saves the meta data of the machine learning workflow.

4. Event-Based Scheduler: It is a scheduler that triggered jobs by some events happened.

## Documentation

### QuickStart

You can follow our [Quick Start](https://github.com/flink-extended/ai-flow/wiki/Quick-Start) to get your hands on AI Flow quickly. Besides, you can also take a look at our [Tutorial](https://github.com/flink-extended/ai-flow/wiki/Tutorial) to learn how to write your own workflow. You can use AI Flow according to the guidelines of. 

### API

Please refer to the [Python API](https://github.com/flink-extended/ai-flow/wiki/Python-API) to find the details of the API supported by AI Flow.

### Design

If you are interested in design principles of AI Flow, please see the [Design](https://github.com/flink-extended/ai-flow/wiki/Design) for more details.

### Examples

We have provided some examples of AI Flow to help you get a better understanding of how to write a workflow. Please see the [Examples](https://github.com/flink-extended/ai-flow/tree/master/examples/) directory.

## Reporting bugs

If you encounter any issues please open an issue in GitHub and we encourage you to provide a patch through GitHub pull request as well.

## Contribution

We happily welcome contributions to AI Flow. Please see our [Contribution](https://github.com/flink-extended/ai-flow/wiki/Contribution) for details.

## Contact Us

For more information, you can join the **AI Flow Users Group** on [DingTalk](https://www.dingtalk.com) to contact us. The number of the DingTalk group is `35876083`. 

You can also join the group by scanning the QR code below:

![](https://raw.githubusercontent.com/wiki/alibaba/flink-ai-extended/images/dingtalk_qr_code.png)
