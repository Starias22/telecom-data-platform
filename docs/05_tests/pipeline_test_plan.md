# Pipeline Test PLan
ID | Test | Expected Result | Status
-----|----|------------------|-----------
T01 | Platform Setup | All tables (staging, dw, dq, ref and pipeline batch logs and watermark tables) created successfully and potentially populated | Passed |
T02 | Pipeline setup restart | Do not erase any database, table or data, but simply notify platform already setup | To be tested |
T03 | Initial Pipeline | Full load successful for all dw tables, and initital metadata inserted or updated successfully | Passed |
T04 | Initial Pipeline restart| No duplicate and no error, simply notify platform already initalized | To be tested |
T05 | Incremental Execution without new data | No duplicates and no error (idempotency) | To be tested|
T06 | Creation of a new offer | New offer loaded | To be tested|
T07 | Update of an offer | Offer record updated (SCD1) | To be tested|
T08 | Creation of a new customer | New customer loaded | To be tested|
T09 | Update of a customer | Coherent SCD 2 historic | To be tested|
T10 | Temporary failure of a task | Retry working | To be tested|
T11 | Replay of the same batch | No duplicate | To be tested|
T12 | Failure during load | Reprise corecte | To be tested|
T13 | Failure of the pipeline | Coherent watermark | To be tested|
T14 | Restart Kafka consumer (service usage extractor) or any other extractor | Reprise Correct pour lextractor conerne | To be tested|
