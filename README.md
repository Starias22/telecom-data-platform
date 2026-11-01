# Telecom Data Platform

## Project Overview

This is a batch-oriented data engineering platform designed to simulate data infrascturcture of a fictional Beninese telecommunications operator.

The platform integrates data from multiple operational systems into a staging area where it performs data quality checks, and consolidates the processed data into a centralized PostgreSQL data warehouse to support business intelligence and analitical use cases.

It handles different data formats and source systems, including relational databases, CSV files, Parquet files, and Kafka event streams consumed in batches.

The platform uses Python and Apache Airflow to manage and orchestrate batch workflows, PostgreSQL and SQL for data extraction from relational source systems, and processing, psql to execute database operations, and DuckDB to extract data from Parquet files.

## Table of Contents

- [Project Overview](#project-overview)
- [Business Context and Objectives](#business-context-and-objectives)
- [Data Architecture](#data-architecture)
- [Technology Stack](#technology-stack)
- [Data Sources](#data-sources)
- [Data Pipeline](#data-pipeline)
- [Data Warehouse](#data-warehouse)
- [Pipeline Orchestration](#pipeline-orchestration)
- [Analytical Use Cases](#analytical-use-cases)
- [Project Structure](#project-structure)
- [Installation and Execution](#installation-and-execution)
- [Future Improvements](#future-improvements)


## Business Context and Objectives

[Business Requirements](./docs/01_business_requirements/business_requirements.md)


## Data Architecture
![alt text](./docs/resources/data_pipeline.png)

## Technology Stack

## Data Sources
## Data Pipeline

## Data Warehouse

## Pipeline Orchestration

## Analytical Use Cases

## Project Structure

## Installation and Execution

## Future Improvements