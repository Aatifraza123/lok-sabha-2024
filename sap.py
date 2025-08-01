import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np
import io
import folium
from streamlit_folium import st_folium
import geopandas as gpd

# Page configuration
st.set_page_config(
    page_title="2024 Lok Sabha Election Analysis",
    page_icon="🗳️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for styling
st.markdown("""

<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/7.0.0/css/all.min.css">
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Poppins:wght@400;500;600;700&display=swap" rel="stylesheet">
<style>
    /* Import your existing styles and enhance them */
    .main-header {
        font-size: 2.5rem;
        color: #FF6B35;
        text-align: center;
        margin-bottom: 2rem;
        font-family: 'Poppins', sans-serif;
        font-weight: 700;
    }
    
    .main-header::before {
        content: " ";
        margin-right: 10px;
    }
    
    .metric-card {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        padding: 1rem;
        border-radius: 10px;
        color: white;
        text-align: center;
        font-family: 'Inter', sans-serif;
        box-shadow: 0 4px 15px rgba(0,0,0,0.2);
        transition: transform 0.3s ease;
    }
    
    .metric-card:hover {
        transform: translateY(-5px);
    }
    
    .metric-card i {
        font-size: 2rem;
        margin-bottom: 0.5rem;
        display: block;
    }
    
    .winner-highlight {
        background-color: #90EE90;
        padding: 0.5rem;
        border-radius: 5px;
        font-weight: bold;
        font-family: 'Inter', sans-serif;
    }
    
    /* Icon-enhanced metric cards */
    .metric-states::before {
        content: "\f024";
        font-family: "Font Awesome 6 Free";
        font-weight: 900;
        color: #ff6b6b;
        font-size: 2rem;
        display: block;
        margin-bottom: 0.5rem;
    }
    
    .metric-constituencies::before {
        content: "\f3c5";
        font-family: "Font Awesome 6 Free";
        font-weight: 900;
        color: #4ecdc4;
        font-size: 2rem;
        display: block;
        margin-bottom: 0.5rem;
    }
    
    .metric-votes::before {
        content: "\f0c0";
        font-family: "Font Awesome 6 Free";
        font-weight: 900;
        color: #45b7d1;
        font-size: 2rem;
        display: block;
        margin-bottom: 0.5rem;
    }
    
    .metric-parties::before {
        content: "\f0e8";
        font-family: "Font Awesome 6 Free";
        font-weight: 900;
        color: #96ceb4;
        font-size: 2rem;
        display: block;
        margin-bottom: 0.5rem;
    }
    
    /* Enhanced sidebar styling */
    .css-1d391kg {
        font-family: 'Inter', sans-serif;
    }
    
    /* Icon classes for various elements */
    .icon-search::before {
        content: "\f002";
        font-family: "Font Awesome 6 Free";
        font-weight: 900;
        margin-right: 8px;
    }
    
    .icon-filter::before {
        content: "\f0b0";
        font-family: "Font Awesome 6 Free";
        font-weight: 900;
        margin-right: 8px;
    }
    
    .icon-chart::before {
        content: "\f080";
        font-family: "Font Awesome 6 Free";
        font-weight: 900;
        margin-right: 8px;
    }
    
    .icon-download::before {
        content: "\f019";
        font-family: "Font Awesome 6 Free";
        font-weight: 900;
        margin-right: 8px;
    }
    
    /* Button enhancements */
    .stButton > button {
        font-family: 'Inter', sans-serif;
        font-weight: 500;
    }
    
    /* Header improvements */
    h1, h2, h3, h4, h5, h6 {
        font-family: 'Poppins', sans-serif;
    }
    
    /* Body text */
    .stMarkdown, .stText {
        font-family: 'Inter', sans-serif;
    }
    
    /* Custom icon button style */
    .icon-button {
        background: linear-gradient(45deg, #667eea, #764ba2);
        color: white;
        border: none;
        padding: 10px 20px;
        border-radius: 8px;
        font-family: 'Inter', sans-serif;
        font-weight: 500;
        cursor: pointer;
        transition: all 0.3s ease;
    }
    
    .icon-button:hover {
        transform: translateY(-2px);
        box-shadow: 0 5px 15px rgba(0,0,0,0.2);
    }
</style>
""", unsafe_allow_html=True)

st.markdown("""
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/7.0.0/css/all.min.css">
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Poppins:wght@400;500;600;700&display=swap" rel="stylesheet">
<style>
    .main-header {
        font-size: 2.5rem;
        color: #FF6B35;
        text-align: center;
        margin-bottom: 2rem;
        font-family: 'Poppins', sans-serif;
        font-weight: 700;
    }
    .metric-card {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        padding: 1rem;
        border-radius: 10px;
        color: white;
        text-align: center;
        font-family: 'Inter', sans-serif;
        box-shadow: 0 4px 15px rgba(0,0,0,0.2);
        transition: transform 0.3s ease;
    }
    .metric-card:hover {
        transform: translateY(-5px);
    }
    .winner-highlight {
        background-color: #90EE90;
        padding: 0.5rem;
        border-radius: 5px;
        font-weight: bold;
        font-family: 'Inter', sans-serif;
    }
    h1, h2, h3, h4, h5, h6 {
        font-family: 'Poppins', sans-serif;
    }
    .stMarkdown, .stText {
        font-family: 'Inter', sans-serif;
    }
</style>
""", unsafe_allow_html=True)






@st.cache_data
def load_data():
    """Load and process the election data"""
    try:
        df = pd.read_csv("results_2024.csv")
        # Clean column names
        df.columns = df.columns.str.strip()
        
        # Convert numeric columns
        numeric_cols = ['EVM Votes', 'Postal Votes', 'Total Votes', 'Vote Share']
        for col in numeric_cols:
            if col in df.columns:
                df[col] = pd.to_numeric(df[col], errors='coerce')
        
        # Calculate total votes if not present
        if 'Total Votes' not in df.columns:
            df['Total Votes'] = df['EVM Votes'] + df['Postal Votes']
        
        # Identify winners (candidate with highest votes in each constituency)
        df['Winner'] = df.groupby(['State', 'PC Name'])['Total Votes'].transform('max') == df['Total Votes']
        
        return df
    except Exception as e:
        st.error(f"Error loading data: {str(e)}")
        return None




def calculate_dashboard_metrics(df):
    """Calculate key metrics for the dashboard from the processed DataFrame."""
    
    # Basic Counts
    total_states = df['State'].nunique()
    total_constituencies = df['PC Name'].nunique()
    total_votes = df['Total Votes'].sum()
    total_candidates = df[df['Party'] != 'None of the Above'].shape[0]

    # Winner Analysis
    winners_df = df[df['Winner'] == True]
    party_wins = winners_df['Party'].value_counts()
    max_wins_party = party_wins.index[0] if not party_wins.empty else "N/A"
    max_wins_count = party_wins.iloc[0] if not party_wins.empty else 0
    
    # Margin Calculation
    margins = []
    for const in df['PC Name'].unique():
        const_df = df[df['PC Name'] == const].nlargest(2, 'Total Votes')
        if len(const_df) > 1:
            margin = const_df.iloc[0]['Total Votes'] - const_df.iloc[1]['Total Votes']
            margins.append({'PC Name': const, 'Margin': margin, 'Winner': const_df.iloc[0]['Candidate']})
    
    margin_df = pd.DataFrame(margins)
    largest_margin = margin_df.nlargest(1, 'Margin').iloc[0] if not margin_df.empty else None

    # Turnout Calculation
    constituency_turnout = df.groupby('PC Name')['Total Votes'].sum()
    highest_turnout_const = constituency_turnout.idxmax() if not constituency_turnout.empty else "N/A"
    
    return {
        'total_states': total_states,
        'total_constituencies': total_constituencies,
        'total_votes': total_votes,
        'total_candidates': total_candidates,
        'max_wins_party': max_wins_party,
        'max_wins_count': max_wins_count,
        'largest_margin_winner': f"{largest_margin['Winner']} ({largest_margin['Margin']:,})",
        'highest_turnout_const': highest_turnout_const,
        'party_wins': party_wins,
        'margin_df': margin_df
    }

def create_party_performance_chart(party_wins):
    """Create a horizontal bar chart for party performance."""
    top_parties = party_wins.head(10)
    
    colors = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4', '#FFEAA7', 
              '#DDA0DD', '#98D8C8', '#FFB6C1', '#87CEEB', '#F0E68C']
    
    fig = px.bar(
        x=top_parties.values,
        y=top_parties.index,
        orientation='h',
        title="Top 10 Parties by Seats Won",
        labels={'x': 'Seats Won', 'y': 'Party'},
        color=top_parties.values,
        color_continuous_scale='viridis'
    )
    
    fig.update_layout(
        height=400,
        showlegend=False,
        title_font_size=16,
        title_x=0.5,
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)'
    )
    
    fig.update_traces(
        texttemplate='%{x}',
        textposition='outside',
        marker_line_color='white',
        marker_line_width=1
    )
    
    return fig

def create_margin_distribution_chart(margin_df):
    """Create a histogram showing distribution of victory margins."""
    fig = px.histogram(
        margin_df,
        x='Margin',
        nbins=30,
        title="Distribution of Victory Margins",
        labels={'Margin': 'Victory Margin (Votes)', 'count': 'Number of Constituencies'},
        color_discrete_sequence=['#FF6B6B']
    )
    
    fig.update_layout(
        height=300,
        title_font_size=16,
        title_x=0.5,
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)'
    )
    
    return fig

