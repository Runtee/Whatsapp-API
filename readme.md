# Whatsapp API

This is a WhatsApp API implementation using Python Django. A part of the interview process for a Python backend engineer position at HYPERHIRE.

## Table of Contents

- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
- [Usage](#usage)
- [Folder Structure](#folder-structure)
- [API Endpoints](#api-endpoints)
- [Built With](#built-with)

## Getting Started

Download or clone the repository. Extract the folder and follow the instructions below.

### Prerequisites

You will need to install Python on your computer.

### Installation

```bash
# Example installation steps
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

## Usage

Explain how to use your project, provide examples, and include screenshots if applicable.

## Folder Structure

Describe the organization of your project's folders and files. Highlight important directories and their purposes.

```
project/
|-- auth_app/
|   |-- migrations/
|   |-- admin.py
|   |-- app.py
|   |-- models.py
|   |-- serializers.py
|   |-- test.py
|   |-- urls.py
|   |-- views.py
|-- chat/
|   |-- migrations/
|   |-- admin.py
|   |-- app.py
|   |-- consumers.py
|   |-- models.py
|   |-- routing.py
|   |-- serializers.py
|   |-- test.py
|   |-- urls.py
|   |-- views.py
|-- whatsapp/
|   |-- settings.py
|   |-- asgi.py
|   |-- wsgi.py
|   |-- urls.py
|-- manage.py
|-- README.md
```

## API Endpoints

### 1. Register User

#### Endpoint:
`POST /auth/register/`

#### Description:
Register a new user.

#### Request:
```bash
curl -X POST http://localhost:8000/auth/register/ -H "Content-Type: application/json" -d '{"username": "your_username", "password": "your_password"}'
```

#### Response:
```json
{
    "id": 1,
    "username": "your_username"
}
```

### 2. Log in User

#### Endpoint:
`POST /auth/login/`

#### Description:
Log in a user.

#### Request:
```bash
curl -X POST http://localhost:8000/auth/login/ -H "Content-Type: application/json" -d '{"username": "your_username", "password": "your_password"}'
```

#### Response:
```json
{
    "message": "Login successful"
}
```

### 3. Log out User

#### Endpoint:
`POST /auth/logout/`

#### Description:
Log out a user.

#### Request:
```bash
curl -X POST http://localhost:8000/auth/logout/ -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

#### Response:
```json
{
    "message": "Logout successful"
}
```

### 1. Create Chatroom

#### Endpoint:
`POST /create-chatroom/`

#### Description:
Create a new chatroom.

#### Request:
```bash
curl -X POST http://localhost:8000/create-chatroom/ -H "Content-Type: application/json" -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

#### Response:
```json
{
    "id": 1,
    "members": [],
    "type": "chat",
    "name": "Chatroom 1",
    "description": "This is a chatroom.",
    "created_by": 1,
    "created_at": "2023-12-01T12:00:00Z",
    "updated_at": "2023-12-01T12:00:00Z"
}
```

### 2. Join Chatroom

#### Endpoint:
`POST /join-chatroom/`

#### Description:
Join an existing chatroom.

#### Request:
```bash
curl -X POST http://localhost:8000/join-chatroom/ -H "Content-Type: application/json" -H "Authorization: Bearer YOUR_ACCESS_TOKEN" -d '{"chatroom_id": 1}'
```

#### Response:
```json
{
    "id": 1,
    "conversation": 1,
    "user": 2
}
```

### 3. List Chatrooms

#### Endpoint:
`GET /list-chatrooms/`

#### Description:
List the chat rooms the user is in.

#### Request:
```bash
curl -X GET http://localhost:8000/list-chatrooms/ -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

#### Response:
```json
[
    {
        "id": 1,
        "members": [],
        "type": "chat",
        "name": "Chatroom 1",
        "description": "This is a chatroom.",
        "created_by": 1,
        "created_at": "2023-12-01T12:00:00Z",
        "updated_at": "2023-12-01T12:00:00Z"
    },
    {
        "id": 2,
        "members": [],
        "type": "group",
        "name": "Group Chat",
        "description": "This is a group chat.",
        "created_by": 2,
        "created_at": "2023-12-02T12:00:00Z",
        "updated_at": "2023-12-02T12:00:00Z"
    }
]
```

### 4. Leave Chatroom

#### Endpoint:
`DELETE /leave-chatroom/<int:conversation_id>/`

#### Description:
Leave a chatroom.

#### Request:
```bash
curl -X DELETE http://localhost:8000/leave-chatroom/1/ -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

#### Response:
```json
{"message": "Leave chatroom successful"}
```

### 5. Send Message

#### Endpoint:
`POST /send-message/`

#### Description:
Send a message in a chatroom.

#### Request:
```bash
curl -X POST http://localhost:8000/send-message/ -H "Content-Type: application/json" -H "Authorization: Bearer YOUR_ACCESS_TOKEN" -d '{"conversation_id": 1, "text": "Hello, world!"}'
```

#### Response:
```json
{
    "id": 1,
    "conversation": 1,
    "sender": 2,
    "receivers": [],
    "attachment_picture": null,
    "attachment_video": null,
    "text": "Hello, world!",
    "created_at": "2023-12-01T12:00:00Z",
    "updated_at": "2023-12-01T12:00:00Z"
}
```

### 6. List Messages

#### Endpoint:
`GET /list-messages/`

#### Description:
Get user messages.

#### Request:
```bash
curl -X GET http://localhost:8000/list-messages/ -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

#### Response:
```json
[
    {
        "id": 1,
        "conversation": 1,
        "sender": 2,
        "receivers": [],
        "attachment_picture": null,
        "attachment_video": null,
        "text": "Hello, world!",
        "created_at": "2023-12-01T12:00:00Z",
        "updated_at": "2023-12-01T12:00:00Z"
    },
    {
        "id": 2,
        "conversation": 1,
        "sender": 1,
        "receivers": [],
        "attachment_picture": null,
        "attachment_video": null,
        "text": "Hi there!",
        "created_at": "2023-12-01T12:05:00Z",
        "updated_at": "2023-12-01T12:05:00Z"
    }
]
```

### 7. List Conversation Messages

#### Endpoint:
`GET /list-conversation-messages/<int:conversation_id>/`

####

 Description:
Get conversation messages a user is in.

#### Request:
```bash
curl -X GET http://localhost:8000/list-conversation-messages/1/ -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

#### Response:
```json
[
    {
        "id": 1,
        "conversation": 1,
        "sender": 2,
        "receivers": [],
        "attachment_picture": null,
        "attachment_video": null,
        "text": "Hello, world!",
        "created_at": "2023-12-01T12:00:00Z",
        "updated_at": "2023-12-01T12:00:00Z"
    },
    {
        "id": 2,
        "conversation": 1,
        "sender": 1,
        "receivers": [],
        "attachment_picture": null,
        "attachment_video": null,
        "text": "Hi there!",
        "created_at": "2023-12-01T12:05:00Z",
        "updated_at": "2023-12-01T12:05:00Z"
    }
]
```

### 8. Read Message

#### Endpoint:
`POST /read-message/`

#### Description:
Mark messages as read.

#### Request:
```bash
curl -X POST http://localhost:8000/read-message/ -H "Content-Type: application/json" -H "Authorization: Bearer YOUR_ACCESS_TOKEN" -d '{"conversation_id": 1, "message_ids": [1, 2]}'
```

#### Response:
```json
{"success": true}
```

---

## WebSocket Chat Consumer

This WebSocket consumer handles real-time chat functionality using Django Channels. Users can connect to specific chat rooms, send messages, and receive updates about typing status.

### Connect to WebSocket

Connect to the WebSocket by providing the `room_name` in the URL. The `room_name` corresponds to the `id` of the conversation.

### Endpoint

`ws/chat/<int:room_name>/`

### Example

```javascript
const roomName = 1; // Replace with the conversation ID
const socket = new WebSocket(`ws://your-domain/ws/chat/${roomName}/`);

socket.onopen = (event) => {
    console.log("WebSocket connection opened:", event);
};

socket.onmessage = (event) => {
    console.log("WebSocket message received:", event);
    const data = JSON.parse(event.data);

    // Handle different types of messages (e.g., message, typing)
    if (data.type === "message") {
        // Handle chat message
        console.log("Chat message:", data);
    } else if (data.type === "typing") {
        // Handle typing notification
        console.log("Typing notification:", data);
    }
};

socket.onclose = (event) => {
    console.log("WebSocket connection closed:", event);
};

// Send a message
const message = {
    type: "message",
    conversation: roomName,
    sender: 1, // Replace with the sender's user ID
    text: "Hello, world!",
};

socket.send(JSON.stringify(message));
```


### `connect`

The `connect` method is called when a client connects to the WebSocket. It adds the client to the room's group.

### `disconnect`

The `disconnect` method is called when a client disconnects from the WebSocket. It removes the client from the room's group.

### `receive`

The `receive` method is called when the server receives a message from a client. It handles different types of messages, such as chat messages and typing notifications.

### `handle_chat_message`

The `handle_chat_message` method processes and broadcasts chat messages to all clients in the room.

### `handle_typing_notification`

The `handle_typing_notification` method processes and broadcasts typing notifications to all clients in the room.

### `chat_message`

The `chat_message` method sends a chat message to all clients in the room.

### `typing_notification`

The `typing_notification` method sends a typing notification to all clients in the room.

## Usage

1. Connect to the WebSocket using the provided endpoint.
2. Send and receive messages in real-time.

## WebSocket URL Patterns

Configure Django to handle WebSocket connections by including the provided URL pattern in your project's `urls.py` file.

```python
from django.urls import path
from . import consumers

websocket_urlpatterns = [
    path("ws/chat/<int:room_name>/", consumers.ChatConsumer.as_asgi()),
]
```

Make sure to include this pattern in your routing configuration.

**Note:** Adjust the `room_name` in the URL to match the conversation or chat room you want to connect to.

---


## Built With

- [Django](https://www.djangoproject.com/)
- [Django REST Framework](https://www.django-rest-framework.org/)
- [Channels](https://channels.readthedocs.io/)
```