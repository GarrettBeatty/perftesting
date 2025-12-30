# Performance Analysis Report

This report compares Regular APIs vs WithResponse APIs download performance across different platforms.

## LINUX Platform Results

| Test Type | File Size | Storage | Regular (Gb/s) | WithResp (Gb/s) | Difference | Faster API |
|-----------|-----------|---------|----------------|-----------------|------------|------------|
| download-30GiB ram | 30.0GiB | RAM | 0.80 | 11.78 | 93.2% | WithResponse |
| download-30GiB | 30.0GiB | Disk | 0.79 | 11.82 | 93.3% | WithResponse |
| download-5GiB ram | 5.0GiB | RAM | 0.80 | 16.25 | 95.1% | WithResponse |
| download-5GiB | 5.0GiB | Disk | 0.79 | 12.25 | 93.6% | WithResponse |

## Detailed Performance Breakdown - LINUX

### 30.0GiB Download to RAM

| Metric | Regular APIs | WithResponse APIs | Comparison |
|--------|--------------|-------------------|------------|
| **Throughput (Gb/s)** | 0.80 | 11.78 | 0.07x |
| **Average Time (s)** | 322.2 | 22.1 | 0.07x |

#### Statistical Details

| Statistic | Regular APIs | WithResponse APIs |
|-----------|--------------|-------------------|
| **Min Time (s)** | 322.13 | 19.11 |
| **Max Time (s)** | 322.48 | 26.62 |
| **Std Dev Time** | 0.13 | 2.66 |
| **Min Throughput (Gb/s)** | 0.80 | 9.68 |
| **Max Throughput (Gb/s)** | 0.80 | 13.49 |
| **Std Dev Throughput** | 0.00 | 1.36 |

### 30.0GiB Download to Disk

| Metric | Regular APIs | WithResponse APIs | Comparison |
|--------|--------------|-------------------|------------|
| **Throughput (Gb/s)** | 0.79 | 11.82 | 0.07x |
| **Average Time (s)** | 327.5 | 21.8 | 0.07x |

#### Statistical Details

| Statistic | Regular APIs | WithResponse APIs |
|-----------|--------------|-------------------|
| **Min Time (s)** | 322.23 | 21.51 |
| **Max Time (s)** | 358.91 | 22.54 |
| **Std Dev Time** | 11.32 | 0.29 |
| **Min Throughput (Gb/s)** | 0.72 | 11.43 |
| **Max Throughput (Gb/s)** | 0.80 | 11.98 |
| **Std Dev Throughput** | 0.03 | 0.15 |

### 5.0GiB Download to RAM

| Metric | Regular APIs | WithResponse APIs | Comparison |
|--------|--------------|-------------------|------------|
| **Throughput (Gb/s)** | 0.80 | 16.25 | 0.05x |
| **Average Time (s)** | 53.7 | 2.9 | 0.05x |

#### Statistical Details

| Statistic | Regular APIs | WithResponse APIs |
|-----------|--------------|-------------------|
| **Min Time (s)** | 53.69 | 1.96 |
| **Max Time (s)** | 53.93 | 5.55 |
| **Std Dev Time** | 0.07 | 1.06 |
| **Min Throughput (Gb/s)** | 0.80 | 7.75 |
| **Max Throughput (Gb/s)** | 0.80 | 21.95 |
| **Std Dev Throughput** | 0.00 | 4.25 |

### 5.0GiB Download to Disk

| Metric | Regular APIs | WithResponse APIs | Comparison |
|--------|--------------|-------------------|------------|
| **Throughput (Gb/s)** | 0.79 | 12.25 | 0.06x |
| **Average Time (s)** | 54.4 | 3.5 | 0.06x |

#### Statistical Details

| Statistic | Regular APIs | WithResponse APIs |
|-----------|--------------|-------------------|
| **Min Time (s)** | 53.79 | 3.37 |
| **Max Time (s)** | 60.24 | 4.64 |
| **Std Dev Time** | 2.04 | 0.39 |
| **Min Throughput (Gb/s)** | 0.71 | 9.26 |
| **Max Throughput (Gb/s)** | 0.80 | 12.74 |
| **Std Dev Throughput** | 0.03 | 1.05 |


