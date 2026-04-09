# FBA Emailer Data Documentation

## Auto-Generated Overview
- **File**: fba_emailer.csv
- **Columns**: Timestamp, Batch Id, PO, FBA Id, Vendor
- **Last Modified**: 2025-09-19

## Column Information with Business Meanings

### ⏰ **Timestamp**
- **Description**: Date and time when the FBA shipment notification was sent or logged
- **Format**: ISO 8601 datetime (e.g., "2025-09-03T11:14:32.460Z")
- **Business Context**: Tracks when vendors were notified about FBA shipment requirements
- **Sample Values**: 2025-09-03T11:14:32.460Z, 2025-09-16T10:32:28.000Z

### 📦 **Batch Id**
- **Description**: Unique identifier for a shipment batch
- **Format**: "BATCH" + 7-digit number (e.g., "BATCH0010572")
- **Business Context**: Groups multiple purchase orders that will ship together
- **Unique Values**: 10 (one per row in current dataset)
- **Sample Values**: BATCH0010572, BATCH0010571, BATCH0010569

### 📋 **PO (Purchase Order)**
- **Description**: Purchase Order number
- **Format**: "PO" + 6-digit number (e.g., "PO375435")
- **Business Context**: Links to the main procurement system for order tracking
- **Relationship**: Can be joined with OnTime_Data.csv on po_number field
- **Sample Values**: PO375435, PO374371, PO374007

### 🏷️ **FBA Id**
- **Description**: Fulfillment by Amazon shipment identifier
- **Format**: "FBA" + alphanumeric code (e.g., "FBA190K4N93X")
- **Business Context**: Amazon's tracking ID for inbound shipments to FBA warehouses
- **Unique Values**: 10 (one per row - no duplicates)
- **Sample Values**: FBA190K4N93X, FBA190K536CY, FBA190K4R1Z6

### 🏢 **Vendor**
- **Description**: Supplier/vendor company name
- **Format**: Company legal name, often includes location or business type
- **Business Context**: The supplier responsible for shipping goods to Amazon FBA
- **Notable**: One vendor (SHANGHAI XIYUAN IMP. & EXP. CO.,LTD) appears twice
- **Sample Values**: 
  - Quanzhou Jiasheng Wujin Sujiao Co.,Ltd.
  - GHTLINK (HK) International Trading Limited
  - YOLINK FASTENER (JIAXING) CO., LTD

## Dataset Structure

### What This Dataset Contains
This is a **FBA shipment notification log** that tracks when vendors were informed about Amazon FBA (Fulfillment by Amazon) shipping requirements. Each row represents a single notification event linking a purchase order to an FBA shipment ID within a specific batch.

### Key Characteristics
- **Record Type**: Transaction log / Notification tracker
- **Granularity**: One row per PO-to-FBA assignment
- **Time Range**: September 3-16, 2025 (based on sample data)
- **Primary Use**: Track vendor notifications for FBA shipment preparation

## 🔍 Understanding the Data

### Business Process Flow
```
Purchase Order Created (PO) 
    ↓
Assigned to Shipment Batch (Batch Id)
    ↓
FBA Shipment ID Generated (FBA Id)
    ↓
Vendor Notified (Timestamp)
    ↓
Record Created in fba_emailer.csv
```

### Relationships
- **1:1 Relationship**: Each PO maps to exactly one FBA ID in this dataset
- **Batch Grouping**: Multiple POs can belong to the same batch for consolidated shipping
- **Vendor Association**: Each record identifies which vendor needs to prepare the shipment

## 📊 Quick Start: Loading and Analyzing the Data

### Python/Pandas Example
```python
import pandas as pd
from datetime import datetime

# Load the FBA emailer data
df = pd.read_csv('fba_emailer.csv')

# Parse timestamp column
df['Timestamp'] = pd.to_datetime(df['Timestamp'])

# Basic inspection
print(f"Dataset shape: {df.shape}")
print(f"Date range: {df['Timestamp'].min()} to {df['Timestamp'].max()}")
print(f"\nColumn types:")
print(df.dtypes)

# View first few rows
df.head()
```

