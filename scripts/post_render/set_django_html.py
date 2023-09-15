from bs4 import BeautifulSoup
from pathlib import Path 
import sys

# root project path
root = Path(__file__).resolve().parents[2]
sys.path.append(root.as_posix())

# import utils
from source import utils

site = root / '_site'

# all quarto generated html files
html_files = site.glob('**/*.html')

# file manipulation happens in this for loop
for file in html_files:
    html = file.read_text()
    soup = BeautifulSoup(html)

    # html elements that need to be altered
    scripts = soup.find_all('script')
    links = soup.find_all('link')
    a_s = soup.find_all('a')
    imgs = soup.find_all('img')

    for script in scripts:
        if script.attrs.get('src') and ("site_libs" in script.attrs['src'] or '../' in script.attrs['src'] or './' in script.attrs['src']):
            src = script.attrs['src']
            src = src if ('../' not in src and './' not in src) else src.replace('../', '').replace('./', '')
            script.attrs['src'] = f"{{% static '{src}' %}}"

    for link in links:
        if link.attrs.get('href') and "site_libs" in link.attrs["href"] or '../' in link.attrs['href'] or './' in link.attrs['href']:
            href = link.attrs['href']
            href = href if ('../' not in href and './' not in href) else href.replace('../', '').replace('./', '')
            link.attrs['href'] = f"{{% static '{href}' %}}"

    for a in a_s:
        if a.attrs.get('href') and ( "./" == a.attrs['href'][:2] or '../' in a.attrs['href'] or './' in a.attrs['href']):
            href = a.attrs['href']
            href = href if ('../' not in href and './' not in href) else href.replace('../', '').replace('./', '')
            a.attrs['href'] = '/' + href

    for img in imgs:
        if img.attrs.get('src') and 'http' not in img.attrs['src']:
            src = img.attrs.get('src')
            src = src.replace('../', '').replace('./', '')
            if 'index_files' in src and file.parent.name != '_site':
                subpath = utils.get_project_subpath(file)  
                src = Path('projects') / Path(subpath).parent / src

            img.attrs['src'] = f"{{%  static '{src}' %}}"

    # Adding support for 
        # django's `static` templating tag
        # custom tags set in django_site/quarto/templatetags/tags.py
        # The ability to pass messages to the user (A bit ugly on the front end, I might change this)
    new_html = '''
    {% load static %}\n{% load tags %}\n\n{% if messages %}
    <ul class="messages">
    {% for message in messages %}
    <li{% if message.tags %} class="{{ message.tags }}"{% endif %}>{{ message }}</li>
    {% endfor %}
</ul>
{% endif %}'''

    # Adding a button to copy a share link to the clipboard
    # Remove this code block if you do not want this feature
    if 'projects' in file.as_posix():
        children = soup.find('main', {'id': 'quarto-document-content'}).findNext()
        button = soup.new_tag('button')
        button.attrs['id'] = 'copy-button'
        button.attrs['type'] = 'button'
        button.attrs['class'] = "copy-button btn btn-primary"
        button.attrs['onclick'] = "CopyToClipboard('share_link')"
        button.string = "Copy Share Link"
        children.append(button)

        new_html += """
        <script>
        function CopyToClipboard(id) {
                var copyText = document.getElementById(id);

                // Select the text field
                copyText.select();
                copyText.setSelectionRange(0, 99999); // For mobile devices

                // Copy the text inside the text field
                navigator.clipboard.writeText(copyText.value);

                var button = document.getElementById("copy-button")
                button.style.background = "grey";
                button.textContent = 'Copied!'
                }
        </script>
        <textarea id="share_link" style="display: none;">{% call_method request.user 'generate_share_link' request.path %}</textarea>
        """
    
    # final html content
    new_html += str(soup) + """
    {% if 'share' in request.path %}
    <script>
        var element = document.getElementById("copy-button");
        element.remove();
    </script>
    {% endif %}
    """

    file.write_text(new_html)