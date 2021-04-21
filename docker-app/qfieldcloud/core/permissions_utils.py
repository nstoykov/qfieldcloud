import warnings
from typing import List, Union

from qfieldcloud.core.models import (
    Delta,
    Organization,
    OrganizationMember,
    Project,
    ProjectCollaborator,
)
from qfieldcloud.core.models import User as QfcUser


def _project_for_owner(user: QfcUser, project: Project):
    return Project.objects.for_user(user).filter(pk=project.pk)


def _organization_of_owner(user: QfcUser, organization: Organization):
    return Organization.objects.of_user(user).filter(pk=organization.pk)


def user_has_project_roles(
    user: QfcUser, project: Project, roles: List[ProjectCollaborator.Roles]
):
    return _project_for_owner(user, project).filter(user_role__in=roles).exists()


def user_has_organization_roles(
    user: QfcUser, organization: Organization, roles: List[OrganizationMember.Roles]
):
    return (
        _organization_of_owner(user, organization)
        .filter(membership_role__in=roles)
        .exists()
    )


def get_param_from_request(request, param):
    """Try to get the param from the request data or the request
    context, returns None otherwise"""

    result = request.data.get(param, None)
    if not result:
        result = request.parser_context["kwargs"].get(param, None)
    return result


def can_create_project(
    user: QfcUser, organization: Union[QfcUser, Organization] = None
) -> bool:
    """Return True if the `user` can create a project. Accepts additional
    `organizaiton` to check whether the user has permissions to do so on
    that organization. Return False otherwise."""

    if organization is None:
        return True
    if user == organization:
        return True

    if organization.is_organization and not isinstance(organization, Organization):
        organization = organization.organization  # type: ignore
    else:
        return False

    if user_has_organization_roles(
        user, organization, [OrganizationMember.Roles.ADMIN]
    ):
        return True

    return False


def can_read_project(user: QfcUser, project: Project) -> bool:
    return user_has_project_roles(
        user,
        project,
        [
            ProjectCollaborator.Roles.ADMIN,
            ProjectCollaborator.Roles.MANAGER,
            ProjectCollaborator.Roles.EDITOR,
            ProjectCollaborator.Roles.REPORTER,
            ProjectCollaborator.Roles.READER,
        ],
    )


ROLES_CAN_UPDATE_PROJECT = [
    ProjectCollaborator.Roles.ADMIN,
    ProjectCollaborator.Roles.MANAGER,
]
ROLES_CAN_DELETE_PROJECT = [
    ProjectCollaborator.Roles.ADMIN,
    ProjectCollaborator.Roles.MANAGER,
]


def can_update_project(user: QfcUser, project: Project) -> bool:
    warnings.warn(
        DeprecationWarning,
        "can_update_project is deprecated, use `project.user_role in ROLES_CAN_UPDATE_PROJECT` instead",
    )
    return user_has_project_roles(
        user,
        project,
        [
            ProjectCollaborator.Roles.ADMIN,
            ProjectCollaborator.Roles.MANAGER,
        ],
    )


def can_delete_project(user: QfcUser, project: Project) -> bool:
    warnings.warn(
        DeprecationWarning,
        "can_update_project is deprecated, use `project.user_role in ROLES_CAN_DELETE_PROJECT` instead",
    )
    return user_has_project_roles(
        user,
        project,
        [
            ProjectCollaborator.Roles.ADMIN,
            ProjectCollaborator.Roles.MANAGER,
        ],
    )


def can_create_files(user: QfcUser, project: Project) -> bool:
    return user_has_project_roles(
        user,
        project,
        [
            ProjectCollaborator.Roles.ADMIN,
            ProjectCollaborator.Roles.MANAGER,
            ProjectCollaborator.Roles.EDITOR,
            ProjectCollaborator.Roles.REPORTER,
        ],
    )


def can_read_projects(user: QfcUser, _account: QfcUser) -> bool:
    return user.is_authenticated


def can_read_public_projects(user: QfcUser) -> bool:
    return user.is_authenticated


def can_read_files(user: QfcUser, project: Project) -> bool:
    return user_has_project_roles(
        user,
        project,
        [
            ProjectCollaborator.Roles.ADMIN,
            ProjectCollaborator.Roles.MANAGER,
            ProjectCollaborator.Roles.EDITOR,
            ProjectCollaborator.Roles.REPORTER,
            ProjectCollaborator.Roles.READER,
        ],
    )


def can_delete_files(user: QfcUser, project: Project) -> bool:
    return user_has_project_roles(
        user,
        project,
        [
            ProjectCollaborator.Roles.ADMIN,
            ProjectCollaborator.Roles.MANAGER,
            ProjectCollaborator.Roles.EDITOR,
        ],
    )


def can_create_deltas(user: QfcUser, project: Project) -> bool:
    """Whether the user can store deltas in a project."""
    return user_has_project_roles(
        user,
        project,
        [
            ProjectCollaborator.Roles.ADMIN,
            ProjectCollaborator.Roles.MANAGER,
            ProjectCollaborator.Roles.EDITOR,
            ProjectCollaborator.Roles.REPORTER,
        ],
    )


def can_read_deltas(user: QfcUser, project: Project) -> bool:
    return user_has_project_roles(
        user,
        project,
        [
            ProjectCollaborator.Roles.ADMIN,
            ProjectCollaborator.Roles.MANAGER,
            ProjectCollaborator.Roles.EDITOR,
            ProjectCollaborator.Roles.REPORTER,
        ],
    )


def can_apply_deltas(user: QfcUser, project: Project) -> bool:
    return user_has_project_roles(
        user,
        project,
        [
            ProjectCollaborator.Roles.ADMIN,
            ProjectCollaborator.Roles.MANAGER,
            ProjectCollaborator.Roles.EDITOR,
            ProjectCollaborator.Roles.REPORTER,
        ],
    )


