from service_catalog.forms.approval_workflow_form import ApprovalWorkflowForm, ApprovalWorkflowFormEdit
from service_catalog.models import ApprovalWorkflow
from tests.test_service_catalog.base import BaseTest


class TestApprovalWorkflowForm(BaseTest):

    def setUp(self):
        super(TestApprovalWorkflowForm, self).setUp()

    def test_create_approval_workflow(self):
        data = {
            'name': 'test_approval_workflow',
            'operation': self.create_operation_test,
            'scopes': [self.test_quota_scope]
        }
        form = ApprovalWorkflowForm(data)
        self.assertTrue(form.is_valid())

    def test_clean(self):
        existing_approval = ApprovalWorkflow.objects.create(name="test",
                                                            operation=self.create_operation_test,
                                                            enabled=True)
        existing_approval.scopes.set([self.test_quota_scope])

        data = {
            'name': 'test_approval_workflow',
            'operation': self.create_operation_test,
            'scopes': [self.test_quota_scope]
        }
        form = ApprovalWorkflowForm(data)
        self.assertFalse(form.is_valid())
        self.assertIn("has already an approval workflow", form["scopes"].errors[0])

    def test_add_scope_to_scopes(self):
        existing_approval = ApprovalWorkflow.objects.create(name="test",
                                                            operation=self.create_operation_test,
                                                            enabled=True)
        existing_approval.scopes.set([self.test_quota_scope])

        data = {
            'name': 'test_approval_workflow',
            'operation': self.create_operation_test,
            'scopes': [self.test_quota_scope, self.test_quota_scope2]
        }
        form = ApprovalWorkflowFormEdit(instance=existing_approval, data=data)
        self.assertTrue(form.is_valid())

    def test_clean_with_empty_scopes(self):
        existing_approval = ApprovalWorkflow.objects.create(name="test",
                                                            operation=self.create_operation_test,
                                                            enabled=True)

        data = {
            'name': 'test_approval_workflow',
            'operation': self.create_operation_test
        }
        form = ApprovalWorkflowForm(data)
        self.assertFalse(form.is_valid())
        self.assertIn("An approval workflow for all scopes already exists", form["scopes"].errors[0])

    def test_create_specific_workflow_with_generic_already_there(self):
        # we have a global workflow on a particular operation
        ApprovalWorkflow.objects.create(name="generic",
                                        operation=self.create_operation_test,
                                        enabled=True)

        # we add a new workflow targeting the same operation but restricted to a scope
        data = {
            'name': 'specific',
            'operation': self.create_operation_test,
            'scopes': [self.test_quota_scope]
        }
        form = ApprovalWorkflowForm(data)
        self.assertTrue(form.is_valid())

    def test_cannot_change_operation_when_edit(self):
        existing_approval = ApprovalWorkflow.objects.create(name="test",
                                                            operation=self.create_operation_test_2,
                                                            enabled=True)

        data = {
            'name': "test1",
            'operation': self.update_operation_test
        }
        form = ApprovalWorkflowFormEdit(instance=existing_approval, data=data)
        self.assertTrue(form.is_valid())
        # Check that operation is not changed
        self.assertEqual(existing_approval.operation, self.create_operation_test_2)
        self.assertEqual(existing_approval.name, data["name"])