def create_top_margins_chart(margin_df):
    """Create a bar chart showing top 10 victory margins."""
    top_margins = margin_df.nlargest(10, 'Margin')
    
    fig = px.bar(
        top_margins,
        x='PC Name',
        y='Margin',
        title="Top 10 Largest Victory Margins",
        labels={'Margin': 'Victory Margin (Votes)', 'PC Name': 'Constituency'},
        color='Margin',
        color_continuous_scale='Reds'
    )
    
    fig.update_layout(
        height=400,
        title_font_size=16,
        title_x=0.5,
        xaxis_tickangle=-45,
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)'
    )
    
    return fig


def dashboard_overview(df):
    """Display the enhanced dashboard overview with styled metric cards and visualizations."""
    
    # Enhanced CSS styling
    st.markdown("""
    <style>
    .main-header {
        color: #2E86AB;
        text-align: center;
        padding: 20px 0;
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 2.5rem;
        font-weight: bold;
        margin-bottom: 30px;
    }
    
    .metric-card {
        background: linear-gradient(135deg, #0ba360 0%, #764ba2 100%);
        
        padding: 20px;
        border-radius: 15px;
        box-shadow: 0 8px 32px rgba(102, 126, 234, 0.3);
        margin: 10px 0;
        border: 1px solid rgba(255, 255, 255, 0.2);
        backdrop-filter: blur(10px);
        transition: transform 0.3s ease;
    }
    
    .metric-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 12px 40px rgba(102, 126, 234, 0.4);
    }
    
    .metric-card-icon {
        font-size: 2rem;
        text-align: center;
        margin-bottom: 10px;
        filter: drop-shadow(0 2px 4px rgba(0,0,0,0.3));
    }
    
    .metric-value {
        font-size: 1.8rem;
        font-weight: bold;
        color: white;
        text-align: center;
        margin: 10px 0;
    }
    
    .metric-label {
        color: rgba(255, 255, 255, 0.9);
        text-align: center;
        font-size: 0.9rem;
        margin-bottom: 5px;
    }
    
    .section-header {
        color: #2E86AB;
        font-size: 1.5rem;
        font-weight: bold;
        margin: 30px 0 20px 0;
        padding-bottom: 10px;
        border-bottom: 2px solid #667eea;
    }
    
    .chart-container {
        background: white;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 4px 20px rgba(0,0,0,0.1);
        margin: 20px 0;
    }
    </style>
    """, unsafe_allow_html=True)
    
    st.markdown('<h1 class="main-header">🗳️ 2024 Lok Sabha Election Analysis Dashboard</h1>', unsafe_allow_html=True)
    
    metrics = calculate_dashboard_metrics(df)

    # --- Display Metrics in Two Rows ---
    st.markdown('<div class="section-header">📊 National Snapshot</div>', unsafe_allow_html=True)
    
    row1_col1, row1_col2, row1_col3, row1_col4 = st.columns(4)
    
    with row1_col1:
        st.markdown(f'''
        <div class="metric-card">
            <div class="metric-card-icon">🗺️</div>
            <div class="metric-value">{metrics['total_states']}</div>
            <div class="metric-label">Total States/UTs</div>
        </div>
        ''', unsafe_allow_html=True)
    
    with row1_col2:
        st.markdown(f'''
        <div class="metric-card">
            <div class="metric-card-icon">🏛️</div>
            <div class="metric-value">543</div>
            <div class="metric-label">Constituencies</div>
        </div>
        ''', unsafe_allow_html=True)
    
    with row1_col3:
        st.markdown(f'''
        <div class="metric-card">
            <div class="metric-card-icon">✋</div>
            <div class="metric-value">{metrics['total_votes']:,}</div>
            <div class="metric-label">Total Votes Cast</div>
        </div>
        ''', unsafe_allow_html=True)
        
    with row1_col4:
        st.markdown(f'''
        <div class="metric-card">
            <div class="metric-card-icon">👥</div>
            <div class="metric-value">{metrics['total_candidates']:,}</div>
            <div class="metric-label">Total Candidates</div>
        </div>
        ''', unsafe_allow_html=True)

    # Second row of metrics
    row2_col1, row2_col2, row2_col3 = st.columns(3)

    with row2_col1:
        st.markdown(f'''
        <div class="metric-card">
            <div class="metric-card-icon">🏆</div>
            <div class="metric-value">{metrics['max_wins_party']}</div>
            <div class="metric-label">Leading Party ({metrics['max_wins_count']} Seats)</div>
        </div>
        ''', unsafe_allow_html=True)
        
    with row2_col2:
        st.markdown(f'''
        <div class="metric-card">
            <div class="metric-card-icon">📈</div>
            <div class="metric-value" style="font-size: 1.2rem;">{metrics['largest_margin_winner']}</div>
            <div class="metric-label">Largest Victory Margin</div>
        </div>
        ''', unsafe_allow_html=True)
        
    with row2_col3:
        st.markdown(f'''
        <div class="metric-card">
            <div class="metric-card-icon">🔝</div>
            <div class="metric-value" style="font-size: 1.3rem;">{metrics['highest_turnout_const']}</div>
            <div class="metric-label">Highest Turnout Constituency</div>
        </div>
        ''', unsafe_allow_html=True)

    # --- Visualizations Section ---
    st.markdown('<div class="section-header">📈 Performance Analytics</div>', unsafe_allow_html=True)
    
    # Party Performance Chart
    col1, col2 = st.columns([2, 1])
    
    with col1:
        party_chart = create_party_performance_chart(metrics['party_wins'])
        st.plotly_chart(party_chart, use_container_width=True)
    
    with col2:
        # Create a donut chart for top 5 parties
        top_5_parties = metrics['party_wins'].head(5)
        fig_donut = px.pie(
            values=top_5_parties.values,
            names=top_5_parties.index,
            title="Top 5 Parties Distribution",
            hole=0.4,
            color_discrete_sequence=px.colors.qualitative.Set3
        )
        fig_donut.update_layout(
            height=400,
            title_font_size=14,
            title_x=0.5
        )
        st.plotly_chart(fig_donut, use_container_width=True)

    # Victory Margins Analysis
    st.markdown('<div class="section-header">🎯 Victory Margin Analysis</div>', unsafe_allow_html=True)
    
    col3, col4 = st.columns(2)
    
    with col3:
        margin_dist_chart = create_margin_distribution_chart(metrics['margin_df'])
        st.plotly_chart(margin_dist_chart, use_container_width=True)
    
    with col4:
        # Summary statistics for margins
        margin_stats = metrics['margin_df']['Margin'].describe()
        st.markdown("### Victory Margin Statistics")
        
        stats_col1, stats_col2 = st.columns(2)
        with stats_col1:
            st.metric("Average Margin", f"{margin_stats['mean']:,.0f}")
            st.metric("Median Margin", f"{margin_stats['50%']:,.0f}")
        
        with stats_col2:
            st.metric("Largest Margin", f"{margin_stats['max']:,.0f}")
            st.metric("Smallest Margin", f"{margin_stats['min']:,.0f}")

    # Top Margins Chart
    top_margins_chart = create_top_margins_chart(metrics['margin_df'])
    st.plotly_chart(top_margins_chart, use_container_width=True)

    # Additional insights
    st.markdown('<div class="section-header">💡 Key Insights</div>', unsafe_allow_html=True)
    
    insight_col1, insight_col2, insight_col3 = st.columns(3)
    
    with insight_col1:
        close_contests = len(metrics['margin_df'][metrics['margin_df']['Margin'] < 5000])
        st.info(f"🔥 **Close Contests:** {close_contests} constituencies decided by less than 5,000 votes")
    
    with insight_col2:
        landslide_wins = len(metrics['margin_df'][metrics['margin_df']['Margin'] > 100000])
        st.success(f"🏆 **Landslide Victories:** {landslide_wins} constituencies won by more than 1 lakh votes")
    
    with insight_col3:
        # Fixed calculation using 543 constituencies
        avg_candidates_per_seat = metrics['total_candidates'] / 543
        st.warning(f"👥 **Competition Level:** Average {avg_candidates_per_seat:.1f} candidates per constituency")




# ---------





