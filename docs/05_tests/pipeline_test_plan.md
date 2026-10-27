# Pipeline Test Plan
ID | Test | Expected Result | Status
-----|----|------------------|-----------
T01 | Platform Setup | All tables (staging, dw, dq, ref and pipeline batch logs and watermark tables) created successfully and potentially populated | Passed |
T02 | Platform setup restart | Do not erase any database, table or data, but simply notify platform already setup | Passed |
T03 | Initial Pipeline | Full load successful for all dw tables, and initital metadata inserted or updated successfully | Passed |
T04 | Initial Pipeline restart| No duplicate and no error, simply notify platform already initalized | To be tested |
T05 | Incremental Execution without new data | No duplicates and no error (idempotency) | To be tested|
T06 | Creation of a new offer | New offer loaded | To be tested|
T07 | Update of an offer | Offer record updated (SCD1) | To be tested|
T08 | Creation of a new customer | New customer loaded | To be tested|
T09 | Update of a customer | Coherent SCD 2 historic | To be tested
T10 | Purchase of an offer by a customer | Purchase loaded into purchase fact table with correct attributes | To be tested|
T11 | Service usage events for a purchased offer accrosss multiple days | Events daily aggregated into the consumption fact table, with correct attributes and without double count | To be testd |
T12 | Temporary failure of a task | Retry working | To be tested|
T13 | Replay of the same batch | No duplicate | To be tested|
T14 | Failure during load | Reprise corecte | To be tested|
T15 | Failure of the pipeline | Coherent watermark | To be tested|
T16 | Restart Kafka consumer (service usage extractor) or any other extractor | Reprise Correct pour lextractor conerne | To be tested|
