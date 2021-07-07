from odoo import fields, models


class AccountInvoiceSummary(models.TransientModel):
    _name = "account.invoice.summary"
    _description = "Account Invoice Summary"

    start = fields.Date(
        required=True,
        default=fields.Date.today(),
        string="Fecha inicial",
    )
    end = fields.Date(
        required=True,
        default=fields.Date.today(),
        string="Fecha final",
    )
   
    

    account_type=fields.Selection([
        ("out_invoice","Factura de cliente"),
        ("out_refund","Rectificativa de cliente"),
        
    ], string="Tipo de factura"     
    )
  
    validate_type=fields.Boolean(
        default=False,
        string="Filtrar por tipo de factura"

    )

    def generate(self):
        report = self.env.ref("invoice_summary.invoice_summary_report")
        return report.report_action(self)

    def get_invoices(self):
        if self.validate_type:
            invoices = self.env["account.invoice"].search(
                [
                    ("type", "=", self.account_type),
                    ("date_invoice", ">=", self.start),
                    ("date_invoice", "<=", self.end),
                    ("state", "in", ("open","paid")),
                ]
            )
        else:
            invoices = self.env["account.invoice"].search(
                [
                    ("date_invoice", ">=", self.start),
                    ("date_invoice", "<=", self.end),
                    ("state", "in", ("open","paid")),
                ]
            )

        return invoices