def constituency_results(df):
    """Display constituency-wise results with enhanced visualizations"""
    st.header("🏛️ Constituency-wise Results")
    
    col1, col2 = st.columns(2)
    
    with col1:
        selected_state = st.selectbox("Select State/UT", sorted(df['State'].unique()))
    
    with col2:
        constituencies = sorted(df[df['State'] == selected_state]['PC Name'].unique())
        selected_constituency = st.selectbox("Select Constituency", constituencies)
    
    # Filter data for selected constituency
    constituency_data = df[(df['State'] == selected_state) & 
                          (df['PC Name'] == selected_constituency)].copy()
    
    if not constituency_data.empty:
        constituency_data = constituency_data.sort_values('Total Votes', ascending=False)
        
        st.subheader(f"Results for {selected_constituency}, {selected_state}")
        
        # Key Statistics at the top
        total_votes_constituency = constituency_data['Total Votes'].sum()
        total_candidates = len(constituency_data)
        winner = constituency_data.iloc[0]
        
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Total Votes", f"{total_votes_constituency:,}")
        with col2:
            st.metric("Total Candidates", total_candidates)
        with col3:
            st.metric("Winner", winner['Candidate'])
        with col4:
            st.metric("Winning Party", winner['Party'])
        
      


    #   Display results in a formatted table
        st.subheader("📋 Candidate Performance")
        for idx, row in constituency_data.iterrows():
            if row['Winner']:
                st.markdown(f"""
                <div style="background-color: #90EE90; padding: 10px; border-radius: 5px; margin: 5px 0;">
                    🏆 WINNER: <b>{row['Candidate']}</b> ({row['Party']}) - {row['Total Votes']:,} votes ({row['Vote Share']:.2f}%)
                </div>
                """, unsafe_allow_html=True)
               
            else:
                st.markdown(f"""
                <div style="background-color: #f0f0f0; padding: 8px; border-radius: 5px; margin: 3px 0;">
                    • <b>{row['Candidate']}</b> ({row['Party']}) - {row['Total Votes']:,} votes ({row['Vote Share']:.2f}%)
                </div>
                """, unsafe_allow_html=True)


        
        # Victory margin analysis
        if len(constituency_data) > 1:
            margin = constituency_data.iloc[0]['Total Votes'] - constituency_data.iloc[1]['Total Votes']
            margin_percentage = (margin / total_votes_constituency) * 100
            runner_up = constituency_data.iloc[1]
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Victory Margin", f"{margin:,} votes")
            with col2:
                st.metric("Margin %", f"{margin_percentage:.2f}%")
            with col3:
                st.metric("Runner-up", runner_up['Candidate'])
        
        # Comprehensive Visualizations
        st.header("📊 Visual Analysis")
        
        # 1. Main Vote Distribution Charts
        col1, col2 = st.columns(2)
        
        with col1:
            # Bar chart showing vote distribution
            fig_bar = px.bar(
                constituency_data, 
                x='Candidate', 
                y='Total Votes',
                color='Party',
                title=f"Vote Distribution - {selected_constituency}",
                labels={'Total Votes': 'Total Votes', 'Candidate': 'Candidate'},
                text='Total Votes'
            )
            fig_bar.update_traces(texttemplate='%{text:,}', textposition='outside')
            fig_bar.update_xaxes(tickangle=45)
            fig_bar.update_layout(height=500)
            st.plotly_chart(fig_bar, use_container_width=True)
        
        with col2:
            # Pie chart showing vote share
            fig_pie = px.pie(
                constituency_data,
                values='Total Votes',
                names='Candidate',
                title=f"Vote Share Distribution - {selected_constituency}",
                color_discrete_sequence=px.colors.qualitative.Set3
            )
            fig_pie.update_traces(textposition='inside', textinfo='percent+label')
            fig_pie.update_layout(height=500)
            st.plotly_chart(fig_pie, use_container_width=True)
        
        # 2. Vote Share Analysis
        st.subheader("📈 Vote Share Analysis")
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Horizontal bar chart for better readability
            fig_horizontal = px.bar(
                constituency_data,
                x='Vote Share',
                y='Candidate',
                orientation='h',
                color='Party',
                title="Vote Share Percentage by Candidate",
                labels={'Vote Share': 'Vote Share (%)', 'Candidate': 'Candidate'},
                text='Vote Share'
            )
            fig_horizontal.update_traces(texttemplate='%{text:.1f}%', textposition='outside')
            fig_horizontal.update_layout(height=max(400, len(constituency_data) * 40))
            st.plotly_chart(fig_horizontal, use_container_width=True)
        
        with col2:
            # Donut chart for party-wise vote aggregation
            party_votes = constituency_data.groupby('Party')['Total Votes'].sum().reset_index()
            fig_donut = px.pie(
                party_votes,
                values='Total Votes',
                names='Party',
                title="Party-wise Vote Distribution",
                hole=0.4
            )
            fig_donut.update_traces(textposition='inside', textinfo='percent+label')
            st.plotly_chart(fig_donut, use_container_width=True)
        
        # 3. Performance Metrics Visualization
        st.subheader("🎯 Performance Metrics")
        
        # Create performance comparison chart
        performance_data = constituency_data.copy()
        performance_data['Position'] = range(1, len(performance_data) + 1)
        performance_data['Performance_Score'] = (performance_data['Vote Share'] / performance_data['Vote Share'].max()) * 100
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Scatter plot showing votes vs vote share
            fig_scatter = px.scatter(
                performance_data,
                x='Total Votes',
                y='Vote Share',
                size='Total Votes',
                color='Party',
                hover_data=['Candidate'],
                title="Votes vs Vote Share Analysis",
                labels={'Total Votes': 'Total Votes', 'Vote Share': 'Vote Share (%)'}
            )
            fig_scatter.update_layout(height=400)
            st.plotly_chart(fig_scatter, use_container_width=True)
        
        with col2:
            # Performance score radar chart for top 5 candidates
            top_5 = performance_data.head(5)
            
            fig_radar = go.Figure()
            
            for idx, candidate in top_5.iterrows():
                fig_radar.add_trace(go.Scatterpolar(
                    r=[candidate['Vote Share'], candidate['Performance_Score'], 
                       100 - (candidate['Position'] - 1) * 20],  # Position score (inverted)
                    theta=['Vote Share', 'Performance Score', 'Position Score'],
                    fill='toself',
                    name=candidate['Candidate'][:15] + ('...' if len(candidate['Candidate']) > 15 else '')
                ))
            
            fig_radar.update_layout(
                polar=dict(
                    radialaxis=dict(visible=True, range=[0, 100])
                ),
                showlegend=True,
                title="Top 5 Candidates Performance Radar",
                height=400
            )
            st.plotly_chart(fig_radar, use_container_width=True)
        
        # 4. Margin Analysis
        if len(constituency_data) > 1:
            st.subheader("⚖️ Victory Margin Analysis")
            
            # Calculate margins between consecutive candidates
            margins_data = []
            for i in range(len(constituency_data) - 1):
                current = constituency_data.iloc[i]
                next_candidate = constituency_data.iloc[i + 1]
                margin = current['Total Votes'] - next_candidate['Total Votes']
                margins_data.append({
                    'Between': f"{current['Candidate'][:10]}... vs {next_candidate['Candidate'][:10]}...",
                    'Margin': margin,
                    'Percentage': (margin / total_votes_constituency) * 100
                })
            
            margins_df = pd.DataFrame(margins_data)
            
            col1, col2 = st.columns(2)
            
            with col1:
                fig_margins = px.bar(
                    margins_df,
                    x='Between',
                    y='Margin',
                    title="Vote Margins Between Consecutive Candidates",
                    labels={'Margin': 'Vote Margin', 'Between': 'Candidates'},
                    text='Margin'
                )
                fig_margins.update_traces(texttemplate='%{text:,}', textposition='outside')
                fig_margins.update_xaxes(tickangle=45)
                st.plotly_chart(fig_margins, use_container_width=True)
            
            with col2:
                # Cumulative vote percentage
                constituency_data['Cumulative_Votes'] = constituency_data['Total Votes'].cumsum()
                constituency_data['Cumulative_Percentage'] = (constituency_data['Cumulative_Votes'] / total_votes_constituency) * 100
                
                fig_cumulative = px.line(
                    constituency_data,
                    x=range(1, len(constituency_data) + 1),
                    y='Cumulative_Percentage',
                    title="Cumulative Vote Percentage",
                    labels={'x': 'Candidate Rank', 'y': 'Cumulative Vote %'},
                    markers=True
                )
                fig_cumulative.update_layout(xaxis_title="Candidate Position")
                st.plotly_chart(fig_cumulative, use_container_width=True)
        
        # 5. Party Performance Summary
        if len(constituency_data['Party'].unique()) > 1:
            st.subheader("🏛️ Party Performance Summary")
            
            party_summary = constituency_data.groupby('Party').agg({
                'Total Votes': ['sum', 'count'],
                'Vote Share': 'sum'
            }).round(2)
            
            party_summary.columns = ['Total Votes', 'Candidates', 'Total Vote Share']
            party_summary = party_summary.reset_index()
            party_summary['Avg Votes per Candidate'] = (party_summary['Total Votes'] / party_summary['Candidates']).round(0)
            
            # Display party summary table
            st.dataframe(party_summary, use_container_width=True)
            
            # Party performance bar chart
            fig_party_performance = px.bar(
                party_summary,
                x='Party',
                y='Total Votes',
                color='Candidates',
                title="Party-wise Total Votes and Candidate Count",
                labels={'Total Votes': 'Total Votes', 'Party': 'Party', 'Candidates': 'Number of Candidates'},
                text='Total Votes'
            )
            fig_party_performance.update_traces(texttemplate='%{text:,}', textposition='outside')
            st.plotly_chart(fig_party_performance, use_container_width=True)
        
        # 6. Competition Intensity Analysis
        st.subheader("🔥 Competition Intensity")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            # Competition metrics
            vote_spread = constituency_data['Total Votes'].max() - constituency_data['Total Votes'].min()
            st.metric("Vote Spread", f"{vote_spread:,}")
        
        with col2:
            # Average vote share
            avg_vote_share = constituency_data['Vote Share'].mean()
            st.metric("Avg Vote Share", f"{avg_vote_share:.2f}%")
        
        with col3:
            # Competitiveness index (lower margin = more competitive)
            if len(constituency_data) > 1:
                competitiveness = 100 - margin_percentage
                st.metric("Competitiveness", f"{competitiveness:.1f}%")
        
        # 7. Insights and Summary
        st.subheader("🔍 Key Insights")
        
        insights = []
        
        # Winner analysis
        insights.append(f"🏆 **{winner['Candidate']}** from **{winner['Party']}** won with **{winner['Total Votes']:,} votes** ({winner['Vote Share']:.2f}% vote share)")
        
        # Margin analysis
        if len(constituency_data) > 1:
            if margin_percentage < 5:
                insights.append(f"🔥 **Close Contest**: Victory margin of only {margin_percentage:.2f}% indicates a highly competitive race")
            elif margin_percentage > 20:
                insights.append(f"💪 **Dominant Victory**: {margin_percentage:.2f}% margin shows strong candidate support")
            else:
                insights.append(f"⚖️ **Moderate Victory**: {margin_percentage:.2f}% margin indicates decent lead")
        
        # Party performance
        unique_parties = len(constituency_data['Party'].unique())
        insights.append(f"🏛️ **{unique_parties} different parties** contested in this constituency")
        
        # Vote concentration
        top_3_share = constituency_data.head(3)['Vote Share'].sum()
        insights.append(f"📊 Top 3 candidates secured **{top_3_share:.1f}%** of total votes")
        
        # Turnout quality
        if constituency_data['Vote Share'].iloc[0] > 50:
            insights.append(f"✅ **Clear Mandate**: Winner secured majority with {constituency_data['Vote Share'].iloc[0]:.1f}% vote share")
        else:
            insights.append(f"📈 **Fractured Mandate**: Winner secured {constituency_data['Vote Share'].iloc[0]:.1f}% vote share (less than 50%)")
        
        for insight in insights:
            st.write(insight)
        
        # 8. Export Options
        st.subheader("📥 Export Options")
        
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("Export Constituency Results"):
                csv = constituency_data.to_csv(index=False)
                st.download_button(
                    label="Download Detailed Results CSV",
                    data=csv,
                    file_name=f"{selected_constituency}_{selected_state}_results.csv",
                    mime="text/csv"
                )
        
        with col2:
            if st.button("Export Party Summary"):
                if 'party_summary' in locals():
                    party_csv = party_summary.to_csv(index=False)
                    st.download_button(
                        label="Download Party Summary CSV",
                        data=party_csv,
                        file_name=f"{selected_constituency}_party_summary.csv",
                        mime="text/csv"
                    )
    
    else:
        st.warning("No data found for the selected constituency.")





