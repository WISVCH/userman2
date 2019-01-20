workflow "Build and deploy on push to master" {
  on = "push"
  resolves = ["Push image"]
}

action "Filter master branch" {
  uses = "actions/bin/filter@master"
  args = "branch master"
}

action "Build Docker image" {
  uses = "actions/docker/cli@master"
  args = "build -t quay.io/wisvch/userman2:$GITHUB_SHA ."
  needs = ["Filter master branch"]
}

action "Log in to Quay" {
  uses = "actions/docker/login@master"
  needs = ["Build Docker image"]
  secrets = ["DOCKER_USERNAME", "DOCKER_PASSWORD", "DOCKER_REGISTRY_URL"]
}

action "Push image" {
  uses = "actions/docker/cli@master"
  needs = ["Log in to Quay"]
  args = "push quay.io/wisvch/userman2:$GITHUB_SHA"
}
