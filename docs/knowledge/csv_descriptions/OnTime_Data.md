# OnTime_Data.csv

## Auto-Generated Overview
- **File**: OnTime_Data.csv
- **Columns**: po_razin_id, po_razin_line_unique_key, po_number, po_line_unique_key, razin, asin, marketplace, go_forward_flag, batch_id, shipment_number, item_receipt_number, acquisition_source, marketplace_header, vendor_name, final_status, total_quantity, is_zero_quantity_po_line, item_price_eur, scm_link_to_po, po_created_date, po_approval_date, po_negotiation_date, supplier_confirmation_status, supplier_confirmation_date, po_line_value, po_value, scm_po_scm_memo, po_batch, qi_flag, historical_anti_po, first_prd_date, prd_reconfirmation, prd_status, accepted_prd, planned_prd, final_prd_date, qi_date, po_open_closed, compliance, line_id, receive_final_prd_date, qc_schedule_date, prd_reconfirmed_date, receive_first_prd_date, ffw_booking_ts, spd_ts, batch_spd, stock_pickup_date, batch_telex_date, ffwp_telex_release_date, supplier_telex_release_date, telex_release_date, packaging_file_date, po_im_date_value, po_sm_date_value, pi_invoice_number, pi_submission_ts, pi_invoice_create_date_ns, pi_invoice_approval_date, pi_payment_date, compliance_flag_ns, anti_po_flag, supplier_payment_terms, pi_value, ci_value, bl_value, pi_flag, ci_flag, bi_flag, ir_quantity_on_order, ir_quantity_received, item_receipt_date, item_receipt_date_70_perc, compliance_testing_date, batch_created_ts, sm_signoff_ts, leadtime_production_days, scm_link_to_inbship, shipment_creation_date, cargo_ready_date, actual_cargo_pick_up_date, actual_shipping_date, actual_arrival_date, actual_delivery_date, receiving_location, quantity_expected, po_line_quantity_expected, shipment_ratio, po_line_value_shipment_ratio, inbship_open_closed, shipment_telex_release_date, gate_in, gate_out, customs_clearance, customs_clearance_date, shipment_in_transit_date, shipment_stock_delivery_date, shipment_inb_receiving_date, ci_invoice_number, ci_submission_ts, ci_invoice_create_date_ns, ci_invoice_approval_date, ci_payment_date, bi_invoice_number, bi_invoice_create_date_ns, bi_invoice_approval_date, bi_payment_date, absolute_value_of_quantity, quantity, quantity_fulfilled/received
- **Last Modified**: 2025-09-19T06:07:00.230377


## Column Information with Business Meanings

### 🆔 **Core Identifiers**
- **po_razin_id**: Combined Purchase Order + Product ID (e.g., "PO361424YUMA-0000102")
- **po_razin_line_unique_key**: Unique line item identifier combining PO and product
- **po_number**: Purchase Order number (e.g., "PO361424")
- **po_line_unique_key**: Numeric line item ID within the PO
- **razin**: Internal product SKU code (e.g., "YUMA-000010")
- **asin**: Amazon Standard Identification Number for products
- **line_id**: Sequential line number within the purchase order

### 🏢 **Vendor & Supplier Information**
- **vendor_name**: SUPPLIER/VENDOR COMPANY NAME (e.g., "73905 LAMRON INTERNATIONAL")
- **supplier_confirmation_status**: Vendor acceptance status (Confirmed, Pending, etc.)
- **supplier_confirmation_date**: Date when supplier confirmed the order
- **supplier_payment_terms**: Payment structure (e.g., "30% PI 0d 70% CI 0d")

### 🌍 **Market & Acquisition**
- **marketplace**: Target market region (Pan-EU, US, etc.)
- **marketplace_header**: Market region header identifier
- **acquisition_source**: How/where the order was sourced
- **go_forward_flag**: Whether order continues in process (0.0=No, 1.0=Yes)

### 📦 **Product & Quantity Fields**
- **total_quantity**: Original purchase order quantity
- **quantity**: Order quantity (same as total_quantity)
- **quantity_expected**: Expected delivery quantity for shipment
- **po_line_quantity_expected**: Expected quantity at PO line level
- **quantity_fulfilled/received**: Actually received/delivered quantity
- **ir_quantity_on_order**: Item receipt - quantity on order
- **ir_quantity_received**: Item receipt - quantity actually received
- **absolute_value_of_quantity**: Absolute value of quantity (for calculations)
- **is_zero_quantity_po_line**: Flag for zero-quantity lines (0=Normal, 1=Zero)

### 💰 **Financial Fields**
- **item_price_eur**: Unit price in Euros
- **po_line_value**: Total value of this purchase order line
- **po_value**: Total value of entire purchase order
- **pi_value**: Proforma Invoice payment percentage (0-100)
- **ci_value**: Commercial Invoice payment percentage (0-100)
- **bl_value**: Bill of Lading payment percentage (0-100)
- **shipment_ratio**: Shipment quantity ratio (usually 1)
- **po_line_value_shipment_ratio**: Value ratio for this shipment

