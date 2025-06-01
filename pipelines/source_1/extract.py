import logging
from datetime import datetime
from typing import Dict, List, Any
import aiohttp
import asyncio

logger = logging.getLogger(__name__)

class DataExtractor:
    def __init__(self, credentials: Dict[str, str]):
        self.credentials = credentials
        self.session = None
        self.base_url = "https://api.example.com/v1"  # Replace with actual API URL

    async def __aenter__(self):
        """Set up aiohttp session."""
        self.session = aiohttp.ClientSession()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Clean up aiohttp session."""
        if self.session:
            await self.session.close()

    async def _make_request(self, endpoint: str, params: Dict[str, Any] = None) -> Dict:
        """Make an API request with authentication."""
        if not self.session:
            self.session = aiohttp.ClientSession()

        headers = {
            "Authorization": f"Bearer {self.credentials['client_secret']}",
            "Content-Type": "application/json"
        }

        async with self.session.get(
            f"{self.base_url}/{endpoint}",
            headers=headers,
            params=params
        ) as response:
            response.raise_for_status()
            return await response.json()

    async def fetch_data(self, start_date: datetime, end_date: datetime) -> List[Dict]:
        """Fetch data from the API for the specified date range."""
        logger.info(f"Fetching data from {start_date} to {end_date}")
        
        try:
            # Implement pagination and rate limiting
            all_data = []
            page = 1
            
            while True:
                params = {
                    "start_date": start_date.isoformat(),
                    "end_date": end_date.isoformat(),
                    "page": page,
                    "per_page": 100
                }
                
                data = await self._make_request("data", params)
                
                if not data.get("items"):
                    break
                    
                all_data.extend(data["items"])
                page += 1
                
                # Rate limiting
                await asyncio.sleep(1)
            
            logger.info(f"Fetched {len(all_data)} records")
            return all_data
            
        except Exception as e:
            logger.error(f"Error fetching data: {str(e)}")
            raise 