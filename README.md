<!DOCTYPE html>
<html lang="hi">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Lok Sabha Election 2024 - Results Dashboard</title>
    <style>
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            line-height: 1.6;
            color: #333;
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
            background-color: #f8f9fa;
        }
        .header {
            text-align: center;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 40px 20px;
            border-radius: 10px;
            margin-bottom: 30px;
        }
        .header h1 {
            margin: 0;
            font-size: 2.5em;
            font-weight: bold;
        }
        .header p {
            font-size: 1.2em;
            margin: 10px 0 0 0;
            opacity: 0.9;
        }
        .badge {
            display: inline-block;
            padding: 5px 10px;
            background-color: #28a745;
            color: white;
            border-radius: 15px;
            text-decoration: none;
            font-size: 0.9em;
            margin: 5px;
        }
        .section {
            background: white;
            margin: 20px 0;
            padding: 30px;
            border-radius: 10px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }
        .section h2 {
            color: #2c3e50;
            border-bottom: 3px solid #3498db;
            padding-bottom: 10px;
            margin-bottom: 20px;
        }
        .section h3 {
            color: #34495e;
            margin-top: 25px;
        }
        .feature-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 20px;
            margin: 20px 0;
        }
        .feature-card {
            background: #f8f9fa;
            padding: 20px;
            border-radius: 8px;
            border-left: 4px solid #3498db;
        }
        .feature-card h4 {
            color: #2980b9;
            margin: 0 0 10px 0;
        }
        .code-block {
            background-color: #2d3748;
            color: #e2e8f0;
            padding: 20px;
            border-radius: 8px;
            overflow-x: auto;
            font-family: 'Courier New', monospace;
            margin: 15px 0;
        }
        .live-demo {
            text-align: center;
            background: linear-gradient(45deg, #ff6b6b, #ee5a24);
            color: white;
            padding: 20px;
            border-radius: 10px;
            margin: 20px 0;
        }
        .live-demo a {
            color: white;
            text-decoration: none;
            font-weight: bold;
            font-size: 1.2em;
            border: 2px solid white;
            padding: 10px 20px;
            border-radius: 25px;
            display: inline-block;
            margin-top: 10px;
            transition: all 0.3s ease;
        }
        .live-demo a:hover {
            background-color: white;
            color: #ff6b6b;
        }
        .stats-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 15px;
            margin: 20px 0;
        }
        .stat-card {
            text-align: center;
            background: #3498db;
            color: white;
            padding: 20px;
            border-radius: 8px;
        }
        .stat-number {
            font-size: 2em;
            font-weight: bold;
            display: block;
        }
        .emoji {
            font-size: 1.2em;
        }
        ul {
            padding-left: 20px;
        }
        li {
            margin: 8px 0;
        }
        .installation-steps {
            background: #e8f5e8;
            padding: 20px;
            border-radius: 8px;
            border-left: 4px solid #27ae60;
        }
        .footer {
            text-align: center;
            background: #2c3e50;
            color: white;
            padding: 30px;
            border-radius: 10px;
            margin-top: 40px;
        }
        .footer p {
            margin: 5px 0;
        }
        @media (max-width: 768px) {
            body {
                padding: 10px;
            }
            .header h1 {
                font-size: 2em;
            }
            .section {
                padding: 20px;
            }
        }
    </style>
</head>
<body>

<div class="header">
    <h1><span class="emoji">🗳️</span> Lok Sabha Election 2024</h1>
    <p>Results Dashboard - A Comprehensive Streamlit Web Application</p>
    <div style="margin-top: 20px;">
        <a href="https://streamlit.io/" class="badge">Streamlit</a>
        <a href="https://pandas.pydata.org/" class="badge">Pandas</a>
        <a href="https://plotly.com/" class="badge">Plotly</a>
        <a href="https://python.org/" class="badge">Python</a>
    </div>
</div>

<div class="live-demo">
    <h2><span class="emoji">🚀</span> Live Demo</h2>
    <p>Experience the interactive dashboard now!</p>
    <a href="https://lok-sabha-2024.streamlit.app/" target="_blank">Visit Live Application</a>
</div>

