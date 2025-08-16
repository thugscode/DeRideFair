import plotly.graph_objects as go
import pandas as pd
import os

# Get the directory where this script is located
script_dir = os.path.dirname(os.path.abspath(__file__))

# Create the data for all three algorithms, including empty drivers
data = [
    {"Algorithm": "DeRide", "Total_Riders": 335, "Std_Dev": 2.08, "Utilization_Rate": 67.0, "Empty_Drivers": 22},
    {"Algorithm": "DeRideFair", "Total_Riders": 254, "Std_Dev": 1.87, "Utilization_Rate": 50.8, "Empty_Drivers": 23},
    {"Algorithm": "SCIP", "Total_Riders": 345, "Std_Dev": 2.17, "Utilization_Rate": 69.0, "Empty_Drivers": 26}
]

df = pd.DataFrame(data)

# Define the metrics and their abbreviated names for x-axis
metric_labels = ['Total Riders', 'Std Dev', 'Util Rate %', 'Empty Drivers']

# Define colors for the three algorithms
colors = ['#1FB8CD', '#DB4545', '#2E8B57']

fig = go.Figure()

# Create bars for each algorithm
for i, algorithm in enumerate(df['Algorithm']):
    values = [df.loc[i, 'Total_Riders'], df.loc[i, 'Std_Dev'], df.loc[i, 'Utilization_Rate'], df.loc[i, 'Empty_Drivers']]
    text_values = [f'{val}' if val < 10 else f'{int(val)}' for val in values]
    
    fig.add_trace(go.Bar(
        name=algorithm,
        x=metric_labels,
        y=values,
        marker_color=colors[i],
        cliponaxis=False,
        text=text_values,
        textposition='outside',
        hovertemplate='<b>%{fullData.name}</b><br>%{x}: %{y}<extra></extra>'
    ))

# Update layout
fig.update_layout(
    title="Ride-Share Algorithm Comparison",
    xaxis_title="Performance Metrics",
    yaxis_title="Metric Values",
    barmode='group',
    legend=dict(
        orientation='h',
        yanchor='bottom',
        y=1.05,
        xanchor='center',
        x=0.5
    )
)

# Save the chart in the same directory as the script
output_path = os.path.join(script_dir, 'ride_share_performance_chart.png')
fig.write_image(output_path)
print(f"Chart saved to: {output_path}")