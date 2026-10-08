from bs4 import BeautifulSoup, NavigableString, Comment
import requests
import re
import json
from anthropic import Anthropic

def load_keys(path):
    with open(path, "r") as file:
        data = json.load(file)
        claude_key = data['claude-api']
        workspace_id = data['workspace-id']
        headers = data['headers']
    return claude_key, workspace_id, headers

def clean_file(url, headers):
    try:
        response = requests.get(url, headers=headers)
    except:
        return "Make sure to enter a valid URL :)"
    output = ""
    cleaned_html = ""
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, "html.parser")
        cleaned_html = ' '.join(soup.stripped_strings)
        cleaned_html = re.split(r"[\u200e\n\xa0*]", cleaned_html)
        cleaned_html = list(filter(None, cleaned_html))
        cleaned_html = " ".join(cleaned_html)
    return cleaned_html

LEGAL_ANALYSIS_PROMPT = """
You are an exceptional career adviser with outstanding legal expertise and ability to communicate complex legal terms to people with no legal background.

The user has uploaded a link to a "AGREEMENT AND PLAN OF MERGER" or "FORM OF SEPARATION AGREEMENT".
Data extraction and cleansing has already been performed.
Your job is to list out a/some:

1. SUMMARY: Write a plain-English summary of what is happening between the two companies (max 200 words). Be as succinct as possible.
 Avoid legal jargon. State the section that this is quoted from. Format the output as follows:
 - Who (the name of the two companies)
 - What (Are they merging or separating)
 - When (When will the process begin plus an overall timeline)
 - Why (Why is this merger or separation happen and the desired outcome this action hopes to produce)

2. AFFECTED DEPARTMENTS: One result of company acquisitions or separation is sometimes layoffs or relocation.
For mergers and acquisitions, owners and leaders may choose to layoff any employee if there are overlapping job responsibilities and position titles once the two companies combine.
For separations, employees may be reassigned, asked to relocate, or converted to different reporting structures as the new entities define operating models. State the section that this is quoted from. Be as succinct as possible.
For each affected department or product line, list out:
- name of the affected department or product line
- how will this department or product line be impacted
- recommended action step: continue to adapt to this changing organization or start applying elsewhere. If the answer is it depends, clearly state out why.

Format your response exactly like this:

## Summary
[Your summary here. If the text does not contain enough content to address the prompt, say "I don't think this is the right document."]

## AFFECTED DEPARTMENTS
[List each affected department followed by the reasoning. If none, say “No affected individuals identified.”]

DOCUMENT:
{document_text}
"""

def build_prompt(truncated_text):
 """Insert the document text into the prompt template."""
 return LEGAL_ANALYSIS_PROMPT.format(document_text=truncated_text)

token_1 = 128000
model_2 = "claude-sonnet-5-5"

def _analyze_with_anthropic(prompt, claude_key, workplace_id):
    """Use Claude via the Anthropic SDK."""
    client = Anthropic(
        api_key=claude_key,
        default_headers={"anthropic-workspace-id": workplace_id},
    )

    output_text = ""
    with client.messages.stream(
        model=model_2,
        max_tokens=token_1,
        messages=[{"role": "user", "content": prompt}],
    ) as stream:
        for text in st
        ream.text_stream:
            output_text = output_text + text + " "

    return output_text

