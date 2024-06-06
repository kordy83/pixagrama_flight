# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
from odoo.exceptions import UserError


class AccountInvoice(models.Model):
    _inherit = 'account.move'

    def write(self, vals):
        res = super(AccountInvoice, self).write(vals)
        if not self.env.user.has_group('pixagrama_flight.group_edit_invoice'):
            raise UserError(_("Sorry, you don't have privileges to edit invoice."))
        return res


class Insurance(models.Model):
    _name = "insurance.order"

    name = fields.Char("Name")
    address = fields.Char("Address")
    mobile1 = fields.Char("Mobile Number 1")
    mobile2 = fields.Char("Mobile Number 2")
    country = fields.Char("country")
    q_number = fields.Char("Voucher Number")
    q_code = fields.Char("Voucher Code")
    traveling_date = fields.Date("Traveling Date")
    arrival_date = fields.Date("Return Date")
    number_of_days = fields.Integer("Number Of Days")
    responsible_employee = fields.Char("Responsible Employee")


class ProjectTask(models.Model):
    _inherit = "project.task"

    child_group_id = fields.Many2one('child.travel.group', string='child Group',)


class ChildTravel(models.Model):
    _name = "child.travel.group"

    name = fields.Char("Name")
    coordinator = fields.Char("Coordinator")
    address = fields.Char("Address")
    mobile1 = fields.Char("Mobile Number 1")
    mobile2 = fields.Char("Mobile Number 2")
    region = fields.Char("Region")
    program_price = fields.Float("Program Price")
    sale_price = fields.Float("Sale Price")
    profit = fields.Float("Profit")
    child_ids = fields.Many2many('res.partner', 'child_travel_group_id', string='Clients')
    active = fields.Boolean(default=True)
    image = fields.Binary()
    # partner_files_ids = fields.One2many('partner.attach.file', 'partner_file_id', string='ملفات')
    task_count = fields.Integer(compute='_compute_task_count', string='# Tasks')
    total_invoiced = fields.Float(compute='_compute_total_invoiced')

    def open_partner_history2(self):
        for rec in self:
            for line in rec.child_ids:
                if line.total_invoiced > 0:
                    line.child_travel_group_id = rec.id
            return {
                'type': 'ir.actions.act_window',
                'name': 'Children',
                'res_model': 'res.partner',
                'view_type': 'form',
                'view_mode': 'tree,form',
                'domain': [('child_travel_group_id', '=', rec.id)],
                'target': 'current',
            }

    def get_related_tasks(self):
        for record in self:
            return {
                'type': 'ir.actions.act_window',
                'name': 'tasks',
                'res_model': 'project.task',
                'view_type': 'form',
                'view_mode': 'tree,form',
                'domain': [('child_group_id', '=', record.id)],
                'target': 'current',
            }

    def _compute_total_invoiced(self):
        for partner in self:
            partner.total_invoiced = sum(line.total_invoiced for line in partner.child_ids)

    def _compute_task_count(self):
        for partner in self:
            partner.task_count = self.env['project.task'].search_count([('child_group_id', '=', partner.id)])


class ResPartnerFlight(models.Model):
    _name = "res.partner.flight"

    name = fields.Char("Name")
    address = fields.Char("Address")
    mobile1 = fields.Char("Mobile Number 1")
    mobile_fly = fields.Char("Mobile Number 2")
    reservation_date_fly = fields.Date("booking date")
    travel_date_fly = fields.Date("date of Travel")
    transient_time_fly = fields.Datetime("Transit duration")
    leaving_time_fly = fields.Datetime("Departure Date")
    transient_period_fly = fields.Datetime("Transit duration in back")
    reference_number_fly = fields.Char("Return number")
    ticket_number_fly = fields.Char("Ticket Number")
    visa_name_fly = fields.Char("Last Name in Passport")
    ticket_price_fly = fields.Float("Ticket Price")
    sale_price_fly = fields.Float("Sale Price")
    profit_fly = fields.Float("Profit")
    walking_line_fly = fields.Char("Itinerary")
    country_id_fly = fields.Many2one(comodel_name="res.country", string="Transit Country")
    transient_visa_fly = fields.Char("Transit Visa")
    state_fly = fields.Selection(string="Client Type", selection=[('vip', 'Vip'), ('local', 'local'), ])
    commission_line_fly = fields.Float("Commission Line")
    weight_fly = fields.Float("Luggage weight")
    degree_fly = fields.Char("class")
    flight_type_fly = fields.Char("Flight type")
    time_difference_fly = fields.Datetime("Time Difference")