def party_analysis(df):
    """Display party-wise analysis"""
    st.header("🎯 Party-wise Analysis")
    
    # Calculate party statistics
    winners_df = df[df['Winner'] == True]
    party_seats = winners_df['Party'].value_counts()
    party_votes = df.groupby('Party')['Total Votes'].sum().sort_values(ascending=False)
    party_vote_share = df.groupby('Party')['Vote Share'].mean().sort_values(ascending=False)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Seats Won by Party")
        seats_fig = px.bar(x=party_seats.values, y=party_seats.index, 
                          orientation='h', title="Seats per Party")
        seats_fig.update_layout(yaxis={'categoryorder':'total ascending'})
        st.plotly_chart(seats_fig, use_container_width=True)
    
    with col2:
        st.subheader("Vote Share Distribution")
        # Top 10 parties by total votes
        top_parties = party_votes.head(10)
        pie_fig = px.pie(values=top_parties.values, names=top_parties.index, 
                        title="Vote Share by Top 10 Parties")
        st.plotly_chart(pie_fig, use_container_width=True)
    
    # Party performance table
    st.subheader("Party Performance Summary")
    party_summary = pd.DataFrame({
        'Party': party_seats.index,
        'Seats Won': party_seats.values,
        'Total Votes': [party_votes.get(party, 0) for party in party_seats.index],
        'Average Vote Share (%)': [party_vote_share.get(party, 0) for party in party_seats.index]
    })
    st.dataframe(party_summary, use_container_width=True)





