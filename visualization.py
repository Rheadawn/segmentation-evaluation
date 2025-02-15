import matplotlib.pyplot as plt
from matplotlib import colormaps
import numpy as np

def save2DGraph(filePath, xAxis, yAxis, title, xLabel, yLabel):
    fig = plt.figure(figsize=(8, 6))
    plt.plot(xAxis, yAxis)
    plt.title(title)
    plt.xlabel(xLabel)
    plt.ylabel(yLabel)

    fig.savefig(filePath, dpi=600)

def save2DGraphComparison(filePath, xAxes, yAxes, labels, title, xLabel, yLabel):
    fig = plt.figure(figsize=(8, 6))
    for i in range(len(xAxes)):
        plt.plot(xAxes[i], yAxes[i], label=labels[i])
    plt.title(title)
    plt.xlabel(xLabel)
    plt.ylabel(yLabel)
    plt.legend()

    fig.savefig(filePath, dpi=600)

def save2DGraphComparisonWithSeparateScales(filePath, xAxes, yAxes, labels, title, xLabel, yLabel):
    fig, ax1 = plt.subplots(figsize=(8, 6))
    ax2 = ax1.twinx()
    for i in range(len(xAxes)):
        if i == 0:
            line1 = ax1.plot(xAxes[i], yAxes[i], label=labels[i], color='tab:blue')
        else:
            line2 = ax2.plot(xAxes[i], yAxes[i], label=labels[i], color='tab:orange')
    ax1.set_xlabel(xLabel)
    ax1.set_ylabel(yLabel[0], color='tab:blue')
    ax2.set_ylabel(yLabel[1], color='tab:orange')
    plt.title(title)
    lines = line1 + line2
    labels = [l.get_label() for l in lines]
    ax1.legend(lines, labels)
    fig.savefig(filePath, dpi=600)

def saveScatterPlot(filePath, xAxes, yAxes, labels, title, xLabel, yLabel):
    fig = plt.figure(figsize=(8, 6))
    for i in range(len(xAxes)):
        plt.scatter(xAxes[i], yAxes[i], label=labels[i])
    plt.title(title)
    plt.xlabel(xLabel)
    plt.ylabel(yLabel)
    plt.legend()

    fig.savefig(filePath, dpi=600)

def saveDumbellGraph(filePath, interval_groups, labels, title):
    fig, ax = plt.subplots(figsize=(16, 6))
    
    # Get tab10 colormap
    colors = plt.cm.tab10(np.linspace(0, 1, len(interval_groups)))
    
    # Assuming interval_groups is a list of lists, where each inner list contains tuples of (start, optimum, end)
    for i, (intervals, color) in enumerate(zip(interval_groups, colors)):
        for start, optimum, end in intervals:
            ax.plot([start, end], [i, i], '-o', markersize=4, color=color)
            ax.plot([optimum, optimum], [i-0.05, i+0.05], '-', linewidth=2, color=color)
    
    ax.set_yticks(range(len(labels)))
    ax.set_yticklabels(labels)
    
    ax.grid(which="major", axis='x', color='#758D99', alpha=0.6)
    ax.spines[['top', 'right']].set_visible(False)
    
    plt.title(title)
    
    fig.savefig(filePath, dpi=600)

    #filePath, xAxis, yAxis, title, xLabel, yLabel

def saveDumbellGraphAnd2DGraph(filePath, interval_groups, labels, title, xAxis, yAxis, xLabel, yLabel):
    # Create figure with two subplots, with different heights (3:1 ratio)
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(16, 6), height_ratios=[2.5, 1.5], sharex=True)
    
    # Get tab10 colormap
    colors = plt.cm.tab10(np.linspace(0, 1, len(interval_groups)))
    
    # Plot dumbell graph on top subplot
    for i, (intervals, color) in enumerate(zip(interval_groups, colors)):
        if intervals:  # Only plot if intervals is not empty
            for start, optimum, end in intervals:
                ax1.plot([start, end], [i, i], '-o', markersize=4, color=color)
                ax1.plot([optimum, optimum], [i-0.05, i+0.05], '-', linewidth=2, color=color)
    
    ax1.set_yticks(range(len(labels)))
    ax1.set_yticklabels(labels)
    ax1.grid(which="major", axis='x', color='#758D99', alpha=0.6)
    ax1.spines[['top', 'right']].set_visible(False)
    
    # Plot 2D graph on bottom subplot
    ax2.plot(xAxis, yAxis)
    ax2.grid(axis='x')
    ax2.set_xlabel(xLabel)
    ax2.set_ylabel(yLabel)
    ax2.set_yticks([])  # Remove y-axis ticks
    
    # Set common title
    fig.suptitle(title)
    
    # Adjust layout to prevent overlap
    plt.tight_layout()
    
    fig.savefig(filePath, dpi=600)
    plt.close(fig)
