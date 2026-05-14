# Kong Gateway

API gateway for Pentrius platform, handling authentication, routing, and rate limiting.

## Overview

Kong serves as the edge proxy for all API requests, providing:
- JWT validation and authentication
- Route dispatching to backend services
- Rate limiting and throttling
- Plugin system for security headers

## Configuration

Key plugins enabled:
- `jwt` - JWT token validation
- `rate-limiting` - Request throttling
- `cors` - Cross-origin request handling
- `azp-check` - Audience validation for JWT tokens

## Development

```bash
# Start Kong
docker-compose -f kong/docker-compose.yml up -d

# Add routes
curl -X POST http://localhost:8001/apis \
  --data name=pentrius-backend \
  --data url=http://backend:8000 \
  --data strip_path=true \
  --data protocols=http,https
```

## License

Apache License 2.0