# Booking Pickup Form Data Documentation

## Auto-Generated Overview
- **File**: bookingpickup_form 1.csv
- **Columns**: Timestamp, Batch Id, Supplier, SM, Form Type
- **Last Modified**: 2025-09-24
- **Date Range**: August 1, 2025 to September 24, 2025

## Column Information with Business Meanings

### ⏰ **Timestamp**
- **Description**: Date and time when the booking or pickup form was submitted
- **Format**: ISO 8601 datetime (e.g., "2025-05-29T20:07:05.000Z")
- **Business Context**: Tracks when supply managers submitted logistics forms for batch shipments
- **Unique Values**: 1,619 (one per row - no duplicates)
- **Data Quality**: 100% complete (no nulls)

### 📦 **Batch Id**
- **Description**: Unique identifier for a shipment batch
- **Format**: "BATCH" + 7-digit number (e.g., "BATCH0009223")
- **Business Context**: Groups multiple purchase orders for consolidated shipping
- **Unique Values**: 1,463 unique batches
- **Duplicate Rate**: ~10% (57 duplicate batch-supplier combinations)
- **Sample Values**: BATCH0009223, BATCH0009232, BATCH0009136

### 🏢 **Supplier**
- **Description**: Supplier/vendor company name
- **Format**: Company name with leading space (note: data has leading spaces)
- **Business Context**: The vendor responsible for providing goods in the batch
- **Unique Values**: 347 unique suppliers
- **Missing Values**: 6 records (99.6% complete)
- **Top Suppliers**: Fuzhou Sino Trading Co., Ltd., YOLINK FASTENER, Verslo Linija UAB

### 👤 **SM (Supply Manager)**
- **Description**: Name of the supply manager handling the batch
- **Format**: Full name (First Last format)
- **Business Context**: The supply chain manager responsible for coordinating the shipment
- **Unique Values**: 15 different supply managers
- **Missing Values**: 7 records (99.6% complete)
- **Top SMs**: 
  - Vivian Gao (246 forms)
  - Teresa Xiong (172 forms)
  - Lemon Shen (159 forms)

### 📋 **Form Type**
- **Description**: Type of logistics form submitted
- **Format**: Text field with two possible values
- **Business Context**: Indicates the stage of shipment coordination
- **Values**: 
  - **Booking Form** (98.6% - 1,596 records): Initial freight booking request
  - **Pickup Form** (1.1% - 17 records): Cargo pickup scheduling
- **Missing Values**: 6 records (99.6% complete)

## Dataset Structure

### What This Dataset Contains
This is a **logistics form submission log** tracking when supply managers submit booking and pickup forms for shipment batches. Each row represents a single form submission linking a batch to a supplier with SM oversight.

### Key Characteristics
- **Record Type**: Form submission log
- **Granularity**: One row per form submission
- **Time Span**: ~2 months (August-September 2025)
- **Primary Purpose**: Track logistics coordination activities between SMs and suppliers

## 🔍 Understanding the Data

### Business Process Flow
```
Batch Created
    ↓
Supply Manager Assigned
    ↓
Booking Form Submitted (98.6% of cases)
    ↓
[Optional] Pickup Form Submitted (1.1% of cases)
    ↓
Record Created in bookingpickup_form
```

### Key Relationships
- **SM to Supplier**: Many-to-many (one SM handles multiple suppliers, one supplier works with multiple SMs)
- **Batch to Forms**: Usually 1:1, but some batches have multiple forms (duplicates exist)
- **Form Type Progression**: Booking Form typically precedes Pickup Form

## 📊 Quick Start: Loading and Analyzing the Data

### Python/Pandas Example
```python
import pandas as pd
from datetime import datetime

# Load the booking/pickup form data
df = pd.read_csv('bookingpickup_form 1.csv')

# Parse timestamp column
df['Timestamp'] = pd.to_datetime(df['Timestamp'])

# Clean supplier names (remove leading spaces)
df['Supplier'] = df['Supplier'].str.strip()

# Basic inspection
print(f"Dataset shape: {df.shape}")
print(f"Date range: {df['Timestamp'].min()} to {df['Timestamp'].max()}")
print(f"\nForm Type distribution:")
print(df['Form Type'].value_counts())
print(f"\nTop 5 Supply Managers:")
print(df['SM'].value_counts().head())

# View first few rows
df.head()
```