<div class="section">
    <h2><span class="emoji">📋</span> Overview</h2>
    <p>This interactive dashboard provides detailed insights into the <strong>2024 Indian General Election results</strong>. Built with <strong>Streamlit</strong>, the app offers an intuitive interface to explore constituency-wise results, party performance, state-wise trends, and comprehensive election analytics.</p>
</div>

<div class="section">
    <h2><span class="emoji">✨</span> Features</h2>
    <div class="feature-grid">
        <div class="feature-card">
            <h4><span class="emoji">🏛️</span> Election Analysis</h4>
            <ul>
                <li>Constituency-wise Results (543 constituencies)</li>
                <li>Party Performance Analysis</li>
                <li>State-wise Trends & Patterns</li>
                <li>Candidate Information</li>
            </ul>
        </div>
        <div class="feature-card">
            <h4><span class="emoji">📊</span> Data Visualizations</h4>
            <ul>
                <li>Interactive Charts & Graphs</li>
                <li>Vote Share Distribution</li>
                <li>Geographic Visualizations</li>
                <li>Trend Analysis</li>
            </ul>
        </div>
        <div class="feature-card">
            <h4><span class="emoji">🔍</span> Search & Filter</h4>
            <ul>
                <li>Search by Constituency</li>
                <li>Filter by State/UT</li>
                <li>Filter by Political Party</li>
                <li>Advanced Filtering Options</li>
            </ul>
        </div>
        <div class="feature-card">
            <h4><span class="emoji">📱</span> User Experience</h4>
            <ul>
                <li>Responsive Design</li>
                <li>Clean Navigation</li>
                <li>Real-time Updates</li>
                <li>Export Functionality</li>
            </ul>
        </div>
    </div>
</div>

<div class="section">
    <h2><span class="emoji">🛠️</span> Installation & Setup</h2>
    
    <h3>Prerequisites</h3>
    <ul>
        <li>Python 3.8 or higher</li>
        <li>pip package manager</li>
    </ul>

    <div class="installation-steps">
        <h3>Local Development Steps</h3>
        
        <p><strong>1. Clone the repository</strong></p>
        <div class="code-block">
git clone https://github.com/your-username/lok-sabha-2024.git
cd lok-sabha-2024
        </div>

        <p><strong>2. Create virtual environment</strong></p>
        <div class="code-block">
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
        </div>

        <p><strong>3. Install dependencies</strong></p>
        <div class="code-block">
pip install -r requirements.txt
        </div>

        <p><strong>4. Run the application</strong></p>
        <div class="code-block">
streamlit run app.py
        </div>

        <p><strong>5. Access the app</strong></p>
        <p>Open your browser and navigate to <code>http://localhost:8501</code></p>
    </div>
</div>

<div class="section">
    <h2><span class="emoji">📦</span> Dependencies</h2>
    <div class="code-block">
streamlit>=1.28.0
pandas>=2.0.0
plotly>=5.15.0
numpy>=1.24.0
altair>=5.0.0
    </div>
</div>

<div class="section">
    <h2><span class="emoji">📁</span> Project Structure</h2>
    <div class="code-block">
lok-sabha-2024/
├── app.py                 # Main Streamlit application
├── data/
│   ├── election_results.csv
│   ├── constituency_data.csv
│   └── party_info.csv
├── utils/
│   ├── data_processing.py
│   ├── visualizations.py
│   └── helpers.py
├── assets/
│   ├── images/
│   └── styles/
├── requirements.txt
└── README.md
    </div>
</div>

<div class="section">
    <h2><span class="emoji">🎯</span> Usage Examples</h2>
    
    <h3>URL Parameters</h3>
    <p>You can directly access specific results using URL parameters:</p>
    <div class="code-block">
# View specific party results
https://lok-sabha-2024.streamlit.app/?party=BJP

# View state-wise results
https://lok-sabha-2024.streamlit.app/?state=Maharashtra

# View constituency results
https://lok-sabha-2024.streamlit.app/?constituency=Mumbai-North
    </div>

    <h3>Interactive Features</h3>
    <ul>
        <li>Use the sidebar to navigate between different analysis modes</li>
        <li>Click on charts for detailed breakdowns</li>
        <li>Download filtered data as CSV files</li>
        <li>Share specific views via URL parameters</li>
    </ul>
