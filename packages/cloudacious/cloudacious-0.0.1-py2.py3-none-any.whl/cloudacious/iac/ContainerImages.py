import pulumi
import pulumi_aws as aws
import pulumi_docker as docker


class Image:
    """
    Pulumi builds a container image and pushes it to ECR.

    Note: Changing this to receive docker.RegistryArgs as args passed in would make this lots more versatile rather than ECR only, it would just take a bit of testing of Pulumi outputs which can get finicky.
    """
    def __init__(
        self,
        stack_name: str,
        image_name: str,
        aws_account_id: str,
        client: str,
        target: str,
        fn_purpose: str,
        context: str,
        build_args: dict,
        dockerfile_name: str,
        ecr_registry_id: str,
        ecr_repo: str,
    ):
        """
        `image_info` required fields:

        `stack_name`: str, name of the stack
        `aws_account_id`: str, ID of AWS account (e.g. 123456789012)
        `client`: str, the name of the client
        `target`: str, the target of the dockerfile (does None work?)
        `fn_purpose`: str, comprises part of the image name (pass in image_name instead?)
        `context`: str, the context of the dockerfile, i.e. where in relation to current working directory is the Dockerfile stored. Typically will be a blank string, "".
        `build_args`: dict, the build args required by the Dockerfile; in other words, if your Dockerfile has lines that start with `ARG`, each of those is a build arg you'd pass in at build time in the CLI with `--build-arg ARG=$ENV_VAR`. For example, given `ARG GITLAB_TOKEN`, you would include `--build-arg GITLAB_TOKEN=$GITLAB_TOKEN` in your docker build command, assuming a prior `export GITLAB_TOKEN=<secret token value>` was run.
        `dockerfile_name`: str, the name of the dockerfile to use in the build
        `ecr_registry_id`: str, the id of the ECR registry, e.g. `<account id>.dkr.ecr.us-east-1.amazonaws.com` WITHOUT the repository name.
        `ecr_repo`: str, the name of the ECR repo, e.g. `cloudacious`

        ...
        """
        self.stack_name: str = stack_name
        self.image_name: str = image_name
        self.aws_account_id: str = aws_account_id
        self.client: str = client
        self.target: str = target
        self.fn_purpose: str = fn_purpose
        self.context: str = context
        self.build_args: dict = build_args
        self.dockerfile_name: str = dockerfile_name
        self.ecr_registry_id: str = ecr_registry_id
        self.ecr_repo: str = ecr_repo

        self._resource_name: str = self.stack_name.replace("-", "_") 

    def create_image(self):
        """
        Logs into ECR repo, builds image, and pushes it to ECR.
        """
        self._auth_token = aws.ecr.get_authorization_token_output(
            registry_id=self.aws_account_id
        )

        self._ecr_build_image = docker.Image(
            resource_name=f"{self._resource_name}-{self.fn_purpose}",
            build=docker.DockerBuildArgs(
                args=self.build_args,
                # cache_from=docker.CacheFromArgs(
                #     images=[
                #         ecr.ecr_repo.repository_url.apply(
                #             lambda repository_url: f"{repository_url}:base"
                #         )
                #     ],
                # ),
                context=self.context,
                dockerfile=f"{self.context}{self.dockerfile_name}",
                platform="linux/amd64",
                target=self.target,
            ),
            image_name=f"{self.ecr_registry_id}/{self.ecr_repo}:{self.image_name}",
            registry=docker.RegistryArgs(
                username="AWS",
                password=pulumi.Output.secret(self._auth_token.password),
                server=self.ecr_registry_id,
            ),
        )
        self.base_image_name = self._ecr_build_image.base_image_name.apply(
            lambda base_image_name: base_image_name
        )
        pulumi.export('base_image_name', self.base_image_name)
        return
