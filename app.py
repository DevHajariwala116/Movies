import requests
import streamlit as st
from typing import Optional

API_BASE = "https://movie-rec-466x.onrender.com"
TMDB_IMG = "https://image.tmdb.org/t/p/w500"

st.set_page_config(
    page_title="Devflix",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="collapsed",
)

st.markdown(
    """
    <link href="https://fonts.googleapis.com/css2?family=Bebas+Neue&family=DM+Sans:ital,wght@0,300;0,400;0,500;0,600;1,300&family=Space+Mono:wght@400;700&family=Playfair+Display:ital,wght@0,700;0,900;1,700&display=swap" rel="stylesheet">

    <style>
        /* ══ HIDE STREAMLIT CHROME ══ */
        #MainMenu, header, footer,
        [data-testid="stSidebar"],
        [data-testid="collapsedControl"],
        [data-testid="stToolbar"],
        section[data-testid="stSidebarNav"],
        .stDeployButton { display: none !important; visibility: hidden !important; }

        /* ══ TOKENS ══ */
        :root {
            --void:      #04060F;
            --deep:      #070A17;
            --surface:   #0C1020;
            --elevated:  #101525;

            --cyan:      #00E5FF;
            --cyan-mid:  #00B8D9;
            --crimson:   #FF2D5B;
            --teal:      #00C9A7;
            --violet:    #7C3FFF;

            --t1: rgba(255,255,255,0.94);
            --t2: rgba(200,215,235,0.62);
            --t3: rgba(140,165,200,0.32);

            --gc:  rgba(0,229,255,0.08);
            --gb:  rgba(0,229,255,0.12);

            --grad: linear-gradient(135deg,#00E5FF 0%,#7C3FFF 50%,#FF2D5B 100%);
            --gradct: linear-gradient(135deg,#00E5FF 0%,#00C9A7 100%);
        }

        /* ══ GLOBAL RESET ══ */
        html, body, [data-testid="stAppViewContainer"] {
            background: var(--void) !important;
            font-family: 'DM Sans', sans-serif;
        }

        /* ══ AMBIENT GLOW ══ */
        [data-testid="stAppViewContainer"]::before {
            content: '';
            position: fixed; inset: 0; pointer-events: none; z-index: 0;
            background:
                radial-gradient(ellipse 80% 55% at 10% 10%, rgba(0,229,255,.06) 0%, transparent 55%),
                radial-gradient(ellipse 60% 70% at 90% 90%, rgba(255,45,91,.08) 0%, transparent 55%),
                radial-gradient(ellipse 50% 50% at 55% 45%, rgba(124,63,255,.05) 0%, transparent 65%);
        }

        /* film-grain */
        [data-testid="stAppViewContainer"]::after {
            content: '';
            position: fixed; inset: 0; pointer-events: none; z-index: 0; opacity: .5;
            background-image: url("data:image/svg+xml,%3Csvg viewBox='0 0 512 512' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='g'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.85' numOctaves='4' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23g)' opacity='0.03'/%3E%3C/svg%3E");
        }

        [data-testid="stAppViewContainer"] > .main { background: transparent; position: relative; z-index: 1; }

        /* ══ FULL WIDTH CONTAINER ══ */
        .block-container {
            padding: 0 0 4rem !important;
            max-width: 100% !important;
            position: relative; z-index: 1;
        }

        /* ══ TOP NAV ══ */
        .devflix-nav {
            position: sticky; top: 0; z-index: 100;
            display: flex; align-items: center; justify-content: space-between;
            padding: 0 clamp(1rem, 4vw, 3.5rem);
            height: 64px;
            background: rgba(4,6,15,.88);
            border-bottom: 1px solid rgba(0,229,255,.08);
            backdrop-filter: blur(28px);
            -webkit-backdrop-filter: blur(28px);
        }
        .nav-logo {
            font-family: 'Bebas Neue', sans-serif;
            font-size: clamp(1.5rem, 4vw, 2rem);
            letter-spacing: 6px;
            background: var(--grad);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            filter: drop-shadow(0 0 16px rgba(0,229,255,.35));
            flex-shrink: 0;
        }
        .nav-center {
            display: flex; gap: 28px; align-items: center;
        }
        .nav-link {
            font-family: 'Space Mono', monospace;
            font-size: .62rem; letter-spacing: 2.5px;
            text-transform: uppercase; color: var(--t2);
            cursor: pointer; border: none; background: none; padding: 4px 0;
            transition: color .2s ease; border-bottom: 1px solid transparent;
            white-space: nowrap;
        }
        .nav-link:hover, .nav-link.active { color: var(--cyan); border-bottom-color: rgba(0,229,255,.5); }
        .nav-right { display: flex; gap: 10px; align-items: center; }

        /* ══ HERO ══ */
        .hero-section {
            padding: clamp(2.5rem, 6vw, 5rem) clamp(1rem, 4vw, 3.5rem) clamp(2rem, 4vw, 3rem);
        }
        .hero-eyebrow {
            font-family: 'Space Mono', monospace; font-size: clamp(.55rem,.9vw,.65rem);
            letter-spacing: 5px; text-transform: uppercase; color: var(--cyan); opacity: .7; margin-bottom: 14px;
        }
        .hero-title {
            font-family: 'Bebas Neue', sans-serif;
            font-size: clamp(4rem, 13vw, 11rem);
            letter-spacing: clamp(2px, .5vw, 6px); line-height: .9; color: var(--t1);
        }
        .hero-accent-word {
            background: var(--grad);
            -webkit-background-clip: text; -webkit-text-fill-color: transparent;
            background-clip: text; filter: drop-shadow(0 0 40px rgba(0,229,255,.4));
        }
        .hero-rule { width: clamp(40px,5vw,64px); height: 2px; background: var(--gradct);
            border-radius: 2px; margin: clamp(12px,2vw,20px) 0;
            box-shadow: 0 0 14px rgba(0,229,255,.5); }
        .hero-tagline {
            font-family: 'DM Sans', sans-serif; font-weight: 300;
            font-size: clamp(.75rem,1.2vw,.95rem); color: var(--t3);
            letter-spacing: 4px; text-transform: uppercase;
        }

        /* ══ CONTROLS BAR ══ */
        .controls-bar {
            padding: 0 clamp(1rem, 4vw, 3.5rem) clamp(1rem,2vw,1.5rem);
            display: flex; flex-direction: column; gap: 14px;
        }

        /* ══ SEARCH ══ */
        .stTextInput > div > div > input {
            background: rgba(0,229,255,.03) !important;
            border: 1px solid rgba(0,229,255,.14) !important;
            border-radius: 8px !important;
            color: var(--t1) !important;
            padding: 14px 22px !important;
            font-size: clamp(.85rem,1.5vw,.97rem) !important;
            font-family: 'DM Sans', sans-serif !important;
            font-weight: 300 !important;
            transition: all .35s ease !important;
            box-shadow: 0 8px 32px rgba(0,0,0,.4) !important;
        }
        .stTextInput > div > div > input::placeholder { color: rgba(140,165,200,.28) !important; font-style: italic; }
        .stTextInput > div > div > input:focus {
            border-color: rgba(0,229,255,.5) !important;
            background: rgba(0,229,255,.055) !important;
            box-shadow: 0 0 0 3px rgba(0,229,255,.08), 0 8px 40px rgba(0,229,255,.12) !important;
        }

        /* ══ SELECTBOX ══ */
        .stSelectbox > div > div {
            background: rgba(0,229,255,.03) !important;
            border: 1px solid rgba(0,229,255,.12) !important;
            border-radius: 8px !important; color: var(--t1) !important;
            font-family: 'DM Sans', sans-serif !important;
        }

        /* ══ SLIDER ══ */
        .stSlider [data-baseweb="slider"] div[role="slider"] {
            background: linear-gradient(135deg,#00E5FF,#7C3FFF) !important;
            box-shadow: 0 0 12px rgba(0,229,255,.6) !important;
        }
        .stSlider [data-baseweb="slider"] [role="progressbar"] {
            background: linear-gradient(90deg,#00E5FF,#7C3FFF) !important;
        }
        .stSlider label { font-family: 'Space Mono',monospace !important; font-size: .6rem !important;
            letter-spacing: 2px !important; text-transform: uppercase !important;
            color: rgba(0,229,255,.5) !important; }

        /* ══ CATEGORY PILLS ROW ══ */
        .cat-pills {
            display: flex; gap: 8px; flex-wrap: wrap; align-items: center;
            padding: 0 clamp(1rem, 4vw, 3.5rem); margin-bottom: 1rem;
        }
        .cat-pill {
            font-family: 'Space Mono', monospace; font-size: .60rem; letter-spacing: 2px;
            text-transform: uppercase; padding: 7px 16px; border-radius: 20px; cursor: pointer;
            border: 1px solid rgba(0,229,255,.15); color: var(--t2);
            background: rgba(0,229,255,.04); transition: all .25s ease; white-space: nowrap;
        }
        .cat-pill:hover, .cat-pill.active {
            background: rgba(0,229,255,.12); border-color: rgba(0,229,255,.45);
            color: var(--cyan); box-shadow: 0 2px 16px rgba(0,229,255,.12);
        }

        /* ══ SECTION LABEL ══ */
        .section-label {
            font-family: 'Bebas Neue', sans-serif; font-size: clamp(1.2rem,2.5vw,1.6rem);
            letter-spacing: 5px; color: var(--t1);
            display: flex; align-items: center; gap: 14px;
            margin: 0 0 .5rem; text-transform: uppercase;
        }
        .section-label::before { content: ''; width: 4px; height: 1.3rem;
            background: var(--gradct); border-radius: 2px;
            box-shadow: 0 0 12px rgba(0,229,255,.5); flex-shrink: 0; }
        .section-label::after { content: ''; flex: 1; height: 1px;
            background: linear-gradient(90deg,rgba(0,229,255,.3),rgba(124,63,255,.12),transparent); }

        .rec-subhead { font-family: 'Space Mono', monospace; font-size: .62rem;
            letter-spacing: 3px; text-transform: uppercase; color: var(--t3);
            margin-top: -.3rem; margin-bottom: 1.2rem; font-weight: 400; }

        /* ══ GRID WRAPPER ══ */
        .grid-section { padding: 0 clamp(1rem, 4vw, 3.5rem); }

        /* ══ MOVIE CARDS ══ */
        .movie-card-wrap {
            position: relative; border-radius: 10px; overflow: hidden;
            background: rgba(12,16,32,.97); border: 1px solid rgba(0,229,255,.07);
            transition: all .4s cubic-bezier(.34,1.56,.64,1); cursor: pointer;
            display: flex; flex-direction: column; height: 100%;
            box-shadow: 0 6px 24px rgba(0,0,0,.55);
        }
        .movie-card-wrap:hover {
            transform: translateY(-12px) scale(1.03);
            border-color: rgba(0,229,255,.42);
            box-shadow: 0 24px 55px rgba(0,0,0,.75),
                        0 0 0 1px rgba(0,229,255,.2),
                        0 0 50px rgba(0,229,255,.06);
        }
        .movie-card-wrap::before {
            content: ''; position: absolute; top: 0; left: 0; right: 0; height: 1px;
            background: var(--grad); opacity: 0; transition: opacity .3s; z-index: 10;
        }
        .movie-card-wrap:hover::before { opacity: .7; }

        .movie-poster-box { width: 100%; aspect-ratio: 2/3; overflow: hidden;
            background: #070A17; flex-shrink: 0; position: relative; }
        .movie-poster-box img { width: 100%; height: 100%; object-fit: cover; display: block;
            transition: transform .55s ease; }
        .movie-card-wrap:hover .movie-poster-box img { transform: scale(1.09); }
        .movie-poster-box::after { content: ''; position: absolute; bottom: 0; left: 0; right: 0;
            height: 45%; background: linear-gradient(0deg,rgba(7,10,23,.95) 0%,transparent 100%); }

        .movie-card-overlay { padding: 10px 12px 12px;
            background: linear-gradient(180deg,rgba(7,10,23,.97) 0%,rgba(4,6,15,.99) 100%);
            flex: 1; display: flex; flex-direction: column; justify-content: space-between; }
        .movie-card-title { font-family: 'DM Sans', sans-serif; font-size: clamp(.72rem,.9vw,.82rem);
            font-weight: 500; color: rgba(210,225,245,.87); line-height: 1.35; height: 2.3rem;
            overflow: hidden; display: -webkit-box; -webkit-line-clamp: 2;
            -webkit-box-orient: vertical; margin-bottom: 10px; text-align: center; }

        /* ══ BUTTONS ══ */
        .stButton > button {
            background: linear-gradient(135deg,rgba(0,229,255,.85) 0%,rgba(0,184,217,.85) 100%) !important;
            color: #03060F !important; border: none !important; border-radius: 6px !important;
            padding: 7px 12px !important; font-family: 'Space Mono',monospace !important;
            font-weight: 700 !important; font-size: clamp(.58rem,.7vw,.70rem) !important;
            letter-spacing: 2px !important; text-transform: uppercase !important;
            width: 100% !important; transition: all .3s cubic-bezier(.34,1.56,.64,1) !important;
            box-shadow: 0 4px 18px rgba(0,229,255,.26) !important;
        }
        .stButton > button:hover {
            background: linear-gradient(135deg,#00E5FF 0%,#00C9A7 100%) !important;
            transform: translateY(-2px) scale(1.03) !important;
            box-shadow: 0 8px 30px rgba(0,229,255,.5) !important;
        }
        .stButton > button:active { transform: translateY(0) scale(.97) !important; }

        /* ══ DETAIL TITLE ══ */
        .detail-title {
            font-family: 'Playfair Display', serif; font-weight: 900; font-style: italic;
            font-size: clamp(2rem, 5vw, 5rem); color: var(--t1); line-height: 1; margin-bottom: 14px;
        }
        .detail-meta-label { font-family: 'Space Mono',monospace; font-size: .58rem; font-weight: 700;
            letter-spacing: 4px; text-transform: uppercase; color: var(--cyan); margin-bottom: 5px; opacity: .8; }
        .detail-meta-value { font-family: 'DM Sans',sans-serif; font-size: .9rem;
            color: var(--t2); font-weight: 300; }
        .genre-pill { display: inline-block; background: rgba(0,229,255,.07);
            border: 1px solid rgba(0,229,255,.22); color: var(--cyan);
            padding: 4px 12px; border-radius: 3px; font-size: .65rem; font-weight: 600;
            letter-spacing: 1.5px; text-transform: uppercase; margin: 3px 4px 3px 0;
            font-family: 'Space Mono',monospace; transition: all .2s ease; }
        .genre-pill:hover { background: rgba(0,229,255,.13); border-color: rgba(0,229,255,.50); }
        .overview-text { font-family: 'DM Sans',sans-serif; font-size: clamp(.88rem,1.3vw,1rem);
            font-weight: 300; color: var(--t2); line-height: 1.90; font-style: italic; }
        .info-strip { display: flex; gap: clamp(16px,3vw,32px); margin: 16px 0 22px; flex-wrap: wrap; }
        .info-strip-item { display: flex; flex-direction: column; gap: 5px; }
        .hero-accent { width: 40px; height: 3px; background: var(--gradct); border-radius: 2px;
            margin-bottom: 14px; box-shadow: 0 0 14px rgba(0,229,255,.5); }
        .stat-badge { display: inline-flex; align-items: center; gap: 6px;
            background: rgba(255,45,91,.10); border: 1px solid rgba(255,45,91,.25); color: #FF2D5B;
            padding: 5px 14px; border-radius: 4px; font-family: 'Space Mono',monospace;
            font-size: .75rem; font-weight: 700; letter-spacing: 1px; }

        /* ══ BACKDROP ══ */
        .backdrop-hero { width: 100%; max-height: clamp(220px,35vw,500px);
            overflow: hidden; position: relative; margin-bottom: 0; }
        .backdrop-hero img { width: 100%; object-fit: cover; display: block;
            filter: brightness(.32) saturate(1.5) hue-rotate(8deg); }
        .backdrop-hero::after { content: ''; position: absolute; inset: 0;
            background: linear-gradient(180deg,transparent 10%,rgba(4,6,15,.8) 70%,#04060F 100%); }
        .backdrop-hero::before { content: ''; position: absolute; inset: 0;
            border-bottom: 1px solid rgba(0,229,255,.10); z-index: 2; pointer-events: none; }

        .poster-shadow img { border-radius: 12px !important;
            box-shadow: 0 32px 72px rgba(0,0,0,.88), 0 0 0 1px rgba(0,229,255,.09) !important; }

        /* ══ BACK BUTTON ══ */
        .back-btn .stButton > button {
            background: rgba(0,229,255,.04) !important; color: var(--t2) !important;
            border: 1px solid rgba(0,229,255,.12) !important; box-shadow: none !important;
            font-size: .68rem !important; letter-spacing: 1px !important;
            border-radius: 6px !important; font-family: 'Space Mono',monospace !important;
        }
        .back-btn .stButton > button:hover {
            background: rgba(0,229,255,.08) !important; color: var(--cyan) !important;
            transform: translateX(-4px) !important; box-shadow: none !important;
        }

        /* ══ HR ══ */
        hr { border: 0 !important; border-top: 1px solid rgba(0,229,255,.07) !important; margin: 1.8rem 0 !important; }

        /* ══ ALERTS ══ */
        .stAlert { background: rgba(0,229,255,.03) !important; border: 1px solid rgba(0,229,255,.10) !important;
            border-radius: 8px !important; color: var(--t2) !important; }

        /* ══ SCROLLBAR ══ */
        ::-webkit-scrollbar { width: 4px; }
        ::-webkit-scrollbar-thumb { background: linear-gradient(180deg,#00E5FF,#7C3FFF,#FF2D5B); border-radius: 4px; }

        /* ══ SPINNER ══ */
        .stSpinner > div { border-top-color: #00E5FF !important; }

        /* ══ PAGE REVEAL ══ */
        @keyframes revealUp {
            from { opacity: 0; transform: translateY(20px); }
            to   { opacity: 1; transform: translateY(0); }
        }
        .reveal { animation: revealUp .5s cubic-bezier(.16,1,.3,1) forwards; }

        /* ══ RESPONSIVE BREAKPOINTS ══ */
        @media (max-width: 768px) {
            .nav-center { display: none; }
            .devflix-nav { padding: 0 1rem; }
            .hero-section { padding: 1.8rem 1rem 1.4rem; }
            .controls-bar { padding: 0 1rem; }
            .cat-pills { padding: 0 1rem; gap: 6px; }
            .grid-section { padding: 0 1rem; }
            .cat-pill { font-size: .55rem; padding: 6px 12px; }
            .movie-card-wrap:hover { transform: translateY(-6px) scale(1.02); }
        }

        @media (max-width: 480px) {
            .nav-logo { font-size: 1.4rem; letter-spacing: 4px; }
            .hero-title { font-size: clamp(3rem, 16vw, 5.5rem); }
        }

        /* ══ DETAIL PAGE PADDING ══ */
        .detail-section { padding: 0 clamp(1rem, 4vw, 3.5rem); }
    </style>
    """,
    unsafe_allow_html=True,
)

