from odoo import models, fields


class DeviceLocation(models.Model):
    _name = 'device.location'
    _description = 'Device Location'

    name = fields.Char(
        string='Name',
        required=True,
        translate=True,
        help="The position where the device is equipped. E.g. Out Door, In Door, etc")

    hr_work_location_id = fields.Many2one(
        'hr.work.location',
        string='Work Location',
        required=True,
        help="The work location to where this device location belongs. E.g. factory, office, etc")
