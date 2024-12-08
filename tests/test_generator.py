import time
import pytest
from autocr_test.entrypoints.server import app
from httpx import AsyncClient

client = AsyncClient(app=app, base_url="http://localhost:8000")


async def test_cache_hit():
    response = await client.post("api/v1/generator/generate_review", json={
        "assignment_description": "In this assignment, your goal is to create a backend prototype for a Coding Assignment Auto-Review Tool using Python. This tool will help automate the process of revewing coding assignments by leveraging OpenAI's GPT API for code analysis and the GitHub API for repository access",
        "github_repo_url": "https://github.com/LbP22/AutoCR-test",
        "candidate_level": "middle"
    })
    assert response.status_code == 200
    resp = response.json()
    assert resp['cache_hit'] == False

    response = await client.post("api/v1/generator/generate_review", json={
        "assignment_description": "In this assignment, your goal is to create a backend prototype for a Coding Assignment Auto-Review Tool using Python. This tool will help automate the process of revewing coding assignments by leveraging OpenAI's GPT API for code analysis and the GitHub API for repository access",
        "github_repo_url": "https://github.com/LbP22/AutoCR-test",
        "candidate_level": "middle"
    })
    assert response.status_code == 200
    resp = response.json()
    assert resp['cache_hit'] == True


async def test_cache_miss():
    response = await client.post("api/v1/generator/generate_review", json={
        "assignment_description": "In this assignment, your goal is to create a backend prototype for a Coding Assignment Auto-Review Tool using Python. This tool will help automate the process of revewing coding assignments by leveraging OpenAI's GPT API for code analysis and the GitHub API for repository access",
        "github_repo_url": "htts://github.com/LbP22/AutoCR-test",
        "candidate_level": "middle"
    })
    assert response.status_code == 200

    response = await client.post("api/v1/generator/generate_review", json={
        "assignment_description": "Test",
        "github_repo_url": "https://github.com/LbP22/AutoCR-test",
        "candidate_level": "middle"
    })
    assert response.status_code == 200
    resp = response.json()
    assert resp['cache_hit'] == False