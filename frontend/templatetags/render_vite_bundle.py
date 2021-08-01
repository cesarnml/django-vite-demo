# This template tag is needed for production
# Add it to (/frontend/templatetags/render_vite_bundle.py)

import os
import json
from pathlib import Path

from django import template
from django.conf import settings
from django.utils.safestring import mark_safe

# Will use to register templatetags as simple_tag
register = template.Library()

# Helper method to load vite's manifest.json
def load_json_from_dist(json_filename="manifest.json"):
  manifest_file_path = Path(str(settings.VITE_APP_DIR), 'dist', json_filename)
  if not manifest_file_path.exists():
    raise FileNotFoundError(f"Vite manifest file not found on path: {str(manifest_file_path)}")
  else:
    with open(manifest_file_path, 'r') as manifest_file:
      try:
        manifest = json.load(manifest_file)
      except json.decoder.JSONDecodeError as e:
        raise ValueError(f"Failed to parse Vite manifest file: {str(manifest_file_path)}") from e
      else:
        return manifest

@register.simple_tag
def render_vite_bundle():
  """
  Template tag to render a vite bundle.
  Only use in production.
  """
  manifest = load_json_from_dist()

  imports_files = "".join(
    [
      f'<script type="module" src="/static/{manifest[file]["file"]}"></script>'
      for file in manifest["index.html"]["imports"]
    ]
  )

  return mark_safe(
    f"""<script type="module" src="/static/{manifest['index.html']['file']}"></script>
    <link rel="stylesheet" type="text/css" href="/static/{manifest['index.html']['css'][0]}" />
    {imports_files}"""
  )
