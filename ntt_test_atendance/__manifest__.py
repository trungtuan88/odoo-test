{
    'name': "NTT Test Attendance",
    'summary': """
    """,
    'support': '',
    'category': 'Human Resources',
    'version': '1.0.0',

    'description': """
    """,

    'depends': ['hr_attendance'],

    'data': [
        'security/module_security.xml',
        'security/ir.model.access.csv',
        # Data
        'data/attendance_status_data.xml',
        'data/cron_attendance.xml',
        # Demo Data
        'demo/demo_device_location.xml',
        'demo/demo_attendance_device.xml',
        'demo/demo_user_on_device.xml',
        'demo/demo_user_bio_template.xml',
        # Views
        'views/attendance_device_views.xml',
        'views/device_location_view.xml',
        'views/device_trans_time_views.xml',
        'views/device_command_views.xml',
        'views/user_on_device_views.xml',
        'views/user_attendance_line_views.xml',
        'views/attendance_status_template_views.xml',
        'views/user_bio_template_views.xml',
        'views/user_finger_template_views.xml',
        'views/hr_employee_views.xml',
        'views/hr_attendance_views.xml',
        'wizard/attendance_download_wizard_views.xml',
        'wizard/upload_employee_wizard_views.xml',
    ],
    'assets': {
        'web.assets_backend': [
            'ntt_atendance_device_zkteco/static/src/components/**/*.js',
        ],
    },
    'images': [],
    'installable': True,
    'price': 0.0,
    'currency': 'EUR',
    'license': 'OPL-1',
}
