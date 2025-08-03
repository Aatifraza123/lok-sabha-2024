# 🗳️ Lok Sabha Election 2024 - Results Dashboard

**A comprehensive Streamlit web application for analyzing and visualizing the 2024 Lok Sabha Election results**

[![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)](https://streamlit.io/)
[![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org/)
[![Pandas](https://img.shields.io/badge/Pandas-150458?style=for-the-badge&logo=pandas&logoColor=white)](https://pandas.pydata.org/)
[![Plotly](https://img.shields.io/badge/Plotly-3F4F75?style=for-the-badge&logo=plotly&logoColor=white)](https://plotly.com/)

## 🚀 Live Demo

**Visit the live application:** [https://lok-sabha-2024.streamlit.app/](https://lok-sabha-2024.streamlit.app/)

---

## 📋 Overview

This interactive dashboard provides detailed insights into the **2024 Indian General Election results**. Built with **Streamlit**, the app offers an intuitive interface to explore constituency-wise results, party performance, state-wise trends, and comprehensive election analytics.

## ✨ Features

### 🏛️ **Election Analysis**
- **Constituency-wise Results**: Detailed breakdown of results for all 543 constituencies
- **Party Performance**: Comprehensive analysis of major political parties (BJP, INC, AAP, etc.)
- **State-wise Trends**: Regional election patterns and voting behavior
- **Candidate Information**: Details about winning and runner-up candidates

### 📊 **Data Visualizations**
- Interactive charts and graphs
- Pie charts for vote share distribution
- Bar charts for party-wise seat count
- Geographic visualization of results
- Trend analysis and comparisons

### 🔍 **Search & Filter Options**
- Search by constituency name
- Filter by state/union territory
- Filter by political party
- Advanced filtering options

### 📱 **User-Friendly Interface**
- Responsive design for all devices
- Clean and intuitive navigation
- Real-time data updates
- Export functionality for data analysis

## 🛠️ Installation & Setup

### Prerequisites
- Python 3.8 or higher
- pip package manager

### Local Development

1. **Clone the repository**
git clone https://github.com/your-username/lok-sabha-2024.git
cd lok-sabha-2024

2. **Create virtual environment**
python -m venv venv
source venv/bin/activate # On Windows: venv\Scripts\activate

3. **Install dependencies**
pip install -r requirements.txt

4. **Run the application**
streamlit run app.py

5. **Access the app**
Open your browser and navigate to `http://localhost:8501`

## 📦 Dependencies
streamlit>=1.28.0
pandas>=2.0.0
plotly>=5.15.0
numpy>=1.24.0
altair>=5.0.0
requests>=2.31.0

## 📁 Project Structure
lok-sabha-2024/
├── app.py # Main Streamlit application
├── data/
│ ├── election_results.csv
│ ├── constituency_data.csv
│ └── party_info.csv
├── utils/
│ ├── data_processing.py
│ ├── visualizations.py
│ └── helpers.py
├── assets/
│ ├── images/
│ └── styles/
├── requirements.txt
└── README.md

## 🎯 Usage Examples

### Query by URL Parameters
You can directly access specific results using URL parameters:
View specific party results
https://lok-sabha-2024.streamlit.app/?party=BJP

View state-wise results
https://lok-sabha-2024.streamlit.app/?state=Maharashtra

View constituency results
https://lok-sabha-2024.streamlit.app/?constituency=Mumbai-North


### Interactive Features
- Use the sidebar to navigate between different analysis modes
- Click on charts for detailed breakdowns
- Download filtered data as CSV files
- Share specific views via URL parameters

## 📊 Key Statistics

| Metric | Count |
|--------|-------|
| **Lok Sabha Constituencies** | 543 |
| **States Covered** | 28 |
| **Union Territories** | 8 |
| **Political Parties & Candidates** | 2000+ |

## 💾 Data Sources

- **Election Commission of India**: Official election results data
- **Constituency boundaries**: Geographic and demographic information
- **Historical data**: Previous election comparisons
- **Real-time updates**: Live result feeds during counting

## 🤝 Contributing

We welcome contributions! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Development Guidelines
- Follow PEP 8 style guide
- Add comments for complex logic
- Update documentation for new features
- Write tests for new functionality

## 🔗 Related Projects

- [Election Results Dashboard](https://github.com/RAJPUTRoCkStAr/Election-results-dashboard)
- [GEMSQL Election Analysis](https://github.com/tanayatipre/GEMSQL-End-To-End-Text-to-SQL-LLM-Application)

## 📱 Mobile Compatibility

The app is fully responsive and works seamlessly on:
- 📱 Mobile devices
- 📱 Tablets  
- 💻 Desktop computers
- 🖥️ Large screens

## 🚀 Deployment

The app is deployed on **Streamlit Community Cloud** for free hosting and automatic deployments from GitHub.

### Deploy Your Own Version
1. Fork this repository
2. Connect your GitHub account to [Streamlit Community Cloud](https://streamlit.io/cloud)
3. Deploy directly from your forked repository

## 📸 Screenshots

### Main Dashboard
![Main Dashboard](assets/images/dashboard.png)

### Constituency Analysis
![Constituency Analysis](assets/images/constituency.png)

### Party Performance
![Party Performance](assets/images/party_performance.png)

## 🔧 Configuration

### Environment Variables

Optional: Set custom configuration
STREAMLIT_SERVER_PORT=8501
STREAMLIT_SERVER_HEADLESS=true

### Custom Styling
Modify `assets/styles/custom.css` to customize the appearance.

## 📈 Performance

- **Load Time**: < 3 seconds
- **Data Processing**: Optimized for large datasets
- **Memory Usage**: Efficient data handling
- **Caching**: Streamlit's built-in caching for faster responses

## 🔒 Privacy & Security

- No personal data collection
- Public election data only
- Secure hosting on Streamlit Cloud
- No cookies or tracking

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **Election Commission of India** for providing comprehensive election data
- **Streamlit** team for the amazing framework
- **Open source community** for various data visualization libraries
- **Contributors** who helped improve this project

## 📞 Contact & Support

- **Issues**: [GitHub Issues](https://github.com/your-username/lok-sabha-2024/issues)
- **Discussions**: [GitHub Discussions](https://github.com/your-username/lok-sabha-2024/discussions)
- **Email**: your-email@domain.com

## 🗺️ Roadmap

- [ ] Add more interactive visualizations
- [ ] Include historical election comparisons
- [ ] Add multilingual support
- [ ] Implement advanced analytics features
- [ ] Mobile app development

## ❓ FAQ

**Q: How often is the data updated?**
A: Data is updated in real-time during election counting and regularly thereafter.

**Q: Can I use this for commercial purposes?**
A: Yes, under the MIT license terms.

**Q: How can I contribute data?**
A: Please follow the contributing guidelines and submit a pull request.

---

⭐ **If you find this project useful, please consider giving it a star!**

*Built with ❤️ using Python and Streamlit*

---

## 🏷️ Tags

`streamlit` `python` `election-results` `data-visualization` `dashboard` `plotly` `pandas` `lok-sabha` `india` `politics` `analytics` `interactive` `web-app`