# ── Session state ────────────────────────────────────────────────────
if "view" not in st.session_state:
    st.session_state.view = "home"
if "selected_tmdb_id" not in st.session_state:
    st.session_state.selected_tmdb_id = None
if "category" not in st.session_state:
    st.session_state.category = "trending"
if "grid_cols" not in st.session_state:
    st.session_state.grid_cols = 5

# ── Query params ─────────────────────────────────────────────────────
qp_view = st.query_params.get("view")
qp_id   = st.query_params.get("id")
if qp_view in ("home", "details"):
    st.session_state.view = qp_view
if qp_id:
    try:
        st.session_state.selected_tmdb_id = int(qp_id)
        st.session_state.view = "details"
    except:
        pass


def goto_home():
    st.session_state.view = "home"
    st.session_state.selected_tmdb_id = None
    st.query_params["view"] = "home"
    if "id" in st.query_params:
        del st.query_params["id"]
    st.rerun()


def goto_details(tmdb_id: int):
    st.session_state.view              = "details"
    st.session_state.selected_tmdb_id = int(tmdb_id)
    st.query_params["view"]            = "details"
    st.query_params["id"]              = str(int(tmdb_id))
    st.rerun()


@st.cache_data(ttl=60)
def api_get_json(path: str, params: Optional[dict] = None):
    try:
        r = requests.get(f"{API_BASE}{path}", params=params, timeout=25)
        if r.status_code >= 400:
            return None, f"HTTP {r.status_code}: {r.text[:300]}"
        return r.json(), None
    except Exception as e:
        return None, f"Request failed: {e}"


