# WordPresser: Automated WordPress Vulnerability Management

WordPresser is an integrated vulnerability management toolchain built to identify and manage vulnerabilities in WordPress installations. This solution taps into the power of Pantheon's Terminus CLI and WPScan's API, offering a non-intrusive method of ascertaining vulnerabilities in WordPress plugins.

## 🚀 Key Features

- **Pantheon's Terminus CLI Integration**: Efficiently fetches WordPress sites and their installed plugins.
- **WPScan API Lookup**: Queries WPScan's API to fetch vulnerability data for each identified plugin, as opposed to active scanning.
- **Alerting Mechanism**: Utilizes `pymsteams` to forward detailed vulnerability alerts to Microsoft Teams.
- **Database Operations**: Engages a custom database for structured data storage, retrieval, and analysis.
- **SharePoint Integration**: Pushes database snapshots to SharePoint for data retention and sharing.
- **PowerBI Reporting**: Provides a graphical interface for users to introspect site details, plugin versions, and associated vulnerabilities.

## 💡 Technical Stack

- **Python**: Core scripting and automation.
- **Pantheon's Terminus CLI**: Facilitates WordPress site and plugin discovery.
- **WPScan**: Sourced for vulnerability details via its RESTful API.
- **pymsteams**: Powers Microsoft Teams notifications.
- **Pandas**: Data manipulation and CSV operations.
- **Requests**: Manages API interactions.

## 📋 Getting Started

### Prerequisites

- A working Python environment (Python 3.x recommended).
- API access to WPScan.
- Pantheon Terminus CLI configured and authenticated.
- Microsoft Teams Webhook for notifications.

### Installation

1. Clone this repository:

2. Navigate to the project directory and install the required dependencies:


### Configuration

Before you begin, ensure you've set up and configured the necessary integrations in the `settings.py`:

- Terminus CLI configurations
- WPScan API keys
- Database configurations
- Microsoft Teams Webhook
- SharePoint details for data uploads
- PowerBI setup details (if applicable)

## 🖥️ Usage

Once configurations are in place:

1. **Discovery & Analysis**:


2. **Alerting**:


3. **Reporting**:
- This process is automated via the PowerBI interface, fetching data uploaded to SharePoint.

## ✅ Benefits & Insights

- **Non-Intrusive Operation**: By directly interacting with WPScan's API instead of scanning sites, there's a substantial reduction in network noise and potential detection by intrusion detection systems.
- **Comprehensive Reporting**: With data storage on SharePoint and visualization through PowerBI, teams can easily introspect vulnerabilities, their associated risks, and the required mitigation steps.
- **Automated Workflows**: Eliminates manual efforts, offering a systematic approach to WordPress vulnerability management.

## 🤝 Contribution

Feel free to fork this repository and submit pull requests. For major changes, open an issue first to discuss what you would like to change.

## 📜 License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details.
