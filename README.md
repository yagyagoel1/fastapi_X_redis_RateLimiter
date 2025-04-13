
# FastAPI X Redis RateLimiter

This repository demonstrates how to implement multiple rate limiting strategies in a FastAPI application using Redis as a backend for storage and Poetry for dependency management. Rate limiting helps prevent abuse, distribute load evenly, and secure your API.

## Overview

Rate limiting is a crucial aspect of API development that protects resources from excessive use. This project implements several rate limiting strategies, including:

- **Fixed Window:** Limits the number of requests allowed during a fixed time window.
- **Sliding Window:** Provides a moving window approach for more granular control of request limits.
- **Token Bucket:** Uses tokens to allow bursts of traffic up to a certain limit, replenishing at a constant rate.

Redis is used to persist rate limiting state, making it effective for distributed systems.

## Features

- **FastAPI Integration:** Easily integrate rate limiting as middleware within a FastAPI application.
- **Redis Backend:** Leverages Redis for storing counters and tokens, ensuring consistency even in scaled environments.
- **Multiple Strategies:** Choose from fixed window, sliding window, or token bucket methods.
- **Poetry Managed:** Dependency management and reproducibility through Poetry.
- **Docker & Docker Compose:** Containerize the application and Redis backend for easy deployment and development setup.

## Prerequisites

- **Python 3.8+**  
- **Redis:** Ensure you have Redis installed and running if not using Docker. (See [Redis Documentation](https://redis.io/) for installation instructions.)
- **Poetry:** For managing dependencies.
- **Docker and Docker Compose:** Required for containerized deployment.

## Installation

### Clone the Repository

```bash
git clone https://github.com/yagyagoel1/fastapi_X_redis_RateLimiter.git
cd fastapi_X_redis_RateLimiter
```

### Install Dependencies with Poetry (Local Development)

```bash
poetry install
```

### Configure Redis

Adjust any settings in `redis_client.py` if needed (such as host, port, or authentication details).

## Running the Application

### Local Environment

Start the FastAPI app using Uvicorn:

```bash
uvicorn main:app --reload
```

The `--reload` flag enables auto-reloading during development. Once the server is up, you can test the API endpoints to see the rate limiting in action.

### Using Docker

To build and run the containers using Docker Compose, run:

```bash
docker-compose up --build
```

This command will build the FastAPI Docker image, start up both the FastAPI app and a Redis container, and map the appropriate ports for local access.

### YOU CAN TEST THE LIMITER AFTER STARTING HERE
```
http://localhost:8000/
```

## Project Structure

```
fastapi_X_redis_RateLimiter/
├── limiter/
│   ├── fixed_window.py      # Fixed window rate limiting strategy
│   ├── sliding_window.py    # Sliding window rate limiting strategy
│   └── token_bucket.py      # Token bucket rate limiting strategy
├── redis_client.py          # Redis connection setup
├── main.py                  # FastAPI application setup with middleware
├── sampleLimiter.py         # Sample usage for testing rate limiters
├── pyproject.toml           # Poetry project configuration file
├── poetry.lock              # Locked dependency versions for reproducibility
├── Dockerfile               # Docker configuration file for containerizing the app
└── docker-compose.yml       # Docker Compose file for containerized deployment
```

## How It Works

- **Middleware Integration:**  
  The FastAPI middleware intercepts every incoming HTTP request. It uses the token bucket limiter (or any other strategy) to check if the request’s originating IP (or client identifier) is within the allowed limits. If the limit is exceeded, a `429 Too Many Requests` response is returned. For example, the middleware in `main.py` looks like this:

  ```python
  @app.middleware("http")
  async def rate_limiting(request: Request, call_next):
      ok = tokenBucket.is_allowed(request.client.host)
      if not ok:
          return JSONResponse(status_code=429, content={"details": "Rate Limit Exceeded"})
      response = await call_next(request)
      return response
  ```

- **Rate Limiting Strategies:**  
  Each strategy is implemented in its respective file under the `limiter/` directory. This modular design allows you to easily extend or replace a strategy according to your needs.

## Extending the Project

- **Add New Strategies:** Create new modules in the `limiter/` folder and integrate them similarly.
- **Customize Limits:** Modify the initialization parameters in `main.py` to adjust the rate limits.
- **Logging and Monitoring:** Integrate logging to capture rate limit events for analysis.
- **Scale:** Ensure Redis is properly configured to handle distributed environments if deploying at scale.
