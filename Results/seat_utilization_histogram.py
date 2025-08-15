import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import json
import os

# Load the data
data_json = {"distribution_data": [{"System": "DeRideFair", "0_seats": 23, "1_seat": 12, "2_seats": 13, "3_seats": 15, "4_seats": 13, "5_seats": 24}, {"System": "DeRide", "0_seats": 22, "1_seat": 10, "2_seats": 7, "3_seats": 10, "4_seats": 6, "5_seats": 45}]}

# Convert to DataFrame and reshape
df = pd.DataFrame(data_json['distribution_data'])

# Reshape data for plotting
seats_categories = ['0_seats', '1_seat', '2_seats', '3_seats', '4_seats', '5_seats']
seat_labels = ['0', '1', '2', '3', '4', '5']

# Extract data for both systems
deridefare_values = [df[df['System'] == 'DeRideFair'][col].iloc[0] for col in seats_categories]
deride_values = [df[df['System'] == 'DeRide'][col].iloc[0] for col in seats_categories]

# Calculate percentages
deridefare_total = sum(deridefare_values)
deride_total = sum(deride_values)
deridefare_pct = [round(v/deridefare_total * 100) for v in deridefare_values]
deride_pct = [round(v/deride_total * 100) for v in deride_values]

# Create the grouped bar chart
fig = go.Figure()

# Add DeRideFair bars
fig.add_trace(go.Bar(
    name='DeRideFair',
    x=seat_labels,
    y=deridefare_values,
    marker_color='#1FB8CD',
    text=[f'{v}<br>({p}%)' for v, p in zip(deridefare_values, deridefare_pct)],
    textposition='outside',
    cliponaxis=False
))

# Add DeRide bars
fig.add_trace(go.Bar(
    name='DeRide',
    x=seat_labels,
    y=deride_values,
    marker_color='#DB4545',
    text=[f'{v}<br>({p}%)' for v, p in zip(deride_values, deride_pct)],
    textposition='outside',
    cliponaxis=False
))

# Update layout
fig.update_layout(
    title='Seat Distribution by System',
    xaxis_title='Filled Seats',
    yaxis_title='Drivers',
    barmode='group',
    legend=dict(orientation='h', yanchor='bottom', y=1.05, xanchor='center', x=0.5)
)

# Get the directory where this script is located
script_dir = os.path.dirname(os.path.abspath(__file__))

# Save the chart in the same directory as the script
output_path = os.path.join(script_dir, 'seat_distribution_histogram.png')
fig.write_image(output_path)
print(f"Chart saved to: {output_path}")