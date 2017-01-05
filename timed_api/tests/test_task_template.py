"""Tests for the task templates endpoint."""

from django.core.urlresolvers import reverse
from rest_framework.status import (HTTP_200_OK, HTTP_201_CREATED,
                                   HTTP_204_NO_CONTENT, HTTP_401_UNAUTHORIZED,
                                   HTTP_403_FORBIDDEN)

from timed.jsonapi_test_case import JSONAPITestCase
from timed_api.factories import TaskTemplateFactory


class TaskTemplateTests(JSONAPITestCase):
    """Tests for the task templates endpoint.

    This endpoint should be read only for normal users and project admins.
    """

    def setUp(self):
        """Setup the environment for the tests."""
        super().setUp()

        self.task_templates = TaskTemplateFactory.create_batch(5)

    def test_task_template_list(self):
        """Should respond with a list of task templates."""
        url = reverse('task-template-list')

        noauth_res = self.noauth_client.get(url)
        user_res   = self.client.get(url)

        assert noauth_res.status_code == HTTP_401_UNAUTHORIZED
        assert user_res.status_code == HTTP_200_OK

        result = self.result(user_res)

        assert len(result['data']) == len(self.task_templates)

    def test_task_template_detail(self):
        """Should respond with a single task template."""
        task_template = self.task_templates[0]

        url = reverse('task-template-detail', args=[
            task_template.id
        ])

        noauth_res = self.noauth_client.get(url)
        user_res   = self.client.get(url)

        assert noauth_res.status_code == HTTP_401_UNAUTHORIZED
        assert user_res.status_code == HTTP_200_OK

    def test_task_template_create(self):
        """Should create a new task template."""
        data = {
            'data': {
                'type': 'task-templates',
                'id': None,
                'attributes': {
                    'name': 'Test Task Template'
                }
            }
        }

        url = reverse('task-template-list')

        noauth_res        = self.noauth_client.post(url, data)
        user_res          = self.client.post(url, data)
        project_admin_res = self.project_admin_client.post(url, data)
        system_admin_res  = self.system_admin_client.post(url, data)

        assert noauth_res.status_code == HTTP_401_UNAUTHORIZED
        assert user_res.status_code == HTTP_403_FORBIDDEN
        assert project_admin_res.status_code == HTTP_403_FORBIDDEN
        assert system_admin_res.status_code == HTTP_201_CREATED

    def test_task_template_update(self):
        """Should update an existing task template."""
        task_template = self.task_templates[0]

        data = {
            'data': {
                'type': 'task-templates',
                'id': task_template.id,
                'attributes': {
                    'name': 'Test Task Template 2'
                }
            }
        }

        url = reverse('task-template-detail', args=[
            task_template.id
        ])

        noauth_res        = self.noauth_client.patch(url, data)
        user_res          = self.client.patch(url, data)
        project_admin_res = self.project_admin_client.patch(url, data)
        system_admin_res  = self.system_admin_client.patch(url, data)

        assert noauth_res.status_code == HTTP_401_UNAUTHORIZED
        assert user_res.status_code == HTTP_403_FORBIDDEN
        assert project_admin_res.status_code == HTTP_403_FORBIDDEN
        assert system_admin_res.status_code == HTTP_200_OK

        result = self.result(system_admin_res)

        assert (
            result['data']['attributes']['name'] ==
            data['data']['attributes']['name']
        )

    def test_task_template_delete(self):
        """Should delete a task template."""
        task_template = self.task_templates[0]

        url = reverse('task-template-detail', args=[
            task_template.id
        ])

        noauth_res        = self.noauth_client.delete(url)
        user_res          = self.client.delete(url)
        project_admin_res = self.project_admin_client.delete(url)
        system_admin_res  = self.system_admin_client.delete(url)

        assert noauth_res.status_code == HTTP_401_UNAUTHORIZED
        assert user_res.status_code == HTTP_403_FORBIDDEN
        assert project_admin_res.status_code == HTTP_403_FORBIDDEN
        assert system_admin_res.status_code == HTTP_204_NO_CONTENT
