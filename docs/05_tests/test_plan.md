# Tests
ID | Test | Expected Result | Status
-----|----|------------------|-----------
T01 | Platform Setup | All tables created successfully and potentially populated | To be tested|
T02 | Initial Pipeline | Full load successful for all dw tables | To be tested|
T03 | Incremental Execution without new data | No duplicates | To be tested|
T04 | Creation of a new offer | New offer loaded | To be tested|
T05 | Update of an offer | Offer record updated (SCD1) | To be tested|
T06 | Creation of a new customer | New customer loaded | To be tested|
T07 | Update of a customer | Coherent SCD 2 historic | To be tested|
T08 | Temporary failure of a task | Retry working | To be tested|
T09 | Replay of the same batch | No duplicate | To be tested|
T10 | Failure during load | Reprise correcte | To be tested|
T11 | Failure of the pipeline | Coherent watermark | To be tested|
T12 | Restart Kafca consumer (service usage extractor) | Reprise Correct | To be tested|
