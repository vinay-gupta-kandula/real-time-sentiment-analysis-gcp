# Real-time Sentiment Analysis Inference Pipeline (AWS)

## Project Overview

This project implements a **real-time sentiment analysis inference pipeline** using **serverless and event-driven architecture**. Text messages are published to a queue, automatically processed by a cloud function, and sentiment results are logged for monitoring and verification.

The original task specification was based on **Google Cloud Platform (GCP)** using Pub/Sub and Cloud Functions. Due to billing limitations, the same architecture and requirements have been **faithfully re-implemented on Amazon Web Services (AWS)** using equivalent services.

The system is designed to be scalable, fault-tolerant, and cost-efficient, following cloud best practices.

---

## Architecture

### Original (GCP – Task Specification)

| GCP Service     | Purpose                         |
| --------------- | ------------------------------- |
| Pub/Sub         | Message ingestion (text events) |
| Cloud Functions | Serverless sentiment inference  |
| Cloud Logging   | Logs and monitoring             |

### Implemented (AWS – Final Submission)

| AWS Service            | Purpose                                |
| ---------------------- | -------------------------------------- |
| Amazon SQS             | Message ingestion (queue-based events) |
| AWS Lambda             | Serverless sentiment inference         |
| Amazon CloudWatch Logs | Logging and monitoring                 |
| IAM                    | Secure permissions and execution roles |

**Architecture Flow:**

1. Text messages are published from a local script to **Amazon SQS**
2. SQS triggers an **AWS Lambda** function
3. Lambda performs sentiment analysis using **NLTK VADER**
4. Results are logged to **CloudWatch Logs**

---

## Project Structure

```
sentiment-analysis-aws/
│
├── publisher.py
├── publisher_requirements.txt
├── sample_texts.json
├── README.md
│
├── sentiment_analyzer/
│   ├── main.py
│   └── requirements.txt
│
├── tests/
│   └── test_sentiment.py
│
└── screenshots/
    ├── 01_lambda_function_overview.png
    ├── 02_sqs_trigger_configuration.png
    ├── 03_cloudwatch_logs_success.png
    ├── 04_local_publisher_output.png
    └── 05_local_tests_and_project_structure.png
```

---

## Core Components

### 1. Sentiment Analysis Lambda (`sentiment_analyzer/main.py`)

* Uses **NLTK VADER** for sentiment scoring
* Performs global model initialization (cold-start optimized)
* Classifies text as **POSITIVE**, **NEGATIVE**, or **NEUTRAL**
* Triggered automatically by SQS events

### 2. Publisher Script (`publisher.py`)

* Reads sample messages from `sample_texts.json`
* Publishes messages to Amazon SQS using **boto3**
* Configured using environment variables

### 3. Unit Tests (`tests/test_sentiment.py`)

* Tests sentiment classification logic
* Validates edge cases and input validation
* Executed locally using `unittest`

---

## Setup Instructions (AWS)

### Prerequisites

* Python **3.10**
* AWS Account
* AWS CLI installed
* IAM user with programmatic access

---

### AWS Configuration

1. Configure AWS CLI:

```bash
aws configure
```

* Default region: `us-east-1`
* Output format: `json`

2. Verify identity:

```bash
aws sts get-caller-identity
```

---

### AWS Resources Setup

#### Amazon SQS

* Queue Name: `sentiment-input`
* Type: Standard Queue

#### AWS Lambda

* Function Name: `sentiment-analyzer-function`
* Runtime: Python 3.10
* Trigger: Amazon SQS (`sentiment-input`)
* Batch size: 1

#### IAM Role

* Permissions:

  * `AWSLambdaBasicExecutionRole`
  * `AmazonSQSFullAccess` (or scoped send/receive permissions)

---

## Deployment

### Lambda Deployment

* Code deployed directly via AWS Console
* No external layers used
* Dependencies handled in local testing only

### Trigger Configuration

* SQS trigger enabled
* Event source mapping active

---

## Local Development & Testing

### Install Dependencies

```bash
pip install -r sentiment_analyzer/requirements.txt
pip install -r publisher_requirements.txt
```

### Run Unit Tests

```bash
python -m unittest discover -s tests
```

Expected output:

```
Ran 5 tests
OK
```

---

## Running the Pipeline

### Set Environment Variables (PowerShell)

```powershell
$env:AWS_REGION="us-east-1"
$env:SQS_QUEUE_URL="https://sqs.us-east-1.amazonaws.com/<ACCOUNT_ID>/sentiment-input"
```

### Publish Messages

```bash
python publisher.py
```

---

## Monitoring & Logs

### CloudWatch Logs

* Navigate to:

  * **CloudWatch → Log groups → /aws/lambda/sentiment-analyzer-function**
* Logs show:

  * Incoming text
  * Sentiment label
  * Sentiment scores
  * Execution duration and memory usage

---

## Screenshots Included

1. **Lambda Function Overview** – Deployment confirmation
2. **SQS Trigger Configuration** – Event-driven setup
3. **CloudWatch Logs** – Successful sentiment outputs
4. **Local Publisher Output** – Messages sent to SQS
5. **Local Tests & Project Structure** – Test validation

---

## Key Learnings

* Event-driven serverless architecture
* Cloud-native logging and monitoring
* Secure IAM-based access
* Dependency handling in AWS Lambda
* Translating architectures between cloud providers (GCP → AWS)

---

## Conclusion

This project successfully delivers a **real-time sentiment analysis inference pipeline** that meets all functional and architectural requirements of the original GCP-based task while being fully implemented on AWS. The solution demonstrates strong understanding of **serverless computing, messaging systems, testing, and monitoring**.

---

**Author:** Vinay