class ResPartner(models.Model):
    _inherit = "res.partner"

    child_travel_group_id = fields.Many2one('child.travel.group')
    is_child = fields.Boolean()
    is_insurance = fields.Boolean()
    is_flight = fields.Boolean()
    coordinator = fields.Char("coordinator")
    mobile2_child = fields.Char("Mobile Number 2")
    region = fields.Char("Region")
    program_price = fields.Float("Program Price")
    sale_price = fields.Float("Sale Price")
    profit = fields.Float("profit")
    #flight
    mobile_fly = fields.Char("Mobile Number 2")
    reservation_date_fly = fields.Date("booking date")
    travel_date_fly = fields.Date("Travel date")
    transient_time_fly = fields.Datetime("Transit Time")
    leaving_time_fly = fields.Datetime("Leaving Time")
    transient_period_fly = fields.Datetime("Transit duration in back")
    reference_number_fly = fields.Char("Return number")
    ticket_number_fly = fields.Char("Ticket Number")
    visa_name_fly = fields.Char("Last Name in Passport")
    ticket_price_fly = fields.Float("Ticket Price")
    sale_price_fly = fields.Float("Sale Price")
    profit_fly = fields.Float("Profit")
    walking_line_fly = fields.Char("Itinerary")
    country_id_fly = fields.Many2one(comodel_name="res.country", string="Transit Country")
    transient_visa_fly = fields.Char("Transit Visa")
    state_fly = fields.Selection(string="Client Type", selection=[('vip', 'Vip'), ('local', 'local'), ])
    commission_line_fly = fields.Float("Commission Line")

    weight_fly = fields.Char("Traveling weight")
    back_weight_fly = fields.Char("Return weight")
    going_degree = fields.Char("travel class")
    back_degree = fields.Char("return class")
    time_difference_fly2 = fields.Char("Time Difference")
    trip_time = fields.Char("Flight duration")

    degree_fly = fields.Char("Class")
    flight_type_fly = fields.Char("Flight type")
    time_difference_fly = fields.Datetime("Time Difference")

    #insurance
    mobile2_insurance = fields.Char("Mobile Number 2")
    country_insurance = fields.Char("Country")
    q_number_insurance = fields.Char("Voucher Number")
    q_code_insurance = fields.Char("Voucher Code")
    traveling_date_insurance = fields.Date("Travel date")
    arrival_date_insurance = fields.Date("Return date")
    number_of_days_insurance = fields.Integer("Number of days")
    responsible_employee_insurance = fields.Char("Responsible Employee")
    show_in_flights = fields.Boolean('Create airline tickets')
    related_flight = fields.Many2one(comodel_name="res.partner", string='airline tickets', compute='_compute_related_flight')

    @api.depends('show_in_flights')
    def _compute_related_flight(self):
        for rec in self:
            if rec.show_in_flights:
                rec.related_flight = self.env['res.partner'].search([('is_flight', '=', True),('name', '=', rec.name)],limit=1)
            else:
                rec.related_flight = False

    @api.onchange('show_in_flights')
    def onchange_show_in_flights(self):
        for rec in self:
            if rec.show_in_flights == True:
               self.env['res.partner'].create({  
                                                'name': rec.name,
                                                'is_flight': True,
                                                'is_external': False,
                                                'notify_email': rec.notify_email,
                                                'invoice_warn': rec.invoice_warn,
                                                'sale_warn': rec.sale_warn,
                                                'company_id': rec.company_id.id,
                                                })

