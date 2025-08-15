import plotly.graph_objects as go
import pandas as pd
import os

# Get the directory where this script is located
script_dir = os.path.dirname(os.path.abspath(__file__))

# Load the data from the provided JSON
data_json = {"metrics": [{"System": "DeRideFair", "Total_Riders": 255, "Avg_Seats": 2.55, "Std_Dev": 1.90, "Gini_Coeff": 0.4195, "Utilization": 0.510, "Empty_Drivers": 23, "Full_Drivers": 24}, {"System": "DeRide", "Total_Riders": 303, "Avg_Seats": 3.03, "Std_Dev": 2.09, "Gini_Coeff": 0.3711, "Utilization": 0.606, "Empty_Drivers": 22, "Full_Drivers": 45}]}

df = pd.DataFrame(data_json['metrics'])

# Focus on metrics with more comparable scales
metrics = ['Total_Riders', 'Avg_Seats', 'Empty_Drivers', 'Full_Drivers']
metric_labels = ['Total Riders', 'Avg Seats', 'Empty Drivers', 'Full Drivers']

# Brand colors
colors = ['#1FB8CD', '#DB4545']

fig = go.Figure()

# Add bars for each system with data labels
for i, system in enumerate(['DeRideFair', 'DeRide']):
    system_data = df[df['System'] == system].iloc[0]
    values = [system_data[metric] for metric in metrics]
    
    # Format text labels for display
    text_labels = []
    for j, val in enumerate(values):
        if metrics[j] == 'Avg_Seats':
            text_labels.append(f'{val:.2f}')
        else:
            text_labels.append(f'{val}')
    
    fig.add_trace(go.Bar(
        name=system,
        x=metric_labels,
        y=values,
        marker_color=colors[i],
        text=text_labels,
        textposition='outside',
        cliponaxis=False
    ))

# Update layout
fig.update_layout(
    title='DeRideFair vs DeRide Key Metrics',
    xaxis_title='Metrics',
    yaxis_title='Values',
    barmode='group',
    showlegend=True,
    legend=dict(
        orientation='h', 
        yanchor='bottom', 
        y=1.05, 
        xanchor='center', 
        x=0.5
    ),
    yaxis=dict(showgrid=True)
)

# Save the chart in the same directory as the script
output_path = os.path.join(script_dir, 'deride_comparison.png')
fig.write_image(output_path)
print(f"Chart saved to: {output_path}")