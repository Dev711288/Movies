import requests
import streamlit as st
from typing import Optional

API_BASE = "https://movie-rec-466x.onrender.com" or "http://127.0.0.1:8000"
TMDB_IMG = "https://image.tmdb.org/t/p/w500"
NO_POSTER_URL = "https://dummyimage.com/500x750/0f172a/cbd5e1.png&text=No+Poster"

st.set_page_config(page_title="Devflix", page_icon="🎬", layout="wide")

st.markdown(
    """
    <link href="https://fonts.googleapis.com/css2?family=Bebas+Neue&family=DM+Sans:ital,opsz,wght@0,9..40,300;0,9..40,400;0,9..40,600;1,9..40,300&display=swap" rel="stylesheet">

    <style>
        html, body, [data-testid="stAppViewContainer"] {
            background: radial-gradient(circle at 20% 10%, #2B0C12 0%, #13070A 35%, #090909 100%) !important;
        }

        [data-testid="stAppViewContainer"] > .main {
            background: transparent;
        }

        .block-container {
            padding: 4.2rem 2.5rem 4rem !important;
            max-width: 1600px !important;
            font-family: 'DM Sans', sans-serif;
        }

        [data-testid="stAppViewContainer"]::before {
            content: '';
            position: fixed;
            inset: 0;
            background-image: url("data:image/svg+xml,%3Csvg viewBox='0 0 256 256' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='noise'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.9' numOctaves='4' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23noise)' opacity='0.04'/%3E%3C/svg%3E");
            pointer-events: none;
            z-index: 0;
            opacity: 0.18;
        }

        .devflix-title {
            font-family: 'Bebas Neue', sans-serif;
            font-size: clamp(3rem, 7vw, 6rem);
            letter-spacing: 8px;
            color: #F0F4FF;
            line-height: 1;
            margin: 0;
        }

        .devflix-title span {
            color: #E0B04A;
        }

        .devflix-tagline {
            font-family: 'DM Sans', sans-serif;
            font-size: 0.9rem;
            font-weight: 300;
            color: #5A6E8A;
            letter-spacing: 4px;
            text-transform: uppercase;
            margin-top: 4px;
        }

        .stSelectbox > div > div {
            background: rgba(24,24,24,0.95) !important;
            border: 1px solid rgba(255,255,255,0.12) !important;
            border-radius: 6px !important;
            color: #F4F4F4 !important;
        }

        .section-label {
            font-family: 'Bebas Neue', sans-serif;
            font-size: 1.6rem;
            letter-spacing: 4px;
            color: #FFFFFF;
            display: flex;
            align-items: center;
            gap: 10px;
            margin: 1.5rem 0 1rem;
        }

        .section-label::after {
            content: '';
            flex: 1;
            height: 1px;
            background: linear-gradient(90deg, rgba(229, 9, 20, 0.95), rgba(229, 9, 20, 0.35), transparent);
            margin-left: 12px;
        }

        .movie-card-wrap {
            position: relative;
            border-radius: 6px;
            overflow: hidden;
            background: #141414;
            border: 1px solid rgba(255,255,255,0.08);
            transition: transform 0.28s ease, box-shadow 0.28s ease, border-color 0.28s ease;
            cursor: pointer;
            display: flex;
            flex-direction: column;
            height: 100%;
            box-shadow: 0 8px 24px rgba(0, 0, 0, 0.4);
        }

        .movie-card-wrap:hover {
            transform: translateY(-8px) scale(1.05);
            border-color: rgba(229, 9, 20, 0.55);
            box-shadow:
                0 18px 34px rgba(0, 0, 0, 0.62),
                0 0 0 1px rgba(229, 9, 20, 0.25);
        }

        .movie-poster-box {
            width: 100%;
            aspect-ratio: 2 / 3;
            overflow: hidden;
            background: #0D0D0D;
            flex-shrink: 0;
        }

        .movie-poster-box img {
            width: 100%;
            height: 100%;
            object-fit: cover;
            display: block;
            transition: transform 0.4s ease;
        }

        .movie-card-wrap:hover .movie-poster-box img {
            transform: scale(1.06);
        }

        .movie-card-overlay {
            padding: 12px 14px 14px;
            background: linear-gradient(180deg, rgba(20, 20, 20, 0.1) 0%, rgba(20, 20, 20, 0.95) 80%);
            flex: 1;
            display: flex;
            flex-direction: column;
            justify-content: space-between;
        }

        .movie-card-title {
            font-family: 'DM Sans', sans-serif;
            font-size: 0.88rem;
            font-weight: 600;
            color: #F5F5F5;
            line-height: 1.35;
            height: 2.4rem;
            overflow: hidden;
            display: -webkit-box;
            -webkit-line-clamp: 2;
            -webkit-box-orient: vertical;
            margin-bottom: 10px;
            text-align: center;
        }

        .play-link {
            display: inline-block;
            width: 100%;
            text-align: center;
            text-decoration: none !important;
            background: #E50914;
            color: #FFFFFF !important;
            border: 1px solid rgba(229, 9, 20, 0.9);
            border-radius: 4px;
            padding: 8px 14px;
            font-family: 'DM Sans', sans-serif;
            font-weight: 700;
            font-size: 0.78rem;
            letter-spacing: 1.5px;
            text-transform: uppercase;
            transition: all 0.25s ease;
            box-shadow: 0 6px 16px rgba(229, 9, 20, 0.35);
        }

        .play-link:hover {
            background: #FF1F2D;
            transform: translateY(-2px);
            box-shadow: 0 10px 24px rgba(229, 9, 20, 0.45);
        }

        .play-link-disabled {
            display: inline-block;
            width: 100%;
            text-align: center;
            background: #2A2A2A;
            color: #9A9A9A;
            border: 1px solid rgba(255,255,255,0.1);
            border-radius: 4px;
            padding: 8px 14px;
            font-family: 'DM Sans', sans-serif;
            font-weight: 700;
            font-size: 0.78rem;
            letter-spacing: 1.5px;
            text-transform: uppercase;
        }

        .stButton > button {
            background: #E50914 !important;
            color: #FFFFFF !important;
            border: 1px solid rgba(229, 9, 20, 0.9) !important;
            border-radius: 4px !important;
            padding: 8px 14px !important;
            font-family: 'DM Sans', sans-serif !important;
            font-weight: 700 !important;
            font-size: 0.78rem !important;
            letter-spacing: 1.5px !important;
            text-transform: uppercase !important;
            width: 100% !important;
            transition: all 0.25s ease !important;
            box-shadow: 0 6px 16px rgba(229, 9, 20, 0.35) !important;
        }

        .stButton > button:hover {
            background: #FF1F2D !important;
            transform: translateY(-2px) !important;
            box-shadow: 0 10px 24px rgba(229, 9, 20, 0.45) !important;
        }

        .stButton > button:active {
            transform: translateY(0) !important;
        }

        hr {
            border: 0 !important;
            border-top: 1px solid rgba(255,255,255,0.12) !important;
            margin: 1.5rem 0 !important;
        }

        .stSlider [data-baseweb="slider"] div[role="slider"] {
            background-color: #E50914 !important;
        }

        .detail-title {
            font-family: 'Bebas Neue', sans-serif;
            font-size: clamp(2.5rem, 5vw, 4.5rem);
            letter-spacing: 4px;
            color: #F0F4FF;
            line-height: 1.05;
            margin-bottom: 12px;
        }

        .detail-meta-label {
            font-family: 'DM Sans', sans-serif;
            font-size: 0.72rem;
            font-weight: 600;
            letter-spacing: 3px;
            text-transform: uppercase;
            color: #E50914;
            margin-bottom: 6px;
        }

        .detail-meta-value {
            font-family: 'DM Sans', sans-serif;
            font-size: 0.95rem;
            color: #CFCFCF;
            font-weight: 300;
        }

        .genre-pill {
            display: inline-block;
            background: rgba(229,9,20,0.14);
            border: 1px solid rgba(229,9,20,0.35);
            color: #FF8A92;
            padding: 4px 12px;
            border-radius: 20px;
            font-size: 0.78rem;
            font-weight: 600;
            letter-spacing: 0.5px;
            margin: 3px 4px 3px 0;
        }

        .overview-text {
            font-family: 'DM Sans', sans-serif;
            font-size: 1rem;
            font-weight: 300;
            color: #D1D1D1;
            line-height: 1.8;
        }

        .stAlert {
            background: rgba(35,35,35,0.92) !important;
            border: 1px solid rgba(255,255,255,0.1) !important;
            border-radius: 12px !important;
            color: #DDDDDD !important;
        }

        ::-webkit-scrollbar { width: 6px; }
        ::-webkit-scrollbar-track { background: #090909; }
        ::-webkit-scrollbar-thumb {
            background: linear-gradient(180deg, #E50914, #8C030B);
            border-radius: 4px;
        }

        .stSpinner > div {
            border-top-color: #E50914 !important;
        }

        .back-btn .stButton > button {
            background: rgba(28,28,28,0.95) !important;
            color: #F0F0F0 !important;
            border: 1px solid rgba(255,255,255,0.14) !important;
            box-shadow: none !important;
            font-size: 0.8rem !important;
            letter-spacing: 1px !important;
        }
        .back-btn .stButton > button:hover {
            background: rgba(40,40,40,0.95) !important;
            color: #FFFFFF !important;
            transform: none !important;
            box-shadow: none !important;
        }

        .poster-shadow img {
            border-radius: 16px !important;
            box-shadow: 0 32px 64px rgba(0,0,0,0.8) !important;
        }

        .hero-accent {
            width: 60px;
            height: 4px;
            background: linear-gradient(90deg, #E50914, #8C030B);
            border-radius: 2px;
            margin-bottom: 10px;
        }

        .info-strip {
            display: flex;
            gap: 24px;
            margin: 14px 0 20px;
            flex-wrap: wrap;
        }
        .info-strip-item {
            display: flex;
            flex-direction: column;
            gap: 4px;
        }

        .rec-subhead {
            font-family: 'DM Sans', sans-serif;
            font-size: 0.78rem;
            letter-spacing: 2px;
            text-transform: uppercase;
            color: #9F9F9F;
            margin-top: -0.5rem;
            margin-bottom: 1rem;
        }

        .top-controls {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin: 1.2rem 0 1.6rem;
            gap: 1rem;
            flex-wrap: wrap;
        }

        .hero-panel {
            position: relative;
            padding: 2.3rem 2.4rem;
            border-radius: 10px;
            overflow: hidden;
            margin: 0.7rem 0 2rem;
            background:
                linear-gradient(90deg, rgba(0,0,0,0.86) 20%, rgba(0,0,0,0.58) 54%, rgba(0,0,0,0.15) 100%),
                url('https://images.unsplash.com/photo-1478720568477-152d9b164e26?auto=format&fit=crop&w=1800&q=80');
            background-size: cover;
            background-position: center;
            border: 1px solid rgba(255,255,255,0.12);
            box-shadow: 0 30px 60px rgba(0,0,0,0.55);
        }

        .hero-kicker {
            font-family: 'DM Sans', sans-serif;
            font-size: 0.75rem;
            letter-spacing: 4px;
            text-transform: uppercase;
            color: #E50914;
            margin-bottom: 8px;
        }

        .hero-heading {
            font-family: 'Bebas Neue', sans-serif;
            font-size: clamp(2.4rem, 6vw, 5.5rem);
            letter-spacing: 5px;
            color: #FFFFFF;
            line-height: 0.95;
            margin: 0;
        }

        .hero-copy {
            margin-top: 14px;
            max-width: 560px;
            font-family: 'DM Sans', sans-serif;
            color: #D8D8D8;
            font-size: 0.98rem;
            line-height: 1.7;
            font-weight: 300;
        }

    </style>
    """,
    unsafe_allow_html=True,
)

