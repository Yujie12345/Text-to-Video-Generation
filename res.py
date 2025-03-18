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
    Plot a specific quality metric for all ComfyUI video files.
    
    Parameters:
    - metric_type: 'PSNR', 'SSIM', or 'VMAF'
    - output_file: File path to save the plot (if None, display instead)
    """
    plt.figure(figsize=(16, 8))
    
    # Setup the plot with a logarithmic y-scale
    if metric_type == 'PSNR' or metric_type == 'VMAF':
        plt.yscale('log')
    
    # Find all relevant CSV files in the res_results directory
    pattern = f"res_results/ComfyUI_*.{metric_type}.csv"
    csv_files = glob.glob(pattern)
    
    # Set up colors for the plot
    colors = plt.cm.tab20(np.linspace(0, 1, len(csv_files)))
    
    # Process each CSV file
    for i, file_path in enumerate(csv_files):
        # Extract video name from the file path
        video_name = os.path.basename(file_path).split('.')[0]
        
        # Load the data
        df = load_metric_data(file_path)
        if df is None:
            continue
        
        # Select the appropriate column based on metric type
        if metric_type == 'PSNR':
            y_data = df['psnr_avg'] if 'psnr_avg' in df.columns else df['psnr_y']
        elif metric_type == 'SSIM':
            y_data = df['All'] if 'All' in df.columns else df['Y']
        elif metric_type == 'VMAF':
            y_data = df['vmaf'] if 'vmaf' in df.columns else None
        else:
            print(f"Unknown metric type: {metric_type}")
            return
        
        # Skip files with no valid data
        if y_data is None:
            continue
            
        # Get frame numbers for x-axis
        x_data = df['frame'] if 'frame' in df.columns else np.arange(len(y_data))
        
        # Plot the data
        plt.plot(x_data, y_data, label=video_name, color=colors[i])
    
    # Set up labels and title
    plt.xlabel('Frame')
    plt.ylabel(metric_type)
    plt.title(f'{metric_type} Comparison of ComfyUI Videos')
    plt.grid(True, alpha=0.3)
    
    # Add legend below the plot
    plt.legend(loc='upper center', bbox_to_anchor=(0.5, -0.1),
              fancybox=True, shadow=True, ncol=5)
    
    # Tight layout to accommodate the legend
    plt.tight_layout()
    plt.subplots_adjust(bottom=0.2)
    
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
    plot_metric('PSNR', 'comfyui_psnr_comparison.png')
    plot_metric('SSIM', 'comfyui_ssim_comparison.png')
    plot_metric('VMAF', 'comfyui_vmaf_comparison.png')
    
    print("Plots generated successfully!")

if __name__ == "__main__":
    main()