⚠️ **IMPORTANT - PO Value Calculation:**
- `po_value` is **duplicated across all line items** of the same purchase order
- Each PO can have multiple lines (razins/SKUs), but the PO value remains the same for all lines
- **To calculate total unique PO value**: Group by `po_number` first, then sum
- **Incorrect**: `df['po_value'].sum()` - This counts each PO multiple times
- **Correct**: `df.groupby('po_number')['po_value'].first().sum()` - This counts each PO once
- Example: PO361424 has 2 lines with po_value=6173.35 each, but the actual PO value is only 6173.35 (not 12346.70)

### 📅 **Purchase Order Dates**
- **po_created_date**: When the PO was initially created
- **po_approval_date**: When the PO was internally approved
- **po_negotiation_date**: Date of price/terms negotiation
- **po_open_closed**: PO status (open_po, closed_po)

### 📅 **Production Ready Dates (PRD)**
- **first_prd_date**: Initial promised ready date from supplier
- **planned_prd**: Originally planned production ready date
- **accepted_prd**: PRD that was accepted/agreed upon
- **final_prd_date**: Final confirmed production ready date
- **prd_reconfirmation**: Whether PRD was reconfirmed (Yes/No)
- **prd_status**: Current status of PRD (Pending SM, etc.)
- **prd_reconfirmed_date**: Date when PRD was reconfirmed
- **receive_first_prd_date**: First received PRD date
- **receive_final_prd_date**: Final received PRD date

### 🚢 **Shipping & Logistics**
- **batch_id**: Shipping batch identifier (e.g., "BATCH0010542")
- **shipment_number**: Shipment tracking ID (e.g., "INBSHIP14524")
- **shipment_creation_date**: When shipment record was created
- **cargo_ready_date**: Date goods were ready for pickup
- **actual_cargo_pick_up_date**: Actual pickup date from supplier
- **actual_shipping_date**: Date goods departed origin
- **actual_arrival_date**: Date goods arrived at destination port/hub
- **actual_delivery_date**: Final delivery date to warehouse
- **receiving_location**: Destination warehouse/3PL facility
- **inbship_open_closed**: Inbound shipment status
- **leadtime_production_days**: Production lead time in days

### 🚚 **Transportation & Customs**
- **stock_pickup_date**: Date for stock collection
- **gate_in**: Gate entry timestamp
- **gate_out**: Gate exit timestamp
- **customs_clearance**: Customs clearance value/status
- **customs_clearance_date**: Date customs was cleared
- **shipment_in_transit_date**: In-transit date
- **shipment_stock_delivery_date**: Stock delivery date
- **shipment_inb_receiving_date**: Inbound receiving date

### 📋 **Quality & Compliance**
- **qi_flag**: Quality Inspection flag (Y/N/Other/Failed)
- **qi_date**: Quality inspection date
- **qc_schedule_date**: Quality control scheduled date
- **compliance**: Regulatory compliance status
- **compliance_flag_ns**: Compliance flag (NetSuite)
- **compliance_testing_date**: Date of compliance testing
- **anti_po_flag**: Anti-PO flag (special handling indicator)
- **historical_anti_po**: Historical anti-PO status

### 📄 **Invoice & Payment Fields**
- **pi_invoice_number**: Proforma Invoice number (e.g., "AI-PO361424")
- **pi_submission_ts**: Proforma invoice submission timestamp
- **pi_invoice_create_date_ns**: PI creation date (NetSuite)
- **pi_invoice_approval_date**: PI approval date
- **pi_payment_date**: Proforma invoice payment date
- **pi_flag**: Proforma invoice flag (Y/N)

- **ci_invoice_number**: Commercial Invoice number (e.g., "CI-PO361424")
- **ci_submission_ts**: Commercial invoice submission timestamp
- **ci_invoice_create_date_ns**: CI creation date (NetSuite)
- **ci_invoice_approval_date**: CI approval date
- **ci_payment_date**: Commercial invoice payment date
- **ci_flag**: Commercial invoice flag (Y/N)

- **bi_invoice_number**: Bill of Lading invoice number
- **bi_invoice_create_date_ns**: BL creation date (NetSuite)
- **bi_invoice_approval_date**: BL approval date
- **bi_payment_date**: BL payment date
- **bi_flag**: Bill of lading flag (Y/N)

### 📨 **Communication & Documentation**
- **batch_telex_date**: Batch telex communication date
- **ffwp_telex_release_date**: Freight forwarder telex release date
- **supplier_telex_release_date**: Supplier telex release date
- **telex_release_date**: General telex release date
- **shipment_telex_release_date**: Shipment telex release date
- **packaging_file_date**: Packaging file submission date

