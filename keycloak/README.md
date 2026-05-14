# Keycloak

Identity provider for Pentrius platform, handling user authentication and authorization.

## Overview

Keycloak manages:
- User registration and authentication
- OAuth2/OpenID Connect flows
- Role-based access control (RBAC)
- Realm configuration for Pentrius

## Configuration

Realm setup:
- **Realm**: pentrius
- **Client**: pentrius-frontend
- **Roles**: admin, pentester, viewer

## Development

```bash
# Start Keycloak
docker-compose -f keycloak/docker-compose.yml up -d

# Access admin console
http://localhost:8080/admin
```

## License

Apache License 2.0