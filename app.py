import requests
import streamlit as st

API_BASE = "https://movie-rec-466x.onrender.com" or "http://127.0.0.1:8000"
TMDB_IMG = "https://image.tmdb.org/t/p/w500"

st.set_page_config(page_title="Devflix", page_icon="🎬", layout="wide")

st.markdown(
"""
    <style>
        .block-container {
            padding-top: 1rem;
            padding-bottom: 2rem;
            max-width: 1400px;
            font-family: 'Segoe UI', sans-serif;
        }

        body {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        }

        .card {
            border-radius: 16px;
            padding: 16px;
            background: linear-gradient(145deg, #1a2a4a, #162340);
            box-shadow: 
                0 8px 32px rgba(0,0,0,0.4),
                inset 0 1px 0 rgba(255,255,255,0.1);
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
            text-align: center;
            border: 1px solid rgba(255,255,255,0.1);
        }
        .card:hover {
            transform: translateY(-8px) scale(1.02);
            box-shadow: 
                0 20px 40px rgba(0,0,0,0.6),
                inset 0 1px 0 rgba(255,255,255,0.2);
            border-color: rgba(255,255,255,0.2);
        }

        .movie-title {
            font-size: 1rem;
            line-height: 1.3rem;
            height: 2.6rem;
            overflow: hidden;
            font-weight: 700;
            color: #ffd700;  /* Gold accent color */
            margin-top: 12px;
            text-shadow: 0 2px 4px rgba(0,0,0,0.5);
            letter-spacing: 0.5px;
        }

        .small-muted {
            color: #93c5fd;   /* Soft blue text */
            font-size: 0.85rem;
            font-weight: 500;
        }

        .stButton>button {
            background: linear-gradient(135deg, #667eea, #764ba2);
            color: white;
            border: none;
            border-radius: 12px;
            padding: 10px 20px;
            font-weight: 600;
            width: 100%;
            margin-top: 12px;
            transition: all 0.3s ease;
            box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4);
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }
        .stButton>button:hover {
            background: linear-gradient(135deg, #5a67d8, #6b46c1);
            transform: translateY(-2px);
            box-shadow: 0 8px 25px rgba(102, 126, 234, 0.6);
        }

        h1, h2, h3, h4 {
            color: #ffffff;
            text-shadow: 0 2px 4px rgba(0,0,0,0.3);
            font-weight: 700;
        }

        hr {
            border: 0;
            border-top: 1px solid rgba(255,255,255,0.2);
            margin: 2rem 0;
            background: linear-gradient(90deg, transparent, rgba(255,255,255,0.2), transparent);
        }

        img {
            border-radius: 12px;
            box-shadow: 0 8px 25px rgba(0,0,0,0.5);
            transition: transform 0.3s ease;
        }
        img:hover {
            transform: scale(1.05);
        }

        .css-1d391kg {
            background: linear-gradient(180deg, #1a2a4a, #162340) !important;
            color: #ffffff !important;
            border-right: 1px solid rgba(255,255,255,0.1);
        }

        .css-1lsmgbg h2 {
            color: #ffd700 !important;
            font-size: 1.2rem;
            margin-bottom: 1rem;
        }

        .css-1p6f50i, .css-1avcm0n {
            color: #ffffff !important;
        }

        .stTextInput > div > div > input {
            background-color: rgba(255,255,255,0.1) !important;
            border: 1px solid rgba(255,255,255,0.2) !important;
            border-radius: 12px !important;
            color: #ffffff !important;
            padding: 12px 16px !important;
            font-size: 1rem !important;
            transition: all 0.3s ease !important;
        }
        .stTextInput > div > div > input:focus {
            border-color: #667eea !important;
            box-shadow: 0 0 0 2px rgba(102, 126, 234, 0.2) !important;
            background-color: rgba(255,255,255,0.15) !important;
        }

        .stSelectbox > div > div > select {
            background-color: rgba(255,255,255,0.1) !important;
            border: 1px solid rgba(255,255,255,0.2) !important;
            border-radius: 12px !important;
            color: #ffffff !important;
            padding: 8px 12px !important;
        }
        .stSelectbox > div > div > select:focus {
            border-color: #667eea !important;
            box-shadow: 0 0 0 2px rgba(102, 126, 234, 0.2) !important;
        }

        .stSlider > div > div > div > div {
            background-color: rgba(255,255,255,0.2) !important;
        }
        .stSlider > div > div > div > div > div {
            background-color: #667eea !important;
        }

        .stAlert {
            border-radius: 12px;
            border: 1px solid rgba(255,255,255,0.2);
            background: rgba(255,255,255,0.05);
            backdrop-filter: blur(10px);
        }
        .stAlert h4 {
            color: #ffffff !important;
        }

        [data-testid="column"] {
            transition: transform 0.3s ease, box-shadow 0.3s ease;
        }
        [data-testid="column"]:hover {
            transform: translateY(-4px);
            box-shadow: 0 8px 25px rgba(0,0,0,0.3);
        }

        .stSpinner > div {
            border-top-color: #667eea !important;
            border-right-color: #764ba2 !important;
        }

        ::-webkit-scrollbar {
            width: 10px;
        }
        ::-webkit-scrollbar-track {
            background: rgba(255,255,255,0.1);
        }
        ::-webkit-scrollbar-thumb {
            background: linear-gradient(180deg, #667eea, #764ba2);
            border-radius: 5px;
        }
        ::-webkit-scrollbar-thumb:hover {
            background: linear-gradient(180deg, #5a67d8, #6b46c1);
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
qp_id = st.query_params.get("id")
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
    st.session_state.view = "details"
    st.session_state.selected_tmdb_id = int(tmdb_id)
    st.query_params["view"] = "details"
    st.query_params["id"] = str(int(tmdb_id))
    st.rerun()

@st.cache_data(ttl=30)
def api_get_json(path: str, params: dict | None = None):
    try:
        r = requests.get(f"{API_BASE}{path}", params=params, timeout=25)
        if r.status_code >= 400:
            return None, f"HTTP {r.status_code}: {r.text[:300]}"
        return r.json(), None
    except Exception as e:
        return None, f"Request failed: {e}"


def poster_grid(cards, cols=6, key_prefix="grid"):
    if not cards:
        st.info("No movies to show.")
        return

    rows = (len(cards) + cols - 1) // cols
    idx = 0
    for r in range(rows):
        colset = st.columns(cols)
        for c in range(cols):
            if idx >= len(cards):
                break
            m = cards[idx]
            idx += 1

            tmdb_id = m.get("tmdb_id")
            title = m.get("title", "Untitled")
            poster = m.get("poster_url")

            with colset[c]:
                if poster:
                    st.image(poster, use_column_width=True)
                else:
                    st.write("🖼️ No poster")

                if st.button("Watch Now", key=f"{key_prefix}_{r}_{c}_{idx}_{tmdb_id}"):
                    if tmdb_id:
                        goto_details(tmdb_id)

                st.markdown(
                    f"<div class='movie-title' style='text-align: center;'>{title}</div>", unsafe_allow_html=True
                )


def to_cards_from_tfidf_items(tfidf_items):
    cards = []
    for x in tfidf_items or []:
        tmdb = x.get("tmdb") or {}
        if tmdb.get("tmdb_id"):
            cards.append(
                {
                    "tmdb_id": tmdb["tmdb_id"],
                    "title": tmdb.get("title") or x.get("title") or "Untitled",
                    "poster_url": tmdb.get("poster_url"),
                }
            )
    return cards

def parse_tmdb_search_to_cards(data, keyword: str, limit: int = 24):
    """
    Returns:
      suggestions: list[(label, tmdb_id)]
      cards: list[{tmdb_id,title,poster_url}]
    """
    keyword_l = keyword.strip().lower()

    if isinstance(data, dict) and "results" in data:
        raw = data.get("results") or []
        raw_items = []
        for m in raw:
            title = (m.get("title") or "").strip()
            tmdb_id = m.get("id")
            poster_path = m.get("poster_path")
            if not title or not tmdb_id:
                continue
            raw_items.append(
                {
                    "tmdb_id": int(tmdb_id),
                    "title": title,
                    "poster_url": f"{TMDB_IMG}{poster_path}" if poster_path else None,
                    "release_date": m.get("release_date", ""),
                }
            )

    elif isinstance(data, list):
        raw_items = []
        for m in data:
            tmdb_id = m.get("tmdb_id") or m.get("id")
            title = (m.get("title") or "").strip()
            poster_url = m.get("poster_url")
            if not title or not tmdb_id:
                continue
            raw_items.append(
                {
                    "tmdb_id": int(tmdb_id),
                    "title": title,
                    "poster_url": poster_url,
                    "release_date": m.get("release_date", ""),
                }
            )
    else:
        return [], []

    matched = [x for x in raw_items if keyword_l in x["title"].lower()]

    final_list = matched if matched else raw_items

    suggestions = []
    for x in final_list[:10]:
        year = (x.get("release_date") or "")[:4]
        label = f"{x['title']} ({year})" if year else x["title"]
        suggestions.append((label, x["tmdb_id"]))

    cards = [
        {"tmdb_id": x["tmdb_id"], "title": x["title"], "poster_url": x["poster_url"]}
        for x in final_list[:limit]
    ]
    return suggestions, cards

with st.sidebar:
    st.markdown("## 🎬 Menu")
    if st.button("🏠 Home"):
        goto_home()

    st.markdown("---")
    st.markdown("### 🏠 Home Feed (only home)")
    
    category_options = {
        "trending": "🔥 Trending",
        "popular": "⭐ Popular", 
        "top_rated": "🏆 Top Rated",
        "now_playing": "🎬 Now Playing",
        "upcoming": "📅 Upcoming"
    }
    
    selected_category = st.selectbox(
        "Category",
        options=list(category_options.keys()),
        format_func=lambda x: category_options[x],
        index=0,
    )
    
    grid_cols = st.slider(
        "Grid columns", 
        min_value=3, 
        max_value=8, 
        value=6,
        help="Adjust the number of movie cards per row"
    )
    
    st.divider()
    st.markdown("### 🎯 Quick Actions")
    if st.button("🔄 Refresh Feed"):
        st.rerun()
    
    st.markdown(
        "<div style='font-size: 0.8rem; color: #93c5fd; margin-top: 10px;'>"
        "Tip: Use the search above to find specific movies!"
        "</div>",
        unsafe_allow_html=True
    )

st.title("🎬 Devflix Movie's")
st.markdown(
    "<div class='small-muted'>Exploring the world of movies with Devflix</div>",
    unsafe_allow_html=True,
)

st.markdown(
    """
    <div style="
        background: linear-gradient(90deg, rgba(255,255,255,0.1), rgba(255,255,255,0.05), rgba(255,255,255,0.1));
        border-radius: 12px;
        padding: 10px;
        margin: 10px 0;
        text-align: center;
        animation: shimmer 3s infinite;
        border: 1px solid rgba(255,255,255,0.1);
    ">
        <span style="color: #93c5fd; font-weight: 600;">✨ Discover your next favorite movie! ✨</span>
    </div>
    <style>
    @keyframes shimmer {
        0% { background-position: -200px 0; }
        100% { background-position: 200px 0; }
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.divider()

if st.session_state.view == "home":
    typed = st.text_input(
        "Search by movie title (keyword)", placeholder="Type: avenger, batman, love..."
    )

    st.divider()

    if typed.strip():
        if len(typed.strip()) < 2:
            st.caption("Type at least 2 characters for suggestions.")
        else:
            data, err = api_get_json("/tmdb/search", params={"query": typed.strip()})

            if err or data is None:
                st.error(f"Search failed: {err}")
            else:
                suggestions, cards = parse_tmdb_search_to_cards(
                    data, typed.strip(), limit=24
                )

                if suggestions:
                    labels = ["-- Select a movie --"] + [s[0] for s in suggestions]
                    selected = st.selectbox("Suggestions", labels, index=0)

                    if selected != "-- Select a movie --":
                        label_to_id = {s[0]: s[1] for s in suggestions}
                        goto_details(label_to_id[selected])
                else:
                    st.info("No suggestions found. Try another keyword.")

                st.markdown("### 🎯 Search Results")
                if cards:
                    st.markdown(f"Found **{len(cards)}** movies matching your search")
                poster_grid(cards, cols=grid_cols, key_prefix="search_results")

        st.stop()

    st.markdown(f"### 🏠 Home — {category_options[selected_category]}")

    home_cards, err = api_get_json(
        "/home", params={"category": selected_category, "limit": 24}
    )
    if err or not home_cards:
        st.error(f"Home feed failed: {err or 'Unknown error'}")
        st.stop()

    poster_grid(home_cards, cols=grid_cols, key_prefix="home_feed")

elif st.session_state.view == "details":
    tmdb_id = st.session_state.selected_tmdb_id
    if not tmdb_id:
        st.warning("No movie selected.")
        if st.button("← Back to Home"):
            goto_home()
        st.stop()

    a, b = st.columns([3, 1])
    with a:
        st.markdown("### 📄 Movie Details")
    with b:
        if st.button("← Back to Home"):
            goto_home()

    data, err = api_get_json(f"/movie/id/{tmdb_id}")
    if err or not data:
        st.error(f"Could not load details: {err or 'Unknown error'}")
        st.stop()

    poster_col, details_col = st.columns([1, 2.5], gap="large")

    with poster_col:
        if data.get("poster_url"):
            st.image(data["poster_url"], use_column_width=True)
        else:
            st.write("🖼️ No poster")

    with details_col:
        st.markdown(f"<h1 style='color: #ffd700; margin: 0 0 10px 0; text-shadow: 2px 2px 4px rgba(0,0,0,0.5);'>{data.get('title','')}</h1>", unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**📅 Release Date**")
            st.markdown(f"<div class='small-muted'>{data.get('release_date') or '-'}</div>", unsafe_allow_html=True)
        
        with col2:
            st.markdown("**🎭 Genres**")
            genres = [g["name"] for g in data.get("genres", [])]
            if genres:
                genre_badges = " ".join([f"<span style='background: rgba(102, 126, 234, 0.3); padding: 4px 8px; border-radius: 12px; margin: 2px; font-size: 0.8rem;'>{genre}</span>" for genre in genres])
                st.markdown(f"<div>{genre_badges}</div>", unsafe_allow_html=True)
            else:
                st.markdown(f"<div class='small-muted'>-</div>", unsafe_allow_html=True)
        
        st.markdown("---")
        
        st.markdown("**📝 Overview**")
        overview = data.get("overview") or "No overview available."
        st.markdown(f"<div style='line-height: 1.6; color: #e2e8f0;'>{overview}</div>", unsafe_allow_html=True)

    if data.get("backdrop_url"):
        st.markdown("#### Backdrop")
        st.image(data["backdrop_url"], use_column_width=True)

    st.divider()
    st.markdown("### ✅ Recommendations")

    title = (data.get("title") or "").strip()
    if title:
        bundle, err2 = api_get_json(
            "/movie/search",
            params={"query": title, "tfidf_top_n": 12, "genre_limit": 12},
        )

        if not err2 and bundle:
            tfidf_cards = to_cards_from_tfidf_items(bundle.get("tfidf_recommendations"))
            if tfidf_cards:
                st.markdown("#### 🔎 Similar Movies (TF-IDF)")
                st.markdown(f"Based on plot similarity and keywords")
                poster_grid(
                    tfidf_cards,
                    cols=grid_cols,
                    key_prefix="details_tfidf",
                )
            else:
                st.info("No TF-IDF recommendations found.")

            genre_cards = bundle.get("genre_recommendations", [])
            if genre_cards:
                st.markdown("#### 🎭 More Like This (Genre)")
                st.markdown(f"Based on similar genres and popularity")
                poster_grid(
                    genre_cards,
                    cols=grid_cols,
                    key_prefix="details_genre",
                )
            else:
                st.info("No genre recommendations found.")
        else:
            st.info("Showing Genre recommendations (fallback).")
            genre_only, err3 = api_get_json(
                "/recommend/genre", params={"tmdb_id": tmdb_id, "limit": 18}
            )
            if not err3 and genre_only:
                st.markdown("#### 🎬 Genre-Based Recommendations")
                poster_grid(
                    genre_only, cols=grid_cols, key_prefix="details_genre_fallback"
                )
            else:
                st.warning("No recommendations available right now.")
    else:
        st.warning("No title available to compute recommendations.")