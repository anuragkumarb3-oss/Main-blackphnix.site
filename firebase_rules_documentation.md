# Firebase Security Rules (Version: 2026-01-29)

These rules enforce strict data ownership and administrative access.

## Collections

### Plans (`/plans`)
- **Read**: Publicly available.
- **Write**: Restricted to Admin users only.

### Users (`/users/{uid}`)
- **Read/Write**: Restricted to the owner of the UID.
- **Read**: Admins can read all user profiles.

### Domains (`/domains/{id}`)
- **Create**: Authenticated users can create, but `userId` MUST match their `uid`.
- **Read**: Users can read their own domains; Admins can read all.
- **Update/Delete**: Restricted to Admin users only.

### Orders (`/orders/{id}`)
- **Create**: Authenticated users can create, but `userId` MUST match their `uid`.
- **Read**: Users can read their own orders; Admins can read all.
- **Update/Delete**: Restricted to Admin users only.

### Tasks (`/tasks`)
- **Read**: Publicly available.
- **Write**: Restricted to Admin users only.

### System Logs (`/system`)
- **Read/Write**: Restricted to Admin users only.

## Default Policy
- All other paths are blocked by default.
