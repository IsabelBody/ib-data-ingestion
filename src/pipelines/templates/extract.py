from typing import Dict, Any, List, Optional
from datetime import datetime, timedelta
import aiohttp
import asyncio
from utils.logger import logger

class DataExtractor:
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.session: Optional[aiohttp.ClientSession] = None
        self.rate_limit = config.get('rate_limit', 100)  # requests per minute
        self.retry_attempts = config.get('retry_attempts', 3)
        self.retry_delay = config.get('retry_delay', 5)  # seconds
    
    async def __aenter__(self):
        """Initialize aiohttp session."""
        self.session = aiohttp.ClientSession()
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Close aiohttp session."""
        if self.session:
            await self.session.close()
    
    async def fetch_data(self, start_date: datetime, end_date: datetime) -> List[Dict[str, Any]]:
        """Fetch data from the source API."""
        if not self.session:
            raise RuntimeError("Session not initialized. Use 'async with' context manager.")
        
        all_data = []
        current_date = start_date
        
        while current_date < end_date:
            try:
                # Implement rate limiting
                await asyncio.sleep(60 / self.rate_limit)
                
                # Fetch data for current date
                data = await self._fetch_page(current_date)
                all_data.extend(data)
                
                # Move to next date
                current_date += timedelta(days=1)
                
            except Exception as e:
                logger.error(
                    "Error fetching data",
                    source=self.config['source_name'],
                    date=current_date.isoformat(),
                    error=str(e)
                )
                raise
        
        return all_data
    
    async def _fetch_page(self, date: datetime) -> List[Dict[str, Any]]:
        """Fetch a single page of data."""
        for attempt in range(self.retry_attempts):
            try:
                # Implement your API call here
                # This is a template - replace with actual API implementation
                url = self.config['api_url']
                params = {
                    'date': date.isoformat(),
                    'api_key': self.config['api_key']
                }
                
                async with self.session.get(url, params=params) as response:
                    response.raise_for_status()
                    data = await response.json()
                    
                    # Add metadata
                    for item in data:
                        item['_metadata'] = {
                            'fetched_at': datetime.utcnow().isoformat(),
                            'source': self.config['source_name'],
                            'api_version': self.config.get('api_version', '1.0')
                        }
                    
                    return data
                    
            except aiohttp.ClientError as e:
                if attempt == self.retry_attempts - 1:
                    raise
                await asyncio.sleep(self.retry_delay * (attempt + 1))
            
            except Exception as e:
                logger.error(
                    "Unexpected error fetching data",
                    source=self.config['source_name'],
                    date=date.isoformat(),
                    error=str(e)
                )
                raise 