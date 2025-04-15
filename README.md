# Vision One Container Security for AWS EKS

This repository contains GitHub Actions workflows for managing AWS EKS (Elastic Kubernetes Service) clusters and deploying Trend Micro Vision One Container Security.

## Workflows

### 1. Create EKS Cluster
Creates a new AWS EKS cluster with the specified configuration.

**Workflow file:** `.github/workflows/create-eks-cluster.yml`

**Parameters:**
- Customer Name
- Cluster Name
- SSH Key Name (must exist in AWS)
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

### 3. Deploy Vision One Container Security
Deploys Trend Micro Vision One Container Security solution to an existing EKS cluster.

**Workflow file:** `.github/workflows/deploy-v1cs-to-eks-split.yml`

**Parameters:**
- Vision One Container Security Policy ID
- Vision One Container Security Group ID
- EKS Cluster Name
- AWS Region
- Namespaces to exclude (comma-separated)

### 4. Create Vision One Container Security Policy
Creates a new Vision One Container Security policy and associated ruleset.

**Workflow file:** `.github/workflows/create-v1cs-policy.yml`

**Parameters:**
- Ruleset Name
- Policy Name

### 5. Uninstall Vision One Container Security
Removes Vision One Container Security from an EKS cluster and deregisters it from Vision One.

**Workflow file:** `.github/workflows/uninstall-v1cs-from-eks.yml`

**Parameters:**
- EKS Cluster Name
- AWS Region
- Vision One Cluster ID
- Skip Vision One Deregistration (optional)

## Prerequisites

1. **AWS Credentials**: Store these as GitHub secrets
   - `AWS_ACCESS_KEY_ID`
   - `AWS_SECRET_ACCESS_KEY`
   
   Your AWS IAM user needs permissions to:
   - Create/manage EKS clusters
   - Create/manage EC2 resources
   - Read EC2 key pairs (no create permission needed)

2. **SSH Key Pair**: Create an SSH key pair with your desired name in your target AWS region before running the cluster creation workflow

3. **Vision One Container Security**: For Vision One Container Security workflows
   - `CONTAINER_SECURITY_API_KEY` - Your Vision One API key with Container Security permissions

4. **GitHub Repository Variables**: Set these in your repository settings
   - `AWS_REGION` - The AWS region where your cluster is created
   - `EKS_CLUSTER_NAME` - The name of your EKS cluster (set automatically after creation)

## Directory Structure

```
.
├── .github
│   └── workflows
│       ├── create-eks-cluster.yml
│       ├── delete-eks-cluster.yml
│       ├── deploy-v1cs-to-eks-split.yml
│       ├── create-v1cs-policy.yml
│       └── uninstall-v1cs-from-eks.yml
├── trendmicro
│   ├── policy.json
│   ├── runtimeruleset.json
│   ├── overrides.yaml
│   └── scripts/
│       ├── check_policy.py
│       ├── check_ruleset.py
│       ├── create_policy.py
│       ├── create_ruleset.py
│       └── delete_ruleset.py
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
   - SSH Key Name (must exist in AWS)
   - Kubernetes Version
   - Node Instance Type
   - Node Count
   - AWS Region
5. Click "Run workflow" to start the creation process

Once the cluster is created, the workflow will automatically set the `EKS_CLUSTER_NAME` GitHub variable.

### Deploying Vision One Container Security

1. Create a Vision One Container Security policy (if needed):
   - Go to the "Actions" tab in your GitHub repository
   - Select the "Create Vision One Container Security Policy" workflow
   - Enter the desired ruleset and policy names
   - Run the workflow

2. Deploy Vision One Container Security to your EKS cluster:
   - Go to the "Actions" tab in your GitHub repository
   - Select the "Deploy Vision One Container Security" workflow
   - Fill in the required parameters:
     - Vision One Container Security Policy ID (created in the previous step)
     - Vision One Container Security Group ID
     - EKS Cluster Name
     - AWS Region
     - Namespaces to exclude (comma-separated, default: kube-system)
   - Run the workflow

The workflow will:
- Connect to your EKS cluster
- Check for any existing Trend Micro installation
- Create the necessary Kubernetes secret with your Vision One API key
- Deploy the Vision One Container Security Helm chart
- Wait for the cluster to register with Vision One
- Display the Vision One Cluster ID for future reference

### Uninstalling Vision One Container Security

1. Go to the "Actions" tab in your GitHub repository
2. Select the "Uninstall Vision One Container Security" workflow
3. Fill in the required parameters:
   - EKS Cluster Name
   - AWS Region
   - Vision One Cluster ID (obtained from the deployment summary)
   - Skip Vision One Deregistration (optional)
4. Run the workflow

The workflow will:
- Connect to your EKS cluster
- Uninstall the Trend Micro Helm chart
- Remove the trendmicro-system namespace
- Deregister the cluster from Vision One

### Deleting the Cluster

1. Go to the "Actions" tab in your GitHub repository
2. Select the "Delete EKS Cluster" workflow
3. Click "Run workflow"
4. Fill in the cluster name and region
5. Type "DELETE" in the confirmation field
6. Click "Run workflow" to start the deletion process

## Vision One Container Security

### Policy and Ruleset Management

The repository contains templates for Vision One Container Security policies and rulesets in the `trendmicro` directory:

- `policy.json`: Template for a container security policy
- `runtimeruleset.json`: Template for runtime security rules
- `overrides.yaml`: Helm chart configuration values

The `scripts` subdirectory contains Python scripts used by the policy creation workflow:
- `check_policy.py`: Checks if a policy exists in Vision One
- `check_ruleset.py`: Checks if a ruleset exists in Vision One
- `create_policy.py`: Creates a new policy in Vision One
- `create_ruleset.py`: Creates a new ruleset in Vision One
- `delete_ruleset.py`: Deletes a ruleset from Vision One if needed

### Workflow Dependencies

The workflows are designed to work together:

1. Create a Vision One Container Security policy with `create-v1cs-policy.yml`
2. Deploy Vision One Container Security to your EKS cluster with `deploy-v1cs-to-eks-split.yml`
3. When needed, uninstall Vision One Container Security with `uninstall-v1cs-from-eks.yml`

## Cost Considerations

**Important:** Running EKS clusters and security services incurs AWS charges and may incur Trend Micro charges. Make sure to delete clusters and uninstall services when they're no longer needed to avoid unnecessary costs.

## Customization

You can customize the workflows by modifying the YAML files in the `.github/workflows` directory. Common customizations include:

- Changing the node instance types
- Adjusting auto-scaling parameters
- Modifying Vision One Container Security policy settings
- Customizing the Helm chart values in `overrides.yaml`