### Data Quality Checks
```python
# Check for missing values
null_summary = df.isnull().sum()
print("Missing Values:")
print(null_summary[null_summary > 0])

# Check for duplicates
duplicate_batches = df[df.duplicated(subset=['Batch Id', 'Supplier'], keep=False)]
print(f"\nDuplicate Batch-Supplier combinations: {len(duplicate_batches)}")

# Verify batch ID format
batch_pattern = r'^BATCH\d{7}$'
df['batch_format_valid'] = df['Batch Id'].str.match(batch_pattern)
print(f"\nValid Batch ID format: {df['batch_format_valid'].sum()}/{len(df)}")

# Check for leading/trailing spaces in text fields
df['supplier_has_spaces'] = df['Supplier'].str.contains(r'^\s|\s$', na=False)
print(f"Suppliers with leading/trailing spaces: {df['supplier_has_spaces'].sum()}")
```

## 📈 Analysis Examples

### 1. Supply Manager Workload Analysis
```python
# SM workload distribution
sm_workload = df.groupby('SM').agg({
    'Batch Id': 'count',
    'Supplier': 'nunique',
    'Timestamp': ['min', 'max'],
    'Form Type': lambda x: (x == 'Pickup Form').sum()
}).round(2)

sm_workload.columns = ['Total_Forms', 'Unique_Suppliers', 'First_Form', 'Last_Form', 'Pickup_Forms']
sm_workload['Booking_Forms'] = sm_workload['Total_Forms'] - sm_workload['Pickup_Forms']
sm_workload['Active_Days'] = (sm_workload['Last_Form'] - sm_workload['First_Form']).dt.days

# Calculate average forms per day
sm_workload['Forms_Per_Day'] = sm_workload['Total_Forms'] / (sm_workload['Active_Days'] + 1)
sm_workload = sm_workload.sort_values('Total_Forms', ascending=False)

print("Supply Manager Workload Analysis:")
print(sm_workload.head(10))
```

### 2. Supplier Activity Patterns
```python
# Supplier analysis
supplier_analysis = df.groupby('Supplier').agg({
    'Batch Id': 'nunique',
    'SM': lambda x: ', '.join(x.dropna().unique()),
    'Form Type': lambda x: dict(x.value_counts()),
    'Timestamp': ['min', 'max']
}).round(2)

supplier_analysis.columns = ['Unique_Batches', 'Supply_Managers', 'Form_Types', 'First_Activity', 'Last_Activity']

# Top suppliers by batch count
top_suppliers = supplier_analysis.sort_values('Unique_Batches', ascending=False).head(10)
print("Top 10 Most Active Suppliers:")
print(top_suppliers[['Unique_Batches', 'Supply_Managers']])
```

### 3. Daily Submission Patterns
```python
# Extract time components
df['date'] = df['Timestamp'].dt.date
df['hour'] = df['Timestamp'].dt.hour
df['day_of_week'] = df['Timestamp'].dt.day_name()
df['week'] = df['Timestamp'].dt.isocalendar().week

# Daily submission volume
daily_volume = df.groupby('date').agg({
    'Batch Id': 'count',
    'SM': 'nunique',
    'Form Type': lambda x: (x == 'Booking Form').sum()
}).rename(columns={
    'Batch Id': 'Total_Forms',
    'SM': 'Active_SMs',
    'Form Type': 'Booking_Forms'
})

# Peak submission times
hourly_dist = df.groupby('hour')['Batch Id'].count()
peak_hours = hourly_dist.nlargest(5)
print("Peak Submission Hours:")
print(peak_hours)

# Day of week pattern
dow_pattern = df.groupby('day_of_week')['Batch Id'].count()
print("\nSubmissions by Day of Week:")
print(dow_pattern.sort_values(ascending=False))
```

