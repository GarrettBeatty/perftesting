# Performance Analysis Report

This report compares Regular APIs vs WithResponse APIs download performance across different platforms.

## Executive Overview - Cross-Platform Comparison

### Summary Table - All Platforms

| Platform | File Size | Storage | Regular (Gb/s) | WithResp (Gb/s) | Difference | Faster API |
|----------|-----------|---------|----------------|-----------------|------------|------------|
| linux_netstandard | 30.0GiB | RAM | 0.80 | 11.78 | 1373.5% | WithResponse |
| linux_netstandard | 30.0GiB | Disk | 0.79 | 11.82 | 1400.3% | WithResponse |
| linux_netstandard | 5.0GiB | RAM | 0.80 | 16.25 | 1932.0% | WithResponse |
| linux_netstandard | 5.0GiB | Disk | 0.79 | 12.25 | 1451.1% | WithResponse |
| windows_netframework | 100.0MiB | RAM | 0.77 | 4.08 | 427.9% | WithResponse |
| windows_netframework | 100.0MiB | Disk | 0.70 | 0.52 | 26.8% | Regular |
| windows_netframework | 1.0GiB | RAM | 0.80 | 4.86 | 509.8% | WithResponse |
| windows_netframework | 1.0GiB | Disk | 0.79 | 0.58 | 26.9% | Regular |
| windows_netframework | 30.0GiB | RAM | 0.80 | 4.03 | 404.2% | WithResponse |
| windows_netframework | 30.0GiB | Disk | 0.79 | 0.34 | 56.4% | Regular |
| windows_netframework | 5.0GiB | RAM | 0.79 | 4.41 | 459.0% | WithResponse |
| windows_netframework | 5.0GiB | Disk | 0.80 | 0.50 | 37.7% | Regular |
| windows_netstandard | 100.0MiB | RAM | 0.78 | 6.06 | 671.7% | WithResponse |
| windows_netstandard | 100.0MiB | Disk | 0.70 | 3.60 | 411.1% | WithResponse |
| windows_netstandard | 1.0GiB | RAM | 0.80 | 12.18 | 1426.1% | WithResponse |
| windows_netstandard | 1.0GiB | Disk | 0.79 | 8.27 | 952.9% | WithResponse |
| windows_netstandard | 30.0GiB | RAM | 0.80 | 19.88 | 2385.3% | WithResponse |
| windows_netstandard | 30.0GiB | Disk | 0.78 | 5.13 | 555.4% | WithResponse |
| windows_netstandard | 5.0GiB | RAM | 0.80 | 24.13 | 2917.9% | WithResponse |
| windows_netstandard | 5.0GiB | Disk | 0.79 | 5.83 | 641.1% | WithResponse |

### Key Insights

- **Total Test Scenarios:** 20
- **WithResponse API Wins:** 16 scenarios (80.0%)
- **Regular API Wins:** 4 scenarios (20.0%)

#### Platform-Specific Observations

**LINUX_NETSTANDARD:**
- WithResponse wins: 4/4 scenarios
- Regular wins: 0/4 scenarios
- Average WithResponse throughput: 13.02 Gb/s
- Average Regular throughput: 0.79 Gb/s

**WINDOWS_NETFRAMEWORK:**
- WithResponse wins: 4/8 scenarios
- Regular wins: 4/8 scenarios
- Average WithResponse throughput: 2.41 Gb/s
- Average Regular throughput: 0.78 Gb/s

**WINDOWS_NETSTANDARD:**
- WithResponse wins: 8/8 scenarios
- Regular wins: 0/8 scenarios
- Average WithResponse throughput: 10.63 Gb/s
- Average Regular throughput: 0.78 Gb/s

#### Storage Type Impact

**RAM Storage:**
- WithResponse wins: 10/10 scenarios (100.0%)

**Disk Storage:**
- WithResponse wins: 6/10 scenarios (60.0%)

---

## LINUX_NETSTANDARD Platform Results

| Test Type | File Size | Storage | Regular (Gb/s) | WithResp (Gb/s) | Difference | Faster API |
|-----------|-----------|---------|----------------|-----------------|------------|------------|
| download-30GiB ram | 30.0GiB | RAM | 0.80 | 11.78 | 1373.5% | WithResponse |
| download-30GiB | 30.0GiB | Disk | 0.79 | 11.82 | 1400.3% | WithResponse |
| download-5GiB ram | 5.0GiB | RAM | 0.80 | 16.25 | 1932.0% | WithResponse |
| download-5GiB | 5.0GiB | Disk | 0.79 | 12.25 | 1451.1% | WithResponse |

