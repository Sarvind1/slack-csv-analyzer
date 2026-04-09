# OTIF_Pull.csv - Column References

## 📊 Column Names Reference

**Format: column_name | description | synonymous_names**

- `document number` | Purchase order identifier (each PO can have multiple lines - group by this to get unique PO totals) | PO, PO number, purchase order, order number
- `per unit amount` | Unit price/cost per item | unit price, price per unit, item price, price, unit cost
- `pending value` | Monetary value of outstanding units | outstanding value, remaining value, pending cost
- `prd` | Production Ready Date (current/final) | PRD, production date, ready date
- `first prd` | Initial Production Ready Date | first PRD, initial PRD, original PRD
- `planned prd` | Originally planned Production Ready Date | planned PRD, planned production date
- `name` | Supplier/vendor company name | supplier, vendor, vendor name, company
- `item` | Product SKU/identifier | SKU, product code, razin, product ID
- `asin number` | Amazon Standard Identification Number | ASIN, amazon ID, product ASIN
- `quantity` | Total ordered quantity | qty, amount ordered, order quantity
- `quantity fulfilled/received` | Delivered quantity | received, fulfilled, delivered quantity
- `pending units` | Outstanding quantity | pending, outstanding, remaining quantity
- `final status` | Overall order status | status, order status, current state
- `current status` | Real-time operational status | operational status, workflow status
- `date created` | Order creation date | creation date, order date, PO date
- `batch_id` | Shipment batch identifier | batch, batch number, batch code, shipment batch, consolidation ID
- `confirmed crd` | Confirmed Cargo Ready Date | CRD, cargo date, ready date
- `quality control date` | QC inspection date | QC date, inspection date, quality date
- `estimated otif delivery date` | Expected delivery for OTIF | delivery date, OTIF date, expected delivery
- `cm` | Category Manager name | category manager, CM name
- `sm` | Supply Manager name | supply manager, SM name
- `final poc` | Point of Contact person (full name format like "Rita Wu", "Jeremy Lin") | POC, contact person, responsible person
- `team` | Responsible team | assigned team, managing team
- `days bucket` | Processing time range in format "XX-XX" (e.g., "01-03", "04-08", "09-15") | processing days, time bucket, day range
- `line payment status` | Payment status for line item | payment status, paid status
- `invoice number` | Invoice reference number | invoice ID, invoice ref