import pandas as pd
import plotly.express as px
import streamlit as st

def format_number(num):
    """Format large numbers with commas"""
    if pd.isna(num):
        return "N/A"
    return f"{int(num):,}"

def calculate_vote_percentage(votes, total_votes):
    """Calculate vote percentage"""
    if pd.isna(votes) or pd.isna(total_votes) or total_votes == 0:
        return 0
    return (votes / total_votes) * 100

def get_winner_by_constituency(df, state, constituency):
    """Get winner for a specific constituency"""
    constituency_data = df[(df['State'] == state) & (df['PC Name'] == constituency)]
    if constituency_data.empty:
        return None
    return constituency_data.loc[constituency_data['Total Votes'].idxmax()]

def create_party_color_map(parties):
    """Create consistent color mapping for parties"""
    colors = px.colors.qualitative.Set3
    return {party: colors[i % len(colors)] for i, party in enumerate(parties)}
