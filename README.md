# trollpurse-ops

CloudFormation Templates used by [Troll Purse](https://trollpurse.com). Hobby game development.

## Features

This repository exposes features for the Continuous Integration pipeline for building games. Below is a list of supported features. Continuous Deployment will be coming soon.

- [X] Serverless Git LFS
  - [X] GitHub Authentication
  - [ ] BitBucket Authentication
  - [ ] HTTP Basic Authorization Header
- [X] Game Engine Builds
  - [X] Custom Game/Engine
  - [X] Unreal Engine 4
  - [ ] Unity
  - [ ] Lumberyard
- [X] Source Control Management Integration
  - [X] GitHub
  - [ ] Bitbucket
  - [ ] CodeCommit
  - [ ] Helix Core
- [ ] Distribute Client Packages
  - [ ] Itch.io
  - [ ] Steam
  - [ ] GameJolt
- [ ] Distribute Server Packages
  - [ ] GameLift - EC2
  - [ ] GameLift - ECS

## Getting Started

Below is a list of what you need to get started.

### AWS Account (Required)

You will need access to an AWS Account and a user that has access to CodePipeline and the related suite of developer tools. If you do not have an AWS Account, you will need an email and credit card to [Sign Up for AWS](https://aws.amazon.com/free).

### GitHub Integration (Optional)

If you are using any of the GitHub pipelines, you will need to sign into the AWS Account that is using said integration and navigate to CodeBuild. There you will be able to add credentials for that account to access GitHub. This is a one time per account configuration. [More on this here](https://docs.aws.amazon.com/codebuild/latest/userguide/sample-access-tokens.html).

The Unreal Engine 4 builder will require a GitHub Personal Access Token as well to execute UE4 source builds. Here is the documentation on [generating Personal Access Tokens](https://docs.github.com/en/free-pro-team@latest/github/authenticating-to-github/creating-a-personal-access-token).

We would recommend one Personal Access Token per service requiring it. So if you are doing a GitHub Integration with a UE4 build, generate two (2) tokens.

### Unreal Engine 4 Licensing (Optional)

To use UE4, you must [sign up and agree to the EULA](https://www.unrealengine.com/en-US/download). With the CI/CD pipelines, we do use docker containers that _must_ remain private, which is the default configuration. They are stored in AWS ECR, and only the build pipelines will have access. When continuous deployment is enabled, you will need to add an `appspec.yml` file for your project. See [CodeDeploy Documentation](https://docs.aws.amazon.com/codedeploy/) for more details.

### Custom Game Engine/Project

Once you execute the cloud formation script for "custom" projects, simply add a `buildspec.yml` file to your project and add the commands needed to build. See [CodeBuild Documentation](https://docs.aws.amazon.com/codebuild/) for more details. When continuous deployment is enabled, you will need to add an `appspec.yml` file for your project. See [CodeDeploy Documentation](https://docs.aws.amazon.com/codedeploy/) for more details.

## Deploying This Project

This project has a 3-step deployment phase. The first step is to bootstrap, this will create a build project for this repo so you will get the latest updates (you can point it to a fork to keep control of costs). The second step is to create pipelines for each of your projects.

> __Advanced Users__
> There is an optional intermediate step (not provided) where you can create another CodePipeline project that listens to the Artifact Bucket from Part A to trigger CloudFormation stack updates on all of your stacks generated in Phases One and Two.

### Phase One - Bootstrap Part A


### Phase Two - Bootstrap Part B


### Phase Three - For Each New Project

Using the magic links from Phase One, you can now use project specific CloudFormation templates. The next section will demonstrate scripts for default configurations and specific engine builds.

## Per Project Deployments

There are currently two supported configurations for per project pipelines. These pipelines are specifically for continuous integration. This means it will pull the project when pushed to the specific build branch (default is `main`) from github (currently). The final output will be an S3 bucket with the client application. So we currently support build pipelines for single player games. However, you can easily fork this repository and start plopping in support for server fleets.

### Custom Engine



### Unreal Engine 4

