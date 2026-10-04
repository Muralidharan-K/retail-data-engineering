- Architecture
- S3 setup
- IAM/Storage Integration
- External Stage
- Snowpipe
- SQS notification
- Stream
- Task
- Error encountered: 11 vs 12 columns
- Resolution using explicit column mapping
- Validation results
- Final data-flow diagram

New CSV
   ↓
S3
   ↓
S3 ObjectCreated event
   ↓
SQS
   ↓
Snowpipe
   ↓
RAW +1,000
   ↓
Stream +1,000
   ↓
Scheduled Task detects data
   ↓
FACT +1,000
   ↓
Stream = 0