## NETCORE Platform Results

| Test Type | File Size | Storage | Regular (Gb/s) | WithResp (Gb/s) | Difference | Faster API |
|-----------|-----------|---------|----------------|-----------------|------------|------------|
| download-30GiB ram | 30.0GiB | RAM | 0.78 | 3.90 | 80.0% | WithResponse |
| download-30GiB | 30.0GiB | Disk | 0.75 | 0.57 | 31.1% | Regular |
| download-5GiB ram | 5.0GiB | RAM | 0.80 | 4.35 | 81.7% | WithResponse |
| download-5GiB | 5.0GiB | Disk | 0.74 | 0.62 | 20.9% | Regular |

## Detailed Performance Breakdown - NETCORE

### 30.0GiB Download to RAM

| Metric | Regular APIs | WithResponse APIs | Comparison |
|--------|--------------|-------------------|------------|
| **Throughput (Gb/s)** | 0.78 | 3.90 | 0.20x |
| **Average Time (s)** | 329.5 | 66.0 | 0.20x |

#### Statistical Details

| Statistic | Regular APIs | WithResponse APIs |
|-----------|--------------|-------------------|
| **Min Time (s)** | 322.13 | 64.23 |
| **Max Time (s)** | 352.06 | 66.92 |
| **Std Dev Time** | 10.51 | 0.82 |
| **Min Throughput (Gb/s)** | 0.73 | 3.85 |
| **Max Throughput (Gb/s)** | 0.80 | 4.01 |
| **Std Dev Throughput** | 0.02 | 0.05 |

### 30.0GiB Download to Disk

| Metric | Regular APIs | WithResponse APIs | Comparison |
|--------|--------------|-------------------|------------|
| **Throughput (Gb/s)** | 0.75 | 0.57 | 1.31x |
| **Average Time (s)** | 347.1 | 452.5 | 1.30x |

#### Statistical Details

| Statistic | Regular APIs | WithResponse APIs |
|-----------|--------------|-------------------|
| **Min Time (s)** | 322.26 | 443.20 |
| **Max Time (s)** | 403.80 | 461.89 |
| **Std Dev Time** | 28.97 | 13.22 |
| **Min Throughput (Gb/s)** | 0.64 | 0.56 |
| **Max Throughput (Gb/s)** | 0.80 | 0.58 |
| **Std Dev Throughput** | 0.06 | 0.02 |

### 5.0GiB Download to RAM

| Metric | Regular APIs | WithResponse APIs | Comparison |
|--------|--------------|-------------------|------------|
| **Throughput (Gb/s)** | 0.80 | 4.35 | 0.18x |
| **Average Time (s)** | 53.8 | 9.9 | 0.18x |

#### Statistical Details

| Statistic | Regular APIs | WithResponse APIs |
|-----------|--------------|-------------------|
| **Min Time (s)** | 53.69 | 8.91 |
| **Max Time (s)** | 54.17 | 11.27 |
| **Std Dev Time** | 0.20 | 0.68 |
| **Min Throughput (Gb/s)** | 0.79 | 3.81 |
| **Max Throughput (Gb/s)** | 0.80 | 4.82 |
| **Std Dev Throughput** | 0.00 | 0.29 |

### 5.0GiB Download to Disk

| Metric | Regular APIs | WithResponse APIs | Comparison |
|--------|--------------|-------------------|------------|
| **Throughput (Gb/s)** | 0.74 | 0.62 | 1.21x |
| **Average Time (s)** | 58.3 | 69.8 | 1.20x |

#### Statistical Details

| Statistic | Regular APIs | WithResponse APIs |
|-----------|--------------|-------------------|
| **Min Time (s)** | 53.80 | 69.01 |
| **Max Time (s)** | 72.75 | 70.56 |
| **Std Dev Time** | 6.10 | 0.58 |
| **Min Throughput (Gb/s)** | 0.59 | 0.61 |
| **Max Throughput (Gb/s)** | 0.80 | 0.62 |
| **Std Dev Throughput** | 0.07 | 0.01 |


