import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import numpy as np
import json
import os

# Parse the data
data_json = {"fairness_data": [{"driver_id": "d1", "deride_fair_seats": 0, "deride_fair_deviation": -2.55, "deride_seats": 0, "deride_deviation": -3.03}, {"driver_id": "d2", "deride_fair_seats": 1, "deride_fair_deviation": -1.55, "deride_seats": 2, "deride_deviation": -1.03}, {"driver_id": "d3", "deride_fair_seats": 5, "deride_fair_deviation": 2.45, "deride_seats": 5, "deride_deviation": 1.97}]}

fairness_data = data_json["fairness_data"]

# Create lists for each system
deride_fair_seats = []
deride_fair_deviations = []
deride_seats = []
deride_deviations = []
driver_ids = []

for item in fairness_data:
    driver_ids.append(item["driver_id"])
    deride_fair_seats.append(item["deride_fair_seats"])
    deride_fair_deviations.append(item["deride_fair_deviation"])
    deride_seats.append(item["deride_seats"])
    deride_deviations.append(item["deride_deviation"])

# Create the figure
fig = go.Figure()

# Add DeRideFair scatter points with larger markers and circle shape
fig.add_trace(go.Scatter(
    x=deride_fair_seats,
    y=deride_fair_deviations,
    mode='markers',
    name='DeRideFair',
    marker=dict(
        color='#1FB8CD', 
        size=12,
        symbol='circle',
        line=dict(width=1, color='white')
    ),
    hovertemplate='Seats: %{x}<br>Deviation: %{y:.2f}<extra></extra>',
    cliponaxis=False
))

# Add DeRide scatter points with larger markers and diamond shape
fig.add_trace(go.Scatter(
    x=deride_seats,
    y=deride_deviations,
    mode='markers',
    name='DeRide',
    marker=dict(
        color='#DB4545', 
        size=12,
        symbol='diamond',
        line=dict(width=1, color='white')
    ),
    hovertemplate='Seats: %{x}<br>Deviation: %{y:.2f}<extra></extra>',
    cliponaxis=False
))

# Add trend lines
# For DeRideFair
if len(deride_fair_seats) > 1:
    z_fair = np.polyfit(deride_fair_seats, deride_fair_deviations, 1)
    p_fair = np.poly1d(z_fair)
    x_trend = np.linspace(0, 5, 100)
    fig.add_trace(go.Scatter(
        x=x_trend,
        y=p_fair(x_trend),
        mode='lines',
        name='DeRideFair Trend',
        line=dict(color='#1FB8CD', dash='dash', width=2),
        showlegend=False,
        hoverinfo='skip',
        cliponaxis=False
    ))

# For DeRide
if len(deride_seats) > 1:
    z_deride = np.polyfit(deride_seats, deride_deviations, 1)
    p_deride = np.poly1d(z_deride)
    fig.add_trace(go.Scatter(
        x=x_trend,
        y=p_deride(x_trend),
        mode='lines',
        name='DeRide Trend',
        line=dict(color='#DB4545', dash='dash', width=2),
        showlegend=False,
        hoverinfo='skip',
        cliponaxis=False
    ))

# Add horizontal line at y=0
fig.add_hline(y=0, line_dash="solid", line_color="gray", line_width=1)

# Update layout
fig.update_layout(
    title='Load Fairness: DeRideFair vs DeRide',
    xaxis_title='Filled Seats',
    yaxis_title='Deviation',
    legend=dict(orientation='h', yanchor='bottom', y=1.05, xanchor='center', x=0.5)
)

# Update axes with better scaling to reduce white space
all_y_values = deride_fair_deviations + deride_deviations
y_min = min(all_y_values) - 0.5
y_max = max(all_y_values) + 0.5

fig.update_xaxes(range=[-0.3, 5.3])
fig.update_yaxes(range=[y_min, y_max])

# Get the directory where this script is located
script_dir = os.path.dirname(os.path.abspath(__file__))

# Save the chart in the same directory as the script
output_path = os.path.join(script_dir, "load_fairness_comparison.png")
fig.write_image(output_path)
print(f"Chart saved to: {output_path}")