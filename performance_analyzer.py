#!/usr/bin/env python3
"""
Performance Log Analyzer
Parses and compares single-part vs multi-part download performance logs
Supports multiple platforms (Linux, Windows, etc.)
"""

import os
import re
import json
import csv
import argparse
from pathlib import Path
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass
from statistics import mean, median, stdev
import sys


@dataclass
class TestRun:
    """Represents a single test run with timing and throughput data"""
    run_number: int
    seconds: float
    gbps: float


@dataclass
class TestResult:
    """Represents complete test results from a log file"""
    platform: str
    test_name: str
    file_size_bytes: int
    files_on_disk: bool
    with_response_apis: bool
    max_repeat_count: int
    max_repeat_secs: int
    runs: List[TestRun]
    
    def get_stats(self) -> Dict[str, float]:
        """Calculate statistical metrics for the test runs"""
        times = [run.seconds for run in self.runs]
        throughputs = [run.gbps for run in self.runs]
        
        return {
            'mean_time': mean(times),
            'median_time': median(times),
            'min_time': min(times),
            'max_time': max(times),
            'std_time': stdev(times) if len(times) > 1 else 0.0,
            'mean_throughput': mean(throughputs),
            'median_throughput': median(throughputs),
            'min_throughput': min(throughputs),
            'max_throughput': max(throughputs),
            'std_throughput': stdev(throughputs) if len(throughputs) > 1 else 0.0
        }


class LogParser:
    """Parses performance log files and extracts test data"""
    
    def __init__(self):
        self.workload_pattern = re.compile(r'- MaxRepeatCount: (\d+)')
        self.repeat_secs_pattern = re.compile(r'- MaxRepeatSecs: (\d+)')
        self.files_on_disk_pattern = re.compile(r'- FilesOnDisk: (True|False)')
        self.with_response_pattern = re.compile(r'- WithResponseApis: (True|False)')
        self.task_pattern = re.compile(r'- Task: action=download, size=([\d,]+) bytes')
        self.run_pattern = re.compile(r'Run:(\d+) Secs:([\d.]+) Gb/s:([\d.]+)')
    
    def parse_log_file(self, file_path: Path) -> Optional[TestResult]:
        """Parse a single log file and return TestResult"""
        try:
            # Detect encoding by reading BOM (Byte Order Mark)
            encoding = 'utf-8'
            with open(file_path, 'rb') as f:
                bom = f.read(2)
                if bom == b'\xff\xfe':
                    encoding = 'utf-16-le'
                elif bom == b'\xfe\xff':
                    encoding = 'utf-16-be'
                elif bom.startswith(b'\xef\xbb\xbf'):
                    encoding = 'utf-8-sig'
            
            with open(file_path, 'r', encoding=encoding) as f:
                content = f.read()
            
            # Extract platform from path (e.g., linux/, windows/)
            platform = file_path.parent.name
            test_name = file_path.stem
            
            # Parse workload configuration
            max_repeat_count = int(self.workload_pattern.search(content).group(1))
            max_repeat_secs = int(self.repeat_secs_pattern.search(content).group(1))
            files_on_disk = self.files_on_disk_pattern.search(content).group(1) == 'True'
            with_response_apis = self.with_response_pattern.search(content).group(1) == 'True'
            
            # Parse file size (remove commas)
            size_match = self.task_pattern.search(content)
            file_size_bytes = int(size_match.group(1).replace(',', ''))
            
            # Parse test runs
            runs = []
            for match in self.run_pattern.finditer(content):
                run_number = int(match.group(1))
                seconds = float(match.group(2))
                gbps = float(match.group(3))
                runs.append(TestRun(run_number, seconds, gbps))
            
            return TestResult(
                platform=platform,
                test_name=test_name,
                file_size_bytes=file_size_bytes,
                files_on_disk=files_on_disk,
                with_response_apis=with_response_apis,
                max_repeat_count=max_repeat_count,
                max_repeat_secs=max_repeat_secs,
                runs=runs
            )
        
        except Exception as e:
            print(f"Error parsing {file_path}: {e}")
            return None


