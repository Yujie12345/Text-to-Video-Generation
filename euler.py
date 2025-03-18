import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os
import glob
import sys
from pathlib import Path

def load_metric_data(file_path):
    """Load data from a CSV file containing quality metrics."""
    try:
        df = pd.read_csv(file_path, sep='\t')
        return df
    except Exception as e:
        print(f"Error loading file {file_path}: {e}")
        return None

def plot_metric(metric_type='PSNR', output_file=None):
    """
    Plot a specific quality metric for all Euler video files.
    
    Parameters:
    - metric_type: 'PSNR', 'SSIM', or 'VMAF'
    - output_file: File path to save the plot (if None, display instead)
    """
    plt.figure(figsize=(16, 8))
    
    # Find all relevant CSV files
    csv_pattern = f'euler2/*{metric_type}.csv'
    csv_files = glob.glob(csv_pattern)
    
    if not csv_files:
        print(f"No files found matching pattern: {csv_pattern}")
        print(f"Current working directory: {os.getcwd()}")
        return
    
    print(f"Found {len(csv_files)} files for {metric_type}")
    csv_files.sort()
    
    # Define colors for the plot lines
    colors = plt.cm.tab20(np.linspace(0, 1, len(csv_files)))
    
    # Plot each file's data
    for i, file_path in enumerate(csv_files):
        df = load_metric_data(file_path)
        if df is None:
            continue
        
        # Extract video name from file path
        video_name = Path(file_path).stem.split('.')[0]
        
        try:
            if metric_type == 'PSNR':
                # Plot PSNR average value
                y_values = df['psnr_avg']
            elif metric_type == 'SSIM':
                # Plot SSIM 'All' column
                y_values = df['All']
            elif metric_type == 'VMAF':
                # Plot VMAF column
                y_values = df['vmaf']
            
            plt.plot(df['frame'], y_values, label=video_name, color=colors[i])
        except KeyError as e:
            print(f"Error with file {file_path}: {e}")
            print(f"Available columns: {df.columns.tolist()}")
    
    # Set plot attributes
    plt.grid(True, alpha=0.3)
    plt.xlabel('Frame')
    plt.ylabel(metric_type)
    
    # Adjust y-axis limits based on metric type
    if metric_type == 'PSNR':
        plt.ylim(0, 100)
    elif metric_type == 'SSIM':
        plt.ylim(0, 1.1)
    elif metric_type == 'VMAF':
        plt.ylim(0, 100)
    
    # Add legend with small font size
    plt.legend(loc='upper center', bbox_to_anchor=(0.5, -0.05), 
               ncol=8, fontsize='small')
    
    plt.title(f'{metric_type} Comparison of Euler Videos')
    
    if output_file:
        plt.savefig(output_file, dpi=300, bbox_inches='tight')
        print(f"Saved plot to {output_file}")
    else:
        plt.show()

def main():
    # Print environment info for debugging
    print(f"Python version: {sys.version}")
    import matplotlib
    print(f"Matplotlib version: {matplotlib.__version__}")
    print(f"Pandas version: {pd.__version__}")
    print(f"Working directory: {os.getcwd()}")
    
    # Plot each metric
    plot_metric('PSNR', 'euler_psnr_comparison.png')
    plot_metric('SSIM', 'euler_ssim_comparison.png')
    plot_metric('VMAF', 'euler_vmaf_comparison.png')
    
    print("Plots generated successfully!")

if __name__ == "__main__":
    main()


