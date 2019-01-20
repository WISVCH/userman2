workflow "Build and deploy on push to master" {
  on = "push"
  resolves = ["Push latest image"]
}

action "Filter master branch" {
  uses = "actions/bin/filter@master"
  args = "branch master"
  needs = ["Build Docker image"]
}

action "Build Docker image" {
  uses = "actions/docker/cli@master"
  args = "build -t userman2 ."
}

action "Log in to Quay" {
  uses = "actions/docker/login@master"
  needs = ["Filter master branch"]
  secrets = ["DOCKER_USERNAME", "DOCKER_PASSWORD", "DOCKER_REGISTRY_URL"]
}

action "Docker Tag" {
  uses = "actions/docker/tag@master"
  needs = ["Filter master branch"]
  args = "userman2 quay.io/wisvch/userman2"
}

action "Push image" {
  uses = "actions/docker/cli@master"
  needs = ["Log in to Quay", "Docker Tag"]
  args = "push quay.io/wisvch/userman2:$IMAGE_SHA"
}

action "Push latest image" {
  uses = "actions/docker/cli@master"
  needs = ["Push image"]
  args = "push quay.io/wisvch/userman2:latest"
}