## Detailed Performance Breakdown - LINUX_NETSTANDARD

### 30.0GiB Download to RAM

| Metric | Regular APIs | WithResponse APIs | Comparison |
|--------|--------------|-------------------|------------|
| **Throughput (Gb/s)** | 0.80 | 11.78 | 14.73x |
| **Average Time (s)** | 322.2 | 22.1 | 14.55x |

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
| **Throughput (Gb/s)** | 0.79 | 11.82 | 15.00x |
| **Average Time (s)** | 327.5 | 21.8 | 15.02x |

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
| **Throughput (Gb/s)** | 0.80 | 16.25 | 20.32x |
| **Average Time (s)** | 53.7 | 2.9 | 18.66x |

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
| **Throughput (Gb/s)** | 0.79 | 12.25 | 15.51x |
| **Average Time (s)** | 54.4 | 3.5 | 15.40x |

#### Statistical Details

| Statistic | Regular APIs | WithResponse APIs |
|-----------|--------------|-------------------|
| **Min Time (s)** | 53.79 | 3.37 |
| **Max Time (s)** | 60.24 | 4.64 |
| **Std Dev Time** | 2.04 | 0.39 |
| **Min Throughput (Gb/s)** | 0.71 | 9.26 |
| **Max Throughput (Gb/s)** | 0.80 | 12.74 |
| **Std Dev Throughput** | 0.03 | 1.05 |


## WINDOWS_NETFRAMEWORK Platform Results

| Test Type | File Size | Storage | Regular (Gb/s) | WithResp (Gb/s) | Difference | Faster API |
|-----------|-----------|---------|----------------|-----------------|------------|------------|
| download-100MiB (RAM) | 100.0MiB | RAM | 0.77 | 4.08 | 427.9% | WithResponse |
| download-100MiB | 100.0MiB | Disk | 0.70 | 0.52 | 26.8% | Regular |
| download-1GiB ram | 1.0GiB | RAM | 0.80 | 4.86 | 509.8% | WithResponse |
| download-1GiB | 1.0GiB | Disk | 0.79 | 0.58 | 26.9% | Regular |
| download-30GiB ram | 30.0GiB | RAM | 0.80 | 4.03 | 404.2% | WithResponse |
| download-30GiB | 30.0GiB | Disk | 0.79 | 0.34 | 56.4% | Regular |
| download-5GiB ram | 5.0GiB | RAM | 0.79 | 4.41 | 459.0% | WithResponse |
| download-5GiB | 5.0GiB | Disk | 0.80 | 0.50 | 37.7% | Regular |

## Detailed Performance Breakdown - WINDOWS_NETFRAMEWORK

### 100.0MiB Download to RAM

| Metric | Regular APIs | WithResponse APIs | Comparison |
|--------|--------------|-------------------|------------|
| **Throughput (Gb/s)** | 0.77 | 4.08 | 5.28x |
| **Average Time (s)** | 1.1 | 0.2 | 4.46x |

#### Statistical Details

| Statistic | Regular APIs | WithResponse APIs |
|-----------|--------------|-------------------|
| **Min Time (s)** | 1.05 | 0.19 |
| **Max Time (s)** | 1.52 | 0.75 |
| **Std Dev Time** | 0.15 | 0.18 |
| **Min Throughput (Gb/s)** | 0.55 | 1.12 |
| **Max Throughput (Gb/s)** | 0.80 | 4.53 |
| **Std Dev Throughput** | 0.08 | 1.05 |

### 100.0MiB Download to Disk

| Metric | Regular APIs | WithResponse APIs | Comparison |
|--------|--------------|-------------------|------------|
| **Throughput (Gb/s)** | 0.70 | 0.52 | 0.73x |
| **Average Time (s)** | 1.2 | 1.6 | 0.73x |

#### Statistical Details

| Statistic | Regular APIs | WithResponse APIs |
|-----------|--------------|-------------------|
| **Min Time (s)** | 1.15 | 1.54 |
| **Max Time (s)** | 1.72 | 2.22 |
| **Std Dev Time** | 0.18 | 0.20 |
| **Min Throughput (Gb/s)** | 0.49 | 0.38 |
| **Max Throughput (Gb/s)** | 0.73 | 0.54 |
| **Std Dev Throughput** | 0.08 | 0.05 |

