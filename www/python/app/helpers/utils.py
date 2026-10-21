from pprint import pformat

def dd(data):
    if hasattr(data, 'to_dict') and callable(data.to_dict):
        content = data.to_dict()
    elif hasattr(data, '__dict__'):
        content = data.__dict__
    else:
        content = data

    formatted = pformat(content)
    
    html = f"""
    <div style="background: #1e1e1e; color: #d4d4d4; padding: 20px; font-family: monospace; font-size: 14px; line-height: 1.5; border-radius: 5px; margin: 20px;">
        <pre style="margin: 0;">{formatted}</pre>
    </div>
    """
    return html, 200