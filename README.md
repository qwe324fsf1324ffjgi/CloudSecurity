Here's a **`README.md`** file for your project, with the **S3 public access check removed**, as requested. It includes a clean structure, overview, architecture, tech stack, deployment details, and usage instructions.

---

````markdown
# 🔒 Cloud Security Scout

Cloud Security Scout is a lightweight, serverless AWS security monitoring tool built with **AWS Lambda**, **DynamoDB**, **SES**, and **CloudFormation**. It automatically scans your AWS environment for critical misconfigurations and sends email alerts to help maintain compliance with the **CIS AWS Foundations Benchmark**.

---

## 🚀 Features

- Detects **insecure security group rules** (e.g., SSH/RDP open to the world).
- Flags **unencrypted RDS instances**.
- Stores findings in a **DynamoDB** table with timestamps.
- Sends **automated email alerts** using **Amazon SES**.
- Runs automatically every 6 minutes via **EventBridge rule**.
- Fully deployable with **AWS CloudFormation**.

---

## 🧱 Architecture

```text
 EventBridge (rate: 6 minutes)
           │
           ▼
     AWS Lambda Function
        /       |       \
   EC2 Check   RDS Check   DynamoDB Logging
           \       |
            ▼     ▼
        Email Alerts (SES)
````

---

## 🛠️ Tech Stack

* AWS Lambda (Python 3.9)
* Amazon EC2 (Security Group analysis)
* Amazon RDS (Encryption check)
* Amazon DynamoDB
* Amazon SES (Simple Email Service)
* AWS EventBridge (Scheduled execution)
* AWS CloudFormation (Infrastructure as Code)

---

## 📦 Deployment

> Prerequisites:
>
> * You must have a verified email in **Amazon SES** (in sandbox or production).
> * Upload your Lambda code as `index.zip` to the specified S3 bucket.

### Step 1: Package Your Lambda Function

```bash
zip -r index.zip index.py
aws s3 cp index.zip s3://your-bucket-name/
```

> Replace `your-bucket-name` in the template with the actual name.

### Step 2: Deploy CloudFormation Stack

```bash
aws cloudformation deploy \
  --template-file template.yaml \
  --stack-name CloudSecurityScout \
  --capabilities CAPABILITY_NAMED_IAM
```

---

## 📩 Email Alerts

Alerts are sent from and to the following email (ensure it's verified in SES):

* **Sender/Recipient:** `zerahabba1@gmail.com`

Each alert includes:

* Type of finding
* Affected resource
* Specific details

---

## 📊 Findings Stored in DynamoDB

Table: `CloudSecurityFindings`

Each item includes:

* `id`: Combination of finding type and resource
* `timestamp`: ISO-formatted UTC time
* `type`, `resource`, `details`

---

## ✅ CIS AWS Foundations Benchmark Coverage

This tool helps monitor for:

* **1.1** Avoid use of root account (indirect support via security group hardening)
* **4.1-4.3** Ensure RDS instances are encrypted
* **4.4-4.5** Security group auditing for restricted ports

---

## 📌 Note

* S3 bucket findings were **intentionally excluded** in this version.
* Ensure IAM roles and policies are correctly applied for Lambda execution.
* Run frequency is customizable via the `ScheduleExpression` in the EventBridge rule.

---

## 📤 Outputs

Upon deployment, CloudFormation outputs:

* Lambda function ARN
* DynamoDB table name
* SES notification configuration

---

## 🤝 Contributing

Pull requests are welcome! For major changes, please open an issue first to discuss what you’d like to change.

---

## 📜 License

MIT

---

## 🧠 Author

**Zerah Abba**
🔗 [LinkedIn](https://www.linkedin.com/in/zerah-abba)
💻 [GitHub](https://github.com/zerahabba1)
📧 [Send Email](https://mail.google.com/mail/?view=cm&fs=1&to=zerahabba1@gmail.com)

```

---

Let me know if you'd like:

- A GitHub Actions CI/CD workflow
- A PDF version of the README
- A project logo or architecture diagram image

Happy to help you make this fully production-ready or polished for recruiters!
```
