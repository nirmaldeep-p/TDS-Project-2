# /// script
# requires-python = ">=3.11"
# dependencies = [
#   "seaborn",
#   "pandas",
#   "matplotlib",
#   "httpx",
#   "chardet",
#   "ipykernel",
#   "openai",
#   "numpy",
#   "scipy",
#   "pathlib",
#   "asyncio",
#   "ipykernel",
# ]
# ///

import os
import sys
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import httpx
import chardet
from pathlib import Path
import asyncio
import scipy.stats as stats


API_URL = "https://aiproxy.sanand.workers.dev/openai/v1/chat/completions"

def get_token():
    try:
        return os.environ["AIPROXY_TOKEN"]
    except KeyError as e:
        print(f"Error")
        raise

async def data_load(file_path):
    """Load CSV data with encoding detection."""
    if not os.path.isfile(file_path):
        raise FileNotFoundError(f"Error: File '{file_path}' not found.")

    with open(file_path, 'rb') as f:
        result = chardet.detect(f.read())
    enc = result['encoding']
    print(f"File Encoding: {enc}")
    return pd.read_csv(file_path, encoding=enc)

async def post_request(headers, data):
    """Async function to make HTTP requests."""
    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(API_URL, headers=headers, json=data, timeout=30.0)
            response.raise_for_status()
            return response.json()['choices'][0]['message']['content']
        except httpx.HTTPStatusError as e:
            print(f"HTTP error occurred: {e}")
            raise
        except Exception as e:
            print(f"Error during request: {e}")
            raise

async def generate_narr(analysis, token, file_path):
    """Generating narrative using LLM."""
    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json'
    }

    prompt = (
        f"Assume you are a data analyst. Provide a detailed narrative based on the following data analysis results for the file '{file_path.name}':\n\n"
        f"Column Names & Types: {list(analysis['summary'].keys())}\n\n"
        f"Summary Statistics: {analysis['summary']}\n\n"
        f"Missing Values: {analysis['missing_values']}\n\n"
        f"Correlation Matrix: {analysis['correlation']}\n\n"
        "Please provide detailed insights into trends, outliers, anomalies, or patterns. "
        "Suggest further analyses like clustering or anomaly detection. "
        "Discuss how these trends may impact future decisions."
    )

    data = {
        "model": "gpt-4o-mini",
        "messages": [{"role": "user", "content": prompt}]
    }

    return await post_request(headers, data)

async def analyze_data(df, token):
    """Use LLM to suggest and perform data analysis."""
    if df.empty:
        raise ValueError("Error: Dataset is empty.")

    # Enhanced prompt for better LLM analysis suggestions
    prompt = (
        f"You are a data analyst. Given the following dataset information, provide an analysis plan and suggest useful techniques:\n\n"
        f"Columns: {list(df.columns)}\n"
        f"Data Types: {df.dtypes.to_dict()}\n"
        f"First 5 rows of data:\n{df.head()}\n\n"
        "Suggest data analysis techniques, such as correlation, regression, anomaly detection, clustering, or others. "
        "Consider missing values, categorical variables, and scalability."
    )

    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json'
    }
    data = {
        "model": "gpt-4o-mini",
        "messages": [{"role": "user", "content": prompt}]
    }

    try:
        suggestions = await post_request(headers, data)
    except Exception as e:
        suggestions = f"Error fetching suggestions: {e}"

    print(f"LLM Suggestions: {suggestions}")

    # Basic analysis (summary statistics, missing values, correlations)
    numeric_df = df.select_dtypes(include=['number'])
    analysis = {
        'summary': df.describe(include='all').to_dict(),
        'missing_values': df.isnull().sum().to_dict(),
        'correlation': numeric_df.corr().to_dict() if not numeric_df.empty else {}
    }

    # Hypothesis testing example (if 'A' and 'B' columns exist)
    if 'A' in df.columns and 'B' in df.columns:
        t_stat, p_value = stats.ttest_ind(df['A'].dropna(), df['B'].dropna())
        analysis['hypothesis_test'] = {
            't_stat': t_stat,
            'p_value': p_value
        }

    print("Data analysis complete.")
    return analysis, suggestions

async def visualize_data(df, output_dir):
    numeric_cols = df.select_dtypes(include=[np.number]).columns

    if len(numeric_cols) == 0:
        print("No numeric columns available for visualization.")
        return []

    image_paths = []

    # Plot 1: Distribution of the first numeric column
    plt.figure(figsize=(8, 6))
    sns.histplot(df[numeric_cols[0]], kde=True, color='blue')
    plt.title(f"Distribution of {numeric_cols[0]}")
    image_path = os.path.join(output_dir, f"distribution_{numeric_cols[0]}.png")
    plt.savefig(image_path)
    plt.close()
    image_paths.append(image_path)

    # Plot 2: Distribution of the second numeric column (if available)
    if len(numeric_cols) > 1:
        plt.figure(figsize=(8, 6))
        sns.histplot(df[numeric_cols[1]], kde=True, color='green')
        plt.title(f"Distribution of {numeric_cols[1]}")
        image_path = os.path.join(output_dir, f"distribution_{numeric_cols[1]}.png")
        plt.savefig(image_path)
        plt.close()
        image_paths.append(image_path)

    # Plot 3: Correlation heatmap
    plt.figure(figsize=(10, 8))
    corr = df[numeric_cols].corr()
    sns.heatmap(corr, annot=True, cmap='coolwarm', fmt=".2f")
    plt.title("Correlation Heatmap")
    image_path = os.path.join(output_dir, "correlation_heatmap.png")
    plt.savefig(image_path)
    plt.close()
    image_paths.append(image_path)

    print("Visualizations saved.")
    return image_paths


async def save_narrative_with_images(narrative, output_dir):
    """Save narrative to README.md and embed image links."""
    readme_path = output_dir / 'README.md'
    image_links = "\n".join(
        [f"![{img.name}]({img.name})" for img in output_dir.glob('*.png')]
    )
    with open(readme_path, 'w') as f:
        f.write(narrative + "\n\n" + image_links)
    print(f"Narrative successfully written to {readme_path}")

async def main(file_path):
    print("Starting autolysis process...")

    # Ensure input file exists
    file_path = Path(file_path)
    if not file_path.is_file():
        print(f"Error: File '{file_path}' does not exist.")
        sys.exit(1)

    # Load token
    try:
        token = get_token()
    except Exception as e:
        print(e)
        sys.exit(1)

    # Load dataset
    try:
        df = await data_load(file_path)
    except FileNotFoundError as e:
        print(e)
        sys.exit(1)

    # Analyze data with LLM insights
    try:
        analysis, suggestions = await analyze_data(df, token)
    except ValueError as e:
        print(e)
        sys.exit(1)

    print(f"Suggestions: {suggestions}")

    # Create output directory
    output_dir = Path(file_path.stem)  # Create a directory named after the dataset
    output_dir.mkdir(exist_ok=True)

    # Generate visualizations with LLM suggestions
    await visualize_data(df, output_dir)

    # Generate narrative
    narrative = await generate_narr(analysis, token, file_path)

    if narrative != "Narrative generation failed due to an error.":
        await save_narrative_with_images(narrative, output_dir)
    else:
        print("Narrative generation failed.")

# Execute script
if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python script.py <file_path>")
        sys.exit(1)
    asyncio.run(main(sys.argv[1]))
