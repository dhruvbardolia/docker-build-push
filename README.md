# 🚀 Docker Build & Push Action

This is a GitHub Composite Action to build and push Docker images to Amazon ECR, with caching support and dynamic build arguments.

## 🔧 Inputs

| Name                   | Required | Description                                  |
|------------------------|----------|----------------------------------------------|
| `aws-role`             | ✅        | AWS IAM role to assume                       |
| `aws-region`           | ✅        | AWS region                                   |
| `image-dockerfile`     | ✅        | Path to the Dockerfile                       |
| `image`                | ✅        | Docker image name (e.g., my-app)             |
| `image-version`        | ❌        | Image version/tag                            |
| `image-previous-version` | ❌     | Previous image version (for build caching)   |
| `args`                 | ❌        | Additional build arguments (as string)       |

## 📦 Outputs

| Name   | Description            |
|--------|------------------------|
| `image`| The full image name    |

## 📘 Example Usage

```yaml
jobs:
  docker:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout code
        uses: actions/checkout@v3

      - name: Build and push Docker image
        uses: dhruvbardolia/docker-build-push@v1
        with:
          aws-role: arn:aws:iam::123456789012:role/github-ecr-role
          aws-region: us-east-1
          image-dockerfile: ./Dockerfile
          image: my-app
          image-version: latest
