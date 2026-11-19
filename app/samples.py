from typing import Dict

SAMPLE_INVOICES: Dict[str, str] = {
    "clean_software_invoice": """
INVOICE: INV-2024-8841
Date: 2024-11-10
Due Date: 2024-12-10

FROM:
NexSphere Cloud Technologies Inc.
Tax ID: US-EIN-8849102
Email: billing@nexsphere.io
Address: 400 Innovation Way, Austin, TX

BILL TO:
Quantum Financial Corp
Contact: accounts-payable@quantumfin.com

DESCRIPTION                          QTY    UNIT PRICE     TOTAL
Kubernetes Production Cluster Node     2       $1200.00   $2400.00
Managed PostgreSQL Replica Pool        1        $650.00    $650.00
Enterprise 24/7 SLA Support Tier       1        $450.00    $450.00

-----------------------------------------------------------------
Subtotal: $3500.00
Tax (8%): $280.00
Shipping: $0.00
TOTAL AMOUNT DUE: $3780.00
""".strip(),

    "invoice_with_math_discrepancy": """
INVOICE: INV-FAIL-1044
Date: 2024-11-12
Due Date: 2024-12-12

FROM:
Legacy IT Contractors Ltd.
Tax ID: None
Email: invoices@legacyit.com

BILL TO:
Acme Logistics

DESCRIPTION                          QTY    UNIT PRICE     TOTAL
Server Rack Maintenance               3        $300.00    $900.00
Network Switch Diagnostics            2        $250.00    $400.00

-----------------------------------------------------------------
Subtotal: $1500.00
Tax: $120.00
TOTAL AMOUNT DUE: $1750.00
""".strip(),

    "cloud_infrastructure_bill": """
INVOICE: INV-AWS-9021
Date: 2024-11-01
Due Date: 2024-11-20

FROM:
Amazon Web Services Partner Cloud
Tax ID: US-WA-98109-AWS
Email: aws-invoices@cloudhost.net

BILL TO:
DataStream Analytics Lab

DESCRIPTION                          QTY    UNIT PRICE     TOTAL
EC2 Compute Instances c6i.2xlarge      4        $280.00   $1120.00
S3 Multi-Region Data Lake Storage     10         $45.00    $450.00
CloudFront Global CDN Data Transfer    1        $180.00    $180.00

-----------------------------------------------------------------
Subtotal: $1750.00
Tax: $140.00
TOTAL AMOUNT DUE: $1890.00
""".strip()
}

