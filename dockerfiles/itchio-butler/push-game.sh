#!/bin/bash
while getopts b:o:d:u:p:g:c:v: flag
do
    case "${flag}" in
        b) bucket=${OPTARG};;
        o) object=${OPTARG};;
        d) directory=${OPTARG};;
        u) username=${OPTARG};;
        p) password_parameter=${OPTARG};;
        g) game=${OPTARG};;
        c) channel=${OPTARG};;
        v) version=${OPTARG};;
        *) echo "Invalid flag: ${flag}"; exit 1;;
    esac
done

export BUTLER_API_KEY = $(aws ssm get-parameter --name "${password_parameter}" --output text --query "Parameter.Value")
aws s3 cp s3://$bucket/$object artifact.zip
unzip artifact.zip
butler push $directory $username/$game:$channel --userversion $version
