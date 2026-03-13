import streamlit as st
import random
import math
from typing import Optional

# ─────────────────────────────────────────────────────────────────────────────
# PAGE CONFIG
# ─────────────────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Lotto Number Generator",
    page_icon="🎱",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─────────────────────────────────────────────────────────────────────────────
# CSS
# ─────────────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
/* ── Base ── */
html, body, [class*="css"] { font-family: 'Segoe UI', Arial, sans-serif; }
.stApp { background: #0d1b2a; }

/* ── Sidebar ── */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #1a2f45 0%, #0d1b2a 100%);
    border-right: 1px solid #2e4a6a;
}
[data-testid="stSidebar"] * { color: #c8daf0 !important; }
[data-testid="stSidebar"] label { color: #8ab4d8 !important; font-size: 0.82rem !important; font-weight: 600 !important; letter-spacing: 0.04em; }
[data-testid="stSidebar"] .stSelectbox div[data-baseweb="select"] > div,
[data-testid="stSidebar"] .stNumberInput input {
    background: #0d1b2a !important;
    border: 1px solid #2e5080 !important;
    color: #e0f0ff !important;
    border-radius: 6px !important;
}
[data-testid="stSidebar"] h1, [data-testid="stSidebar"] h2, [data-testid="stSidebar"] h3 {
    color: #7eb8e8 !important;
}
[data-testid="stSidebar"] hr { border-color: #2e4a6a !important; }

/* ── Main area ── */
.main .block-container { padding: 2rem 2.5rem; max-width: 1100px; }

/* ── Hero header ── */
.hero {
    background: linear-gradient(135deg, #1a3a5c 0%, #0d2640 50%, #1a1a3e 100%);
    border: 1px solid #2e5080;
    border-radius: 16px;
    padding: 2rem 2.5rem;
    text-align: center;
    margin-bottom: 2rem;
    box-shadow: 0 8px 32px rgba(0,0,0,0.4);
}
.hero h1 { color: #ffffff; font-size: 2.2rem; font-weight: 800; margin: 0 0 0.3rem; letter-spacing: 0.02em; }
.hero p  { color: #8ab4d8; margin: 0; font-size: 1rem; }

/* ── Section cards ── */
.section-card {
    background: #112035;
    border: 1px solid #1e3a5a;
    border-radius: 12px;
    padding: 1.4rem 1.8rem;
    margin-bottom: 1.5rem;
}
.section-title {
    color: #5ba3d9;
    font-size: 0.78rem;
    font-weight: 700;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    margin-bottom: 1rem;
    display: flex;
    align-items: center;
    gap: 0.5rem;
}

/* ── Preset buttons ── */
.preset-btn { cursor: pointer; }
[data-testid="baseButton-secondary"] {
    background: #1a3050 !important;
    border: 1px solid #2e5080 !important;
    color: #8ab4d8 !important;
    border-radius: 8px !important;
    font-size: 0.78rem !important;
    padding: 0.3rem 0.8rem !important;
    transition: all 0.2s !important;
}
[data-testid="baseButton-secondary"]:hover {
    background: #2e5080 !important;
    color: #ffffff !important;
    border-color: #5ba3d9 !important;
}

/* ── Generate button ── */
[data-testid="baseButton-primary"] {
    background: linear-gradient(135deg, #1e7b34, #145228) !important;
    border: none !important;
    border-radius: 10px !important;
    color: white !important;
    font-size: 1.05rem !important;
    font-weight: 700 !important;
    padding: 0.7rem 2rem !important;
    width: 100% !important;
    letter-spacing: 0.05em !important;
    box-shadow: 0 4px 16px rgba(30,123,52,0.35) !important;
    transition: all 0.2s !important;
}
[data-testid="baseButton-primary"]:hover {
    background: linear-gradient(135deg, #28a745, #1e7b34) !important;
    box-shadow: 0 6px 20px rgba(30,123,52,0.5) !important;
    transform: translateY(-1px) !important;
}

/* ── Results ── */
.results-header {
    background: linear-gradient(135deg, #1f4e79, #0d2640);
    color: white;
    border-radius: 12px 12px 0 0;
    padding: 1rem 1.5rem;
    font-size: 1.1rem;
    font-weight: 700;
    letter-spacing: 0.05em;
    text-align: center;
}
.results-table {
    background: #0d1b2a;
    border: 1px solid #1e3a5a;
    border-radius: 0 0 12px 12px;
    overflow: hidden;
    margin-bottom: 1.5rem;
}
.game-row {
    display: flex;
    align-items: center;
    padding: 0.6rem 1rem;
    border-bottom: 1px solid #1a3050;
    gap: 0.5rem;
}
.game-row:last-child { border-bottom: none; }
.game-row:nth-child(even) { background: #0f2236; }
.game-label {
    color: #5ba3d9;
    font-weight: 700;
    font-size: 0.85rem;
    width: 70px;
    flex-shrink: 0;
}
.balls-container { display: flex; flex-wrap: wrap; gap: 6px; align-items: center; }
.ball {
    width: 40px; height: 40px;
    border-radius: 50%;
    display: inline-flex;
    align-items: center;
    justify-content: center;
    font-weight: 800;
    font-size: 0.88rem;
    box-shadow: 0 2px 8px rgba(0,0,0,0.35);
    flex-shrink: 0;
}
.ball-primary {
    background: radial-gradient(circle at 35% 35%, #4a9fd4, #1a5a8a);
    color: white;
    border: 2px solid #5ba3d9;
}
.ball-lucky {
    background: radial-gradient(circle at 35% 35%, #f5c842, #c09010);
    color: #3a2800;
    border: 2px solid #e6b820;
}
.ball-secondary {
    background: radial-gradient(circle at 35% 35%, #e05a28, #8a2800);
    color: white;
    border: 2px solid #e07040;
    width: 44px; height: 44px;
    font-size: 0.95rem;
}
.ball-separator {
    color: #2e5080;
    font-size: 1.4rem;
    font-weight: 300;
    padding: 0 2px;
}
.legend {
    display: flex;
    gap: 1.5rem;
    padding: 0.7rem 1rem;
    background: #091525;
    border-radius: 0 0 12px 12px;
    margin-top: -1px;
    flex-wrap: wrap;
}
.legend-item { display: flex; align-items: center; gap: 0.4rem; font-size: 0.78rem; color: #8ab4d8; }
.legend-dot { width: 14px; height: 14px; border-radius: 50%; flex-shrink: 0; }

/* ── Validation error ── */
.error-box {
    background: #2a0d0d;
    border: 1px solid #8b1a1a;
    border-radius: 8px;
    padding: 1rem 1.2rem;
    color: #ff8080;
    font-size: 0.9rem;
    margin-bottom: 1rem;
}

/* ── Info box ── */
.info-box {
    background: #0d2233;
    border-left: 3px solid #2e75b6;
    border-radius: 0 8px 8px 0;
    padding: 0.7rem 1rem;
    color: #8ab4d8;
    font-size: 0.82rem;
    margin-top: 0.5rem;
}

/* ── Stats bar ── */
.stats-bar {
    display: flex;
    gap: 1.5rem;
    background: #091525;
    border: 1px solid #1e3a5a;
    border-radius: 10px;
    padding: 0.8rem 1.2rem;
    margin-bottom: 1.5rem;
    flex-wrap: wrap;
}
.stat-item { text-align: center; }
.stat-value { color: #5ba3d9; font-size: 1.4rem; font-weight: 800; }
.stat-label { color: #4a7090; font-size: 0.72rem; text-transform: uppercase; letter-spacing: 0.08em; }

/* ── Misc ── */
[data-testid="stNumberInput"] input { border-radius: 6px !important; }
.stCheckbox label { color: #8ab4d8 !important; font-size: 0.85rem !important; }
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────────────────
# PRESETS
# ─────────────────────────────────────────────────────────────────────────────
PRESETS = {
    "OzLotto":         dict(primary_per=7,  secondary_per=0, primary_pool=45, secondary_pool=0),
    "US Powerball":    dict(primary_per=5,  secondary_per=1, primary_pool=69, secondary_pool=26),
    "US Mega Millions":dict(primary_per=5,  secondary_per=1, primary_pool=70, secondary_pool=25),
    "EuroMillions":    dict(primary_per=5,  secondary_per=2, primary_pool=50, secondary_pool=12),
    "UK Lotto":        dict(primary_per=6,  secondary_per=0, primary_pool=59, secondary_pool=0),
    "Saturday Lotto":  dict(primary_per=6,  secondary_per=0, primary_pool=45, secondary_pool=0),
    "Tattslotto":      dict(primary_per=6,  secondary_per=0, primary_pool=45, secondary_pool=0),
    "Custom":          dict(primary_per=6,  secondary_per=1, primary_pool=49, secondary_pool=10),
}

# ─────────────────────────────────────────────────────────────────────────────
# CORE GENERATION LOGIC
# ─────────────────────────────────────────────────────────────────────────────
def validate(primary_per, secondary_per, num_games, primary_pool, secondary_pool,
             allow_dup_pri, allow_dup_sec, must_nums) -> Optional[str]:
    if primary_per < 1 or primary_per > primary_pool:
        return f"Primary numbers per game ({primary_per}) must be between 1 and the pool size ({primary_pool})."
    if num_games < 1:
        return "Number of games must be at least 1."
    if primary_pool < 1:
        return "Primary pool size must be at least 1."
    if secondary_per > 0 and secondary_pool < secondary_per:
        return f"Secondary pool ({secondary_pool}) must be ≥ secondary numbers per game ({secondary_per})."
    if len(must_nums) != len(set(must_nums)):
        return "Must-include numbers contain duplicates. Each lucky number must be unique."
    bad = [n for n in must_nums if n < 1 or n > primary_pool]
    if bad:
        return f"Must-include number(s) {bad} are outside the primary pool range (1–{primary_pool})."
    max_must_per_game = math.ceil(len(must_nums) / num_games) if num_games > 0 else 0
    if max_must_per_game > primary_per:
        return (f"Cannot distribute {len(must_nums)} lucky numbers across {num_games} game(s) "
                f"with only {primary_per} numbers per game. Add more games or reduce lucky numbers.")
    if not allow_dup_pri:
        rand_need  = primary_per * num_games - len(must_nums)
        rand_avail = primary_pool - len(must_nums)
        if rand_need > rand_avail:
            return (f"Unique primary mode: need {rand_need} unique random numbers "
                    f"but only {rand_avail} available in pool after reserving lucky numbers.\n"
                    f"Reduce games, reduce numbers-per-game, increase pool, or allow duplicates.")
    if secondary_per > 0 and not allow_dup_sec:
        need = secondary_per * num_games
        if need > secondary_pool:
            return (f"Unique secondary mode: need {need} unique bonus numbers "
                    f"but pool only has {secondary_pool}.\n"
                    f"Reduce games, reduce secondary-per-game, increase secondary pool, or allow duplicates.")
    return None


def generate_games(primary_per, secondary_per, num_games, primary_pool, secondary_pool,
                   allow_dup_pri, allow_dup_sec, must_nums):
    must_nums = list(must_nums)
    must_count = len(must_nums)

    # Assign each must-include to exactly one game (randomised round-robin)
    must_assign = {}  # must_nums[i] -> game index (0-based)
    if must_count > 0:
        assignment = list(range(num_games)) * (math.ceil(must_count / num_games))
        assignment = assignment[:must_count]
        random.shuffle(assignment)
        for i, mn in enumerate(must_nums):
            must_assign[i] = assignment[i]

    # Build pre-shuffled primary pool (excludes must-includes)
    pri_pool_list = []
    if not allow_dup_pri:
        must_set = set(must_nums)
        pri_pool_list = [n for n in range(1, primary_pool + 1) if n not in must_set]
        random.shuffle(pri_pool_list)
    pri_pos = [0]

    # Build pre-shuffled secondary pool
    sec_pool_list = []
    if secondary_per > 0 and not allow_dup_sec:
        sec_pool_list = list(range(1, secondary_pool + 1))
        random.shuffle(sec_pool_list)
    sec_pos = [0]

    games = []
    for g in range(num_games):
        # Primary: seed with must-includes assigned to this game
        game_must = [must_nums[i] for i in range(must_count) if must_assign.get(i) == g]
        picks = list(game_must)

        slots_left = primary_per - len(picks)

        if allow_dup_pri:
            # Within-game uniqueness always enforced
            used = set(picks)
            attempts = 0
            while len(picks) < primary_per:
                n = random.randint(1, primary_pool)
                if n not in used:
                    picks.append(n)
                    used.add(n)
                attempts += 1
                if attempts > 500_000:
                    raise RuntimeError(f"Could not fill game {g+1} — pool too small for within-game uniqueness.")
        else:
            # No cross-game duplicates — draw from pre-shuffled pool
            for _ in range(slots_left):
                picks.append(pri_pool_list[pri_pos[0]])
                pri_pos[0] += 1

        picks.sort()

        # Secondary
        bonus = []
        if secondary_per > 0:
            if allow_dup_sec:
                used_s = set()
                attempts = 0
                while len(bonus) < secondary_per:
                    n = random.randint(1, secondary_pool)
                    if n not in used_s:
                        bonus.append(n)
                        used_s.add(n)
                    attempts += 1
                    if attempts > 500_000:
                        break
            else:
                for _ in range(secondary_per):
                    bonus.append(sec_pool_list[sec_pos[0]])
                    sec_pos[0] += 1
            bonus.sort()

        games.append({
            "game":     g + 1,
            "picks":    picks,
            "bonus":    bonus,
            "must_set": set(game_must),
        })

    return games


def render_results(games, game_name, primary_per, secondary_per,
                   primary_pool, secondary_pool, allow_dup_pri, allow_dup_sec, must_nums):
    title = f"🎱 {game_name.upper()} — GENERATED NUMBERS"
    st.markdown(f'<div class="results-header">{title}</div>', unsafe_allow_html=True)

    # Stats bar
    total_nums = len(games) * primary_per
    total_bonus = len(games) * secondary_per
    has_lucky = any(g["must_set"] for g in games)

    st.markdown(f"""
    <div class="stats-bar">
        <div class="stat-item"><div class="stat-value">{len(games)}</div><div class="stat-label">Games</div></div>
        <div class="stat-item"><div class="stat-value">{primary_per}</div><div class="stat-label">Numbers/Game</div></div>
        <div class="stat-item"><div class="stat-value">{total_nums}</div><div class="stat-label">Total Numbers</div></div>
        <div class="stat-item"><div class="stat-value">1–{primary_pool}</div><div class="stat-label">Primary Pool</div></div>
        {"" if secondary_per == 0 else f'<div class="stat-item"><div class="stat-value">1–{secondary_pool}</div><div class="stat-label">Bonus Pool</div></div>'}
        <div class="stat-item"><div class="stat-value">{"YES" if allow_dup_pri else "NO"}</div><div class="stat-label">Allow Dup Primary</div></div>
        {"" if secondary_per == 0 else f'<div class="stat-item"><div class="stat-value">{"YES" if allow_dup_sec else "NO"}</div><div class="stat-label">Allow Dup Bonus</div></div>'}
    </div>
    """, unsafe_allow_html=True)

    # Game rows
    rows_html = '<div class="results-table"><div style="border-radius:0 0 12px 12px; overflow:hidden;">'
    for g in games:
        balls_html = ""
        for n in g["picks"]:
            css = "ball-lucky" if n in g["must_set"] else "ball-primary"
            balls_html += f'<div class="ball {css}">{n}</div>'
        if g["bonus"]:
            balls_html += '<div class="ball-separator">|</div>'
            for n in g["bonus"]:
                balls_html += f'<div class="ball ball-secondary">{n}</div>'

        stripe = "background:#0f2236;" if g["game"] % 2 == 0 else ""
        rows_html += f"""
        <div class="game-row" style="{stripe}">
            <div class="game-label">GAME {g["game"]}</div>
            <div class="balls-container">{balls_html}</div>
        </div>"""

    rows_html += "</div></div>"
    st.markdown(rows_html, unsafe_allow_html=True)

    # Legend
    legend_html = '<div class="legend">'
    legend_html += '<div class="legend-item"><div class="legend-dot" style="background:radial-gradient(circle at 35% 35%,#4a9fd4,#1a5a8a);border:1px solid #5ba3d9"></div> Primary numbers</div>'
    if has_lucky:
        legend_html += '<div class="legend-item"><div class="legend-dot" style="background:radial-gradient(circle at 35% 35%,#f5c842,#c09010);border:1px solid #e6b820"></div> Lucky / must-include numbers</div>'
    if secondary_per > 0:
        legend_html += '<div class="legend-item"><div class="legend-dot" style="background:radial-gradient(circle at 35% 35%,#e05a28,#8a2800);border:1px solid #e07040"></div> Bonus / Powerball numbers</div>'
    legend_html += '</div>'
    st.markdown(legend_html, unsafe_allow_html=True)

    # Text export
    lines = [f"{game_name} - Generated Numbers", "=" * 50]
    for g in games:
        picks_str = "  ".join(f"{n:>2}" for n in g["picks"])
        bonus_str = ("  |  Bonus: " + "  ".join(f"{n:>2}" for n in g["bonus"])) if g["bonus"] else ""
        lucky_str = (f"  ★ Lucky: {sorted(g['must_set'])}") if g["must_set"] else ""
        lines.append(f"Game {g['game']:>3}:  {picks_str}{bonus_str}{lucky_str}")
    lines += ["", f"Primary pool: 1-{primary_pool}",
              f"Duplicates allowed (primary): {'Yes' if allow_dup_pri else 'No'}"]
    if secondary_per > 0:
        lines += [f"Bonus pool: 1-{secondary_pool}",
                  f"Duplicates allowed (bonus): {'Yes' if allow_dup_sec else 'No'}"]
    if must_nums:
        lines.append(f"Lucky numbers (each used once): {sorted(must_nums)}")

    st.download_button(
        label="📥  Download Results (.txt)",
        data="\n".join(lines),
        file_name=f"{game_name.replace(' ', '_')}_lotto_numbers.txt",
        mime="text/plain",
        use_container_width=True,
    )


# ─────────────────────────────────────────────────────────────────────────────
# SIDEBAR
# ─────────────────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("### 🎮 Game Setup")
    st.markdown("---")

    # Preset selector
    preset_name = st.selectbox("Quick Preset", list(PRESETS.keys()), index=0)
    preset = PRESETS[preset_name]

    if preset_name != "Custom":
        game_name = preset_name
    else:
        game_name = st.text_input("Game Name", value="My Lotto")

    st.markdown("---")
    st.markdown("**Numbers**")

    primary_per   = st.number_input("Primary numbers per game",   min_value=1,  max_value=20,  value=preset["primary_per"])
    secondary_per = st.number_input("Bonus numbers per game (0 = none)", min_value=0, max_value=10, value=preset["secondary_per"])
    num_games     = st.number_input("Number of games to generate", min_value=1, max_value=200, value=10)

    st.markdown("---")
    st.markdown("**Number Pools**")

    primary_pool   = st.number_input("Primary pool size (pick from 1 to...)",  min_value=1, max_value=1000, value=preset["primary_pool"])
    if secondary_per > 0:
        secondary_pool = st.number_input("Bonus pool size (pick from 1 to...)", min_value=1, max_value=1000, value=max(preset["secondary_pool"], secondary_per))
    else:
        secondary_pool = preset["secondary_pool"] or 1

    st.markdown("---")
    st.markdown("**Duplicate Settings**")

    allow_dup_pri = st.checkbox("Allow duplicate primary numbers across games",  value=True)
    if secondary_per > 0:
        allow_dup_sec = st.checkbox("Allow duplicate bonus numbers across games", value=True)
    else:
        allow_dup_sec = True

    st.markdown("---")
    st.markdown("**⭐ Lucky / Must-Include Numbers**")
    st.caption("Each number appears in exactly ONE game only.")

    must_nums_raw = []
    cols = st.columns(2)
    for i in range(8):
        col = cols[i % 2]
        val = col.number_input(f"Lucky #{i+1}", min_value=0, max_value=primary_pool,
                               value=0, key=f"lucky_{i}",
                               help=f"0 = not used. Must be between 1 and {primary_pool}.")
        if val > 0:
            must_nums_raw.append(val)

    must_nums = must_nums_raw

    st.markdown("---")
    generate = st.button("▶  GENERATE NUMBERS", type="primary", use_container_width=True)

# ─────────────────────────────────────────────────────────────────────────────
# MAIN AREA
# ─────────────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero">
    <h1>🎱 Lotto Number Generator</h1>
    <p>Configure your game in the sidebar, then hit Generate Numbers</p>
</div>
""", unsafe_allow_html=True)

# Info cards when idle
if not generate and "last_games" not in st.session_state:
    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown("""
        <div class="section-card">
            <div class="section-title">🎯 Any Game Format</div>
            <p style="color:#8ab4d8;font-size:0.88rem;">Supports OzLotto, Powerball, Mega Millions, EuroMillions, Saturday Lotto — or any custom format with or without bonus balls.</p>
        </div>""", unsafe_allow_html=True)
    with c2:
        st.markdown("""
        <div class="section-card">
            <div class="section-title">🔒 Unique Number Mode</div>
            <p style="color:#8ab4d8;font-size:0.88rem;">Turn off duplicates to ensure no number appears in more than one game across your entire set of tickets. Numbers are always unique within a single game.</p>
        </div>""", unsafe_allow_html=True)
    with c3:
        st.markdown("""
        <div class="section-card">
            <div class="section-title">⭐ Lucky Numbers</div>
            <p style="color:#8ab4d8;font-size:0.88rem;">Add up to 8 birthdays or lucky numbers. Each is placed in exactly one game — spread across your tickets, highlighted in gold.</p>
        </div>""", unsafe_allow_html=True)

# Generate
if generate:
    err = validate(primary_per, secondary_per, num_games, primary_pool, secondary_pool,
                   allow_dup_pri, allow_dup_sec, must_nums)
    if err:
        st.markdown(f'<div class="error-box">⚠️  {err.replace(chr(10), "<br>")}</div>', unsafe_allow_html=True)
    else:
        with st.spinner("Generating your lucky numbers..."):
            games = generate_games(primary_per, secondary_per, num_games, primary_pool,
                                   secondary_pool, allow_dup_pri, allow_dup_sec, must_nums)
        st.session_state["last_games"] = games
        st.session_state["last_params"] = dict(
            game_name=game_name, primary_per=primary_per, secondary_per=secondary_per,
            primary_pool=primary_pool, secondary_pool=secondary_pool,
            allow_dup_pri=allow_dup_pri, allow_dup_sec=allow_dup_sec, must_nums=must_nums
        )

if "last_games" in st.session_state:
    p = st.session_state["last_params"]
    render_results(
        st.session_state["last_games"],
        p["game_name"], p["primary_per"], p["secondary_per"],
        p["primary_pool"], p["secondary_pool"],
        p["allow_dup_pri"], p["allow_dup_sec"], p["must_nums"]
    )