def poster_grid(cards, cols=5, key_prefix="grid"):
    if not cards:
        st.info("No movies to show.")
        return
    rows = (len(cards) + cols - 1) // cols
    idx  = 0
    for r in range(rows):
        colset = st.columns(cols, gap="small")
        for c in range(cols):
            if idx >= len(cards):
                break
            m = cards[idx]; idx += 1
            tmdb_id = m.get("tmdb_id")
            title   = m.get("title", "Untitled")
            poster  = m.get("poster_url")
            with colset[c]:
                st.markdown("<div class='movie-card-wrap'>", unsafe_allow_html=True)
                if poster:
                    st.markdown(
                        f"<div class='movie-poster-box'><img src='{poster}' alt='{title}' loading='lazy'/></div>",
                        unsafe_allow_html=True,
                    )
                else:
                    st.markdown(
                        "<div class='movie-poster-box' style='display:flex;align-items:center;"
                        "justify-content:center;color:rgba(0,229,255,.12);font-size:2.5rem;'>🎬</div>",
                        unsafe_allow_html=True,
                    )
                st.markdown(
                    f"<div class='movie-card-overlay'><div class='movie-card-title'>{title}</div></div>",
                    unsafe_allow_html=True,
                )
                if st.button("▶  Play", key=f"{key_prefix}_{r}_{c}_{idx}_{tmdb_id}"):
                    if tmdb_id:
                        goto_details(tmdb_id)
                st.markdown("</div>", unsafe_allow_html=True)


