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

import logging

from django import template
from django import shortcuts
from django.contrib import messages

from django_openstack import api
from django_openstack import forms
from openstackx.api import exceptions as api_exceptions


LOG = logging.getLogger('django_openstack.auth.gakunin')


def login(request):
    if request.user and request.user.is_authenticated():
        return shortcuts.redirect('dash_containers', request.user.tenant_id)

    # check ssl
    if not request.is_secure():
        messages.error(request, "Gakunin Support needs to be accessed through TLS")
        return shortcuts.redirect('auth_login')
    from_email = request.META.get('email', None)
    from_eppn = request.META.get('eppn', None)

    try:
        token = None
        # first , try by eppn
        if from_eppn:
            token = api.token_create_by_eppn(request, from_eppn)
 
        # second, try by email
        if not token and from_email:
            token = api.token_create_by_email(request, from_email)
            if token:
                api.user_update_eppn(request, token.user['id'], from_eppn)
 
        def get_first_tenant_for_user():
            tenants = api.tenant_list_for_token(request, token.id)
            return tenants[0] if len(tenants) else None
 
        if not token:
            messages.error(request, "Can't retrieve information from Gakunin")
            return shortcuts.redirect('auth_login')
 
        tenant = get_first_tenant_for_user()
 
        if not tenant:
            messages.error(request, 'No tenants present for user')
            return shortcuts.redirect('auth_login')
 
        request.session['unscoped_token'] = token.id
 
        def is_admin(token):
            for role in token.user['roles']:
                if role['name'].lower() == 'admin':
                    return True
            return False
 
 
        request.session['admin'] = is_admin(token)
 
        if not token.user or not token.user.has_key('name'):
            return shortcuts.redirect('auth_login')
        request.session['serviceCatalog'] = token.serviceCatalog
        request.session['tenant_id'] = tenant.id
        request.session['tenant'] = tenant.name
        request.session['token'] = token.id
        request.session['user'] = token.user['name']
 
        return shortcuts.redirect('dash_containers', tenant.id)
    except Exception, e:
        messages.error('Exception occured while gakunin login %s' % str(e))
        return shortcuts.redirect('auth_login') 

