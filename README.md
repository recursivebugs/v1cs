# AWS EKS Cluster Management with GitHub Actions

This repository contains GitHub Actions workflows for creating, deploying to, and deleting AWS EKS (Elastic Kubernetes Service) clusters.

## Workflows

### 1. Create EKS Cluster
Creates a new AWS EKS cluster with the specified configuration.

**Workflow file:** `.github/workflows/create-eks-cluster.yml`

**Parameters:**
- Cluster Name
- Kubernetes Version
- Node Instance Type
- Node Count
- AWS Region

### 2. Delete EKS Cluster
Safely deletes an existing AWS EKS cluster.

**Workflow file:** `.github/workflows/delete-eks-cluster.yml`

**Parameters:**
- Cluster Name
- AWS Region
- Confirmation (type "DELETE" to confirm)

### 3. Deploy to EKS
Builds, scans, and deploys a Docker image to the EKS cluster.

**Workflow file:** `.github/workflows/deploy-to-eks.yml`

## Prerequisites

1. **AWS Credentials**: Store these as GitHub secrets
   - `AWS_ACCESS_KEY_ID`
   - `AWS_SECRET_ACCESS_KEY`
   
   Your AWS IAM user needs permissions to:
   - Create/manage EKS clusters
   - Create/manage EC2 resources
   - Read EC2 key pairs (no create permission needed)
   - Push to ECR repositories

2. **SSH Key Pair**: Create an SSH key pair named `keyNameCluster` in your target AWS region before running the cluster creation workflow

2. **GitHub Repository Variables**: Set these in your repository settings
   - `AWS_REGION` - The AWS region where your cluster is created
   - `EKS_CLUSTER_NAME` - The name of your EKS cluster (set automatically after creation)
   - `ECR_REPOSITORY_NAME` - Your Amazon ECR repository name
   - `SECURITY_MODE` - Set to "protect" to fail the workflow on critical security issues, or "log" to continue

3. **Application Secrets**: For deployment
   - `APP_KEY` - Your application key
   - `DB_PASSWORD` - Database password

## Directory Structure

```
.
├── .github
│   └── workflows
│       ├── create-eks-cluster.yml
│       ├── delete-eks-cluster.yml
│       └── deploy-to-eks.yml
├── k8s
│   ├── deployment.yaml (generated during deployment)
│   └── service.yaml (generated during deployment)
├── Dockerfile
└── README.md
```

## Usage

### Creating an EKS Cluster

1. Go to the "Actions" tab in your GitHub repository
2. Select the "Create EKS Cluster" workflow
3. Click "Run workflow"
4. Fill in the required parameters:
   - Customer Name (defaults to "DemoCluster001")
   - Cluster Name
   - Kubernetes Version
   - Node Instance Type
   - Node Count
   - AWS Region
5. Click "Run workflow" to start the creation process

Once the cluster is created, the workflow will automatically set the `EKS_CLUSTER_NAME` GitHub variable.

#### SSH Access Prerequisites

Before running the cluster creation workflow, you must create an SSH key pair named `keyNameCluster` in your target AWS region. This is a security requirement to prevent private keys from being stored in GitHub.

To create the key pair:

1. Log in to the AWS Management Console
2. Navigate to EC2 > Key Pairs
3. Click "Create key pair"
4. Enter "keyNameCluster" as the name
5. Select the key pair type (RSA)
6. Select the private key file format (.pem)
7. Click "Create key pair"
8. Save the downloaded .pem file securely on your local machine

#### SSH Access to Worker Nodes

To SSH into a worker node:

1. Use the `keyNameCluster.pem` key you downloaded when creating the key pair
2. Find the public IP of the node you want to access
3. Connect using:
   ```
   ssh -i /path/to/keyNameCluster.pem ec2-user@<NODE_PUBLIC_IP>
   ```

### Deploying to the Cluster

1. Push to your main branch or manually trigger the "Build and Deploy to EKS" workflow
2. The workflow will:
   - Build your Docker image
   - Scan it for vulnerabilities
   - Push it to Amazon ECR
   - Deploy it to your EKS cluster with appropriate configuration

### Deleting the Cluster

1. Go to the "Actions" tab in your GitHub repository
2. Select the "Delete EKS Cluster" workflow
3. Click "Run workflow"
4. Fill in the cluster name and region
5. Type "DELETE" in the confirmation field
6. Click "Run workflow" to start the deletion process

## Security Features

The deployment workflow includes a vulnerability scan using Trivy. In "protect" mode, the workflow will fail if critical vulnerabilities are found.

## Cost Considerations

**Important:** Running EKS clusters incurs AWS charges. Make sure to delete clusters when they're no longer needed to avoid unnecessary costs.

## Customization

You can customize the workflows by modifying the YAML files in the `.github/workflows` directory. Common customizations include:

- Changing the node instance types
- Adjusting auto-scaling parameters
- Modifying deployment configurations
- Adding additional security scans