#   file: Makefile
# author: simshadows <contact@simshadows.com>

ROOT_PATH := $(abspath .)

CONTAINER_NAME := template-node
CONTAINER_HOSTNAME := $(CONTAINER_NAME)
IMAGE_NAME := simshadows/$(CONTAINER_NAME)

CLAUDE_VOLUME_NAME := $(CONTAINER_NAME)--claude

################################################################################

.PHONY: all
all: build up npm-install start

################################################################################

# Build image
.PHONY: build
build:
	podman build --pull -t $(IMAGE_NAME) $(ROOT_PATH)

# Start container
.PHONY: up
up:
	podman run \
		--name $(CONTAINER_NAME) \
		--hostname $(CONTAINER_HOSTNAME) \
		--mount type=bind,src=$(ROOT_PATH),dst=/repo \
		--mount type=volume,src=$(CLAUDE_VOLUME_NAME),dst=/home/node/.claude \
		--userns keep-id \
		--rm -itd \
		$(IMAGE_NAME)

################################################################################

# Open shell
.PHONY: shell bash attach enter
shell bash attach enter:
	podman exec -it $(CONTAINER_NAME) bash

# `npm install`
.PHONY: npm-install
npm-install:
	podman exec -it $(CONTAINER_NAME) npm install

# Build release artifacts for use in Prod
.PHONY: release
release:
	podman exec -it $(CONTAINER_NAME) npm run build

# Run
.PHONY: run
run:
	podman exec -it $(CONTAINER_NAME) npm run run

# Run `npm start`
.PHONY: start
start:
	podman exec -it $(CONTAINER_NAME) npm start

# Run auto-tests
.PHONY: test
test:
	podman exec -it $(CONTAINER_NAME) npm test

# Run static type checking
.PHONY: typecheck
typecheck:
	podman exec -it $(CONTAINER_NAME) npm run typecheck

# Run Claude Code CLI
.PHONY: ai claude
ai claude:
	podman exec -it $(CONTAINER_NAME) claude

################################################################################

# Stop container
.PHONY: down
down:
	-podman stop $(CONTAINER_NAME)


# Clean up images/containers
.PHONY: clean teardown destroy
clean teardown destroy: down
	-podman rm $(CONTAINER_NAME)
	-podman image rm localhost/$(IMAGE_NAME)

# Cleans more up
.PHONY: clean-more teardown-more destroy-more
clean-more teardown-more destroy-more: clean
	-podman volume rm $(CLAUDE_VOLUME_NAME)

