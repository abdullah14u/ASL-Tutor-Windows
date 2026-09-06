# Fluent-inspired Dark Theme Styling

COLORS = {
    "background": "#0F172A",      # Slate 900
    "surface": "#1E293B",         # Slate 800
    "surface_light": "#334155",   # Slate 700
    "primary": "#06B6D4",         # Cyan 500
    "success": "#10B981",         # Emerald 500
    "error": "#EF4444",           # Red 500
    "warning": "#F59E0B",         # Amber 500
    "text": "#F8FAFC",            # Slate 50
    "text_muted": "#94A3B8"       # Slate 400
}

MAIN_STYLE = f"""
QMainWindow {{
    background-color: {COLORS['background']};
    color: {COLORS['text']};
}}

QWidget {{
    color: {COLORS['text']};
    font-family: 'Segoe UI', -apple-system, BlinkMacSystemFont, Roboto, Arial, sans-serif;
}}

QFrame#SurfaceFrame {{
    background-color: {COLORS['surface']};
    border-radius: 12px;
}}

QLabel {{
    color: {COLORS['text']};
}}

QLabel#TitleLabel {{
    font-size: 24px;
    font-weight: bold;
    color: {COLORS['primary']};
}}

QLabel#SubtitleLabel {{
    font-size: 14px;
    color: {COLORS['text_muted']};
}}

QLabel#SignPrompt {{
    font-size: 120px;
    font-weight: bold;
    color: {COLORS['text']};
}}

QComboBox {{
    background-color: {COLORS['surface_light']};
    color: {COLORS['text']};
    border: 1px solid {COLORS['surface_light']};
    border-radius: 6px;
    padding: 6px 12px;
    font-size: 14px;
}}

QComboBox::drop-down {{
    border: none;
}}

QComboBox QAbstractItemView {{
    background-color: {COLORS['surface']};
    color: {COLORS['text']};
    selection-background-color: {COLORS['primary']};
    border: 1px solid {COLORS['surface_light']};
    border-radius: 4px;
}}
"""
