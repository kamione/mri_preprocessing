# Environment ------------------------------------------------------------------
from pathlib import Path
import altair as alt
import pandas as pd


# Data I/O
data = pd.read_csv('summary.csv')

# define selection
click = alt.selection_multi(encodings=['color'])

scatter_fd = alt.Chart(data).mark_circle(size=250).encode(
    x=alt.X('sub:Q', title=''),
    y=alt.Y('fd-mean:Q', title='Mean Framewise Displacement'),
    color=alt.Color('task:N',
                    scale=alt.Scale(range=['#E7DECD', '#B9314F', '#312F2F']),
                    legend=None),
    tooltip=[alt.Tooltip('sub:N', title='Subject No.'),
             alt.Tooltip('fd-per:Q', format='.2f', title='>0.2 (%)'),
             alt.Tooltip('fd-mean:Q', format='.4f', title='Mean'),
             alt.Tooltip('fd-std:Q', format='.4f', title='SD'),
             alt.Tooltip('fd-max:Q', format='.4f', title='Max'),
             alt.Tooltip('fd-min:Q', format='.4f', title='Min')]
).properties(
    width=700,
    height=400
).transform_filter(
    click
).interactive()


scatter_dvars = alt.Chart(data).mark_circle(size=250).encode(
    x=alt.X('sub:Q', title=''),
    y=alt.Y('dvars-mean:Q', title='Mean DVARS'),
    color=alt.Color('task:N',
                    scale=alt.Scale(range=['#E7DECD', '#B9314F', '#312F2F']),
                    legend=None),
    tooltip=[alt.Tooltip('sub:N', title='Subject No.'),
             alt.Tooltip('dvars-per:Q', format='.2f', title='>20 (%)'),
             alt.Tooltip('dvars-mean:Q', format='.2f', title='Mean'),
             alt.Tooltip('dvars-std:Q', format='.2f', title='SD'),
             alt.Tooltip('dvars-max:Q', format='.2f', title='Max'),
             alt.Tooltip('dvars-min:Q', format='.2f', title='Min')]
).properties(
    width=700,
    height=400,
).transform_filter(
    click
).interactive()


threshold_fd = alt.Chart(pd.DataFrame({'y': [0.2]})).mark_rule().encode(y='y')
threshold_dvars = alt.Chart(pd.DataFrame(
    {'y': [20]})).mark_rule().encode(y='y')

legend = alt.Chart(data).mark_rect().encode(
    y=alt.Y('task:N', axis=alt.Axis(title='Select Task')),
    color=alt.condition(click, 'task:N',
                        alt.value('lightgray'), legend=None),
    size=alt.value(250)
).properties(
    width=30,
    height=180,
    selection=click
)
chart = (scatter_fd + threshold_fd | scatter_dvars + threshold_dvars | legend)

chart.save('interactive_plot_headmotion.html')
