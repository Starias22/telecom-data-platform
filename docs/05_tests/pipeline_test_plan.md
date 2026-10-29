# Data Pipeline Testing and Validatin Plan
ID | Test | Expected Result | Status
-----|----|------------------|-----------
T01 | Platform Setup | All tables (staging, dw, dq, ref and pipeline batch logs and watermark tables) created successfully and potentially populated | Passed |
T02 | Platform setup restart | Do not erase any database, table or data, but simply notify platform already setup | Passed |
T03 | Initial Pipeline | Full load successful for all dw tables, and initital metadata inserted or updated successfully, including watermark updated to the extraction start datetime | Passed |
T04 | Initial Pipeline restart| No duplicate and no error, do nothing,  but simply notify platform already initalized | Passed |
T05 | Incremental Execution of the Pipeline without new data | No duplicates and no error, no data loaded or processed, moved to saging or even extracted, existant raw data directory intact and not modified (idempotency), simply update (advance) watermark to the datetime the extraction process has started | Passed |
T06 | Creation of a new offer | New offer loaded into the datawarehouse with correct attributes | Passed |
T07 | Update the name of an offer (which is a SCD 1 attribute in dim_offer) | offer name updated to that new name for all records of of the concerned offer in dim_offer (SCD1) | Passed |
T08 | Update the end date of an offer configuration (which is a SCD 1 attribute in dim_offer) | offer end date updated to that new end date for the concerned record of offer configuration in dim_offer | Passed |
T09 | Creation of a new customer | One version of new customer loaded into dim_customer with correct attributes | Passed |
T10 | Update an SCD 2 attribute of a customer | Two versions of customers now available in dim_customer, all with correct attributes (the previous one closed and the new one current with the new value of the updated attribute) | Passed
T11 | Update an SCD 1 attribute of a customer (preferly the one of the previous test, so prerelery permor this test without rolling back the previous one) | The attribute updated in dim_customer for all versions of the concerned customer | Passed |
T12 | Purchase of an offer by a customer | Purchase loaded into purchase fact table with correct attributes | Passed |
T13 | New service usage events for a purchased offer accrosss multiple days | Events daily aggregated into the consumption fact table, with correct attributes, without error and without double count | Passed |
T14 | New service usage events including events with already existing record of (purchase, date) in the consumption fact table | Service usage indicator values aggregated and added to the aggregated value of their corresponding (purchase, date) in the consumption fact table | Passed |
T15 | Temporary failure of a task | Retry working | To be tested |
T16 | Replay of the same batch | No duplicate | To be tested |
T17 | Failure during load | Reprise corecte | To be tested |
T18 | Failure of the pipeline | Coherent watermark | To be tested |
T19 | Restart Kafka consumer (service usage extractor) or any other extractor | Reprise Correct pour lextractor conerne | To be tested |
T20 | Failure after partial processing | Une reprise correcte sans perte/rater de de donne , sans erreur et sans double comptabilisation | To be tested |
T21 | Data quality issues from source systems | Correctly handle the issue | To be tested |
error handling
logs
possibilite de continuer une tache echouee

