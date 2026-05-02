import requests
from bs4 import BeautifulSoup


def extract_text(file=None, url=None):
    """
    Extract raw text from PDF file or URL.
    Returns string of extracted text.
    """
    if file:
        return _extract_from_pdf(file)
    elif url:
        return _extract_from_url(url)
    return ''


def _extract_from_pdf(file):
    """Extract text from PDF file."""
    try:
        import PyPDF2
        text_parts = []
        if hasattr(file, 'read'):
            reader = PyPDF2.PdfReader(file)
        else:
            reader = PyPDF2.PdfReader(file.path)
        for page in reader.pages:
            text = page.extract_text()
            if text:
                text_parts.append(text.strip())
        return '\n'.join(text_parts)
    except Exception as e:
        return f"PDF o'qishda xato: {str(e)}"


def _extract_from_url(url):
    """Extract text from URL by scraping."""
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        response = requests.get(url, headers=headers, timeout=15)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        # Remove scripts and styles
        for tag in soup(['script', 'style', 'nav', 'footer', 'header']):
            tag.decompose()
        text = soup.get_text(separator=' ', strip=True)
        # Limit to 3000 chars for API efficiency
        return text[:3000]
    except Exception as e:
        return f"URL o'qishda xato: {str(e)}"
