# otif_pull.csv

## Auto-Generated Overview
- **File**: otif_pull.csv
- **Columns**: Unnamed: 0, internal id, date created, document number, associated brands, id, name, supplier confirmation status, final status, memo (main), market place, supplier payment terms, incoterm, line id, item, asin number, quantity, quantity fulfilled/received, quantity on shipments, first prd, prd, planned prd, confirmed crd, quality control date, quality control status, hs | sign-off shipment booking im line, hs | sign-off shipment booking sm line, production status, batch_id, wh type, considered for anti-po, prd reconfirmed, invoice number, invoice status, summary filter, otif focus, mp, per unit amount, pending units, pending value, po_razin_id, line payment type, batch payment type, inb payment type, line invoice submission status, batch invoice submission status, inb invoice submission status, line payment status, batch payment status, inb payment status, batch qc pending, vp booking status, fob date, fob status, batch pickup status, shipping status, inb#, shipment_status, shipment_substatus, estimated otif delivery date, supplier telex status, sm telex status, ffw telex status, cm, sm, compliance status, current status, sub status, days bucket, team, reporting status, reporting days bucket, l2 final status, final poc, final team, snapshot_ts
- **Last Modified**: 2025-09-24T01:52:56.975441


## 📋 Enhanced Column Descriptions

### ⚠️ **Important Notes About Data Types and Special Fields**
- **Date Fields**: All date columns are stored as `object` type and need parsing with `pd.to_datetime()`
- **CM/SM Fields**: These refer to Category Manager and Supply Manager NAMES (not dates like in OnTime_Data)
- **Payment Structure**: Three-tier tracking system (line → batch → inbound)
- **Status Hierarchy**: Multiple status levels from operational to reporting views

---

### 🆔 **Core Identifiers & System Fields**
- **Unnamed: 0** (int64): System-generated row index number for dataset ordering
- **internal id** (int64): Unique internal system identifier for the purchase order
- **document number** (object): Purchase order number (e.g., "PO377368") - main business identifier
- **id** (float64): Secondary ID field, often contains null values
- **line id** (int64): Line item number within the purchase order (1, 2, 3, etc.)
- **po_razin_id** (object): Composite identifier combining PO number with product SKU

### 🏢 **Supplier & Vendor Information**
- **name** (object): Full supplier/vendor company name (e.g., "JIANGSU PLUS INTERNATIONAL TRADING CO.,LTD")
- **associated brands** (object): Brand name associated with the order (e.g., "Prestee", "Bolt Dropper")
- **supplier confirmation status** (object): Supplier's acceptance status (Confirmed, Rejected, Pending)
- **supplier payment terms** (object): Payment structure (e.g., "0% PI 0d 0% CI 0d 100% BL 45d")
- **supplier telex status** (object): Supplier communication/release status (Released, Pending)

### 📦 **Product & Order Information**
- **item** (object): Product SKU/RAZIN identifier (e.g., "PXPR-000161", "BOLT-001284")
- **asin number** (object): Amazon Standard Identification Number for the product
- **market place** (object): Target marketplace for the product (US, EU, etc.)
- **mp** (object): Abbreviated marketplace identifier
- **memo (main)** (object): Main order notes/comments (e.g., "Razor_July_Cycle_2025")

### 📊 **Quantity & Fulfillment Tracking**
- **quantity** (int64): Original ordered quantity
- **quantity fulfilled/received** (int64): Actual quantity delivered/received
- **quantity on shipments** (float64): Quantity currently in transit
- **pending units** (int64): Outstanding quantity still to be delivered
- **pending value** (float64): Monetary value of pending/outstanding units

### 💰 **Financial & Payment Information**
- **per unit amount** (float64): Unit price/cost per item
- **incoterm** (object): International commercial terms (FOB, CIF, etc.)
- **invoice number** (object): Invoice reference number
- **invoice status** (object): Invoice processing status
- **line payment type** (object): Payment method for this line item (BL = Bill of Lading)
- **batch payment type** (object): Payment method for the batch
- **inb payment type** (object): Payment method for inbound shipment
- **line payment status** (object): Payment status for this line (Paid, Not Paid, Pending)
- **batch payment status** (object): Payment status for the batch
- **inb payment status** (object): Payment status for inbound shipment
- **line invoice submission status** (object): Invoice submission status for line
- **batch invoice submission status** (object): Invoice submission status for batch
- **inb invoice submission status** (object): Invoice submission status for inbound

⚠️ **IMPORTANT - PO Value Calculation:**
- This dataset does NOT have a direct `po_value` column
- **To calculate total PO value**: Multiply `per unit amount` × `quantity` for each line, then group by `document number`
- **Total unique PO value**: `df.groupby('document number').apply(lambda x: (x['per unit amount'] * x['quantity']).sum()).sum()`
- Each PO (document number) can have multiple line items with different products and quantities
- **Line value** = `per unit amount` × `quantity`
- **PO value** = Sum of all line values for that document number

