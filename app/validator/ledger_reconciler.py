from typing import Tuple, List
from app.models.schemas import InvoiceData, ValidationAudit
from app.config import settings


class LedgerReconciler:
    @classmethod
    def audit_invoice(cls, invoice: InvoiceData) -> ValidationAudit:
        errors: List[str] = []
        flags: List[str] = []

        # 1. Check Line Items Math (Quantity * Unit Price == Total)
        calc_subtotal = 0.0
        for i, item in enumerate(invoice.line_items):
            expected_line = round(item.quantity * item.unit_price, 2)
            if abs(expected_line - item.total) > settings.math_tolerance_cents:
                errors.append(
                    f"Line {i+1} ('{item.description}'): Qty ({item.quantity}) * Price (${item.unit_price:.2f}) "
                    f"= ${expected_line:.2f}, but extracted line total is ${item.total:.2f}"
                )
            calc_subtotal += item.total

        calc_subtotal = round(calc_subtotal, 2)

        # 2. Check Subtotal vs Sum of Line Items
        if abs(calc_subtotal - invoice.financials.subtotal) > settings.math_tolerance_cents:
            errors.append(
                f"Subtotal Mismatch: Sum of line items (${calc_subtotal:.2f}) does not match stated subtotal (${invoice.financials.subtotal:.2f})"
            )

        # 3. Check Overall Total (Subtotal + Tax + Shipping == Total)
        calc_total = round(
            invoice.financials.subtotal + invoice.financials.tax_amount + invoice.financials.shipping_amount,
            2
        )
        discrepancy = round(abs(calc_total - invoice.financials.total_amount), 2)
        if discrepancy > settings.math_tolerance_cents:
            errors.append(
                f"Total Mismatch: Subtotal (${invoice.financials.subtotal:.2f}) + Tax (${invoice.financials.tax_amount:.2f}) "
                f"+ Shipping (${invoice.financials.shipping_amount:.2f}) = ${calc_total:.2f}, but stated total is ${invoice.financials.total_amount:.2f}"
            )

        # 4. Compliance & Tax ID Validation
        if not invoice.vendor.tax_id or invoice.vendor.tax_id.lower() in ("none", "null", "unknown"):
            flags.append("Vendor Tax ID / VAT number is missing or unverified.")

        if not invoice.due_date:
            flags.append("Due date is not specified; default net-30 terms assumed.")

        # Determine Confidence and Review Status
        is_math_valid = len(errors) == 0
        base_confidence = 0.96 if is_math_valid else 0.72
        if flags:
            base_confidence -= (0.05 * len(flags))
        confidence = round(max(min(base_confidence, 0.99), 0.50), 2)

        if is_math_valid and confidence >= settings.auto_approve_confidence_threshold:
            status = "AUTO_APPROVED"
        elif not is_math_valid:
            status = "NEEDS_HUMAN_REVIEW"
        else:
            status = "NEEDS_HUMAN_REVIEW"

        return ValidationAudit(
            is_mathematically_valid=is_math_valid,
            calculated_subtotal=calc_subtotal,
            calculated_total=calc_total,
            discrepancy_amount=discrepancy,
            validation_errors=errors,
            compliance_flags=flags,
            confidence_score=confidence,
            review_status=status
        )