</div>

<div class="section">
    <h2><span class="emoji">📊</span> Key Statistics</h2>
    <div class="stats-grid">
        <div class="stat-card">
            <span class="stat-number">543</span>
            <span>Lok Sabha Constituencies</span>
        </div>
        <div class="stat-card">
            <span class="stat-number">28</span>
            <span>States Covered</span>
        </div>
        <div class="stat-card">
            <span class="stat-number">8</span>
            <span>Union Territories</span>
        </div>
        <div class="stat-card">
            <span class="stat-number">2000+</span>
            <span>Political Parties & Candidates</span>
        </div>
    </div>
</div>

<div class="section">
    <h2><span class="emoji">💾</span> Data Sources</h2>
    <ul>
        <li><strong>Election Commission of India</strong>: Official election results data</li>
        <li><strong>Constituency boundaries</strong>: Geographic and demographic information</li>
        <li><strong>Historical data</strong>: Previous election comparisons</li>
        <li><strong>Real-time updates</strong>: Live result feeds during counting</li>
    </ul>
</div>

<div class="section">
    <h2><span class="emoji">🤝</span> Contributing</h2>
    <p>We welcome contributions! Please follow these steps:</p>
    <ol>
        <li>Fork the repository</li>
        <li>Create a feature branch (<code>git checkout -b feature/amazing-feature</code>)</li>
        <li>Commit your changes (<code>git commit -m 'Add amazing feature'</code>)</li>
        <li>Push to the branch (<code>git push origin feature/amazing-feature</code>)</li>
        <li>Open a Pull Request</li>
    </ol>
</div>

<div class="section">
    <h2><span class="emoji">📱</span> Mobile Compatibility</h2>
    <p>The app is fully responsive and works seamlessly on:</p>
    <ul>
        <li><span class="emoji">📱</span> Mobile devices</li>
        <li><span class="emoji">📱</span> Tablets</li>
        <li><span class="emoji">💻</span> Desktop computers</li>
        <li><span class="emoji">🖥️</span> Large screens</li>
    </ul>
</div>

<div class="section">
    <h2><span class="emoji">🚀</span> Deployment</h2>
    <p>The app is deployed on <strong>Streamlit Community Cloud</strong> for free hosting and automatic deployments from GitHub.</p>
    
    <h3>Deploy Your Own Version</h3>
    <ol>
        <li>Fork this repository</li>
        <li>Connect your GitHub account to <a href="https://streamlit.io/cloud">Streamlit Community Cloud</a></li>
        <li>Deploy directly from your forked repository</li>
    </ol>
</div>

<div class="section">
    <h2><span class="emoji">🔗</span> Related Projects</h2>
    <ul>
        <li><a href="https://github.com/RAJPUTRoCkStAr/Election-results-dashboard">Election Results Dashboard</a></li>
        <li><a href="https://github.com/tanayatipre/GEMSQL-End-To-End-Text-to-SQL-LLM-Application">GEMSQL Election Analysis</a></li>
    </ul>
</div>

<div class="section">
    <h2><span class="emoji">📄</span> License</h2>
    <p>This project is licensed under the <strong>MIT License</strong> - see the LICENSE file for details.</p>
</div>

<div class="section">
    <h2><span class="emoji">🙏</span> Acknowledgments</h2>
    <ul>
        <li><strong>Election Commission of India</strong> for providing comprehensive election data</li>
        <li><strong>Streamlit</strong> team for the amazing framework</li>
        <li><strong>Open source community</strong> for various data visualization libraries</li>
        <li><strong>Contributors</strong> who helped improve this project</li>
    </ul>
</div>

<div class="footer">
    <h2><span class="emoji">📞</span> Contact & Support</h2>
    <p><strong>Issues</strong>: GitHub Issues</p>
    <p><strong>Discussions</strong>: GitHub Discussions</p>
    <p><strong>Email</strong>: your-email@domain.com</p>
    <br>
    <p><span class="emoji">⭐</span> <strong>If you find this project useful, please consider giving it a star!</strong></p>
    <br>
    <p><em>Built with <span class="emoji">❤️</span> using Python and Streamlit</em></p>
</div>

</body>
</html>