## WINDOWS Platform Results

| Test Type | File Size | Storage | Regular (Gb/s) | WithResp (Gb/s) | Difference | Faster API |
|-----------|-----------|---------|----------------|-----------------|------------|------------|
| download-30GiB ram | 30.0GiB | RAM | 0.74 | 20.71 | 96.4% | WithResponse |
| download-30GiB | 30.0GiB | Disk | 0.77 | 4.63 | 83.4% | WithResponse |
| download-5GiB ram | 5.0GiB | RAM | 0.80 | 29.37 | 97.3% | WithResponse |
| download-5GiB | 5.0GiB | Disk | 0.80 | 4.69 | 83.0% | WithResponse |

## Detailed Performance Breakdown - WINDOWS

### 30.0GiB Download to RAM

| Metric | Regular APIs | WithResponse APIs | Comparison |
|--------|--------------|-------------------|------------|
| **Throughput (Gb/s)** | 0.74 | 20.71 | 0.04x |
| **Average Time (s)** | 347.2 | 12.6 | 0.04x |

#### Statistical Details

| Statistic | Regular APIs | WithResponse APIs |
|-----------|--------------|-------------------|
| **Min Time (s)** | 322.14 | 10.97 |
| **Max Time (s)** | 377.91 | 15.96 |
| **Std Dev Time** | 22.56 | 1.38 |
| **Min Throughput (Gb/s)** | 0.68 | 16.15 |
| **Max Throughput (Gb/s)** | 0.80 | 23.48 |
| **Std Dev Throughput** | 0.05 | 2.01 |

### 30.0GiB Download to Disk

| Metric | Regular APIs | WithResponse APIs | Comparison |
|--------|--------------|-------------------|------------|
| **Throughput (Gb/s)** | 0.77 | 4.63 | 0.17x |
| **Average Time (s)** | 336.9 | 55.7 | 0.17x |

#### Statistical Details

| Statistic | Regular APIs | WithResponse APIs |
|-----------|--------------|-------------------|
| **Min Time (s)** | 322.29 | 53.06 |
| **Max Time (s)** | 355.31 | 57.18 |
| **Std Dev Time** | 16.41 | 1.87 |
| **Min Throughput (Gb/s)** | 0.73 | 4.51 |
| **Max Throughput (Gb/s)** | 0.80 | 4.86 |
| **Std Dev Throughput** | 0.04 | 0.16 |

### 5.0GiB Download to RAM

| Metric | Regular APIs | WithResponse APIs | Comparison |
|--------|--------------|-------------------|------------|
| **Throughput (Gb/s)** | 0.80 | 29.37 | 0.03x |
| **Average Time (s)** | 53.7 | 1.6 | 0.03x |

#### Statistical Details

| Statistic | Regular APIs | WithResponse APIs |
|-----------|--------------|-------------------|
| **Min Time (s)** | 53.69 | 1.27 |
| **Max Time (s)** | 53.89 | 2.91 |
| **Std Dev Time** | 0.06 | 0.51 |
| **Min Throughput (Gb/s)** | 0.80 | 14.75 |
| **Max Throughput (Gb/s)** | 0.80 | 33.72 |
| **Std Dev Throughput** | 0.00 | 6.10 |

### 5.0GiB Download to Disk

| Metric | Regular APIs | WithResponse APIs | Comparison |
|--------|--------------|-------------------|------------|
| **Throughput (Gb/s)** | 0.80 | 4.69 | 0.17x |
| **Average Time (s)** | 53.8 | 9.3 | 0.17x |

#### Statistical Details

| Statistic | Regular APIs | WithResponse APIs |
|-----------|--------------|-------------------|
| **Min Time (s)** | 53.79 | 7.74 |
| **Max Time (s)** | 54.01 | 10.14 |
| **Std Dev Time** | 0.07 | 0.93 |
| **Min Throughput (Gb/s)** | 0.80 | 4.24 |
| **Max Throughput (Gb/s)** | 0.80 | 5.55 |
| **Std Dev Throughput** | 0.00 | 0.50 |

