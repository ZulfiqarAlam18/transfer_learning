# API Reference - WhatsApp Limit Bot

## Table of Contents
- [Endpoints](#endpoints)
- [Environment Variables](#environment-variables)
- [Admin Commands](#admin-commands)
- [Data Structures](#data-structures)

---

## Endpoints

### GET /
**Description**: Health check endpoint

**Response**:
```json
{
  "status": "running",
  "service": "WhatsApp Limit Bot",
  "timestamp": "2026-01-16T10:30:00.000Z",
  "config": {
    "messageLimit": 5,
    "adminCount": 2,
    "activeUsers": 10,
    "bannedUsers": 0
  }
}
```

---

### GET /webhook
**Description**: Webhook verification endpoint for WhatsApp

**Query Parameters**:
- `hub.mode` (string, required): Should be "subscribe"
- `hub.verify_token` (string, required): Must match WEBHOOK_VERIFY_TOKEN
- `hub.challenge` (string, required): Challenge string to echo back

**Response**: Returns the challenge string if verification succeeds

**Example**:
```
GET /webhook?hub.mode=subscribe&hub.verify_token=verify123&hub.challenge=test123
```

---

### POST /webhook
**Description**: Receives WhatsApp messages and handles bot logic

**Headers**:
```
Content-Type: application/json
```

**Request Body** (WhatsApp format):
```json
{
  "entry": [{
    "changes": [{
      "value": {
        "messages": [{
          "from": "15551234567",
          "text": {
            "body": "Hello"
          },
          "context": {
            "group_id": "GROUP_ID"
          }
        }]
      }
    }]
  }]
}
```

**Response**: `200 OK`

**Behavior**:
1. Extracts message and sender info
2. Checks if sender is banned
3. Processes admin commands if from admin
4. Increments message count
5. Warns/removes user if limit exceeded

---

### GET /dashboard
**Description**: Web-based monitoring dashboard

**Response**: HTML page showing:
- Real-time message statistics
- Active users count
- Message counts per user
- List of banned users
- Current configuration

**Auto-refresh**: Every 30 seconds

---

## Environment Variables

### Required Variables

| Variable | Description | Example | Required |
|----------|-------------|---------|----------|
| `WHATSAPP_TOKEN` | WhatsApp Cloud API access token | `EAAxxxxxxxxxxxxx` | ✅ Yes |
| `PHONE_NUMBER_ID` | WhatsApp Business phone number ID | `123456789012345` | ✅ Yes |

### Optional Variables

| Variable | Description | Default | Example |
|----------|-------------|---------|---------|
| `WEBHOOK_VERIFY_TOKEN` | Token for webhook verification | `verify123` | `my_secret_token` |
| `PORT` | Server port | `3000` | `8080` |
| `MESSAGE_LIMIT` | Daily message limit per user | `5` | `10` |
| `ADMIN_NUMBERS` | Comma-separated admin phone numbers | `""` | `15551234567,15557654321` |

---

## Admin Commands

Commands must be sent via WhatsApp from a number listed in `ADMIN_NUMBERS`.

### /limit <number>

**Description**: Change the daily message limit

**Parameters**:
- `number` (integer, required): New message limit (must be > 0)

**Example**:
```
/limit 10
```

**Response**:
```
✅ Daily message limit updated to 10.
```

---

### /reset

**Description**: Reset all message counts to zero

**Parameters**: None

**Example**:
```
/reset
```

**Response**:
```
✅ All message counts have been reset.
```

---

### /stats

**Description**: Show current message statistics for all users

**Parameters**: None

**Example**:
```
/stats
```

**Response**:
```
📊 *Message Statistics*

🟢 15551234567: 3/5
🟢 15557654321: 2/5
🔴 15559876543: 6/5
```

Legend:
- 🟢 = Under limit
- 🔴 = Over limit

---

### /ban <phone_number>

**Description**: Permanently ban a user from sending messages

**Parameters**:
- `phone_number` (string, required): Phone number to ban (with country code)

**Example**:
```
/ban 15551234567
```

**Response**:
```
✅ 15551234567 has been banned.
```

**Behavior**: 
- User added to ban list
- Future messages ignored
- Optionally removed from group

---

### /unban <phone_number>

**Description**: Remove a user from the ban list

**Parameters**:
- `phone_number` (string, required): Phone number to unban

**Example**:
```
/unban 15551234567
```

**Response**:
```
✅ 15551234567 has been unbanned.
```

---

### /help

**Description**: Display list of available admin commands

**Parameters**: None

**Example**:
```
/help
```

**Response**:
```
📋 *Admin Commands*

/limit <number> - Change daily message limit
/reset - Reset all message counts
/stats - Show message statistics
/ban <number> - Ban a user
/unban <number> - Unban a user
/help - Show this help message

Current limit: 5 messages/day
```

---

## Data Structures

### dailyCount
**Type**: Object
**Description**: Stores message count for each user

```javascript
{
  "15551234567": 3,
  "15557654321": 5,
  "15559876543": 1
}
```

### bannedUsers
**Type**: Array
**Description**: List of banned phone numbers

```javascript
[
  "15551234567",
  "15559876543"
]
```

### groupInfo
**Type**: Object
**Description**: Stores information about WhatsApp groups

```javascript
{
  "GROUP_ID_123": {
    "id": "GROUP_ID_123",
    "name": "My WhatsApp Group"
  }
}
```

---

## WhatsApp API Integration

### Sending Messages

**Endpoint**: `https://graph.facebook.com/v20.0/{PHONE_NUMBER_ID}/messages`

**Method**: POST

**Headers**:
```
Authorization: Bearer {WHATSAPP_TOKEN}
Content-Type: application/json
```

**Body**:
```json
{
  "messaging_product": "whatsapp",
  "to": "15551234567",
  "text": {
    "body": "Your message here"
  }
}
```

### Removing User from Group

**Endpoint**: `https://graph.facebook.com/v20.0/{GROUP_ID}/participants`

**Method**: POST

**Headers**:
```
Authorization: Bearer {WHATSAPP_TOKEN}
Content-Type: application/json
```

**Body**:
```json
{
  "messaging_product": "whatsapp",
  "action": "remove",
  "participant": "15551234567"
}
```

---

## Error Handling

### Common Errors

**401 Unauthorized**
- Invalid or expired WHATSAPP_TOKEN
- Solution: Regenerate token in Meta Developer Console

**403 Forbidden**
- Webhook verification failed
- Solution: Check WEBHOOK_VERIFY_TOKEN matches

**400 Bad Request**
- Invalid phone number format
- Missing required fields
- Solution: Verify data format

**500 Internal Server Error**
- Server-side error
- Solution: Check server logs for details

---

## Rate Limits

### WhatsApp API Limits
- **Cloud API**: 80 messages/second per phone number
- **On-Premises API**: 1000 messages/second

### Bot Limits
- No artificial rate limiting by default
- Consider adding rate limiting for production

---

## Best Practices

1. **Token Security**: Never expose WHATSAPP_TOKEN in client code
2. **Error Handling**: Always wrap API calls in try-catch
3. **Logging**: Log important events for debugging
4. **Validation**: Validate admin commands before execution
5. **Testing**: Test in development environment before production

---

## Examples

### Complete Message Flow

1. User sends message to WhatsApp Business number
2. WhatsApp sends webhook POST to `/webhook`
3. Bot receives and parses message
4. Bot checks if user is banned → If yes, ignore
5. Bot checks if message is admin command → If yes, execute
6. Bot increments user's message count
7. Bot checks if count > limit → If yes, warn and remove
8. Bot responds with status code 200

### Admin Workflow

1. Admin sends `/limit 10` command
2. Bot receives message
3. Bot verifies sender is in ADMIN_NUMBERS
4. Bot parses command and validates parameter
5. Bot updates MESSAGE_LIMIT to 10
6. Bot sends confirmation message
7. New limit applies to all subsequent messages

---

## Troubleshooting

### Debug Mode

Add console logs to track message flow:

```javascript
console.log('Received message:', {
  from: messageData.from,
  text: messageData.text?.body,
  timestamp: new Date().toISOString()
});
```

### Test Webhook Locally

Use ngrok or localtunnel to expose local server:

```bash
ngrok http 3000
```

Then use the ngrok URL in Meta Developer Console.

---

## Version History

- **v1.0.0**: Initial release with core features
  - Message limiting
  - Auto-removal
  - Admin commands
  - Dashboard

---

For more information, see the main [README.md](README.md).
