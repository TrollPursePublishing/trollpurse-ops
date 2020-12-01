# trollpurse-ops

CloudFormation Templates used by [Troll Purse](https://trollpurse.com). Hobby game development.

## Why

This project provides a low server management model (commonly known as "serverless") for managing Continuous Integration (CI) and Continuous Deployment (CD) for common source control management services, popular game engines, and well known storefronts for video games and game related products.

The primary focus is Continuous Integration for Git stored game products. The reason this came about is due to the amount of storage needed for game projects and the high expense of LFS support for hosted git providers. It also avoids the time and money spent for small to mid-sized studios on managing self-hosted versions of the aforementioned git service providers. Ultimately, this project focuses on supporting CI/CD game projects with users only paying based on time and usage of resources, instead of high flat monthly or per seat costs. This is ideal for small teams that plan for only a few builds a week. It is also excellent for the hobbyist as they do not need to remember to shut down resources during a break, but still maintain the automation of deploying a project when necessary.

This project also enables private storage of licensed products. The best example is UE4, our automation builds a CI pipeline for Unreal Engine 4 using the popular ue4-docker project. The container image is stored in a private ECR to maintain the UE4 EULA.

>*Here is an example of the cost advantage in context of Git LFS* A GitHub storage plan for 50GB of LFS storage is $5/month. 50GB of storage (so long as your aggregate S3 storage is less than 50TB) in AWS S3 costs $1.15/month in US-EAST-2. Your first 1 GB of download is free OUT of AWS. A full-depth clone of a single branch containing up to 50 GB of LFS data will cost $4.41 locally or about $1 in CodeBuild. Ideally this really only happens if you are adding a new team member or local copy of the remote repository. These are extreme examples maxing out storage. All in all, the monthly costs greatly beat the data pack cost and the usage costs are negligible. The ideal project for this pipeline will primarily be a code first project with about 20GB of assets and a final build (for a PC Client) size of about 5 GB.

## Features

This repository exposes features for the Continuous Integration pipeline for building games. Below is a list of supported features. Continuous Deployment will be coming soon.

- [X] Serverless Git LFS
  - [X] GitHub Authentication
  - [ ] BitBucket Authentication
  - [ ] HTTP Basic Authorization Header
- [X] Game Engine Builds
  - [X] Custom Game/Engine
    - [X] Windows Builds
    - [X] Linux Builds
  - [X] Unreal Engine 4
    - [X] Windows Builds
    - [ ] Linux Builds
  - [ ] Unity
    - [ ] Windows Builds
    - [ ] Linux Builds
  - [ ] Lumberyard
    - [ ] Windows Builds
    - [ ] Linux Builds
- [X] Source Control Management Integration
  - [X] GitHub
  - [ ] BitBucket
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

> __About Roles__ For the most part, the roles and access granted and enabled is typically scoped to the _/ops/_ path. This includes access control policies and IAM role policy documents.

### Phase One - Bootstrap Part A

Create a build project for this project. This will create packaged cloudformation scripts and magic links for the next phases.

```bash
aws cloudformation deploy --template-file ./templates/bootstrap/bootstrap-self.yml --capabilities CAPABILITY_NAMED_IAM --stack-name OpsBuild --parameter-overrides "OAuthToken={Your GitHub Personal Access Token}"
```

> __Note__ The stack creation should only take a few minutes. After which, a CodeBuild project will kick off providing this repository's templates packaged in a convenient manner. This is what the Exports in CloudFormation reference.

### Phase Two - Bootstrap Part B

Create a CloudFormation Stack that will create storage resources, a CodePipeline project that will create another CloudFormation stack for building large containers on windows called `WindowsLargeDockerBuilder` (by default), as well as another CodePipeline pipeline for building Unreal Engine 4 containers for build pipelines (if configured).

You can launch this stack following the Magic Links provided in the below script.

```bash
aws cloudformation --no-paginate list-exports --query "Exports[*].{Name:Name,Link:Value}"
```

The link to launch this phase is named `GlobalOps-GamePipelineMagicLink` if you used the default options.

>*Unreal Engine 4* If you choose to support UE4 in this stage, your costs will go up for each build of UE4 you wish to store for CI. This will be in the range of about $3 - $6 a month for each engine version you build. Due to the build pipeline of the custom windows docker container. You will also incur a one time EC2 charge of about $2 - $9 to build the engine. This can be modified by forking this project and integrating a private docker repository for the following: `templates/ops-github-build-project.yml` and the repository referenced in `templates/bootstrap-ue4-container-build.yml`. You can further cut costs by building the docker image locally and pushing to ECR or a **private** docker repository.

### Phase Three - For Each New Project

You can now get the magic links with the following script. You may also login to your instance of the AWS Console, go to CloudFormation within the region you deployed Phase One, open the sidebar, select Exports, and click on the magic links.

```bash
aws cloudformation --no-paginate list-exports --query "Exports[*].{Name:Name,Link:Value}"
```

Copy and Paste the "Link" field for any of the exports with the "Name" like *MagicLink in your browser. This will let you start a new cloudformation job in the AWS Console.

Using the magic links from Phase One, you can now use project specific CloudFormation templates. The next section will demonstrate scripts for default configurations and specific engine builds.

### Cleaning Up

After the build succeeds you may opt out of automatically keeping templates up to date by destroying the stack. The s3 bucket created to store the CloudFormation scripts for the Magic Links are set to 'Retain' and thus still available after the stack is deleted. Keep in mind you may need to save the links from the script shown in Phase Two before deleting the stack.

```bash
aws cloudformation delete-stack --stack-name OpsBuild
```

The `./templates/bootstrap/bootstrap-self.yml` template will create two (2) S3 buckets with the deletion and update/replace policies set to 'Retain'. Therefore, after deletion the buckets will still exist. One of the buckets is used to store the final templates you will be using for building pipelines for your games, so it is not recommended to delete this bucket. It is referenced in the "Magic Links". To keep these buckets is negligible to your S3 storage bill.

If you chose to run the Engine specific or Large Container builder templates found in the main stack `./templates/bootstrap/main.yml`, there will be four (4) artifacts created. These artifacts are two (2) S3 buckets, one (1) IAM role, and one (1) ECR. The latter is what you definitely want to keep around if you ran this project with the option to create UE4 artifacts. The IAM Role is required to update or delete the stack created from the CodePipeline created by this stack, which was used to build Unreal Engine 4.

## Per Project Deployments

There are currently two supported configurations for per project pipelines. These pipelines are specifically for continuous integration. This means it will pull the project when pushed to the specific build branch (default is `main`) from github (currently). The final output will be an S3 bucket with the client application. So we currently support build pipelines for single player games. However, you can easily fork this repository and start plopping in support for server fleets.

>*Triggering a Build* By default, these builds will only be triggered under two conditions. These conditions are the repository is pushed to with a commit starting with "release" (case sensitive, do no include quotes) or a tag is pushed following [semantic versioning format](https://semver.org/).

>*Buildspec Templates Available* Troll Purse provides buildspec templates by engine at https://github.com/TrollPursePublishing/trollpurse-ops-engine-buildspecs. Simply find the one for your desired engine and copy and paste the content to your own buildspec. The most important part is that it setups git lfs.

### Custom Engine

Custom Engines are a wild card, therefore the support is only in providing a CodeBuild runtime and artifact store. Using this as a baseline, if additional requirements similar to other engines are needed, see those engines' CloudFormation templates.

### Unreal Engine 4

Before building for Unreal Engine 4, assert that you have built the ue4-full image for the engine version you are wishing to build for. This image is stored in ECR and you can search for it using the below command.

```bash
aws ecr describe-images --repository-name ops/ue4-full --query "imageDetails[*].{Images:imageTags}" --output text
```

>**Building UE4 Versions** By default the project builds the latest ue4-docker stable version of Unreal Engine 4. If you wish to build another version or update the version to build, update the `UE4EngineVersion` parameters in the child stack `./templates/bootstrap/ue4/bootstrap-ue4-container-build.yml`.

## Third Party Forks

The foundation of this project would not be possible without the support of the open source community. There are several forked repositories that are modified to enable these pipelines. Below is a list acknowledging the original authors and a link to our fork.

- UE4 Docker: [Original](https://github.com/adamrehn/ue4-docker) | [Fork](https://github.com/TrollPursePublishing/ue4-docker)
- AWS CodePipeline Custom Action: [Original](https://github.com/aws-samples/aws-codepipeline-custom-action) | [Fork](https://github.com/TrollPursePublishing/aws-codepipeline-custom-action)
- Estranged LFS: [Original](https://github.com/alanedwardes/Estranged.Lfs) | [Fork](https://github.com/TrollPursePublishing/Estranged.Lfs)

## Security Best Practices Disclosures

This project is built to be as cost effective as possible. It was also created to make integration fast. So there are some security considerations that need to be brought to light before adopting this project. Most of these considerations will become options in the future for this project.

### IAM Roles are created

This project, for ease of integration, creates required IAM roles with the `/ops/` path. The project tries to restrict access and role passing to this path. Most of the stacks are created with IAM Role ARNs as parameters, which will enable those with experience to use the stacks with IAM Roles managed by AWS mature organizations. This current template structure will be followed, and we may provide `*-no-iam.yml` type stacks in the future.

### The Large Docker Builder is in the default VPC

The large docker container fork currently deploys EC2 instances into the default VPC. While it is a short lived service - several hours - this is not ideal. This EC2 instance should be deployed to a private subnet with a route table pointing to a NAT that points to an Internet Gateway. [See this documentation](https://docs.aws.amazon.com/vpc/latest/userguide/VPC_Scenario2.html). This strategy dramatically impacts the per month billing due to the NAT gateway charges which is why it was left out of the current iteration. Another option would be to build the network on demand, but this may impact build time for large windows containers if done from a cold start. It is a planned fix.

### NoEcho properties are not SSM Parameters

As it stands right now, the CloudFormation templates set secrets to NoEcho. While this is a step in the right direction, it doesn't actually secure secrets. Therefore there is a high risk of the secret echoing in build pipelines and the like. We will be actively finding instances of this and changing those inputs to [SSM Secure String Parameters](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ssm-parameter.html). This will be a breaking change.
