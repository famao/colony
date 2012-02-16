# vim: tabstop=4 shiftwidth=4 softtabstop=4

# Copyright 2011 United States Government as represented by the
# Administrator of the National Aeronautics and Space Administration.
# All Rights Reserved.
#
# Copyright 2011 Nebula, Inc.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

from django.conf.urls.defaults import *

SECURITY_GROUPS = r'^(?P<tenant_id>[^/]+)/security_groups/(?P<security_group_id>[^/]+)/%s$'
INSTANCES = r'^(?P<tenant_id>[^/]+)/instances/(?P<instance_id>[^/]+)/%s$'
IMAGES = r'^(?P<tenant_id>[^/]+)/images/(?P<image_id>[^/]+)/%s$'
IMAGES_METADATA = r'^(?P<tenant_id>[^/]+)/images_metadata/(?P<image_id>[^/]+)/%s$'
KEYPAIRS = r'^(?P<tenant_id>[^/]+)/keypairs/%s$'
SNAPSHOTS = r'^(?P<tenant_id>[^/]+)/snapshots/(?P<instance_id>[^/]+)/%s$'
CONTAINERS = r'^(?P<tenant_id>[^/]+)/containers/%s$'
USERS = r'^(?P<tenant_id>[^/]+)/containers/user/%s$'
FLOATING_IPS = r'^(?P<tenant_id>[^/]+)/floating_ips/(?P<ip_id>[^/]+)/%s$'
OBJECTS = r'^(?P<tenant_id>[^/]+)/containers/(?P<container_name>[^/]+)/%s$'
NETWORKS = r'^(?P<tenant_id>[^/]+)/networks/%s$'
PORTS = r'^(?P<tenant_id>[^/]+)/networks/(?P<network_id>[^/]+)/ports/%s$'

urlpatterns = patterns('django_openstack.dash.views.instances',
    url(r'^(?P<tenant_id>[^/]+)/$', 'usage', name='dash_usage'),
    url(r'^(?P<tenant_id>[^/]+)/instances/$', 'index', name='dash_instances'),
    url(r'^(?P<tenant_id>[^/]+)/instances/refresh$', 'refresh',
        name='dash_instances_refresh'),
    url(INSTANCES % 'console', 'console', name='dash_instances_console'),
    url(INSTANCES % 'vnc', 'vnc', name='dash_instances_vnc'),
    url(INSTANCES % 'update', 'update', name='dash_instances_update'),
)

urlpatterns += patterns('django_openstack.dash.views.security_groups',
    url(r'^(?P<tenant_id>[^/]+)/security_groups/$', 'index', name='dash_security_groups'),
    url(r'^(?P<tenant_id>[^/]+)/security_groups/create$', 'create', name='dash_security_groups_create'),
    url(SECURITY_GROUPS % 'edit_rules', 'edit_rules', name='dash_security_groups_edit_rules'),
)

urlpatterns += patterns('django_openstack.dash.views.images',
    url(r'^(?P<tenant_id>[^/]+)/images/$', 'index', name='dash_images'),
    url(IMAGES % 'launch', 'launch', name='dash_images_launch'),
    url(IMAGES % 'update', 'update', name='dash_images_update'),
)

urlpatterns += patterns('django_openstack.dash.views.images_metadata',
    url(r'^(?P<tenant_id>[^/]+)/images_metadata/$', 'index', name='dash_images_metadata'),
    url(IMAGES_METADATA % 'download', 'download', name='dash_metadata_download'),
    url(IMAGES_METADATA % 'update', 'update', name='dash_metadata_update'),
)

urlpatterns += patterns('django_openstack.dash.views.keypairs',
    url(r'^(?P<tenant_id>[^/]+)/keypairs/$', 'index', name='dash_keypairs'),
    url(KEYPAIRS % 'create', 'create', name='dash_keypairs_create'),
    url(KEYPAIRS % 'import', 'import_keypair', name='dash_keypairs_import'),
)

urlpatterns += patterns('django_openstack.dash.views.floating_ips',
    url(r'^(?P<tenant_id>[^/]+)/floating_ips/$', 'index', name='dash_floating_ips'),
    url(FLOATING_IPS % 'associate', 'associate', name='dash_floating_ips_associate'),
    url(FLOATING_IPS % 'disassociate', 'disassociate', name='dash_floating_ips_disassociate'),
)

urlpatterns += patterns('django_openstack.dash.views.snapshots',
    url(r'^(?P<tenant_id>[^/]+)/snapshots/$', 'index', name='dash_snapshots'),
    url(SNAPSHOTS % 'create', 'create', name='dash_snapshots_create'),
)

# Swift containers and objects.
urlpatterns += patterns('django_openstack.dash.views.containers',
    url(CONTAINERS % '', 'index', name='dash_containers'),
    url(CONTAINERS % 'index_storage_url', 'index_storage_url', name='dash_containers_storage_url'),
    url(CONTAINERS % 'create', 'create', name='dash_containers_create'),
    url(OBJECTS % 'public', 'public', name='dash_containers_public'),
    url(OBJECTS % 'acl', 'acl', name='dash_containers_acl'),
    url(OBJECTS % 'meta', 'meta', name='dash_containers_meta'),
    url(USERS % 'user_list', 'user_list', name='dash_users_list'),
)

urlpatterns += patterns('django_openstack.dash.views.objects',
    url(OBJECTS % '', 'index', name='dash_objects'),
    url(OBJECTS % 'upload', 'upload', name='dash_objects_upload'),
    url(OBJECTS % '(?P<object_name>[^/]+)/copy',
        'copy', name='dash_object_copy'),
    url(OBJECTS % '(?P<object_name>[^/]+)/download',
        'download', name='dash_objects_download'),
    url(OBJECTS % '(?P<object_name>[^/]+)/meta',
        'meta', name='dash_objects_meta'),
)

urlpatterns += patterns('django_openstack.dash.views.networks',
    url(r'^(?P<tenant_id>[^/]+)/networks/$', 'index', name='dash_networks'),
    url(NETWORKS % 'create', 'create', name='dash_network_create'),
    url(NETWORKS % '(?P<network_id>[^/]+)/detail', 'detail',
        name='dash_networks_detail'),
    url(NETWORKS % '(?P<network_id>[^/]+)/rename', 'rename',
        name='dash_network_rename'),
)

urlpatterns += patterns('django_openstack.dash.views.ports',
    url(PORTS % 'create', 'create', name='dash_ports_create'),
    url(PORTS % '(?P<port_id>[^/]+)/attach', 'attach',
        name='dash_ports_attach'),
)