### 1.0GiB Download to RAM

| Metric | Regular APIs | WithResponse APIs | Comparison |
|--------|--------------|-------------------|------------|
| **Throughput (Gb/s)** | 0.80 | 4.86 | 6.10x |
| **Average Time (s)** | 10.8 | 1.8 | 6.06x |

#### Statistical Details

| Statistic | Regular APIs | WithResponse APIs |
|-----------|--------------|-------------------|
| **Min Time (s)** | 10.74 | 1.57 |
| **Max Time (s)** | 11.22 | 2.05 |
| **Std Dev Time** | 0.15 | 0.15 |
| **Min Throughput (Gb/s)** | 0.77 | 4.20 |
| **Max Throughput (Gb/s)** | 0.80 | 5.47 |
| **Std Dev Throughput** | 0.01 | 0.40 |

### 1.0GiB Download to Disk

| Metric | Regular APIs | WithResponse APIs | Comparison |
|--------|--------------|-------------------|------------|
| **Throughput (Gb/s)** | 0.79 | 0.58 | 0.73x |
| **Average Time (s)** | 10.9 | 15.0 | 0.72x |

#### Statistical Details

| Statistic | Regular APIs | WithResponse APIs |
|-----------|--------------|-------------------|
| **Min Time (s)** | 10.84 | 13.69 |
| **Max Time (s)** | 11.34 | 19.71 |
| **Std Dev Time** | 0.16 | 1.71 |
| **Min Throughput (Gb/s)** | 0.76 | 0.44 |
| **Max Throughput (Gb/s)** | 0.79 | 0.63 |
| **Std Dev Throughput** | 0.01 | 0.05 |

### 30.0GiB Download to RAM

| Metric | Regular APIs | WithResponse APIs | Comparison |
|--------|--------------|-------------------|------------|
| **Throughput (Gb/s)** | 0.80 | 4.03 | 5.04x |
| **Average Time (s)** | 322.3 | 63.9 | 5.04x |

#### Statistical Details

| Statistic | Regular APIs | WithResponse APIs |
|-----------|--------------|-------------------|
| **Min Time (s)** | 322.13 | 62.90 |
| **Max Time (s)** | 322.60 | 65.31 |
| **Std Dev Time** | 0.27 | 1.24 |
| **Min Throughput (Gb/s)** | 0.80 | 3.95 |
| **Max Throughput (Gb/s)** | 0.80 | 4.10 |
| **Std Dev Throughput** | 0.00 | 0.08 |

### 30.0GiB Download to Disk

| Metric | Regular APIs | WithResponse APIs | Comparison |
|--------|--------------|-------------------|------------|
| **Throughput (Gb/s)** | 0.79 | 0.34 | 0.44x |
| **Average Time (s)** | 325.7 | 926.2 | 0.35x |

#### Statistical Details

| Statistic | Regular APIs | WithResponse APIs |
|-----------|--------------|-------------------|
| **Min Time (s)** | 323.74 | 580.68 |
| **Max Time (s)** | 329.01 | 1598.34 |
| **Std Dev Time** | 2.88 | 582.20 |
| **Min Throughput (Gb/s)** | 0.78 | 0.16 |
| **Max Throughput (Gb/s)** | 0.80 | 0.44 |
| **Std Dev Throughput** | 0.01 | 0.16 |

### 5.0GiB Download to RAM

| Metric | Regular APIs | WithResponse APIs | Comparison |
|--------|--------------|-------------------|------------|
| **Throughput (Gb/s)** | 0.79 | 4.41 | 5.59x |
| **Average Time (s)** | 54.4 | 9.7 | 5.59x |

#### Statistical Details

| Statistic | Regular APIs | WithResponse APIs |
|-----------|--------------|-------------------|
| **Min Time (s)** | 53.69 | 9.39 |
| **Max Time (s)** | 56.52 | 10.59 |
| **Std Dev Time** | 1.13 | 0.34 |
| **Min Throughput (Gb/s)** | 0.76 | 4.06 |
| **Max Throughput (Gb/s)** | 0.80 | 4.58 |
| **Std Dev Throughput** | 0.02 | 0.15 |

