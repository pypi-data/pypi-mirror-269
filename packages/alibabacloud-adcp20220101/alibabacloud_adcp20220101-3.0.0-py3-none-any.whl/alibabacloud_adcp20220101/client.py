# -*- coding: utf-8 -*-
# This file is auto-generated, don't edit it. Thanks.
from typing import Dict
from Tea.core import TeaCore

from alibabacloud_tea_openapi.client import Client as OpenApiClient
from alibabacloud_tea_openapi import models as open_api_models
from alibabacloud_tea_util.client import Client as UtilClient
from alibabacloud_endpoint_util.client import Client as EndpointUtilClient
from alibabacloud_adcp20220101 import models as adcp_20220101_models
from alibabacloud_tea_util import models as util_models
from alibabacloud_openapi_util.client import Client as OpenApiUtilClient


class Client(OpenApiClient):
    """
    *\
    """
    def __init__(
        self, 
        config: open_api_models.Config,
    ):
        super().__init__(config)
        self._endpoint_rule = 'central'
        self._endpoint_map = {
            'cn-beijing': 'adcp.cn-beijing.aliyuncs.com',
            'cn-zhangjiakou': 'adcp.cn-zhangjiakou.aliyuncs.com',
            'cn-hangzhou': 'adcp.cn-hangzhou.aliyuncs.com',
            'cn-shanghai': 'adcp.cn-shanghai.aliyuncs.com',
            'cn-shenzhen': 'adcp.cn-shenzhen.aliyuncs.com',
            'cn-heyuan': 'adcp.cn-heyuan.aliyuncs.com',
            'cn-hongkong': 'adcp.cn-hongkong.aliyuncs.com',
            'ap-northeast-1': 'adcp.ap-northeast-1.aliyuncs.com',
            'ap-southeast-1': 'adcp.ap-southeast-1.aliyuncs.com',
            'ap-southeast-5': 'adcp.ap-southeast-5.aliyuncs.com',
            'ap-south-1': 'adcp.ap-south-1.aliyuncs.com',
            'ap-southeast-2': 'adcp.ap-southeast-2.aliyuncs.com',
            'ap-southeast-3': 'adcp.ap-southeast-3.aliyuncs.com',
            'cn-chengdu': 'adcp-vpc.cn-chengdu.aliyuncs.com',
            'cn-huhehaote': 'adcp.cn-huhehaote.aliyuncs.com',
            'cn-qingdao': 'adcp.cn-qingdao.aliyuncs.com',
            'cn-shanghai-finance-1': 'adcp-vpc.cn-shanghai-finance-1.aliyuncs.com',
            'cn-wulanchabu': 'adcp.cn-wulanchabu.aliyuncs.com',
            'eu-central-1': 'adcp.eu-central-1.aliyuncs.com',
            'eu-west-1': 'adcp-vpc.eu-west-1.aliyuncs.com',
            'me-east-1': 'adcp.me-east-1.aliyuncs.com',
            'us-east-1': 'adcp.us-east-1.aliyuncs.com',
            'us-west-1': 'adcp.us-west-1.aliyuncs.com'
        }
        self.check_config(config)
        self._endpoint = self.get_endpoint('adcp', self._region_id, self._endpoint_rule, self._network, self._suffix, self._endpoint_map, self._endpoint)

    def get_endpoint(
        self,
        product_id: str,
        region_id: str,
        endpoint_rule: str,
        network: str,
        suffix: str,
        endpoint_map: Dict[str, str],
        endpoint: str,
    ) -> str:
        if not UtilClient.empty(endpoint):
            return endpoint
        if not UtilClient.is_unset(endpoint_map) and not UtilClient.empty(endpoint_map.get(region_id)):
            return endpoint_map.get(region_id)
        return EndpointUtilClient.get_endpoint_rules(product_id, region_id, endpoint_rule, network, suffix)

    def attach_cluster_to_hub_with_options(
        self,
        request: adcp_20220101_models.AttachClusterToHubRequest,
        runtime: util_models.RuntimeOptions,
    ) -> adcp_20220101_models.AttachClusterToHubResponse:
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.attach_to_mesh):
            query['AttachToMesh'] = request.attach_to_mesh
        if not UtilClient.is_unset(request.cluster_id):
            query['ClusterId'] = request.cluster_id
        body = {}
        if not UtilClient.is_unset(request.cluster_ids):
            body['ClusterIds'] = request.cluster_ids
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query),
            body=OpenApiUtilClient.parse_to_map(body)
        )
        params = open_api_models.Params(
            action='AttachClusterToHub',
            version='2022-01-01',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            adcp_20220101_models.AttachClusterToHubResponse(),
            self.call_api(params, req, runtime)
        )

    async def attach_cluster_to_hub_with_options_async(
        self,
        request: adcp_20220101_models.AttachClusterToHubRequest,
        runtime: util_models.RuntimeOptions,
    ) -> adcp_20220101_models.AttachClusterToHubResponse:
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.attach_to_mesh):
            query['AttachToMesh'] = request.attach_to_mesh
        if not UtilClient.is_unset(request.cluster_id):
            query['ClusterId'] = request.cluster_id
        body = {}
        if not UtilClient.is_unset(request.cluster_ids):
            body['ClusterIds'] = request.cluster_ids
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query),
            body=OpenApiUtilClient.parse_to_map(body)
        )
        params = open_api_models.Params(
            action='AttachClusterToHub',
            version='2022-01-01',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            adcp_20220101_models.AttachClusterToHubResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def attach_cluster_to_hub(
        self,
        request: adcp_20220101_models.AttachClusterToHubRequest,
    ) -> adcp_20220101_models.AttachClusterToHubResponse:
        runtime = util_models.RuntimeOptions()
        return self.attach_cluster_to_hub_with_options(request, runtime)

    async def attach_cluster_to_hub_async(
        self,
        request: adcp_20220101_models.AttachClusterToHubRequest,
    ) -> adcp_20220101_models.AttachClusterToHubResponse:
        runtime = util_models.RuntimeOptions()
        return await self.attach_cluster_to_hub_with_options_async(request, runtime)

    def create_hub_cluster_with_options(
        self,
        request: adcp_20220101_models.CreateHubClusterRequest,
        runtime: util_models.RuntimeOptions,
    ) -> adcp_20220101_models.CreateHubClusterResponse:
        UtilClient.validate_model(request)
        body = {}
        if not UtilClient.is_unset(request.api_server_public_eip):
            body['ApiServerPublicEip'] = request.api_server_public_eip
        if not UtilClient.is_unset(request.argo_server_enabled):
            body['ArgoServerEnabled'] = request.argo_server_enabled
        if not UtilClient.is_unset(request.audit_log_enabled):
            body['AuditLogEnabled'] = request.audit_log_enabled
        if not UtilClient.is_unset(request.is_enterprise_security_group):
            body['IsEnterpriseSecurityGroup'] = request.is_enterprise_security_group
        if not UtilClient.is_unset(request.name):
            body['Name'] = request.name
        if not UtilClient.is_unset(request.price_limit):
            body['PriceLimit'] = request.price_limit
        if not UtilClient.is_unset(request.profile):
            body['Profile'] = request.profile
        if not UtilClient.is_unset(request.region_id):
            body['RegionId'] = request.region_id
        if not UtilClient.is_unset(request.resource_group_id):
            body['ResourceGroupID'] = request.resource_group_id
        if not UtilClient.is_unset(request.v_switches):
            body['VSwitches'] = request.v_switches
        if not UtilClient.is_unset(request.vpc_id):
            body['VpcId'] = request.vpc_id
        if not UtilClient.is_unset(request.workflow_schedule_mode):
            body['WorkflowScheduleMode'] = request.workflow_schedule_mode
        req = open_api_models.OpenApiRequest(
            body=OpenApiUtilClient.parse_to_map(body)
        )
        params = open_api_models.Params(
            action='CreateHubCluster',
            version='2022-01-01',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            adcp_20220101_models.CreateHubClusterResponse(),
            self.call_api(params, req, runtime)
        )

    async def create_hub_cluster_with_options_async(
        self,
        request: adcp_20220101_models.CreateHubClusterRequest,
        runtime: util_models.RuntimeOptions,
    ) -> adcp_20220101_models.CreateHubClusterResponse:
        UtilClient.validate_model(request)
        body = {}
        if not UtilClient.is_unset(request.api_server_public_eip):
            body['ApiServerPublicEip'] = request.api_server_public_eip
        if not UtilClient.is_unset(request.argo_server_enabled):
            body['ArgoServerEnabled'] = request.argo_server_enabled
        if not UtilClient.is_unset(request.audit_log_enabled):
            body['AuditLogEnabled'] = request.audit_log_enabled
        if not UtilClient.is_unset(request.is_enterprise_security_group):
            body['IsEnterpriseSecurityGroup'] = request.is_enterprise_security_group
        if not UtilClient.is_unset(request.name):
            body['Name'] = request.name
        if not UtilClient.is_unset(request.price_limit):
            body['PriceLimit'] = request.price_limit
        if not UtilClient.is_unset(request.profile):
            body['Profile'] = request.profile
        if not UtilClient.is_unset(request.region_id):
            body['RegionId'] = request.region_id
        if not UtilClient.is_unset(request.resource_group_id):
            body['ResourceGroupID'] = request.resource_group_id
        if not UtilClient.is_unset(request.v_switches):
            body['VSwitches'] = request.v_switches
        if not UtilClient.is_unset(request.vpc_id):
            body['VpcId'] = request.vpc_id
        if not UtilClient.is_unset(request.workflow_schedule_mode):
            body['WorkflowScheduleMode'] = request.workflow_schedule_mode
        req = open_api_models.OpenApiRequest(
            body=OpenApiUtilClient.parse_to_map(body)
        )
        params = open_api_models.Params(
            action='CreateHubCluster',
            version='2022-01-01',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            adcp_20220101_models.CreateHubClusterResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def create_hub_cluster(
        self,
        request: adcp_20220101_models.CreateHubClusterRequest,
    ) -> adcp_20220101_models.CreateHubClusterResponse:
        runtime = util_models.RuntimeOptions()
        return self.create_hub_cluster_with_options(request, runtime)

    async def create_hub_cluster_async(
        self,
        request: adcp_20220101_models.CreateHubClusterRequest,
    ) -> adcp_20220101_models.CreateHubClusterResponse:
        runtime = util_models.RuntimeOptions()
        return await self.create_hub_cluster_with_options_async(request, runtime)

    def delete_hub_cluster_with_options(
        self,
        tmp_req: adcp_20220101_models.DeleteHubClusterRequest,
        runtime: util_models.RuntimeOptions,
    ) -> adcp_20220101_models.DeleteHubClusterResponse:
        UtilClient.validate_model(tmp_req)
        request = adcp_20220101_models.DeleteHubClusterShrinkRequest()
        OpenApiUtilClient.convert(tmp_req, request)
        if not UtilClient.is_unset(tmp_req.retain_resources):
            request.retain_resources_shrink = OpenApiUtilClient.array_to_string_with_specified_style(tmp_req.retain_resources, 'RetainResources', 'json')
        query = {}
        if not UtilClient.is_unset(request.cluster_id):
            query['ClusterId'] = request.cluster_id
        if not UtilClient.is_unset(request.force):
            query['Force'] = request.force
        if not UtilClient.is_unset(request.retain_resources_shrink):
            query['RetainResources'] = request.retain_resources_shrink
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='DeleteHubCluster',
            version='2022-01-01',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            adcp_20220101_models.DeleteHubClusterResponse(),
            self.call_api(params, req, runtime)
        )

    async def delete_hub_cluster_with_options_async(
        self,
        tmp_req: adcp_20220101_models.DeleteHubClusterRequest,
        runtime: util_models.RuntimeOptions,
    ) -> adcp_20220101_models.DeleteHubClusterResponse:
        UtilClient.validate_model(tmp_req)
        request = adcp_20220101_models.DeleteHubClusterShrinkRequest()
        OpenApiUtilClient.convert(tmp_req, request)
        if not UtilClient.is_unset(tmp_req.retain_resources):
            request.retain_resources_shrink = OpenApiUtilClient.array_to_string_with_specified_style(tmp_req.retain_resources, 'RetainResources', 'json')
        query = {}
        if not UtilClient.is_unset(request.cluster_id):
            query['ClusterId'] = request.cluster_id
        if not UtilClient.is_unset(request.force):
            query['Force'] = request.force
        if not UtilClient.is_unset(request.retain_resources_shrink):
            query['RetainResources'] = request.retain_resources_shrink
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='DeleteHubCluster',
            version='2022-01-01',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            adcp_20220101_models.DeleteHubClusterResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def delete_hub_cluster(
        self,
        request: adcp_20220101_models.DeleteHubClusterRequest,
    ) -> adcp_20220101_models.DeleteHubClusterResponse:
        runtime = util_models.RuntimeOptions()
        return self.delete_hub_cluster_with_options(request, runtime)

    async def delete_hub_cluster_async(
        self,
        request: adcp_20220101_models.DeleteHubClusterRequest,
    ) -> adcp_20220101_models.DeleteHubClusterResponse:
        runtime = util_models.RuntimeOptions()
        return await self.delete_hub_cluster_with_options_async(request, runtime)

    def delete_policy_instance_with_options(
        self,
        tmp_req: adcp_20220101_models.DeletePolicyInstanceRequest,
        runtime: util_models.RuntimeOptions,
    ) -> adcp_20220101_models.DeletePolicyInstanceResponse:
        UtilClient.validate_model(tmp_req)
        request = adcp_20220101_models.DeletePolicyInstanceShrinkRequest()
        OpenApiUtilClient.convert(tmp_req, request)
        if not UtilClient.is_unset(tmp_req.cluster_ids):
            request.cluster_ids_shrink = OpenApiUtilClient.array_to_string_with_specified_style(tmp_req.cluster_ids, 'ClusterIds', 'json')
        query = {}
        if not UtilClient.is_unset(request.cluster_id):
            query['ClusterId'] = request.cluster_id
        if not UtilClient.is_unset(request.cluster_ids_shrink):
            query['ClusterIds'] = request.cluster_ids_shrink
        if not UtilClient.is_unset(request.policy_name):
            query['PolicyName'] = request.policy_name
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='DeletePolicyInstance',
            version='2022-01-01',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            adcp_20220101_models.DeletePolicyInstanceResponse(),
            self.call_api(params, req, runtime)
        )

    async def delete_policy_instance_with_options_async(
        self,
        tmp_req: adcp_20220101_models.DeletePolicyInstanceRequest,
        runtime: util_models.RuntimeOptions,
    ) -> adcp_20220101_models.DeletePolicyInstanceResponse:
        UtilClient.validate_model(tmp_req)
        request = adcp_20220101_models.DeletePolicyInstanceShrinkRequest()
        OpenApiUtilClient.convert(tmp_req, request)
        if not UtilClient.is_unset(tmp_req.cluster_ids):
            request.cluster_ids_shrink = OpenApiUtilClient.array_to_string_with_specified_style(tmp_req.cluster_ids, 'ClusterIds', 'json')
        query = {}
        if not UtilClient.is_unset(request.cluster_id):
            query['ClusterId'] = request.cluster_id
        if not UtilClient.is_unset(request.cluster_ids_shrink):
            query['ClusterIds'] = request.cluster_ids_shrink
        if not UtilClient.is_unset(request.policy_name):
            query['PolicyName'] = request.policy_name
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='DeletePolicyInstance',
            version='2022-01-01',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            adcp_20220101_models.DeletePolicyInstanceResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def delete_policy_instance(
        self,
        request: adcp_20220101_models.DeletePolicyInstanceRequest,
    ) -> adcp_20220101_models.DeletePolicyInstanceResponse:
        runtime = util_models.RuntimeOptions()
        return self.delete_policy_instance_with_options(request, runtime)

    async def delete_policy_instance_async(
        self,
        request: adcp_20220101_models.DeletePolicyInstanceRequest,
    ) -> adcp_20220101_models.DeletePolicyInstanceResponse:
        runtime = util_models.RuntimeOptions()
        return await self.delete_policy_instance_with_options_async(request, runtime)

    def delete_user_permission_with_options(
        self,
        request: adcp_20220101_models.DeleteUserPermissionRequest,
        runtime: util_models.RuntimeOptions,
    ) -> adcp_20220101_models.DeleteUserPermissionResponse:
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.cluster_id):
            query['ClusterId'] = request.cluster_id
        if not UtilClient.is_unset(request.user_id):
            query['UserId'] = request.user_id
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='DeleteUserPermission',
            version='2022-01-01',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            adcp_20220101_models.DeleteUserPermissionResponse(),
            self.call_api(params, req, runtime)
        )

    async def delete_user_permission_with_options_async(
        self,
        request: adcp_20220101_models.DeleteUserPermissionRequest,
        runtime: util_models.RuntimeOptions,
    ) -> adcp_20220101_models.DeleteUserPermissionResponse:
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.cluster_id):
            query['ClusterId'] = request.cluster_id
        if not UtilClient.is_unset(request.user_id):
            query['UserId'] = request.user_id
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='DeleteUserPermission',
            version='2022-01-01',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            adcp_20220101_models.DeleteUserPermissionResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def delete_user_permission(
        self,
        request: adcp_20220101_models.DeleteUserPermissionRequest,
    ) -> adcp_20220101_models.DeleteUserPermissionResponse:
        runtime = util_models.RuntimeOptions()
        return self.delete_user_permission_with_options(request, runtime)

    async def delete_user_permission_async(
        self,
        request: adcp_20220101_models.DeleteUserPermissionRequest,
    ) -> adcp_20220101_models.DeleteUserPermissionResponse:
        runtime = util_models.RuntimeOptions()
        return await self.delete_user_permission_with_options_async(request, runtime)

    def deploy_policy_instance_with_options(
        self,
        tmp_req: adcp_20220101_models.DeployPolicyInstanceRequest,
        runtime: util_models.RuntimeOptions,
    ) -> adcp_20220101_models.DeployPolicyInstanceResponse:
        UtilClient.validate_model(tmp_req)
        request = adcp_20220101_models.DeployPolicyInstanceShrinkRequest()
        OpenApiUtilClient.convert(tmp_req, request)
        if not UtilClient.is_unset(tmp_req.cluster_ids):
            request.cluster_ids_shrink = OpenApiUtilClient.array_to_string_with_specified_style(tmp_req.cluster_ids, 'ClusterIds', 'json')
        if not UtilClient.is_unset(tmp_req.namespaces):
            request.namespaces_shrink = OpenApiUtilClient.array_to_string_with_specified_style(tmp_req.namespaces, 'Namespaces', 'json')
        query = {}
        if not UtilClient.is_unset(request.cluster_id):
            query['ClusterId'] = request.cluster_id
        if not UtilClient.is_unset(request.cluster_ids_shrink):
            query['ClusterIds'] = request.cluster_ids_shrink
        if not UtilClient.is_unset(request.namespaces_shrink):
            query['Namespaces'] = request.namespaces_shrink
        if not UtilClient.is_unset(request.policy_action):
            query['PolicyAction'] = request.policy_action
        if not UtilClient.is_unset(request.policy_name):
            query['PolicyName'] = request.policy_name
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='DeployPolicyInstance',
            version='2022-01-01',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            adcp_20220101_models.DeployPolicyInstanceResponse(),
            self.call_api(params, req, runtime)
        )

    async def deploy_policy_instance_with_options_async(
        self,
        tmp_req: adcp_20220101_models.DeployPolicyInstanceRequest,
        runtime: util_models.RuntimeOptions,
    ) -> adcp_20220101_models.DeployPolicyInstanceResponse:
        UtilClient.validate_model(tmp_req)
        request = adcp_20220101_models.DeployPolicyInstanceShrinkRequest()
        OpenApiUtilClient.convert(tmp_req, request)
        if not UtilClient.is_unset(tmp_req.cluster_ids):
            request.cluster_ids_shrink = OpenApiUtilClient.array_to_string_with_specified_style(tmp_req.cluster_ids, 'ClusterIds', 'json')
        if not UtilClient.is_unset(tmp_req.namespaces):
            request.namespaces_shrink = OpenApiUtilClient.array_to_string_with_specified_style(tmp_req.namespaces, 'Namespaces', 'json')
        query = {}
        if not UtilClient.is_unset(request.cluster_id):
            query['ClusterId'] = request.cluster_id
        if not UtilClient.is_unset(request.cluster_ids_shrink):
            query['ClusterIds'] = request.cluster_ids_shrink
        if not UtilClient.is_unset(request.namespaces_shrink):
            query['Namespaces'] = request.namespaces_shrink
        if not UtilClient.is_unset(request.policy_action):
            query['PolicyAction'] = request.policy_action
        if not UtilClient.is_unset(request.policy_name):
            query['PolicyName'] = request.policy_name
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='DeployPolicyInstance',
            version='2022-01-01',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            adcp_20220101_models.DeployPolicyInstanceResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def deploy_policy_instance(
        self,
        request: adcp_20220101_models.DeployPolicyInstanceRequest,
    ) -> adcp_20220101_models.DeployPolicyInstanceResponse:
        runtime = util_models.RuntimeOptions()
        return self.deploy_policy_instance_with_options(request, runtime)

    async def deploy_policy_instance_async(
        self,
        request: adcp_20220101_models.DeployPolicyInstanceRequest,
    ) -> adcp_20220101_models.DeployPolicyInstanceResponse:
        runtime = util_models.RuntimeOptions()
        return await self.deploy_policy_instance_with_options_async(request, runtime)

    def describe_hub_cluster_details_with_options(
        self,
        request: adcp_20220101_models.DescribeHubClusterDetailsRequest,
        runtime: util_models.RuntimeOptions,
    ) -> adcp_20220101_models.DescribeHubClusterDetailsResponse:
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.cluster_id):
            query['ClusterId'] = request.cluster_id
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='DescribeHubClusterDetails',
            version='2022-01-01',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            adcp_20220101_models.DescribeHubClusterDetailsResponse(),
            self.call_api(params, req, runtime)
        )

    async def describe_hub_cluster_details_with_options_async(
        self,
        request: adcp_20220101_models.DescribeHubClusterDetailsRequest,
        runtime: util_models.RuntimeOptions,
    ) -> adcp_20220101_models.DescribeHubClusterDetailsResponse:
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.cluster_id):
            query['ClusterId'] = request.cluster_id
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='DescribeHubClusterDetails',
            version='2022-01-01',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            adcp_20220101_models.DescribeHubClusterDetailsResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def describe_hub_cluster_details(
        self,
        request: adcp_20220101_models.DescribeHubClusterDetailsRequest,
    ) -> adcp_20220101_models.DescribeHubClusterDetailsResponse:
        runtime = util_models.RuntimeOptions()
        return self.describe_hub_cluster_details_with_options(request, runtime)

    async def describe_hub_cluster_details_async(
        self,
        request: adcp_20220101_models.DescribeHubClusterDetailsRequest,
    ) -> adcp_20220101_models.DescribeHubClusterDetailsResponse:
        runtime = util_models.RuntimeOptions()
        return await self.describe_hub_cluster_details_with_options_async(request, runtime)

    def describe_hub_cluster_kubeconfig_with_options(
        self,
        request: adcp_20220101_models.DescribeHubClusterKubeconfigRequest,
        runtime: util_models.RuntimeOptions,
    ) -> adcp_20220101_models.DescribeHubClusterKubeconfigResponse:
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.cluster_id):
            query['ClusterId'] = request.cluster_id
        if not UtilClient.is_unset(request.private_ip_address):
            query['PrivateIpAddress'] = request.private_ip_address
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='DescribeHubClusterKubeconfig',
            version='2022-01-01',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            adcp_20220101_models.DescribeHubClusterKubeconfigResponse(),
            self.call_api(params, req, runtime)
        )

    async def describe_hub_cluster_kubeconfig_with_options_async(
        self,
        request: adcp_20220101_models.DescribeHubClusterKubeconfigRequest,
        runtime: util_models.RuntimeOptions,
    ) -> adcp_20220101_models.DescribeHubClusterKubeconfigResponse:
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.cluster_id):
            query['ClusterId'] = request.cluster_id
        if not UtilClient.is_unset(request.private_ip_address):
            query['PrivateIpAddress'] = request.private_ip_address
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='DescribeHubClusterKubeconfig',
            version='2022-01-01',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            adcp_20220101_models.DescribeHubClusterKubeconfigResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def describe_hub_cluster_kubeconfig(
        self,
        request: adcp_20220101_models.DescribeHubClusterKubeconfigRequest,
    ) -> adcp_20220101_models.DescribeHubClusterKubeconfigResponse:
        runtime = util_models.RuntimeOptions()
        return self.describe_hub_cluster_kubeconfig_with_options(request, runtime)

    async def describe_hub_cluster_kubeconfig_async(
        self,
        request: adcp_20220101_models.DescribeHubClusterKubeconfigRequest,
    ) -> adcp_20220101_models.DescribeHubClusterKubeconfigResponse:
        runtime = util_models.RuntimeOptions()
        return await self.describe_hub_cluster_kubeconfig_with_options_async(request, runtime)

    def describe_hub_cluster_logs_with_options(
        self,
        request: adcp_20220101_models.DescribeHubClusterLogsRequest,
        runtime: util_models.RuntimeOptions,
    ) -> adcp_20220101_models.DescribeHubClusterLogsResponse:
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.cluster_id):
            query['ClusterId'] = request.cluster_id
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='DescribeHubClusterLogs',
            version='2022-01-01',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            adcp_20220101_models.DescribeHubClusterLogsResponse(),
            self.call_api(params, req, runtime)
        )

    async def describe_hub_cluster_logs_with_options_async(
        self,
        request: adcp_20220101_models.DescribeHubClusterLogsRequest,
        runtime: util_models.RuntimeOptions,
    ) -> adcp_20220101_models.DescribeHubClusterLogsResponse:
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.cluster_id):
            query['ClusterId'] = request.cluster_id
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='DescribeHubClusterLogs',
            version='2022-01-01',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            adcp_20220101_models.DescribeHubClusterLogsResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def describe_hub_cluster_logs(
        self,
        request: adcp_20220101_models.DescribeHubClusterLogsRequest,
    ) -> adcp_20220101_models.DescribeHubClusterLogsResponse:
        runtime = util_models.RuntimeOptions()
        return self.describe_hub_cluster_logs_with_options(request, runtime)

    async def describe_hub_cluster_logs_async(
        self,
        request: adcp_20220101_models.DescribeHubClusterLogsRequest,
    ) -> adcp_20220101_models.DescribeHubClusterLogsResponse:
        runtime = util_models.RuntimeOptions()
        return await self.describe_hub_cluster_logs_with_options_async(request, runtime)

    def describe_hub_clusters_with_options(
        self,
        request: adcp_20220101_models.DescribeHubClustersRequest,
        runtime: util_models.RuntimeOptions,
    ) -> adcp_20220101_models.DescribeHubClustersResponse:
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.profile):
            query['Profile'] = request.profile
        if not UtilClient.is_unset(request.resource_group_id):
            query['ResourceGroupId'] = request.resource_group_id
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='DescribeHubClusters',
            version='2022-01-01',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            adcp_20220101_models.DescribeHubClustersResponse(),
            self.call_api(params, req, runtime)
        )

    async def describe_hub_clusters_with_options_async(
        self,
        request: adcp_20220101_models.DescribeHubClustersRequest,
        runtime: util_models.RuntimeOptions,
    ) -> adcp_20220101_models.DescribeHubClustersResponse:
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.profile):
            query['Profile'] = request.profile
        if not UtilClient.is_unset(request.resource_group_id):
            query['ResourceGroupId'] = request.resource_group_id
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='DescribeHubClusters',
            version='2022-01-01',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            adcp_20220101_models.DescribeHubClustersResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def describe_hub_clusters(
        self,
        request: adcp_20220101_models.DescribeHubClustersRequest,
    ) -> adcp_20220101_models.DescribeHubClustersResponse:
        runtime = util_models.RuntimeOptions()
        return self.describe_hub_clusters_with_options(request, runtime)

    async def describe_hub_clusters_async(
        self,
        request: adcp_20220101_models.DescribeHubClustersRequest,
    ) -> adcp_20220101_models.DescribeHubClustersResponse:
        runtime = util_models.RuntimeOptions()
        return await self.describe_hub_clusters_with_options_async(request, runtime)

    def describe_managed_clusters_with_options(
        self,
        request: adcp_20220101_models.DescribeManagedClustersRequest,
        runtime: util_models.RuntimeOptions,
    ) -> adcp_20220101_models.DescribeManagedClustersResponse:
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.cluster_id):
            query['ClusterId'] = request.cluster_id
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='DescribeManagedClusters',
            version='2022-01-01',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            adcp_20220101_models.DescribeManagedClustersResponse(),
            self.call_api(params, req, runtime)
        )

    async def describe_managed_clusters_with_options_async(
        self,
        request: adcp_20220101_models.DescribeManagedClustersRequest,
        runtime: util_models.RuntimeOptions,
    ) -> adcp_20220101_models.DescribeManagedClustersResponse:
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.cluster_id):
            query['ClusterId'] = request.cluster_id
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='DescribeManagedClusters',
            version='2022-01-01',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            adcp_20220101_models.DescribeManagedClustersResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def describe_managed_clusters(
        self,
        request: adcp_20220101_models.DescribeManagedClustersRequest,
    ) -> adcp_20220101_models.DescribeManagedClustersResponse:
        runtime = util_models.RuntimeOptions()
        return self.describe_managed_clusters_with_options(request, runtime)

    async def describe_managed_clusters_async(
        self,
        request: adcp_20220101_models.DescribeManagedClustersRequest,
    ) -> adcp_20220101_models.DescribeManagedClustersResponse:
        runtime = util_models.RuntimeOptions()
        return await self.describe_managed_clusters_with_options_async(request, runtime)

    def describe_policies_with_options(
        self,
        runtime: util_models.RuntimeOptions,
    ) -> adcp_20220101_models.DescribePoliciesResponse:
        req = open_api_models.OpenApiRequest()
        params = open_api_models.Params(
            action='DescribePolicies',
            version='2022-01-01',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            adcp_20220101_models.DescribePoliciesResponse(),
            self.call_api(params, req, runtime)
        )

    async def describe_policies_with_options_async(
        self,
        runtime: util_models.RuntimeOptions,
    ) -> adcp_20220101_models.DescribePoliciesResponse:
        req = open_api_models.OpenApiRequest()
        params = open_api_models.Params(
            action='DescribePolicies',
            version='2022-01-01',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            adcp_20220101_models.DescribePoliciesResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def describe_policies(self) -> adcp_20220101_models.DescribePoliciesResponse:
        runtime = util_models.RuntimeOptions()
        return self.describe_policies_with_options(runtime)

    async def describe_policies_async(self) -> adcp_20220101_models.DescribePoliciesResponse:
        runtime = util_models.RuntimeOptions()
        return await self.describe_policies_with_options_async(runtime)

    def describe_policy_details_with_options(
        self,
        request: adcp_20220101_models.DescribePolicyDetailsRequest,
        runtime: util_models.RuntimeOptions,
    ) -> adcp_20220101_models.DescribePolicyDetailsResponse:
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.policy_name):
            query['PolicyName'] = request.policy_name
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='DescribePolicyDetails',
            version='2022-01-01',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            adcp_20220101_models.DescribePolicyDetailsResponse(),
            self.call_api(params, req, runtime)
        )

    async def describe_policy_details_with_options_async(
        self,
        request: adcp_20220101_models.DescribePolicyDetailsRequest,
        runtime: util_models.RuntimeOptions,
    ) -> adcp_20220101_models.DescribePolicyDetailsResponse:
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.policy_name):
            query['PolicyName'] = request.policy_name
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='DescribePolicyDetails',
            version='2022-01-01',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            adcp_20220101_models.DescribePolicyDetailsResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def describe_policy_details(
        self,
        request: adcp_20220101_models.DescribePolicyDetailsRequest,
    ) -> adcp_20220101_models.DescribePolicyDetailsResponse:
        runtime = util_models.RuntimeOptions()
        return self.describe_policy_details_with_options(request, runtime)

    async def describe_policy_details_async(
        self,
        request: adcp_20220101_models.DescribePolicyDetailsRequest,
    ) -> adcp_20220101_models.DescribePolicyDetailsResponse:
        runtime = util_models.RuntimeOptions()
        return await self.describe_policy_details_with_options_async(request, runtime)

    def describe_policy_governance_in_cluster_with_options(
        self,
        request: adcp_20220101_models.DescribePolicyGovernanceInClusterRequest,
        runtime: util_models.RuntimeOptions,
    ) -> adcp_20220101_models.DescribePolicyGovernanceInClusterResponse:
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.cluster_id):
            query['ClusterId'] = request.cluster_id
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='DescribePolicyGovernanceInCluster',
            version='2022-01-01',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            adcp_20220101_models.DescribePolicyGovernanceInClusterResponse(),
            self.call_api(params, req, runtime)
        )

    async def describe_policy_governance_in_cluster_with_options_async(
        self,
        request: adcp_20220101_models.DescribePolicyGovernanceInClusterRequest,
        runtime: util_models.RuntimeOptions,
    ) -> adcp_20220101_models.DescribePolicyGovernanceInClusterResponse:
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.cluster_id):
            query['ClusterId'] = request.cluster_id
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='DescribePolicyGovernanceInCluster',
            version='2022-01-01',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            adcp_20220101_models.DescribePolicyGovernanceInClusterResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def describe_policy_governance_in_cluster(
        self,
        request: adcp_20220101_models.DescribePolicyGovernanceInClusterRequest,
    ) -> adcp_20220101_models.DescribePolicyGovernanceInClusterResponse:
        runtime = util_models.RuntimeOptions()
        return self.describe_policy_governance_in_cluster_with_options(request, runtime)

    async def describe_policy_governance_in_cluster_async(
        self,
        request: adcp_20220101_models.DescribePolicyGovernanceInClusterRequest,
    ) -> adcp_20220101_models.DescribePolicyGovernanceInClusterResponse:
        runtime = util_models.RuntimeOptions()
        return await self.describe_policy_governance_in_cluster_with_options_async(request, runtime)

    def describe_policy_instances_with_options(
        self,
        request: adcp_20220101_models.DescribePolicyInstancesRequest,
        runtime: util_models.RuntimeOptions,
    ) -> adcp_20220101_models.DescribePolicyInstancesResponse:
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.cluster_id):
            query['ClusterId'] = request.cluster_id
        if not UtilClient.is_unset(request.policy_name):
            query['PolicyName'] = request.policy_name
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='DescribePolicyInstances',
            version='2022-01-01',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            adcp_20220101_models.DescribePolicyInstancesResponse(),
            self.call_api(params, req, runtime)
        )

    async def describe_policy_instances_with_options_async(
        self,
        request: adcp_20220101_models.DescribePolicyInstancesRequest,
        runtime: util_models.RuntimeOptions,
    ) -> adcp_20220101_models.DescribePolicyInstancesResponse:
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.cluster_id):
            query['ClusterId'] = request.cluster_id
        if not UtilClient.is_unset(request.policy_name):
            query['PolicyName'] = request.policy_name
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='DescribePolicyInstances',
            version='2022-01-01',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            adcp_20220101_models.DescribePolicyInstancesResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def describe_policy_instances(
        self,
        request: adcp_20220101_models.DescribePolicyInstancesRequest,
    ) -> adcp_20220101_models.DescribePolicyInstancesResponse:
        runtime = util_models.RuntimeOptions()
        return self.describe_policy_instances_with_options(request, runtime)

    async def describe_policy_instances_async(
        self,
        request: adcp_20220101_models.DescribePolicyInstancesRequest,
    ) -> adcp_20220101_models.DescribePolicyInstancesResponse:
        runtime = util_models.RuntimeOptions()
        return await self.describe_policy_instances_with_options_async(request, runtime)

    def describe_policy_instances_status_with_options(
        self,
        request: adcp_20220101_models.DescribePolicyInstancesStatusRequest,
        runtime: util_models.RuntimeOptions,
    ) -> adcp_20220101_models.DescribePolicyInstancesStatusResponse:
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.cluster_id):
            query['ClusterId'] = request.cluster_id
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='DescribePolicyInstancesStatus',
            version='2022-01-01',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            adcp_20220101_models.DescribePolicyInstancesStatusResponse(),
            self.call_api(params, req, runtime)
        )

    async def describe_policy_instances_status_with_options_async(
        self,
        request: adcp_20220101_models.DescribePolicyInstancesStatusRequest,
        runtime: util_models.RuntimeOptions,
    ) -> adcp_20220101_models.DescribePolicyInstancesStatusResponse:
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.cluster_id):
            query['ClusterId'] = request.cluster_id
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='DescribePolicyInstancesStatus',
            version='2022-01-01',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            adcp_20220101_models.DescribePolicyInstancesStatusResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def describe_policy_instances_status(
        self,
        request: adcp_20220101_models.DescribePolicyInstancesStatusRequest,
    ) -> adcp_20220101_models.DescribePolicyInstancesStatusResponse:
        runtime = util_models.RuntimeOptions()
        return self.describe_policy_instances_status_with_options(request, runtime)

    async def describe_policy_instances_status_async(
        self,
        request: adcp_20220101_models.DescribePolicyInstancesStatusRequest,
    ) -> adcp_20220101_models.DescribePolicyInstancesStatusResponse:
        runtime = util_models.RuntimeOptions()
        return await self.describe_policy_instances_status_with_options_async(request, runtime)

    def describe_regions_with_options(
        self,
        request: adcp_20220101_models.DescribeRegionsRequest,
        runtime: util_models.RuntimeOptions,
    ) -> adcp_20220101_models.DescribeRegionsResponse:
        UtilClient.validate_model(request)
        query = OpenApiUtilClient.query(UtilClient.to_map(request))
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='DescribeRegions',
            version='2022-01-01',
            protocol='HTTPS',
            pathname='/',
            method='GET',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            adcp_20220101_models.DescribeRegionsResponse(),
            self.call_api(params, req, runtime)
        )

    async def describe_regions_with_options_async(
        self,
        request: adcp_20220101_models.DescribeRegionsRequest,
        runtime: util_models.RuntimeOptions,
    ) -> adcp_20220101_models.DescribeRegionsResponse:
        UtilClient.validate_model(request)
        query = OpenApiUtilClient.query(UtilClient.to_map(request))
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='DescribeRegions',
            version='2022-01-01',
            protocol='HTTPS',
            pathname='/',
            method='GET',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            adcp_20220101_models.DescribeRegionsResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def describe_regions(
        self,
        request: adcp_20220101_models.DescribeRegionsRequest,
    ) -> adcp_20220101_models.DescribeRegionsResponse:
        runtime = util_models.RuntimeOptions()
        return self.describe_regions_with_options(request, runtime)

    async def describe_regions_async(
        self,
        request: adcp_20220101_models.DescribeRegionsRequest,
    ) -> adcp_20220101_models.DescribeRegionsResponse:
        runtime = util_models.RuntimeOptions()
        return await self.describe_regions_with_options_async(request, runtime)

    def describe_user_permissions_with_options(
        self,
        request: adcp_20220101_models.DescribeUserPermissionsRequest,
        runtime: util_models.RuntimeOptions,
    ) -> adcp_20220101_models.DescribeUserPermissionsResponse:
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.user_id):
            query['UserId'] = request.user_id
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='DescribeUserPermissions',
            version='2022-01-01',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            adcp_20220101_models.DescribeUserPermissionsResponse(),
            self.call_api(params, req, runtime)
        )

    async def describe_user_permissions_with_options_async(
        self,
        request: adcp_20220101_models.DescribeUserPermissionsRequest,
        runtime: util_models.RuntimeOptions,
    ) -> adcp_20220101_models.DescribeUserPermissionsResponse:
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.user_id):
            query['UserId'] = request.user_id
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='DescribeUserPermissions',
            version='2022-01-01',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            adcp_20220101_models.DescribeUserPermissionsResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def describe_user_permissions(
        self,
        request: adcp_20220101_models.DescribeUserPermissionsRequest,
    ) -> adcp_20220101_models.DescribeUserPermissionsResponse:
        runtime = util_models.RuntimeOptions()
        return self.describe_user_permissions_with_options(request, runtime)

    async def describe_user_permissions_async(
        self,
        request: adcp_20220101_models.DescribeUserPermissionsRequest,
    ) -> adcp_20220101_models.DescribeUserPermissionsResponse:
        runtime = util_models.RuntimeOptions()
        return await self.describe_user_permissions_with_options_async(request, runtime)

    def detach_cluster_from_hub_with_options(
        self,
        request: adcp_20220101_models.DetachClusterFromHubRequest,
        runtime: util_models.RuntimeOptions,
    ) -> adcp_20220101_models.DetachClusterFromHubResponse:
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.cluster_id):
            query['ClusterId'] = request.cluster_id
        if not UtilClient.is_unset(request.detach_from_mesh):
            query['DetachFromMesh'] = request.detach_from_mesh
        body = {}
        if not UtilClient.is_unset(request.cluster_ids):
            body['ClusterIds'] = request.cluster_ids
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query),
            body=OpenApiUtilClient.parse_to_map(body)
        )
        params = open_api_models.Params(
            action='DetachClusterFromHub',
            version='2022-01-01',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            adcp_20220101_models.DetachClusterFromHubResponse(),
            self.call_api(params, req, runtime)
        )

    async def detach_cluster_from_hub_with_options_async(
        self,
        request: adcp_20220101_models.DetachClusterFromHubRequest,
        runtime: util_models.RuntimeOptions,
    ) -> adcp_20220101_models.DetachClusterFromHubResponse:
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.cluster_id):
            query['ClusterId'] = request.cluster_id
        if not UtilClient.is_unset(request.detach_from_mesh):
            query['DetachFromMesh'] = request.detach_from_mesh
        body = {}
        if not UtilClient.is_unset(request.cluster_ids):
            body['ClusterIds'] = request.cluster_ids
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query),
            body=OpenApiUtilClient.parse_to_map(body)
        )
        params = open_api_models.Params(
            action='DetachClusterFromHub',
            version='2022-01-01',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            adcp_20220101_models.DetachClusterFromHubResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def detach_cluster_from_hub(
        self,
        request: adcp_20220101_models.DetachClusterFromHubRequest,
    ) -> adcp_20220101_models.DetachClusterFromHubResponse:
        runtime = util_models.RuntimeOptions()
        return self.detach_cluster_from_hub_with_options(request, runtime)

    async def detach_cluster_from_hub_async(
        self,
        request: adcp_20220101_models.DetachClusterFromHubRequest,
    ) -> adcp_20220101_models.DetachClusterFromHubResponse:
        runtime = util_models.RuntimeOptions()
        return await self.detach_cluster_from_hub_with_options_async(request, runtime)

    def grant_user_permission_with_options(
        self,
        request: adcp_20220101_models.GrantUserPermissionRequest,
        runtime: util_models.RuntimeOptions,
    ) -> adcp_20220101_models.GrantUserPermissionResponse:
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.cluster_id):
            query['ClusterId'] = request.cluster_id
        if not UtilClient.is_unset(request.is_ram_role):
            query['IsRamRole'] = request.is_ram_role
        if not UtilClient.is_unset(request.namespace):
            query['Namespace'] = request.namespace
        if not UtilClient.is_unset(request.role_name):
            query['RoleName'] = request.role_name
        if not UtilClient.is_unset(request.role_type):
            query['RoleType'] = request.role_type
        if not UtilClient.is_unset(request.user_id):
            query['UserId'] = request.user_id
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='GrantUserPermission',
            version='2022-01-01',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            adcp_20220101_models.GrantUserPermissionResponse(),
            self.call_api(params, req, runtime)
        )

    async def grant_user_permission_with_options_async(
        self,
        request: adcp_20220101_models.GrantUserPermissionRequest,
        runtime: util_models.RuntimeOptions,
    ) -> adcp_20220101_models.GrantUserPermissionResponse:
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.cluster_id):
            query['ClusterId'] = request.cluster_id
        if not UtilClient.is_unset(request.is_ram_role):
            query['IsRamRole'] = request.is_ram_role
        if not UtilClient.is_unset(request.namespace):
            query['Namespace'] = request.namespace
        if not UtilClient.is_unset(request.role_name):
            query['RoleName'] = request.role_name
        if not UtilClient.is_unset(request.role_type):
            query['RoleType'] = request.role_type
        if not UtilClient.is_unset(request.user_id):
            query['UserId'] = request.user_id
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='GrantUserPermission',
            version='2022-01-01',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            adcp_20220101_models.GrantUserPermissionResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def grant_user_permission(
        self,
        request: adcp_20220101_models.GrantUserPermissionRequest,
    ) -> adcp_20220101_models.GrantUserPermissionResponse:
        runtime = util_models.RuntimeOptions()
        return self.grant_user_permission_with_options(request, runtime)

    async def grant_user_permission_async(
        self,
        request: adcp_20220101_models.GrantUserPermissionRequest,
    ) -> adcp_20220101_models.GrantUserPermissionResponse:
        runtime = util_models.RuntimeOptions()
        return await self.grant_user_permission_with_options_async(request, runtime)

    def grant_user_permissions_with_options(
        self,
        tmp_req: adcp_20220101_models.GrantUserPermissionsRequest,
        runtime: util_models.RuntimeOptions,
    ) -> adcp_20220101_models.GrantUserPermissionsResponse:
        """
        @deprecated : GrantUserPermissions is deprecated, please use adcp::2022-01-01::GrantUserPermission instead.
        
        @param tmp_req: GrantUserPermissionsRequest
        @param runtime: runtime options for this request RuntimeOptions
        @return: GrantUserPermissionsResponse
        Deprecated
        """
        UtilClient.validate_model(tmp_req)
        request = adcp_20220101_models.GrantUserPermissionsShrinkRequest()
        OpenApiUtilClient.convert(tmp_req, request)
        if not UtilClient.is_unset(tmp_req.permissions):
            request.permissions_shrink = OpenApiUtilClient.array_to_string_with_specified_style(tmp_req.permissions, 'Permissions', 'json')
        query = {}
        if not UtilClient.is_unset(request.permissions_shrink):
            query['Permissions'] = request.permissions_shrink
        if not UtilClient.is_unset(request.user_id):
            query['UserId'] = request.user_id
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='GrantUserPermissions',
            version='2022-01-01',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            adcp_20220101_models.GrantUserPermissionsResponse(),
            self.call_api(params, req, runtime)
        )

    async def grant_user_permissions_with_options_async(
        self,
        tmp_req: adcp_20220101_models.GrantUserPermissionsRequest,
        runtime: util_models.RuntimeOptions,
    ) -> adcp_20220101_models.GrantUserPermissionsResponse:
        """
        @deprecated : GrantUserPermissions is deprecated, please use adcp::2022-01-01::GrantUserPermission instead.
        
        @param tmp_req: GrantUserPermissionsRequest
        @param runtime: runtime options for this request RuntimeOptions
        @return: GrantUserPermissionsResponse
        Deprecated
        """
        UtilClient.validate_model(tmp_req)
        request = adcp_20220101_models.GrantUserPermissionsShrinkRequest()
        OpenApiUtilClient.convert(tmp_req, request)
        if not UtilClient.is_unset(tmp_req.permissions):
            request.permissions_shrink = OpenApiUtilClient.array_to_string_with_specified_style(tmp_req.permissions, 'Permissions', 'json')
        query = {}
        if not UtilClient.is_unset(request.permissions_shrink):
            query['Permissions'] = request.permissions_shrink
        if not UtilClient.is_unset(request.user_id):
            query['UserId'] = request.user_id
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='GrantUserPermissions',
            version='2022-01-01',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            adcp_20220101_models.GrantUserPermissionsResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def grant_user_permissions(
        self,
        request: adcp_20220101_models.GrantUserPermissionsRequest,
    ) -> adcp_20220101_models.GrantUserPermissionsResponse:
        """
        @deprecated : GrantUserPermissions is deprecated, please use adcp::2022-01-01::GrantUserPermission instead.
        
        @param request: GrantUserPermissionsRequest
        @return: GrantUserPermissionsResponse
        Deprecated
        """
        runtime = util_models.RuntimeOptions()
        return self.grant_user_permissions_with_options(request, runtime)

    async def grant_user_permissions_async(
        self,
        request: adcp_20220101_models.GrantUserPermissionsRequest,
    ) -> adcp_20220101_models.GrantUserPermissionsResponse:
        """
        @deprecated : GrantUserPermissions is deprecated, please use adcp::2022-01-01::GrantUserPermission instead.
        
        @param request: GrantUserPermissionsRequest
        @return: GrantUserPermissionsResponse
        Deprecated
        """
        runtime = util_models.RuntimeOptions()
        return await self.grant_user_permissions_with_options_async(request, runtime)

    def update_hub_cluster_feature_with_options(
        self,
        tmp_req: adcp_20220101_models.UpdateHubClusterFeatureRequest,
        runtime: util_models.RuntimeOptions,
    ) -> adcp_20220101_models.UpdateHubClusterFeatureResponse:
        UtilClient.validate_model(tmp_req)
        request = adcp_20220101_models.UpdateHubClusterFeatureShrinkRequest()
        OpenApiUtilClient.convert(tmp_req, request)
        if not UtilClient.is_unset(tmp_req.access_control_list):
            request.access_control_list_shrink = OpenApiUtilClient.array_to_string_with_specified_style(tmp_req.access_control_list, 'AccessControlList', 'json')
        if not UtilClient.is_unset(tmp_req.v_switches):
            request.v_switches_shrink = OpenApiUtilClient.array_to_string_with_specified_style(tmp_req.v_switches, 'VSwitches', 'json')
        query = {}
        if not UtilClient.is_unset(request.access_control_list_shrink):
            query['AccessControlList'] = request.access_control_list_shrink
        if not UtilClient.is_unset(request.api_server_eip_id):
            query['ApiServerEipId'] = request.api_server_eip_id
        if not UtilClient.is_unset(request.argo_cdenabled):
            query['ArgoCDEnabled'] = request.argo_cdenabled
        if not UtilClient.is_unset(request.argo_cdhaenabled):
            query['ArgoCDHAEnabled'] = request.argo_cdhaenabled
        if not UtilClient.is_unset(request.argo_events_enabled):
            query['ArgoEventsEnabled'] = request.argo_events_enabled
        if not UtilClient.is_unset(request.argo_server_enabled):
            query['ArgoServerEnabled'] = request.argo_server_enabled
        if not UtilClient.is_unset(request.audit_log_enabled):
            query['AuditLogEnabled'] = request.audit_log_enabled
        if not UtilClient.is_unset(request.cluster_id):
            query['ClusterId'] = request.cluster_id
        if not UtilClient.is_unset(request.deletion_protection):
            query['DeletionProtection'] = request.deletion_protection
        if not UtilClient.is_unset(request.enable_mesh):
            query['EnableMesh'] = request.enable_mesh
        if not UtilClient.is_unset(request.gateway_enabled):
            query['GatewayEnabled'] = request.gateway_enabled
        if not UtilClient.is_unset(request.monitor_enabled):
            query['MonitorEnabled'] = request.monitor_enabled
        if not UtilClient.is_unset(request.name):
            query['Name'] = request.name
        if not UtilClient.is_unset(request.price_limit):
            query['PriceLimit'] = request.price_limit
        if not UtilClient.is_unset(request.public_access_enabled):
            query['PublicAccessEnabled'] = request.public_access_enabled
        if not UtilClient.is_unset(request.public_api_server_enabled):
            query['PublicApiServerEnabled'] = request.public_api_server_enabled
        if not UtilClient.is_unset(request.v_switches_shrink):
            query['VSwitches'] = request.v_switches_shrink
        if not UtilClient.is_unset(request.workflow_schedule_mode):
            query['WorkflowScheduleMode'] = request.workflow_schedule_mode
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='UpdateHubClusterFeature',
            version='2022-01-01',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            adcp_20220101_models.UpdateHubClusterFeatureResponse(),
            self.call_api(params, req, runtime)
        )

    async def update_hub_cluster_feature_with_options_async(
        self,
        tmp_req: adcp_20220101_models.UpdateHubClusterFeatureRequest,
        runtime: util_models.RuntimeOptions,
    ) -> adcp_20220101_models.UpdateHubClusterFeatureResponse:
        UtilClient.validate_model(tmp_req)
        request = adcp_20220101_models.UpdateHubClusterFeatureShrinkRequest()
        OpenApiUtilClient.convert(tmp_req, request)
        if not UtilClient.is_unset(tmp_req.access_control_list):
            request.access_control_list_shrink = OpenApiUtilClient.array_to_string_with_specified_style(tmp_req.access_control_list, 'AccessControlList', 'json')
        if not UtilClient.is_unset(tmp_req.v_switches):
            request.v_switches_shrink = OpenApiUtilClient.array_to_string_with_specified_style(tmp_req.v_switches, 'VSwitches', 'json')
        query = {}
        if not UtilClient.is_unset(request.access_control_list_shrink):
            query['AccessControlList'] = request.access_control_list_shrink
        if not UtilClient.is_unset(request.api_server_eip_id):
            query['ApiServerEipId'] = request.api_server_eip_id
        if not UtilClient.is_unset(request.argo_cdenabled):
            query['ArgoCDEnabled'] = request.argo_cdenabled
        if not UtilClient.is_unset(request.argo_cdhaenabled):
            query['ArgoCDHAEnabled'] = request.argo_cdhaenabled
        if not UtilClient.is_unset(request.argo_events_enabled):
            query['ArgoEventsEnabled'] = request.argo_events_enabled
        if not UtilClient.is_unset(request.argo_server_enabled):
            query['ArgoServerEnabled'] = request.argo_server_enabled
        if not UtilClient.is_unset(request.audit_log_enabled):
            query['AuditLogEnabled'] = request.audit_log_enabled
        if not UtilClient.is_unset(request.cluster_id):
            query['ClusterId'] = request.cluster_id
        if not UtilClient.is_unset(request.deletion_protection):
            query['DeletionProtection'] = request.deletion_protection
        if not UtilClient.is_unset(request.enable_mesh):
            query['EnableMesh'] = request.enable_mesh
        if not UtilClient.is_unset(request.gateway_enabled):
            query['GatewayEnabled'] = request.gateway_enabled
        if not UtilClient.is_unset(request.monitor_enabled):
            query['MonitorEnabled'] = request.monitor_enabled
        if not UtilClient.is_unset(request.name):
            query['Name'] = request.name
        if not UtilClient.is_unset(request.price_limit):
            query['PriceLimit'] = request.price_limit
        if not UtilClient.is_unset(request.public_access_enabled):
            query['PublicAccessEnabled'] = request.public_access_enabled
        if not UtilClient.is_unset(request.public_api_server_enabled):
            query['PublicApiServerEnabled'] = request.public_api_server_enabled
        if not UtilClient.is_unset(request.v_switches_shrink):
            query['VSwitches'] = request.v_switches_shrink
        if not UtilClient.is_unset(request.workflow_schedule_mode):
            query['WorkflowScheduleMode'] = request.workflow_schedule_mode
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='UpdateHubClusterFeature',
            version='2022-01-01',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            adcp_20220101_models.UpdateHubClusterFeatureResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def update_hub_cluster_feature(
        self,
        request: adcp_20220101_models.UpdateHubClusterFeatureRequest,
    ) -> adcp_20220101_models.UpdateHubClusterFeatureResponse:
        runtime = util_models.RuntimeOptions()
        return self.update_hub_cluster_feature_with_options(request, runtime)

    async def update_hub_cluster_feature_async(
        self,
        request: adcp_20220101_models.UpdateHubClusterFeatureRequest,
    ) -> adcp_20220101_models.UpdateHubClusterFeatureResponse:
        runtime = util_models.RuntimeOptions()
        return await self.update_hub_cluster_feature_with_options_async(request, runtime)

    def update_user_permission_with_options(
        self,
        request: adcp_20220101_models.UpdateUserPermissionRequest,
        runtime: util_models.RuntimeOptions,
    ) -> adcp_20220101_models.UpdateUserPermissionResponse:
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.cluster_id):
            query['ClusterId'] = request.cluster_id
        if not UtilClient.is_unset(request.namespace):
            query['Namespace'] = request.namespace
        if not UtilClient.is_unset(request.role_name):
            query['RoleName'] = request.role_name
        if not UtilClient.is_unset(request.role_type):
            query['RoleType'] = request.role_type
        if not UtilClient.is_unset(request.user_id):
            query['UserId'] = request.user_id
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='UpdateUserPermission',
            version='2022-01-01',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            adcp_20220101_models.UpdateUserPermissionResponse(),
            self.call_api(params, req, runtime)
        )

    async def update_user_permission_with_options_async(
        self,
        request: adcp_20220101_models.UpdateUserPermissionRequest,
        runtime: util_models.RuntimeOptions,
    ) -> adcp_20220101_models.UpdateUserPermissionResponse:
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.cluster_id):
            query['ClusterId'] = request.cluster_id
        if not UtilClient.is_unset(request.namespace):
            query['Namespace'] = request.namespace
        if not UtilClient.is_unset(request.role_name):
            query['RoleName'] = request.role_name
        if not UtilClient.is_unset(request.role_type):
            query['RoleType'] = request.role_type
        if not UtilClient.is_unset(request.user_id):
            query['UserId'] = request.user_id
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='UpdateUserPermission',
            version='2022-01-01',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            adcp_20220101_models.UpdateUserPermissionResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def update_user_permission(
        self,
        request: adcp_20220101_models.UpdateUserPermissionRequest,
    ) -> adcp_20220101_models.UpdateUserPermissionResponse:
        runtime = util_models.RuntimeOptions()
        return self.update_user_permission_with_options(request, runtime)

    async def update_user_permission_async(
        self,
        request: adcp_20220101_models.UpdateUserPermissionRequest,
    ) -> adcp_20220101_models.UpdateUserPermissionResponse:
        runtime = util_models.RuntimeOptions()
        return await self.update_user_permission_with_options_async(request, runtime)