### 4. Batch Processing Efficiency
```python
# Analyze batch processing patterns
batch_analysis = df.groupby('Batch Id').agg({
    'Supplier': 'first',
    'SM': 'first',
    'Form Type': list,
    'Timestamp': ['min', 'max']
})

batch_analysis.columns = ['Supplier', 'SM', 'Form_Types', 'First_Form', 'Last_Form']

# Identify batches with multiple forms
batch_analysis['Form_Count'] = batch_analysis['Form_Types'].apply(len)
batch_analysis['Has_Pickup'] = batch_analysis['Form_Types'].apply(lambda x: 'Pickup Form' in x)
batch_analysis['Processing_Time'] = (batch_analysis['Last_Form'] - batch_analysis['First_Form']).dt.total_seconds() / 3600

# Batches with both booking and pickup
complete_batches = batch_analysis[batch_analysis['Has_Pickup']]
print(f"Batches with Pickup Forms: {len(complete_batches)} ({len(complete_batches)/len(batch_analysis)*100:.1f}%)")

# Average time between booking and pickup
if len(complete_batches) > 0:
    avg_processing = complete_batches['Processing_Time'].mean()
    print(f"Average time between forms: {avg_processing:.2f} hours")
```

### 5. SM-Supplier Relationship Matrix
```python
# Create SM-Supplier interaction matrix
sm_supplier_matrix = pd.crosstab(df['SM'], df['Supplier'])

# Find exclusive relationships
exclusive_suppliers = []
for supplier in sm_supplier_matrix.columns:
    sm_count = (sm_supplier_matrix[supplier] > 0).sum()
    if sm_count == 1:
        sm_name = sm_supplier_matrix[sm_supplier_matrix[supplier] > 0].index[0]
        exclusive_suppliers.append({'Supplier': supplier, 'Exclusive_SM': sm_name})

exclusive_df = pd.DataFrame(exclusive_suppliers)
print(f"Suppliers with exclusive SM relationships: {len(exclusive_df)}")
print(exclusive_df.head(10))

# SM collaboration patterns
sm_overlap = pd.DataFrame(index=sm_supplier_matrix.index, columns=sm_supplier_matrix.index)
for sm1 in sm_supplier_matrix.index:
    for sm2 in sm_supplier_matrix.index:
        if sm1 != sm2:
            shared = ((sm_supplier_matrix.loc[sm1] > 0) & (sm_supplier_matrix.loc[sm2] > 0)).sum()
            sm_overlap.loc[sm1, sm2] = shared

print("\nSM Collaboration (Shared Suppliers):")
print(sm_overlap.fillna(0).astype(int))
```

## 🔗 Integration with Other Datasets

### Join with OnTime_Data.csv
```python
# Load OnTime data
ontime_df = pd.read_csv('OnTime_Data.csv')

# Join on batch ID
merged_df = df.merge(
    ontime_df[['batch_id', 'po_number', 'vendor_name', 'po_value', 'actual_shipping_date']],
    left_on='Batch Id',
    right_on='batch_id',
    how='left'
)

# Analyze forms with shipping data
if 'actual_shipping_date' in merged_df.columns:
    merged_df['actual_shipping_date'] = pd.to_datetime(merged_df['actual_shipping_date'])
    merged_df['form_to_ship_days'] = (merged_df['actual_shipping_date'] - merged_df['Timestamp']).dt.days
    
    print("Form Submission to Shipping Analysis:")
    print(f"Average days from form to shipping: {merged_df['form_to_ship_days'].mean():.1f}")
    print(f"Forms with shipping data: {merged_df['actual_shipping_date'].notna().sum()}")
```

### Join with FBA Emailer Data
```python
# Load FBA emailer data
fba_df = pd.read_csv('fba_emailer.csv')

# Join on batch ID
fba_merged = df.merge(
    fba_df[['Batch Id', 'FBA Id', 'PO']],
    on='Batch Id',
    how='left'
)

# Analyze FBA assignments
fba_coverage = fba_merged['FBA Id'].notna().sum()
print(f"Forms with FBA assignments: {fba_coverage} ({fba_coverage/len(df)*100:.1f}%)")
```

## 📋 Data Dictionary

