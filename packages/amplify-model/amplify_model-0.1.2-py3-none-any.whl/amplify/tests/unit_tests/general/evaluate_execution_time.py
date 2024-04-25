import statistics
import os
import sys
import pandas as pd
import plotly.graph_objects as go

execution_times = []
with open(os.path.join(sys.path[0],'execution_time.csv')) as csv_file:
    csv_str = csv_file.readlines()
    for val in csv_str[0].split(', '):
        if val != '':
            execution_times.append(float(val)*1e3)

print(f'Maximum: {max(execution_times)} ms\n'
      f'Minimum: {min(execution_times)} ms\n'
      f'Average: {statistics.mean(execution_times)} ms\n'
      f'Stdev: {statistics.stdev(execution_times)} ms')

### Box plot
df_execution_times = pd.DataFrame(columns=['time_s'], data=execution_times)

fig = go.Figure()
fig.add_trace(
    go.Box(
        y=df_execution_times["time_s"],
        boxpoints=False,
        name='Amplify',
    )
)
fig.update_yaxes(
            range=[0, 2], 
            title="Calculation time in ms"
        )
fig.update_layout(
            showlegend=False,
            font_size=20,
        )
fig.show()