### Data Quality Checks
```python
# Check for duplicates
duplicate_pos = df[df.duplicated(subset=['PO'], keep=False)]
if len(duplicate_pos) > 0:
    print(f"Warning: {len(duplicate_pos)} duplicate PO entries found")

duplicate_fbas = df[df.duplicated(subset=['FBA Id'], keep=False)]
if len(duplicate_fbas) > 0:
    print(f"Warning: {len(duplicate_fbas)} duplicate FBA IDs found")

# Check for null values
null_summary = df.isnull().sum()
print("\nNull value summary:")
print(null_summary[null_summary > 0])

# Verify format patterns
po_pattern = r'^PO\d{6}$'
fba_pattern = r'^FBA[A-Z0-9]+$'
batch_pattern = r'^BATCH\d{7}$'

df['po_format_valid'] = df['PO'].str.match(po_pattern)
df['fba_format_valid'] = df['FBA Id'].str.match(fba_pattern)
df['batch_format_valid'] = df['Batch Id'].str.match(batch_pattern)

print(f"\nFormat validation:")
print(f"Valid PO format: {df['po_format_valid'].sum()}/{len(df)}")
print(f"Valid FBA format: {df['fba_format_valid'].sum()}/{len(df)}")
print(f"Valid Batch format: {df['batch_format_valid'].sum()}/{len(df)}")
```

## 📈 Analysis Examples

### 1. Vendor Notification Summary
```python
# Analyze vendor notifications
vendor_summary = df.groupby('Vendor').agg({
    'PO': 'count',
    'Batch Id': 'nunique',
    'Timestamp': ['min', 'max']
}).round(2)

vendor_summary.columns = ['PO_Count', 'Unique_Batches', 'First_Notification', 'Last_Notification']
vendor_summary = vendor_summary.sort_values('PO_Count', ascending=False)
print(vendor_summary)
```

### 2. Batch Analysis
```python
# Analyze batches
batch_analysis = df.groupby('Batch Id').agg({
    'PO': 'count',
    'Vendor': lambda x: ', '.join(x.unique()),
    'Timestamp': 'first'
}).rename(columns={
    'PO': 'PO_Count',
    'Vendor': 'Vendors',
    'Timestamp': 'Notification_Time'
})

print("Batch Summary:")
print(batch_analysis)

# Time between notifications within batches
df_sorted = df.sort_values(['Batch Id', 'Timestamp'])
df_sorted['time_diff'] = df_sorted.groupby('Batch Id')['Timestamp'].diff()
print(f"\nAverage time between notifications in same batch: {df_sorted['time_diff'].mean()}")
```

### 3. Daily Notification Pattern
```python
# Extract time components
df['date'] = df['Timestamp'].dt.date
df['hour'] = df['Timestamp'].dt.hour
df['day_of_week'] = df['Timestamp'].dt.day_name()

# Daily summary
daily_summary = df.groupby('date')['PO'].count()
print("Notifications per day:")
print(daily_summary)

# Hourly distribution
hourly_dist = df.groupby('hour')['PO'].count()
print("\nNotifications by hour:")
print(hourly_dist)
```

### 4. Join with OnTime Data
```python
# Load OnTime data for enrichment
ontime_df = pd.read_csv('OnTime_Data.csv')

# Join on PO number
merged_df = df.merge(
    ontime_df[['po_number', 'vendor_name', 'marketplace', 'po_value', 'final_status']],
    left_on='PO',
    right_on='po_number',
    how='left'
)

# Analyze FBA shipments by marketplace
if 'marketplace' in merged_df.columns:
    marketplace_summary = merged_df.groupby('marketplace').agg({
        'FBA Id': 'count',
        'po_value': 'sum'
    }).rename(columns={
        'FBA Id': 'FBA_Shipment_Count',
        'po_value': 'Total_PO_Value'
    })
    print("FBA Shipments by Marketplace:")
    print(marketplace_summary)
```

## 🔗 Integration with OnTime_Data.csv

