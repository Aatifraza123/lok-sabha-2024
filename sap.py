import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np
import io

# Page configuration
st.set_page_config(
    page_title="2024 Lok Sabha Election Analysis",
    page_icon="🗳️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for styling
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #FF6B35;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        padding: 1rem;
        border-radius: 10px;
        color: white;
        text-align: center;
    }
    .winner-highlight {
        background-color: #90EE90;
        padding: 0.5rem;
        border-radius: 5px;
        font-weight: bold;
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

# def calculate_dashboard_metrics(df):
#     """Calculate key metrics for dashboard"""
#     total_states = df['State'].nunique()
#     total_constituencies = df['PC Name'].nunique()
#     total_votes = df['Total Votes'].sum()
#     total_parties = df['Party'].nunique()
    
#     # Party with maximum wins
#     winners_df = df[df['Winner'] == True]
#     party_wins = winners_df['Party'].value_counts()
#     max_wins_party = party_wins.index[0] if len(party_wins) > 0 else "N/A"
    
#     return {
#         'total_states': total_states,
#         'total_constituencies': total_constituencies,
#         'total_votes': total_votes,
#         'total_parties': total_parties,
#         'max_wins_party': max_wins_party,
#         'max_wins_count': party_wins.iloc[0] if len(party_wins) > 0 else 0
#     }

# def dashboard_overview(df):
#     """Display dashboard overview"""
#     st.markdown('<h1 class="main-header">🗳️ 2024 Lok Sabha Election Analysis Dashboard</h1>', unsafe_allow_html=True)
    
#     metrics = calculate_dashboard_metrics(df)
    
#     col1, col2, col3, col4, col5 = st.columns(5)
    
#     with col1:
#         st.metric("Total States/UTs", metrics['total_states'])
    
#     with col2:
#         st.metric("Parliamentary Constituencies", metrics['total_constituencies'])
    
#     with col3:
#         st.metric("Total Votes Cast", f"{metrics['total_votes']:,}")
    
#     with col4:
#         st.metric("Parties Participated", metrics['total_parties'])
    
#     with col5:
#         st.metric("Leading Party", f"{metrics['max_wins_party']} ({metrics['max_wins_count']} seats)")


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
            <div class="metric-value">{metrics['total_constituencies']}</div>
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
        avg_candidates_per_seat = metrics['total_candidates'] / metrics['total_constituencies']
        st.warning(f"👥 **Competition Level:** Average {avg_candidates_per_seat:.1f} candidates per constituency")

# -----------------------------


def constituency_results(df):
    """Display constituency-wise results"""
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
        
        # Display results in a formatted table
        for idx, row in constituency_data.iterrows():
            if row['Winner']:
                st.markdown(f"""
                <div class="winner-highlight">
                    🏆 WINNER: {row['Candidate']} ({row['Party']}) - {row['Total Votes']:,} votes ({row['Vote Share']:.2f}%)
                </div>
                """, unsafe_allow_html=True)
            else:
                st.write(f"• {row['Candidate']} ({row['Party']}) - {row['Total Votes']:,} votes ({row['Vote Share']:.2f}%)")
        
        # Victory margin
        if len(constituency_data) > 1:
            margin = constituency_data.iloc[0]['Total Votes'] - constituency_data.iloc[1]['Total Votes']
            st.info(f"Victory Margin: {margin:,} votes")
        
        # Visualization
        fig = px.bar(constituency_data, x='Candidate', y='Total Votes', 
                    color='Party', title=f"Vote Distribution - {selected_constituency}")
        fig.update_xaxes(tickangle=45)
        st.plotly_chart(fig, use_container_width=True)

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
    """Compare two candidates"""
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
        st.info(f"Vote Difference: {vote_diff:,} votes")

def state_summary(df):
    """Display state-wise summary"""
    st.header("🗺️ State-wise Summary")
    
    selected_state = st.selectbox("Select State for Analysis", sorted(df['State'].unique()))
    
    state_data = df[df['State'] == selected_state]
    state_winners = state_data[state_data['Winner'] == True]
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Constituencies", state_data['PC Name'].nunique())
    
    with col2:
        st.metric("Total Votes", f"{state_data['Total Votes'].sum():,}")
    
    with col3:
        top_party = state_winners['Party'].value_counts()
        if len(top_party) > 0:
            st.metric("Leading Party", f"{top_party.index[0]} ({top_party.iloc[0]} seats)")
    
    # Party-wise seat distribution in state
    party_seats_state = state_winners['Party'].value_counts()
    
    if len(party_seats_state) > 0:
        fig = px.bar(x=party_seats_state.values, y=party_seats_state.index,
                    orientation='h', title=f"Party-wise Seats in {selected_state}")
        fig.update_layout(yaxis={'categoryorder':'total ascending'})
        st.plotly_chart(fig, use_container_width=True)

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
    """Search and filter functionality"""
    st.header("🔍 Search & Filter")
    
    col1, col2 = st.columns(2)
    
    with col1:
        search_term = st.text_input("Search by Candidate/Party/Constituency")
        
    with col2:
        vote_share_range = st.slider("Vote Share Range (%)", 0.0, 100.0, (0.0, 100.0))
    
    # Apply filters
    filtered_df = df.copy()
    
    if search_term:
        mask = (
            filtered_df['Candidate'].str.contains(search_term, case=False, na=False) |
            filtered_df['Party'].str.contains(search_term, case=False, na=False) |
            filtered_df['PC Name'].str.contains(search_term, case=False, na=False)
        )
        filtered_df = filtered_df[mask]
    
    filtered_df = filtered_df[
        (filtered_df['Vote Share'] >= vote_share_range[0]) & 
        (filtered_df['Vote Share'] <= vote_share_range[1])
    ]
    
    st.write(f"Found {len(filtered_df)} results")
    
    if not filtered_df.empty:
        # Display results
        display_cols = ['Candidate', 'Party', 'State', 'PC Name', 'Total Votes', 'Vote Share', 'Winner']
        st.dataframe(filtered_df[display_cols].sort_values('Total Votes', ascending=False), 
                    use_container_width=True)
        
        # Export functionality
        if st.button("Export Results to CSV"):
            csv = filtered_df.to_csv(index=False)
            st.download_button(
                label="Download CSV",
                data=csv,
                file_name="filtered_election_results.csv",
                mime="text/csv"
            )

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

if __name__ == "__main__":
    main()
