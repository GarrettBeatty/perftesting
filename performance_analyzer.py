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
        """Find matching single vs multi-part test pairs"""
        if platform not in self.results:
            return []
        
        pairs = []
        tests = self.results[platform]
        
        for single_test in tests:
            if '-multi' not in single_test.test_name:
                # Look for corresponding multi-part test
                multi_name = single_test.test_name + '-multi'
                multi_test = next(
                    (t for t in tests if t.test_name == multi_name 
                     and t.files_on_disk == single_test.files_on_disk 
                     and t.file_size_bytes == single_test.file_size_bytes), 
                    None
                )
                if multi_test:
                    pairs.append((single_test, multi_test))
        
        return pairs
    
    def calculate_improvement(self, single: TestResult, multi: TestResult) -> Dict[str, float]:
        """Calculate performance improvement metrics"""
        single_stats = single.get_stats()
        multi_stats = multi.get_stats()
        
        # Calculate improvement ratios
        time_improvement = single_stats['mean_time'] / multi_stats['mean_time']
        throughput_improvement = multi_stats['mean_throughput'] / single_stats['mean_throughput']
        
        return {
            'time_improvement_ratio': time_improvement,
            'throughput_improvement_ratio': throughput_improvement,
            'time_reduction_percent': ((single_stats['mean_time'] - multi_stats['mean_time']) / single_stats['mean_time']) * 100,
            'throughput_increase_percent': ((multi_stats['mean_throughput'] - single_stats['mean_throughput']) / single_stats['mean_throughput']) * 100,
            'single_mean_time': single_stats['mean_time'],
            'multi_mean_time': multi_stats['mean_time'],
            'single_mean_throughput': single_stats['mean_throughput'],
            'multi_mean_throughput': multi_stats['mean_throughput']
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
        report_lines.append("=" * 80)
        
        for plat in platforms_to_process:
            if not self.results[plat]:
                continue
                
            report_lines.append(f"\n{'='*20} {plat.upper()} PLATFORM RESULTS {'='*20}")
            
            pairs = self.find_test_pairs(plat)
            if not pairs:
                report_lines.append(f"No matching single/multi-part test pairs found for {plat}")
                continue
            
            # Summary table header
            report_lines.append("\nSUMMARY TABLE:")
            report_lines.append("-" * 120)
            report_lines.append(f"{'Test Type':<25} {'File Size':<12} {'Storage':<8} {'Single (Gb/s)':<15} {'Multi (Gb/s)':<15} {'Improvement':<15} {'Time Reduction':<15}")
            report_lines.append("-" * 120)
            
            for single, multi in pairs:
                improvement = self.calculate_improvement(single, multi)
                storage_type = "Disk" if single.files_on_disk else "RAM"
                file_size = self.format_file_size(single.file_size_bytes)
                
                # Extract base test name (remove size and single/multi indicators)
                base_name = single.test_name.replace('-1x', '').replace('GiB-', 'GiB ')
                if '-ram' in base_name:
                    base_name = base_name.replace('-ram', ' (RAM)')
                
                report_lines.append(
                    f"{base_name:<25} {file_size:<12} {storage_type:<8} "
                    f"{improvement['single_mean_throughput']:<15.2f} "
                    f"{improvement['multi_mean_throughput']:<15.2f} "
                    f"{improvement['throughput_improvement_ratio']:<15.1f}x "
                    f"{improvement['time_reduction_percent']:<15.1f}%"
                )
            
            # Detailed breakdown
            report_lines.append(f"\nDETAILED BREAKDOWN for {plat.upper()}:")
            report_lines.append("=" * 60)
            
            for single, multi in pairs:
                improvement = self.calculate_improvement(single, multi)
                storage_type = "to Disk" if single.files_on_disk else "to RAM"
                file_size = self.format_file_size(single.file_size_bytes)
                
                report_lines.append(f"\n📊 {file_size} Download {storage_type}")
                report_lines.append("-" * 40)
                report_lines.append(f"Single-part:  {improvement['single_mean_throughput']:8.2f} Gb/s (avg {improvement['single_mean_time']:6.1f}s)")
                report_lines.append(f"Multi-part:   {improvement['multi_mean_throughput']:8.2f} Gb/s (avg {improvement['multi_mean_time']:6.1f}s)")
                report_lines.append(f"Improvement:  {improvement['throughput_improvement_ratio']:8.1f}x faster ({improvement['time_reduction_percent']:5.1f}% time reduction)")
        
        return "\n".join(report_lines)
    
    def export_csv(self, filename: str, platform: str = None) -> None:
        """Export results to CSV format"""
        platforms_to_process = [platform] if platform else list(self.results.keys())
        
        with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
            fieldnames = [
                'Platform', 'Test_Type', 'File_Size_GB', 'Storage_Type', 
                'Single_Throughput_Gbps', 'Multi_Throughput_Gbps', 
                'Improvement_Ratio', 'Time_Reduction_Percent',
                'Single_Mean_Time', 'Multi_Mean_Time'
            ]
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            
            for plat in platforms_to_process:
                pairs = self.find_test_pairs(plat)
                for single, multi in pairs:
                    improvement = self.calculate_improvement(single, multi)
                    storage_type = "Disk" if single.files_on_disk else "RAM"
                    
                    writer.writerow({
                        'Platform': plat,
                        'Test_Type': single.test_name.replace('-1x', '').replace('-ram', '_RAM'),
                        'File_Size_GB': single.file_size_bytes / (1024**3),
                        'Storage_Type': storage_type,
                        'Single_Throughput_Gbps': improvement['single_mean_throughput'],
                        'Multi_Throughput_Gbps': improvement['multi_mean_throughput'],
                        'Improvement_Ratio': improvement['throughput_improvement_ratio'],
                        'Time_Reduction_Percent': improvement['time_reduction_percent'],
                        'Single_Mean_Time': improvement['single_mean_time'],
                        'Multi_Mean_Time': improvement['multi_mean_time']
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
                    'avg_improvement': 0
                }
            }
            
            pairs = self.find_test_pairs(plat)
            improvements = []
            
            for single, multi in pairs:
                improvement = self.calculate_improvement(single, multi)
                improvements.append(improvement['throughput_improvement_ratio'])
                
                pair_data = {
                    'test_name': single.test_name,
                    'file_size_bytes': single.file_size_bytes,
                    'file_size_formatted': self.format_file_size(single.file_size_bytes),
                    'storage_type': "disk" if single.files_on_disk else "ram",
                    'single_part': {
                        'stats': single.get_stats(),
                        'runs': [{'run': r.run_number, 'time': r.seconds, 'throughput': r.gbps} for r in single.runs]
                    },
                    'multi_part': {
                        'stats': multi.get_stats(),
                        'runs': [{'run': r.run_number, 'time': r.seconds, 'throughput': r.gbps} for r in multi.runs]
                    },
                    'improvement_metrics': improvement
                }
                json_data[plat]['test_pairs'].append(pair_data)
            
            json_data[plat]['summary']['total_pairs'] = len(pairs)
            json_data[plat]['summary']['avg_improvement'] = mean(improvements) if improvements else 0
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(json_data, f, indent=2)
        
        print(f"JSON report exported to: {filename}")
    
    def generate_markdown_summary_table(self, platform: str) -> str:
        """Generate a markdown summary table for a specific platform"""
        pairs = self.find_test_pairs(platform)
        if not pairs:
            return f"No matching single/multi-part test pairs found for {platform}"
        
        markdown_lines = []
        markdown_lines.append(f"## {platform.upper()} Platform Results")
        markdown_lines.append("")
        markdown_lines.append("| Test Type | File Size | Storage | Single (Gb/s) | Multi (Gb/s) | Improvement | Time Reduction |")
        markdown_lines.append("|-----------|-----------|---------|---------------|--------------|-------------|----------------|")
        
        for single, multi in pairs:
            improvement = self.calculate_improvement(single, multi)
            storage_type = "Disk" if single.files_on_disk else "RAM"
            file_size = self.format_file_size(single.file_size_bytes)
            
            # Extract base test name
            base_name = single.test_name.replace('-1x', '').replace('GiB-', 'GiB ')
            if '-ram' in base_name:
                base_name = base_name.replace('-ram', ' (RAM)')
            
            markdown_lines.append(
                f"| {base_name} | {file_size} | {storage_type} | "
                f"{improvement['single_mean_throughput']:.2f} | "
                f"{improvement['multi_mean_throughput']:.2f} | "
                f"{improvement['throughput_improvement_ratio']:.1f}x | "
                f"{improvement['time_reduction_percent']:.1f}% |"
            )
        
        return "\n".join(markdown_lines)
    
    def generate_markdown_detailed_table(self, platform: str) -> str:
        """Generate a markdown detailed breakdown table for a specific platform"""
        pairs = self.find_test_pairs(platform)
        if not pairs:
            return f"No matching single/multi-part test pairs found for {platform}"
        
        markdown_lines = []
        markdown_lines.append(f"## Detailed Performance Breakdown - {platform.upper()}")
        markdown_lines.append("")
        
        for single, multi in pairs:
            improvement = self.calculate_improvement(single, multi)
            storage_type = "to Disk" if single.files_on_disk else "to RAM"
            file_size = self.format_file_size(single.file_size_bytes)
            
            markdown_lines.append(f"### {file_size} Download {storage_type}")
            markdown_lines.append("")
            markdown_lines.append("| Metric | Single-part | Multi-part | Improvement |")
            markdown_lines.append("|--------|-------------|------------|-------------|")
            markdown_lines.append(f"| **Throughput (Gb/s)** | {improvement['single_mean_throughput']:.2f} | {improvement['multi_mean_throughput']:.2f} | {improvement['throughput_improvement_ratio']:.1f}x |")
            markdown_lines.append(f"| **Average Time (s)** | {improvement['single_mean_time']:.1f} | {improvement['multi_mean_time']:.1f} | {improvement['time_reduction_percent']:.1f}% reduction |")
            
            # Add statistical details
            single_stats = single.get_stats()
            multi_stats = multi.get_stats()
            
            markdown_lines.append("")
            markdown_lines.append("#### Statistical Details")
            markdown_lines.append("")
            markdown_lines.append("| Statistic | Single-part | Multi-part |")
            markdown_lines.append("|-----------|-------------|------------|")
            markdown_lines.append(f"| **Min Time (s)** | {single_stats['min_time']:.2f} | {multi_stats['min_time']:.2f} |")
            markdown_lines.append(f"| **Max Time (s)** | {single_stats['max_time']:.2f} | {multi_stats['max_time']:.2f} |")
            markdown_lines.append(f"| **Std Dev Time** | {single_stats['std_time']:.2f} | {multi_stats['std_time']:.2f} |")
            markdown_lines.append(f"| **Min Throughput (Gb/s)** | {single_stats['min_throughput']:.2f} | {multi_stats['min_throughput']:.2f} |")
            markdown_lines.append(f"| **Max Throughput (Gb/s)** | {single_stats['max_throughput']:.2f} | {multi_stats['max_throughput']:.2f} |")
            markdown_lines.append(f"| **Std Dev Throughput** | {single_stats['std_throughput']:.2f} | {multi_stats['std_throughput']:.2f} |")
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
        markdown_lines.append("This report compares single-part vs multi-part download performance across different platforms.")
        markdown_lines.append("")
        
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
        description="Analyze performance logs comparing single vs multi-part downloads",
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