def candidate_comparison(df):
    """Compare two candidates with detailed visualizations"""
    st.header("⚖️ Candidate Comparison")
    
    candidates = df['Candidate'].unique()
    
    col1, col2 = st.columns(2)
    
    with col1:
        candidate1 = st.selectbox("Select First Candidate", sorted(candidates), key="cand1")
    
    with col2:
        candidate2 = st.selectbox("Select Second Candidate", sorted(candidates), key="cand2")
    
    if candidate1 and candidate2 and candidate1 != candidate2:
        cand1_data = df[df['Candidate'] == candidate1].iloc[0]
        cand2_data = df[df['Candidate'] == candidate2].iloc[0]
        
        # Comparison Table
        comparison_data = pd.DataFrame({
            'Metric': ['Candidate', 'Party', 'State', 'Constituency', 'Total Votes', 
                      'Vote Share (%)', 'Result'],
            candidate1: [
                cand1_data['Candidate'],
                cand1_data['Party'],
                cand1_data['State'],
                cand1_data['PC Name'],
                f"{cand1_data['Total Votes']:,}",
                f"{cand1_data['Vote Share']:.2f}%",
                "Won" if cand1_data['Winner'] else "Lost"
            ],
            candidate2: [
                cand2_data['Candidate'],
                cand2_data['Party'],
                cand2_data['State'],
                cand2_data['PC Name'],
                f"{cand2_data['Total Votes']:,}",
                f"{cand2_data['Vote Share']:.2f}%",
                "Won" if cand2_data['Winner'] else "Lost"
            ]
        })
        
        st.table(comparison_data)
        
        # Vote difference
        vote_diff = abs(cand1_data['Total Votes'] - cand2_data['Total Votes'])
        vote_share_diff = abs(cand1_data['Vote Share'] - cand2_data['Vote Share'])
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Vote Difference", f"{vote_diff:,}")
        with col2:
            st.metric("Vote Share Difference", f"{vote_share_diff:.2f}%")
        with col3:
            higher_votes = candidate1 if cand1_data['Total Votes'] > cand2_data['Total Votes'] else candidate2
            st.metric("Higher Votes", higher_votes)
        
        # Visualizations Section
        st.header("📊 Visual Comparison")
        
        # 1. Side-by-side vote comparison
        col1, col2 = st.columns(2)
        
        with col1:
            # Total Votes Comparison Bar Chart
            votes_comparison = pd.DataFrame({
                'Candidate': [candidate1, candidate2],
                'Total Votes': [cand1_data['Total Votes'], cand2_data['Total Votes']],
                'Party': [cand1_data['Party'], cand2_data['Party']]
            })
            
            fig_votes = px.bar(
                votes_comparison,
                x='Candidate',
                y='Total Votes',
                color='Party',
                title="Total Votes Comparison",
                labels={'Total Votes': 'Total Votes', 'Candidate': 'Candidate'},
                text='Total Votes'
            )
            fig_votes.update_traces(texttemplate='%{text:,}', textposition='outside')
            fig_votes.update_layout(showlegend=True)
            st.plotly_chart(fig_votes, use_container_width=True)
        
        with col2:
            # Vote Share Comparison
            fig_share = px.bar(
                votes_comparison,
                x='Candidate',
                y=[cand1_data['Vote Share'], cand2_data['Vote Share']],
                color='Party',
                title="Vote Share Comparison (%)",
                labels={'y': 'Vote Share (%)', 'Candidate': 'Candidate'},
                text=[f"{cand1_data['Vote Share']:.2f}%", f"{cand2_data['Vote Share']:.2f}%"]
            )
            fig_share.update_traces(textposition='outside')
            st.plotly_chart(fig_share, use_container_width=True)
        
        # 2. Pie Chart Comparison
        col1, col2 = st.columns(2)
        
        with col1:
            # Candidate 1 Constituency Analysis
            const1_data = df[df['PC Name'] == cand1_data['PC Name']].sort_values('Total Votes', ascending=False)
            fig_pie1 = px.pie(
                const1_data,
                values='Total Votes',
                names='Candidate',
                title=f"Vote Distribution in {cand1_data['PC Name']}",
                color_discrete_sequence=px.colors.qualitative.Set3
            )
            # Highlight selected candidate
            colors = ['gold' if name == candidate1 else 'lightblue' for name in const1_data['Candidate']]
            fig_pie1.update_traces(marker=dict(colors=colors))
            st.plotly_chart(fig_pie1, use_container_width=True)
        
        with col2:
            # Candidate 2 Constituency Analysis
            const2_data = df[df['PC Name'] == cand2_data['PC Name']].sort_values('Total Votes', ascending=False)
            fig_pie2 = px.pie(
                const2_data,
                values='Total Votes',
                names='Candidate',
                title=f"Vote Distribution in {cand2_data['PC Name']}",
                color_discrete_sequence=px.colors.qualitative.Set3
            )
            # Highlight selected candidate
            colors = ['gold' if name == candidate2 else 'lightblue' for name in const2_data['Candidate']]
            fig_pie2.update_traces(marker=dict(colors=colors))
            st.plotly_chart(fig_pie2, use_container_width=True)
        
        # 3. Performance Radar Chart
        st.subheader("🎯 Performance Radar Chart")
        
        # Normalize values for radar chart (0-100 scale)
        max_votes = df['Total Votes'].max()
        max_vote_share = df['Vote Share'].max()
        
        # Calculate rankings (lower rank = better performance)
        votes_rank1 = (df['Total Votes'] >= cand1_data['Total Votes']).sum()
        votes_rank2 = (df['Total Votes'] >= cand2_data['Total Votes']).sum()
        share_rank1 = (df['Vote Share'] >= cand1_data['Vote Share']).sum()
        share_rank2 = (df['Vote Share'] >= cand2_data['Vote Share']).sum()
        
        radar_data = pd.DataFrame({
            'Metric': ['Votes (Normalized)', 'Vote Share', 'Vote Rank', 'Share Rank', 'Win Status'],
            candidate1: [
                (cand1_data['Total Votes'] / max_votes) * 100,
                cand1_data['Vote Share'],
                max(0, 100 - (votes_rank1 / len(df)) * 100),  # Invert rank for better visualization
                max(0, 100 - (share_rank1 / len(df)) * 100),
                100 if cand1_data['Winner'] else 20
            ],
            candidate2: [
                (cand2_data['Total Votes'] / max_votes) * 100,
                cand2_data['Vote Share'],
                max(0, 100 - (votes_rank2 / len(df)) * 100),
                max(0, 100 - (share_rank2 / len(df)) * 100),
                100 if cand2_data['Winner'] else 20
            ]
        })
        
        fig_radar = go.Figure()
        
        fig_radar.add_trace(go.Scatterpolar(
            r=radar_data[candidate1],
            theta=radar_data['Metric'],
            fill='toself',
            name=candidate1,
            line_color='blue'
        ))
        
        fig_radar.add_trace(go.Scatterpolar(
            r=radar_data[candidate2],
            theta=radar_data['Metric'],
            fill='toself',
            name=candidate2,
            line_color='red'
        ))
        
        fig_radar.update_layout(
            polar=dict(
                radialaxis=dict(
                    visible=True,
                    range=[0, 100]
                )),
            showlegend=True,
            title="Performance Comparison Radar Chart"
        )
        
        st.plotly_chart(fig_radar, use_container_width=True)
        
        # 4. Constituency Competition Analysis
        st.subheader("🏟️ Constituency Competition Analysis")
        
        if cand1_data['PC Name'] == cand2_data['PC Name']:
            # Same constituency - direct competition
            st.success("🎯 Direct Competition: Both candidates contested from the same constituency!")
            
            same_const_data = df[df['PC Name'] == cand1_data['PC Name']].sort_values('Total Votes', ascending=False)
            
            fig_competition = px.bar(
                same_const_data,
                x='Candidate',
                y='Total Votes',
                color='Party',
                title=f"All Candidates in {cand1_data['PC Name']}",
                labels={'Total Votes': 'Total Votes', 'Candidate': 'Candidate'},
                text='Total Votes'
            )
            fig_competition.update_traces(texttemplate='%{text:,}', textposition='outside')
            fig_competition.update_layout(xaxis_tickangle=-45)
            
            # Highlight our two candidates
            colors = []
            for candidate in same_const_data['Candidate']:
                if candidate == candidate1:
                    colors.append('gold')
                elif candidate == candidate2:
                    colors.append('red')
                else:
                    colors.append('lightblue')
            
            fig_competition.update_traces(marker_color=colors)
            st.plotly_chart(fig_competition, use_container_width=True)
            
            # Position analysis
            pos1 = same_const_data[same_const_data['Candidate'] == candidate1].index[0] + 1
            pos2 = same_const_data[same_const_data['Candidate'] == candidate2].index[0] + 1
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric(f"{candidate1} Position", f"#{pos1}")
            with col2:
                st.metric(f"{candidate2} Position", f"#{pos2}")
            with col3:
                st.metric("Position Difference", abs(pos1 - pos2))
        
        else:
            # Different constituencies
            st.info("📍 Different Constituencies: Candidates contested from different areas")
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.write(f"**{candidate1}** - {cand1_data['PC Name']}")
                const1_competition = df[df['PC Name'] == cand1_data['PC Name']].sort_values('Total Votes', ascending=False)
                pos1 = const1_competition[const1_competition['Candidate'] == candidate1].index[0] + 1
                st.metric("Position in Constituency", f"#{pos1} out of {len(const1_competition)}")
                
            with col2:
                st.write(f"**{candidate2}** - {cand2_data['PC Name']}")
                const2_competition = df[df['PC Name'] == cand2_data['PC Name']].sort_values('Total Votes', ascending=False)
                pos2 = const2_competition[const2_competition['Candidate'] == candidate2].index[0] + 1
                st.metric("Position in Constituency", f"#{pos2} out of {len(const2_competition)}")
        
        # 5. Additional Insights
        st.subheader("🔍 Additional Insights")
        
        insights = []
        
        # Vote efficiency
        if cand1_data['Vote Share'] > cand2_data['Vote Share']:
            insights.append(f"📈 **{candidate1}** has a higher vote share ({cand1_data['Vote Share']:.2f}%) compared to **{candidate2}** ({cand2_data['Vote Share']:.2f}%)")
        else:
            insights.append(f"📈 **{candidate2}** has a higher vote share ({cand2_data['Vote Share']:.2f}%) compared to **{candidate1}** ({cand1_data['Vote Share']:.2f}%)")
        
        # Winner status
        if cand1_data['Winner'] and not cand2_data['Winner']:
            insights.append(f"🏆 **{candidate1}** won their constituency while **{candidate2}** lost")
        elif cand2_data['Winner'] and not cand1_data['Winner']:
            insights.append(f"🏆 **{candidate2}** won their constituency while **{candidate1}** lost")
        elif cand1_data['Winner'] and cand2_data['Winner']:
            insights.append(f"🏆 Both candidates won their respective constituencies")
        else:
            insights.append(f"❌ Both candidates lost their respective constituencies")
        
        # Party analysis
        if cand1_data['Party'] == cand2_data['Party']:
            insights.append(f"🤝 Both candidates belong to the same party: **{cand1_data['Party']}**")
        else:
            insights.append(f"⚡ Candidates belong to different parties: **{candidate1}** ({cand1_data['Party']}) vs **{candidate2}** ({cand2_data['Party']})")
        
        # State analysis
        if cand1_data['State'] == cand2_data['State']:
            insights.append(f"📍 Both candidates contested from **{cand1_data['State']}**")
        else:
            insights.append(f"🗺️ Candidates contested from different states: **{candidate1}** from {cand1_data['State']}, **{candidate2}** from {cand2_data['State']}")
        
        for insight in insights:
            st.write(insight)
        
        # Export comparison
        st.subheader("📥 Export Comparison")
        if st.button("Export Comparison to CSV"):
            csv = comparison_data.to_csv(index=False)
            st.download_button(
                label="Download Comparison CSV",
                data=csv,
                file_name=f"comparison_{candidate1}_vs_{candidate2}.csv",
                mime="text/csv"
            )
    
    elif candidate1 == candidate2:
        st.warning("⚠️ Please select two different candidates for comparison.")
    else:
        st.info("👆 Please select two candidates to compare their performance.")




