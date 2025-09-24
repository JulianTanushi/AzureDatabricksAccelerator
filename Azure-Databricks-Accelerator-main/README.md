# Azure Databricks Accelerator
Welcome to the Azure Databricks Provisioning in a Private Network repository! This repository contains code and documentation to help you deploy Azure Databricks in a secure, private network environment. It is designed to accelerate customer adoption by providing best practices, sample configurations, and comprehensive guides.

## Contents

- [Introduction](#introduction)
- [Prerequisites](#prerequisites)
- [Architecture](#architecture)
- [Getting Started](#getting-started)
- [Configuration Files](#configuration-files)
- [Deployment](#deployment)
- [Best Practices](#best-practices)
- [Troubleshooting](#troubleshooting)
- [Contributing](#contributing)
- [License](#license)

## Introduction

This repository provides a comprehensive guide to provisioning Azure Databricks in a private network. It includes Terraform scripts, ARM templates, and configuration files to help you set up and configure your Azure Databricks environment securely and efficiently.

## Prerequisites

Before you begin, ensure you have the following:

- An Azure subscription
- Azure CLI installed and configured
- Terraform installed
- Permissions to create resources in your Azure subscription

## Architecture

The architecture involves deploying Azure Databricks in a private network with the following components:

- Azure Virtual Network (VNet)
- Subnets for different Azure Databricks components
- Network Security Groups (NSGs) for traffic control
- Azure Databricks workspace
- Integration with Azure Key Vault for secret management
- Private Endpoints for secure connectivity

## Getting Started

To get started, follow these steps:

1. **Clone the Repository**:
    ```bash
    git clone https://github.com/jtanushi_microsoft/Azure-Databricks-Accelerator.git
    cd Azure-Databricks-Accelerator
    ```

2. **Set Up Configuration**:
    Update the configuration files with your Azure subscription details, resource group names, and other necessary parameters.

## Configuration Files

The repository includes several configuration files:

- `main.tf`: The main Terraform script for provisioning resources
- `variables.tf`: Variable definitions for customizable parameters
- `outputs.tf`: Outputs for tracking resource details
- `databricks.tf`: Specific configurations for Azure Databricks

## Deployment

Deploy the Azure Databricks environment using Terraform:

1. **Initialize Terraform**:
    ```bash
    terraform init
    ```

2. **Plan the Deployment**:
    ```bash
    terraform plan
    ```

3. **Apply the Deployment**:
    ```bash
    terraform apply
    ```

Follow the prompts to confirm the deployment.

## Best Practices

Here are some best practices for deploying Azure Databricks in a private network:

- Use separate subnets for different Azure Databricks components to enhance security.
- Implement Network Security Groups (NSGs) to control traffic between subnets.
- Integrate with Azure Key Vault to manage secrets securely.
- Use Private Endpoints to limit exposure to the public internet.


By following this guide, you can securely provision Azure Databricks in a private network, ensuring a robust and efficient deployment. If you have any questions or need further assistance, please feel free to raise an issue in the repository.

Happy deploying!
