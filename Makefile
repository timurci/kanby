# --- Configuration ------------------------------------------------------------

# Docker Compose settings
COMPOSE := docker compose
COMPOSE_ENV := .env.compose
COMPOSE_FLAGS := --env-file $(COMPOSE_ENV)

# Application settings
SECRET_ENV := .env
KANBY_DIR := kanby

# --- Colors and Icons ---------------------------------------------------------

# Detect if terminal supports colors: checks TTY, tput availability, and ≥8 colors
TERM_HAS_COLORS := $(shell \
  command -v tput >/dev/null 2>&1 && \
  colors=$$(tput colors 2>/dev/null) && \
  test "$$colors" -ge 8 && \
  echo 1 || echo 0)

# Enable colors only in interactive terminals
ifeq ($(TERM_HAS_COLORS),1)
    RED := $(shell tput setaf 1)
    GREEN := $(shell tput setaf 2)
    YELLOW := $(shell tput setaf 3)
    BLUE := $(shell tput setaf 4)
    BOLD := $(shell tput bold)
    NO_COLOR := $(shell tput sgr0)
    ICON_WARN := ⚠️ 
    ICON_OK := ✅ 
    ICON_INFO := ℹ️ 
else
    ICON_WARN := [WARN]
    ICON_OK := [OK]
    ICON_INFO := [INFO]
endif

# --- Help Target --------------------------------------------------------------

.PHONY: help
help: ## Show this help message
	@echo "$(BOLD)$(BLUE)Kanby Makefile Commands${NO_COLOR}"
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / { \
		printf "  $(GREEN)%-15s$(NO_COLOR) %s\n", $$1, $$2 \
	}' $(MAKEFILE_LIST)

.DEFAULT_GOAL := help

# --- Environment File Generation ----------------------------------------------

# Pattern rule: create .env files from examples (atomic)
.env%: .env%.example
	@echo "$(ICON_WARN) Creating $(GREEN)$@$(NO_COLOR) from template..."
	@cp $< $@

# --- Local Development --------------------------------------------------------

.PHONY: install
install: ## Install Python dependencies with uv
	@echo "$(ICON_INFO) Installing dependencies..."
	uv sync --locked
	@echo "$(ICON_OK) Installation complete."

.PHONY: adk-web
adk-web: install $(SECRET_ENV) ## Run ADK web interface locally
	@echo "$(ICON_INFO) Starting ADK web interface..."
	uv run adk web

.PHONY: adk-run
adk-run: install $(SECRET_ENV) ## Run ADK agent locally
	@echo "$(ICON_INFO) Running ADK agent from $(KANBY_DIR)..."
	uv run adk run $(KANBY_DIR)

# --- Docker Operations --------------------------------------------------------

.PHONY: build
build: $(COMPOSE_ENV) ## Build Docker containers
	@echo "$(ICON_INFO) Building containers..."
	$(COMPOSE) $(COMPOSE_FLAGS) build
	@echo "$(ICON_OK) Build complete."

.PHONY: up
up: $(COMPOSE_ENV) ## Start Docker services in detached mode
	@echo "$(ICON_INFO) Starting services..."
	$(COMPOSE) $(COMPOSE_FLAGS) up -d
	@echo "$(ICON_OK) Services started."

.PHONY: down
down: $(COMPOSE_ENV) ## Stop Docker services
	@echo "$(ICON_INFO) Stopping services..."
	$(COMPOSE) $(COMPOSE_FLAGS) down
	@echo "$(ICON_OK) Services stopped."

.PHONY: clean
clean: $(COMPOSE_ENV) ## Stop and REMOVE containers, images, and volumes
	@echo "$(RED)$(ICON_WARN) DESTRUCTIVE OPERATION $(ICON_WARN)$(NO_COLOR)"
	@echo "This will permanently delete:"
	@echo "  - All project containers"
	@echo "  - All associated images"
	@echo "  - All associated volumes"
	@read -p "Type 'yes' to confirm: " -r; \
	if [ "$$REPLY" = "yes" ]; then \
		echo ""; \
		echo "$(ICON_INFO) Cleaning up Docker resources..."; \
		$(COMPOSE) $(COMPOSE_FLAGS) down --rmi all --volumes; \
		echo "$(ICON_OK) Cleanup complete."; \
	else \
		echo "Aborted."; \
		exit 1; \
	fi

.PHONY: restart
restart: down up ## Restart Docker services

.PHONY: logs
logs: $(COMPOSE_ENV) ## Follow container logs
	$(COMPOSE) $(COMPOSE_FLAGS) logs -f

.PHONY: ps
ps: $(COMPOSE_ENV) ## Show container status
	$(COMPOSE) $(COMPOSE_FLAGS) ps

# --- Validation ---------------------------------------------------------------

# Check for required command and exit with helpful message
define require
@command -v $(1) >/dev/null || { \
	echo "$(RED)Error: '$(1)' is required but not installed.$(NO_COLOR)" >&2; \
	echo "       Please install it first." >&2; \
	exit 1; \
}
endef

.PHONY: check-local
check-local: ## Validate environment and dependencies for local development
	@echo "$(ICON_INFO) Validating local setup..."
	$(call require,uv)
	@test -f $(SECRET_ENV) || { echo "$(ICON_WARN) $(SECRET_ENV) missing. See $(SECRET_ENV).example"; exit 1; }
	@echo "$(ICON_OK) All checks passed."

.PHONY: check-docker
check-docker: ## Validate environment and dependencies for running docker
	@echo "$(ICON_INFO) Validating docker setup..."
	$(call require,docker)
	@test -f $(COMPOSE_ENV) || { echo "$(ICON_WARN) $(COMPOSE_ENV) missing. See $(COMPOSE_ENV).example"; exit 1; }
	@test -f $(SECRET_ENV) || { echo "$(ICON_WARN) $(SECRET_ENV) missing. See $(SECRET_ENV).example"; exit 1; }
	@echo "$(ICON_OK) All checks passed."

# --- Safety & Housekeeping ----------------------------------------------------

# Delete partially built files on error
.DELETE_ON_ERROR:

# Prevent parallel execution of certain targets
.NOTPARALLEL: clean env install