def state_summary(df):
    """Display enhanced state-wise summary with detailed winner analysis"""
    st.header("🗺️ State-wise Summary")
    
    selected_state = st.selectbox("Select State for Analysis", sorted(df['State'].unique()))
    
    state_data = df[df['State'] == selected_state]
    state_winners = state_data[state_data['Winner'] == True]
    
    # Enhanced Key Metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Constituencies", state_data['PC Name'].nunique())
    
    with col2:
        st.metric("Total Votes", f"{state_data['Total Votes'].sum():,}")
    
    with col3:
        st.metric("Total Candidates", len(state_data))
    
    with col4:
        top_party = state_winners['Party'].value_counts()
        if len(top_party) > 0:
            st.metric("Leading Party", f"{top_party.index[0]} ({top_party.iloc[0]} seats)")
    
    # Additional State Statistics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        avg_votes_per_constituency = state_data.groupby('PC Name')['Total Votes'].sum().mean()
        st.metric("Avg Votes/Constituency", f"{avg_votes_per_constituency:,.0f}")
    
    with col2:
        unique_parties = state_data['Party'].nunique()
        st.metric("Participating Parties", unique_parties)
    
    with col3:
        avg_candidates_per_constituency = state_data.groupby('PC Name').size().mean()
        st.metric("Avg Candidates/Seat", f"{avg_candidates_per_constituency:.1f}")
    
    with col4:
        state_vote_share = (state_data['Total Votes'].sum() / df['Total Votes'].sum()) * 100
        st.metric("State Vote Share", f"{state_vote_share:.2f}%")
    
    # Detailed Winners Analysis
    st.header("🏆 Winners Analysis")
    
    if not state_winners.empty:
        st.subheader("📋 All Winners in State")
        
        # Display winners in a formatted table
        winners_display = state_winners[['Candidate', 'Party', 'PC Name', 'Total Votes', 'Vote Share']].copy()
        winners_display = winners_display.sort_values('Total Votes', ascending=False)
        winners_display['Rank'] = range(1, len(winners_display) + 1)
        
        # Reorder columns
        winners_display = winners_display[['Rank', 'Candidate', 'Party', 'PC Name', 'Total Votes', 'Vote Share']]
        
        st.dataframe(winners_display, use_container_width=True)
        
        # Top Performers
        st.subheader("🥇 Top Performing Winners")
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Top 10 winners by votes
            top_winners = state_winners.nlargest(10, 'Total Votes')
            fig_top_votes = px.bar(
                top_winners,
                x='Total Votes',
                y='Candidate',
                orientation='h',
                color='Party',
                title="Top 10 Winners by Total Votes",
                labels={'Total Votes': 'Total Votes', 'Candidate': 'Candidate'},
                text='Total Votes'
            )
            fig_top_votes.update_traces(texttemplate='%{text:,}', textposition='outside')
            fig_top_votes.update_layout(height=500)
            st.plotly_chart(fig_top_votes, use_container_width=True)
        
        with col2:
            # Top 10 winners by vote share
            top_vote_share = state_winners.nlargest(10, 'Vote Share')
            fig_top_share = px.bar(
                top_vote_share,
                x='Vote Share',
                y='Candidate',
                orientation='h',
                color='Party',
                title="Top 10 Winners by Vote Share",
                labels={'Vote Share': 'Vote Share (%)', 'Candidate': 'Candidate'},
                text='Vote Share'
            )
            fig_top_share.update_traces(texttemplate='%{text:.1f}%', textposition='outside')
            fig_top_share.update_layout(height=500)
            st.plotly_chart(fig_top_share, use_container_width=True)
    
    # Party-wise Analysis
    st.header("🏛️ Party-wise Analysis")
    
    # Party-wise seat distribution in state
    party_seats_state = state_winners['Party'].value_counts()
    
    if len(party_seats_state) > 0:
        col1, col2 = st.columns(2)
        
        with col1:
            fig_seats = px.bar(
                x=party_seats_state.values, 
                y=party_seats_state.index,
                orientation='h', 
                title=f"Party-wise Seats Won in {selected_state}",
                labels={'x': 'Seats Won', 'y': 'Party'},
                text=party_seats_state.values,
                color=party_seats_state.values,
                color_continuous_scale='viridis'
            )
            fig_seats.update_layout(yaxis={'categoryorder':'total ascending'}, showlegend=False)
            fig_seats.update_traces(texttemplate='%{text}', textposition='outside')
            st.plotly_chart(fig_seats, use_container_width=True)
        
        with col2:
            # Pie chart for seat distribution
            fig_pie_seats = px.pie(
                values=party_seats_state.values,
                names=party_seats_state.index,
                title=f"Seat Share Distribution in {selected_state}",
                color_discrete_sequence=px.colors.qualitative.Set3
            )
            fig_pie_seats.update_traces(textposition='inside', textinfo='percent+label')
            st.plotly_chart(fig_pie_seats, use_container_width=True)
    
    # Party-wise vote analysis
    party_votes = state_data.groupby('Party')['Total Votes'].sum().sort_values(ascending=False)
    party_vote_share = state_data.groupby('Party')['Vote Share'].sum().sort_values(ascending=False)
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Party-wise total votes
        fig_party_votes = px.bar(
            x=party_votes.index,
            y=party_votes.values,
            title=f"Party-wise Total Votes in {selected_state}",
            labels={'x': 'Party', 'y': 'Total Votes'},
            color=party_votes.values,
            color_continuous_scale='plasma',
            text=party_votes.values
        )
        fig_party_votes.update_traces(texttemplate='%{text:,}', textposition='outside')
        fig_party_votes.update_layout(xaxis_tickangle=-45, showlegend=False)
        st.plotly_chart(fig_party_votes, use_container_width=True)
    
    with col2:
        # Party-wise vote share
        fig_party_share = px.bar(
            x=party_vote_share.index,
            y=party_vote_share.values,
            title=f"Party-wise Vote Share in {selected_state}",
            labels={'x': 'Party', 'y': 'Total Vote Share (%)'},
            color=party_vote_share.values,
            color_continuous_scale='blues',
            text=party_vote_share.values
        )
        fig_party_share.update_traces(texttemplate='%{text:.1f}%', textposition='outside')
        fig_party_share.update_layout(xaxis_tickangle=-45, showlegend=False)
        st.plotly_chart(fig_party_share, use_container_width=True)
    
    # Constituency-wise Analysis
    st.header("🗳️ Constituency-wise Analysis")
    
    constituency_summary = state_data.groupby('PC Name').agg({
        'Total Votes': 'sum',
        'Candidate': 'count',
        'Winner': 'any'  # True if any winner in constituency
    }).reset_index()
    
    constituency_summary.columns = ['Constituency', 'Total Votes', 'Candidates', 'Has Winner']
    constituency_summary = constituency_summary.sort_values('Total Votes', ascending=False)
    
    # Winner details per constituency
    winner_details = state_winners.groupby('PC Name').agg({
        'Candidate': 'first',
        'Party': 'first',
        'Total Votes': 'first',
        'Vote Share': 'first'
    }).reset_index()
    
    # Merge for complete constituency info
    constituency_complete = pd.merge(constituency_summary, winner_details, 
                                   left_on='Constituency', right_on='PC Name', how='left')
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Total votes per constituency
        fig_const_votes = px.bar(
            constituency_summary.head(15),  # Top 15 constituencies
            x='Total Votes',
            y='Constituency',
            orientation='h',
            title=f"Top 15 Constituencies by Total Votes in {selected_state}",
            labels={'Total Votes': 'Total Votes', 'Constituency': 'Constituency'},
            text='Total Votes',
            color='Total Votes',
            color_continuous_scale='greens'
        )
        fig_const_votes.update_traces(texttemplate='%{text:,}', textposition='outside')
        fig_const_votes.update_layout(height=600, showlegend=False)
        st.plotly_chart(fig_const_votes, use_container_width=True)
    
    with col2:
        # Number of candidates per constituency
        fig_const_candidates = px.bar(
            constituency_summary.sort_values('Candidates', ascending=False).head(15),
            x='Candidates',
            y='Constituency',
            orientation='h',
            title=f"Top 15 Constituencies by Candidate Count in {selected_state}",
            labels={'Candidates': 'Number of Candidates', 'Constituency': 'Constituency'},
            text='Candidates',
            color='Candidates',
            color_continuous_scale='oranges'
        )
        fig_const_candidates.update_traces(texttemplate='%{text}', textposition='outside')
        fig_const_candidates.update_layout(height=600, showlegend=False)
        st.plotly_chart(fig_const_candidates, use_container_width=True)
    
    # Victory Margins Analysis
    if not state_winners.empty:
        st.header("⚖️ Victory Margins Analysis")
        
        # Calculate victory margins for each constituency
        margin_data = []
        for constituency in state_data['PC Name'].unique():
            const_data = state_data[state_data['PC Name'] == constituency].sort_values('Total Votes', ascending=False)
            if len(const_data) > 1:
                winner_votes = const_data.iloc[0]['Total Votes']
                runner_up_votes = const_data.iloc[1]['Total Votes']
                margin = winner_votes - runner_up_votes
                margin_percentage = (margin / const_data['Total Votes'].sum()) * 100
                
                margin_data.append({
                    'Constituency': constituency,
                    'Winner': const_data.iloc[0]['Candidate'],
                    'Winner_Party': const_data.iloc[0]['Party'],
                    'Margin': margin,
                    'Margin_Percentage': margin_percentage,
                    'Total_Votes': const_data['Total Votes'].sum()
                })
        
        if margin_data:
            margins_df = pd.DataFrame(margin_data)
            
            col1, col2 = st.columns(2)
            
            with col1:
                # Closest contests
                closest_contests = margins_df.nsmallest(10, 'Margin')
                fig_closest = px.bar(
                    closest_contests,
                    x='Margin',
                    y='Constituency',
                    orientation='h',
                    color='Winner_Party',
                    title="10 Closest Contests (Smallest Victory Margins)",
                    labels={'Margin': 'Victory Margin (Votes)', 'Constituency': 'Constituency'},
                    text='Margin'
                )
                fig_closest.update_traces(texttemplate='%{text:,}', textposition='outside')
                fig_closest.update_layout(height=500)
                st.plotly_chart(fig_closest, use_container_width=True)
            
            with col2:
                # Biggest victories
                biggest_victories = margins_df.nlargest(10, 'Margin')
                fig_biggest = px.bar(
                    biggest_victories,
                    x='Margin',
                    y='Constituency',
                    orientation='h',
                    color='Winner_Party',
                    title="10 Biggest Victories (Largest Victory Margins)",
                    labels={'Margin': 'Victory Margin (Votes)', 'Constituency': 'Constituency'},
                    text='Margin'
                )
                fig_biggest.update_traces(texttemplate='%{text:,}', textposition='outside')
                fig_biggest.update_layout(height=500)
                st.plotly_chart(fig_biggest, use_container_width=True)
            
            # Margin distribution
            fig_margin_dist = px.histogram(
                margins_df,
                x='Margin_Percentage',
                nbins=20,
                title=f"Distribution of Victory Margins in {selected_state}",
                labels={'Margin_Percentage': 'Victory Margin (%)', 'count': 'Number of Constituencies'},
                color_discrete_sequence=['lightcoral']
            )
            st.plotly_chart(fig_margin_dist, use_container_width=True)
    
    # Performance Insights
    st.header("🔍 State Performance Insights")
    
    insights = []
    
    # Party dominance
    if len(party_seats_state) > 0:
        dominant_party = party_seats_state.index[0]
        dominant_seats = party_seats_state.iloc[0]
        total_seats = len(state_winners)
        dominance_percentage = (dominant_seats / total_seats) * 100
        
        insights.append(f"🏛️ **{dominant_party}** is the dominant party with **{dominant_seats} seats** ({dominance_percentage:.1f}% of total seats)")
    
    # Vote concentration
    if len(party_votes) > 0:
        top_3_parties_votes = party_votes.head(3).sum()
        total_state_votes = state_data['Total Votes'].sum()
        concentration = (top_3_parties_votes / total_state_votes) * 100
        insights.append(f"📊 Top 3 parties secured **{concentration:.1f}%** of total votes in the state")
    
    # Competition analysis
    if 'margins_df' in locals() and not margins_df.empty:
        avg_margin = margins_df['Margin_Percentage'].mean()
        close_contests = len(margins_df[margins_df['Margin_Percentage'] < 5])
        
        insights.append(f"⚖️ Average victory margin is **{avg_margin:.2f}%** with **{close_contests} close contests** (margin < 5%)")
    
    # Candidate diversity
    avg_candidates = state_data.groupby('PC Name').size().mean()
    insights.append(f"👥 Average of **{avg_candidates:.1f} candidates** per constituency indicates {'high' if avg_candidates > 10 else 'moderate' if avg_candidates > 5 else 'low'} competition")
    
    # Vote efficiency
    if not state_winners.empty:
        avg_winner_share = state_winners['Vote Share'].mean()
        insights.append(f"🎯 Winners achieved an average vote share of **{avg_winner_share:.1f}%**")
    
    for insight in insights:
        st.write(insight)
    
    # Export Options
    st.header("📥 Export State Data")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("Export All State Data"):
            csv = state_data.to_csv(index=False)
            st.download_button(
                label="Download Complete State Data",
                data=csv,
                file_name=f"{selected_state}_complete_data.csv",
                mime="text/csv"
            )
    
    with col2:
        if st.button("Export Winners Only"):
            if not state_winners.empty:
                winners_csv = state_winners.to_csv(index=False)
                st.download_button(
                    label="Download Winners Data",
                    data=winners_csv,
                    file_name=f"{selected_state}_winners.csv",
                    mime="text/csv"
                )
    
    with col3:
        if st.button("Export Constituency Summary"):
            const_csv = constituency_complete.to_csv(index=False)
            st.download_button(
                label="Download Constituency Summary",
                data=const_csv,
                file_name=f"{selected_state}_constituency_summary.csv",
                mime="text/csv"
            )





