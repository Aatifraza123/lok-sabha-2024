import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# Page configuration
st.set_page_config(
    page_title="2024 Lok Sabha Election Results",
    page_icon="🗳️",
    layout="wide"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #FF6B35;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 10px;
        border-left: 5px solid #FF6B35;
    }
    .search-result {
        background-color: #ffffff;
        padding: 1.5rem;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        margin: 2rem 0;
    }
</style>
""", unsafe_allow_html=True)

# Title
st.markdown('<h1 class="main-header">🗳️ 2024 Lok Sabha Election Results Dashboard</h1>', unsafe_allow_html=True)

# Load data function
@st.cache_data
def load_data():
    try:
        # Assuming your CSV file is in the same directory
        df = pd.read_csv('sample_data.csv')
        return df
    except FileNotFoundError:
        st.error("CSV file 'sample_data.csv' not found. Please upload your file.")
        return None

# Load the data
df = load_data()

if df is not None:
    # Data preprocessing
    df.columns = df.columns.str.strip()  # Remove any extra spaces from column names
    
    # Sidebar for navigation
    st.sidebar.title("Navigation")
    option = st.sidebar.selectbox(
        "Choose a section:",
        ["🔍 Constituency Search", "📊 Overall Results", "📈 Analytics"]
    )
    
    if option == "🔍 Constituency Search":
        st.header("🔍 Search Constituency Results")
        
        # Search functionality
        search_term = st.text_input(
            "Enter constituency name to search:",
            placeholder="Type constituency name..."
        )
        
        if search_term:
            # Filter data based on search term
            filtered_df = df[df['Constituency'].str.contains(search_term, case=False, na=False)]
            
            if not filtered_df.empty:
                st.success(f"Found {len(filtered_df)} constituency(ies) matching '{search_term}'")
                
                for idx, row in filtered_df.iterrows():
                    with st.container():
                        st.markdown('<div class="search-result">', unsafe_allow_html=True)
                        
                        col1, col2 = st.columns(2)
                        
                        with col1:
                            st.markdown(f"### {row['Constituency']}")
                            st.markdown(f"**Constituency No.:** {row['Const. No.']}")
                            st.markdown(f"**Status:** {row['Status']}")
                        
                        with col2:
                            st.markdown(f"**Leading Candidate:** {row['Leading Candidate']}")
                            st.markdown(f"**Leading Party:** {row['Leading Party']}")
                            st.markdown(f"**Trailing Candidate:** {row['Trailing Candidate']}")
                            st.markdown(f"**Trailing Party:** {row['Trailing Party']}")
                            st.markdown(f"**Victory Margin:** {row['Margin']}")

                        
                        st.markdown('</div>', unsafe_allow_html=True)
            else:
                st.warning(f"No constituency found matching '{search_term}'. Please try a different search term.")
    
    elif option == "📊 Overall Results":
        st.header("📊 Overall Election Results")
        
        # Key metrics
        total_seats = len(df)
        leading_parties = df['Leading Party'].value_counts()
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.markdown('<div class="metric-card">', unsafe_allow_html=True)
            st.metric("Total Constituencies", total_seats)
            st.markdown('</div>', unsafe_allow_html=True)
        
        with col2:
            st.markdown('<div class="metric-card">', unsafe_allow_html=True)
            st.metric("Leading Party", leading_parties.index[0])
            st.markdown('</div>', unsafe_allow_html=True)
        
        with col3:
            st.markdown('<div class="metric-card">', unsafe_allow_html=True)
            st.metric("Seats by Leading Party", leading_parties.iloc[0])
            st.markdown('</div>', unsafe_allow_html=True)
        
        with col4:
            st.markdown('<div class="metric-card">', unsafe_allow_html=True)
            st.metric("Total Parties", len(leading_parties))
            st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown("---")
        
        # Party-wise seats visualization
        st.subheader("🏆 Party-wise Seat Distribution")
        
        # Create two columns for different chart types
        chart_col1, chart_col2 = st.columns(2)
        
        with chart_col1:
            # Bar chart using Plotly
            fig_bar = px.bar(
                x=leading_parties.values,
                y=leading_parties.index,
                orientation='h',
                title="Seats Won by Each Party",
                labels={'x': 'Number of Seats', 'y': 'Political Party'},
                color=leading_parties.values,
                color_continuous_scale='viridis'
            )
            fig_bar.update_layout(height=600, showlegend=False)
            st.plotly_chart(fig_bar, use_container_width=True)
        
        with chart_col2:
            # Pie chart using Plotly
            fig_pie = px.pie(
                values=leading_parties.values,
                names=leading_parties.index,
                title="Seat Share Percentage"
            )
            fig_pie.update_traces(textposition='inside', textinfo='percent+label')
            fig_pie.update_layout(height=600)
            st.plotly_chart(fig_pie, use_container_width=True)
        
        # Detailed results table
        st.subheader("📋 Detailed Party-wise Results")
        party_summary = pd.DataFrame({
            'Party': leading_parties.index,
            'Seats Won': leading_parties.values,
            'Percentage': (leading_parties.values / total_seats * 100).round(2)
        }).reset_index(drop=True)
        
        st.dataframe(party_summary, use_container_width=True)
    
    elif option == "📈 Analytics":
        st.header("📈 Advanced Analytics")
        
        # Victory margin analysis
        st.subheader("🎯 Victory Margin Analysis")
        
        # Convert margin to numeric, handling any non-numeric values
        df['Margin_Numeric'] = pd.to_numeric(df['Margin'], errors='coerce')
        
        # Filter out invalid margins
        valid_margins = df.dropna(subset=['Margin_Numeric'])
        
        if not valid_margins.empty:
            # Victory margin distribution
            fig_margin = px.histogram(
                valid_margins,
                x='Margin_Numeric',
                nbins=30,
                title="Distribution of Victory Margins",
                labels={'Margin_Numeric': 'Victory Margin', 'count': 'Number of Constituencies'}
            )
            st.plotly_chart(fig_margin, use_container_width=True)
            
            # Top 10 closest contests
            st.subheader("🔥 Closest Contests (Top 10)")
            closest_contests = valid_margins.nsmallest(10, 'Margin_Numeric')[
                ['Constituency', 'Leading Candidate', 'Leading Party', 'Trailing Candidate', 'Trailing Party', 'Margin_Numeric']
            ]
            st.dataframe(closest_contests, use_container_width=True)
            
            # Top 10 biggest victories
            st.subheader("🏆 Biggest Victory Margins (Top 10)")
            biggest_victories = valid_margins.nlargest(10, 'Margin_Numeric')[
                ['Constituency', 'Leading Candidate', 'Leading Party', 'Trailing Party', 'Margin_Numeric']
            ]
            st.dataframe(biggest_victories, use_container_width=True)
        else:
            st.warning("Unable to analyze victory margins due to data format issues.")
        
        # Party performance by margin ranges
        st.subheader("📊 Party Performance by Victory Margin Ranges")
        
        if not valid_margins.empty:
            # Create margin ranges
            valid_margins['Margin_Range'] = pd.cut(
                valid_margins['Margin_Numeric'],
                bins=[0, 5000, 25000, 50000, 100000, float('inf')],
                labels=['0-5K', '5K-25K', '25K-50K', '50K-100K', '100K+']
            )
            
            margin_party_analysis = pd.crosstab(
                valid_margins['Leading Party'],
                valid_margins['Margin_Range']
            )
            
            # Create stacked bar chart
            fig_stacked = go.Figure()
            
            for column in margin_party_analysis.columns:
                fig_stacked.add_trace(go.Bar(
                    name=column,
                    x=margin_party_analysis.index,
                    y=margin_party_analysis[column]
                ))
            
            fig_stacked.update_layout(
                barmode='stack',
                title='Party Performance by Victory Margin Ranges',
                xaxis_title='Political Party',
                yaxis_title='Number of Constituencies',
                height=600
            )
            
            st.plotly_chart(fig_stacked, use_container_width=True)

    # Footer
    st.markdown("---")
    st.markdown(
        """
        <div style='text-align: center; color: #666;'>
            <p>📊 Data Source: 2024 Lok Sabha Election Results | Built with ❤️ using Streamlit</p>
        </div>
        """,
        unsafe_allow_html=True
    )

else:
    # File upload option if CSV is not found
    st.warning("Please upload your 2024 Lok Sabha election data CSV file.")
    
    uploaded_file = st.file_uploader(
        "Choose your CSV file",
        type="csv",
        help="Upload a CSV file with columns: Constituency, Const. No., Leading Candidate, Leading Party, Trailing Candidate, Trailing Party, Margin, Status"
    )
    
    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file)
        st.success("File uploaded successfully! Please refresh the page.")
        st.dataframe(df.head())
