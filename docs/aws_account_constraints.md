# AWS Account Constraints

The AWS training account used for this project restricts
creation of AWS Glue resources.

## Tested Operations

| Operation | Result |
|---|---|
| GetCrawlers | PASS |
| GetDatabases | PASS |
| GetJobs | PASS |
| CreateCrawler | DENIED |
| CreateJob | DENIED |

## Error

AWS returned:

Account <account-id> is denied access.

The CreateCrawler operation was tested in:
- eu-north-1
- us-east-1

The same account-level denial was observed.

CreateJob was subsequently tested in eu-north-1
and produced the same account-level denial.

## Impact

AWS Glue Crawler and Glue Job execution cannot be
implemented using the available training account.

## Alternative Implementation

The project uses:

S3 → Python ETL → Processed S3 → Snowflake

while retaining AWS S3, SQS, SNS and Snowflake
integration.

Glue remains documented as the intended enterprise
implementation where the required account permissions
are available.