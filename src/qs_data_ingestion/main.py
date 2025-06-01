#!/usr/bin/env python3
import argparse
import asyncio
import logging
from datetime import datetime, timedelta
from typing import Optional

from utils.logger import setup_logger
from utils.db import DatabaseConnection
from utils.security import CredentialManager
from utils.monitoring import MetricsCollector

logger = setup_logger(__name__)

class PipelineRunner:
    def __init__(self):
        self.credential_manager = CredentialManager()
        self.metrics_collector = MetricsCollector()
        self.db = DatabaseConnection()

    async def run_pipeline(self, source_name: str, start_date: Optional[datetime] = None, end_date: Optional[datetime] = None):
        """Run the ETL pipeline for a specific source."""
        try:
            logger.info(f"Starting pipeline for source: {source_name}")
            
            # Set default dates if not provided
            if not end_date:
                end_date = datetime.now()
            if not start_date:
                start_date = end_date - timedelta(days=1)

            # Import source-specific modules
            extract_module = __import__(f"pipelines.{source_name}.extract", fromlist=["DataExtractor"])
            transform_module = __import__(f"pipelines.{source_name}.transform", fromlist=["DataTransformer"])
            load_module = __import__(f"pipelines.{source_name}.load", fromlist=["DataLoader"])

            # Initialize pipeline components
            extractor = extract_module.DataExtractor(self.credential_manager.get_credentials(source_name))
            transformer = transform_module.DataTransformer()
            loader = load_module.DataLoader(self.db)

            # Execute pipeline
            raw_data = await extractor.fetch_data(start_date, end_date)
            transformed_data = transformer.transform(raw_data)
            load_result = await loader.load(transformed_data)

            # Record metrics
            self.metrics_collector.record_ingestion_metrics(source_name, {
                'records_processed': load_result.records_processed,
                'errors': len(load_result.errors)
            })

            logger.info(f"Pipeline completed for source: {source_name}")
            return load_result

        except Exception as e:
            logger.error(f"Pipeline failed for source {source_name}: {str(e)}")
            raise

async def main():
    parser = argparse.ArgumentParser(description="Run data ingestion pipeline")
    parser.add_argument("source", help="Name of the data source to ingest")
    parser.add_argument("--start-date", help="Start date (YYYY-MM-DD)", type=str)
    parser.add_argument("--end-date", help="End date (YYYY-MM-DD)", type=str)
    
    args = parser.parse_args()
    
    # Parse dates if provided
    start_date = datetime.strptime(args.start_date, "%Y-%m-%d") if args.start_date else None
    end_date = datetime.strptime(args.end_date, "%Y-%m-%d") if args.end_date else None
    
    runner = PipelineRunner()
    await runner.run_pipeline(args.source, start_date, end_date)

if __name__ == "__main__":
    asyncio.run(main()) 