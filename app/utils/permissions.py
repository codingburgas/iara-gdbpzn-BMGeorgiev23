"""
Role-based permission system for the application.
"""

# Permission definitions for each role
ROLE_PERMISSIONS = {
    'admin': {
        'user_manage': True,
        'incident_create': True,
        'incident_edit': True,
        'incident_delete': True,
        'incident_resolve': True,
        'incident_view_all': True,
        'team_create': True,
        'team_edit': True,
        'team_delete': True,
        'team_view_all': True,
        'resource_manage': True,
        'operations_access': True,
        'communications_access': True,
        'reports_access': True,
        'dashboard_access': True,
    },
    'incident_manager': {
        'user_manage': False,
        'incident_create': True,
        'incident_edit': True,
        'incident_delete': False,
        'incident_resolve': True,
        'incident_view_all': True,
        'team_create': False,
        'team_edit': False,
        'team_delete': False,
        'team_view_all': True,
        'resource_manage': False,
        'operations_access': True,
        'communications_access': True,
        'reports_access': True,
        'dashboard_access': True,
    },
    'dispatcher': {
        'user_manage': False,
        'incident_create': True,
        'incident_edit': True,
        'incident_delete': False,
        'incident_resolve': False,
        'incident_view_all': True,
        'team_create': False,
        'team_edit': False,
        'team_delete': False,
        'team_view_all': True,
        'resource_manage': False,
        'operations_access': False,
        'communications_access': True,
        'reports_access': False,
        'dashboard_access': True,
    },
    'firefighter': {
        'user_manage': False,
        'incident_create': True,
        'incident_edit': False,
        'incident_delete': False,
        'incident_resolve': False,
        'incident_view_all': True,
        'team_create': False,
        'team_edit': False,
        'team_delete': False,
        'team_view_all': True,
        'resource_manage': False,
        'operations_access': False,
        'communications_access': True,
        'reports_access': False,
        'dashboard_access': True,
    },
    'user': {
        'user_manage': False,
        'incident_create': True,
        'incident_edit': False,
        'incident_delete': False,
        'incident_resolve': False,
        'incident_view_all': False,
        'team_create': False,
        'team_edit': False,
        'team_delete': False,
        'team_view_all': False,
        'resource_manage': False,
        'operations_access': False,
        'communications_access': False,
        'reports_access': False,
        'dashboard_access': False,
    }
}

# Navigation items for each role
ROLE_NAVIGATION = {
    'admin': [
        {'name': 'Потребители', 'url': 'admin.users', 'icon': 'users-cog'},
        {'name': 'Табло', 'url': 'dashboard.index', 'icon': 'chart-pie'},
        {'name': 'Произшествия', 'url': 'incidents.list_incidents', 'icon': 'fire-extinguisher'},
        {'name': 'Екипи', 'url': 'teams.list_teams', 'icon': 'users'},
        {'name': 'Операции', 'url': 'operations.live', 'icon': 'tv'},
        {'name': 'Комуникации', 'url': 'communications.chat', 'icon': 'comments'},
        {'name': 'Ресурси', 'url': 'resources.inventory', 'icon': 'boxes'},
        {'name': 'Доклади', 'url': 'reports.overview', 'icon': 'chart-bar'},
    ],
    'incident_manager': [
        {'name': 'Табло', 'url': 'dashboard.index', 'icon': 'chart-pie'},
        {'name': 'Произшествия', 'url': 'incidents.list_incidents', 'icon': 'fire-extinguisher'},
        {'name': 'Екипи', 'url': 'teams.list_teams', 'icon': 'users'},
        {'name': 'Операции', 'url': 'operations.live', 'icon': 'tv'},
        {'name': 'Комуникации', 'url': 'communications.chat', 'icon': 'comments'},
        {'name': 'Доклади', 'url': 'reports.overview', 'icon': 'chart-bar'},
    ],
    'dispatcher': [
        {'name': 'Табло', 'url': 'dashboard.index', 'icon': 'chart-pie'},
        {'name': 'Произшествия', 'url': 'incidents.list_incidents', 'icon': 'fire-extinguisher'},
        {'name': 'Екипи', 'url': 'teams.list_teams', 'icon': 'users'},
        {'name': 'Комуникации', 'url': 'communications.chat', 'icon': 'comments'},
    ],
    'firefighter': [
        {'name': 'Табло', 'url': 'dashboard.index', 'icon': 'chart-pie'},
        {'name': 'Произшествия', 'url': 'incidents.list_incidents', 'icon': 'fire-extinguisher'},
        {'name': 'Екипи', 'url': 'teams.list_teams', 'icon': 'users'},
        {'name': 'Комуникации', 'url': 'communications.chat', 'icon': 'comments'},
        {'name': 'Ресурси', 'url': 'resources.inventory', 'icon': 'boxes'},
    ],
    'user': [
        {'name': 'Начало', 'url': 'main.index', 'icon': 'home'},
        {'name': 'За нас', 'url': 'main.about', 'icon': 'info-circle'},
        {'name': 'Контакти', 'url': 'main.contact', 'icon': 'envelope'},
        {'name': 'Докладвай', 'url': 'main.report', 'icon': 'exclamation-triangle'},
        {'name': 'Моите доклади', 'url': 'main.my_reports', 'icon': 'list'},
    ]
}


def has_permission(user, permission):
    """Check if a user has a specific permission."""
    if user is None or not user.is_authenticated:
        return False
    return ROLE_PERMISSIONS.get(user.role, {}).get(permission, False)


def get_navigation(user):
    """Get the navigation items for a user based on their role."""
    if user is None or not user.is_authenticated:
        # Public navigation
        return [
            {'name': 'Начало', 'url': 'main.index', 'icon': 'home'},
            {'name': 'За нас', 'url': 'main.about', 'icon': 'info-circle'},
            {'name': 'Контакти', 'url': 'main.contact', 'icon': 'envelope'},
            {'name': 'Вход', 'url': 'auth.login', 'icon': 'sign-in-alt'},
        ]
    return ROLE_NAVIGATION.get(user.role, ROLE_NAVIGATION['user'])


def get_available_roles():
    """Get all available roles for selection (admin only)."""
    return [
        {'value': 'admin', 'label': 'Администратор'},
        {'value': 'incident_manager', 'label': 'Мениджър произшествия'},
        {'value': 'dispatcher', 'label': 'Диспечер'},
        {'value': 'firefighter', 'label': 'Пожарникар'},
        {'value': 'user', 'label': 'Потребител'},
    ]