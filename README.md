# trollpurse-trollops

CloudFormation Templates used by [Troll Purse](https://trollpurse.com). Hobby game development.

## Features

This repository exposes features for the Continuous Integration pipeline for building games. Below is a list of supported features.

- [X] Serverless Git LFS
  - [X] GitHub Authentication
  - [] BitBucket Authentication
  - [] HTTP Basic Authorization Header
- [X] Game Engine Builds
  - [X] Custom
  - [X] Unreal Engine 4
  - [] Unity
  - [] Lumberyard
- [X] Source Control Management Integration
  - [X] Git
    - [X] GitHub
    - [] Bitbucket
    - [] CodeCommit
  - [] Perforce
    - [] Helix Core
    - [] Assembla
- [] Distribute Client Packages
  - [] Itch.io
  - [] Steam

## Getting Started

Below is a list of what you need to get started.

### AWS

You will need access to an AWS Account and a user that has access to CodePipeline and the related suite of developer tools. If you do not have an AWS Account, you will need an email and credit card to [Sign Up for AWS](https://aws.amazon.com/free).

### CloudFormation

Execute the two scripts below. This will create a CodePipeline to manage the CloudFormation for the CI/CD CodePipeline. If you do not wish to get or use automatic updates, simply copy the `./lfs` and `./ops` folders to an S3 bucket or upload the files via the CloudFormation Console. See [Cloud Formation Get Started](https://aws.amazon.com/cloudformation/getting-started/) if you are not familiar with how to use Cloud Formation.

### Unreal Engine 4

To use UE4, you must [sign up and agree to the EULA](https://www.unrealengine.com/en-US/download). With the CI/CD pipelines, we do use docker containers that _must_ remain private, which is the default configuration. They are stored in AWS ECR, and only the build pipelines will have access.
