def section_header(title: str, subtitle: str = "", icon: str = "") -> str:
    """Return an HTML section header."""
    return f"""
    <div style="margin: 20px 0 24px 0; 
                padding-bottom: 16px;
                border-bottom: 1px solid rgba(0,212,255,0.15);">
        <div style="font-size:28px; 
                   font-weight:700; 
                   color:white;
                   font-family: sans-serif; 
                   letter-spacing:2px;">
            {icon}; {title.upper()}
        </div>
        <div style="font-size:16px; 
                    color:white;
                    margin-top:4px;
                    font-family:sans-serif; letter-spacing:1px;">
            {subtitle}
        </div>
    </div>
    """

def load_css():
    return """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Rajdhani:wght@400;600;700&display=swap');

    [data-testid="stAppViewContainer"] {
    background: radial-gradient(circle at 80% 20%, rgba(139,92,246,0.25), transparent 40%),
                radial-gradient(circle at 20% 30%, rgba(236,72,153,0.2), transparent 40%),
                linear-gradient(135deg, #0b0f2a 0%, #1a1147 50%, #0b0f2a 100%) !important;
    }

    /*glow ring*/
    [data-testid="stAppViewContainer"]::after {
        content: "";
        position: fixed;
        right: -150px;
        top: 50px;
        width: 400px;
        height: 400px;
        background: radial-gradient(circle, rgba(168,85,247,0.25), transparent 70%);
        filter: blur(60px);
        z-index: 0;
    }


    /* ===== BUTTONS ===== */
    .stButton > button {
        background: linear-gradient(135deg, #6366f1, #ec4899);
        color: white;
        border-radius: 10px;
        border: none;
        font-weight: 600;
    }
    </style>
    """