### ⏰ **Process Timestamps**
- **ffw_booking_ts**: Freight forwarder booking timestamp
- **spd_ts**: SPD (Supplier Planned Delivery) timestamp
- **batch_spd**: Batch SPD date
- **batch_created_ts**: When the batch was created
- **sm_signoff_ts**: Supply Manager sign-off timestamp (NOT manager name)
- **item_receipt_date**: Item receipt processed date
- **item_receipt_date_70_perc**: 70% of items received date

### 📋 **Status & Process Fields**
- **final_status**: Overall order status (Partially Received, Fully Received, etc.)
- **po_batch**: PO batch classification (Q3_Batch_1_Automated_PO_2024, etc.)
- **scm_po_scm_memo**: Supply chain memo for the PO
- **item_receipt_number**: Item receipt tracking number

### 🔗 **System Links**
- **scm_link_to_po**: URL link to PO in SCM system
- **scm_link_to_inbship**: URL link to inbound shipment

### ⚠️ **Important Notes About "SM" Fields**
- **po_sm_date_value**: Purchase Order Supply Manager DATE (this is a DATE field, NOT the manager's name)
- **sm_signoff_ts**: Supply Manager sign-off TIMESTAMP (this is a TIMESTAMP, NOT the manager's name)

⚠️ **CRITICAL**: This dataset does NOT contain Supply Manager NAMES or any person names - only dates/timestamps related to SM processes. If you need to find "who is the SM", this data cannot answer that question.

## Data Ranges
- **po_line_unique_key**: 129538775.0 to 326272879.0 (avg: 306805891.37)
- **go_forward_flag**: 0.0 to 1.0 (avg: 0.87)
- **total_quantity**: 1.0 to 990000.0 (avg: 1060.78)
- **is_zero_quantity_po_line**: 0.0 to 0.0 (avg: 0.00)
- **item_price_eur**: 0.0304823 to 93.45 (avg: 7.35)
- **po_line_value**: 2.65 to 180931.5 (avg: 3078.91)
- **po_value**: 25.526592 to 581534.1 (avg: 25781.47)
- **line_id**: 1.0 to 3414.0 (avg: 9.83)
- **pi_value**: 0.0 to 100.0 (avg: 16.00)
- **ci_value**: 0.0 to 100.0 (avg: 15.75)
- **bl_value**: 0.0 to 100.0 (avg: 68.25)
- **ir_quantity_on_order**: 200.0 to 15120.0 (avg: 1943.31)
- **ir_quantity_received**: 136.0 to 14909.0 (avg: 1714.21)
- **leadtime_production_days**: 10.0 to 180.0 (avg: 50.01)
- **quantity_expected**: 8.0 to 55500.0 (avg: 964.82)
- **po_line_quantity_expected**: 8.0 to 55500.0 (avg: 964.82)
- **shipment_ratio**: 1.0 to 1.0 (avg: 1.00)
- **po_line_value_shipment_ratio**: 2.65 to 180931.5 (avg: 3078.91)
- **customs_clearance**: nan to nan (avg: nan)
- **absolute_value_of_quantity**: 8.0 to 55500.0 (avg: 921.10)
- **quantity**: 1.0 to 990000.0 (avg: 1060.78)
- **quantity_fulfilled/received**: 0.0 to 14909.0 (avg: 15.88)

## Sample Data
| po_razin_id | po_razin_line_unique_key | po_number | po_line_unique_key | razin | asin | marketplace | go_forward_flag | batch_id | shipment_number | item_receipt_number | acquisition_source | marketplace_header | vendor_name | final_status | total_quantity | is_zero_quantity_po_line | item_price_eur | scm_link_to_po | po_created_date | po_approval_date | po_negotiation_date | supplier_confirmation_status | supplier_confirmation_date | po_line_value | po_value | scm_po_scm_memo | po_batch | qi_flag | historical_anti_po | first_prd_date | prd_reconfirmation | prd_status | accepted_prd | planned_prd | final_prd_date | qi_date | po_open_closed | compliance | line_id | receive_final_prd_date | qc_schedule_date | prd_reconfirmed_date | receive_first_prd_date | ffw_booking_ts | spd_ts | batch_spd | stock_pickup_date | batch_telex_date | ffwp_telex_release_date | supplier_telex_release_date | telex_release_date | packaging_file_date | po_im_date_value | po_sm_date_value | pi_invoice_number | pi_submission_ts | pi_invoice_create_date_ns | pi_invoice_approval_date | pi_payment_date | compliance_flag_ns | anti_po_flag | supplier_payment_terms | pi_value | ci_value | bl_value | pi_flag | ci_flag | bi_flag | ir_quantity_on_order | ir_quantity_received | item_receipt_date | item_receipt_date_70_perc | compliance_testing_date | batch_created_ts | sm_signoff_ts | leadtime_production_days | scm_link_to_inbship | shipment_creation_date | cargo_ready_date | actual_cargo_pick_up_date | actual_shipping_date | actual_arrival_date | actual_delivery_date | receiving_location | quantity_expected | po_line_quantity_expected | shipment_ratio | po_line_value_shipment_ratio | inbship_open_closed | shipment_telex_release_date | gate_in | gate_out | customs_clearance | customs_clearance_date | shipment_in_transit_date | shipment_stock_delivery_date | shipment_inb_receiving_date | ci_invoice_number | ci_submission_ts | ci_invoice_create_date_ns | ci_invoice_approval_date | ci_payment_date | bi_invoice_number | bi_invoice_create_date_ns | bi_invoice_approval_date | bi_payment_date | absolute_value_of_quantity | quantity | quantity_fulfilled/received |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| PO361424YUMA-0000102 | PO361424YUMA-000010157826946 | PO361424 | 157826946 | YUMA-000010 | B088RHJNSV | Pan-EU | 0.0 | nan | nan | nan | Stryze | Pan-EU | 73905 LAMRON INTERNATIONAL | Partially Received | 1595 | 0 | 1.92261904 | https://6979138.app.netsuite.com/app/accounting/transactions/purchord.nl?id=34336593 | 08/03/24 | 14/04/24 | 08/04/24 | Confirmed | 19/04/24 | 3066.577369 | 6173.354946 | Q3_Batch_1_Automated_PO_2024 | Other | N | Yes | 30/07/24 | No | nan | nan | 24/04/24 | 30/07/24 | nan | open_po | nan | 2 | 14/06/24 | nan | nan | 27/06/24 | nan | nan | nan | nan | nan | nan | nan | nan | 27/06/24 | 01/08/24 | 06/08/24 | PI-361424 | 29/04/24 | 27/05/24 | 27/05/24 | 31/05/24 | nan | Yes | 30% PI 0d 70% CI 0d 0% BL 0d | 30 | 70 | 0 | Y | Y | N | nan | nan | nan | nan | 26/04/24 | nan | nan | 60.0 | nan | nan | 01/01/29 | nan | nan | nan | nan | nan | nan | nan | 1 | 3066.577369 | nan | nan | nan | nan | nan | nan | nan | nan | nan | CI-361424 | nan | 10/09/24 | 10/09/24 | 14/02/25 | nan | nan | nan | nan | 1595.0 | 1595 | 0 |
| PO362782WOND-0001582 | PO362782WOND-000158161543224 | PO362782 | 161543224 | WOND-000158 | nan | US | nan | BATCH0010542 | INBSHIP14524 | nan | nan | US | 70507 SHANGHAI XIYUAN IMP. & EXP. CO.,LTD | Partially Received | 240 | 0 | 6.81 | https://6979138.app.netsuite.com/app/accounting/transactions/purchord.nl?id=35021929 | 08/04/24 | 16/04/24 | 08/04/24 | Confirmed | 04/05/24 | 1634.4 | 7311.2 | nan | Other | N | Yes | 08/10/24 | Yes | Pending SM | nan | 23/10/23 | 27/05/25 | 06/11/24 | open_po | nan | 2 | 27/05/25 | 04/11/24 | 27/05/25 | 27/06/24 | 21/08/25 | 22/08/25 | 23/08/25 | 25/08/25 | 09/09/25 | 09/09/25 | 09/09/25 | 09/09/25 | 27/06/24 | 14/08/25 | 20/08/25 | AI-PO362782 | nan | 06/05/24 | 06/05/24 | 31/05/24 | nan | No | 15% PI 0d 0% CI 0d 85% BL 0d | 15 | 0 | 85 | Y | N | Y | nan | nan | nan | 18/12/24 | 11/05/24 | 20/08/25 | 21/08/25 | nan | https://6979138.app.netsuite.com/app/accounting/transactions/shipping/inboundshipment/inboundshipment.nl?id=14637 | 27/08/25 | 15/08/25 | 25/08/25 | 30/08/25 | 13/09/25 | nan | 3PL_USCO_AVAIL_RGA Wonder Products LLC | 240.0 | 240.0 | 1 | 1634.4 | open_inbship | 09/09/25 | 27/08/25 | 16/09/25 | nan | 08/09/25 | 02/09/25 | nan | nan | nan | nan | nan | nan | nan | CI-PO362782-2 | 26/08/25 | 26/08/25 | 09/09/25 | 240.0 | 240 | 0 |
| PO365584BAHI-0000432 | PO365584BAHI-000043165860740 | PO365584 | 165860740 | BAHI-000043 | B075VDTJ6Z | Pan-EU | 0.0 | nan | nan | nan | Stryze | Pan-EU | 73773 DANYANG CHENXUAN GARMENTS CO.,LTD | Partially Received | 480 | 0 | 5.09605878 | https://6979138.app.netsuite.com/app/accounting/transactions/purchord.nl?id=35957888 | 15/05/24 | 03/06/24 | 31/05/24 | Confirmed | 04/06/24 | 2446.108214 | 9597.268517 | Q4_2024_April | Other | N | Yes | 16/08/24 | No | Pending SM | nan | 26/06/24 | 16/08/24 | nan | open_po | nan | 2 | nan | nan | nan | 12/07/24 | nan | nan | nan | nan | nan | nan | nan | nan | 12/07/24 | 13/09/24 | 13/09/24 | AI-PO365584 | 19/08/24 | 06/06/24 | 06/06/24 | 05/07/24 | To Be Tested | Yes | 30% PI 0d 70% CI 7d 0% BL 0d | 30 | 70 | 0 | Y | Y | N | nan | nan | nan | nan | 11/06/24 | nan | nan | 35.0 | nan | nan | 01/01/29 | nan | nan | nan | nan | nan | nan | nan | 1 | 2446.108214 | nan | nan | nan | nan | nan | nan | nan | nan | nan | CI-PO365584 | nan | 22/08/24 | 22/08/24 | 05/11/24 | nan | nan | nan | nan | 480.0 | 480 | 0 |


### File Information
- **Dataset Name**: `OnTime_Data.csv`
- **Total Fields**: 109 columns
- **Data Type**: Wide-format CSV with mixed lifecycle stages

### What This Dataset Contains
This is a consolidated supply chain tracking dataset that combines multiple business processes into a single table. Each row can represent different stages of the procurement lifecycle - from purchase order creation through delivery and payment. Think of it as a "master view" where not all columns are relevant for every row.

## 🎯 Quick Start: Loading the Data

### Python/Pandas Example
```python
import pandas as pd
import numpy as np

# Data is already loaded as 'df' variable
# Parse important date columns for analysis
date_cols = ['po_created_date', 'po_approval_date', 'actual_delivery_date', 'actual_shipping_date']
for col in date_cols:
    if col in df.columns:
        df[col] = pd.to_datetime(df[col], errors='coerce')

# Quick data inspection
print(f"Dataset shape: {df.shape}")
print(f"Memory usage: {df.memory_usage(deep=True).sum() / 1024**2:.2f} MB")
print(f"Null percentage: {(df.isnull().sum().sum() / (df.shape[0] * df.shape[1]) * 100):.1f}%")

# View first few rows
df.head()
```

## 🔍 Understanding the Data Structure

### Why So Many NULL Values?
This dataset has approximately **60-70% NULL values** because it combines different lifecycle stages:
- **PO Creation Records**: Have PO fields filled but shipment fields empty
- **Shipment Records**: Have logistics fields filled but may lack invoice data
- **Invoice Records**: Have financial fields filled but may lack shipment details

### Key Identifier Hierarchy
```
Purchase Order (PO) Level
    ├── po_number (e.g., "PO361424")
    └── po_razin_id (e.g., "PO361424YUMA-0000102")
        └── PO Line Level
            ├── po_line_unique_key (numeric ID)
            └── po_razin_line_unique_key (composite ID)
                └── Shipment Level
                    ├── shipment_number (e.g., "INBSHIP14524")
                    └── batch_id (e.g., "BATCH0010542")
```

## 📊 Core Data Dimensions

### 1. Vendor/Supplier Information
```python
# Example: Analyze vendor distribution
vendor_analysis = df.groupby('vendor_name').agg({
    'po_number': 'nunique',  # Count unique POs
    'po_value': 'sum',        # Total spend
    'actual_delivery_date': lambda x: (x.notna()).sum()  # Delivered orders
}).rename(columns={
    'po_number': 'total_orders',
    'po_value': 'total_spend_eur',
    'actual_delivery_date': 'delivered_orders'
})
vendor_analysis['delivery_rate'] = vendor_analysis['delivered_orders'] / vendor_analysis['total_orders']
vendor_analysis.sort_values('total_spend_eur', ascending=False).head(10)
```

**Key Vendor Fields**:
- `vendor_name`: Supplier identifier (e.g., "73905 LAMRON INTERNATIONAL")
- `supplier_confirmation_status`: Order acceptance status
- `supplier_payment_terms`: Payment structure (e.g., "30% PI 0d 70% CI 0d")

### 2. Product Information
```python
# Example: Product analysis by ASIN
product_metrics = df[df['asin'].notna()].groupby('asin').agg({
    'quantity_expected': 'sum',
    'quantity_fulfilled/received': 'sum',
    'item_price_eur': 'mean',
    'marketplace': 'first'
})
product_metrics['fill_rate'] = (product_metrics['quantity_fulfilled/received'] / 
                                 product_metrics['quantity_expected'])
product_metrics[product_metrics['quantity_expected'] > 100].head()
```

**Key Product Fields**:
- `asin`: Amazon Standard Identification Number
- `razin`: Internal SKU code
- `marketplace`: Target market (Pan-EU, US, etc.)
- `item_price_eur`: Unit price in EUR

### 3. Quantity Tracking
```python
# Example: Calculate fulfillment metrics
fulfillment_df = df[df['quantity_expected'] > 0].copy()
fulfillment_df['fulfillment_rate'] = (
    fulfillment_df['quantity_fulfilled/received'] / 
    fulfillment_df['quantity_expected']
)

# Monthly fulfillment trends
fulfillment_df['month'] = pd.to_datetime(fulfillment_df['po_created_date']).dt.to_period('M')
monthly_fulfillment = fulfillment_df.groupby('month').agg({
    'fulfillment_rate': 'mean',
    'po_number': 'count'
}).rename(columns={'po_number': 'order_count'})
```

**Quantity Field Relationships**:
- `total_quantity`: Original PO quantity
- `quantity_expected`: Expected delivery quantity
- `quantity_fulfilled/received`: Actually received quantity
- `ir_quantity_on_order`: Item receipt order quantity
- `ir_quantity_received`: Item receipt received quantity

## 📅 Date Fields Guide

### Critical Date Sequences
```python
# Example: Calculate key time metrics
date_cols = ['po_created_date', 'po_approval_date', 'final_prd_date', 
             'actual_shipping_date', 'actual_delivery_date']

for col in date_cols:
    df[col] = pd.to_datetime(df[col], errors='coerce')

# Calculate cycle times
df['approval_time_days'] = (df['po_approval_date'] - df['po_created_date']).dt.days
df['lead_time_days'] = (df['actual_delivery_date'] - df['po_created_date']).dt.days
df['transit_time_days'] = (df['actual_delivery_date'] - df['actual_shipping_date']).dt.days
df['prd_accuracy_days'] = (df['actual_delivery_date'] - df['final_prd_date']).dt.days

# Summary statistics
time_metrics = df[['approval_time_days', 'lead_time_days', 
                   'transit_time_days', 'prd_accuracy_days']].describe()
```

### Date Field Categories

#### Purchase Order Dates
- `po_created_date`: PO initiation
- `po_approval_date`: Internal approval
- `po_negotiation_date`: Price negotiation
- `supplier_confirmation_date`: Vendor acceptance

#### Production & Ready Dates (PRD)
- `first_prd_date`: Initial promised ready date
- `final_prd_date`: Final confirmed ready date
- `prd_reconfirmed_date`: Updated PRD after delays
- `planned_prd`: Original planned date

#### Shipment Dates
- `cargo_ready_date`: Goods ready for pickup
- `actual_cargo_pick_up_date`: Actual collection
- `actual_shipping_date`: Departure date
- `actual_arrival_date`: Port/warehouse arrival
- `actual_delivery_date`: Final delivery

#### Invoice & Payment Dates
- `pi_submission_ts`: Proforma invoice submission
- `ci_submission_ts`: Commercial invoice submission
- `pi_payment_date`: Proforma payment
- `ci_payment_date`: Commercial payment

## 💰 Financial Fields

### Invoice Type Breakdown
```python
# Example: Analyze payment structure
payment_df = df[df['supplier_payment_terms'].notna()].copy()

# Parse payment terms (e.g., "30% PI 0d 70% CI 0d 0% BL 0d")
payment_df['pi_percentage'] = payment_df['pi_value']
payment_df['ci_percentage'] = payment_df['ci_value']
payment_df['bl_percentage'] = payment_df['bl_value']

# Calculate weighted average payment terms
avg_payment_structure = payment_df[['pi_percentage', 'ci_percentage', 'bl_percentage']].mean()
print("Average Payment Structure:")
print(f"Proforma Invoice (PI): {avg_payment_structure['pi_percentage']:.1f}%")
print(f"Commercial Invoice (CI): {avg_payment_structure['ci_percentage']:.1f}%")
print(f"Bill of Lading (BL): {avg_payment_structure['bl_percentage']:.1f}%")
```

**Financial Fields**:
- `po_line_value`: Individual line item value
- `po_value`: Total PO value
- `pi_value`, `ci_value`, `bl_value`: Payment percentages
- `item_price_eur`: Unit price

## 🚢 Shipment & Logistics Fields

### Shipment Analysis
```python
# Example: Shipment performance metrics
shipment_df = df[df['shipment_number'].notna()].copy()

# Group by receiving location
location_metrics = shipment_df.groupby('receiving_location').agg({
    'shipment_number': 'nunique',
    'transit_time_days': 'mean',
    'customs_clearance_date': lambda x: x.notna().sum()
})

# Analyze batch shipments
batch_analysis = shipment_df[shipment_df['batch_id'].notna()].groupby('batch_id').agg({
    'po_number': 'nunique',
    'quantity_expected': 'sum',
    'actual_delivery_date': 'first'
})
```

**Key Shipment Fields**:
- `shipment_number`: Unique shipment ID
- `batch_id`: Consolidated shipment batch
- `receiving_location`: Destination warehouse/3PL
- `inbship_open_closed`: Shipment status
- `customs_clearance_date`: Import clearance

## 🏷️ Status & Flag Fields

### Understanding Status Indicators
```python
# Example: Analyze order status distribution
status_analysis = pd.DataFrame({
    'PO Status': df['po_open_closed'].value_counts(),
    'Final Status': df['final_status'].value_counts(),
    'Shipment Status': df['inbship_open_closed'].value_counts()
})

# Check compliance and quality flags
quality_check = pd.DataFrame({
    'QI Flag': df['qi_flag'].value_counts(),
    'Compliance': df['compliance'].value_counts(),
    'Anti-PO Flag': df['anti_po_flag'].value_counts()
})
```

**Status Fields**:
- `final_status`: Overall order status (e.g., "Partially Received")
- `po_open_closed`: PO completion status
- `qi_flag`: Quality inspection requirement
- `compliance`: Regulatory compliance status
- `anti_po_flag`: Special handling indicator

## 🔧 Practical Analysis Examples

### 1. Supplier Performance Dashboard
```python
def supplier_scorecard(df, vendor_name):
    vendor_data = df[df['vendor_name'] == vendor_name].copy()
    
    metrics = {
        'Total POs': vendor_data['po_number'].nunique(),
        'Total Value (EUR)': vendor_data['po_value'].sum(),
        'Avg Lead Time (days)': vendor_data['lead_time_days'].mean(),
        'On-Time Delivery Rate': (vendor_data['prd_accuracy_days'] <= 0).mean(),
        'Fill Rate': (vendor_data['quantity_fulfilled/received'].sum() / 
                     vendor_data['quantity_expected'].sum()),
        'Quality Pass Rate': (vendor_data['qi_flag'] != 'Failed').mean()
    }
    
    return pd.Series(metrics)

# Apply to top vendors
top_vendors = df['vendor_name'].value_counts().head(5).index
scorecard = pd.DataFrame([supplier_scorecard(df, v) for v in top_vendors],
                         index=top_vendors)
```

### 2. Monthly Procurement Trend
```python
# Prepare monthly aggregation
df['po_month'] = pd.to_datetime(df['po_created_date']).dt.to_period('M')

monthly_metrics = df.groupby('po_month').agg({
    'po_number': 'nunique',
    'po_value': 'sum',
    'vendor_name': 'nunique',
    'lead_time_days': 'mean'
}).rename(columns={
    'po_number': 'order_count',
    'po_value': 'total_spend',
    'vendor_name': 'active_vendors',
    'lead_time_days': 'avg_lead_time'
})

monthly_metrics['avg_order_value'] = monthly_metrics['total_spend'] / monthly_metrics['order_count']
```

### 3. Delivery Performance by Marketplace
```python
marketplace_performance = df.groupby('marketplace').agg({
    'actual_delivery_date': lambda x: x.notna().sum(),
    'po_number': 'nunique',
    'lead_time_days': 'mean',
    'transit_time_days': 'mean',
    'quantity_fulfilled/received': 'sum',
    'quantity_expected': 'sum'
})

marketplace_performance['delivery_rate'] = (
    marketplace_performance['actual_delivery_date'] / 
    marketplace_performance['po_number']
)
marketplace_performance['fill_rate'] = (
    marketplace_performance['quantity_fulfilled/received'] / 
    marketplace_performance['quantity_expected']
)
```

## ⚠️ Data Quality Considerations

### Handling Missing Values
```python
# Identify columns by null percentage
null_summary = pd.DataFrame({
    'null_count': df.isnull().sum(),
    'null_percentage': (df.isnull().sum() / len(df) * 100).round(2)
}).sort_values('null_percentage', ascending=False)

# Columns with >80% nulls (likely stage-specific)
high_null_cols = null_summary[null_summary['null_percentage'] > 80].index.tolist()
print(f"Columns with >80% nulls: {len(high_null_cols)}")

# Filter for specific analysis stages
po_analysis_df = df[df['po_number'].notna()]  # PO-level analysis
shipment_df = df[df['shipment_number'].notna()]  # Shipment analysis
invoice_df = df[df['pi_invoice_number'].notna() | df['ci_invoice_number'].notna()]  # Invoice analysis
```

### Data Validation Checks
```python
# Temporal sequence validation
def validate_date_sequence(row):
    checks = []
    
    # Check PO dates
    if pd.notna(row['po_created_date']) and pd.notna(row['po_approval_date']):
        checks.append(row['po_created_date'] <= row['po_approval_date'])
    
    # Check shipment dates
    if pd.notna(row['actual_shipping_date']) and pd.notna(row['actual_delivery_date']):
        checks.append(row['actual_shipping_date'] <= row['actual_delivery_date'])
    
    return all(checks) if checks else None

df['date_sequence_valid'] = df.apply(validate_date_sequence, axis=1)

# Quantity validation
df['quantity_valid'] = df['quantity_fulfilled/received'] <= df['quantity_expected']

print(f"Date sequence violations: {(df['date_sequence_valid'] == False).sum()}")
print(f"Quantity violations: {(df['quantity_valid'] == False).sum()}")
```

## 📈 Key Performance Indicators (KPIs)

### Essential Metrics to Calculate
```python
# Overall supply chain KPIs
kpis = {
    'Perfect Order Rate': (
        df[(df['prd_accuracy_days'] <= 0) & 
           (df['quantity_fulfilled/received'] == df['quantity_expected'])].shape[0] / 
        df[df['actual_delivery_date'].notna()].shape[0]
    ),
    
    'Average Lead Time': df['lead_time_days'].mean(),
    
    'Fill Rate': (
        df['quantity_fulfilled/received'].sum() / 
        df[df['quantity_expected'] > 0]['quantity_expected'].sum()
    ),
    
    'Supplier Diversity': df['vendor_name'].nunique(),
    
    'Average Order Value': df.groupby('po_number')['po_value'].first().mean(),
    
    'On-Time Delivery Rate': (
        (df['prd_accuracy_days'] <= 0).sum() / 
        df['prd_accuracy_days'].notna().sum()
    )
}

kpi_df = pd.DataFrame(list(kpis.items()), columns=['Metric', 'Value'])
kpi_df['Value'] = kpi_df['Value'].round(4)
```

## 🚀 Advanced Analysis Patterns

### 1. Cohort Analysis by PO Creation Month
```python
# Create cohort based on PO creation month
df['cohort'] = pd.to_datetime(df['po_created_date']).dt.to_period('M')
df['delivery_month'] = pd.to_datetime(df['actual_delivery_date']).dt.to_period('M')

# Calculate months to delivery
df['months_to_deliver'] = (
    df['delivery_month'].astype('datetime64[ns]') - 
    df['cohort'].astype('datetime64[ns]')
).dt.days / 30

cohort_analysis = df.pivot_table(
    values='po_number',
    index='cohort',
    columns='months_to_deliver',
    aggfunc='count'
)
```

### 2. Supplier Clustering
```python
# Create supplier feature matrix
supplier_features = df.groupby('vendor_name').agg({
    'lead_time_days': 'mean',
    'prd_accuracy_days': 'std',  # Delivery variance
    'quantity_fulfilled/received': lambda x: x.sum() / df[df['vendor_name'] == x.name]['quantity_expected'].sum(),
    'po_value': 'sum',
    'po_number': 'nunique'
}).dropna()

# Normalize for clustering
from sklearn.preprocessing import StandardScaler
scaler = StandardScaler()
supplier_features_scaled = scaler.fit_transform(supplier_features)
```

## 💡 Tips for Effective Analysis

1. **Always Filter by Lifecycle Stage**: Don't analyze the entire dataset at once
2. **Check Date Formats**: Many date fields are stored as objects - convert before analysis
3. **Handle Outliers**: Some quantity fields have extreme values (e.g., 990,000 units)
4. **Use Composite Keys**: Combine `po_number` + `po_line_unique_key` for line-level uniqueness
5. **Consider Currency**: All monetary values are in EUR
6. **Validate Calculations**: Cross-check fill rates and lead times with business logic

## 🔗 Related Fields Quick Reference

### For Order Analysis
- Primary: `po_number`, `po_created_date`, `po_value`
- Secondary: `vendor_name`, `marketplace`, `final_status`

### For Delivery Analysis
- Primary: `actual_delivery_date`, `final_prd_date`, `quantity_fulfilled/received`
- Secondary: `shipment_number`, `receiving_location`, `transit_time_days`

### For Financial Analysis
- Primary: `po_line_value`, `pi_payment_date`, `ci_payment_date`
- Secondary: `supplier_payment_terms`, `invoice` fields

### For Quality Analysis
- Primary: `qi_flag`, `compliance`, `compliance_testing_date`
- Secondary: `qc_schedule_date`, `anti_po_flag`

## 📚 Additional Resources

- **Data Dictionary**: Refer to the comprehensive field list above
- **Sample Queries**: Use the provided DataFrame examples as templates
- **Validation Rules**: Apply the data quality checks before analysis
- **Best Practices**: Filter → Clean → Transform → Analyze → Validate

---
*Each code example is self-contained and can be executed independently after loading the base CSV file. Please improvise if the ask is different from the ones listed above*