### 📅 **Date & Timeline Fields**
- **date created** (object): Purchase order creation date
- **first prd** (object): Initial Production Ready Date (first planned date)
- **prd** (object): Current/Final Production Ready Date
- **planned prd** (object): Originally planned Production Ready Date
- **confirmed crd** (object): Confirmed Cargo Ready Date
- **prd reconfirmed** (object): Indicator if PRD was reconfirmed/changed
- **quality control date** (object): Date of quality control inspection
- **fob date** (object): Free on Board date (shipping date)
- **estimated otif delivery date** (object): Estimated delivery date for OTIF calculation
- **snapshot_ts** (object): Timestamp when this data snapshot was taken

### 🔄 **Status & Workflow Tracking**
- **final status** (object): Overall order status (Pending Receipt, Partially Received, etc.)
- **current status** (object): Real-time operational status
- **sub status** (object): Detailed sub-status within current status
- **l2 final status** (object): Level 2 categorized final status
- **reporting status** (object): Status used for reporting purposes
- **production status** (object): Manufacturing/production stage status
- **quality control status** (object): QC inspection results (Released, Awaiting Release, etc.)
- **compliance status** (object): Regulatory compliance status (Approved, Pending)
- **shipment_status** (object): Shipping status (In Transit, Delivered, etc.)
- **shipment_substatus** (object): Detailed shipping sub-status
- **shipping status** (object): General shipping status
- **batch pickup status** (object): Status of batch pickup from supplier
- **vp booking status** (object): Vendor Portal booking status (Booked, Not Booked)
- **fob status** (float64): Free on Board status indicator

### 🏭 **Production & Quality Control**
- **batch_id** (object): Production batch identifier (e.g., "BATCH0010616")
- **wh type** (object): Warehouse type (3PL, Direct, etc.)
- **considered for anti-po** (object): Flag for anti-purchase order consideration
- **batch qc pending** (object): Quality control pending status for batch (Yes/No)
- **hs | sign-off shipment booking im line** (object): Import Manager sign-off status
- **hs | sign-off shipment booking sm line** (object): Supply Manager sign-off status

### 👥 **Personnel & Management Fields**
- **cm** (object): Category Manager name - the person responsible for managing the product category and coordinating with suppliers on product-related decisions
- **sm** (object): Supply Manager name - the person responsible for managing supplier relationships, production timelines, and ensuring delivery schedules are met
- **final poc** (object): Final Point of Contact person name - the primary contact person responsible for this order
- **team** (object): Responsible team identifier (CN, US, etc.) - indicates the regional or functional team managing this order
- **final team** (object): Final assigned team - the team ultimately responsible for order completion

### 📋 **Business Intelligence & Reporting**
- **summary filter** (object): Filter category for summary reporting (e.g., "2026 Q1 - Batch 1")
- **otif focus** (object): OTIF (On-Time In-Full) priority flag (NPD, High, Low)
- **days bucket** (object): Time-based categorization bucket (On-Track, 01-03, etc.)
- **reporting days bucket** (float64): Numeric days bucket for reporting

### 🚚 **Shipping & Logistics**
- **inb#** (object): Inbound shipment number identifier
- **sm telex status** (object): Supply Manager telex release status
- **ffw telex status** (object): Freight Forwarder telex status

## Data Ranges
- **Unnamed: 0**: 0.0 to 3143.0 (avg: 1571.50)
- **internal id**: 25706864.0 to 67275512.0 (avg: 63329068.84)
- **id**: nan to nan (avg: nan)
- **line id**: 1.0 to 3414.0 (avg: 9.56)
- **quantity**: 1.0 to 990000.0 (avg: 1056.20)
- **quantity fulfilled/received**: 0.0 to 14909.0 (avg: 16.97)
- **quantity on shipments**: 8.0 to 55500.0 (avg: 936.52)
- **per unit amount**: 0.0304823 to 93.45 (avg: 7.37)
- **pending units**: 1.0 to 990000.0 (avg: 1039.22)
- **pending value**: 2.65 to 180931.5 (avg: 2981.11)
- **fob status**: nan to nan (avg: nan)
- **reporting days bucket**: nan to nan (avg: nan)

