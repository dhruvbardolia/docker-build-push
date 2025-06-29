# 🚀 Multi-Registry Docker Build & Push GitHub Action

This GitHub Action builds and pushes Docker images to various container registries including:

- 🟡 AWS ECR (Elastic Container Registry)
- 🔵 Google Artifact Registry (GCR)
- 🟣 Azure Container Registry (ACR)
- ⚪ Docker Hub

---

## ✨ Features

- Composite action with cross-platform support
- Caching support via previous image version
- Secure credentials usage via GitHub secrets
- Build-time arguments support

---

## 🔧 Inputs

| Name                    | Required | Description |
|-------------------------|----------|-------------|
| `registry`              | ✅       | Target registry type: `ecr`, `gcr`, `acr`, or `dockerhub` |
| `image`                 | ✅       | Docker image name (e.g., `my-app`) |
| `image-version`         | ✅       | Docker image tag (e.g., `latest`, `v1.0.0`) |
| `image-dockerfile`      | ✅       | Path to the Dockerfile |
| `args`                  | ❌       | Additional build arguments |
| `image-previous-version`| ❌       | Previous image tag to use for build cache |
| `aws-role`              | ⚠️ Only for ECR | AWS IAM role to assume |
| `aws-region`            | ⚠️ Only for ECR | AWS region |
| `project-id`            | ⚠️ Only for GCR | GCP project ID |
| `username`              | ⚠️ For DockerHub/ACR/GCR | Registry username or `_json_key` for GCR |
| `password`              | ⚠️ For DockerHub/ACR/GCR | Password, token, or service account JSON |
| `registry-url`          | ⚠️ Only for ACR | ACR registry URL (e.g., `yourregistry.azurecr.io`) |

---

## 📦 Outputs

| Name     | Description              |
|----------|--------------------------|
| `image`  | Full pushed image name (with tag) |

---

## 🧪 Example Workflows

### ✅ AWS ECR

```yaml
uses: dhruvbardolia/docker-build-push@v2
with:
  registry: ecr
  aws-role: arn:aws:iam::123456789012:role/github-ecr-role
  aws-region: us-east-1
  image: my-api
  image-version: latest
  image-dockerfile: Dockerfile
