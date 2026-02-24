from odoo import _, api, fields, models


class IrActionsReport(models.Model):
    _inherit = "ir.actions.report"

    @api.model
    def _render_playwright_pdf(self, report_ref, res_ids, data=None):
        """Generate a PDF and returns it.

        If the action configured on the report is server, it prints the
        generated document as well.
        """
        document, doc_format = super()._render_playwright_pdf(
            report_ref, res_ids=res_ids, data=data
        )
        report = self._get_report(report_ref)
        behaviour = report.behaviour()
        printer = behaviour.pop("printer", None)
        can_print_report = report._can_print_report(behaviour, printer, document)

        if can_print_report:
            printer.print_document(
                report, document, doc_format=report.report_type, **behaviour
            )

        return document, doc_format