class PerformanceAnalyzer:
    """Analyzes and compares performance test results"""
    
    def __init__(self):
        self.parser = LogParser()
        self.results: Dict[str, List[TestResult]] = {}
    
    def scan_directories(self, base_path: Path) -> None:
        """Scan for platform directories and log files"""
        for platform_dir in base_path.iterdir():
            if platform_dir.is_dir():
                platform_name = platform_dir.name
                self.results[platform_name] = []
                
                # Find all .log files in the platform directory
                for log_file in platform_dir.glob("*.log"):
                    result = self.parser.parse_log_file(log_file)
                    if result:
                        self.results[platform_name].append(result)
                
                print(f"Found {len(self.results[platform_name])} log files in {platform_name}/")
    
    def find_test_pairs(self, platform: str) -> List[Tuple[TestResult, TestResult]]:
        """Find matching regular vs WithResponse API test pairs"""
        if platform not in self.results:
            return []
        
        pairs = []
        tests = self.results[platform]
        
        for regular_test in tests:
            if not regular_test.with_response_apis:
                # Look for corresponding WithResponse test with same configuration
                # Replace '-regular' suffix with '-withresponse'
                withresponse_name = regular_test.test_name.replace('-regular', '-withresponse')
                withresponse_test = next(
                    (t for t in tests if t.test_name == withresponse_name 
                     and t.files_on_disk == regular_test.files_on_disk 
                     and t.file_size_bytes == regular_test.file_size_bytes
                     and t.with_response_apis), 
                    None
                )
                if withresponse_test:
                    pairs.append((regular_test, withresponse_test))
        
        return pairs
    
    def calculate_improvement(self, regular: TestResult, withresponse: TestResult) -> Dict[str, float]:
        """Calculate performance comparison metrics between regular and WithResponse APIs"""
        regular_stats = regular.get_stats()
        withresponse_stats = withresponse.get_stats()
        
        # Calculate difference ratios (positive means regular is faster)
        time_ratio = withresponse_stats['mean_time'] / regular_stats['mean_time']
        throughput_ratio = regular_stats['mean_throughput'] / withresponse_stats['mean_throughput']
        
        return {
            'time_ratio': time_ratio,
            'throughput_ratio': throughput_ratio,
            'time_difference_percent': ((withresponse_stats['mean_time'] - regular_stats['mean_time']) / regular_stats['mean_time']) * 100,
            'throughput_difference_percent': ((regular_stats['mean_throughput'] - withresponse_stats['mean_throughput']) / withresponse_stats['mean_throughput']) * 100,
            'regular_mean_time': regular_stats['mean_time'],
            'withresponse_mean_time': withresponse_stats['mean_time'],
            'regular_mean_throughput': regular_stats['mean_throughput'],
            'withresponse_mean_throughput': withresponse_stats['mean_throughput']
        }
    
    def format_file_size(self, size_bytes: int) -> str:
        """Format file size in human readable format"""
        if size_bytes >= 1024**3:
            return f"{size_bytes / (1024**3):.1f}GiB"
        elif size_bytes >= 1024**2:
            return f"{size_bytes / (1024**2):.1f}MiB"
        else:
            return f"{size_bytes}B"
    
    def generate_report(self, platform: str = None) -> str:
        """Generate a comprehensive performance comparison report"""
        if platform and platform not in self.results:
            return f"No results found for platform: {platform}"
        
        platforms_to_process = [platform] if platform else list(self.results.keys())
        report_lines = []
        
        report_lines.append("=" * 80)
        report_lines.append("PERFORMANCE ANALYSIS REPORT")
        report_lines.append("Regular APIs vs WithResponse APIs Comparison")
        report_lines.append("=" * 80)
        
        for plat in platforms_to_process:
            if not self.results[plat]:
                continue
                
            report_lines.append(f"\n{'='*20} {plat.upper()} PLATFORM RESULTS {'='*20}")
            
            pairs = self.find_test_pairs(plat)
            if not pairs:
                report_lines.append(f"No matching regular/withresponse test pairs found for {plat}")
                continue
            
            # Summary table header
            report_lines.append("\nSUMMARY TABLE:")
            report_lines.append("-" * 130)
            report_lines.append(f"{'Test Type':<30} {'File Size':<12} {'Storage':<8} {'Regular (Gb/s)':<16} {'WithResp (Gb/s)':<16} {'Difference':<15} {'Faster API':<15}")
            report_lines.append("-" * 130)
            
            for regular, withresponse in pairs:
                comparison = self.calculate_improvement(regular, withresponse)
                storage_type = "Disk" if regular.files_on_disk else "RAM"
                file_size = self.format_file_size(regular.file_size_bytes)
                
                # Extract base test name
                base_name = regular.test_name.replace('-regular', '').replace('-1x', '').replace('GiB-', 'GiB ')
                if '-ram' in base_name:
                    base_name = base_name.replace('-ram', ' (RAM)')
                
                # Determine which is faster
                if comparison['regular_mean_throughput'] > comparison['withresponse_mean_throughput']:
                    faster = "Regular"
                    diff_pct = comparison['throughput_difference_percent']
                else:
                    faster = "WithResponse"
                    diff_pct = -comparison['throughput_difference_percent']
                
                report_lines.append(
                    f"{base_name:<30} {file_size:<12} {storage_type:<8} "
                    f"{comparison['regular_mean_throughput']:<16.2f} "
                    f"{comparison['withresponse_mean_throughput']:<16.2f} "
                    f"{abs(diff_pct):<15.1f}% "
                    f"{faster:<15}"
                )
            
            # Detailed breakdown
            report_lines.append(f"\nDETAILED BREAKDOWN for {plat.upper()}:")
            report_lines.append("=" * 60)
            
            for regular, withresponse in pairs:
                comparison = self.calculate_improvement(regular, withresponse)
                storage_type = "to Disk" if regular.files_on_disk else "to RAM"
                file_size = self.format_file_size(regular.file_size_bytes)
                
                report_lines.append(f"\n📊 {file_size} Download {storage_type}")
                report_lines.append("-" * 40)
                report_lines.append(f"Regular APIs:     {comparison['regular_mean_throughput']:8.2f} Gb/s (avg {comparison['regular_mean_time']:6.1f}s)")
                report_lines.append(f"WithResponse APIs: {comparison['withresponse_mean_throughput']:8.2f} Gb/s (avg {comparison['withresponse_mean_time']:6.1f}s)")
                
                if comparison['regular_mean_throughput'] > comparison['withresponse_mean_throughput']:
                    report_lines.append(f"Result:           Regular is {comparison['throughput_ratio']:.1f}x faster ({comparison['throughput_difference_percent']:.1f}% better throughput)")
                else:
                    report_lines.append(f"Result:           WithResponse is {1/comparison['throughput_ratio']:.1f}x faster ({-comparison['throughput_difference_percent']:.1f}% better throughput)")
        
        return "\n".join(report_lines)
    
    def export_csv(self, filename: str, platform: str = None) -> None:
        """Export results to CSV format"""
        platforms_to_process = [platform] if platform else list(self.results.keys())
        
        with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
            fieldnames = [
                'Platform', 'Test_Type', 'File_Size_GB', 'Storage_Type', 
                'Regular_Throughput_Gbps', 'WithResponse_Throughput_Gbps', 
                'Throughput_Ratio', 'Throughput_Difference_Percent',
                'Regular_Mean_Time', 'WithResponse_Mean_Time', 'Faster_API'
            ]
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            
            for plat in platforms_to_process:
                pairs = self.find_test_pairs(plat)
                for regular, withresponse in pairs:
                    comparison = self.calculate_improvement(regular, withresponse)
                    storage_type = "Disk" if regular.files_on_disk else "RAM"
                    
                    # Determine which is faster
                    if comparison['regular_mean_throughput'] > comparison['withresponse_mean_throughput']:
                        faster = "Regular"
                    else:
                        faster = "WithResponse"
                    
                    writer.writerow({
                        'Platform': plat,
                        'Test_Type': regular.test_name.replace('-regular', '').replace('-1x', '').replace('-ram', '_RAM'),
                        'File_Size_GB': regular.file_size_bytes / (1024**3),
                        'Storage_Type': storage_type,
                        'Regular_Throughput_Gbps': comparison['regular_mean_throughput'],
                        'WithResponse_Throughput_Gbps': comparison['withresponse_mean_throughput'],
                        'Throughput_Ratio': comparison['throughput_ratio'],
                        'Throughput_Difference_Percent': comparison['throughput_difference_percent'],
                        'Regular_Mean_Time': comparison['regular_mean_time'],
                        'WithResponse_Mean_Time': comparison['withresponse_mean_time'],
                        'Faster_API': faster
                    })
        
        print(f"CSV report exported to: {filename}")
    
    def export_json(self, filename: str, platform: str = None) -> None:
        """Export results to JSON format"""
        platforms_to_process = [platform] if platform else list(self.results.keys())
        
        json_data = {}
        for plat in platforms_to_process:
            json_data[plat] = {
                'test_pairs': [],
                'summary': {
                    'total_pairs': 0,
                    'avg_throughput_ratio': 0
                }
            }
            
            pairs = self.find_test_pairs(plat)
            ratios = []
            
            for regular, withresponse in pairs:
                comparison = self.calculate_improvement(regular, withresponse)
                ratios.append(comparison['throughput_ratio'])
                
                # Determine which is faster
                if comparison['regular_mean_throughput'] > comparison['withresponse_mean_throughput']:
                    faster = "Regular"
                else:
                    faster = "WithResponse"
                
                pair_data = {
                    'test_name': regular.test_name,
                    'file_size_bytes': regular.file_size_bytes,
                    'file_size_formatted': self.format_file_size(regular.file_size_bytes),
                    'storage_type': "disk" if regular.files_on_disk else "ram",
                    'regular_apis': {
                        'stats': regular.get_stats(),
                        'runs': [{'run': r.run_number, 'time': r.seconds, 'throughput': r.gbps} for r in regular.runs]
                    },
                    'withresponse_apis': {
                        'stats': withresponse.get_stats(),
                        'runs': [{'run': r.run_number, 'time': r.seconds, 'throughput': r.gbps} for r in withresponse.runs]
                    },
                    'comparison_metrics': comparison,
                    'faster_api': faster
                }
                json_data[plat]['test_pairs'].append(pair_data)
            
            json_data[plat]['summary']['total_pairs'] = len(pairs)
            json_data[plat]['summary']['avg_throughput_ratio'] = mean(ratios) if ratios else 0
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(json_data, f, indent=2)
        
        print(f"JSON report exported to: {filename}")
    
    def generate_markdown_summary_table(self, platform: str) -> str:
        """Generate a markdown summary table for a specific platform"""
        pairs = self.find_test_pairs(platform)
        if not pairs:
            return f"No matching regular/withresponse test pairs found for {platform}"
        
        markdown_lines = []
        markdown_lines.append(f"## {platform.upper()} Platform Results")
        markdown_lines.append("")
        markdown_lines.append("| Test Type | File Size | Storage | Regular (Gb/s) | WithResp (Gb/s) | Difference | Faster API |")
        markdown_lines.append("|-----------|-----------|---------|----------------|-----------------|------------|------------|")
        
        for regular, withresponse in pairs:
            comparison = self.calculate_improvement(regular, withresponse)
            storage_type = "Disk" if regular.files_on_disk else "RAM"
            file_size = self.format_file_size(regular.file_size_bytes)
            
            # Extract base test name
            base_name = regular.test_name.replace('-regular', '').replace('-1x', '').replace('GiB-', 'GiB ')
            if '-ram' in base_name:
                base_name = base_name.replace('-ram', ' (RAM)')
            
            # Determine which is faster
            if comparison['regular_mean_throughput'] > comparison['withresponse_mean_throughput']:
                faster = "Regular"
                diff_pct = comparison['throughput_difference_percent']
            else:
                faster = "WithResponse"
                diff_pct = -comparison['throughput_difference_percent']
            
            markdown_lines.append(
                f"| {base_name} | {file_size} | {storage_type} | "
                f"{comparison['regular_mean_throughput']:.2f} | "
                f"{comparison['withresponse_mean_throughput']:.2f} | "
                f"{abs(diff_pct):.1f}% | "
                f"{faster} |"
            )
        
        return "\n".join(markdown_lines)
    
    def generate_markdown_detailed_table(self, platform: str) -> str:
        """Generate a markdown detailed breakdown table for a specific platform"""
        pairs = self.find_test_pairs(platform)
        if not pairs:
            return f"No matching regular/withresponse test pairs found for {platform}"
        
        markdown_lines = []
        markdown_lines.append(f"## Detailed Performance Breakdown - {platform.upper()}")
        markdown_lines.append("")
        
        for regular, withresponse in pairs:
            comparison = self.calculate_improvement(regular, withresponse)
            storage_type = "to Disk" if regular.files_on_disk else "to RAM"
            file_size = self.format_file_size(regular.file_size_bytes)
            
            markdown_lines.append(f"### {file_size} Download {storage_type}")
            markdown_lines.append("")
            markdown_lines.append("| Metric | Regular APIs | WithResponse APIs | Comparison |")
            markdown_lines.append("|--------|--------------|-------------------|------------|")
            markdown_lines.append(f"| **Throughput (Gb/s)** | {comparison['regular_mean_throughput']:.2f} | {comparison['withresponse_mean_throughput']:.2f} | {comparison['throughput_ratio']:.2f}x |")
            markdown_lines.append(f"| **Average Time (s)** | {comparison['regular_mean_time']:.1f} | {comparison['withresponse_mean_time']:.1f} | {comparison['time_ratio']:.2f}x |")
            
            # Add statistical details
            regular_stats = regular.get_stats()
            withresponse_stats = withresponse.get_stats()
            
            markdown_lines.append("")
            markdown_lines.append("#### Statistical Details")
            markdown_lines.append("")
            markdown_lines.append("| Statistic | Regular APIs | WithResponse APIs |")
            markdown_lines.append("|-----------|--------------|-------------------|")
            markdown_lines.append(f"| **Min Time (s)** | {regular_stats['min_time']:.2f} | {withresponse_stats['min_time']:.2f} |")
            markdown_lines.append(f"| **Max Time (s)** | {regular_stats['max_time']:.2f} | {withresponse_stats['max_time']:.2f} |")
            markdown_lines.append(f"| **Std Dev Time** | {regular_stats['std_time']:.2f} | {withresponse_stats['std_time']:.2f} |")
            markdown_lines.append(f"| **Min Throughput (Gb/s)** | {regular_stats['min_throughput']:.2f} | {withresponse_stats['min_throughput']:.2f} |")
            markdown_lines.append(f"| **Max Throughput (Gb/s)** | {regular_stats['max_throughput']:.2f} | {withresponse_stats['max_throughput']:.2f} |")
            markdown_lines.append(f"| **Std Dev Throughput** | {regular_stats['std_throughput']:.2f} | {withresponse_stats['std_throughput']:.2f} |")
            markdown_lines.append("")
        
        return "\n".join(markdown_lines)
    
    def generate_markdown_overview(self) -> str:
        """Generate cross-platform overview section"""
        markdown_lines = []
        
        markdown_lines.append("## Executive Overview - Cross-Platform Comparison")
        markdown_lines.append("")
        
        # Collect all test results across platforms
        all_pairs = []
        for platform in self.results.keys():
            if not self.results[platform]:
                continue
            pairs = self.find_test_pairs(platform)
            for regular, withresponse in pairs:
                comparison = self.calculate_improvement(regular, withresponse)
                storage_type = "Disk" if regular.files_on_disk else "RAM"
                file_size = self.format_file_size(regular.file_size_bytes)
                
                faster = "Regular" if comparison['regular_mean_throughput'] > comparison['withresponse_mean_throughput'] else "WithResponse"
                diff_pct = abs(comparison['throughput_difference_percent'])
                
                all_pairs.append({
                    'platform': platform,
                    'file_size': file_size,
                    'storage': storage_type,
                    'regular_throughput': comparison['regular_mean_throughput'],
                    'withresponse_throughput': comparison['withresponse_mean_throughput'],
                    'difference': diff_pct,
                    'faster': faster
                })
        
        if not all_pairs:
            return "No test data available for overview."
        
        # Create comprehensive overview table
        markdown_lines.append("### Summary Table - All Platforms")
        markdown_lines.append("")
        markdown_lines.append("| Platform | File Size | Storage | Regular (Gb/s) | WithResp (Gb/s) | Difference | Faster API |")
        markdown_lines.append("|----------|-----------|---------|----------------|-----------------|------------|------------|")
        
        for pair in all_pairs:
            markdown_lines.append(
                f"| {pair['platform']} | {pair['file_size']} | {pair['storage']} | "
                f"{pair['regular_throughput']:.2f} | {pair['withresponse_throughput']:.2f} | "
                f"{pair['difference']:.1f}% | {pair['faster']} |"
            )
        
        markdown_lines.append("")
        
        # Add key insights
        markdown_lines.append("### Key Insights")
        markdown_lines.append("")
        
        # Count wins for each API type
        regular_wins = sum(1 for p in all_pairs if p['faster'] == 'Regular')
        withresponse_wins = sum(1 for p in all_pairs if p['faster'] == 'WithResponse')
        
        markdown_lines.append(f"- **Total Test Scenarios:** {len(all_pairs)}")
        markdown_lines.append(f"- **WithResponse API Wins:** {withresponse_wins} scenarios ({withresponse_wins/len(all_pairs)*100:.1f}%)")
        markdown_lines.append(f"- **Regular API Wins:** {regular_wins} scenarios ({regular_wins/len(all_pairs)*100:.1f}%)")
        markdown_lines.append("")
        
        # Analyze platform performance
        markdown_lines.append("#### Platform-Specific Observations")
        markdown_lines.append("")
        
        for platform in sorted(self.results.keys()):
            if not self.results[platform]:
                continue
            platform_pairs = [p for p in all_pairs if p['platform'] == platform]
            platform_withresp_wins = sum(1 for p in platform_pairs if p['faster'] == 'WithResponse')
            platform_regular_wins = sum(1 for p in platform_pairs if p['faster'] == 'Regular')
            
            avg_withresp_throughput = sum(p['withresponse_throughput'] for p in platform_pairs) / len(platform_pairs)
            avg_regular_throughput = sum(p['regular_throughput'] for p in platform_pairs) / len(platform_pairs)
            
            markdown_lines.append(f"**{platform.upper()}:**")
            markdown_lines.append(f"- WithResponse wins: {platform_withresp_wins}/{len(platform_pairs)} scenarios")
            markdown_lines.append(f"- Regular wins: {platform_regular_wins}/{len(platform_pairs)} scenarios")
            markdown_lines.append(f"- Average WithResponse throughput: {avg_withresp_throughput:.2f} Gb/s")
            markdown_lines.append(f"- Average Regular throughput: {avg_regular_throughput:.2f} Gb/s")
            markdown_lines.append("")
        
        # Storage impact analysis
        ram_pairs = [p for p in all_pairs if p['storage'] == 'RAM']
        disk_pairs = [p for p in all_pairs if p['storage'] == 'Disk']
        
        if ram_pairs:
            ram_withresp_wins = sum(1 for p in ram_pairs if p['faster'] == 'WithResponse')
            markdown_lines.append("#### Storage Type Impact")
            markdown_lines.append("")
            markdown_lines.append(f"**RAM Storage:**")
            markdown_lines.append(f"- WithResponse wins: {ram_withresp_wins}/{len(ram_pairs)} scenarios ({ram_withresp_wins/len(ram_pairs)*100:.1f}%)")
            markdown_lines.append("")
        
        if disk_pairs:
            disk_withresp_wins = sum(1 for p in disk_pairs if p['faster'] == 'WithResponse')
            markdown_lines.append(f"**Disk Storage:**")
            markdown_lines.append(f"- WithResponse wins: {disk_withresp_wins}/{len(disk_pairs)} scenarios ({disk_withresp_wins/len(disk_pairs)*100:.1f}%)")
            markdown_lines.append("")
        
        markdown_lines.append("---")
        markdown_lines.append("")
        
        return "\n".join(markdown_lines)
    
    def generate_markdown_report(self, platform: str = None) -> str:
        """Generate a comprehensive markdown performance comparison report"""
        if platform and platform not in self.results:
            return f"No results found for platform: {platform}"
        
        platforms_to_process = [platform] if platform else list(self.results.keys())
        markdown_lines = []
        
        markdown_lines.append("# Performance Analysis Report")
        markdown_lines.append("")
        markdown_lines.append("This report compares Regular APIs vs WithResponse APIs download performance across different platforms.")
        markdown_lines.append("")
        
        # Add overview section only if processing all platforms
        if not platform:
            overview = self.generate_markdown_overview()
            markdown_lines.append(overview)
        
        # Add detailed sections for each platform
        for plat in platforms_to_process:
            if not self.results[plat]:
                continue
            
            # Add summary table
            summary_table = self.generate_markdown_summary_table(plat)
            markdown_lines.append(summary_table)
            markdown_lines.append("")
            
            # Add detailed breakdown
            detailed_table = self.generate_markdown_detailed_table(plat)
            markdown_lines.append(detailed_table)
            markdown_lines.append("")
        
        return "\n".join(markdown_lines)
    
    def export_markdown(self, filename: str, platform: str = None) -> None:
        """Export results to Markdown format"""
        markdown_content = self.generate_markdown_report(platform)
        
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(markdown_content)
        
        print(f"Markdown report exported to: {filename}")