## Sample Data
| Unnamed: 0 | internal id | date created | document number | associated brands | id | name | supplier confirmation status | final status | memo (main) | market place | supplier payment terms | incoterm | line id | item | asin number | quantity | quantity fulfilled/received | quantity on shipments | first prd | prd | planned prd | confirmed crd | quality control date | quality control status | hs | sign-off shipment booking im line | hs | sign-off shipment booking sm line | production status | batch_id | wh type | considered for anti-po | prd reconfirmed | invoice number | invoice status | summary filter | otif focus | mp | per unit amount | pending units | pending value | po_razin_id | line payment type | batch payment type | inb payment type | line invoice submission status | batch invoice submission status | inb invoice submission status | line payment status | batch payment status | inb payment status | batch qc pending | vp booking status | fob date | fob status | batch pickup status | shipping status | inb# | shipment_status | shipment_substatus | estimated otif delivery date | supplier telex status | sm telex status | ffw telex status | cm | sm | compliance status | current status | sub status | days bucket | team | reporting status | reporting days bucket | l2 final status | final poc | final team | snapshot_ts |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 0 | 66928377 | 2025-08-13 | PO377368 | Prestee | nan | 74964 JIANGSU PLUS INTERNATIONAL TRADING CO.,LTD | Confirmed | Pending Receipt | Razor_July_Cycle_2025 | US | 0% PI 0d 0% CI 0d 100% BL 45d | FOB | 2 | PXPR-000161 | B0CC35ZCJ2 | 291 | 0 | nan | 2025-09-22 | 2025-09-22 | 2025-09-22 | 2025-10-02 | 2025-09-24 | 1 Awaiting Release | Yes | Yes | Ready for batching | BATCH0010616 | 3PL | No | Yes | nan | nan | 2026 Q1 - Batch 1 | NPD | US | 8.26 | 291 | 2403.66 | PO377368PXPR-0001612 | BL | BL | BL | Submitted | Submitted | Submitted | Paid | Paid | Paid | Yes | Booked | nan | nan | Not Picked | Not Shipped | nan | nan | nan | 2025-11-14 | Released | Released | Released | Paul Fong | Maggie Yang | Approved | 20. Pre Pickup Check | 20a. QC Release Missing | On-Track | CN | 05. Pickup + Shipping | nan | QC scheduled | Young Cao | Compliance & QC | 2025-09-23 14:45:50.495636+00:00 |
| 1 | 67247335 | 2025-09-17 | PO378507 | Bolt Dropper | nan | 73109 YOLINK FASTENER (JIAXING) CO., LTD | Rejected | Pending Receipt | Razor_August_Cycle_2025 | US | 0% PI 0d 0% CI 0d 100% BL 0d | FOB | 37 | BOLT-001284 | B07D1KZ28N | 300 | 0 | nan | nan | nan | 2025-12-11 | nan | nan | 1 Awaiting Release | No | No | nan | nan | nan | No | No | nan | nan | 2026 Q1 - Batch 2 | Low | US | 0.5 | 300 | 150.0 | PO378507BOLT-00128437 | BL | BL | BL | Not Submitted | Not Submitted | Not Submitted | Not Paid | Not Paid | Not Paid | Yes | Not Booked | nan | nan | Not Picked | Not Shipped | nan | nan | nan | 2026-02-05 | Released | Released | Released | Paul Fong | Maggie Yang | Approved | 02. Supplier Confirmation Pending | 02c. Rejected | 01-03 | CN | 01. Pre Production | nan | No L2 Status | Paul Fong | CM | 2025-09-23 14:45:50.495636+00:00 |
| 2 | 63648408 | 2025-04-14 | PO372477 | Kidzlane | nan | 74634 Wah Shing Toys Co.,Ltd. | Confirmed | Partially Received | Q4_2025_Batch1 | US | 30% PI 0d 0% CI 0d 70% BL 0d | FOB | 12 | KIDZ-000235 | B08LJRQV2N | 1452 | 0 | 1452.0 | 2025-08-14 | 2025-08-15 | 2025-08-14 | 2025-08-19 | 2025-08-15 | 3 Released | Yes | Yes | Cargo Picked(SM) | BATCH0010440 | 3PL | No | Yes | Bill #CI-PO372477-5 | Bill:Paid In Full | 2025 Q4 - Batch 1 | High | US | 38.86 | 1452 | 56424.72 | PO372477KIDZ-00023512 | BL | BL | BL | Submitted | Submitted | Submitted | Paid | Paid | Paid | No | Booked | nan | nan | Picked | Shipped | INBSHIP14511 | In Transit | nan | 2025-09-26 | Released | Released | Released | Jeremy Lin | Lemon Shen | Approved | 30. Stock Delivery Pending | 30c. Appointment in Future | On-Track | CN | 07. Arrived | nan | No L2 Status | nan | nan | 2025-09-23 14:45:50.495636+00:00 |


# OTIF Pull Dataset - Comprehensive Analysis Guide

## 📁 Dataset Overview

### File Information
- **Dataset Name**: `otif_pull.csv`
- **Total Fields**: 76 columns
- **Data Type**: Supply chain OTIF (On-Time In-Full) tracking dataset
- **Snapshot Date**: Available in `snapshot_ts` column
- **Focus**: Purchase order fulfillment and delivery performance tracking

### What This Dataset Contains
This is an OTIF (On-Time In-Full) performance tracking dataset designed to monitor supply chain delivery effectiveness. Each row represents a purchase order line item with comprehensive tracking from order creation through delivery, with special emphasis on timeliness and completeness metrics. The dataset is optimized for measuring supplier performance against promised delivery dates and quantities.

## 🎯 Quick Start: Loading the Data

### Python/Pandas Example
```python
import pandas as pd
import numpy as np

# Load the dataset
# Parse important date columns for analysis
date_cols = ['date created', 'first prd', 'prd', 'planned prd', 'confirmed crd', 
             'quality control date', 'estimated otif delivery date', 'fob date', 'snapshot_ts']
for col in date_cols:
    if col in df.columns:
        df[col] = pd.to_datetime(df[col], errors='coerce')

# Quick data inspection
print(f"Dataset shape: {df.shape}")
print(f"Memory usage: {df.memory_usage(deep=True).sum() / 1024**2:.2f} MB")
print(f"OTIF Focus Records: {df['otif focus'].notna().sum()}")
print(f"Date range: {df['date created'].min()} to {df['date created'].max()}")

# View first few rows
df.head()
```

