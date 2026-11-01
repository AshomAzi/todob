from datetime import date

from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from .models import Task


class EditTaskTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="owner", password="test-password")
        self.other_user = User.objects.create_user(username="other", password="test-password")
        self.task = Task.objects.create(
            user=self.user,
            title="Original task",
            description="Original description",
            due_date=date(2026, 12, 1),
            priority=Task.Priority.Low,
        )
        self.url = reverse("edit_task", args=[self.task.id])

    def test_dashboard_uses_root_relative_static_assets(self):
        self.client.login(username="owner", password="test-password")

        response = self.client.get(reverse("dashboard"))

        self.assertContains(response, 'href="/static/css/dashboard.css"')
        self.assertContains(response, 'src="/static/js/dashboard.js"')

    def test_owner_can_edit_task(self):
        self.client.login(username="owner", password="test-password")

        response = self.client.post(self.url, {
            "title": "Updated task",
            "description": "Updated description",
            "due_date": "2026-12-15",
            "priority": Task.Priority.Medium,
        }, follow=True)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "priority-medium")
        self.task.refresh_from_db()
        self.assertEqual(self.task.title, "Updated task")
        self.assertEqual(self.task.description, "Updated description")
        self.assertEqual(self.task.due_date, date(2026, 12, 15))
        self.assertEqual(self.task.priority, Task.Priority.Medium)

    def test_edit_link_opens_prefilled_edit_form_without_javascript(self):
        self.client.login(username="owner", password="test-password")

        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'id="taskModal" class="modal-overlay active"')
        self.assertContains(response, 'value="Original task"')
        self.assertContains(response, 'value="2026-12-01"')
        self.assertContains(response, "Original description")
        self.assertContains(response, '<option value="low" selected>Low</option>')

    def test_invalid_edit_keeps_task_and_renders_errors(self):
        self.client.login(username="owner", password="test-password")

        response = self.client.post(self.url, {
            "title": "",
            "description": "Updated description",
            "due_date": "not-a-date",
            "priority": "urgent",
        })

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Edit Task")
        self.assertContains(response, "This field is required.")
        self.task.refresh_from_db()
        self.assertEqual(self.task.title, "Original task")

    def test_user_cannot_edit_another_users_task(self):
        self.client.login(username="other", password="test-password")

        response = self.client.post(self.url, {
            "title": "Stolen update",
            "description": "No",
            "due_date": "2026-12-15",
            "priority": Task.Priority.High,
        })

        self.assertEqual(response.status_code, 404)
        self.task.refresh_from_db()
        self.assertEqual(self.task.title, "Original task")
