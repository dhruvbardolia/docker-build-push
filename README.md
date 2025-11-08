# 🚀 Multi-Registry Docker Build & Push GitHub Action

This composite GitHub Action builds and pushes Docker images to:

- 🟡 AWS Elastic Container Registry (ECR)
- 🔵 Google Artifact Registry / Container Registry (GCR)
- 🟣 Azure Container Registry (ACR)
- ⚪ Docker Hub

It authenticates, builds (optionally with cache + build arguments), and pushes the image, then shares the resulting reference with downstream steps.

---

## ✨ Features

- Composite action — no Docker-in-Docker setup required
- Registry-specific authentication flows (AWS STS + Docker logins) handled for you
- Optional layer caching via a previously pushed image tag
- Multi-line build argument input automatically mapped to `--build-arg`
- Outputs the fully qualified image name (`registry/repo:tag`)

---

## 🚦 Usage

```yaml
jobs:
  build:
    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@v4

      - name: Build & push
        uses: dhruvbardolia/docker-build-push@v2
        with:
          registry: <ecr|gcr|acr|dockerhub>
          image: my-service
          image-version: ${{ github.sha }}
          image-dockerfile: ./Dockerfile
          args: |
            NODE_ENV=production
            API_BASE_URL=https://api.example.com
          image-previous-version: 123456789012.dkr.ecr.us-east-1.amazonaws.com/my-service:latest
          # plus the registry-specific inputs described below
```

---

## 🔧 Inputs

| Name                     | Required | Description |
|--------------------------|----------|-------------|
| `registry`               | ✅       | Registry to target: `ecr`, `gcr`, `acr`, or `dockerhub`. |
| `image`                  | ✅       | Repository/name portion of the image (registry hostname is added automatically). |
| `image-version`          | ✅       | Tag for the image (e.g., `latest`, `v1.0.0`, `${{ github.sha }}`). |
| `image-dockerfile`       | ✅       | Path to the Dockerfile relative to the repository root. |
| `args`                   | ❌       | Multi-line list of `KEY=VALUE` pairs, each converted to `--build-arg KEY=VALUE`. Leave empty to skip. |
| `image-previous-version` | ❌       | Fully-qualified image reference (`registry/repo:tag`) used as a cache source. Enables `docker buildx build` with inline cache metadata. |
| `aws-role`               | ⚠️ ECR   | IAM role ARN assumed via `aws-actions/configure-aws-credentials`. Leave blank if credentials are already configured. |
| `aws-region`             | ⚠️ ECR   | AWS region used for ECR authentication and registry hostname. Required when `registry=ecr`. |
| `project-id`             | ⚠️ GCR   | GCP project ID appended to `gcr.io/<project-id>`. |
| `username`               | ⚠️ ACR/GCR/DockerHub | Registry username. Use `_json_key` when authenticating to GCR with a service account JSON. |
| `password`               | ⚠️ ACR/GCR/DockerHub | Password, token, or raw GCP service account JSON (store securely in GitHub Secrets). |
| `registry-url`           | ⚠️ ACR   | ACR login server (e.g., `myregistry.azurecr.io`). Not required for the other registries. |

---

## 📦 Outputs

| Name    | Description |
|---------|-------------|
| `image` | Fully-qualified image reference (`registry/repository:tag`) that was pushed. |

---

## 🧠 How it works

1. **AWS credential setup** (ECR only) — calls `aws-actions/configure-aws-credentials@v1` and assumes `aws-role` when provided.
2. **Registry login** — runs the appropriate Docker login command and exports `REGISTRY_URL` for later steps. ECR and GCR URLs are constructed automatically; ACR uses the provided `registry-url`.
3. **Build** — converts the optional `args` input into `--build-arg` flags. When `image-previous-version` is provided, the action switches to `docker buildx build` with remote cache sources/targets; otherwise it uses `docker build`.
4. **Push & output** — pushes the image to the selected registry and writes the final reference to the `image` output for downstream jobs.

---

## 🧪 Example Workflows

### ✅ AWS ECR

```yaml
jobs:
  build:
    runs-on: ubuntu-latest
    permissions:
      id-token: write
      contents: read
    steps:
      - uses: actions/checkout@v4
      - name: Build & push to ECR
        uses: dhruvbardolia/docker-build-push@v2
        with:
          registry: ecr
          aws-role: arn:aws:iam::123456789012:role/github-ecr-role
          aws-region: us-east-1
          image: my-api
          image-version: ${{ github.sha }}
          image-dockerfile: ./Dockerfile
          image-previous-version: 123456789012.dkr.ecr.us-east-1.amazonaws.com/my-api:latest
```

### 🔵 Google Artifact Registry / GCR

```yaml
steps:
  - uses: actions/checkout@v4
  - name: Build & push to GCR
    uses: dhruvbardolia/docker-build-push@v2
    with:
      registry: gcr
      project-id: my-gcp-project
      username: _json_key
      password: ${{ secrets.GCP_ARTIFACT_REGISTRY_JSON }}
      image: services/my-api
      image-version: ${{ github.sha }}
      image-dockerfile: ./Dockerfile
```

### 🟣 Azure Container Registry

```yaml
steps:
  - uses: actions/checkout@v4
  - name: Build & push to ACR
    uses: dhruvbardolia/docker-build-push@v2
    with:
      registry: acr
      registry-url: myregistry.azurecr.io
      username: ${{ secrets.ACR_USERNAME }}
      password: ${{ secrets.ACR_PASSWORD }}
      image: api
      image-version: ${{ github.run_number }}
      image-dockerfile: ./Dockerfile
```

### ⚪ Docker Hub

```yaml
steps:
  - uses: actions/checkout@v4
  - name: Build & push to Docker Hub
    uses: dhruvbardolia/docker-build-push@v2
    with:
      registry: dockerhub
      username: ${{ secrets.DOCKERHUB_USERNAME }}
      password: ${{ secrets.DOCKERHUB_TOKEN }}
      image: my-org/my-api
      image-version: ${{ github.ref_name }}
      image-dockerfile: ./Dockerfile
```