def to_cards_from_tfidf_items(tfidf_items):
    cards = []
    for x in tfidf_items or []:
        tmdb = x.get("tmdb") or {}
        if tmdb.get("tmdb_id"):
            cards.append({
                "tmdb_id":    tmdb["tmdb_id"],
                "title":      tmdb.get("title") or x.get("title") or "Untitled",
                "poster_url": tmdb.get("poster_url"),
            })
    return cards


def parse_tmdb_search_to_cards(data, keyword: str, limit: int = 24):
    keyword_l = keyword.strip().lower()
    if isinstance(data, dict) and "results" in data:
        raw = data.get("results") or []
        raw_items = []
        for m in raw:
            title       = (m.get("title") or "").strip()
            tmdb_id     = m.get("id")
            poster_path = m.get("poster_path")
            if not title or not tmdb_id:
                continue
            raw_items.append({
                "tmdb_id":      int(tmdb_id),
                "title":        title,
                "poster_url":   f"{TMDB_IMG}{poster_path}" if poster_path else None,
                "release_date": m.get("release_date", ""),
            })
    elif isinstance(data, list):
        raw_items = []
        for m in data:
            tmdb_id    = m.get("tmdb_id") or m.get("id")
            title      = (m.get("title") or "").strip()
            poster_url = m.get("poster_url")
            if not title or not tmdb_id:
                continue
            raw_items.append({
                "tmdb_id":      int(tmdb_id),
                "title":        title,
                "poster_url":   poster_url,
                "release_date": m.get("release_date", ""),
            })
    else:
        return [], []

    matched    = [x for x in raw_items if keyword_l in x["title"].lower()]
    final_list = matched if matched else raw_items
    suggestions = []
    for x in final_list[:10]:
        year  = (x.get("release_date") or "")[:4]
        label = f"{x['title']} ({year})" if year else x["title"]
        suggestions.append((label, x["tmdb_id"]))
    cards = [{"tmdb_id": x["tmdb_id"], "title": x["title"], "poster_url": x["poster_url"]}
             for x in final_list[:limit]]
    return suggestions, cards


