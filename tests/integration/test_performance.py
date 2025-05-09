import pytest
import asyncio
import time
from httpx import AsyncClient

@pytest.mark.asyncio
async def test_api_response_time():
    async with AsyncClient(base_url="http://localhost:8000") as client:
        start_time = time.time()
        response = await client.get("/api/status")
        end_time = time.time()
        
        assert (end_time - start_time) < 1.0  # Response under 1 second
        assert response.status_code == 200

@pytest.mark.asyncio
async def test_concurrent_requests():
    async with AsyncClient(base_url="http://localhost:8000") as client:
        tasks = [client.get("/api/status") for _ in range(5)]
        responses = await asyncio.gather(*tasks)
        assert all(r.status_code == 200 for r in responses)