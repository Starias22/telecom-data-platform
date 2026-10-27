# Pipeline Test Plan
ID | Test | Expected Result | Status
-----|----|------------------|-----------
T01 | Platform Setup | All tables (staging, dw, dq, ref and pipeline batch logs and watermark tables) created successfully and potentially populated | Passed |
T02 | Platform setup restart | Do not erase any database, table or data, but simply notify platform already setup | Passed |
T03 | Initial Pipeline | Full load successful for all dw tables, and initital metadata inserted or updated successfully, including watermark updated to the extraction start datetime | Passed |
T04 | Initial Pipeline restart| No duplicate and no error, do nothing,  but simply notify platform already initalized | Passed |
T05 | Incremental Execution of the Pipeline without new data | No duplicates and no error, no data loaded or processed, moved to saging or even extracted, existant raw data directory intact and not modified (idempotency), simply update (advance) watermark to the datetime the extraction process has started | Passed |
T06 | Creation of a new offer | New offer loaded into the datawarehouse with correct attributes | Passed |
T07 | Update of an offer | Offer record updated in the datawarehouse (SCD1) | To be tested|
T08 | Creation of a new customer | New customer loaded | To be tested|
T09 | Update an SCD 1 attribute of a customer | The attribute updated for all versions of the customer | To be tested
T10 | Update an SCD 2 attribute of a customer | Coherent SCD 2 historic | To be tested
T11 | Purchase of an offer by a customer | Purchase loaded into purchase fact table with correct attributes | To be tested|
T12 | Service usage events for a purchased offer accrosss multiple days | Events daily aggregated into the consumption fact table, with correct attributes and without double count | To be testd |
T13 | Temporary failure of a task | Retry working | To be tested|
T14 | Replay of the same batch | No duplicate | To be tested|
T15 | Failure during load | Reprise corecte | To be tested|
T16 | Failure of the pipeline | Coherent watermark | To be tested|
T17 | Restart Kafka consumer (service usage extractor) or any other extractor | Reprise Correct pour lextractor conerne | To be tested|