# ════════════════════════════════════════════════════════════════════
#  TOP NAV  (always rendered)
# ════════════════════════════════════════════════════════════════════
category_options = {
    "trending":    "Trending",
    "popular":     "Popular",
    "top_rated":   "Top Rated",
    "now_playing": "Now Playing",
    "upcoming":    "Upcoming",
}

st.markdown(
    """
    <div class='devflix-nav'>
        <div class='nav-logo'>DEVFLIX</div>
        <div class='nav-center'>
            <span class='nav-link'>Trending</span>
            <span class='nav-link'>Movies</span>
            <span class='nav-link'>Top Rated</span>
            <span class='nav-link'>Upcoming</span>
        </div>
        <div class='nav-right'>
            <span style='font-family:Space Mono,monospace;font-size:.6rem;
            letter-spacing:2px;text-transform:uppercase;color:rgba(0,229,255,.45);'>
            // Cinema Universe</span>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)


# ════════════════════════════════════════════════════════════════════
#  HOME VIEW
# ════════════════════════════════════════════════════════════════════
if st.session_state.view == "home":

    # Hero
    st.markdown(
        "<div class='hero-section reveal'>"
        "<div class='hero-eyebrow'>// Your Personal Cinema Universe</div>"
        "<div class='hero-title'>DEV<span class='hero-accent-word'>FLIX</span></div>"
        "<div class='hero-rule'></div>"
        "<div class='hero-tagline'>Discover &nbsp;·&nbsp; Stream &nbsp;·&nbsp; Experience</div>"
        "</div>",
        unsafe_allow_html=True,
    )

    # Search + column control
    st.markdown("<div class='controls-bar'>", unsafe_allow_html=True)
    search_col, cols_col = st.columns([4, 1])
    with search_col:
        typed = st.text_input(
            "Search",
            placeholder="//  Search — Inception, Dune, Oppenheimer...",
            label_visibility="collapsed",
        )
    with cols_col:
        grid_cols = st.slider("Cols", 2, 8, st.session_state.grid_cols, label_visibility="collapsed")
        st.session_state.grid_cols = grid_cols
    st.markdown("</div>", unsafe_allow_html=True)

    # Category pills  (rendered as buttons in columns)
    st.markdown("<div class='cat-pills'>", unsafe_allow_html=True)
    cat_keys = list(category_options.keys())
    pill_cols = st.columns(len(cat_keys), gap="small")
    for i, (key, label) in enumerate(category_options.items()):
        with pill_cols[i]:
            is_active = st.session_state.category == key
            btn_label = f"{'▸ ' if is_active else ''}{label}"
            if st.button(btn_label, key=f"cat_{key}"):
                st.session_state.category = key
                st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<div class='grid-section'>", unsafe_allow_html=True)

    # ── Search mode ──
    if typed.strip():
        if len(typed.strip()) < 2:
            st.caption("Type at least 2 characters.")
        else:
            data, err = api_get_json("/tmdb/search", params={"query": typed.strip()})
            if err or data is None:
                st.error(f"Search failed: {err}")
            else:
                suggestions, cards = parse_tmdb_search_to_cards(data, typed.strip(), limit=24)
                if suggestions:
                    labels   = ["— Select a title —"] + [s[0] for s in suggestions]
                    selected = st.selectbox("Suggestions", labels, index=0, label_visibility="collapsed")
                    if selected != "— Select a title —":
                        label_to_id = {s[0]: s[1] for s in suggestions}
                        goto_details(label_to_id[selected])
                else:
                    st.info("No suggestions found.")
                st.markdown(
                    f"<div class='section-label'>Search Results</div>"
                    f"<div class='rec-subhead'>{len(cards)} titles for &ldquo;{typed}&rdquo;</div>",
                    unsafe_allow_html=True,
                )
                poster_grid(cards, cols=grid_cols, key_prefix="search")
        st.markdown("</div>", unsafe_allow_html=True)
        st.stop()

    # ── Browse mode ──
    cat_label = category_options[st.session_state.category]
    st.markdown(
        f"<div class='section-label'>{cat_label}</div>"
        f"<div class='rec-subhead'>// {cat_label} on TMDB</div>",
        unsafe_allow_html=True,
    )

    with st.spinner("Loading…"):
        home_cards, err = api_get_json("/home", params={"category": st.session_state.category, "limit": 24})

    if err or not home_cards:
        st.error(f"Feed failed: {err or 'Unknown error'}")
        st.markdown("</div>", unsafe_allow_html=True)
        st.stop()

    poster_grid(home_cards, cols=grid_cols, key_prefix="home_feed")
    st.markdown("</div>", unsafe_allow_html=True)


# ════════════════════════════════════════════════════════════════════
#  DETAILS VIEW
# ════════════════════════════════════════════════════════════════════
elif st.session_state.view == "details":
    tmdb_id = st.session_state.selected_tmdb_id
    if not tmdb_id:
        st.warning("No movie selected.")
        if st.button("← Back to Home"):
            goto_home()
        st.stop()

    with st.spinner("Loading…"):
        data, err = api_get_json(f"/movie/id/{tmdb_id}")
    if err or not data:
        st.error(f"Could not load details: {err or 'Unknown error'}")
        st.stop()

    # Backdrop (full-width, no padding)
    if data.get("backdrop_url"):
        st.markdown(
            f"<div class='backdrop-hero'><img src='{data['backdrop_url']}'/></div>",
            unsafe_allow_html=True,
        )

    st.markdown("<div class='detail-section'>", unsafe_allow_html=True)

    # Back button
    st.markdown("<div class='back-btn' style='margin:1rem 0;'>", unsafe_allow_html=True)
    col_back, _ = st.columns([1, 8])
    with col_back:
        if st.button("← Back"):
            goto_home()
    st.markdown("</div>", unsafe_allow_html=True)

    # Poster + Info
    poster_col, details_col = st.columns([1, 2.8], gap="large")

    with poster_col:
        st.markdown("<div class='poster-shadow'>", unsafe_allow_html=True)
        if data.get("poster_url"):
            st.image(data["poster_url"], use_column_width=True)
        else:
            st.markdown(
                "<div style='background:rgba(0,229,255,.03);border:1px solid rgba(0,229,255,.10);"
                "aspect-ratio:2/3;display:flex;align-items:center;justify-content:center;"
                "color:rgba(0,229,255,.15);font-size:3rem;border-radius:12px;'>🎬</div>",
                unsafe_allow_html=True,
            )
        st.markdown("</div>", unsafe_allow_html=True)

    with details_col:
        release    = data.get("release_date") or "—"
        vote_avg   = data.get("vote_average")
        genres     = [g["name"] for g in data.get("genres", [])]
        genre_html = "".join(f"<span class='genre-pill'>{g}</span>" for g in genres) if genres else \
                     "<span style='color:rgba(255,255,255,.18)'>No genre info</span>"
        rating_html = f"<span class='stat-badge'>★ {vote_avg:.1f}</span>" if vote_avg else ""

        st.markdown(
            f"<div class='hero-accent'></div>"
            f"<div class='detail-title'>{data.get('title','')}</div>"
            f"{rating_html}",
            unsafe_allow_html=True,
        )
        st.markdown(
            f"""<div class='info-strip'>
                <div class='info-strip-item'>
                    <div class='detail-meta-label'>Release Date</div>
                    <div class='detail-meta-value'>{release}</div>
                </div>
                <div class='info-strip-item'>
                    <div class='detail-meta-label'>Genres</div>
                    <div style='margin-top:3px'>{genre_html}</div>
                </div>
            </div>""",
            unsafe_allow_html=True,
        )
        st.markdown("<div class='detail-meta-label' style='margin-bottom:8px;'>Synopsis</div>", unsafe_allow_html=True)
        overview = data.get("overview") or "No overview available."
        st.markdown(f"<div class='overview-text'>{overview}</div>", unsafe_allow_html=True)

    st.markdown("<hr style='margin:2rem 0'>", unsafe_allow_html=True)

    # Recommendations
    st.markdown("<div class='section-label'>Recommendations</div>", unsafe_allow_html=True)

    title = (data.get("title") or "").strip()
    if title:
        with st.spinner("Finding similar movies…"):
            bundle, err2 = api_get_json("/movie/search", params={"query": title, "tfidf_top_n": 12, "genre_limit": 12})

        if not err2 and bundle:
            tfidf_cards = to_cards_from_tfidf_items(bundle.get("tfidf_recommendations"))
            if tfidf_cards:
                st.markdown("<div class='rec-subhead'>// Plot Similarity · TF-IDF Engine</div>", unsafe_allow_html=True)
                poster_grid(tfidf_cards, cols=st.session_state.grid_cols, key_prefix="d_tfidf")

            genre_cards = bundle.get("genre_recommendations", [])
            if genre_cards:
                st.markdown("<hr>", unsafe_allow_html=True)
                st.markdown("<div class='section-label'>More Like This</div>", unsafe_allow_html=True)
                st.markdown("<div class='rec-subhead'>// Genre &amp; Popularity Match</div>", unsafe_allow_html=True)
                poster_grid(genre_cards, cols=st.session_state.grid_cols, key_prefix="d_genre")
        else:
            genre_only, err3 = api_get_json("/recommend/genre", params={"tmdb_id": tmdb_id, "limit": 18})
            if not err3 and genre_only:
                poster_grid(genre_only, cols=st.session_state.grid_cols, key_prefix="d_fallback")
            else:
                st.warning("No recommendations available right now.")
    else:
        st.warning("No title available to compute recommendations.")

    st.markdown("</div>", unsafe_allow_html=True)

    # Footer
    st.markdown(
        "<div style='text-align:center;padding:2rem 0 1rem;"
        "font-family:Space Mono,monospace;font-size:.58rem;letter-spacing:2px;"
        "text-transform:uppercase;color:rgba(0,229,255,.18);'>"
        "// DEVFLIX · POWERED BY TMDB API · CINEMA UNIVERSE</div>",
        unsafe_allow_html=True,
    )