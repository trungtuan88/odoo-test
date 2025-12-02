{
    'name': "NTT Test Attendance",
    'summary': """
    Integrate ZKTeco biometric attendance machines
    """,
    'author': "NTT",
    'support': 'apps.support@ntt.com',
    'category': 'Human Resources',
    'version': '1.0.0',

    'description': """
What it does
============
Biometric Attendance Device – Integrate ZKTeco biometric time attendance devices with Odoo HR Attendance.

Main Features
=============

#. **Flexible Connection:**
    - Connect ZKTeco attendance devices using the ADMS/iClock protocol (/iclock/ping, /iclock/getrequest, /iclock/cdata, /iclock/devicecmd, /iclock/registry).
    - Manage the list of attendance devices (attendance.device), online/offline status, last ping time, timezone, installation location, and multi-company.
    - Receive pushed data from devices:
    - ATTLOG: attendance logs.
    - OPERLOG: USER, FP, FACE, FVEIN, OPLOG...
    - BIODATA: unified biometric templates (fingerprint, face, finger vein, iris, palm...).
    - options: device configuration and capability information (PushOptions, MultiBioDataSupport, ...).

    - Store and manage raw data:
    - user.attendance.line: raw attendance logs from the device (PIN, timestamp, status, verify mode, workcode...).
    - user.on.device: users on the device, mapped to hr.employee.
    - user.finger.template, user.bio.template: fingerprint and unified biometric templates of employees.

    - Automatically synchronize to hr.attendance:
    - Collect unsynchronized attendance lines per employee.
    - Pair check-in/check-out and handle edge cases.
    - Set checkin_device_id/checkout_device_id, in_mode/out_mode = "device".
    - Keep a reverse link to the raw record (user.attendance.line).

    - Manage commands sent to devices (command.to.device):
    - Command queue: DATA QUERY ATTLOG, upload user, upload settings, delete user, etc.
    - Devices automatically fetch commands via /iclock/getrequest and return results via /iclock/devicecmd.
    - Log send time, response time, return code, and detailed error description.

    - Tight integration with hr.employee and hr.attendance:
    - From employees you can upload multiple employees to multiple devices using a device selection wizard.
    - Display the list of devices and device users for each employee.
    - Add fields to view/bind devices in hr.attendance.

    - UI and utilities:
    - "Attendance Devices" menu under HR Attendance: manage devices, raw logs, biometric data.
    - Button box on the device form: view unmapped users, unmapped employees, fingerprint/BIODATA templates, attendance data...
    - Delete confirmation dialog for user/device clearly explains that deleting in Odoo will create a delete request on the device.

Benefits
========

    - No more manual Excel import/export when retrieving attendance data.
    - All biometric data and attendance logs are centrally managed in Odoo.
    - Easy to extend, control, and debug attendance issues from a single place.
    
Editions Supported
==================
1. Community Edition
2. Enterprise Edition
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
    'price': 0,
    'currency': 'EUR',
    'license': 'OPL-1',
}