| Field | Data Type | Format | Nullable | Description |
|-------|-----------|--------|----------|-------------|
| **Timestamp** | DateTime | ISO 8601 | No | Form submission timestamp |
| **Batch Id** | String | BATCH{7 digits} | No | Shipment batch identifier |
| **Supplier** | String | Free text | Yes (0.4%) | Vendor company name (may have leading spaces) |
| **SM** | String | Full name | Yes (0.4%) | Supply Manager name |
| **Form Type** | String | Enum | Yes (0.4%) | "Booking Form" or "Pickup Form" |

## 🚀 Advanced Analysis

### 1. Time Series Forecasting
```python
# Prepare time series data
daily_forms = df.groupby(df['Timestamp'].dt.date).size()
daily_forms.index = pd.to_datetime(daily_forms.index)

# Calculate moving averages
ma_7 = daily_forms.rolling(window=7).mean()
ma_30 = daily_forms.rolling(window=30).mean()

# Trend analysis
from scipy import stats
x = range(len(daily_forms))
y = daily_forms.values
slope, intercept, r_value, p_value, std_err = stats.linregress(x, y)

print(f"Daily form submission trend:")
print(f"  - Slope: {slope:.2f} forms/day")
print(f"  - R-squared: {r_value**2:.3f}")
print(f"  - Trend: {'Increasing' if slope > 0 else 'Decreasing'}")
```

### 2. Supply Manager Performance Metrics
```python
def calculate_sm_metrics(df):
    metrics = []
    
    for sm in df['SM'].dropna().unique():
        sm_data = df[df['SM'] == sm]
        
        # Calculate metrics
        total_forms = len(sm_data)
        unique_suppliers = sm_data['Supplier'].nunique()
        unique_batches = sm_data['Batch Id'].nunique()
        
        # Time-based metrics
        active_days = (sm_data['Timestamp'].max() - sm_data['Timestamp'].min()).days + 1
        forms_per_day = total_forms / active_days
        
        # Form type distribution
        booking_forms = (sm_data['Form Type'] == 'Booking Form').sum()
        pickup_forms = (sm_data['Form Type'] == 'Pickup Form').sum()
        pickup_rate = pickup_forms / total_forms if total_forms > 0 else 0
        
        # Consistency metrics
        daily_counts = sm_data.groupby(sm_data['Timestamp'].dt.date).size()
        consistency_score = daily_counts.std() / daily_counts.mean() if len(daily_counts) > 1 else 0
        
        metrics.append({
            'SM': sm,
            'Total_Forms': total_forms,
            'Unique_Suppliers': unique_suppliers,
            'Unique_Batches': unique_batches,
            'Active_Days': active_days,
            'Forms_Per_Day': round(forms_per_day, 2),
            'Pickup_Rate': round(pickup_rate * 100, 1),
            'Consistency_Score': round(consistency_score, 2)
        })
    
    return pd.DataFrame(metrics).sort_values('Total_Forms', ascending=False)

sm_metrics = calculate_sm_metrics(df)
print("Supply Manager Performance Metrics:")
print(sm_metrics.head(10))
```

### 3. Batch Lifecycle Analysis
```python
# Track batch progression through forms
batch_lifecycle = df.sort_values('Timestamp').groupby('Batch Id').agg({
    'Form Type': lambda x: ' → '.join(x),
    'Timestamp': ['first', 'last'],
    'SM': 'first',
    'Supplier': 'first'
})

batch_lifecycle.columns = ['Form_Progression', 'First_Form_Time', 'Last_Form_Time', 'SM', 'Supplier']
batch_lifecycle['Lifecycle_Hours'] = (
    (batch_lifecycle['Last_Form_Time'] - batch_lifecycle['First_Form_Time']).dt.total_seconds() / 3600
)

# Categorize batch types
def categorize_batch(progression):
    if 'Pickup Form' in progression and 'Booking Form' in progression:
        return 'Complete'
    elif 'Pickup Form' in progression:
        return 'Pickup_Only'
    elif 'Booking Form' in progression:
        return 'Booking_Only'
    else:
        return 'Unknown'

batch_lifecycle['Batch_Type'] = batch_lifecycle['Form_Progression'].apply(categorize_batch)

# Summary statistics
batch_type_summary = batch_lifecycle['Batch_Type'].value_counts()
print("Batch Lifecycle Categories:")
print(batch_type_summary)
print(f"\nAverage lifecycle duration by type:")
for batch_type in batch_lifecycle['Batch_Type'].unique():
    avg_duration = batch_lifecycle[batch_lifecycle['Batch_Type'] == batch_type]['Lifecycle_Hours'].mean()
    print(f"  - {batch_type}: {avg_duration:.2f} hours")
```