def analytics_charts(df):
    """Display various analytics charts"""
    st.header("📊 Advanced Analytics")
    
    tab1, tab2, tab3 = st.tabs(["Vote Distribution", "Top Performers", "Victory Margins"])
    
    with tab1:
        st.subheader("Vote Share Distribution")
        hist_fig = px.histogram(df, x='Vote Share', nbins=50, 
                               title="Distribution of Vote Shares")
        st.plotly_chart(hist_fig, use_container_width=True)
    
    with tab2:
        st.subheader("Top 20 Candidates by Total Votes")
        top_candidates = df.nlargest(20, 'Total Votes')
        bar_fig = px.bar(top_candidates, x='Total Votes', y='Candidate',
                        orientation='h', color='Party',
                        title="Top 20 Candidates by Vote Count")
        bar_fig.update_layout(yaxis={'categoryorder':'total ascending'})
        st.plotly_chart(bar_fig, use_container_width=True)
    
    with tab3:
        st.subheader("Victory Margins Analysis")
        # Calculate margins for each constituency
        margins = []
        for state in df['State'].unique():
            for constituency in df[df['State'] == state]['PC Name'].unique():
                const_data = df[(df['State'] == state) & 
                               (df['PC Name'] == constituency)].sort_values('Total Votes', ascending=False)
                if len(const_data) > 1:
                    margin = const_data.iloc[0]['Total Votes'] - const_data.iloc[1]['Total Votes']
                    margins.append({
                        'Constituency': constituency,
                        'State': state,
                        'Winner': const_data.iloc[0]['Candidate'],
                        'Party': const_data.iloc[0]['Party'],
                        'Margin': margin
                    })
        
        margins_df = pd.DataFrame(margins)
        if not margins_df.empty:
            # Top 20 closest contests
            closest_contests = margins_df.nsmallest(20, 'Margin')
            margin_fig = px.bar(closest_contests, x='Margin', y='Constituency',
                               orientation='h', color='Party',
                               title="20 Closest Electoral Contests")
            margin_fig.update_layout(yaxis={'categoryorder':'total ascending'})
            st.plotly_chart(margin_fig, use_container_width=True)



