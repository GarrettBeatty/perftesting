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


## WINDOWS Platform Results

| Test Type | File Size | Storage | Regular (Gb/s) | WithResp (Gb/s) | Difference | Faster API |
|-----------|-----------|---------|----------------|-----------------|------------|------------|
| download-30GiB ram | 30.0GiB | RAM | 0.74 | 20.71 | 96.4% | WithResponse |
| download-30GiB | 30.0GiB | Disk | 0.79 | 0.55 | 43.7% | Regular |
| download-5GiB ram | 5.0GiB | RAM | 0.80 | 29.37 | 97.3% | WithResponse |
| download-5GiB | 5.0GiB | Disk | 0.80 | 0.56 | 41.9% | Regular |

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
| **Throughput (Gb/s)** | 0.79 | 0.55 | 1.44x |
| **Average Time (s)** | 326.5 | 469.1 | 1.44x |

#### Statistical Details

| Statistic | Regular APIs | WithResponse APIs |
|-----------|--------------|-------------------|
| **Min Time (s)** | 322.23 | 460.61 |
| **Max Time (s)** | 343.75 | 474.05 |
| **Std Dev Time** | 8.90 | 4.14 |
| **Min Throughput (Gb/s)** | 0.75 | 0.54 |
| **Max Throughput (Gb/s)** | 0.80 | 0.56 |
| **Std Dev Throughput** | 0.02 | 0.00 |

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
| **Throughput (Gb/s)** | 0.80 | 0.56 | 1.42x |
| **Average Time (s)** | 53.9 | 76.6 | 1.42x |

#### Statistical Details

| Statistic | Regular APIs | WithResponse APIs |
|-----------|--------------|-------------------|
| **Min Time (s)** | 53.79 | 70.79 |
| **Max Time (s)** | 54.14 | 82.46 |
| **Std Dev Time** | 0.10 | 3.34 |
| **Min Throughput (Gb/s)** | 0.79 | 0.52 |
| **Max Throughput (Gb/s)** | 0.80 | 0.61 |
| **Std Dev Throughput** | 0.00 | 0.02 |