## ⚠️ Data Quality Considerations

### Known Issues
1. **Leading Spaces**: Supplier names have leading spaces that need trimming
2. **Duplicate Entries**: 57 batch-supplier combinations appear multiple times
3. **Missing Values**: ~0.4% of records have missing Supplier, SM, or Form Type
4. **Form Type Imbalance**: Heavy skew towards Booking Forms (98.6%)

### Data Validation Script
```python
def validate_booking_data(df):
    issues = []
    
    # Check timestamp validity
    if df['Timestamp'].isnull().any():
        issues.append(f"Missing timestamps: {df['Timestamp'].isnull().sum()}")
    
    # Check batch ID format
    invalid_batches = ~df['Batch Id'].str.match(r'^BATCH\d{7}$', na=False)
    if invalid_batches.any():
        issues.append(f"Invalid batch ID format: {invalid_batches.sum()}")
    
    # Check for leading/trailing spaces
    if df['Supplier'].str.contains(r'^\s|\s$', na=False).any():
        issues.append("Supplier names contain leading/trailing spaces")
    
    # Check form type values
    valid_forms = ['Booking Form', 'Pickup Form']
    invalid_forms = ~df['Form Type'].isin(valid_forms)
    if invalid_forms.any():
        invalid_values = df.loc[invalid_forms, 'Form Type'].unique()
        issues.append(f"Invalid form types: {invalid_values}")
    
    # Check for duplicates
    duplicates = df.duplicated(subset=['Batch Id', 'Supplier', 'Timestamp'], keep=False)
    if duplicates.any():
        issues.append(f"Duplicate entries: {duplicates.sum()}")
    
    return issues if issues else ["All validation checks passed"]

validation_results = validate_booking_data(df)
print("Data Validation Results:")
for result in validation_results:
    print(f"  • {result}")
```

## 💡 Best Practices

1. **Always Clean Supplier Names**: Strip leading/trailing spaces before analysis
2. **Handle Missing Values**: Check for nulls in SM and Supplier fields
3. **Consider Form Type Imbalance**: Most analysis will be on Booking Forms
4. **Parse Timestamps Properly**: Convert to datetime for time-based analysis
5. **Track Duplicates**: Some batch-supplier combinations appear multiple times
6. **Join Carefully**: Use Batch Id as primary key when joining with other datasets

## 📊 Key Performance Indicators (KPIs)

```python
# Calculate key metrics
kpis = {
    'Total Forms Submitted': len(df),
    'Unique Batches': df['Batch Id'].nunique(),
    'Unique Suppliers': df['Supplier'].nunique(),
    'Active Supply Managers': df['SM'].nunique(),
    'Pickup Form Rate': f"{(df['Form Type'] == 'Pickup Form').sum() / len(df) * 100:.1f}%",
    'Average Forms per SM': round(len(df) / df['SM'].nunique(), 1),
    'Average Batches per Supplier': round(df['Batch Id'].nunique() / df['Supplier'].nunique(), 1),
    'Data Completeness': f"{(1 - df.isnull().sum().sum() / (len(df) * len(df.columns))) * 100:.1f}%"
}

kpi_df = pd.DataFrame(list(kpis.items()), columns=['Metric', 'Value'])
print("Key Performance Indicators:")
print(kpi_df)
```

## 📚 Related Documentation

- **OnTime_Data.csv**: Main procurement dataset - join on batch_id
- **fba_emailer.csv**: FBA notifications - join on Batch Id
- **Integration Points**:
  - Batch Id links across all three datasets
  - Supplier/Vendor names for matching (requires cleaning)
  - Timestamp for temporal analysis

---
*This documentation covers the bookingpickup_form 1.csv dataset containing 1,619 logistics form submissions from August to September 2025.*