## 🔍 Understanding the OTIF Structure

### What is OTIF?
**On-Time In-Full (OTIF)** measures two critical supply chain metrics:
- **On-Time**: Did the order arrive by the promised date?
- **In-Full**: Was the complete quantity delivered?

### Key Identifier Fields
```
Purchase Order Level
    ├── document number (PO number)
    ├── internal id (System ID)
    └── po_razin_id (Composite PO-SKU identifier)
        └── Line Level
            ├── line id (Line item identifier)
            └── item (Product SKU/RAZIN)
                └── Fulfillment Level
                    ├── batch_id (Batch identifier)
                    └── inb# (Inbound shipment number)
```

### OTIF Calculation Framework
```python
# Calculate OTIF metrics
def calculate_otif_metrics(df):
    """Calculate On-Time and In-Full metrics"""
    
    # In-Full: Quantity fulfilled matches quantity ordered
    df['in_full'] = df['quantity fulfilled/received'] >= df['quantity']
    
    # On-Time: Delivery within PRD (requires date comparison)
    df['on_time'] = df['estimated otif delivery date'] <= df['prd']
    
    # OTIF: Both conditions met
    df['otif_achieved'] = df['in_full'] & df['on_time']
    
    # Calculate percentages
    metrics = {
        'In-Full Rate': df['in_full'].mean() * 100,
        'On-Time Rate': df[df['estimated otif delivery date'].notna()]['on_time'].mean() * 100,
        'OTIF Rate': df[df['estimated otif delivery date'].notna()]['otif_achieved'].mean() * 100
    }
    
    return metrics

otif_metrics = calculate_otif_metrics(df)
print(f"Overall OTIF Performance: {otif_metrics}")
```

## 📊 Core Data Dimensions

### 1. Supplier/Vendor Information
```python
# Analyze supplier performance
supplier_analysis = df.groupby('name').agg({
    'document number': 'nunique',  # Unique POs
    'quantity': 'sum',  # Total ordered
    'quantity fulfilled/received': 'sum',  # Total delivered
    'pending units': 'sum',  # Outstanding quantity
    'pending value': 'sum'  # Outstanding value
})

# Top suppliers by volume
supplier_analysis.sort_values('quantity', ascending=False).head(10)
```

**Key Supplier Fields**:
- `name`: Supplier/vendor name
- `supplier confirmation status`: Order acceptance status
- `supplier payment terms`: Payment structure
- `supplier telex status`: Communication/release status

### 2. Product & Marketplace Information
```python
# Product analysis by ASIN and marketplace
product_metrics = df.groupby(['asin number', 'market place']).agg({
    'quantity': 'sum',
    'quantity fulfilled/received': 'sum',
    'per unit amount': 'mean',
    'pending units': 'sum'
})

product_metrics['fulfillment_rate'] = (
    product_metrics['quantity fulfilled/received'] / 
    product_metrics['quantity'] * 100
)

# Marketplace performance
marketplace_summary = df.groupby('mp').agg({
    'document number': 'nunique',
    'quantity': 'sum',
    'pending value': 'sum',
    'otif focus': 'count'
})
```

**Key Product Fields**:
- `item`: Product identifier/SKU
- `asin number`: Amazon Standard Identification Number
- `market place` / `mp`: Target marketplace
- `associated brands`: Brand affiliation
- `per unit amount`: Unit price

### 3. Quantity & Fulfillment Tracking
```python
# Fulfillment analysis
fulfillment_df = df[df['quantity'] > 0].copy()

fulfillment_df['fulfillment_percentage'] = (
    fulfillment_df['quantity fulfilled/received'] / 
    fulfillment_df['quantity'] * 100
)

fulfillment_df['pending_percentage'] = (
    fulfillment_df['pending units'] / 
    fulfillment_df['quantity'] * 100
)

# Categorize fulfillment status
def categorize_fulfillment(row):
    if row['fulfillment_percentage'] >= 100:
        return 'Over-Fulfilled'
    elif row['fulfillment_percentage'] >= 95:
        return 'Nearly Complete'
    elif row['fulfillment_percentage'] >= 50:
        return 'Partially Fulfilled'
    elif row['fulfillment_percentage'] > 0:
        return 'Minimal Fulfillment'
    else:
        return 'Not Started'

fulfillment_df['fulfillment_category'] = fulfillment_df.apply(categorize_fulfillment, axis=1)
fulfillment_distribution = fulfillment_df['fulfillment_category'].value_counts()
```

**Quantity Fields**:
- `quantity`: Original order quantity
- `quantity fulfilled/received`: Delivered quantity
- `quantity on shipments`: In-transit quantity
- `pending units`: Outstanding quantity
- `pending value`: Outstanding monetary value

## 📅 Date Fields & Timeline Management

