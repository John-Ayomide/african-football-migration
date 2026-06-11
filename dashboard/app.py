# ============================================
# AFRICAN FOOTBALL MIGRATION DASHBOARD
# Footballers from Africa and the European Dream
# Data: FBref via soccerdata — 2024/25 season
# Author: John Ayomide
# ============================================

import os
from pathlib import Path
ROOT = Path(__file__).parent.parent
os.chdir(ROOT)

import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import matplotlib
matplotlib.use('Agg')
import warnings
warnings.filterwarnings('ignore')

# ── Page config ─────────────────────────────
st.set_page_config(
    page_title="African Football Migration",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ── Custom CSS ───────────────────────────────
st.markdown("""
<style>
    .stApp{background-color:#0a0a0f;color:#e8e8f0}
    .block-container{padding:2rem 3rem;max-width:1200px}
    [data-testid="metric-container"]{
        background:#111118;border:1px solid #2a2a3a;
        border-radius:12px;padding:16px}
    [data-testid="metric-container"] label{
        color:#6b6b80 !important;font-size:11px !important;
        text-transform:uppercase;letter-spacing:1.5px}
    [data-testid="metric-container"] [data-testid="stMetricValue"]{
        color:#00e5a0 !important;font-size:24px !important;
        font-weight:700 !important}
    h1,h2,h3{color:#e8e8f0 !important}
    hr{border-color:#2a2a3a !important}
    .stSelectbox label,.stMultiSelect label{color:#9999aa !important}
    .stButton button{
        background:linear-gradient(135deg,#00e5a0,#7b61ff) !important;
        color:#000 !important;font-weight:700 !important;
        border:none !important;border-radius:8px !important;
        width:100%}
    #MainMenu{visibility:hidden}
    footer{visibility:hidden}
    header{visibility:hidden}
</style>
""", unsafe_allow_html=True)

# ── Load data ────────────────────────────────
@st.cache_data
def load_data():
    df = pd.read_csv(
        'data/processed/african_players_clean.csv'
    )
    # Add performance score
    league_weights = {
        'Premier League': 1.0, 'La Liga': 0.95,
        'Bundesliga': 0.90, 'Serie A': 0.88,
        'Ligue 1': 0.82
    }
    position_weights = {
        'Forward': 1.0, 'Midfielder/Forward': 0.95,
        'Midfielder': 0.85, 'Defender/Midfielder': 0.75,
        'Defender': 0.65, 'Goalkeeper': 0.3
    }
    df['league_weight'] = df['league'].map(
        league_weights
    ).fillna(0.85)
    df['position_weight'] = df['position_clean'].map(
        position_weights
    ).fillna(0.8)
    df['performance_score'] = (
        df['goal_contributions_per90'] *
        df['league_weight'] *
        (2 - df['position_weight'])
    ).round(4)
    mn = df['performance_score'].min()
    mx = df['performance_score'].max()
    df['performance_score_100'] = (
        (df['performance_score'] - mn) /
        (mx - mn) * 100
    ).round(1)
    return df

df = load_data()
active = df[df['minutes'] >= 450].copy()

# ── Header ───────────────────────────────────
st.markdown("""
<div style='margin-bottom:8px'>
<span style='font-size:11px;color:#00e5a0;
letter-spacing:3px;text-transform:uppercase'>
Portfolio Project 03 — Flagship Football Analytics</span>
</div>
<h1 style='font-size:32px;font-weight:700;
color:#e8e8f0;margin-bottom:8px'>
Footballers from Africa and the
<span style='color:#00e5a0'>European Dream</span>
</h1>
<p style='color:#6b6b80;font-size:15px;
margin-bottom:32px'>
325 African players · Big 5 European Leagues ·
2024/25 Season · FBref Data
</p>
""", unsafe_allow_html=True)

# ── KPIs ─────────────────────────────────────
k1, k2, k3, k4, k5 = st.columns(5)
with k1:
    st.metric("African Players", f"{len(df):,}")
with k2:
    st.metric("Nations", f"{df['nationality'].nunique()}")
with k3:
    top_nation = df['nationality'].value_counts().index[0]
    st.metric("Top Nation", top_nation)
with k4:
    st.metric("Avg Age", f"{df['age'].mean():.1f} yrs")
with k5:
    ligue1 = len(df[df['league']=='Ligue 1'])
    st.metric("In Ligue 1", f"{ligue1} (44%)")

st.markdown("---")

# ── Tabs ─────────────────────────────────────
tab1, tab2, tab3, tab4 = st.tabs([
    "🌍 Migration Overview",
    "📊 Nation Analysis",
    "⚽ Player Explorer",
    "💎 Hidden Gems"
])

# ── TAB 1: MIGRATION OVERVIEW ────────────────
with tab1:
    st.markdown("### Where Do African Players Go?")

    col1, col2 = st.columns(2)

    with col1:
        # League distribution
        fig, ax = plt.subplots(figsize=(8, 5))
        fig.patch.set_facecolor('#111118')
        ax.set_facecolor('#111118')
        league_counts = df['league'].value_counts()
        colors = ['#7b61ff','#ffd166','#ff6b6b',
                  '#00e5a0','#ff9f43']
        bars = ax.bar(league_counts.index,
                      league_counts.values,
                      color=colors,
                      edgecolor='#2a2a3a')
        for bar, val in zip(bars, league_counts.values):
            ax.text(
                bar.get_x()+bar.get_width()/2,
                bar.get_height()+1,
                str(val), ha='center',
                color='#e8e8f0', fontsize=11,
                fontweight='bold'
            )
        ax.set_title('African Players by League',
                     color='#e8e8f0', fontsize=13,
                     fontweight='bold')
        ax.tick_params(colors='#9999aa',
                       labelrotation=15)
        ax.spines['bottom'].set_color('#2a2a3a')
        ax.spines['left'].set_color('#2a2a3a')
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        plt.tight_layout()
        st.pyplot(fig)

    with col2:
        # Regional breakdown
        fig, ax = plt.subplots(figsize=(8, 5))
        fig.patch.set_facecolor('#111118')
        region_counts = df['region'].value_counts()
        colors2 = ['#00e5a0','#7b61ff','#ff6b6b',
                   '#ffd166','#ff9f43']
        wedges, texts, autotexts = ax.pie(
            region_counts.values,
            labels=region_counts.index,
            autopct='%1.1f%%',
            colors=colors2,
            startangle=90,
            pctdistance=0.85,
            wedgeprops={
                'edgecolor':'#111118','linewidth':2
            }
        )
        for t in texts:
            t.set_color('#e8e8f0')
            t.set_fontsize(9)
        for at in autotexts:
            at.set_color('#000')
            at.set_fontsize(9)
            at.set_fontweight('bold')
        ax.set_title('Players by African Region',
                     color='#e8e8f0', fontsize=13,
                     fontweight='bold')
        fig.patch.set_facecolor('#111118')
        plt.tight_layout()
        st.pyplot(fig)

    # Key insight box
    st.markdown("""
    <div style='background:rgba(0,229,160,0.05);
    border:1px solid rgba(0,229,160,0.2);
    border-radius:8px;padding:16px;margin-top:16px'>
        <div style='font-size:11px;color:#00e5a0;
        text-transform:uppercase;letter-spacing:2px;
        margin-bottom:8px'>Key Finding</div>
        <p style='color:#e8e8f0;font-size:15px;
        font-weight:600'>
        France's Ligue 1 has 3x more African players
        than England's Premier League (159 vs 54)
        </p>
        <p style='color:#9999aa;font-size:13px;
        margin-top:8px'>
        Historical colonial ties and language links
        between France and West/North Africa create
        a dominant migration pipeline that no other
        European country matches.
        </p>
    </div>
    """, unsafe_allow_html=True)

# ── TAB 2: NATION ANALYSIS ───────────────────
with tab2:
    st.markdown("### Nation Performance Analysis")

    # Top nations bar chart
    fig, ax = plt.subplots(figsize=(10, 6))
    fig.patch.set_facecolor('#111118')
    ax.set_facecolor('#111118')
    nation_counts = df['nationality'].value_counts().head(12)
    colors = ['#00e5a0' if i==0 else
              '#7b61ff' if i<3 else '#4a4a6a'
              for i in range(len(nation_counts))]
    bars = ax.barh(nation_counts.index[::-1],
                   nation_counts.values[::-1],
                   color=colors[::-1],
                   edgecolor='#2a2a3a', height=0.7)
    for bar, val in zip(bars,
                        nation_counts.values[::-1]):
        ax.text(
            bar.get_width()+0.3,
            bar.get_y()+bar.get_height()/2,
            f'{val}', va='center',
            color='#e8e8f0', fontsize=11,
            fontweight='bold'
        )
    ax.set_title(
        'Top African Nations in Big 5 European Leagues',
        color='#e8e8f0', fontsize=14,
        fontweight='bold'
    )
    ax.tick_params(colors='#e8e8f0')
    ax.spines['bottom'].set_color('#2a2a3a')
    ax.spines['left'].set_color('#2a2a3a')
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    plt.tight_layout()
    st.pyplot(fig)

    # Nation performance table
    st.markdown("#### Performance by Nation")
    act = df[df['minutes'] >= 450]
    nation_perf = act.groupby('nationality').agg(
        Players=('player','count'),
        Avg_Goals_p90=('goals_per90','mean'),
        Avg_Assists_p90=('assists_per90','mean'),
        Avg_GC_p90=('goal_contributions_per90','mean'),
        Total_Goals=('goals','sum')
    ).round(3).reset_index()
    nation_perf = nation_perf[
        nation_perf['Players'] >= 5
    ].sort_values('Avg_GC_p90', ascending=False)
    st.dataframe(
        nation_perf,
        hide_index=True,
        use_container_width=True
    )

# ── TAB 3: PLAYER EXPLORER ───────────────────
with tab3:
    st.markdown("### Player Explorer")
    st.markdown(
        "<p style='color:#6b6b80;font-size:14px'>"
        "Filter and explore all 325 African players"
        " in the Big 5 European leagues.</p>",
        unsafe_allow_html=True
    )

    col1, col2, col3 = st.columns(3)
    with col1:
        nations = ['All'] + sorted(
            df['nationality'].unique().tolist()
        )
        sel_nation = st.selectbox("Nation", nations)
    with col2:
        leagues = ['All'] + sorted(
            df['league'].unique().tolist()
        )
        sel_league = st.selectbox("League", leagues)
    with col3:
        positions = ['All'] + sorted(
            df['position_clean'].dropna().unique().tolist()
        )
        sel_pos = st.selectbox("Position", positions)

    # Filter
    filtered = df.copy()
    if sel_nation != 'All':
        filtered = filtered[
            filtered['nationality'] == sel_nation
        ]
    if sel_league != 'All':
        filtered = filtered[
            filtered['league'] == sel_league
        ]
    if sel_pos != 'All':
        filtered = filtered[
            filtered['position_clean'] == sel_pos
        ]

    st.markdown(
        f"**{len(filtered)} players** match your filters"
    )

    display_cols = [
        'player', 'nationality', 'position_clean',
        'age', 'club', 'league', 'goals',
        'assists', 'matches_played',
        'goal_contributions_per90',
        'performance_score_100'
    ]
    st.dataframe(
        filtered[display_cols].sort_values(
            'performance_score_100', ascending=False
        ).round(3),
        hide_index=True,
        use_container_width=True
    )

# ── TAB 4: HIDDEN GEMS ───────────────────────
with tab4:
    st.markdown("### 💎 Hidden Gems")
    st.markdown("""
    <p style='color:#6b6b80;font-size:14px;
    margin-bottom:20px'>
    African players massively outperforming their
    league level — potential recruitment targets
    for Premier League clubs.
    </p>
    """, unsafe_allow_html=True)

    act2 = df[df['minutes'] >= 450].copy()
    league_avg = act2.groupby('league')[
        'performance_score_100'
    ].mean()
    act2['league_avg'] = act2['league'].map(league_avg)
    act2['outperformance'] = (
        act2['performance_score_100'] -
        act2['league_avg']
    ).round(1)

    gems = act2[
        act2['league'] != 'Premier League'
    ].nlargest(10, 'outperformance')

    for _, row in gems.iterrows():
        score_color = (
            '#00e5a0' if row['performance_score_100'] >= 50
            else '#ffd166' if row['performance_score_100'] >= 25
            else '#ff6b6b'
        )
        st.markdown(f"""
        <div style='background:#111118;
        border:1px solid #2a2a3a;
        border-left:3px solid {score_color};
        border-radius:0 8px 8px 0;
        padding:16px;margin-bottom:10px'>
            <div style='display:flex;
            justify-content:space-between;
            align-items:center'>
                <div>
                    <span style='font-size:15px;
                    font-weight:700;color:#e8e8f0'>
                    {row['player']}
                    </span>
                    <span style='color:#6b6b80;
                    font-size:13px;margin-left:8px'>
                    {row['nationality']} ·
                    Age {row['age']:.0f}
                    </span>
                </div>
                <span style='font-size:18px;
                font-weight:700;color:{score_color}'>
                Score: {row['performance_score_100']:.0f}/100
                </span>
            </div>
            <div style='color:#9999aa;font-size:13px;
            margin-top:8px'>
                {row['club']} · {row['league']} ·
                {row['position_clean']} ·
                {row['goals']:.0f}G {row['assists']:.0f}A ·
                Outperformance: +{row['outperformance']:.1f}
            </div>
        </div>
        """, unsafe_allow_html=True)

# ── Footer ───────────────────────────────────
st.markdown("---")
st.markdown("""
<div style='color:#6b6b80;font-size:12px;
text-align:center'>
    Built by <strong style='color:#e8e8f0'>
    John Ayomide</strong> &nbsp;·&nbsp;
    <a href='https://github.com/John-Ayomide/
african-football-migration'
    style='color:#00e5a0;text-decoration:none'>
    GitHub</a> &nbsp;·&nbsp;
    Data: FBref via soccerdata · 2024/25 Season
</div>
""", unsafe_allow_html=True)