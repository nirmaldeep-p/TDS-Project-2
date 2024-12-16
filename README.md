# TDS_Project2_22f2001246

# Autolysis: Automated Data Analysis and Report Generation

## Project Overview

Autolysis is a Python-based project designed to automate the process of generating data-driven stories, complete with visualizations and narrative insights. Leveraging the power of large language models (LLMs) and OpenAI's Vision API, this project takes in structured datasets, performs analysis, creates visualizations, and composes comprehensive reports in natural language. These outputs include README files with descriptive insights and charts that can be directly used for presentations or evaluations.

## Features

1. **Data Analysis and Visualization**:

   - Autolysis reads structured datasets (e.g., CSV files).
   - It performs automated analysis, including descriptive statistics and trend identification.
   - Charts and graphs are generated to visually represent the data.

2. **Natural Language Story Generation**:

   - The tool generates a narrative that describes the dataset, the analysis performed, insights discovered, and actionable implications.
   - The output README.md file is written in a human-readable format.

3. **Robust API Integration**:

   - Uses OpenAI's LLMs for natural language generation.
   - Utilizes OpenAI's image generation API for creating charts.
   - Built-in retry logic with Tenacity ensures smooth handling of API rate limits and transient errors.

4. **Efficient and Cost-Effective**:

   - Images are generated with `"detail": "low"` to reduce API costs.
   - Tokens for LLM queries are limited to balance cost and effectiveness.

### Output

The script generates the following outputs in the current working directory:

1. **README.md**: Contains the data story and insights.
2. **Charts**: PNG files visualizing key aspects of the data.

## Key Components

### autolysis.py

The main script processes input datasets and performs the following steps:

1. **Data Ingestion**: Reads CSV files into pandas DataFrames.
2. **Analysis**: Performs statistical and trend analyses.
3. **Visualization**: Generates 512x512 px PNG charts using OpenAI Vision API.
4. **Story Generation**: Creates a detailed README.md file using OpenAI LLMs.

### Example Datasets

- **Goodreads**: A dataset of book ratings and reviews.
- **Happiness**: A dataset of happiness scores by country.
- **Media**: A dataset analyzing media consumption patterns.

## Example Output

### Sample README.md

```markdown
# Analysis of the Happiness Dataset

## Dataset Overview
This dataset contains happiness scores for various countries, along with associated metrics such as GDP per capita, social support, and life expectancy.

## Key Insights
1. **Correlation Between Metrics**:
   - High GDP per capita strongly correlates with higher happiness scores.
   - Social support plays a significant role in overall happiness.

2. **Geographical Trends**:
   - Scandinavian countries consistently rank at the top.
   - Developing countries often score lower, highlighting economic disparities.

## Implications
Policymakers should focus on improving social support systems and healthcare infrastructure to boost happiness levels in low-ranking countries.
```

### Example Chart

A 512x512 visualization of the correlation between GDP per capita and happiness scores.

## Cost Considerations

1. **Token Limits**:

   - Maximum tokens for LLM calls: 1500.
   - Estimated cost: \$0.045 per API call (based on GPT-4 rates).

2. **Image Generation**:

   - Small-sized (512x512 px) images.
   - Cost reduction by using `"detail": "low"` in OpenAI Vision API.

## Troubleshooting

### Common Errors and Fixes

1. **AuthenticationError**:

   - Ensure the `AIPROXY_TOKEN` environment variable is set with a valid API key.

2. **Rate Limits (HTTP 429)**:

   - The script automatically retries using Tenacity.

3. **Module Not Found**:

   - Ensure all required libraries are installed.

### Debugging

Use logging to capture errors and debug the script.

## Future Improvements

1. Integrate additional analysis methods (e.g., predictive modeling).
2. Support for larger datasets and more complex visualizations.
3. Add localization for multilingual README outputs.

## License

This project is licensed under the MIT License. See the LICENSE file for details.

## Acknowledgments

- OpenAI for providing GPT-4 and Vision APIs.
- The Tenacity library for robust retry mechanisms.

