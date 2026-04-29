# Serverless URL Shortener (AWS)

A highly scalable, 100% serverless URL shortening service built with AWS Lambda, Amazon DynamoDB, and vanilla JavaScript. 

This project demonstrates cloud-native architecture by eliminating server provisioning (EC2), utilizing managed NoSQL databases for ultra-low latency redirection, and implementing a static analytics dashboard.

## Features
* **Zero-Server Architecture:** Runs entirely on AWS Lambda via a public Function URL.
* **Instant Redirection:** Uses DynamoDB partition keys ($O(1)$ lookup time) for lightning-fast HTTP 302 redirects.
* **Click Tracking:** Features atomic counters in the database to track real-time link engagement.
* **Compression Analytics:** The frontend dashboard locally tracks session history and calculates the exact percentage of string length reduced (easily compressing 300+ character URLs by 75%+).
* **CORS Managed Backend:** Secure, programmatic Cross-Origin Resource Sharing handled entirely within the Python logic.

## Architecture

* **Frontend:** Vanilla HTML/CSS/JS (Hosted locally or via GitHub Pages)
* **Compute:** AWS Lambda (Python 3.12)
* **Trigger:** AWS Lambda Function URL (RESTful API)
* **Database:** Amazon DynamoDB (NoSQL)

## API Reference

The backend exposes a single serverless endpoint handling multiple HTTP methods (Lambdalith pattern).

| Method | Path | Description |
| :--- | :--- | :--- |
| `POST` | `/` | Creates a new short URL. Expects JSON: `{"long_url": "..."}`. Returns the short link. |
| `GET` | `/{short_id}` | Looks up the original URL, increments the `clicks` counter, and returns an HTTP 302 Redirect. |
| `OPTIONS`| `/` | Handles browser pre-flight CORS requests. |

## AWS Setup Instructions

If you wish to deploy this architecture yourself:

1. **DynamoDB:** Create a table named `UrlMapping` with a Partition Key of `short_id` (String).
2. **IAM Role:** Ensure your Lambda execution role has the `AmazonDynamoDBFullAccess` policy attached.
3. **AWS Lambda:** * Create a Python 3.12 function.
   * Enable a **Function URL** with Auth Type: `NONE`.
   * **Crucial:** Disable the AWS Console CORS toggle, as the Python code handles CORS headers directly to prevent multiple-value header conflicts.
4. **Deploy:** Paste the contents of `lambda_function.py` into your function and update the `region_name` and `url_base` variables to match your deployment.

## Local Testing
To run the dashboard locally, simply open the `index.html` file in any modern web browser. No Node.js or build steps are required.
