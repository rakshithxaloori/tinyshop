# TinyShop Monorepo

## Overview

This monorepo contains all the necessary components to run a multi-tenant e-commerce platform, including an AI-powered store editor, backend services, cloud infrastructure, and SDKs for developers. Each project is structured to ensure modularity, scalability, and ease of development.

## Projects

| Repository Name        | Function                                                                                    |
| ---------------------- | ------------------------------------------------------------------------------------------- |
| **ai-editor**          | An editor that allows merchants to customize their e-commerce store using natural language. |
| **api**                | The multi-tenant FastAPI backend handling store logic, user management, and transactions.   |
| **aws-cloudformation** | CloudFormation scripts for provisioning and hosting the API infrastructure.                 |
| **dashboard**          | A dashboard for merchants to manage their store, products, and orders.                      |
| **docs**               | Developer documentation to interact with the store programmatically.                        |
| **node-sdk**           | A Stripe-like Node.js SDK that provides an easy-to-use wrapper around the API.              |
| **proxy-api**          | A reverse proxy that routes traffic based on the secret key type in API requests.           |
| **storefront**         | The e-commerce storefront where merchants' customers browse and place orders.               |

## Getting Started

### Prerequisites

Ensure you have the following installed:

- Node.js (latest LTS)
- Python 3.9+
- Docker (for containerized deployments)
- AWS CLI (for CloudFormation deployments)