### Critical Date Sequences
```python
# Parse and analyze date fields
date_fields = ['date created', 'first prd', 'prd', 'planned prd', 
               'confirmed crd', 'quality control date', 'fob date',
               'estimated otif delivery date']

for col in date_fields:
    df[col] = pd.to_datetime(df[col], errors='coerce')

# Calculate time metrics
df['prd_change_days'] = (df['prd'] - df['first prd']).dt.days
df['qc_to_delivery_days'] = (df['estimated otif delivery date'] - df['quality control date']).dt.days
df['total_lead_time'] = (df['estimated otif delivery date'] - df['date created']).dt.days

# Analyze PRD stability
prd_stability = df.groupby('name').agg({
    'prd_change_days': 'mean',
    'document number': 'count'
}).rename(columns={'document number': 'order_count'})
```

### Date Field Categories

#### Order & Planning Dates
- `date created`: PO creation date
- `first prd`: Initial Production Ready Date
- `prd`: Current/Final PRD
- `planned prd`: Originally planned PRD
- `confirmed crd`: Confirmed Cargo Ready Date
- `prd reconfirmed`: PRD reconfirmation indicator

#### Quality & Production Dates
- `quality control date`: QC inspection date
- `fob date`: Free on Board date
- `estimated otif delivery date`: Expected delivery for OTIF measurement

## 🏷️ Status Fields & Workflow States

### Multi-Level Status Tracking
```python
# Analyze status distribution across different levels
status_overview = pd.DataFrame({
    'Final Status': df['final status'].value_counts(),
    'Current Status': df['current status'].value_counts(),
    'L2 Final Status': df['l2 final status'].value_counts(),
    'Reporting Status': df['reporting status'].value_counts()
})

# Shipment status analysis
shipment_status = df.groupby(['shipment_status', 'shipment_substatus']).size().unstack(fill_value=0)

# Production and quality status
production_quality = pd.crosstab(df['production status'], df['quality control status'])
```

**Status Hierarchy**:
- `final status`: Overall order status
- `current status` & `sub status`: Real-time status tracking
- `l2 final status`: Level 2 categorization
- `reporting status`: Status for reporting purposes
- `shipment_status` & `shipment_substatus`: Detailed shipment tracking

### Payment & Invoice Status
```python
# Payment status analysis by type
payment_types = ['line', 'batch', 'inb']
payment_status_summary = {}

for ptype in payment_types:
    payment_col = f'{ptype} payment status'
    invoice_col = f'{ptype} invoice submission status'
    
    if payment_col in df.columns:
        payment_status_summary[ptype] = {
            'Payment': df[payment_col].value_counts().to_dict(),
            'Invoice': df[invoice_col].value_counts().to_dict() if invoice_col in df.columns else {}
        }

# Overall payment health
df['payment_complete'] = df['line payment status'].str.contains('Paid', case=False, na=False)
payment_completion_rate = df['payment_complete'].mean() * 100
```

**Payment/Invoice Fields**:
- `line payment type/status`: Line-level payment tracking
- `batch payment type/status`: Batch-level payment tracking
- `inb payment type/status`: Inbound shipment payment tracking
- `invoice number` & `invoice status`: Invoice tracking

## 💡 OTIF-Specific Analysis Features

### 1. OTIF Focus Analysis
```python
# Analyze OTIF focus items
otif_focus_df = df[df['otif focus'].notna()].copy()

print(f"OTIF Focus Items: {len(otif_focus_df)} ({len(otif_focus_df)/len(df)*100:.1f}% of total)")

# OTIF focus by supplier
otif_by_supplier = otif_focus_df.groupby('name').agg({
    'document number': 'nunique',
    'quantity': 'sum',
    'quantity fulfilled/received': 'sum',
    'pending value': 'sum'
})

otif_by_supplier['otif_fill_rate'] = (
    otif_by_supplier['quantity fulfilled/received'] / 
    otif_by_supplier['quantity'] * 100
)
```

### 2. Days Bucket Analysis
```python
# Analyze delivery performance by days bucket
days_bucket_analysis = df.groupby('days bucket').agg({
    'document number': 'count',
    'quantity': 'sum',
    'pending units': 'sum',
    'pending value': 'sum'
})

# Reporting days bucket for trend analysis
if 'reporting days bucket' in df.columns:
    reporting_bucket_trend = df.groupby('reporting days bucket').agg({
        'document number': 'nunique',
        'quantity fulfilled/received': 'sum',
        'quantity': 'sum'
    })
    reporting_bucket_trend['fill_rate'] = (
        reporting_bucket_trend['quantity fulfilled/received'] / 
        reporting_bucket_trend['quantity'] * 100
    )
```

### 3. Team & Ownership Analysis
```python
# Analyze performance by team and POC
team_performance = df.groupby(['team', 'final team']).agg({
    'document number': 'nunique',
    'quantity': 'sum',
    'quantity fulfilled/received': 'sum',
    'pending units': 'sum'
})

# POC (Point of Contact) analysis
poc_workload = df.groupby('final poc').agg({
    'document number': 'nunique',
    'pending units': 'sum',
    'pending value': 'sum'
}).sort_values('pending value', ascending=False)

# CM/SM analysis
cm_sm_distribution = df.groupby(['cm', 'sm']).size().unstack(fill_value=0)
```

