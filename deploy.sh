#!/bin/bash

# guindo.me Deployment Script
# This script automates the deployment process for both frontend and backend

set -e

echo "🚀 Starting guindo.me deployment..."

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if required tools are installed
check_dependencies() {
    print_status "Checking dependencies..."
    
    if ! command -v node &> /dev/null; then
        print_error "Node.js is not installed"
        exit 1
    fi
    
    if ! command -v npm &> /dev/null; then
        print_error "npm is not installed"
        exit 1
    fi
    
    if ! command -v python3.11 &> /dev/null; then
        print_error "Python 3.11 is not installed"
        exit 1
    fi
    
    print_status "All dependencies are installed"
}

# Deploy Frontend to Vercel
deploy_frontend() {
    print_status "Deploying frontend to Vercel..."
    
    cd web/frontend
    
    # Install dependencies
    npm install
    
    # Build project
    npm run build
    
    # Deploy to Vercel
    if command -v vercel &> /dev/null; then
        vercel --prod
    else
        print_warning "Vercel CLI not found. Please install it with: npm i -g vercel"
        print_warning "Then run: cd web/frontend && vercel --prod"
        return 1
    fi
    
    cd ../..
    print_status "Frontend deployment completed"
}

# Deploy Backend to Railway
deploy_backend() {
    print_status "Deploying backend to Railway..."
    
    cd web/backend
    
    # Install dependencies
    python3.11 -m pip install -r requirements.txt
    
    # Deploy to Railway
    if command -v railway &> /dev/null; then
        railway up
    else
        print_warning "Railway CLI not found. Please install it with: npm install -g @railway/cli"
        print_warning "Then run: cd web/backend && railway up"
        return 1
    fi
    
    cd ../..
    print_status "Backend deployment completed"
}

# Main deployment flow
main() {
    print_status "Starting deployment process for guindo.me"
    
    check_dependencies
    
    # Deploy frontend
    if ! deploy_frontend; then
        print_error "Frontend deployment failed"
        exit 1
    fi
    
    # Deploy backend
    if ! deploy_backend; then
        print_error "Backend deployment failed"
        exit 1
    fi
    
    print_status "🎉 Deployment completed successfully!"
    print_status "Next steps:"
    print_status "1. Configure environment variables in Vercel and Railway"
    print_status "2. Set up DNS records for guindo.me"
    print_status "3. Test the deployment"
}

# Run main function
main "$@"