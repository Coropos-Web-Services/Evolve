# EchoDesk Development Checklist

## ✅ Session 1: Foundation (COMPLETE)

- [x] Create project structure
- [x] Design complete architecture (ARCHITECTURE.md)
- [x] Set up FastAPI server
- [x] Create database models (Agent, User)
- [x] Implement agent registration API
- [x] Build Python agent with metrics collection
- [x] Set up Docker Compose
- [x] Create development tooling (Makefile)
- [x] Write documentation (README, GETTING_STARTED, STATUS, etc.)

**Deliverables**: Working server + agent that can register and collect metrics

---

## 🚧 Session 2: Real-Time Communication (NEXT)

### WebSocket Server Implementation
- [ ] Add python-socketio to server dependencies
- [ ] Create WebSocket namespace in FastAPI
- [ ] Implement agent connection handler
- [ ] Implement agent disconnection handler
- [ ] Add authentication to WebSocket connections
- [ ] Create message routing system

### Agent Heartbeat System
- [ ] Create heartbeat endpoint/event
- [ ] Update agent to send heartbeat via WebSocket
- [ ] Implement server-side heartbeat tracking
- [ ] Add agent status update logic (online/offline)
- [ ] Add last_seen_at timestamp updates

### Metrics Streaming
- [ ] Create metrics event/endpoint
- [ ] Update agent to send metrics via WebSocket
- [ ] Add metrics table to database
- [ ] Implement metrics storage service
- [ ] Add metrics query endpoint

### Testing
- [ ] Test agent connects via WebSocket
- [ ] Test heartbeat updates agent status
- [ ] Test metrics are stored in database
- [ ] Test reconnection logic
- [ ] Test multiple agents simultaneously

**Goal**: Agents connect via WebSocket, status tracked, metrics stored in real-time

---

## 🎨 Session 3: Basic Frontend (WEEK 1-2)

### React Setup
- [ ] Initialize Vite + React + TypeScript
- [ ] Install and configure shadcn/ui
- [ ] Set up Tailwind CSS
- [ ] Create basic routing structure
- [ ] Add Zustand for state management
- [ ] Add React Query for API calls

### Layout Components
- [ ] Create main layout component
- [ ] Add sidebar navigation
- [ ] Add header with branding
- [ ] Create responsive breakpoints
- [ ] Implement dark mode

### Agent List Page
- [ ] Create agent list component
- [ ] Fetch agents from API
- [ ] Display agent cards/list
- [ ] Show online/offline status
- [ ] Add search/filter functionality

### Dashboard Page
- [ ] Create dashboard layout
- [ ] Implement basic grid system
- [ ] Create system stats widget
- [ ] Create agent list widget
- [ ] Add widget placeholders

### WebSocket Client
- [ ] Set up Socket.IO client
- [ ] Connect to server WebSocket
- [ ] Subscribe to agent status updates
- [ ] Subscribe to metrics updates
- [ ] Update UI in real-time

**Goal**: Basic UI showing agents and metrics in real-time

---

## 🐳 Session 4: Service Discovery (WEEK 2-3)

### Docker Integration
- [ ] Add Docker SDK to agent
- [ ] Implement Docker container discovery
- [ ] Collect container status
- [ ] Collect container stats (CPU, memory)
- [ ] Send container info to server

### systemd Integration (Linux)
- [ ] Implement systemd service discovery
- [ ] Collect service status
- [ ] Handle systemd on non-Linux gracefully

### Server-Side Service Management
- [ ] Create services table in database
- [ ] Create service model
- [ ] Add service endpoints (list, get, control)
- [ ] Store service discovery results

### UI Updates
- [ ] Create services page
- [ ] Display Docker containers
- [ ] Display systemd services
- [ ] Show service status
- [ ] Add basic control buttons (start/stop/restart)

**Goal**: Discover and display Docker containers and systemd services

---

## ⚙️ Session 5: Service Control (WEEK 3-4)

### Command Execution Framework
- [ ] Design command allowlist structure
- [ ] Implement command validator
- [ ] Add resource limits
- [ ] Create execution sandbox
- [ ] Add timeout handling

### Docker Controls
- [ ] Implement docker.start command
- [ ] Implement docker.stop command
- [ ] Implement docker.restart command
- [ ] Implement docker.logs command
- [ ] Add permission checking

### systemd Controls (Linux)
- [ ] Implement systemctl.start command
- [ ] Implement systemctl.stop command
- [ ] Implement systemctl.restart command
- [ ] Implement systemctl.status command

### Audit Logging
- [ ] Create audit_logs table
- [ ] Log all command executions
- [ ] Log command results
- [ ] Add audit log query endpoint
- [ ] Display audit logs in UI

### UI Updates
- [ ] Add control buttons to service cards
- [ ] Implement action confirmation modals
- [ ] Show loading states
- [ ] Display success/error messages
- [ ] Add logs viewer component

**Goal**: Control Docker containers and systemd services from UI

---

## 🤖 Session 6: Automation Engine (WEEK 5-6)

### Database Schema
- [ ] Create automations table
- [ ] Create automation_executions table
- [ ] Add indexes for performance

### Rule Parser
- [ ] Implement YAML rule parser
- [ ] Validate rule syntax
- [ ] Validate permissions
- [ ] Create rule data models

### Trigger System
- [ ] Implement schedule trigger (cron)
- [ ] Implement event trigger
- [ ] Implement metric threshold trigger
- [ ] Create trigger manager
- [ ] Add trigger evaluation logic