## 🔧 Practical Analysis Examples

### 1. Comprehensive OTIF Dashboard
```python
def create_otif_dashboard(df):
    """Generate comprehensive OTIF metrics dashboard"""
    
    # Overall metrics
    total_orders = df['document number'].nunique()
    total_lines = len(df)
    total_value = df['per unit amount'].multiply(df['quantity']).sum()
    
    # Fulfillment metrics
    total_ordered = df['quantity'].sum()
    total_fulfilled = df['quantity fulfilled/received'].sum()
    total_pending = df['pending units'].sum()
    
    # Calculate rates
    overall_fill_rate = (total_fulfilled / total_ordered * 100) if total_ordered > 0 else 0
    
    # Status distribution
    status_dist = df['final status'].value_counts().head(5)
    
    # Time metrics
    avg_lead_time = df['total_lead_time'].mean()
    
    dashboard = {
        'Summary Metrics': {
            'Total POs': total_orders,
            'Total Line Items': total_lines,
            'Total Order Value': f"${total_value:,.2f}",
            'Overall Fill Rate': f"{overall_fill_rate:.1f}%"
        },
        'Quantity Metrics': {
            'Total Ordered': f"{total_ordered:,}",
            'Total Fulfilled': f"{total_fulfilled:,}",
            'Total Pending': f"{total_pending:,}",
            'Pending Value': f"${df['pending value'].sum():,.2f}"
        },
        'Performance Metrics': {
            'Average Lead Time': f"{avg_lead_time:.1f} days",
            'Orders with QC': df['quality control date'].notna().sum(),
            'OTIF Focus Count': df['otif focus'].notna().sum()
        }
    }
    
    return dashboard

dashboard = create_otif_dashboard(df)
for category, metrics in dashboard.items():
    print(f"\n{category}:")
    for metric, value in metrics.items():
        print(f"  {metric}: {value}")
```

### 2. Supplier Scorecard with OTIF Focus
```python
def supplier_otif_scorecard(df, supplier_name):
    """Generate OTIF-focused supplier scorecard"""
    
    supplier_df = df[df['name'] == supplier_name].copy()
    
    if len(supplier_df) == 0:
        return None
    
    # Calculate metrics
    total_pos = supplier_df['document number'].nunique()
    total_quantity = supplier_df['quantity'].sum()
    fulfilled_quantity = supplier_df['quantity fulfilled/received'].sum()
    
    # OTIF specific
    otif_items = supplier_df['otif focus'].notna().sum()
    otif_percentage = (otif_items / len(supplier_df) * 100) if len(supplier_df) > 0 else 0
    
    # Payment status
    paid_lines = supplier_df['line payment status'].str.contains('Paid', case=False, na=False).sum()
    payment_completion = (paid_lines / len(supplier_df) * 100) if len(supplier_df) > 0 else 0
    
    # Quality metrics
    qc_required = supplier_df['quality control date'].notna().sum()
    qc_passed = supplier_df[supplier_df['quality control status'] == 'Passed'].shape[0]
    
    scorecard = {
        'Supplier': supplier_name,
        'Total POs': total_pos,
        'Total Lines': len(supplier_df),
        'Fill Rate': f"{(fulfilled_quantity/total_quantity*100):.1f}%" if total_quantity > 0 else "0%",
        'OTIF Focus Items': f"{otif_items} ({otif_percentage:.1f}%)",
        'Pending Units': f"{supplier_df['pending units'].sum():,}",
        'Pending Value': f"${supplier_df['pending value'].sum():,.2f}",
        'Payment Completion': f"{payment_completion:.1f}%",
        'QC Pass Rate': f"{(qc_passed/qc_required*100):.1f}%" if qc_required > 0 else "N/A"
    }
    
    return scorecard

# Generate scorecards for top suppliers
top_suppliers = df['name'].value_counts().head(5).index
for supplier in top_suppliers:
    scorecard = supplier_otif_scorecard(df, supplier)
    if scorecard:
        print(f"\n{'='*50}")
        for key, value in scorecard.items():
            print(f"{key}: {value}")
```

### 3. PRD Stability Analysis
```python
def analyze_prd_stability(df):
    """Analyze PRD changes and stability"""
    
    # Filter records with PRD data
    prd_df = df[df['prd'].notna() & df['first prd'].notna()].copy()
    
    # Calculate PRD changes
    prd_df['prd_changed'] = prd_df['prd'] != prd_df['first prd']
    prd_df['prd_change_days'] = (prd_df['prd'] - prd_df['first prd']).dt.days
    
    # Categorize PRD changes
    def categorize_prd_change(days):
        if pd.isna(days):
            return 'No Change'
        elif days < 0:
            return 'Pulled In'
        elif days == 0:
            return 'No Change'
        elif days <= 7:
            return 'Delayed 1-7 days'
        elif days <= 14:
            return 'Delayed 8-14 days'
        else:
            return 'Delayed 15+ days'
    
    prd_df['prd_change_category'] = prd_df['prd_change_days'].apply(categorize_prd_change)
    
    # Analysis results
    results = {
        'Total Records with PRD': len(prd_df),
        'PRDs Changed': prd_df['prd_changed'].sum(),
        'PRD Change Rate': f"{(prd_df['prd_changed'].mean() * 100):.1f}%",
        'Average Change (days)': prd_df['prd_change_days'].mean(),
        'PRD Reconfirmed': prd_df['prd reconfirmed'].notna().sum()
    }
    
    # Distribution of changes
    change_distribution = prd_df['prd_change_category'].value_counts()
    
    return results, change_distribution

prd_results, prd_distribution = analyze_prd_stability(df)
print("PRD Stability Analysis:")
for key, value in prd_results.items():
    print(f"  {key}: {value}")
print("\nPRD Change Distribution:")
print(prd_distribution)
```

