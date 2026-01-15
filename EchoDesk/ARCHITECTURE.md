# EchoDesk Technical Architecture Specification

**Version:** 1.0
**Date:** 2026-01-15
**Status:** Design Phase

---

## Table of Contents

1. [System Overview](#system-overview)
2. [Architecture Principles](#architecture-principles)
3. [System Architecture](#system-architecture)
4. [Agent Protocol & Security](#agent-protocol--security)
5. [Automation Engine](#automation-engine)
6. [UI Architecture](#ui-architecture)
7. [AI Orchestration Layer](#ai-orchestration-layer)
8. [Data Models](#data-models)
9. [Deployment Architecture](#deployment-architecture)
10. [Scaling Strategy](#scaling-strategy)
11. [MVP Feature Prioritization](#mvp-feature-prioritization)
12. [Technology Stack](#technology-stack)

---

## System Overview

### Vision
EchoDesk is a local-first infrastructure command center that enables users to observe, control, automate, and orchestrate their digital and physical infrastructure.

### Core Capabilities
- **Observe**: Real-time monitoring of systems, services, and resources
- **Control**: Safe execution of commands and service management
- **Automate**: Rule-based and scheduled task execution
- **Orchestrate**: AI-powered workflow coordination
- **Extend**: Modular plugin system for hardware and service integration

### Target Environment
- Single-server or VM deployment (8-32GB RAM)
- Heterogeneous node fleet (Linux, Windows, macOS, ARM)
- VLAN-aware, firewall-friendly networking
- Docker-first deployment model
- Privacy-preserving, local-first operation

---

## Architecture Principles

### 1. Local-First
- All data stored locally by default
- No external dependencies for core functionality
- Optional cloud sync/backup

### 2. Modular Monolith
- Single deployable service with internal modularity
- Plugin-based extensibility
- Clear module boundaries without microservice complexity

### 3. Security-First
- Default-deny execution model
- RBAC for all operations
- Audit logging for all actions
- TLS everywhere
- Agent identity with rotating keys

### 4. Resilient Communication
- Agents tolerate server downtime
- Automatic reconnection
- Message queuing for reliability
- Health checks and heartbeats

### 5. Extensibility
- Plugin API for custom widgets
- Agent capability extensions
- Custom automation actions
- Integration adapters

---

## System Architecture

### High-Level Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                         EchoDesk Server                         │
│  ┌───────────────────────────────────────────────────────────┐  │
│  │                      Web Interface                        │  │
│  │  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐  │  │
│  │  │Dashboard │  │ Services │  │Automation│  │AI Control│  │  │
│  │  └──────────┘  └──────────┘  └──────────┘  └──────────┘  │  │
│  └───────────────────────────────────────────────────────────┘  │
│                                                                  │
│  ┌───────────────────────────────────────────────────────────┐  │
│  │                    API Gateway (FastAPI)                  │  │
│  │                  REST + WebSocket + SSE                   │  │
│  └───────────────────────────────────────────────────────────┘  │
│                                                                  │
│  ┌──────────────┬──────────────┬──────────────┬─────────────┐  │
│  │              │              │              │             │  │
│  │   Agent      │  Automation  │   Service    │  AI Agent   │  │
│  │  Manager     │   Engine     │  Discovery   │  Runtime    │  │
│  │              │              │              │             │  │
│  └──────────────┴──────────────┴──────────────┴─────────────┘  │
│                                                                  │
│  ┌───────────────────────────────────────────────────────────┐  │
│  │                   Core Services Layer                     │  │
│  │  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐  │  │
│  │  │ Metrics  │  │  Events  │  │   Auth   │  │   Audit  │  │  │
│  │  │  Store   │  │   Bus    │  │          │  │   Log    │  │  │
│  │  └──────────┘  └──────────┘  └──────────┘  └──────────┘  │  │
│  └───────────────────────────────────────────────────────────┘  │
│                                                                  │
│  ┌───────────────────────────────────────────────────────────┐  │
│  │                      Data Layer                           │  │
│  │    SQLite/Postgres  │  Secrets Store  │  File Storage    │  │
│  └───────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────┘
                              │
                    ┌─────────┼─────────┐
                    ▼         ▼         ▼
           ┌────────────┬────────────┬────────────┐
           │   Agent    │   Agent    │   Agent    │
           │  (Linux)   │ (Windows)  │  (macOS)   │
           └────────────┴────────────┴────────────┘
```

### Component Descriptions

#### 1. Web Interface (Frontend)
- **Technology**: React 18+ with TypeScript
- **UI Library**: shadcn/ui (Radix + Tailwind CSS)
- **State Management**: Zustand + React Query
- **Real-time**: WebSocket client + SSE
- **Routing**: React Router v6

**Module Structure**:
```
src/
├── features/
│   ├── dashboard/        # Widget system
│   ├── services/         # Service management
│   ├── automation/       # Automation builder
│   ├── ai/              # AI control panel
│   ├── nodes/           # Node management
│   └── settings/        # Configuration
├── components/
│   ├── ui/              # shadcn components
│   ├── widgets/         # Dashboard widgets
│   └── shared/          # Shared components
├── lib/
│   ├── api/             # API client
│   ├── websocket/       # WS connection
│   └── utils/           # Utilities
└── hooks/               # Custom React hooks
```

#### 2. API Gateway
- **Technology**: FastAPI (Python 3.11+)
- **Features**:
  - REST API for CRUD operations
  - WebSocket for real-time agent communication
  - SSE for UI event streaming
  - OpenAPI/Swagger docs
  - Request validation (Pydantic v2)
  - Rate limiting
  - CORS handling

#### 3. Agent Manager
**Responsibilities**:
- Agent registration and authentication
- Connection lifecycle management
- Command dispatch and response handling
- Agent capability discovery
- Health monitoring

**Key Features**:
- Maintains WebSocket connections to all agents
- Queues commands when agent offline
- Tracks agent capabilities and versions
- Handles agent upgrades

#### 4. Automation Engine
**Responsibilities**:
- Parse and validate automation rules
- Schedule time-based tasks
- React to event triggers
- Execute action sequences
- Manage state machines

**Architecture**: See [Automation Engine](#automation-engine) section

#### 5. Service Discovery
**Responsibilities**:
- Auto-detect Docker containers
- Discover system services
- Monitor service health
- Track dependencies

**Integration Points**:
- Docker API
- systemd D-Bus
- Windows Service API
- Process monitoring

#### 6. AI Agent Runtime
**Responsibilities**:
- Manage AI model connections (Ollama)
- Execute AI workflows
- Provide tool calling interface
- Maintain conversation context
- Manage prompt templates

**Architecture**: See [AI Orchestration Layer](#ai-orchestration-layer) section

#### 7. Core Services

**Metrics Store**:
- Time-series data collection
- Aggregation and downsampling
- Query interface
- Retention policies

**Events Bus**:
- Pub/sub messaging
- Event filtering
- Event persistence
- Webhook delivery

**Auth Service**:
- User authentication (local + optional LDAP/OIDC)
- Session management
- API key generation
- Permission enforcement

**Audit Log**:
- All action logging
- Immutable log storage
- Query and export
- Compliance reporting

---

## Agent Protocol & Security

### Agent Architecture

```
┌─────────────────────────────────────────┐
│           EchoDesk Agent                │
│  ┌───────────────────────────────────┐  │
│  │      Agent Core (Python)          │  │
│  │  - Connection Manager             │  │
│  │  - Authentication                 │  │
│  │  - Command Executor               │  │
│  │  - Metrics Collector              │  │
│  └───────────────────────────────────┘  │
│                                          │
│  ┌───────────────────────────────────┐  │
│  │      Capability Modules           │  │
│  │  ┌─────────┬─────────┬─────────┐  │  │
│  │  │ System  │ Docker  │ Custom  │  │  │
│  │  │  Info   │ Control │ Scripts │  │  │
│  │  └─────────┴─────────┴─────────┘  │  │
│  └───────────────────────────────────┘  │
│                                          │
│  ┌───────────────────────────────────┐  │
│  │      Security Sandbox             │  │
│  │  - Command allowlist              │  │
│  │  - Path restrictions              │  │
│  │  - Resource limits                │  │
│  └───────────────────────────────────┘  │
└─────────────────────────────────────────┘
```

### Communication Protocol

#### Transport Layer
- **Primary**: WebSocket over TLS (wss://)
- **Fallback**: HTTPS polling (if WebSocket blocked)
- **Port**: Single configurable port (default: 8443)

#### Message Format
```json
{
  "id": "msg_uuid_v4",
  "type": "command|response|event|heartbeat",
  "timestamp": "2026-01-15T10:30:00Z",
  "agent_id": "agent_uuid",
  "payload": {
    // Type-specific data
  },
  "signature": "hmac_sha256_signature"
}
```

#### Message Types

**1. Heartbeat** (Agent → Server, every 30s)
```json
{
  "type": "heartbeat",
  "agent_id": "agent_123",
  "payload": {
    "status": "healthy",
    "uptime": 86400,
    "capabilities": ["docker", "systemd", "metrics"],
    "version": "1.0.0"
  }
}
```

**2. Command** (Server → Agent)
```json
{
  "type": "command",
  "id": "cmd_456",
  "payload": {
    "action": "docker.container.restart",
    "params": {
      "container_id": "nginx_prod"
    },
    "timeout": 30,
    "user": "admin"
  }
}
```

**3. Response** (Agent → Server)
```json
{
  "type": "response",
  "id": "cmd_456",
  "payload": {
    "status": "success|error",
    "result": { /* action-specific result */ },
    "error": null,
    "duration_ms": 1234
  }
}
```

**4. Event** (Agent → Server, unsolicited)
```json
{
  "type": "event",
  "payload": {
    "event_type": "service.state_change",
    "data": {
      "service": "nginx",
      "old_state": "running",
      "new_state": "stopped"
    }
  }
}
```

**5. Metrics** (Agent → Server, every 60s)
```json
{
  "type": "metrics",
  "payload": {
    "cpu_percent": 45.2,
    "memory_used_gb": 12.8,
    "memory_total_gb": 32.0,
    "disk_used_gb": 120.5,
    "network_rx_mbps": 15.2,
    "network_tx_mbps": 8.1,
    "services": [
      {
        "name": "nginx",
        "status": "running",
        "cpu": 2.3,
        "memory_mb": 125
      }
    ]
  }
}
```

### Security Model

#### 1. Agent Registration Flow

```
Agent                           Server
  │                              │
  │  1. GET /api/v1/register    │
  │  + install_token            │
  │ ──────────────────────────► │
  │                              │
  │  2. Agent ID + API Key       │
  │  + Server Cert               │
  │ ◄────────────────────────── │
  │                              │
  │  3. WebSocket Connect        │
  │  + API Key Auth              │
  │ ──────────────────────────► │
  │                              │
  │  4. Challenge-Response       │
  │     Authentication           │
  │ ◄───────────────────────► │
  │                              │
  │  5. Connection Established   │
  │ ◄────────────────────────── │
```

**Registration Steps**:
1. Admin generates one-time install token in UI
2. Install token used to register agent (expires after use)
3. Server issues agent ID + long-lived API key
4. API key rotates every 90 days (automatic)
5. Old key valid for 24h grace period during rotation

#### 2. Authentication Methods

**WebSocket Authentication**:
- API key in initial handshake header: `Authorization: Bearer <api_key>`
- Challenge-response after connection to prove key possession
- Session token issued for connection lifetime

**Message Authentication**:
- All messages signed with HMAC-SHA256
- Signature key derived from API key
- Prevents message tampering

**TLS**:
- Server uses self-signed cert or Let's Encrypt
- Agents verify server cert fingerprint (pinning)
- Protects against MITM

#### 3. Authorization Model

**Role-Based Access Control (RBAC)**:

```
User Roles:
- admin: Full access
- operator: Control services, view all
- viewer: Read-only access
- automation: Service account for automated tasks

Agent Permissions:
- Each agent has assigned capabilities
- Capabilities define allowed actions
- Actions mapped to permission requirements

Permission Check:
user.role.permissions ∩ action.required_permissions ∩ agent.capabilities
```

**Example Permission Matrix**:
```
Action                    | Admin | Operator | Viewer | Required Agent Capability
--------------------------|-------|----------|--------|-------------------------
view.metrics              |   ✓   |    ✓     |   ✓    | metrics
view.services             |   ✓   |    ✓     |   ✓    | docker
control.container.restart |   ✓   |    ✓     |   ✗    | docker.control
control.container.delete  |   ✓   |    ✗     |   ✗    | docker.control
execute.script            |   ✓   |    ✗     |   ✗    | script.execute
manage.users              |   ✓   |    ✗     |   ✗    | (server-side)
```

#### 4. Command Execution Sandbox

**Multi-Layer Defense**:

**Layer 1: Command Allowlist**
```python
# Agent configuration
allowed_commands = {
    "docker": {
        "actions": ["ps", "inspect", "restart", "start", "stop"],
        "deny": ["rm", "rmi", "system prune"]
    },
    "systemctl": {
        "actions": ["status", "restart", "start", "stop"],
        "services": ["nginx", "postgres"],  # Allowlist
        "deny": ["shutdown", "reboot"]
    },
    "script": {
        "allowed_paths": ["/opt/echodesk/scripts"],
        "extensions": [".sh", ".py"]
    }
}
```

**Layer 2: Path Restrictions**
- Filesystem access limited to configured paths
- No access to sensitive directories (`/etc/shadow`, `/root/.ssh`)
- Read-only mounts where possible

**Layer 3: Resource Limits**
```python
resource_limits = {
    "cpu_percent": 25,      # Max CPU usage
    "memory_mb": 512,       # Max memory
    "timeout_seconds": 300, # Max execution time
    "max_output_kb": 1024   # Max output size
}
```

**Layer 4: User Context**
- Commands run as dedicated user (`echodesk-agent`)
- No root access by default
- Sudo only for explicitly approved commands

**Layer 5: Audit Logging**
- Every command logged before execution
- Output captured and logged
- Failed commands logged with reason

#### 5. Secrets Management

**Server Secrets**:
- Stored in encrypted SQLite table or separate secrets file
- Encrypted with key derived from master password
- Master password from environment variable or file

**Agent Secrets**:
- API keys never logged
- Stored in agent config file (chmod 600)
- Encrypted at rest with machine-specific key

**Secret References in Automation**:
```yaml
automation:
  - name: "Deploy with credentials"
    action: script.run
    params:
      script: "/opt/scripts/deploy.sh"
      env:
        API_KEY: "{{ secret.deployment_api_key }}"  # Template reference
```

#### 6. Network Security

**Firewall Rules**:
- Server: Only expose single HTTPS port (8443)
- Agents: Outbound only (no inbound ports required)
- Support for reverse proxy (Traefik, Nginx, Caddy)

**IP Allowlisting** (optional):
- Restrict agent connections by IP/subnet
- Useful for VLAN-segmented networks

**Rate Limiting**:
- Commands per agent: 60/minute
- API requests per user: 1000/minute
- Failed auth attempts: 5 per 15 minutes (lockout)

---

## Automation Engine

### Design Philosophy
- **Declarative**: Rules defined in YAML or UI
- **Reactive**: Trigger-based execution
- **Composable**: Actions chain together
- **Auditable**: Full execution history
- **Safe**: Validation before execution

### Automation Rule Structure

```yaml
automation:
  - id: auto_001
    name: "Restart nginx on failure"
    enabled: true
    triggers:
      - type: event
        event: "service.state_change"
        conditions:
          - field: "service"
            operator: "equals"
            value: "nginx"
          - field: "new_state"
            operator: "equals"
            value: "stopped"
    conditions:
      - type: time_range
        start: "00:00"
        end: "23:59"
      - type: custom
        expression: "counter.nginx_restarts < 3"
    actions:
      - type: agent.command
        agent: "server_01"
        command: "systemctl.restart"
        params:
          service: "nginx"
        retry:
          max_attempts: 3
          backoff: "exponential"
      - type: notification
        channel: "slack"
        message: "Nginx auto-restarted on {{ agent.name }}"
      - type: counter.increment
        counter: "nginx_restarts"
    on_error:
      - type: notification
        channel: "critical"
        message: "Failed to restart nginx!"
```

### Trigger Types

#### 1. Event Trigger
```yaml
triggers:
  - type: event
    event: "service.state_change"
    conditions:
      - field: "service"
        operator: "equals"
        value: "postgres"
```

**Available Events**:
- `agent.connected`
- `agent.disconnected`
- `service.state_change`
- `container.created`
- `container.stopped`
- `metric.threshold`
- `custom.*` (user-defined)

#### 2. Schedule Trigger
```yaml
triggers:
  - type: schedule
    cron: "0 2 * * *"  # Daily at 2 AM
    timezone: "America/New_York"
```

#### 3. Metric Threshold Trigger
```yaml
triggers:
  - type: metric_threshold
    metric: "agent.cpu_percent"
    agent: "server_01"
    operator: "greater_than"
    value: 80
    duration: "5m"  # Sustained for 5 minutes
```

#### 4. Webhook Trigger
```yaml
triggers:
  - type: webhook
    path: "/hooks/deploy"
    method: "POST"
    auth:
      type: "bearer_token"
      token: "{{ secret.webhook_token }}"
```

#### 5. Manual Trigger
```yaml
triggers:
  - type: manual
    # Executed only via UI or API call
```

### Condition Types

#### 1. Time Range
```yaml
conditions:
  - type: time_range
    start: "09:00"
    end: "17:00"
    days: ["monday", "tuesday", "wednesday", "thursday", "friday"]
```

#### 2. Agent State
```yaml
conditions:
  - type: agent_state
    agent: "server_01"
    state: "connected"
```

#### 3. Metric Comparison
```yaml
conditions:
  - type: metric
    metric: "agent.memory_used_percent"
    operator: "less_than"
    value: 90
```

#### 4. Custom Expression
```yaml
conditions:
  - type: expression
    expression: |
      agent.uptime > 86400 and
      service.nginx.status == "running"
```

### Action Types

#### 1. Agent Command
```yaml
actions:
  - type: agent.command
    agent: "server_01"
    command: "docker.container.restart"
    params:
      container: "app_production"
    timeout: 30
```

#### 2. Script Execution
```yaml
actions:
  - type: script.run
    agent: "server_01"
    script: "/opt/scripts/backup.sh"
    args: ["--full", "--compress"]
    env:
      BACKUP_TARGET: "{{ config.backup_path }}"
```

#### 3. HTTP Request
```yaml
actions:
  - type: http.request
    method: "POST"
    url: "https://api.example.com/deploy"
    headers:
      Authorization: "Bearer {{ secret.api_token }}"
    body:
      environment: "production"
      version: "{{ trigger.data.version }}"
```

#### 4. Notification
```yaml
actions:
  - type: notification
    channels: ["slack", "email"]
    message: |
      Service {{ trigger.data.service }} failed on {{ agent.name }}
      Status: {{ trigger.data.status }}
    severity: "warning"
```

#### 5. AI Agent Task
```yaml
actions:
  - type: ai.task
    agent: "troubleshooter"
    prompt: |
      Analyze why {{ trigger.data.service }} failed.
      Logs: {{ action.get_logs.result }}
    tools: ["search_logs", "check_metrics", "suggest_fixes"]
```

#### 6. Workflow
```yaml
actions:
  - type: workflow
    workflow_id: "deploy_staging"
    params:
      version: "{{ trigger.data.version }}"
```

### Action Chaining & Data Flow

```yaml
actions:
  - id: step1
    type: agent.command
    agent: "server_01"
    command: "docker.container.inspect"
    params:
      container: "app"
    output: "container_info"  # Store result

  - id: step2
    type: condition
    if: "{{ step1.container_info.status }} == 'running'"
    then:
      - type: agent.command
        command: "docker.container.restart"
    else:
      - type: notification
        message: "Container not running, cannot restart"

  - id: step3
    type: delay
    duration: "10s"

  - id: step4
    type: agent.command
    command: "docker.container.logs"
    params:
      container: "app"
      tail: 50
    output: "logs"

  - id: step5
    type: ai.task
    prompt: "Analyze these logs: {{ step4.logs }}"
```

### Execution Engine Architecture

```
┌─────────────────────────────────────────────────┐
│         Automation Execution Engine             │
│                                                  │
│  ┌────────────────────────────────────────────┐ │
│  │          Rule Loader & Validator           │ │
│  │  - Parse YAML                              │ │
│  │  - Validate syntax                         │ │
│  │  - Check permissions                       │ │
│  └────────────────────────────────────────────┘ │
│                                                  │
│  ┌────────────────────────────────────────────┐ │
│  │           Trigger Manager                  │ │
│  │  ┌──────────┬──────────┬──────────────┐   │ │
│  │  │ Schedule │  Event   │   Webhook    │   │ │
│  │  │ Executor │ Listener │   Handler    │   │ │
│  │  └──────────┴──────────┴──────────────┘   │ │
│  └────────────────────────────────────────────┘ │
│                                                  │
│  ┌────────────────────────────────────────────┐ │
│  │         Condition Evaluator                │ │
│  │  - Time checks                             │ │
│  │  - Metric queries                          │ │
│  │  - Expression parser                       │ │
│  └────────────────────────────────────────────┘ │
│                                                  │
│  ┌────────────────────────────────────────────┐ │
│  │          Action Executor                   │ │
│  │  - Sequential execution                    │ │
│  │  - Data flow between actions               │ │
│  │  - Error handling                          │ │
│  │  - Rollback support                        │ │
│  └────────────────────────────────────────────┘ │
│                                                  │
│  ┌────────────────────────────────────────────┐ │
│  │          Execution History                 │ │
│  │  - Store all executions                    │ │
│  │  - Result logging                          │ │
│  │  - Performance metrics                     │ │
│  └────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────┘
```

### Execution State Machine

```
        ┌─────────────┐
        │   Pending   │
        └──────┬──────┘
               │
        ┌──────▼──────┐
        │  Triggered  │
        └──────┬──────┘
               │
        ┌──────▼──────────┐
        │ Evaluating      │
        │ Conditions      │
        └──────┬──────────┘
               │
         ┌─────┴─────┐
         │           │
    ┌────▼────┐ ┌───▼────┐
    │ Execute │ │ Skipped│
    └────┬────┘ └────────┘
         │
    ┌────▼────────┐
    │  Running    │
    │  Actions    │
    └────┬────────┘
         │
    ┌────┴─────┐
    │          │
┌───▼───┐  ┌──▼───┐
│Success│  │Failed│
└───────┘  └──┬───┘
               │
        ┌──────▼──────┐
        │ On Error    │
        │ Actions     │
        └─────────────┘
```

### UI Builder

**Visual Automation Builder**:
- Drag-and-drop trigger selection
- Visual condition builder (no YAML required)
- Action sequence builder with data flow visualization
- Live validation and testing
- Template library

**Example UI Flow**:
```
[Trigger: Event] → [When: nginx stopped]
        ↓
[Condition: Time between 9 AM - 5 PM]
        ↓
[Action: Restart nginx]
        ↓
[Action: Send Slack notification]
        ↓
[On Error: Alert admin]
```

---

## UI Architecture

### Design System

**Component Library**: shadcn/ui + custom components
- Consistent styling with Tailwind
- Dark mode by default (light mode optional)
- Accessible (WCAG 2.1 AA)
- Responsive (mobile, tablet, desktop)

### Layout Structure

```
┌─────────────────────────────────────────────────────────┐
│  Header                                                  │
│  [Logo] [Search]              [Alerts] [User] [Settings]│
├───────┬─────────────────────────────────────────────────┤
│       │                                                  │
│ Side  │              Main Content Area                  │
│ Nav   │                                                  │
│       │  ┌──────────────────────────────────────────┐   │
│ Home  │  │                                           │   │
│ Nodes │  │                                           │   │
│ Svcs  │  │                                           │   │
│ Auto  │  │          Page Content                     │   │
│ AI    │  │                                           │   │
│ Logs  │  │                                           │   │
│       │  │                                           │   │
│       │  └──────────────────────────────────────────┘   │
│       │                                                  │
└───────┴─────────────────────────────────────────────────┘
```

### Dashboard Widget System

#### Widget Architecture

```typescript
// Widget definition interface
interface Widget {
  id: string;
  type: WidgetType;
  title: string;
  size: 'small' | 'medium' | 'large' | 'xlarge';
  position: { x: number; y: number };
  config: WidgetConfig;
  refreshInterval?: number;
}

// Widget types
enum WidgetType {
  SYSTEM_STATS = 'system_stats',
  SERVICE_STATUS = 'service_status',
  METRIC_CHART = 'metric_chart',
  AGENT_LIST = 'agent_list',
  RECENT_LOGS = 'recent_logs',
  AUTOMATION_STATUS = 'automation_status',
  QUICK_ACTIONS = 'quick_actions',
  CUSTOM = 'custom'
}

// Widget registry
interface WidgetRegistry {
  register(type: string, component: React.ComponentType<WidgetProps>): void;
  get(type: string): React.ComponentType<WidgetProps> | undefined;
  list(): WidgetDefinition[];
}
```

#### Grid System
- **Layout Engine**: react-grid-layout
- **Grid Units**: 12 columns × infinite rows
- **Sizes**:
  - Small: 3 cols × 2 rows
  - Medium: 6 cols × 3 rows
  - Large: 6 cols × 4 rows
  - XLarge: 12 cols × 4 rows
- **Responsive**: Breakpoints for mobile/tablet/desktop

#### Example Widgets

**1. System Stats Widget**
```typescript
interface SystemStatsConfig {
  agentId: string;
  metrics: ('cpu' | 'memory' | 'disk' | 'network')[];
  chartType: 'gauge' | 'line' | 'bar';
}
```

**2. Service Status Widget**
```typescript
interface ServiceStatusConfig {
  agentId: string;
  services: string[];  // Service names or 'all'
  showActions: boolean;  // Quick start/stop buttons
}
```

**3. Metric Chart Widget**
```typescript
interface MetricChartConfig {
  agentId: string;
  metric: string;
  timeRange: '1h' | '6h' | '24h' | '7d';
  chartType: 'line' | 'area' | 'bar';
  thresholds?: { warning: number; critical: number };
}
```

**4. Quick Actions Widget**
```typescript
interface QuickActionsConfig {
  actions: Array<{
    label: string;
    icon: string;
    command: {
      agentId: string;
      action: string;
      params: Record<string, any>;
    };
    confirmRequired: boolean;
  }>;
}
```

#### Dashboard Layouts

**Preset Layouts**:
1. **Overview** - High-level system health
2. **Services** - Focus on service status and logs
3. **Performance** - Metrics and charts
4. **Custom** - User-defined

**Layout Persistence**:
- Saved per user
- Exportable/importable
- Version controlled

### Page Modules

#### 1. Dashboard Page
- Widget grid
- Add widget button
- Layout selector
- Fullscreen mode
- Auto-refresh toggle

#### 2. Nodes Page
```
┌─────────────────────────────────────────────┐
│  Filters: [All] [Online] [Offline]          │
│  Sort: [Name] [Status] [CPU]                │
├─────────────────────────────────────────────┤
│                                              │
│  ┌──────────────────────────────────────┐   │
│  │ Node: server-01        [Online] 🟢  │   │
│  │ OS: Ubuntu 22.04       CPU: 45%     │   │
│  │ IP: 192.168.1.10       RAM: 12/32GB │   │
│  │                                      │   │
│  │ [View Details] [Shell] [Restart]    │   │
│  └──────────────────────────────────────┘   │
│                                              │
│  ┌──────────────────────────────────────┐   │
│  │ Node: pi-01            [Online] 🟢  │   │
│  │ OS: Raspberry Pi OS    CPU: 12%     │   │
│  │ ...                                  │   │
│  └──────────────────────────────────────┘   │
└─────────────────────────────────────────────┘
```

**Features**:
- Node list/grid view
- Real-time status
- Quick actions
- Node detail modal
- Agent installation guide

#### 3. Services Page
```
┌─────────────────────────────────────────────┐
│  Filters: [All Services] [Node: All]        │
│  Search: [__________________]               │
├─────────────────────────────────────────────┤
│                                              │
│  Service Name    │ Node      │ Status │ CPU │
│  ───────────────┼───────────┼────────┼─────│
│  nginx          │ server-01 │🟢 Up   │ 2%  │
│  postgres       │ server-01 │🟢 Up   │15%  │
│  app_container  │ server-01 │🔴 Down │ 0%  │
│  ollama         │ server-02 │🟢 Up   │35%  │
│                                              │
└─────────────────────────────────────────────┘
```

**Features**:
- Service discovery (Docker, systemd, etc.)
- Start/stop/restart controls
- Logs viewer
- Dependency graph
- Health checks

#### 4. Automation Page
```
┌─────────────────────────────────────────────┐
│  [+ New Automation]         [Import]        │
├─────────────────────────────────────────────┤
│                                              │
│  ┌──────────────────────────────────────┐   │
│  │ Restart nginx on failure     [✓] On  │   │
│  │ Trigger: service.state_change        │   │
│  │ Last run: 2 hours ago | Success      │   │
│  │                                      │   │
│  │ [Edit] [Duplicate] [Logs] [Delete]  │   │
│  └──────────────────────────────────────┘   │
│                                              │
│  ┌──────────────────────────────────────┐   │
│  │ Nightly backup           [✓] On      │   │
│  │ Trigger: schedule (2 AM daily)       │   │
│  │ Last run: 5 hours ago | Success      │   │
│  │ ...                                  │   │
│  └──────────────────────────────────────┘   │
└─────────────────────────────────────────────┘
```

**Automation Builder**:
- Visual flow builder
- YAML editor toggle
- Test execution
- Execution history
- Template library

#### 5. AI Control Panel
```
┌─────────────────────────────────────────────┐
│  Model: [llama3.2:latest ▼]    [Settings]  │
├───────────┬─────────────────────────────────┤
│           │                                  │
│ Templates │  Chat Interface                 │
│           │                                  │
│ Deploy    │  User: Deploy the staging app   │
│ Debug     │                                  │
│ Monitor   │  AI: I'll deploy staging for you│
│ Backup    │                                  │
│           │  [Deploying...]  [View Logs]    │
│ + New     │                                  │
│           │  User: [____________]  [Send]   │
│           │                                  │
├───────────┼─────────────────────────────────┤
│ Sessions  │  Tools Used: docker.deploy,     │
│           │  systemctl.restart              │
│ Today     │  Duration: 12.5s                │
│ Yesterday │                                  │
│ Last Week │                                  │
└───────────┴─────────────────────────────────┘
```

**Features**:
- Chat interface
- Prompt templates
- Tool execution log
- Session history
- Model management

#### 6. Logs & Events Page
```
┌─────────────────────────────────────────────┐
│  Filter: [Level: All▼] [Node: All▼]        │
│  Search: [__________________]               │
│  Time: [Last 1 hour ▼]          [Export]   │
├─────────────────────────────────────────────┤
│                                              │
│ 2026-01-15 10:35:12 [INFO] server-01        │
│   Service nginx restarted successfully      │
│                                              │
│ 2026-01-15 10:34:58 [WARN] server-01        │
│   High CPU usage detected: 87%              │
│   [View Details]                            │
│                                              │
│ 2026-01-15 10:30:00 [INFO] Automation       │
│   Executed: Nightly backup (Success)        │
│   [View Execution]                          │
│                                              │
└─────────────────────────────────────────────┘
```

**Features**:
- Real-time log streaming
- Advanced filtering
- Search with regex
- Export logs
- Tail mode

#### 7. Settings Page

**Sections**:
- **General**: Theme, language, timezone
- **Nodes**: Add/remove agents, installation tokens
- **Users**: User management, roles, API keys
- **Integrations**: Ollama, UniFi, webhooks, notifications
- **Security**: Audit logs, sessions, security settings
- **Backup**: Export/import configuration

### Real-Time Updates

**WebSocket Subscriptions**:
```typescript
// Client subscribes to specific data streams
socket.emit('subscribe', {
  streams: [
    'agents:status',           // All agent status changes
    'agents:server-01:metrics', // Metrics from specific agent
    'services:*',              // All service events
    'automations:executions'   // Automation execution events
  ]
});

// Server pushes updates
socket.on('update', (data: {
  stream: string;
  event: string;
  payload: any;
  timestamp: string;
}) => {
  // Update UI
});
```

**Optimistic UI Updates**:
- User actions show immediate feedback
- Revert if server rejects
- Show pending state during execution

---

## AI Orchestration Layer

### Architecture

```
┌─────────────────────────────────────────────────────────┐
│              AI Orchestration Layer                     │
│                                                          │
│  ┌────────────────────────────────────────────────────┐ │
│  │             AI Agent Manager                       │ │
│  │  - Agent lifecycle                                 │ │
│  │  - Context management                              │ │
│  │  - Tool registry                                   │ │
│  └────────────────────────────────────────────────────┘ │
│                                                          │
│  ┌────────────────────────────────────────────────────┐ │
│  │             Model Manager                          │ │
│  │  - Ollama connection pool                          │ │
│  │  - Model selection                                 │ │
│  │  - Prompt templates                                │ │
│  └────────────────────────────────────────────────────┘ │
│                                                          │
│  ┌────────────────────────────────────────────────────┐ │
│  │             Tool Calling Interface                 │ │
│  │  ┌──────────┬──────────┬──────────┬─────────────┐ │ │
│  │  │  Agent   │ Service  │  Query   │   Custom    │ │ │
│  │  │ Commands │ Control  │  Metrics │   Scripts   │ │ │
│  │  └──────────┴──────────┴──────────┴─────────────┘ │ │
│  └────────────────────────────────────────────────────┘ │
│                                                          │
│  ┌────────────────────────────────────────────────────┐ │
│  │            Conversation Memory                     │ │
│  │  - Session context                                 │ │
│  │  - Tool execution history                          │ │
│  │  - System state cache                              │ │
│  └────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────┘
                         │
                         ▼
              ┌──────────────────┐
              │  Ollama Server   │
              │  (Local LLMs)    │
              └──────────────────┘
```

### Model Management

#### Ollama Integration
```python
class OllamaManager:
    """Manages connections to Ollama instances"""

    def __init__(self):
        self.instances = {}  # {name: OllamaClient}

    def add_instance(self, name: str, url: str):
        """Register Ollama instance"""
        self.instances[name] = OllamaClient(url)

    def list_models(self, instance: str = 'default'):
        """List available models on instance"""
        return self.instances[instance].list()

    def pull_model(self, model: str, instance: str = 'default'):
        """Pull model to instance"""
        return self.instances[instance].pull(model)

    def delete_model(self, model: str, instance: str = 'default'):
        """Delete model from instance"""
        return self.instances[instance].delete(model)
```

#### Prompt Templates
```yaml
templates:
  - id: deploy
    name: "Deploy Application"
    system_prompt: |
      You are a deployment assistant. You can:
      - Deploy containers
      - Restart services
      - Check service status
      - View logs

      Always confirm before making changes.
    user_prompt_template: |
      Deploy {{ application }} to {{ environment }}.
      Version: {{ version }}
    tools:
      - docker.deploy
      - systemctl.restart
      - docker.logs

  - id: troubleshoot
    name: "Troubleshoot Issue"
    system_prompt: |
      You are a troubleshooting expert. Analyze issues and suggest fixes.
      Available tools: check metrics, search logs, inspect services.
    user_prompt_template: |
      Service {{ service }} is {{ status }}.
      Help me troubleshoot.
    tools:
      - query.metrics
      - search.logs
      - service.inspect
```

### Tool Calling System

#### Tool Definition Schema
```python
@dataclass
class Tool:
    """AI tool definition"""
    name: str
    description: str
    parameters: dict[str, ToolParameter]
    required_permissions: list[str]
    handler: Callable

@dataclass
class ToolParameter:
    name: str
    type: str  # string, number, boolean, array, object
    description: str
    required: bool
    enum: list[Any] | None = None
```

#### Built-in Tools

**1. Agent Commands**
```python
Tool(
    name="agent_execute_command",
    description="Execute a command on a specific agent",
    parameters={
        "agent_id": ToolParameter(
            name="agent_id",
            type="string",
            description="ID of the agent to execute on",
            required=True
        ),
        "command": ToolParameter(
            name="command",
            type="string",
            description="Command to execute",
            required=True,
            enum=["docker.ps", "docker.restart", "systemctl.status", ...]
        ),
        "params": ToolParameter(
            name="params",
            type="object",
            description="Command parameters",
            required=False
        )
    },
    required_permissions=["agent.execute"],
    handler=execute_agent_command
)
```

**2. Query Metrics**
```python
Tool(
    name="query_metrics",
    description="Query system metrics",
    parameters={
        "agent_id": ToolParameter(
            name="agent_id",
            type="string",
            description="Agent to query",
            required=True
        ),
        "metric": ToolParameter(
            name="metric",
            type="string",
            description="Metric name",
            required=True,
            enum=["cpu", "memory", "disk", "network"]
        ),
        "time_range": ToolParameter(
            name="time_range",
            type="string",
            description="Time range for query",
            required=False,
            enum=["5m", "1h", "6h", "24h"]
        )
    },
    required_permissions=["metrics.read"],
    handler=query_metrics
)
```

**3. Search Logs**
```python
Tool(
    name="search_logs",
    description="Search logs across services",
    parameters={
        "query": ToolParameter(
            name="query",
            type="string",
            description="Search query (supports regex)",
            required=True
        ),
        "agent_id": ToolParameter(
            name="agent_id",
            type="string",
            description="Agent to search on (optional)",
            required=False
        ),
        "service": ToolParameter(
            name="service",
            type="string",
            description="Service to search (optional)",
            required=False
        ),
        "limit": ToolParameter(
            name="limit",
            type="number",
            description="Max results",
            required=False
        )
    },
    required_permissions=["logs.read"],
    handler=search_logs
)
```

**4. Service Control**
```python
Tool(
    name="control_service",
    description="Start, stop, or restart a service",
    parameters={
        "agent_id": ToolParameter(
            name="agent_id",
            type="string",
            description="Agent where service runs",
            required=True
        ),
        "service": ToolParameter(
            name="service",
            type="string",
            description="Service name",
            required=True
        ),
        "action": ToolParameter(
            name="action",
            type="string",
            description="Action to perform",
            required=True,
            enum=["start", "stop", "restart", "status"]
        )
    },
    required_permissions=["service.control"],
    handler=control_service
)
```

#### Tool Execution Flow

```
User Input
    │
    ▼
┌─────────────────┐
│   LLM Model     │ (Ollama)
└────────┬────────┘
         │ Decides to use tool
         ▼
┌─────────────────┐
│  Tool Router    │
│ - Validate      │
│ - Check perms   │
│ - Log request   │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Tool Handler   │
│ - Execute       │
│ - Return result │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│   LLM Model     │
│ - Process result│
│ - Format response│
└────────┬────────┘
         │
         ▼
    User Output
```

### AI Agent Types

#### 1. Interactive Assistant
- **Purpose**: General-purpose chat assistant
- **Capabilities**: All tools available
- **Use case**: User asks questions, requests actions
- **Confirmation**: Required for destructive actions

#### 2. Monitoring Agent
- **Purpose**: Proactive system monitoring
- **Capabilities**: Read-only tools (metrics, logs, status)
- **Use case**: Detect issues, send alerts
- **Runs**: Background, event-triggered

#### 3. Troubleshooting Agent
- **Purpose**: Diagnose and fix issues
- **Capabilities**: Read tools + safe remediation
- **Use case**: Automated issue resolution
- **Runs**: Triggered by alerts

#### 4. Deployment Agent
- **Purpose**: Handle deployments
- **Capabilities**: Container/service control
- **Use case**: Execute deployment workflows
- **Runs**: Manually triggered or scheduled

### Conversation Memory

```python
class ConversationMemory:
    """Manages AI conversation context"""

    def __init__(self, session_id: str):
        self.session_id = session_id
        self.messages = []
        self.context = {}
        self.tool_results = {}

    def add_message(self, role: str, content: str):
        """Add message to conversation"""
        self.messages.append({
            "role": role,
            "content": content,
            "timestamp": datetime.utcnow()
        })

    def add_context(self, key: str, value: Any):
        """Add context information"""
        self.context[key] = value

    def add_tool_result(self, tool: str, result: Any):
        """Store tool execution result"""
        self.tool_results[tool] = result

    def get_context_for_llm(self) -> list[dict]:
        """Format context for LLM"""
        # Return messages with system context injected
        return [
            {"role": "system", "content": self._build_system_context()},
            *self.messages
        ]

    def _build_system_context(self) -> str:
        """Build system context from available data"""
        parts = [
            "Current system state:",
            f"- Active agents: {self.context.get('active_agents', [])}",
            f"- Recent alerts: {self.context.get('recent_alerts', [])}",
            f"- Previous tool results: {self.tool_results}"
        ]
        return "\n".join(parts)
```

### Safety & Guardrails

#### 1. Confirmation Requirements
```python
CONFIRMATION_REQUIRED = [
    "docker.container.delete",
    "docker.container.rm",
    "systemctl.stop",
    "script.execute",  # Unless pre-approved
    "agent.reboot",
    "agent.shutdown"
]
```

#### 2. Rate Limiting
- Max 10 tool calls per conversation
- Max 1 destructive action per minute
- Exponential backoff on errors

#### 3. Scope Limiting
```python
class AIAgentScope:
    """Define what an AI agent can access"""
    allowed_agents: list[str]  # Which agents it can control
    allowed_tools: list[str]   # Which tools it can use
    require_confirmation: bool
    max_cost: float  # Max "cost" of actions (weighted)
```

#### 4. Audit Trail
- All AI actions logged
- Tool calls recorded
- User approval decisions stored
- Rollback capability

### Example AI Workflows

#### Workflow 1: Deploy Application
```
User: "Deploy version 2.1.0 to staging"

AI Process:
1. Use tool: query_metrics(agent="staging", metric="cpu")
   → Check if staging is healthy
2. Use tool: service_control(agent="staging", service="app", action="status")
   → Check current app state
3. Use tool: agent_execute_command(agent="staging", command="docker.pull",
                                    params={"image": "app:2.1.0"})
   → Pull new image
4. [Requests confirmation]
   AI: "Ready to deploy app:2.1.0 to staging. Current version is 2.0.5. Proceed?"
5. User confirms
6. Use tool: agent_execute_command(agent="staging", command="docker.container.update",
                                    params={"container": "app", "image": "app:2.1.0"})
   → Update container
7. Use tool: search_logs(agent="staging", service="app", limit=20)
   → Check for errors
8. AI: "Deployment complete. App:2.1.0 is running on staging. No errors in logs."
```

#### Workflow 2: Troubleshoot High CPU
```
Automation triggers AI agent due to high CPU alert

AI Process:
1. Use tool: query_metrics(agent="server-01", metric="cpu", time_range="1h")
   → Analyze CPU trend
2. Use tool: agent_execute_command(agent="server-01", command="docker.ps")
   → List running containers
3. Use tool: agent_execute_command(agent="server-01", command="docker.stats")
   → Identify high-CPU container
4. Use tool: search_logs(agent="server-01", service="app", query="error|exception")
   → Check for errors
5. AI determines: "App container consuming 85% CPU due to memory leak (logs show 'Out of memory' warnings)"
6. AI suggests: "Recommend restarting app container to clear memory leak. Permanent fix: upgrade to version 2.1.1 which patches this issue."
7. [If configured for auto-remediation]
   Use tool: service_control(agent="server-01", service="app", action="restart")
8. Send notification with analysis and action taken
```

---

## Data Models

### Database Schema (SQLite/Postgres)

#### Core Tables

**agents**
```sql
CREATE TABLE agents (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(255) NOT NULL,
    hostname VARCHAR(255),
    os VARCHAR(100),
    os_version VARCHAR(100),
    architecture VARCHAR(50),
    api_key_hash VARCHAR(255) NOT NULL,
    last_seen_at TIMESTAMP,
    status VARCHAR(50) DEFAULT 'offline',  -- online, offline, error
    capabilities JSONB,  -- Array of capability strings
    metadata JSONB,      -- Custom metadata
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_agents_status ON agents(status);
CREATE INDEX idx_agents_last_seen ON agents(last_seen_at);
```

**users**
```sql
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    username VARCHAR(255) UNIQUE NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    role VARCHAR(50) NOT NULL,  -- admin, operator, viewer
    is_active BOOLEAN DEFAULT true,
    last_login_at TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_users_username ON users(username);
CREATE INDEX idx_users_email ON users(email);
```

**api_keys**
```sql
CREATE TABLE api_keys (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    name VARCHAR(255),
    key_hash VARCHAR(255) NOT NULL,
    key_prefix VARCHAR(20),  -- First few chars for identification
    scopes JSONB,  -- Array of permission scopes
    expires_at TIMESTAMP,
    last_used_at TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_api_keys_user ON api_keys(user_id);
CREATE INDEX idx_api_keys_prefix ON api_keys(key_prefix);
```

**services**
```sql
CREATE TABLE services (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    agent_id UUID REFERENCES agents(id) ON DELETE CASCADE,
    name VARCHAR(255) NOT NULL,
    type VARCHAR(100),  -- docker, systemd, process, custom
    status VARCHAR(50),  -- running, stopped, error
    external_id VARCHAR(255),  -- Docker container ID, systemd unit, etc.
    config JSONB,
    metadata JSONB,
    discovered_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(agent_id, name, type)
);

CREATE INDEX idx_services_agent ON services(agent_id);
CREATE INDEX idx_services_status ON services(status);
CREATE INDEX idx_services_type ON services(type);
```

**metrics**
```sql
CREATE TABLE metrics (
    id BIGSERIAL PRIMARY KEY,
    agent_id UUID REFERENCES agents(id) ON DELETE CASCADE,
    metric_name VARCHAR(100) NOT NULL,
    value NUMERIC,
    tags JSONB,  -- Additional dimensions
    timestamp TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_metrics_agent_time ON metrics(agent_id, timestamp DESC);
CREATE INDEX idx_metrics_name_time ON metrics(metric_name, timestamp DESC);

-- Partitioning recommended for large deployments
-- CREATE TABLE metrics_y2026m01 PARTITION OF metrics
--   FOR VALUES FROM ('2026-01-01') TO ('2026-02-01');
```

**automations**
```sql
CREATE TABLE automations (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(255) NOT NULL,
    description TEXT,
    enabled BOOLEAN DEFAULT true,
    definition JSONB NOT NULL,  -- Full automation YAML as JSON
    created_by UUID REFERENCES users(id),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_automations_enabled ON automations(enabled);
```

**automation_executions**
```sql
CREATE TABLE automation_executions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    automation_id UUID REFERENCES automations(id) ON DELETE CASCADE,
    status VARCHAR(50) NOT NULL,  -- pending, running, success, failed, skipped
    trigger_data JSONB,
    started_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    completed_at TIMESTAMP,
    duration_ms INTEGER,
    logs TEXT,
    error TEXT,
    result JSONB
);

CREATE INDEX idx_executions_automation ON automation_executions(automation_id, started_at DESC);
CREATE INDEX idx_executions_status ON automation_executions(status);
```

**events**
```sql
CREATE TABLE events (
    id BIGSERIAL PRIMARY KEY,
    event_type VARCHAR(100) NOT NULL,
    source VARCHAR(100),  -- agent_id, user_id, system
    source_id UUID,
    severity VARCHAR(50) DEFAULT 'info',  -- debug, info, warning, error, critical
    message TEXT,
    data JSONB,
    timestamp TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_events_type_time ON events(event_type, timestamp DESC);
CREATE INDEX idx_events_severity_time ON events(severity, timestamp DESC);
CREATE INDEX idx_events_source ON events(source, source_id);
```

**audit_logs**
```sql
CREATE TABLE audit_logs (
    id BIGSERIAL PRIMARY KEY,
    user_id UUID REFERENCES users(id),
    action VARCHAR(100) NOT NULL,
    resource_type VARCHAR(100),
    resource_id UUID,
    changes JSONB,  -- Before/after for updates
    ip_address INET,
    user_agent TEXT,
    timestamp TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_audit_user_time ON audit_logs(user_id, timestamp DESC);
CREATE INDEX idx_audit_action ON audit_logs(action);
CREATE INDEX idx_audit_resource ON audit_logs(resource_type, resource_id);
```

**ai_sessions**
```sql
CREATE TABLE ai_sessions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES users(id),
    model VARCHAR(100),
    template_id VARCHAR(100),
    context JSONB,  -- Conversation context
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

**ai_messages**
```sql
CREATE TABLE ai_messages (
    id BIGSERIAL PRIMARY KEY,
    session_id UUID REFERENCES ai_sessions(id) ON DELETE CASCADE,
    role VARCHAR(50) NOT NULL,  -- user, assistant, system, tool
    content TEXT NOT NULL,
    tool_calls JSONB,
    tool_results JSONB,
    timestamp TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_ai_messages_session ON ai_messages(session_id, timestamp);
```

**secrets**
```sql
CREATE TABLE secrets (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(255) UNIQUE NOT NULL,
    encrypted_value TEXT NOT NULL,  -- AES-256 encrypted
    description TEXT,
    created_by UUID REFERENCES users(id),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### File Storage Structure

```
/var/lib/echodesk/
├── data/
│   ├── echodesk.db           # SQLite database (if using SQLite)
│   ├── secrets.key            # Encryption key
│   └── backups/               # Automated backups
├── scripts/                   # Custom user scripts
│   └── allowed/               # Sandboxed script directory
├── logs/
│   ├── server.log
│   ├── agents/
│   │   ├── agent-001.log
│   │   └── agent-002.log
│   └── automations/
│       └── execution-*.log
├── uploads/                   # Temporary file uploads
└── exports/                   # Exported data
```

---

## Deployment Architecture

### Docker Compose Stack

**docker-compose.yml**
```yaml
version: '3.8'

services:
  echodesk-server:
    image: echodesk/server:latest
    container_name: echodesk-server
    restart: unless-stopped
    ports:
      - "8443:8443"  # HTTPS API + WebSocket
    environment:
      - DATABASE_URL=sqlite:////data/echodesk.db
      # Or: postgresql://user:pass@postgres:5432/echodesk
      - SECRET_KEY_FILE=/run/secrets/secret_key
      - OLLAMA_URL=http://ollama:11434
      - LOG_LEVEL=info
    volumes:
      - ./data:/data
      - ./scripts:/scripts:ro
      - ./logs:/logs
      - /var/run/docker.sock:/var/run/docker.sock:ro  # Optional: local Docker
    secrets:
      - secret_key
    networks:
      - echodesk
    depends_on:
      - postgres  # If using Postgres
      - ollama    # If using local Ollama

  postgres:  # Optional: Use for multi-user or larger deployments
    image: postgres:16-alpine
    container_name: echodesk-postgres
    restart: unless-stopped
    environment:
      - POSTGRES_DB=echodesk
      - POSTGRES_USER=echodesk
      - POSTGRES_PASSWORD_FILE=/run/secrets/db_password
    volumes:
      - postgres-data:/var/lib/postgresql/data
    secrets:
      - db_password
    networks:
      - echodesk

  ollama:  # Optional: Run Ollama in same stack
    image: ollama/ollama:latest
    container_name: echodesk-ollama
    restart: unless-stopped
    volumes:
      - ollama-models:/root/.ollama
    networks:
      - echodesk
    # GPU support (NVIDIA)
    # deploy:
    #   resources:
    #     reservations:
    #       devices:
    #         - driver: nvidia
    #           count: 1
    #           capabilities: [gpu]

  echodesk-web:  # Optional: Separate frontend container
    image: echodesk/web:latest
    container_name: echodesk-web
    restart: unless-stopped
    ports:
      - "3000:80"
    environment:
      - API_URL=https://echodesk-server:8443
    networks:
      - echodesk
    depends_on:
      - echodesk-server

volumes:
  postgres-data:
  ollama-models:

secrets:
  secret_key:
    file: ./secrets/secret_key.txt
  db_password:
    file: ./secrets/db_password.txt

networks:
  echodesk:
    driver: bridge
```

### Agent Deployment

#### Installation Script
```bash
#!/bin/bash
# install-agent.sh

set -e

ECHODESK_SERVER="${ECHODESK_SERVER:-https://echodesk.local:8443}"
INSTALL_TOKEN="${INSTALL_TOKEN}"
INSTALL_DIR="/opt/echodesk-agent"

echo "Installing EchoDesk Agent..."

# Install Python if not present
if ! command -v python3 &> /dev/null; then
    echo "Python 3 not found. Please install Python 3.9+."
    exit 1
fi

# Create installation directory
sudo mkdir -p "$INSTALL_DIR"
cd "$INSTALL_DIR"

# Download agent
sudo curl -L "${ECHODESK_SERVER}/downloads/agent/latest" -o agent.tar.gz
sudo tar xzf agent.tar.gz
sudo rm agent.tar.gz

# Create virtual environment
sudo python3 -m venv venv
source venv/bin/activate

# Install dependencies
sudo ./venv/bin/pip install -r requirements.txt

# Register with server
echo "Registering agent with server..."
sudo ./venv/bin/python agent.py register \
    --server "$ECHODESK_SERVER" \
    --token "$INSTALL_TOKEN"

# Install systemd service
sudo tee /etc/systemd/system/echodesk-agent.service > /dev/null <<EOF
[Unit]
Description=EchoDesk Agent
After=network.target

[Service]
Type=simple
User=echodesk
Group=echodesk
WorkingDirectory=$INSTALL_DIR
ExecStart=$INSTALL_DIR/venv/bin/python $INSTALL_DIR/agent.py run
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
EOF

# Create user
sudo useradd -r -s /bin/false echodesk || true
sudo chown -R echodesk:echodesk "$INSTALL_DIR"

# Start service
sudo systemctl daemon-reload
sudo systemctl enable echodesk-agent
sudo systemctl start echodesk-agent

echo "EchoDesk Agent installed and started!"
echo "Check status: sudo systemctl status echodesk-agent"
```

#### Agent Configuration
```yaml
# /opt/echodesk-agent/config.yml

server:
  url: "https://echodesk.local:8443"
  verify_ssl: true
  cert_fingerprint: "sha256:ABC123..."  # Server cert pinning

agent:
  id: "auto"  # Set during registration
  name: "server-01"
  capabilities:
    - system.metrics
    - docker.control
    - systemd.control
    - script.execute

security:
  allowed_commands:
    docker:
      - ps
      - inspect
      - start
      - stop
      - restart
    systemctl:
      allowed_services:
        - nginx
        - postgres
      allowed_actions:
        - status
        - start
        - stop
        - restart
    scripts:
      allowed_paths:
        - /opt/echodesk/scripts

  resource_limits:
    cpu_percent: 25
    memory_mb: 512
    timeout_seconds: 300

logging:
  level: "info"
  file: "/var/log/echodesk-agent/agent.log"
  max_size_mb: 100
  max_files: 5

metrics:
  collection_interval: 60  # seconds
  enabled_metrics:
    - cpu
    - memory
    - disk
    - network
    - services
```

---

## Scaling Strategy

### Phase 1: Single Server (MVP)
- **Capacity**: 10-50 agents
- **Deployment**: Single Docker Compose stack
- **Database**: SQLite
- **Metrics**: In-memory + short-term persistence

**Limitations**:
- Single point of failure
- Limited concurrent connections
- Metric retention: 7 days

### Phase 2: Hardened Single Server
- **Capacity**: 50-200 agents
- **Deployment**: Same stack with optimizations
- **Database**: PostgreSQL
- **Metrics**: Time-series table with partitioning
- **Additions**:
  - Connection pooling
  - Metric downsampling
  - Backup automation

**Optimizations**:
- WebSocket connection pooling
- Metric aggregation (5m, 1h, 1d rollups)
- Database tuning
- Add Redis for caching (optional)

### Phase 3: Horizontal Scaling (Future)
- **Capacity**: 200+ agents
- **Deployment**: Multiple server instances
- **Database**: PostgreSQL with replication
- **Additions**:
  - Load balancer (HAProxy/Nginx)
  - Redis for shared state
  - Message queue (RabbitMQ) for async tasks
  - Separate metrics storage (InfluxDB/TimescaleDB)

**Architecture**:
```
                   ┌──────────────┐
                   │ Load Balancer│
                   └──────┬───────┘
                          │
         ┌────────────────┼────────────────┐
         │                │                │
    ┌────▼────┐      ┌────▼────┐     ┌────▼────┐
    │Server 1 │      │Server 2 │     │Server 3 │
    └────┬────┘      └────┬────┘     └────┬────┘
         │                │                │
         └────────────────┼────────────────┘
                          │
              ┌───────────┼───────────┐
              │           │           │
         ┌────▼────┐ ┌────▼────┐ ┌───▼──────┐
         │Postgres │ │  Redis  │ │InfluxDB  │
         │(Primary)│ │         │ │          │
         └─────────┘ └─────────┘ └──────────┘
```

### Upgrade Strategy

#### Database Migrations
- **Tool**: Alembic (Python migrations)
- **Process**:
  1. Backup database before upgrade
  2. Apply migrations automatically on startup
  3. Rollback capability
  4. Schema versioning

#### Zero-Downtime Updates
1. Agent updates:
   - Rolling updates with version checking
   - Backward-compatible protocol changes
   - Graceful reconnection

2. Server updates:
   - Blue/green deployment (if multi-server)
   - Database migrations before new code
   - WebSocket connection draining

#### Backup & Recovery
```yaml
# Automated backup configuration
backup:
  enabled: true
  schedule: "0 2 * * *"  # Daily at 2 AM
  retention_days: 30
  targets:
    - type: local
      path: /var/backups/echodesk
    - type: s3  # Optional
      bucket: echodesk-backups
      region: us-east-1

  includes:
    - database
    - configuration
    - secrets (encrypted)
    - automation definitions
```

---

## MVP Feature Prioritization

### Milestone 1: Core Foundation (Weeks 1-2)
**Goal**: Basic server-agent communication and UI

✅ Features:
- [ ] FastAPI server with REST + WebSocket
- [ ] Agent registration and authentication
- [ ] Basic agent (system metrics only)
- [ ] SQLite database setup
- [ ] React UI with dashboard layout
- [ ] System stats widget
- [ ] Agent list widget
- [ ] WebSocket real-time updates

**Deliverable**: Can install agent, see it online, view system metrics in dashboard

### Milestone 2: Service Management (Weeks 3-4)
**Goal**: Control Docker containers and systemd services

✅ Features:
- [ ] Docker service discovery
- [ ] systemd service discovery (Linux)
- [ ] Service status widget
- [ ] Service control actions (start/stop/restart)
- [ ] Command execution framework with sandboxing
- [ ] Audit logging
- [ ] Service detail modal

**Deliverable**: Can view and control Docker containers and systemd services from UI

### Milestone 3: Automation Engine (Weeks 5-6)
**Goal**: Create and run basic automations

✅ Features:
- [ ] Automation YAML parser and validator
- [ ] Schedule trigger (cron)
- [ ] Event trigger
- [ ] Basic action types (agent.command, notification)
- [ ] Automation UI (list, create, edit)
- [ ] Visual automation builder (basic)
- [ ] Execution history

**Deliverable**: Can create automation like "restart nginx if it stops"

### Milestone 4: AI Integration (Week 7)
**Goal**: Connect to Ollama and execute basic AI commands

✅ Features:
- [ ] Ollama connection manager
- [ ] Tool calling interface
- [ ] Basic tools (agent commands, query metrics)
- [ ] AI chat UI
- [ ] Prompt templates
- [ ] AI session history

**Deliverable**: Can chat with AI and have it execute commands

### Milestone 5: Production Ready (Week 8)
**Goal**: Polish and deployment

✅ Features:
- [ ] User authentication and RBAC
- [ ] Settings UI
- [ ] Agent installation script
- [ ] Docker Compose deployment
- [ ] Documentation (README, API docs)
- [ ] Error handling and logging improvements
- [ ] Performance optimization

**Deliverable**: Production-ready v1.0

---

## Technology Stack

### Backend
- **Language**: Python 3.11+
- **Framework**: FastAPI 0.109+
- **WebSocket**: FastAPI WebSocket + python-socketio
- **Database ORM**: SQLAlchemy 2.0+
- **Migrations**: Alembic
- **Task Queue**: APScheduler (embedded) or Celery (later)
- **HTTP Client**: httpx
- **Docker SDK**: docker-py
- **Validation**: Pydantic v2

### Frontend
- **Language**: TypeScript 5+
- **Framework**: React 18+
- **Build Tool**: Vite
- **UI Library**: shadcn/ui (Radix + Tailwind CSS)
- **State**: Zustand + React Query
- **Routing**: React Router v6
- **WebSocket**: Socket.IO client
- **Charts**: Recharts or Chart.js
- **Grid Layout**: react-grid-layout

### Agent
- **Language**: Python 3.9+ (broader compatibility)
- **HTTP**: httpx
- **WebSocket**: python-socketio
- **System Info**: psutil
- **Docker**: docker-py (optional)
- **Process**: subprocess (sandboxed)

### AI
- **LLM**: Ollama (local)
- **Client**: ollama-python
- **Prompt Templating**: Jinja2
- **Tool Schema**: JSON Schema

### Infrastructure
- **Container**: Docker + Docker Compose
- **Database**: SQLite (default) / PostgreSQL (optional)
- **Reverse Proxy**: Traefik / Nginx / Caddy
- **Monitoring**: Built-in metrics (future: Prometheus export)

### Development
- **Testing**: pytest, playwright
- **Linting**: ruff (Python), eslint (JS/TS)
- **Formatting**: black (Python), prettier (JS/TS)
- **Type Checking**: mypy (Python), tsc (TypeScript)
- **CI/CD**: GitHub Actions

---

## Next Steps

### Immediate Actions

1. **Validate Architecture**
   - Review this document
   - Identify any gaps or concerns
   - Prioritize must-have vs nice-to-have features

2. **Technology Decisions**
   - Confirm tech stack choices
   - Any preference changes?
   - Additional requirements?

3. **Project Setup**
   - Initialize repository structure
   - Set up development environment
   - Create project scaffolding

4. **Begin Milestone 1**
   - Start with server setup
   - Agent communication protocol
   - Basic UI shell

### Discussion Points

1. **Database**: SQLite vs Postgres from day 1?
2. **Agent Distribution**: Package as Python wheel, standalone binary (PyInstaller), or Docker image?
3. **UI**: Single-page app vs server-rendered? (Recommend SPA)
4. **Notifications**: Which channels needed? (Slack, email, Discord, webhooks?)
5. **Hardware Integration**: Timeline for DeskMate integration?

---

## Appendix

### API Endpoint Examples

#### REST API
```
# Authentication
POST   /api/v1/auth/login
POST   /api/v1/auth/logout
POST   /api/v1/auth/refresh

# Agents
GET    /api/v1/agents
GET    /api/v1/agents/:id
POST   /api/v1/agents/:id/command
DELETE /api/v1/agents/:id

# Services
GET    /api/v1/services
GET    /api/v1/services/:id
POST   /api/v1/services/:id/control

# Automations
GET    /api/v1/automations
POST   /api/v1/automations
GET    /api/v1/automations/:id
PUT    /api/v1/automations/:id
DELETE /api/v1/automations/:id
POST   /api/v1/automations/:id/execute

# Metrics
GET    /api/v1/metrics/query

# AI
POST   /api/v1/ai/chat
GET    /api/v1/ai/sessions
POST   /api/v1/ai/templates
```

#### WebSocket Events
```javascript
// Client → Server
{
  "event": "subscribe",
  "data": {"streams": ["agents:*", "services:*"]}
}

// Server → Client
{
  "event": "agent:status",
  "data": {"agent_id": "123", "status": "online"}
}
```

### Configuration File Example

**config.yml** (Server)
```yaml
server:
  host: "0.0.0.0"
  port: 8443
  ssl:
    enabled: true
    cert: "/certs/server.crt"
    key: "/certs/server.key"

database:
  url: "sqlite:////data/echodesk.db"
  # url: "postgresql://user:pass@localhost/echodesk"
  pool_size: 10
  echo: false

security:
  secret_key_file: "/run/secrets/secret_key"
  session_timeout: 3600
  api_key_rotation_days: 90

logging:
  level: "info"
  format: "json"
  file: "/logs/server.log"

metrics:
  retention_days: 7
  aggregation_intervals:
    - "5m"
    - "1h"
    - "1d"

ollama:
  url: "http://localhost:11434"
  timeout: 300
  default_model: "llama3.2:latest"

automation:
  max_concurrent: 10
  execution_timeout: 3600

notifications:
  slack:
    enabled: false
    webhook_url: ""
  email:
    enabled: false
    smtp_host: ""
    smtp_port: 587
```

---

**End of Architecture Specification**
