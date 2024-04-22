import plotly.graph_objs as go
from plotly.offline import iplot
import pandas as pd
import numpy as np

def create_animated_bar_plot(x_values, y_values, num_frames=10):
    """
    Create an animated bar plot with unique colors for each bar.

    Args:
        x_values (pandas.Series or list): The values for the x-axis.
        y_values (pandas.Series or list): The values for the y-axis.
        num_frames (int): The number of frames for the animation. Default is 10.

    Returns:
        str: The filename of the HTML file containing the plot.
    """
    # Sample data
    y_values_list = [y_values.sample(frac=1).values for _ in range(num_frames)]

    # Generate unique colors for each bar
    num_bars = len(x_values)
    colors = ['rgb({},{},{})'.format(np.random.randint(0, 256), np.random.randint(0, 256), np.random.randint(0, 256)) for _ in range(num_bars)]

    # Create figure
    fig = go.Figure()

    # Add traces for each frame
    for i in range(num_frames):
        # Add trace for current frame with unique color for each bar
        trace = go.Bar(
            x=x_values,
            y=y_values_list[i],
            name=f'Frame {i}',
            visible=False if i > 0 else True,  # Show only the first frame initially
            marker=dict(color=colors)  # Set unique colors for each bar
        )
        fig.add_trace(trace)

    # Set layout options
    fig.update_layout(
        title='Animated Bar Plot with Unique Colors',
        xaxis=dict(title='X-axis'),
        yaxis=dict(title='Y-axis'),
        updatemenus=[
            {
                'buttons': [
                    {
                        'args': [None, {'frame': {'duration': 500, 'redraw': True}, 'fromcurrent': True}],
                        'label': 'Play',
                        'method': 'animate'
                    },
                    {
                        'args': [[None], {'frame': {'duration': 0, 'redraw': True}, 'mode': 'immediate', 'transition': {'duration': 0}}],
                        'label': 'Pause',
                        'method': 'animate'
                    }
                ],
                'direction': 'left',
                'pad': {'r': 10, 't': 87},
                'showactive': False,
                'type': 'buttons',
                'x': 0.1,
                'xanchor': 'right',
                'y': 0,
                'yanchor': 'top'
            }
        ]
    )

    # Add frames
    frames = [go.Frame(
        data=[go.Bar(y=y_values_list[i], name=f'Frame {i}', marker=dict(color=colors))],
        name=f'Frame {i}'
    ) for i in range(num_frames)]
    fig.frames = frames

    # Display the plot in the notebook
    iplot(fig)