### Action Executor
- [ ] Implement agent.command action
- [ ] Implement notification action
- [ ] Add action chaining
- [ ] Implement error handling
- [ ] Add retry logic

### Execution Engine
- [ ] Create execution state machine
- [ ] Implement execution loop
- [ ] Store execution history
- [ ] Add execution monitoring
- [ ] Implement execution cancellation

### UI - Automation Management
- [ ] Create automation list page
- [ ] Add automation create/edit form
- [ ] Implement simple rule builder
- [ ] Add execution history view
- [ ] Add enable/disable toggle

**Goal**: Create and run basic automations (e.g., restart service on failure)

---

## 🧠 Session 7: AI Integration (WEEK 7)

### Ollama Integration
- [ ] Add ollama-python to dependencies
- [ ] Implement Ollama connection manager
- [ ] Add model list endpoint
- [ ] Test model inference

### Tool System
- [ ] Define tool schema
- [ ] Implement tool registry
- [ ] Create built-in tools (agent commands, metrics query)
- [ ] Add tool execution handler
- [ ] Implement tool permission checking

### AI Agent Runtime
- [ ] Create AI session manager
- [ ] Implement conversation memory
- [ ] Add prompt templates
- [ ] Implement tool calling loop
- [ ] Add confirmation system

### Database
- [ ] Create ai_sessions table
- [ ] Create ai_messages table
- [ ] Store tool execution results

### UI - AI Control Panel
- [ ] Create AI chat page
- [ ] Implement chat interface
- [ ] Add model selector
- [ ] Display tool executions
- [ ] Add prompt template selector
- [ ] Show session history

**Goal**: Chat with AI to execute commands and query system

---

## 🎯 Session 8: Production Ready (WEEK 8)

### Authentication System
- [ ] Implement user registration
- [ ] Add login endpoint
- [ ] Add JWT token generation
- [ ] Implement token validation middleware
- [ ] Add password reset flow

### RBAC Implementation
- [ ] Create permissions table
- [ ] Implement role-based checks
- [ ] Add permission decorators
- [ ] Enforce on all endpoints
- [ ] Add permission management UI

### Settings UI
- [ ] Create settings page
- [ ] Add user management
- [ ] Add agent management
- [ ] Add integration configuration
- [ ] Add security settings

### Agent Installer
- [ ] Create install script template
- [ ] Add install token generation
- [ ] Test on multiple platforms
- [ ] Add uninstall script

### Documentation
- [ ] Update README with screenshots
- [ ] Create user guide
- [ ] Create admin guide
- [ ] Add API documentation examples
- [ ] Create troubleshooting guide

### Testing & Polish
- [ ] Add unit tests (server)
- [ ] Add unit tests (agent)
- [ ] Add integration tests
- [ ] Fix bugs and edge cases
- [ ] Performance optimization
- [ ] Error handling improvements

### Deployment
- [ ] Create production Docker Compose
- [ ] Add backup scripts
- [ ] Add upgrade procedure
- [ ] Test production deployment
- [ ] Create release notes

**Goal**: Production-ready v1.0 release

---

## 🚀 Beyond MVP (V2+)

### Network Integration (V2)
- [ ] UniFi API integration
- [ ] Network device discovery
- [ ] Client tracking
- [ ] VLAN visibility
- [ ] Network alerts

### Advanced Automations (V2)
- [ ] Visual flow builder
- [ ] Conditional branching
- [ ] Loops and iterations
- [ ] Variable storage
- [ ] HTTP request actions

### Advanced AI (V2)
- [ ] Multiple AI agent types
- [ ] Background monitoring agent
- [ ] Autonomous troubleshooting
- [ ] Learning from patterns
- [ ] Proactive suggestions

### Hardware Integration (V3)
- [ ] Raspberry Pi GPIO support
- [ ] Touchscreen UI
- [ ] Physical buttons/knobs
- [ ] LED indicators
- [ ] DeskMate integration

### Scaling Features (V3)
- [ ] Multi-server support
- [ ] Load balancing
- [ ] High availability
- [ ] Metric downsampling
- [ ] Advanced analytics

---

## 📊 Progress Tracking

### Overall MVP Progress

| Milestone | Status | Completion |
|-----------|--------|------------|
| Foundation | ✅ Complete | 100% |
| Real-time Comm | ⏳ Next | 0% |
| Basic UI | 🔜 Pending | 0% |
| Service Discovery | 🔜 Pending | 0% |
| Service Control | 🔜 Pending | 0% |
| Automation | 🔜 Pending | 0% |
| AI Integration | 🔜 Pending | 0% |
| Production Ready | 🔜 Pending | 0% |

**Overall MVP**: 12.5% complete (1/8 milestones)

### Time Estimates

- ✅ Session 1 (Foundation): 2 hours (DONE)
- ⏳ Session 2 (WebSocket): 2-3 hours
- 🔜 Session 3 (UI): 3-4 hours
- 🔜 Session 4 (Discovery): 2-3 hours
- 🔜 Session 5 (Control): 3-4 hours
- 🔜 Session 6 (Automation): 4-5 hours
- 🔜 Session 7 (AI): 3-4 hours
- 🔜 Session 8 (Production): 4-5 hours

**Total Estimated Time**: 24-33 hours (~4-6 weeks at 6 hours/week)

---

## 🎯 Current Focus

**Now**: Session 2 - Real-Time Communication

**Immediate tasks**:
1. Add WebSocket to server
2. Connect agent via WebSocket
3. Implement heartbeat tracking
4. Store metrics in database

**Ready to start?** See `GETTING_STARTED.md` for setup instructions!

---

**Last Updated**: 2026-01-15
