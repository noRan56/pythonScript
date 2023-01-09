import re
import requests
from bs4 import BeautifulSoup
page_content = ''

def extract_emails(text):
  # Use a regular expression to find email addresses
  email_pattern = r'[\w\.-]+@[\w\.-]+'
  return re.findall(email_pattern, text)

def get_emails_from_page (url):
  # Fetch the page content
  response = requests.get(url)
  page_content = response.text
  
  emails = extract_emails(page_content)

  
  # Find any links in the page content
  soup = BeautifulSoup(page_content, 'html.parser')
  links = soup.find_all('a')

  
  # Follow the links and extract email addresses from any pages we find
  for link in links:
    link_url = link.get('href')
    if link_url and link_url.startswith('http'):
      emails.extend(get_emails_from_page(link_url))
  
  return emails

def get_subdomains(root_domain):
  # Use a regular expression to find subdomains
  subdomain_pattern = r'[\w\.-]+\.' + root_domain
  return re.findall(subdomain_pattern, page_content )

def get_emails_from_subdomain(subdomain):
  # Construct the URL for the subdomain
  url = f"http://{subdomain}"
  return get_emails_from_page(url)

# Test the functions
root_domains = ["example.com", "example.net", "example.org"]
for root_domain in root_domains:
  subdomains = get_subdomains(root_domain)
  for subdomain in subdomains:
    emails = get_emails_from_subdomain(subdomain)
    print(f"Emails from {subdomain}: {emails}")