if "view" not in st.session_state:
    st.session_state.view = "home"
if "selected_tmdb_id" not in st.session_state:
    st.session_state.selected_tmdb_id = None

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


@st.cache_data(ttl=30)
def api_get_json(path: str, params: Optional[dict] = None):
    try:
        r = requests.get(f"{API_BASE}{path}", params=params, timeout=25)
        if r.status_code >= 400:
            return None, f"HTTP {r.status_code}: {r.text[:300]}"
        return r.json(), None
    except Exception as e:
        return None, f"Request failed: {e}"


def poster_grid(cards, cols=6, key_prefix="grid"):
    """Render a uniform grid of movie cards — every card identical in height."""
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

                poster_src = poster or NO_POSTER_URL
                st.markdown(
                    f"<div class='movie-poster-box'>"
                    f"<img src='{poster_src}' alt='{title}' loading='lazy' onerror=\"this.onerror=null;this.src='{NO_POSTER_URL}';\" />"
                    f"</div>",
                    unsafe_allow_html=True,
                )

                st.markdown(
                    f"<div class='movie-card-overlay'>"
                    f"<div class='movie-card-title'>{title}</div>"
                    f"</div>",
                    unsafe_allow_html=True,
                )

                if tmdb_id:
                    play_key = f"play_{key_prefix}_{int(tmdb_id)}_{r}_{c}_{idx}"
                    if st.button("▶ Play", key=play_key):
                        goto_details(int(tmdb_id))
                else:
                    st.markdown(
                        "<span class='play-link-disabled'>Unavailable</span>",
                        unsafe_allow_html=True,
                    )

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

    cards = [
        {"tmdb_id": x["tmdb_id"], "title": x["title"], "poster_url": x["poster_url"]}
        for x in final_list[:limit]
    ]
    return suggestions, cards