### 5.0GiB Download to Disk

| Metric | Regular APIs | WithResponse APIs | Comparison |
|--------|--------------|-------------------|------------|
| **Throughput (Gb/s)** | 0.80 | 0.50 | 0.62x |
| **Average Time (s)** | 53.8 | 87.6 | 0.61x |

#### Statistical Details

| Statistic | Regular APIs | WithResponse APIs |
|-----------|--------------|-------------------|
| **Min Time (s)** | 53.79 | 77.29 |
| **Max Time (s)** | 54.29 | 107.71 |
| **Std Dev Time** | 0.16 | 11.85 |
| **Min Throughput (Gb/s)** | 0.79 | 0.40 |
| **Max Throughput (Gb/s)** | 0.80 | 0.56 |
| **Std Dev Throughput** | 0.00 | 0.06 |


## WINDOWS_NETSTANDARD Platform Results

| Test Type | File Size | Storage | Regular (Gb/s) | WithResp (Gb/s) | Difference | Faster API |
|-----------|-----------|---------|----------------|-----------------|------------|------------|
| download-100MiB (RAM) | 100.0MiB | RAM | 0.78 | 6.06 | 671.7% | WithResponse |
| download-100MiB | 100.0MiB | Disk | 0.70 | 3.60 | 411.1% | WithResponse |
| download-1GiB ram | 1.0GiB | RAM | 0.80 | 12.18 | 1426.1% | WithResponse |
| download-1GiB | 1.0GiB | Disk | 0.79 | 8.27 | 952.9% | WithResponse |
| download-30GiB ram | 30.0GiB | RAM | 0.80 | 19.88 | 2385.3% | WithResponse |
| download-30GiB | 30.0GiB | Disk | 0.78 | 5.13 | 555.4% | WithResponse |
| download-5GiB ram | 5.0GiB | RAM | 0.80 | 24.13 | 2917.9% | WithResponse |
| download-5GiB | 5.0GiB | Disk | 0.79 | 5.83 | 641.1% | WithResponse |

## Detailed Performance Breakdown - WINDOWS_NETSTANDARD

### 100.0MiB Download to RAM

| Metric | Regular APIs | WithResponse APIs | Comparison |
|--------|--------------|-------------------|------------|
| **Throughput (Gb/s)** | 0.78 | 6.06 | 7.72x |
| **Average Time (s)** | 1.1 | 0.2 | 6.70x |

#### Statistical Details

| Statistic | Regular APIs | WithResponse APIs |
|-----------|--------------|-------------------|
| **Min Time (s)** | 1.05 | 0.12 |
| **Max Time (s)** | 1.24 | 0.44 |
| **Std Dev Time** | 0.06 | 0.10 |
| **Min Throughput (Gb/s)** | 0.67 | 1.93 |
| **Max Throughput (Gb/s)** | 0.80 | 7.08 |
| **Std Dev Throughput** | 0.04 | 1.51 |

### 100.0MiB Download to Disk

| Metric | Regular APIs | WithResponse APIs | Comparison |
|--------|--------------|-------------------|------------|
| **Throughput (Gb/s)** | 0.70 | 3.60 | 5.11x |
| **Average Time (s)** | 1.2 | 0.3 | 4.73x |

#### Statistical Details

| Statistic | Regular APIs | WithResponse APIs |
|-----------|--------------|-------------------|
| **Min Time (s)** | 1.15 | 0.20 |
| **Max Time (s)** | 1.65 | 0.55 |
| **Std Dev Time** | 0.15 | 0.11 |
| **Min Throughput (Gb/s)** | 0.51 | 1.51 |
| **Max Throughput (Gb/s)** | 0.73 | 4.25 |
| **Std Dev Throughput** | 0.07 | 0.83 |

### 1.0GiB Download to RAM

| Metric | Regular APIs | WithResponse APIs | Comparison |
|--------|--------------|-------------------|------------|
| **Throughput (Gb/s)** | 0.80 | 12.18 | 15.26x |
| **Average Time (s)** | 10.8 | 0.7 | 14.82x |

#### Statistical Details

| Statistic | Regular APIs | WithResponse APIs |
|-----------|--------------|-------------------|
| **Min Time (s)** | 10.74 | 0.58 |
| **Max Time (s)** | 10.94 | 1.11 |
| **Std Dev Time** | 0.06 | 0.15 |
| **Min Throughput (Gb/s)** | 0.79 | 7.75 |
| **Max Throughput (Gb/s)** | 0.80 | 14.80 |
| **Std Dev Throughput** | 0.00 | 1.94 |

