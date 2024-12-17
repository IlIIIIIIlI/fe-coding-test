# Real-time Chat Application

A real-time chat application built with FastAPI and WebSocket, featuring multi-client support, username-based messaging, and graceful disconnection handling. Got a similar project done in university time, written in Java: https://github.com/IlIIIIIIlI/Canvas_privateloveapp, using sockets.

## Features

- ✨ Real-time messaging with WebSocket
- 👥 Multiple client support
- 🔰 Username-based connections
- 📨 Message broadcasting
- ⚡ Automatic reconnection
- 📝 Comprehensive logging
- 🔄 Graceful disconnection handling

## Project Structure

```
chat-app/
├── main.py                 # Application entry point
├── app/                    # Core application code
│   ├── __init__.py
│   ├── core/              # Core configurations
│   │   ├── __init__.py
│   │   ├── config.py      # Application settings
│   │   └── logging.py     # Logging configuration
│   ├── api/               # API endpoints
│   │   ├── __init__.py
│   │   └── websocket.py   # WebSocket handlers
│   └── services/          # Business logic
│       ├── __init__.py
│       └── chat.py        # Chat management service
├── static/                # Static files
│   └── index.html        # Frontend interface
├── logs/                  # Log files directory
├── requirements.txt       # Python dependencies
├── Dockerfile            # Docker configuration
└── docker-compose.yml    # Docker Compose configuration
```

## Requirements Fulfillment

1. Multiple Client Connections

   - Implemented through `ConnectionManager` class
   - Maintains active connections in a dictionary
   - Each client gets a unique session

2. Message Broadcasting

   - Real-time message distribution to all connected clients
   - Username-prefixed messages
   - System notifications for join/leave events

3. Username Management

   - Username validation on connection
   - Duplicate username prevention
   - Username persistence throughout session

4. Disconnection Handling
   - Graceful connection cleanup
   - Automatic reconnection attempts
   - System notifications for disconnections

## Installation & Running

### Using Python directly (Development)

1. Create virtual environment

```bash
python -m venv webapp
source webapp/bin/activate  # Linux/Mac
webapp\Scripts\activate     # Windows
```

2. Install dependencies

```bash
pip install -r requirements.txt
```

3. Run the application

```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### Using Docker (Recommended for Production)

```bash
# Build and start containers
docker-compose up --build

# Run in background
docker-compose up -d
```

## Accessing the Application

Open your browser and navigate to:

```
http://localhost:8000/
```

## Viewing Logs

### Direct Python Run

```bash
# Access log
tail -f logs/access.log

# Error log
tail -f logs/error.log

# WebSocket log
tail -f logs/websocket.log
```

### Docker Environment

```bash
# All logs
docker-compose logs -f

# Specific logs
docker-compose exec chat tail -f /app/logs/access.log
docker-compose exec chat tail -f /app/logs/error.log
docker-compose exec chat tail -f /app/logs/websocket.log
```

## Screenshots

![alt text](image.png)
![alt text](image-1.png)
![alt text](image-2.png)
![alt text](image-3.png)

## Development

### Prerequisites

- Python 3.11+
- Docker & Docker Compose (optional)

## Monitoring

The application provides comprehensive logging with three main log files:

- `access.log`: HTTP request logging
- `error.log`: Error tracking
- `websocket.log`: WebSocket connections and messages

---

## Future Enhancements (TODO)

While the current implementation uses WebSocket for real-time communication, future enhancements might require Celery for handling background tasks:

### Potential Features Requiring Background Processing

1. Message Management

   - Chat history persistence
   - Message archiving
   - Old message cleanup
   - Chat digest generation

2. File Operations

   - File upload processing
   - Image resizing and optimization
   - Document format conversion
   - Media file compression

3. Notification System

   - Email notifications
   - Push notifications
   - Daily/Weekly digest emails
   - Offline message queuing

4. Analytics

   - Chat statistics generation
   - User activity reports
   - Usage pattern analysis
   - Performance metrics collection

5. Scheduled Tasks
   - Regular database cleanup
   - Periodic data backups
   - Cache management
   - System health checks

### Implementation Considerations

When implementing these features, the following architecture changes would be needed:

1. Infrastructure Additions

   - Message broker (Redis/RabbitMQ)
   - Celery workers
   - Result backend
   - Monitoring tools (Flower)

2. Code Structure

   ```python
   from celery import Celery

   # Celery configuration
   celery_app = Celery('chat_app',
                       broker='redis://localhost:6379/0',
                       backend='redis://localhost:6379/1')

   # Example background tasks
   @celery_app.task
   def send_chat_digest(user_email, messages):
       """Send daily chat digest to users"""
       pass

   @celery_app.task
   def process_uploaded_file(file_path):
       """Process and optimize uploaded files"""
       pass

   @celery_app.task
   def archive_chat_messages(room_id, date):
       """Archive old chat messages to database"""
       pass
   ```

3. Additional Dependencies
   ```
   celery==5.3.6
   redis==5.0.1
   flower==2.0.1
   ```