### Key Join Fields
- **PO** (fba_emailer) ↔ **po_number** (OnTime_Data)
- **Vendor** (fba_emailer) ↔ **vendor_name** (OnTime_Data)
- **Batch Id** (fba_emailer) ↔ **batch_id** (OnTime_Data)

### Example: Complete Shipment Analysis
```python
# Comprehensive analysis joining both datasets
def analyze_fba_shipments(fba_df, ontime_df):
    # Join datasets
    merged = fba_df.merge(
        ontime_df,
        left_on=['PO', 'Batch Id'],
        right_on=['po_number', 'batch_id'],
        how='left'
    )
    
    # Calculate key metrics
    metrics = {
        'Total FBA Shipments': len(fba_df),
        'Unique Vendors': fba_df['Vendor'].nunique(),
        'Unique Batches': fba_df['Batch Id'].nunique(),
        'Date Range': f"{fba_df['Timestamp'].min()} to {fba_df['Timestamp'].max()}",
        'Average POs per Batch': len(fba_df) / fba_df['Batch Id'].nunique(),
        'Matched with OnTime': merged['po_number'].notna().sum(),
        'Match Rate': f"{(merged['po_number'].notna().sum() / len(fba_df) * 100):.1f}%"
    }
    
    return pd.Series(metrics)

# Run analysis
fba_metrics = analyze_fba_shipments(df, ontime_df)
print("FBA Shipment Metrics:")
print(fba_metrics)
```

## 📋 Data Dictionary

| Field | Data Type | Format | Nullable | Description |
|-------|-----------|--------|----------|-------------|
| **Timestamp** | DateTime | ISO 8601 | No | When vendor was notified about FBA shipment |
| **Batch Id** | String | BATCH{7 digits} | No | Shipment batch identifier |
| **PO** | String | PO{6 digits} | No | Purchase order number |
| **FBA Id** | String | FBA{alphanumeric} | No | Amazon FBA shipment identifier |
| **Vendor** | String | Free text | No | Supplier company name |

## 🚀 Advanced Use Cases

### 1. Vendor Performance Tracking
```python
def vendor_fba_performance(fba_df, ontime_df):
    # Join to get additional vendor metrics
    vendor_metrics = fba_df.groupby('Vendor').agg({
        'PO': 'count',
        'FBA Id': 'nunique',
        'Batch Id': 'nunique',
        'Timestamp': lambda x: (x.max() - x.min()).days
    }).rename(columns={
        'PO': 'total_pos',
        'FBA Id': 'unique_fba_shipments',
        'Batch Id': 'unique_batches',
        'Timestamp': 'active_days'
    })
    
    # Calculate notification frequency
    vendor_metrics['pos_per_batch'] = (
        vendor_metrics['total_pos'] / vendor_metrics['unique_batches']
    )
    
    return vendor_metrics.sort_values('total_pos', ascending=False)
```

### 2. Batch Optimization Analysis
```python
def batch_optimization_analysis(df):
    # Analyze batch composition
    batch_stats = df.groupby('Batch Id').agg({
        'Vendor': 'nunique',
        'PO': 'count',
        'Timestamp': lambda x: (x.max() - x.min()).total_seconds() / 60
    }).rename(columns={
        'Vendor': 'vendor_count',
        'PO': 'po_count',
        'Timestamp': 'processing_time_minutes'
    })
    
    # Identify optimization opportunities
    batch_stats['single_vendor_batch'] = batch_stats['vendor_count'] == 1
    batch_stats['efficiency_score'] = (
        batch_stats['po_count'] / (batch_stats['processing_time_minutes'] + 1)
    )
    
    return batch_stats
```

