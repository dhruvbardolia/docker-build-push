import os
import subprocess
import sys

registry = os.getenv("INPUT_REGISTRY")
image = os.getenv("INPUT_IMAGE")
image_version = os.getenv("INPUT_IMAGE_VERSION")
dockerfile = os.getenv("INPUT_IMAGE_DOCKERFILE")
args = os.getenv("INPUT_ARGS", "")
prev_version = os.getenv("INPUT_IMAGE_PREVIOUS_VERSION", "")
username = os.getenv("INPUT_USERNAME", "")
password = os.getenv("INPUT_PASSWORD", "")
aws_role = os.getenv("INPUT_AWS_ROLE", "")
aws_region = os.getenv("INPUT_AWS_REGION", "")
project_id = os.getenv("INPUT_PROJECT_ID", "")
registry_url = os.getenv("INPUT_REGISTRY_URL", "")

def run(cmd, mask=False):
    if not mask:
        print(f"Running: {cmd}")
    result = subprocess.run(cmd, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    return result.stdout.decode().strip()

def login():
    global registry_url
    if registry == "ecr":
        print("🔐 Logging into AWS ECR...")
        run(f"aws configure set region {aws_region}")
        account_id = run("aws sts get-caller-identity --query Account --output text")
        registry_url = f"{account_id}.dkr.ecr.{aws_region}.amazonaws.com"
        login_cmd = f"aws ecr get-login-password --region {aws_region} | docker login --username AWS --password-stdin {registry_url}"
        run(login_cmd)
    elif registry == "gcr":
        print("🔐 Logging into GCR...")
        run(f"echo '{password}' | docker login -u _json_key https://gcr.io --password-stdin")
        registry_url = f"gcr.io/{project_id}"
    elif registry == "acr":
        print("🔐 Logging into ACR...")
        run(f"echo '{password}' | docker login {registry_url} -u {username} --password-stdin")
    elif registry == "dockerhub":
        print("🔐 Logging into Docker Hub...")
        run(f"echo '{password}' | docker login -u {username} --password-stdin")
        registry_url = "docker.io"
    else:
        print(f"❌ Unsupported registry type: {registry}")
        sys.exit(1)

def build_and_push():
    full_image = f"{registry_url}/{image}:{image_version}"
    print(f"🛠 Building and pushing image: {full_image}")

    build_args = " ".join([f"--build-arg {arg.strip()}" for arg in args.split() if arg.strip()])
    if prev_version:
        cmd = f"docker buildx build -t {full_image} {build_args} -f {dockerfile} . --cache-to type=inline --cache-from type=registry,ref={prev_version}"
    else:
        cmd = f"docker build -t {full_image} {build_args} -f {dockerfile} ."

    run(cmd)
    run(f"docker push {full_image}")

    # Set GitHub Action output
    with open(os.environ["GITHUB_OUTPUT"], "a") as f:
        f.write(f"image={full_image}\n")

if __name__ == "__main__":
    try:
        login()
        build_and_push()
    except subprocess.CalledProcessError as e:
        print(f"❌ Command failed:\n{e.stderr.decode().strip()}")
        sys.exit(1)