### 4. Workflow Bottleneck Analysis
```python
def identify_bottlenecks(df):
    """Identify bottlenecks in the fulfillment process"""
    
    bottlenecks = {}
    
    # Quality control bottleneck
    qc_pending = df[df['batch qc pending'] == 'Yes'].shape[0]
    bottlenecks['QC Pending'] = qc_pending
    
    # Payment bottlenecks
    payment_pending = df[~df['line payment status'].str.contains('Paid', case=False, na=False)].shape[0]
    bottlenecks['Payment Pending'] = payment_pending
    
    # Invoice bottlenecks
    invoice_pending = df[df['invoice status'] != 'Approved'].shape[0]
    bottlenecks['Invoice Pending'] = invoice_pending
    
    # Booking bottlenecks
    booking_issues = df[df['vp booking status'].isna()].shape[0]
    bottlenecks['Booking Issues'] = booking_issues
    
    # Telex bottlenecks
    telex_fields = ['supplier telex status', 'sm telex status', 'ffw telex status']
    for field in telex_fields:
        if field in df.columns:
            pending = df[df[field] != 'Released'].shape[0]
            bottlenecks[f"{field.split()[0].title()} Telex Pending"] = pending
    
    # Sort by impact
    bottlenecks_sorted = dict(sorted(bottlenecks.items(), key=lambda x: x[1], reverse=True))
    
    return bottlenecks_sorted

bottlenecks = identify_bottlenecks(df)
print("\nWorkflow Bottlenecks (Line Items Affected):")
for bottleneck, count in bottlenecks.items():
    percentage = (count / len(df) * 100)
    print(f"  {bottleneck}: {count:,} ({percentage:.1f}%)")
```

## ⚠️ Data Quality Considerations

### Data Validation Checks
```python
def validate_data_quality(df):
    """Perform comprehensive data quality checks"""
    
    quality_issues = []
    
    # Check for negative quantities
    negative_qty = df[df['quantity'] < 0].shape[0]
    if negative_qty > 0:
        quality_issues.append(f"Negative quantities found: {negative_qty} records")
    
    # Check fulfillment > ordered
    over_fulfilled = df[df['quantity fulfilled/received'] > df['quantity']].shape[0]
    if over_fulfilled > 0:
        quality_issues.append(f"Over-fulfillment found: {over_fulfilled} records")
    
    # Check for duplicate PO lines
    duplicates = df[df.duplicated(subset=['document number', 'line id'], keep=False)]
    if len(duplicates) > 0:
        quality_issues.append(f"Duplicate PO lines found: {len(duplicates)} records")
    
    # Check date consistency
    date_issues = df[df['prd'] < df['date created']].shape[0]
    if date_issues > 0:
        quality_issues.append(f"PRD before creation date: {date_issues} records")
    
    # Check pending units vs quantity math
    df['calculated_pending'] = df['quantity'] - df['quantity fulfilled/received']
    pending_mismatch = df[abs(df['calculated_pending'] - df['pending units']) > 1].shape[0]
    if pending_mismatch > 0:
        quality_issues.append(f"Pending units calculation mismatch: {pending_mismatch} records")
    
    return quality_issues

quality_issues = validate_data_quality(df)
if quality_issues:
    print("Data Quality Issues Found:")
    for issue in quality_issues:
        print(f"  ⚠️ {issue}")
else:
    print("✅ No major data quality issues detected")
```

## 📈 Key Performance Indicators (KPIs)

