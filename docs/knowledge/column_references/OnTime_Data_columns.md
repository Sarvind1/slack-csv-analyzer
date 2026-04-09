# OnTime_Data.csv - Column References

## 📊 Column Names Reference

**Format: column_name | description | synonymous_names**

- `po_number` | Purchase order identifier | PO, PO number, purchase order, order number
- `po_value` | Total PO value (DUPLICATED across all lines of same PO - use groupby to get unique PO values) | PO value, purchase order value, total order value
- `po_line_value` | Individual line item value (quantity × unit price) | line value, PO line value, line item value
- `item_price_eur` | Unit price in Euros | unit price, price per unit, item price, price
- `final_prd_date` | Final Production Ready Date | PRD, production date, ready date, final PRD
- `first_prd_date` | Initial Production Ready Date | first PRD, initial PRD, original PRD
- `planned_prd` | Originally planned Production Ready Date | planned PRD, planned production date
- `vendor_name` | Supplier/vendor company name | supplier, vendor, vendor name, company
- `razin` | Product SKU/identifier | SKU, product code, item, product ID
- `asin` | Amazon Standard Identification Number | ASIN, amazon ID, product ASIN
- `total_quantity` | Total ordered quantity | qty, amount ordered, order quantity
- `quantity_fulfilled/received` | Delivered quantity | received, fulfilled, delivered quantity
- `final_status` | Overall order status | status, order status, current state
- `marketplace` | Target market region | market, region, marketplace region
- `batch_id` | Shipment batch identifier | batch, batch number, batch code, shipment batch, consolidation ID
- `po_created_date` | Order creation date | creation date, order date, PO date
- `po_approval_date` | Order approval date | approval date, approved date
- `supplier_confirmation_date` | Supplier po confirmation or acceptance date | confirmation date, accepted date, supplier confirmation for POs
- `po_sm_date_value` | Supply Manager DATE (not name) | SM date, supply manager date
- `sm_signoff_ts` | Supply Manager sign-off TIMESTAMP (not name) | SM signoff, supply manager signoff
- `po_im_date_value` | Import Manager DATE (not name) | IM date, import manager date
- `pi_invoice_number` | Proforma Invoice number | PI invoice, proforma invoice ID
- `ci_invoice_number` | Commercial Invoice number | CI invoice, commercial invoice ID
- `bi_invoice_number` | Bill Invoice number | BI invoice, bill invoice ID
- `pi_payment_date` | Proforma Invoice payment date | PI payment, proforma payment
- `ci_payment_date` | Commercial Invoice payment date | CI payment, commercial payment
- `bi_payment_date` | Bill Invoice payment date | BI payment, bill payment