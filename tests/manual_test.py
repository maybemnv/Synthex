import httpx
import asyncio

async def test_endpoints():
    async with httpx.AsyncClient() as client:
        # Test status
        response = await client.get('http://localhost:8000/api/status')
        print(f"Status: {response.status_code}")
        print(response.json())

        # Test explain
        explain_data = {
            "code": "def hello(): print('Hello')",
            "language": "python",
            "difficulty": "beginner"
        }
        response = await client.post(
            'http://localhost:8000/api/explain',
            json=explain_data
        )
        print(f"\nExplain: {response.status_code}")
        print(response.json())

if __name__ == "__main__":
    asyncio.run(test_endpoints())