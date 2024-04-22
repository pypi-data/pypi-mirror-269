import aws_cdk as cdk
from constructs import Construct
from aws_cdk import aws_apigateway as _apigateway

from aws_cdk_constructs.utils import (
    normalize_environment_parameter,
    get_version,
)


class API(Construct):
    """

    The FAO CDK API Construct creates an AWS API Gateway REST API, providing a Swagger JSON file.

    Every resource created by the construct will be tagged according to the FAO AWS tagging strategy described at https://aws.fao.org

    Args:

        id (str): the logical id of the newly created resource

        app_name (str): The application name. This will be used to generate the 'ApplicationName' tag for CSI compliancy. The ID of the application. This must be unique for each system, as it will be used to calculate the AWS costs of the system

        environment (str): Specify the environment in which you want to deploy you system. Allowed values: Development, QA, Production, SharedServices

        environments_parameters (dict): The dictionary containing the references to CSI AWS environments. This will simplify the environment promotions and enable a parametric development of the infrastructures.

        swagger_path (str): The path to the Swagger file (or OpenAPI compatibile) to use to auto-generate API Gateway

    """

    def __init__(
        self,
        scope: Construct,
        id: str,
        app_name: str,
        environment: str,
        environments_parameters: dict,
        swagger_path: str = None,
        **kwargs
    ) -> None:
        super().__init__(scope, id, **kwargs)
        environment = normalize_environment_parameter(environment)

        # Apply mandatory tags
        cdk.Tags.of(self).add('ApplicationName', app_name.lower().strip())
        cdk.Tags.of(self).add('Environment', environment)

        # Apply FAO CDK tags
        cdk.Tags.of(self).add('fao-cdk-construct', 'api')
        cdk.Tags.of(cdk.Stack.of(self)).add('fao-cdk-version', get_version())
        cdk.Tags.of(cdk.Stack.of(self)).add('fao-cdk', 'true')

        # Declare variables
        self.api = None

        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ Create conditions
        swagger_path = swagger_path.strip()
        swagger_was_provided = swagger_path

        environment = environment.lower()
        aws_account = environments_parameters['accounts'][environment]

        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ Conditionally create resources

        if swagger_was_provided:
            # Read the base user data from file
            with open(swagger_path) as swagger_content:
                pws_swagger = swagger_content.read()
            swagger_content.close()

            api = _apigateway.CfnRestApi(
                self,
                app_name + '-api',
                body=None,
                body_s3_location=_apigateway.CfnRestApi.S3LocationProperty(
                    bucket=aws_account['s3_config_bucket'],
                    key=app_name + '/' + environment + '/swagger.json',
                ),
                description=app_name + '/' + environment + ' API',
                name=app_name + '/' + environment,
            )
