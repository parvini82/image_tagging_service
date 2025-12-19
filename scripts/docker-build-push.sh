#!/bin/bash

# Docker Build & Push Script for Image Tagging Service
# Usage: ./scripts/docker-build-push.sh [version-tag]
# Example: ./scripts/docker-build-push.sh v1.0.0

set -e

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Configuration
DOCKER_USERNAME=${DOCKER_USERNAME:-}
IMAGE_NAME="image_tagging_service"
REPO="${DOCKER_USERNAME}/${IMAGE_NAME}"
VERSION_TAG=${1:-latest}
LATEST_TAG="latest"

echo -e "${BLUE}========================================${NC}"
echo -e "${BLUE}Docker Build & Push Script${NC}"
echo -e "${BLUE}========================================${NC}"
echo ""

# Check prerequisites
if ! command -v docker &> /dev/null; then
    echo -e "${RED}✗ Docker is not installed${NC}"
    exit 1
fi

echo -e "${GREEN}✓ Docker found: $(docker --version)${NC}"

if [ -z "$DOCKER_USERNAME" ]; then
    echo -e "${YELLOW}Enter your Docker Hub username:${NC}"
    read -p "> " DOCKER_USERNAME
    if [ -z "$DOCKER_USERNAME" ]; then
        echo -e "${RED}✗ Docker username is required${NC}"
        exit 1
    fi
    REPO="${DOCKER_USERNAME}/${IMAGE_NAME}"
fi

echo -e "${GREEN}✓ Docker Hub username: ${DOCKER_USERNAME}${NC}"
echo -e "${GREEN}✓ Repository: ${REPO}${NC}"
echo -e "${GREEN}✓ Version tag: ${VERSION_TAG}${NC}"
echo ""

# Step 1: Build image
echo -e "${BLUE}[1/5] Building Docker image...${NC}"
if docker build -t "${REPO}:${VERSION_TAG}" -t "${REPO}:${LATEST_TAG}" .; then
    echo -e "${GREEN}✓ Image built successfully${NC}"
else
    echo -e "${RED}✗ Build failed${NC}"
    exit 1
fi
echo ""

# Step 2: Show image info
echo -e "${BLUE}[2/5] Image information:${NC}"
docker images | grep "${IMAGE_NAME}" || true
echo ""

# Step 3: Check if logged in
echo -e "${BLUE}[3/5] Checking Docker Hub authentication...${NC}"
if docker info | grep -q "Username: ${DOCKER_USERNAME}"; then
    echo -e "${GREEN}✓ Already logged in as: ${DOCKER_USERNAME}${NC}"
else
    echo -e "${YELLOW}Not logged in. Please log in to Docker Hub:${NC}"
    docker login -u "${DOCKER_USERNAME}" || {
        echo -e "${RED}✗ Login failed${NC}"
        exit 1
    }
    echo -e "${GREEN}✓ Logged in successfully${NC}"
fi
echo ""

# Step 4: Push image
echo -e "${BLUE}[4/5] Pushing to Docker Hub...${NC}"
echo -e "${YELLOW}Pushing tag: ${VERSION_TAG}${NC}"
if docker push "${REPO}:${VERSION_TAG}"; then
    echo -e "${GREEN}✓ Pushed: ${REPO}:${VERSION_TAG}${NC}"
else
    echo -e "${RED}✗ Push failed${NC}"
    exit 1
fi

if [ "${VERSION_TAG}" != "${LATEST_TAG}" ]; then
    echo -e "${YELLOW}Pushing tag: ${LATEST_TAG}${NC}"
    if docker push "${REPO}:${LATEST_TAG}"; then
        echo -e "${GREEN}✓ Pushed: ${REPO}:${LATEST_TAG}${NC}"
    else
        echo -e "${RED}✗ Push latest failed${NC}"
        exit 1
    fi
fi
echo ""

# Step 5: Verify
echo -e "${BLUE}[5/5] Verifying on Docker Hub...${NC}"
echo -e "${GREEN}✓ Image successfully pushed!${NC}"
echo ""
echo -e "${GREEN}========================================${NC}"
echo -e "${GREEN}Deployment Information${NC}"
echo -e "${GREEN}========================================${NC}"
echo ""
echo -e "${BLUE}Repository:${NC} ${REPO}"
echo -e "${BLUE}Version:${NC} ${VERSION_TAG}"
echo -e "${BLUE}Latest:${NC} ${LATEST_TAG}"
echo ""
echo -e "${BLUE}View on Docker Hub:${NC}"
echo "https://hub.docker.com/r/${REPO}"
echo ""
echo -e "${BLUE}To deploy on a server, run:${NC}"
echo "docker pull ${REPO}:${VERSION_TAG}"
echo "docker compose pull && docker compose up -d"
echo ""
echo -e "${GREEN}✓ Build and push completed successfully!${NC}"