def search_and_filters(df):
    """Search and filter functionality with conditional visualizations"""
    st.header("🔍 Search & Filter")
    
    col1, col2 = st.columns(2)
    
    with col1:
        search_term = st.text_input("Search by Candidate/Party/Constituency")
        
    with col2:
        vote_share_range = st.slider("Vote Share Range (%)", 0.0, 100.0, (0.0, 100.0))
    
    # Apply filters
    filtered_df = df.copy()
    search_applied = False
    
    if search_term:
        search_applied = True
        mask = (
            filtered_df['Candidate'].str.contains(search_term, case=False, na=False) |
            filtered_df['Party'].str.contains(search_term, case=False, na=False) |
            filtered_df['PC Name'].str.contains(search_term, case=False, na=False)
        )
        filtered_df = filtered_df[mask]
    
    # Check if vote share range is changed from default
    if vote_share_range != (0.0, 100.0):
        search_applied = True
    
    filtered_df = filtered_df[
        (filtered_df['Vote Share'] >= vote_share_range[0]) & 
        (filtered_df['Vote Share'] <= vote_share_range[1])
    ]
    
    # Only show results if search is applied
    if search_applied:
        st.write(f"Found {len(filtered_df)} results")
        
        if not filtered_df.empty:
            # Display results table
            display_cols = ['Candidate', 'Party', 'State', 'PC Name', 'Total Votes', 'Vote Share', 'Winner']
            st.dataframe(filtered_df[display_cols].sort_values('Total Votes', ascending=False), 
                        use_container_width=True)
            
            # Visualization Section - Only show if search is applied
            st.header("📊 Data Visualizations")
            
            # Party-wise Analysis
            if len(filtered_df['Party'].unique()) > 1:
                st.subheader("🏛️ Party-wise Analysis")
                
                col1, col2 = st.columns(2)
                
                with col1:
                    # Party-wise vote count
                    party_votes = filtered_df.groupby('Party')['Total Votes'].sum().sort_values(ascending=False)
                    fig_party_votes = px.bar(
                        x=party_votes.index,
                        y=party_votes.values,
                        title="Total Votes by Party",
                        labels={'x': 'Party', 'y': 'Total Votes'},
                        color=party_votes.values,
                        color_continuous_scale='viridis'
                    )
                    fig_party_votes.update_layout(showlegend=False, xaxis_tickangle=-45)
                    st.plotly_chart(fig_party_votes, use_container_width=True)
                
                with col2:
                    # Party-wise average vote share
                    party_avg_share = filtered_df.groupby('Party')['Vote Share'].mean().sort_values(ascending=False)
                    fig_party_share = px.bar(
                        x=party_avg_share.index,
                        y=party_avg_share.values,
                        title="Average Vote Share by Party (%)",
                        labels={'x': 'Party', 'y': 'Average Vote Share (%)'},
                        color=party_avg_share.values,
                        color_continuous_scale='plasma'
                    )
                    fig_party_share.update_layout(showlegend=False, xaxis_tickangle=-45)
                    st.plotly_chart(fig_party_share, use_container_width=True)
                
                # Party distribution pie chart
                fig_pie = px.pie(
                    values=party_votes.values,
                    names=party_votes.index,
                    title="Vote Share Distribution by Party"
                )
                st.plotly_chart(fig_pie, use_container_width=True)
            
            # Constituency-wise Analysis
            if len(filtered_df['PC Name'].unique()) > 1:
                st.subheader("🗳️ Constituency-wise Analysis")
                
                # Number of candidates per constituency
                constituency_candidates = filtered_df.groupby('PC Name').size().sort_values(ascending=False)
                
                col1, col2 = st.columns(2)
                
                with col1:
                    fig_const_candidates = px.bar(
                        x=constituency_candidates.values,
                        y=constituency_candidates.index,
                        orientation='h',
                        title="Number of Candidates per Constituency",
                        labels={'x': 'Number of Candidates', 'y': 'Constituency'},
                        color=constituency_candidates.values,
                        color_continuous_scale='blues'
                    )
                    fig_const_candidates.update_layout(showlegend=False, height=max(400, len(constituency_candidates) * 25))
                    st.plotly_chart(fig_const_candidates, use_container_width=True)
                
                with col2:
                    # Total votes per constituency
                    constituency_votes = filtered_df.groupby('PC Name')['Total Votes'].sum().sort_values(ascending=False)
                    fig_const_votes = px.bar(
                        x=constituency_votes.values,
                        y=constituency_votes.index,
                        orientation='h',
                        title="Total Votes per Constituency",
                        labels={'x': 'Total Votes', 'y': 'Constituency'},
                        color=constituency_votes.values,
                        color_continuous_scale='greens'
                    )
                    fig_const_votes.update_layout(showlegend=False, height=max(400, len(constituency_votes) * 25))
                    st.plotly_chart(fig_const_votes, use_container_width=True)
            
            # Individual Constituency Analysis (if specific constituency is searched)
            specific_constituencies = filtered_df['PC Name'].unique()
            if len(specific_constituencies) <= 5:  # Show detailed analysis for specific constituencies
                for constituency in specific_constituencies:
                    st.subheader(f"📍 Detailed Analysis: {constituency}")
                    
                    const_data = filtered_df[filtered_df['PC Name'] == constituency].sort_values('Total Votes', ascending=False)
                    
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        # Candidate performance in constituency
                        fig_candidates = px.bar(
                            const_data,
                            x='Candidate',
                            y='Total Votes',
                            color='Party',
                            title=f"Candidates Performance in {constituency}",
                            labels={'Total Votes': 'Votes', 'Candidate': 'Candidate'}
                        )
                        fig_candidates.update_layout(xaxis_tickangle=-45)
                        st.plotly_chart(fig_candidates, use_container_width=True)
                    
                    with col2:
                        # Vote share in constituency
                        fig_vote_share = px.pie(
                            const_data,
                            values='Total Votes',
                            names='Candidate',
                            title=f"Vote Share in {constituency}",
                            color_discrete_sequence=px.colors.qualitative.Set3
                        )
                        st.plotly_chart(fig_vote_share, use_container_width=True)
                    
                    # Summary stats for constituency
                    st.write("**Constituency Summary:**")
                    total_votes_const = const_data['Total Votes'].sum()
                    winner = const_data.iloc[0] if not const_data.empty else None
                    
                    if winner is not None:
                        col1, col2, col3, col4 = st.columns(4)
                        with col1:
                            st.metric("Total Votes", f"{total_votes_const:,}")
                        with col2:
                            st.metric("Winner", winner['Candidate'])
                        with col3:
                            st.metric("Winning Party", winner['Party'])
                        with col4:
                            st.metric("Winning Margin", f"{winner['Vote Share']:.2f}%")
            
            # Candidate Analysis
            st.subheader("👤 Candidate Analysis")
            
            # Top performers
            top_candidates = filtered_df.nlargest(10, 'Total Votes')
            
            col1, col2 = st.columns(2)
            
            with col1:
                fig_top_candidates = px.bar(
                    top_candidates,
                    x='Total Votes',
                    y='Candidate',
                    orientation='h',
                    color='Party',
                    title="Top Candidates by Votes",
                    labels={'Total Votes': 'Votes', 'Candidate': 'Candidate'}
                )
                fig_top_candidates.update_layout(height=400)
                st.plotly_chart(fig_top_candidates, use_container_width=True)
            
            with col2:
                # Vote share vs Total votes scatter
                fig_scatter = px.scatter(
                    filtered_df,
                    x='Total Votes',
                    y='Vote Share',
                    color='Party',
                    size='Total Votes',
                    hover_data=['Candidate', 'PC Name'],
                    title="Vote Share vs Total Votes",
                    labels={'Vote Share': 'Vote Share (%)', 'Total Votes': 'Total Votes'}
                )
                st.plotly_chart(fig_scatter, use_container_width=True)
            
            # Summary Statistics
            st.subheader("📈 Summary Statistics")
            
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric("Total Candidates", len(filtered_df))
            with col2:
                st.metric("Unique Parties", len(filtered_df['Party'].unique()))
            with col3:
                st.metric("Constituencies", len(filtered_df['PC Name'].unique()))
            with col4:
                st.metric("Total Votes", f"{filtered_df['Total Votes'].sum():,}")
            
            # Additional insights
            if len(filtered_df) > 1:
                st.subheader("🔍 Key Insights")
                
                # Highest vote share
                highest_vote_share = filtered_df.loc[filtered_df['Vote Share'].idxmax()]
                st.write(f"**Highest Vote Share:** {highest_vote_share['Candidate']} ({highest_vote_share['Party']}) - {highest_vote_share['Vote Share']:.2f}% in {highest_vote_share['PC Name']}")
                
                # Most votes
                most_votes = filtered_df.loc[filtered_df['Total Votes'].idxmax()]
                st.write(f"**Most Votes:** {most_votes['Candidate']} ({most_votes['Party']}) - {most_votes['Total Votes']:,} votes in {most_votes['PC Name']}")
                
                # Party with most candidates
                party_candidate_count = filtered_df['Party'].value_counts()
                if len(party_candidate_count) > 0:
                    top_party = party_candidate_count.index[0]
                    st.write(f"**Most Active Party:** {top_party} with {party_candidate_count.iloc[0]} candidates")
            
            # Export functionality
            st.subheader("📥 Export Data")
            if st.button("Export Results to CSV"):
                csv = filtered_df.to_csv(index=False)
                st.download_button(
                    label="Download CSV",
                    data=csv,
                    file_name="filtered_election_results.csv",
                    mime="text/csv"
                )
        else:
            st.warning("No results found for the current search criteria.")
    else:
        st.info("👆 Please enter a search term or adjust the vote share range to see results and visualizations.")



def main():
    """Main application function"""
    # Load data
    df = load_data()
    
    if df is None:
        st.error("Please upload the results_2024.csv file to proceed.")
        uploaded_file = st.file_uploader("Upload Election Results CSV", type=['csv'])
        if uploaded_file is not None:
            df = pd.read_csv(uploaded_file)
            st.success("Data loaded successfully!")
            st.rerun()
        return
    
    # Sidebar navigation
    st.sidebar.title("Navigation")
    pages = {
        "Dashboard Overview": dashboard_overview,
        "Constituency Results": constituency_results,
        "Party Analysis": party_analysis,
        "Candidate Comparison": candidate_comparison,
        "State Summary": state_summary,
        "Analytics & Charts": analytics_charts,
        "Search & Filter": search_and_filters
    }
    
    selected_page = st.sidebar.selectbox("Select Analysis", list(pages.keys()))
    
    # Dark mode toggle
    dark_mode = st.sidebar.checkbox("Dark Mode")
    if dark_mode:
        st.markdown("""
        <style>
            .stApp {
                background-color: #0E1117;
                color: white;
            }
        </style>
        """, unsafe_allow_html=True)
    
    # Display selected page
    pages[selected_page](df)
    
    # Footer
    st.sidebar.markdown("---")
    st.sidebar.info("2024 Lok Sabha Election Analysis Tool")



# def add_detailed_copyright():
#     """Add detailed copyright and information section"""
#     st.markdown("---")
    
#     st.subheader("📊 About This Application")
    
#     col1, col2 = st.columns(2)
    
#     with col1:
#         st.markdown("""
#         **2024 Lok Sabha Election Analysis Tool**
        
#         This comprehensive dashboard provides:
#         - 🔍 Advanced search and filtering
#         - ⚖️ Candidate comparisons
#         - 🏛️ Constituency-wise analysis
#         - 🗺️ State-wise summaries
#         - 📊 Interactive visualizations
        
#         **Features:**
#         - Real-time data filtering
#         - Export capabilities
#         - Detailed insights and analytics
#         """)
    
#     with col2:
#         st.markdown("""
#         **Copyright & Legal Information**
        
#         © 2024 Election Analysis Dashboard
#         All rights reserved.
        
#         **Data Source:** Election Commission of India
#         **Technology:** Built with Streamlit & Plotly
#         **Version:** 1.0.0
        
#         **Contact Information:**
#         - 📧 Email: razaaatif25@gmail.com
#         - 🌐 Github: https://github.com/Aatifraza123
#         - 📱 Support: +91-8804819102
#         """)
    
#     # Disclaimer
#     st.info("""
#     **Disclaimer:** This tool is for educational and analytical purposes only. 
#     All data is sourced from official Election Commission of India records. 
#     The developers are not responsible for any decisions made based on this analysis.
#     """)

def add_detailed_copyright():
    """Add normal copyright footer at very bottom"""
    st.markdown("---")
    
    st.markdown("""
    <div style="
        background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%); 
        margin-top: 40px;
        margin-bottom: 0;
        color: #ffffff; 
        padding: 15px 20px; 
        border-radius: 12px; 
        text-align: center; 
        font-family: 'Inter', sans-serif; 
        font-size: 13px;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
        border: 1px solid #0f3460;
    ">
    <p style="margin: 0; line-height: 1.5;">
    <i class="fas fa-copyright" style="color: #00d4ff;"></i> 2024 Election Analysis Dashboard | 
    <i class="fas fa-envelope" style="color: #ff6b6b;"></i> razaaatif25@gmail.com | 
    <i class="fab fa-github" style="color: #ffffff;"></i> <a href="https://github.com/Aatifraza123" style="color: #00d4ff; text-decoration: none;">github.com/Aatifraza123</a> | 
    <i class="fas fa-phone" style="color: #4ecdc4;"></i> +91-8804819102 | 
    <i class="fas fa-database" style="color: #ffe66d;"></i> Data: ECI | Built with Streamlit
    </p>
    </div>
    
    <style>
    .main .block-container {
        padding-bottom: 0 !important;
        margin-bottom: 0 !important;
    }
    </style>
    """, unsafe_allow_html=True)




if __name__ == "__main__":
    main()


add_detailed_copyright()