def main():
    """Main function with command line interface"""
    parser = argparse.ArgumentParser(
        description="Analyze performance logs comparing Regular APIs vs WithResponse APIs",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python performance_analyzer.py                    # Analyze all platforms
  python performance_analyzer.py --platform linux  # Analyze only Linux results
  python performance_analyzer.py --export-csv results.csv
  python performance_analyzer.py --export-json results.json
  python performance_analyzer.py --export-markdown results.md
        """
    )
    
    parser.add_argument('--platform', type=str, 
                      help='Specific platform to analyze (e.g., linux, windows)')
    parser.add_argument('--export-csv', type=str, metavar='FILENAME',
                      help='Export results to CSV file')
    parser.add_argument('--export-json', type=str, metavar='FILENAME', 
                      help='Export results to JSON file')
    parser.add_argument('--export-markdown', type=str, metavar='FILENAME',
                      help='Export results to Markdown file')
    parser.add_argument('--base-path', type=str, default='.',
                      help='Base directory containing platform folders (default: current directory)')
    
    args = parser.parse_args()
    
    # Initialize analyzer
    analyzer = PerformanceAnalyzer()
    
    # Scan for log files
    base_path = Path(args.base_path)
    if not base_path.exists():
        print(f"Error: Base path '{base_path}' does not exist")
        sys.exit(1)
    
    analyzer.scan_directories(base_path)
    
    if not any(analyzer.results.values()):
        print("No log files found. Make sure you have platform directories (linux/, windows/, etc.) with .log files")
        sys.exit(1)
    
    # Generate and display report
    report = analyzer.generate_report(args.platform)
    print(report)
    
    # Export data if requested
    if args.export_csv:
        filename = args.export_csv
        if args.platform:
            # Add platform to filename
            base, ext = os.path.splitext(filename)
            filename = f"{base}_{args.platform}{ext}"
        analyzer.export_csv(filename, args.platform)
    
    if args.export_json:
        filename = args.export_json
        if args.platform:
            # Add platform to filename  
            base, ext = os.path.splitext(filename)
            filename = f"{base}_{args.platform}{ext}"
        analyzer.export_json(filename, args.platform)
    
    if args.export_markdown:
        filename = args.export_markdown
        if args.platform:
            # Add platform to filename
            base, ext = os.path.splitext(filename)
            filename = f"{base}_{args.platform}{ext}"
        analyzer.export_markdown(filename, args.platform)


if __name__ == "__main__":
    main()