category_options = {
    "trending":    "🔥 Trending Now",
    "popular":     "⭐ Most Popular",
    "top_rated":   "🏆 Top Rated",
    "now_playing": "🎬 Now Playing",
    "upcoming":    "📅 Upcoming",
}

top_left, top_right = st.columns([3, 1], gap="large")
with top_left:
    selected_category = st.selectbox(
        "Browse category",
        options=list(category_options.keys()),
        format_func=lambda x: category_options[x],
        index=0,
    )
with top_right:
    grid_cols = st.selectbox("Cards per row", options=[4, 5, 6, 7, 8], index=2)


if st.session_state.view == "home":
    st.markdown(
        "<div class='hero-panel'>"
        "<div class='hero-kicker'>Now Streaming</div>"
        "<h1 class='hero-heading'>DEV<span style='color:#E50914'>FLIX</span></h1>"
        "<div class='hero-copy'>Dive into a dark cinematic experience with trending blockbusters, iconic classics, and handpicked recommendations crafted for your next binge session.</div>"
        "</div>",
        unsafe_allow_html=True,
    )

    st.markdown("<div class='top-controls'></div>", unsafe_allow_html=True)

    cat_label = category_options[selected_category].replace("  ", " ")
    st.markdown(
        f"<div class='section-label'>{cat_label}</div>",
        unsafe_allow_html=True,
    )

    with st.spinner("Loading…"):
        home_cards, err = api_get_json("/home", params={"category": selected_category, "limit": 24})

    if err or not home_cards:
        st.error(f"Feed failed: {err or 'Unknown error'}")
        st.stop()

    poster_grid(home_cards, cols=grid_cols, key_prefix="home_feed")


