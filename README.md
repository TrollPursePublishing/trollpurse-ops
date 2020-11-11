# trollpurse-cloudformation

CloudFormation Templates used by [Troll Purse](https://trollpurse.com). Hobby game development.

## Getting Started

Execute the two scripts below, replacing `${BucketName}` with the desired name of the S3 bucket you will deploy the template copies to.

```bash
aws cloudformation deploy \
  --capabilities CAPABILITY_IAM \
  --stack-name AccountTemplatesBootstrap \
  --template-file file:///./templates/bootstrap/bootstrap.yml \
  --parameters TemplateS3BucketName=${BucketName}
```

## Testing Locally

You can validate all of the templates locally via the script below:

```bash
find ./templates -name '*.yml' -print0 -or -name '*.yaml' -print0 | xargs -0 -I {file} sh -c 'echo Validating {file}; aws cloudformation validate-template --template-body file://{file}'
```

This is also the build script.
