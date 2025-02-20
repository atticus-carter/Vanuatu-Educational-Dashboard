import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import streamlit as st

def create_bar_chart(data: pd.DataFrame, column: str):
    """
    Creates a bar chart using Plotly.

    Args:
        data (pd.DataFrame): The DataFrame containing the data.
        column (str): The column to be displayed on the bar chart.

    Returns:
        plotly.graph_objects.Figure: The bar chart figure.
    """
    try:
        fig = px.bar(data, x=data.index, y=column, title=f"Bar Chart of {column}")
        return fig
    except Exception as e:
        st.error(f"Error creating bar chart: {e}")
        return None

def create_scatter_plot(data: pd.DataFrame, column: str):
    """
    Creates a scatter plot using Plotly.

    Args:
        data (pd.DataFrame): The DataFrame containing the data.
        column (str): The column to be displayed on the scatter plot.

    Returns:
        plotly.graph_objects.Figure: The scatter plot figure.
    """
    try:
        fig = px.scatter(data, x=data.index, y=column, title=f"Scatter Plot of {column}")
        return fig
    except Exception as e:
        st.error(f"Error creating scatter plot: {e}")
        return None

def display_table(data: pd.DataFrame):
    """
    Displays a pandas DataFrame as a Streamlit table.

    Args:
        data (pd.DataFrame): The DataFrame to be displayed.
    """
    st.dataframe(data)

def create_enrollment_trend(data):
    """Creates a line plot showing enrollment trends by province."""
    fig = px.line(data, 
                  x=data.columns[0],  # First column contains years
                  y=['Unnamed: 1', 'Unnamed: 2', 'Unnamed: 3'],  # Use actual column names
                  title='Enrollment Trends',
                  labels={'value': 'Number of Students', 'variable': 'Category'})
    return fig

def create_teacher_distribution(data):
    """Creates a stacked bar chart showing teacher distribution."""
    teacher_summary = data.groupby('Province').agg({
        'ECE': 'sum',
        'PS': 'sum',
        'PSET': 'sum',
        'SC': 'sum',
        'SS': 'sum'
    }).reset_index()
    
    fig = px.bar(teacher_summary,
                 x='Province',
                 y=['ECE', 'PS', 'PSET', 'SC', 'SS'],
                 title='Teacher Distribution by Province and Level',
                 labels={'value': 'Number of Teachers', 'variable': 'Education Level'},
                 barmode='stack')
    return fig

def create_gender_ratio_plot(data, data_type="enrollment"):
    """Creates a bar chart comparing gender ratios."""
    try:
        if data_type == "enrollment":
            # Extract gender data from enrollment data
            gender_data = data[data['Province'].isin(['F', 'M'])].copy()
            gender_data = gender_data.rename(columns={'Province': 'Gender'})
            gender_summary = gender_data.groupby(['Gender', 'Province'])['Total'].sum().unstack()
        elif data_type == "teacher":
            # Extract gender data from teacher data
            gender_summary = data.groupby(['Province', 'Gender'])['Total'].sum().unstack()
        else:
            st.error("Invalid data_type specified.")
            return None

        # Create the bar chart
        fig = px.bar(gender_summary,
                     title='Gender Distribution by Province',
                     barmode='group')
        return fig
    except KeyError as e:
        print(f"KeyError in create_gender_ratio_plot: {e}")
        return None
    except Exception as e:
        print(f"Error creating gender ratio plot: {e}")
        return None

def create_enrollment_heatmap(data):
    """Creates a heatmap of enrollment numbers."""
    numeric_cols = data.select_dtypes(include=['float64', 'int64']).columns
    fig = go.Figure(data=go.Heatmap(
        z=data[numeric_cols].values,
        x=numeric_cols,
        y=data.iloc[:, 0],  # First column contains Province names
        colorscale='RdYlBu'))
    fig.update_layout(title='Enrollment Heatmap by Grade and Province')
    return fig

def create_percentage_plot(data, year_cols):
    """Creates a plot showing percentages over time."""
    if not all(col in data.columns for col in year_cols):
        available_cols = [col for col in year_cols if col in data.columns]
        year_cols = available_cols
    
    fig = px.line(data, 
                  x=data.index,
                  y=year_cols,
                  title='Percentage Trends Over Time',
                  labels={'value': 'Percentage', 'variable': 'Year'})
    return fig