### Essential OTIF KPIs
```python
def calculate_kpis(df):
    """Calculate comprehensive OTIF KPIs"""
    
    kpis = {}
    
    # Fulfillment KPIs
    kpis['Overall Fill Rate'] = (
        df['quantity fulfilled/received'].sum() / 
        df['quantity'].sum() * 100
    ) if df['quantity'].sum() > 0 else 0
    
    # OTIF specific
    otif_focus_df = df[df['otif focus'].notna()]
    if len(otif_focus_df) > 0:
        kpis['OTIF Focus Fill Rate'] = (
            otif_focus_df['quantity fulfilled/received'].sum() / 
            otif_focus_df['quantity'].sum() * 100
        )
    
    # Supplier diversity
    kpis['Active Suppliers'] = df['name'].nunique()
    kpis['Active Marketplaces'] = df['market place'].nunique()
    
    # Financial KPIs
    kpis['Total Pending Value'] = df['pending value'].sum()
    kpis['Average Order Value'] = df.groupby('document number')['per unit amount'].sum().mean()
    
    # Quality KPIs
    qc_records = df[df['quality control date'].notna()]
    if len(qc_records) > 0:
        kpis['QC Pass Rate'] = (
            qc_records[qc_records['quality control status'] == 'Passed'].shape[0] / 
            len(qc_records) * 100
        )
    
    # Payment KPIs
    kpis['Payment Completion Rate'] = (
        df['line payment status'].str.contains('Paid', case=False, na=False).mean() * 100
    )
    
    return kpis

kpis = calculate_kpis(df)
print("\n📊 Key Performance Indicators:")
for kpi, value in kpis.items():
    if isinstance(value, float):
        if 'Rate' in kpi:
            print(f"  {kpi}: {value:.1f}%")
        elif 'Value' in kpi:
            print(f"  {kpi}: ${value:,.2f}")
        else:
            print(f"  {kpi}: {value:.2f}")
    else:
        print(f"  {kpi}: {value}")
```

## 🚀 Advanced Analysis Patterns

### 1. Cohort Analysis by PO Creation
```python
# Create monthly cohorts
df['po_month'] = pd.to_datetime(df['date created']).dt.to_period('M')

# Cohort fulfillment analysis
cohort_analysis = df.groupby('po_month').agg({
    'document number': 'nunique',
    'quantity': 'sum',
    'quantity fulfilled/received': 'sum',
    'pending units': 'sum',
    'pending value': 'sum'
})

cohort_analysis['fill_rate'] = (
    cohort_analysis['quantity fulfilled/received'] / 
    cohort_analysis['quantity'] * 100
)

cohort_analysis['avg_pending_value'] = (
    cohort_analysis['pending value'] / 
    cohort_analysis['document number']
)

print("Monthly Cohort Performance:")
print(cohort_analysis[['fill_rate', 'avg_pending_value']].tail(6))
```

### 2. Predictive OTIF Risk Scoring
```python
def calculate_risk_score(row):
    """Calculate OTIF risk score for each line item"""
    risk_score = 0
    
    # PRD changes increase risk
    if pd.notna(row['prd']) and pd.notna(row['first prd']):
        if row['prd'] != row['first prd']:
            risk_score += 20
    
    # Pending units increase risk
    if row['pending units'] > 0:
        pending_pct = row['pending units'] / row['quantity'] if row['quantity'] > 0 else 0
        risk_score += min(30, pending_pct * 30)
    
    # Payment delays increase risk
    if 'Pending' in str(row['line payment status']):
        risk_score += 15
    
    # QC pending increases risk
    if row['batch qc pending'] == 'Yes':
        risk_score += 15
    
    # Compliance issues increase risk
    if row['compliance status'] != 'Compliant':
        risk_score += 20
    
    return min(100, risk_score)  # Cap at 100

df['otif_risk_score'] = df.apply(calculate_risk_score, axis=1)

# Categorize risk
df['risk_category'] = pd.cut(df['otif_risk_score'], 
                              bins=[0, 25, 50, 75, 100],
                              labels=['Low', 'Medium', 'High', 'Critical'])

risk_distribution = df['risk_category'].value_counts()
print("\nOTIF Risk Distribution:")
print(risk_distribution)
```

## 💡 Tips for Effective OTIF Analysis

1. **Focus on OTIF Flag**: Filter by `otif focus` for priority items
2. **Use Status Hierarchy**: Understand the relationship between different status fields
3. **Monitor PRD Changes**: Track `prd reconfirmed` and PRD stability
4. **Check Payment Flow**: Analyze line vs batch vs inbound payment status
5. **Validate Calculations**: Cross-check pending units with quantity math
6. **Consider Snapshot Date**: All data is as of the `snapshot_ts` timestamp

## 🔗 Field Relationships Quick Reference

### For OTIF Analysis
- Primary: `otif focus`, `estimated otif delivery date`, `prd`
- Secondary: `quantity`, `quantity fulfilled/received`, `pending units`

### For Supplier Performance
- Primary: `name`, `supplier confirmation status`, `final status`
- Secondary: `prd reconfirmed`, quality and payment status fields

### For Financial Tracking
- Primary: `pending value`, `per unit amount`, payment status fields
- Secondary: `invoice number`, `invoice status`, payment type fields

### For Operational Tracking
- Primary: `current status`, `sub status`, `shipment_status`
- Secondary: `team`, `final poc`, workflow status fields

## 📚 Best Practices

- **Filter First**: Start with relevant status or OTIF focus filters
- **Check Dates**: Ensure date fields are properly parsed before calculations
- **Validate Math**: Verify quantity calculations and pending unit logic
- **Use Hierarchies**: Leverage multi-level status fields for detailed analysis
- **Monitor Bottlenecks**: Regular checks on QC, payment, and telex status
- **Track Changes**: Monitor PRD changes and reconfirmations

---
*This guide provides comprehensive analysis patterns for OTIF performance tracking. Adapt these examples to your specific business requirements and KPIs.*