def can_create_delta(user: QfcUser, delta: Delta) -> bool:
    """Whether the user can store given delta."""
    project: Project = delta.project

    if user_has_project_roles(
        user,
        project,
        [
            ProjectCollaborator.Roles.ADMIN,
            ProjectCollaborator.Roles.MANAGER,
            ProjectCollaborator.Roles.EDITOR,
        ],
    ):
        return True

    if user_has_project_roles(user, project, [ProjectCollaborator.Roles.REPORTER]):
        if delta.method == Delta.Method.Create:
            return True

    return False


def can_retry_delta(user: QfcUser, delta: Delta) -> bool:
    if not can_apply_deltas(user, delta.project):
        return False

    if delta.status not in (
        Delta.STATUS_CONFLICT,
        Delta.STATUS_NOT_APPLIED,
        Delta.STATUS_ERROR,
    ):
        return False

    return True


def can_ignore_delta(user: QfcUser, delta: Delta) -> bool:
    if not can_apply_deltas(user, delta.project):
        return False

    if delta.status not in (
        Delta.STATUS_CONFLICT,
        Delta.STATUS_NOT_APPLIED,
        Delta.STATUS_ERROR,
    ):
        return False

    return True


def can_list_users_organizations(user: QfcUser) -> bool:
    """Return True if the `user` can list users and organizations.
    Return False otherwise."""

    return True


def can_create_organizations(user: QfcUser) -> bool:
    return user.is_authenticated


def can_update_user(user: QfcUser, account: QfcUser) -> bool:
    if user == account:
        return True

    if user_has_organization_roles(user, account, [OrganizationMember.Roles.ADMIN]):
        return True

    return False


def can_delete_user(user: QfcUser, account: QfcUser) -> bool:
    if user == account:
        return True

    if user_has_organization_roles(user, account, [OrganizationMember.Roles.ADMIN]):
        return True

    return False


def can_create_collaborators(user: QfcUser, project: Project) -> bool:
    return user_has_project_roles(
        user,
        project,
        [
            ProjectCollaborator.Roles.ADMIN,
            ProjectCollaborator.Roles.MANAGER,
        ],
    )


def can_read_collaborators(user: QfcUser, project: Project) -> bool:
    return user_has_project_roles(
        user,
        project,
        [
            ProjectCollaborator.Roles.ADMIN,
            ProjectCollaborator.Roles.MANAGER,
        ],
    )


def can_update_collaborators(user: QfcUser, project: Project) -> bool:
    return user_has_project_roles(
        user,
        project,
        [
            ProjectCollaborator.Roles.ADMIN,
            ProjectCollaborator.Roles.MANAGER,
        ],
    )


def can_delete_collaborators(user: QfcUser, project: Project) -> bool:
    return user_has_project_roles(
        user,
        project,
        [
            ProjectCollaborator.Roles.ADMIN,
            ProjectCollaborator.Roles.MANAGER,
        ],
    )


def can_read_exportations(user: QfcUser, project: Project) -> bool:
    return user_has_project_roles(
        user,
        project,
        [
            ProjectCollaborator.Roles.ADMIN,
            ProjectCollaborator.Roles.MANAGER,
            ProjectCollaborator.Roles.EDITOR,
            ProjectCollaborator.Roles.REPORTER,
            ProjectCollaborator.Roles.READER,
        ],
    )


def can_create_members(user: QfcUser, organization: Organization) -> bool:
    """Return True if the `user` can create members (incl. teams) of `organization`.
    Return False otherwise."""

    return user_has_organization_roles(
        user, organization, [OrganizationMember.Roles.ADMIN]
    )


def can_read_members(user: QfcUser, organization: Organization) -> bool:
    """Return True if the `user` can list members (incl. teams) of `organization`.
    Return False otherwise."""

    return True


def can_update_members(user: QfcUser, organization: Organization) -> bool:
    return user_has_organization_roles(
        user, organization, [OrganizationMember.Roles.ADMIN]
    )


def can_delete_members(user: QfcUser, organization: Organization) -> bool:
    return user_has_organization_roles(
        user, organization, [OrganizationMember.Roles.ADMIN]
    )


def can_become_collaborator(user: QfcUser, project: Project) -> bool:
    return not user_has_project_roles(
        user,
        project,
        [
            ProjectCollaborator.Roles.ADMIN,
            ProjectCollaborator.Roles.MANAGER,
            ProjectCollaborator.Roles.EDITOR,
            ProjectCollaborator.Roles.REPORTER,
            ProjectCollaborator.Roles.READER,
        ],
    )


def can_read_geodb(user: QfcUser, profile: QfcUser) -> bool:
    if not profile.useraccount.is_geodb_enabled:
        return False

    if can_update_user(user, profile):
        return True

    return False


def can_create_geodb(user: QfcUser, profile: QfcUser) -> bool:
    if not profile.useraccount.is_geodb_enabled:
        return False

    if profile.has_geodb:
        return False

    if can_update_user(user, profile):
        return True

    return False


def can_delete_geodb(user: QfcUser, profile: QfcUser) -> bool:
    if not profile.useraccount.is_geodb_enabled:
        return False

    if not profile.has_geodb:
        return False

    if can_update_user(user, profile):
        return True

    return False


def can_become_member(user: QfcUser, organization: Organization) -> bool:
    return not user_has_organization_roles(
        user,
        organization,
        [OrganizationMember.Roles.ADMIN, OrganizationMember.Roles.MEMBER],
    )


def can_send_invitations(user: QfcUser, account: QfcUser) -> bool:
    if account.is_user:
        return True

    return False