elif st.session_state.view == "details":
    tmdb_id = st.session_state.selected_tmdb_id
    if not tmdb_id:
        st.warning("No movie selected.")
        if st.button("← Back to Home"):
            goto_home()
        st.stop()

    st.markdown("<div class='back-btn'>", unsafe_allow_html=True)
    col_back, _ = st.columns([1, 9])
    with col_back:
        if st.button("← Back"):
            goto_home()
    st.markdown("</div>", unsafe_allow_html=True)

    with st.spinner("Loading movie details…"):
        data, err = api_get_json(f"/movie/id/{tmdb_id}")

    if err or not data:
        st.error(f"Could not load details: {err or 'Unknown error'}")
        st.stop()

    if data.get("backdrop_url"):
        st.markdown(
            f"""<div style="
                width:100%;max-height:420px;overflow:hidden;border-radius:20px;
                margin-bottom:2rem;position:relative;
            ">
                <img src="{data['backdrop_url']}" style="
                    width:100%;object-fit:cover;border-radius:20px;
                    filter:brightness(0.5) saturate(1.2);
                " />
                <div style="
                    position:absolute;inset:0;
                    background:linear-gradient(180deg,transparent 30%,#080C14 100%);
                    border-radius:20px;
                "></div>
            </div>""",
            unsafe_allow_html=True,
        )

    poster_col, details_col = st.columns([1, 2.8], gap="large")

    with poster_col:
        st.markdown("<div class='poster-shadow'>", unsafe_allow_html=True)
        detail_poster = data.get("poster_url") or NO_POSTER_URL
        st.image(detail_poster, use_column_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

    with details_col:
        st.markdown(
            f"<div class='hero-accent'></div>"
            f"<div class='detail-title'>{data.get('title', '')}</div>",
            unsafe_allow_html=True,
        )

        release    = data.get("release_date") or "—"
        genres     = [g["name"] for g in data.get("genres", [])]
        genre_html = "".join(f"<span class='genre-pill'>{g}</span>" for g in genres) if genres else "<span style='color:#3E5068'>No genre info</span>"

        st.markdown(
            f"""<div class='info-strip'>
                <div class='info-strip-item'>
                    <div class='detail-meta-label'>Release Date</div>
                    <div class='detail-meta-value'>{release}</div>
                </div>
                <div class='info-strip-item'>
                    <div class='detail-meta-label'>Genres</div>
                    <div>{genre_html}</div>
                </div>
            </div>""",
            unsafe_allow_html=True,
        )

        st.markdown(
            "<div class='detail-meta-label' style='margin-bottom:8px;'>Synopsis</div>",
            unsafe_allow_html=True,
        )
        overview = data.get("overview") or "No overview available."
        st.markdown(f"<div class='overview-text'>{overview}</div>", unsafe_allow_html=True)

    st.markdown("<hr style='margin:2.5rem 0'>", unsafe_allow_html=True)

    st.markdown("<div class='section-label'>Recommendations</div>", unsafe_allow_html=True)

    title = (data.get("title") or "").strip()
    if title:
        with st.spinner("Finding similar movies…"):
            bundle, err2 = api_get_json(
                "/movie/search",
                params={"query": title, "tfidf_top_n": 12, "genre_limit": 12},
            )

        if not err2 and bundle:
            tfidf_cards = to_cards_from_tfidf_items(bundle.get("tfidf_recommendations"))
            if tfidf_cards:
                st.markdown(
                    "<div style='font-family:DM Sans,sans-serif;font-size:0.78rem;"
                    "letter-spacing:3px;text-transform:uppercase;color:#3E5068;"
                    "margin-bottom:1rem;'>Plot Similarity · TF-IDF</div>",
                    unsafe_allow_html=True,
                )
                poster_grid(tfidf_cards, cols=grid_cols, key_prefix="details_tfidf")

            genre_cards = bundle.get("genre_recommendations", [])
            if genre_cards:
                st.markdown("<hr>", unsafe_allow_html=True)
                st.markdown("<div class='section-label'>More Like This</div>", unsafe_allow_html=True)
                st.markdown(
                    "<div style='font-family:DM Sans,sans-serif;font-size:0.78rem;"
                    "letter-spacing:3px;text-transform:uppercase;color:#3E5068;"
                    "margin-bottom:1rem;'>Genre &amp; Popularity Match</div>",
                    unsafe_allow_html=True,
                )
                poster_grid(genre_cards, cols=grid_cols, key_prefix="details_genre")
        else:
            st.info("Falling back to genre recommendations…")
            genre_only, err3 = api_get_json("/recommend/genre", params={"tmdb_id": tmdb_id, "limit": 18})
            if not err3 and genre_only:
                poster_grid(genre_only, cols=grid_cols, key_prefix="details_genre_fallback")
            else:
                st.warning("No recommendations available right now.")
    else:
        st.warning("No title available to compute recommendations.")