### 1.0GiB Download to Disk

| Metric | Regular APIs | WithResponse APIs | Comparison |
|--------|--------------|-------------------|------------|
| **Throughput (Gb/s)** | 0.79 | 8.27 | 10.53x |
| **Average Time (s)** | 11.0 | 1.1 | 10.14x |

#### Statistical Details

| Statistic | Regular APIs | WithResponse APIs |
|-----------|--------------|-------------------|
| **Min Time (s)** | 10.84 | 0.90 |
| **Max Time (s)** | 11.91 | 1.71 |
| **Std Dev Time** | 0.34 | 0.25 |
| **Min Throughput (Gb/s)** | 0.72 | 5.04 |
| **Max Throughput (Gb/s)** | 0.79 | 9.56 |
| **Std Dev Throughput** | 0.02 | 1.50 |

### 30.0GiB Download to RAM

| Metric | Regular APIs | WithResponse APIs | Comparison |
|--------|--------------|-------------------|------------|
| **Throughput (Gb/s)** | 0.80 | 19.88 | 24.85x |
| **Average Time (s)** | 322.2 | 13.0 | 24.73x |

#### Statistical Details

| Statistic | Regular APIs | WithResponse APIs |
|-----------|--------------|-------------------|
| **Min Time (s)** | 322.14 | 12.01 |
| **Max Time (s)** | 322.33 | 14.23 |
| **Std Dev Time** | 0.10 | 1.12 |
| **Min Throughput (Gb/s)** | 0.80 | 18.11 |
| **Max Throughput (Gb/s)** | 0.80 | 21.46 |
| **Std Dev Throughput** | 0.00 | 1.68 |

### 30.0GiB Download to Disk

| Metric | Regular APIs | WithResponse APIs | Comparison |
|--------|--------------|-------------------|------------|
| **Throughput (Gb/s)** | 0.78 | 5.13 | 6.55x |
| **Average Time (s)** | 329.5 | 50.3 | 6.55x |

#### Statistical Details

| Statistic | Regular APIs | WithResponse APIs |
|-----------|--------------|-------------------|
| **Min Time (s)** | 322.74 | 48.33 |
| **Max Time (s)** | 341.38 | 52.63 |
| **Std Dev Time** | 10.35 | 2.17 |
| **Min Throughput (Gb/s)** | 0.75 | 4.90 |
| **Max Throughput (Gb/s)** | 0.80 | 5.33 |
| **Std Dev Throughput** | 0.02 | 0.22 |

### 5.0GiB Download to RAM

| Metric | Regular APIs | WithResponse APIs | Comparison |
|--------|--------------|-------------------|------------|
| **Throughput (Gb/s)** | 0.80 | 24.13 | 30.18x |
| **Average Time (s)** | 53.7 | 1.8 | 29.62x |

#### Statistical Details

| Statistic | Regular APIs | WithResponse APIs |
|-----------|--------------|-------------------|
| **Min Time (s)** | 53.69 | 1.53 |
| **Max Time (s)** | 53.89 | 2.36 |
| **Std Dev Time** | 0.06 | 0.27 |
| **Min Throughput (Gb/s)** | 0.80 | 18.19 |
| **Max Throughput (Gb/s)** | 0.80 | 28.07 |
| **Std Dev Throughput** | 0.00 | 3.34 |

### 5.0GiB Download to Disk

| Metric | Regular APIs | WithResponse APIs | Comparison |
|--------|--------------|-------------------|------------|
| **Throughput (Gb/s)** | 0.79 | 5.83 | 7.41x |
| **Average Time (s)** | 54.7 | 7.6 | 7.20x |

#### Statistical Details

| Statistic | Regular APIs | WithResponse APIs |
|-----------|--------------|-------------------|
| **Min Time (s)** | 53.77 | 5.31 |
| **Max Time (s)** | 63.09 | 9.56 |
| **Std Dev Time** | 2.94 | 1.39 |
| **Min Throughput (Gb/s)** | 0.68 | 4.49 |
| **Max Throughput (Gb/s)** | 0.80 | 8.09 |
| **Std Dev Throughput** | 0.04 | 1.12 |