### 3. Notification Timeline Visualization
```python
import matplotlib.pyplot as plt

def plot_notification_timeline(df):
    # Prepare data
    df_sorted = df.sort_values('Timestamp')
    df_sorted['cumulative_count'] = range(1, len(df_sorted) + 1)
    
    # Create timeline plot
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 8))
    
    # Cumulative notifications
    ax1.plot(df_sorted['Timestamp'], df_sorted['cumulative_count'], marker='o')
    ax1.set_xlabel('Date')
    ax1.set_ylabel('Cumulative Notifications')
    ax1.set_title('FBA Notification Timeline')
    ax1.grid(True)
    
    # Notifications by vendor
    vendor_counts = df.groupby(['Timestamp', 'Vendor']).size().unstack(fill_value=0)
    vendor_counts.plot(kind='bar', stacked=True, ax=ax2)
    ax2.set_xlabel('Timestamp')
    ax2.set_ylabel('Notifications')
    ax2.set_title('Notifications by Vendor')
    
    plt.tight_layout()
    return fig
```

## ⚠️ Data Considerations

### Limitations
1. **Small Dataset**: Only 10 records - likely a sample or subset
2. **Limited Time Range**: Covers only September 2025
3. **No Status Tracking**: Doesn't indicate if vendors acknowledged or acted on notifications
4. **Missing Context**: No information about shipment contents or urgency

### Data Quality Checks
```python
def validate_fba_data(df):
    issues = []
    
    # Check for required fields
    if df[['Timestamp', 'Batch Id', 'PO', 'FBA Id', 'Vendor']].isnull().any().any():
        issues.append("Missing required fields detected")
    
    # Check for duplicates
    if df.duplicated(subset=['PO']).any():
        issues.append("Duplicate PO numbers found")
    
    if df.duplicated(subset=['FBA Id']).any():
        issues.append("Duplicate FBA IDs found")
    
    # Check timestamp sequence
    if not df['Timestamp'].is_monotonic_increasing:
        issues.append("Timestamps are not in chronological order")
    
    # Check format compliance
    if not df['PO'].str.match(r'^PO\d{6}$').all():
        issues.append("Invalid PO format detected")
    
    if not df['Batch Id'].str.match(r'^BATCH\d{7}$').all():
        issues.append("Invalid Batch ID format detected")
    
    return issues if issues else ["All validation checks passed"]

# Run validation
validation_results = validate_fba_data(df)
print("Data Validation Results:")
for result in validation_results:
    print(f"  • {result}")
```

## 💡 Best Practices

1. **Always Parse Timestamps**: Convert Timestamp column to datetime before analysis
2. **Validate Format Patterns**: Check PO, FBA ID, and Batch ID formats match expected patterns
3. **Join Carefully**: When joining with OnTime_Data, be aware of potential many-to-many relationships
4. **Consider Time Zones**: Timestamps may be in UTC - adjust for local analysis if needed
5. **Track Notification Success**: Consider adding fields for delivery confirmation or vendor acknowledgment

## 📚 Related Tables

- **OnTime_Data.csv**: Main procurement dataset with detailed PO information
- **Potential Extensions**: 
  - Vendor response tracking
  - FBA receiving confirmation
  - Shipment problem logs
  - Performance metrics

## Sample Data
| Timestamp | Batch Id | PO | FBA Id | Vendor |
|-----------|----------|-----|---------|---------|
| 2025-09-03T11:14:32.460Z | BATCH0010572 | PO375435 | FBA190K4N93X | Quanzhou Jiasheng Wujin Sujiao Co.,Ltd. |
| 2025-09-03T11:14:38.604Z | BATCH0010571 | PO374371 | FBA190K536CY | GHTLINK (HK) International Trading Limited |
| 2025-09-03T11:14:45.867Z | BATCH0010569 | PO374007 | FBA190K4R1Z6 | YOLINK FASTENER (JIAXING) CO., LTD |
| 2025-09-03T11:14:54.518Z | BATCH0010562 | PO374224 | FBA190H27C0V | SHANGHAI XIYUAN IMP. & EXP. CO.,LTD |
| 2025-09-03T11:15:02.179Z | BATCH0010561 | PO375299 | FBA190GYKBGW | UNISOURCE I.T.CO.,LIMITED |

---
*This documentation is based on a sample of 10 records from the fba_emailer.csv file. The actual production dataset may contain additional records and patterns.*