import dash
from dash import dcc, html, Input, Output
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import requests

# ─────────────────────────────────────────────────────────────
# BRAND
# ─────────────────────────────────────────────────────────────
TEAL        = '#1A7B7A'
TEAL_DARK   = '#0F5B5A'
TEAL_LIGHT  = '#E5F2F2'
GOLD        = '#D4940A'
GOLD_LIGHT  = '#FBF0D8'
BG          = '#F2F6F6'
CARD        = '#FFFFFF'
TEXT_DARK   = '#0F2E2E'
TEXT_MED    = '#3D6060'
TEXT_LIGHT  = '#7A9C9C'
BORDER      = '#D4E5E5'

PALETTE = [TEAL, GOLD, '#2D9B9A', '#E8A820', TEAL_DARK,
           '#B8D9D9', '#7FB5B5', '#F5C842', '#5AAEAE', '#A07808']

ISIC_COLOR = {
    'Residential & Long-term Care (ISIC 8710)':      TEAL,
    'Medical & Dental Practice (ISIC 8620)':          GOLD,
    'Other Health Services & Industry (ISIC 8690)':   '#2D9B9A',
    'Hospitals & Acute Care (ISIC 8610)':             '#E8A820',
    'Staffing & Recruitment (ISIC 7820)':             TEAL_DARK,
    'Mental Health & Rehabilitation (ISIC 8720)':     '#B8D9D9',
}

FONT = 'Outfit, DM Sans, sans-serif'

# ─────────────────────────────────────────────────────────────
# DATA
# ─────────────────────────────────────────────────────────────
TOTAL          = 29_045
HC_JOBS        = 15_724
NON_HC_JOBS    = 13_321
EMPLOYERS      = 10_657
STATES         = 16
DATE_RANGE     = '31 Jan – 10 Mar 2026'

job_cats = [
    ('Nursing & Midwifery Professionals (ISCO 222)',  4207),
    ('Other Health Associates (ISCO 325)',             3049),
    ('Other Health Professionals (ISCO 226)',          2312),
    ('Personal Care Workers (ISCO 532)',               2196),
    ('Medical Doctors (ISCO 221)',                     1663),
    ('Other Healthcare (ISCO 22x/32x/53x)',            2580),
    ('Nursing & Midwifery Associates (ISCO 322)',       909),
    ('Medical & Pharma Technicians (ISCO 321)',         870),
    ('Child Care & Teachers Aides (ISCO 531)',          369),
    ('Non-Healthcare',                                10890),
]

isco4_data = [
    ('Nursing Professionals',                                   2221, 4178),
    ('Social Work & Counselling Professionals',                 2635, 1896),
    ('Specialist Medical Practitioners',                        2212, 1444),
    ('Medical Assistants',                                      3256, 1272),
    ('Health Care Assistants',                                  5321, 1193),
    ('Physiotherapists',                                        2264, 1067),
    ('Health Service Managers',                                 1342, 1067),
    ('Home-based Personal Care Workers',                        5322,  950),
    ('Nursing Associate Professionals',                         3221,  896),
    ('Dental Assistants and Therapists',                        3251,  775),
    ('Sports, Recreation & Cultural Centre Managers',           1431,  717),
    ('Early Childhood Educators',                               2342,  538),
    ('Health Professionals NEC',                                2269,  464),
    ('Specialised Shop Salespersons',                           5223,  455),
    ('Health Associate Professionals NEC',                      3259,  449),
    ('Medical and Dental Prosthetic Technicians',               3214,  435),
    ('Cleaners & Helpers in Offices / Hotels',                  9112,  400),
    ('General Office Clerks',                                   4110,  393),
    ('Audiologists and Speech Therapists',                      2266,  321),
    ('Social Work Associate Professionals',                     3412,  311),
]

titles_data = [
    ('Physiotherapist', 918), ('Nursing Assistant', 732),
    ('Registered Nurse', 615), ('Medical Assistant', 590),
    ('Occupational Therapist', 454), ('Dental Assistant', 437),
    ('Geriatric Nurse', 310), ('Nursing Specialist', 217),
    ('Qualified Nurse', 200), ('Nursing Service Manager', 158),
    ('Nursing Professional', 153), ('Social Pedagogue', 124),
    ('Housekeeping Assistant', 122), ('Educator', 116),
    ('Dental Technician', 112), ('Hairdresser', 110),
    ('Social Worker', 107), ('Cleaner', 104),
    ('Early Childhood Educator', 98), ('Pedagogical Specialist', 98),
]

isic_data = [
    ('Residential & Long-term Care (ISIC 8710)',      9383),
    ('Medical & Dental Practice (ISIC 8620)',          6216),
    ('Other Health Services & Industry (ISIC 8690)',   5131),
    ('Hospitals & Acute Care (ISIC 8610)',             3617),
    ('Staffing & Recruitment (ISIC 7820)',             2446),
    ('Mental Health & Rehabilitation (ISIC 8720)',     2252),
]

employer_data = [
    ('Korian Deutschland GmbH',                            382, 'Residential & Long-term Care (ISIC 8710)'),
    ('inCare by Piening',                                  275, 'Staffing & Recruitment (ISIC 7820)'),
    ('avanti GmbH',                                        263, 'Staffing & Recruitment (ISIC 7820)'),
    ('ZAR Gesundheits- und Therapiezentrum Bad Cannstatt', 233, 'Medical & Dental Practice (ISIC 8620)'),
    ('Schön Klinik Gruppe',                                216, 'Hospitals & Acute Care (ISIC 8610)'),
    ('BSG Bildungsinstitut für Soziales und Gesundheit',   137, 'Other Health Services & Industry (ISIC 8690)'),
    ('Klinikum Westmünsterland GmbH',                      132, 'Hospitals & Acute Care (ISIC 8610)'),
    ('Evangelische Heimstiftung GmbH',                     131, 'Residential & Long-term Care (ISIC 8710)'),
    ('NOVOTERGUM GmbH',                                    116, 'Medical & Dental Practice (ISIC 8620)'),
    ('Starnberger Kliniken GmbH',                          107, 'Hospitals & Acute Care (ISIC 8610)'),
    ('ELBLANDKLINIKEN Stiftung & Co. KG',                  102, 'Hospitals & Acute Care (ISIC 8610)'),
    ('DRK-Schwesternschaft Berlin e.V.',                    99, 'Residential & Long-term Care (ISIC 8710)'),
    ('Vitolus GmbH',                                        95, 'Medical & Dental Practice (ISIC 8620)'),
    ('BeneVit',                                             91, 'Residential & Long-term Care (ISIC 8710)'),
    ('Evangelisches Krankenhaus Wesel GmbH',                86, 'Hospitals & Acute Care (ISIC 8610)'),
]

state_data = {
    'Berlin':                 (1925, 52.52, 13.40, ['Nursing Professionals (2221)', 'Social Work & Counselling Professionals (2635)', 'Specialist Medical Practitioners (2212)']),
    'North Rhine-Westphalia': (1755, 51.43,  7.66, ['Nursing Professionals (2221)', 'Nursing Associate Professionals (3221)', 'Medical Assistants (3256)']),
    'Bavaria':                (1696, 48.79, 11.50, ['Nursing Professionals (2221)', 'Medical Assistants (3256)', 'Specialist Medical Practitioners (2212)']),
    'Hamburg':                ( 955, 53.55, 10.00, ['Nursing Professionals (2221)', 'Social Work & Counselling Professionals (2635)', 'Medical Assistants (3256)']),
    'Baden-Württemberg':      ( 705, 48.66,  9.35, ['Nursing Professionals (2221)', 'Medical Assistants (3256)', 'Specialist Medical Practitioners (2212)']),
    'Lower Saxony':           ( 580, 52.64,  9.84, ['Nursing Professionals (2221)', 'Medical Assistants (3256)', 'Specialist Medical Practitioners (2212)']),
    'Saxony':                 ( 541, 51.11, 13.20, ['Nursing Professionals (2221)', 'Specialist Medical Practitioners (2212)', 'Physiotherapists (2264)']),
    'Hesse':                  ( 382, 50.65,  9.16, ['Nursing Professionals (2221)', 'Specialist Medical Practitioners (2212)', 'Social Work & Counselling Professionals (2635)']),
    'Bremen':                 ( 256, 53.08,  8.81, ['Nursing Professionals (2221)', 'Social Work & Counselling Professionals (2635)', 'Health Service Managers (1342)']),
    'Brandenburg':            ( 251, 52.41, 13.52, ['Nursing Professionals (2221)', 'Specialist Medical Practitioners (2212)', 'Social Work & Counselling Professionals (2635)']),
    'Rhineland-Palatinate':   ( 221, 50.12,  7.31, ['Nursing Professionals (2221)', 'Specialist Medical Practitioners (2212)', 'Nursing Associate Professionals (3221)']),
    'Schleswig-Holstein':     ( 218, 54.22,  9.68, ['Nursing Professionals (2221)', 'Nursing Associate Professionals (3221)', 'Medical Assistants (3256)']),
    'Thuringia':              ( 216, 50.88, 11.03, ['Specialist Medical Practitioners (2212)', 'Nursing Professionals (2221)', 'Health Care Assistants (5321)']),
    'Saxony-Anhalt':          ( 198, 51.88, 11.70, ['Specialist Medical Practitioners (2212)', 'Nursing Professionals (2221)', 'Social Work & Counselling Professionals (2635)']),
    'Mecklenburg-Vorpommern': ( 115, 53.61, 12.43, ['Nursing Professionals (2221)', 'Nursing Associate Professionals (3221)', 'Specialist Medical Practitioners (2212)']),
    'Saarland':               (  85, 49.40,  7.02, ['Nursing Professionals (2221)', 'Social Work & Counselling Professionals (2635)', 'Early Childhood Educators (2342)']),
}

# Fetch Germany GeoJSON once at startup
GEOJSON_URL = ('https://raw.githubusercontent.com/isellsoap/deutschlandGeoJSON'
               '/main/2_bundeslaender/4_niedrig.geo.json')
STATE_DE = {
    'Baden-Württemberg': 'Baden-Württemberg', 'Bavaria': 'Bayern',
    'Berlin': 'Berlin', 'Brandenburg': 'Brandenburg', 'Bremen': 'Bremen',
    'Hamburg': 'Hamburg', 'Hesse': 'Hessen', 'Lower Saxony': 'Niedersachsen',
    'Mecklenburg-Vorpommern': 'Mecklenburg-Vorpommern',
    'North Rhine-Westphalia': 'Nordrhein-Westfalen',
    'Rhineland-Palatinate': 'Rheinland-Pfalz', 'Saarland': 'Saarland',
    'Saxony': 'Sachsen', 'Saxony-Anhalt': 'Sachsen-Anhalt',
    'Schleswig-Holstein': 'Schleswig-Holstein', 'Thuringia': 'Thüringen',
}
germany_geojson = None
try:
    resp = requests.get(GEOJSON_URL, timeout=8)
    if resp.status_code == 200:
        germany_geojson = resp.json()
except Exception:
    pass

# ─────────────────────────────────────────────────────────────
# CHART HELPERS
# ─────────────────────────────────────────────────────────────
BASE = dict(
    paper_bgcolor='rgba(0,0,0,0)',
    plot_bgcolor='rgba(0,0,0,0)',
    font=dict(family=FONT, color=TEXT_DARK, size=11),
    margin=dict(l=8, r=8, t=32, b=8),
)

def hbar(labels, values, colors, title=''):
    order = sorted(range(len(values)), key=lambda i: values[i])
    lbl = [labels[i] for i in order]
    val = [values[i] for i in order]
    col = colors if isinstance(colors, str) else [colors[i] for i in order]
    fig = go.Figure(go.Bar(
        x=val, y=lbl, orientation='h',
        marker=dict(color=col, line=dict(width=0)),
        text=[f'{v:,}' for v in val],
        textposition='outside',
        textfont=dict(size=10, color=TEXT_MED),
        hovertemplate='<b>%{y}</b><br>%{x:,} jobs<extra></extra>',
        cliponaxis=False,
    ))
    fig.update_layout(
        **BASE,
        title=dict(text=title, font=dict(size=12, color=TEXT_MED), x=0, pad=dict(b=8)),
        xaxis=dict(showgrid=True, gridcolor=BORDER, zeroline=False, showticklabels=False),
        yaxis=dict(showgrid=False, tickfont=dict(size=10)),
        bargap=0.3,
    )
    return fig

def donut(labels, values, colors, title='', center_text=''):
    fig = go.Figure(go.Pie(
        labels=labels, values=values, hole=0.58,
        marker=dict(colors=colors, line=dict(color=CARD, width=2)),
        textinfo='percent',
        textfont=dict(size=11),
        hovertemplate='<b>%{label}</b><br>%{value:,} jobs (%{percent})<extra></extra>',
        sort=False,
        direction='clockwise',
    ))
    if center_text:
        fig.add_annotation(
            text=center_text, x=0.5, y=0.5, showarrow=False,
            font=dict(size=13, color=TEXT_DARK, family=FONT),
            xanchor='center', yanchor='middle',
        )
    fig.update_layout(
        **BASE,
        title=dict(text=title, font=dict(size=12, color=TEXT_MED), x=0),
        showlegend=True,
        legend=dict(orientation='v', x=1.01, y=0.5,
                    font=dict(size=10), bgcolor='rgba(0,0,0,0)',
                    itemsizing='constant'),
        margin=dict(l=8, r=130, t=32, b=8),
    )
    return fig

def build_map():
    states = list(state_data.keys())
    counts = [state_data[s][0] for s in states]
    lats   = [state_data[s][1] for s in states]
    lons   = [state_data[s][2] for s in states]
    tops   = [state_data[s][3] for s in states]

    hover_text = [
        f'<b>{s}</b><br>'
        f'Total Jobs: {state_data[s][0]:,}<br>'
        f'<br><i>Top ISCO-4 Roles:</i><br>'
        f'1. {tops[i][0]}<br>'
        f'2. {tops[i][1]}<br>'
        f'3. {tops[i][2]}'
        for i, s in enumerate(states)
    ]

    if germany_geojson:
        de_names = [STATE_DE.get(s, s) for s in states]
        df_map = pd.DataFrame({'name': de_names, 'state': states,
                               'count': counts, 'hover': hover_text})
        fig = px.choropleth(
            df_map, geojson=germany_geojson,
            locations='name', featureidkey='properties.name',
            color='count',
            color_continuous_scale=[[0, TEAL_LIGHT], [0.25, '#7FBFBF'],
                                    [0.6, TEAL], [1, TEAL_DARK]],
            custom_data=['state', 'count', 'hover'],
        )
        fig.update_traces(
            hovertemplate='%{customdata[2]}<extra></extra>',
            marker_line_color='white',
            marker_line_width=1.5,
        )
        fig.update_geos(fitbounds='locations', visible=False,
                        bgcolor='rgba(0,0,0,0)')
        fig.update_coloraxes(
            colorbar=dict(title='Jobs', tickformat=',d',
                          len=0.65, thickness=12,
                          title_font=dict(size=10, color=TEXT_MED),
                          tickfont=dict(size=9, color=TEXT_MED)))
    else:
        fig = go.Figure(go.Scattergeo(
            lat=lats, lon=lons,
            text=hover_text, hoverinfo='text',
            mode='markers',
            marker=dict(
                size=[c / max(counts) * 50 + 12 for c in counts],
                color=counts,
                colorscale=[[0, TEAL_LIGHT], [0.3, TEAL], [1, TEAL_DARK]],
                showscale=True,
                colorbar=dict(title='Jobs', tickformat=',d',
                              len=0.6, thickness=12,
                              title_font=dict(size=10)),
                line=dict(color='white', width=1.2),
                opacity=0.88,
            ),
            showlegend=False,
        ))
        fig.update_geos(
            scope='europe', center=dict(lat=51.2, lon=10.4),
            projection_scale=5.8,
            showland=True, landcolor='#F0F8F8',
            showocean=True, oceancolor='#EAF3F5',
            showcountries=True, countrycolor=BORDER,
            showcoastlines=False,
            bgcolor='rgba(0,0,0,0)',
        )

    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(family=FONT, size=11),
        margin=dict(l=0, r=0, t=0, b=0),
        height=480,
    )
    return fig

# ─────────────────────────────────────────────────────────────
# UI COMPONENTS
# ─────────────────────────────────────────────────────────────
def card(children, mb=20, p='22px 24px'):
    return html.Div(children, style={
        'background': CARD, 'borderRadius': '12px',
        'padding': p, 'marginBottom': f'{mb}px',
        'boxShadow': '0 1px 6px rgba(15,46,46,0.07)',
        'border': f'1px solid {BORDER}',
    })

def card_title(text, subtitle=None):
    return html.Div([
        html.Div(text, style={
            'fontSize': '13px', 'fontWeight': '600',
            'color': TEXT_DARK, 'fontFamily': FONT,
        }),
        html.Div(subtitle, style={
            'fontSize': '11px', 'color': TEXT_LIGHT, 'marginTop': '2px',
        }) if subtitle else None,
    ], style={'marginBottom': '16px', 'paddingBottom': '12px',
              'borderBottom': f'1px solid {BORDER}'})

def kpi(value, label, sub='', accent=TEAL):
    return html.Div([
        html.Div(style={
            'width': '4px', 'background': accent,
            'borderRadius': '4px', 'marginRight': '14px', 'minHeight': '52px',
        }),
        html.Div([
            html.Div(value, style={
                'fontSize': '26px', 'fontWeight': '700',
                'color': TEXT_DARK, 'fontFamily': FONT, 'lineHeight': '1.1',
            }),
            html.Div(label, style={
                'fontSize': '11px', 'color': TEXT_MED,
                'marginTop': '3px', 'fontWeight': '500',
                'textTransform': 'uppercase', 'letterSpacing': '0.05em',
            }),
            html.Div(sub, style={
                'fontSize': '10px', 'color': TEXT_LIGHT, 'marginTop': '2px',
            }) if sub else None,
        ]),
    ], style={
        'background': CARD, 'borderRadius': '10px',
        'padding': '16px 18px', 'display': 'flex', 'alignItems': 'center',
        'flex': '1', 'minWidth': '180px',
        'boxShadow': '0 1px 6px rgba(15,46,46,0.07)',
        'border': f'1px solid {BORDER}',
    })

def note(text):
    return html.Div(text, style={
        'background': GOLD_LIGHT, 'borderLeft': f'3px solid {GOLD}',
        'padding': '10px 14px', 'borderRadius': '0 6px 6px 0',
        'fontSize': '11px', 'color': '#7A5A00', 'marginBottom': '20px',
        'lineHeight': '1.6',
    })

def row(*children, gap=20):
    return html.Div(list(children), style={
        'display': 'flex', 'gap': f'{gap}px',
        'flexWrap': 'wrap', 'marginBottom': f'{gap}px',
    })

def col(*children, flex=1, min_w=300):
    return html.Div(list(children), style={
        'flex': str(flex), 'minWidth': f'{min_w}px',
    })

def graph(fig, height=320):
    return dcc.Graph(
        figure=fig,
        config={'displayModeBar': False, 'responsive': True},
        style={'height': f'{height}px'},
    )

# ─────────────────────────────────────────────────────────────
# TAB CONTENT
# ─────────────────────────────────────────────────────────────
def tab_overview():
    hc_pct = round(HC_JOBS / TOTAL * 100, 1)

    fig_split = donut(
        ['Healthcare Roles', 'Non-Healthcare Roles'],
        [HC_JOBS, NON_HC_JOBS],
        [TEAL, '#C5DEDE'],
        title='Healthcare vs Non-Healthcare',
        center_text=f'{hc_pct}%<br>Healthcare',
    )

    isic_labels = [d[0] for d in isic_data]
    isic_vals   = [d[1] for d in isic_data]
    isic_cols   = [ISIC_COLOR.get(l, TEAL) for l in isic_labels]
    fig_isic = hbar(isic_labels, isic_vals, isic_cols,
                    title='Jobs by ISIC Rev. 4 Employer Category')

    return html.Div([
        # KPIs
        row(
            kpi(f'{TOTAL:,}', 'Total Job Postings', 'StepStone Germany', TEAL),
            kpi(f'{HC_JOBS:,}', 'Healthcare Roles', f'{hc_pct}% of all postings', GOLD),
            kpi(f'{EMPLOYERS:,}', 'Unique Employers', 'Genuine employers only', TEAL_DARK),
            kpi(f'{STATES}', 'Federal States', 'All 16 German states', GOLD),
            gap=14,
        ),
        # Banner
        html.Div([
            html.Span('Data Period: ', style={'fontWeight': '600'}),
            html.Span(f'{DATE_RANGE}   '),
            html.Span('Source: ', style={'fontWeight': '600'}),
            html.Span('StepStone Germany   '),
            html.Span('Classification: ', style={'fontWeight': '600'}),
            html.Span('ISCO-08 (ILO)  ·  ISIC Rev. 4 (UN Statistics Division)'),
        ], style={
            'background': TEAL_LIGHT, 'border': f'1px solid {BORDER}',
            'borderRadius': '8px', 'padding': '10px 16px',
            'fontSize': '11px', 'color': TEXT_MED, 'marginBottom': '20px',
        }),
        # Charts
        row(
            col(
                card([
                    card_title('Role Type Breakdown'),
                    graph(fig_split, 280),
                ]),
                flex=1, min_w=280,
            ),
            col(
                card([
                    card_title('Jobs by Employer Category',
                               'Classified using ISIC Rev. 4 — UN International Standard'),
                    graph(fig_isic, 280),
                ]),
                flex=2, min_w=360,
            ),
        ),
        note(
            '64.9% of postings carry no state-level location on StepStone. '
            'Geographic analysis uses the 35.1% of records with a state tag (n = 10,099). '
            'meinestadt.de (1,435 postings) and EASYFITNESS Franchise GmbH (868 postings) '
            'are flagged as non-genuine and excluded from employer-level analysis.'
        ),
    ])


def tab_job_categories():
    # Healthcare only
    hc_cats = [(l, v) for l, v in job_cats if l != 'Non-Healthcare']
    fig_hc = hbar([x[0] for x in hc_cats], [x[1] for x in hc_cats],
                  TEAL, 'Healthcare Role Categories (ISCO-3)')

    # All incl non-HC
    all_cols = [TEAL if 'Non-Healthcare' not in l else '#AECECE'
                for l, _ in job_cats]
    fig_all = hbar([x[0] for x in job_cats], [x[1] for x in job_cats],
                   all_cols, 'All Categories including Non-Healthcare (ISCO-3)')

    # Top 20 ISCO-4
    i4_labels = [f"{d[0]} ({d[1]})" for d in isco4_data]
    i4_vals   = [d[2] for d in isco4_data]
    fig_isco4 = hbar(i4_labels, i4_vals, GOLD, 'Top 20 ISCO-4 Unit Groups by Volume')

    # Top 20 titles
    fig_titles = hbar([x[0] for x in titles_data],
                      [x[1] for x in titles_data],
                      TEAL_DARK, 'Top 20 Job Titles by Volume')

    return html.Div([
        row(
            col(card([card_title('Healthcare Role Categories',
                                 'ISCO-2 groups 22, 32, 53 only'),
                      graph(fig_hc, 380)]), flex=1, min_w=320),
            col(card([card_title('All Categories incl. Non-Healthcare',
                                 'Full ISCO-3 distribution'),
                      graph(fig_all, 380)]), flex=1, min_w=320),
        ),
        row(
            col(card([card_title('Top 20 ISCO-4 Unit Groups',
                                 'Official ILO unit group classifications with codes'),
                      graph(fig_isco4, 480)]), flex=1, min_w=320),
            col(card([card_title('Top 20 Job Titles',
                                 'Standardised titles from StepStone listings'),
                      graph(fig_titles, 480)]), flex=1, min_w=320),
        ),
    ])


def tab_employers():
    isic_labels = [d[0] for d in isic_data]
    isic_vals   = [d[1] for d in isic_data]
    isic_cols   = [ISIC_COLOR.get(l, TEAL) for l in isic_labels]

    fig_donut = donut(
        isic_labels, isic_vals, isic_cols,
        title='Employer Category Distribution',
    )

    emp_labels = [d[0] for d in employer_data]
    emp_vals   = [d[1] for d in employer_data]
    emp_cols   = [ISIC_COLOR.get(d[2], TEAL) for d in employer_data]
    fig_emp = hbar(emp_labels, emp_vals, emp_cols,
                   'Top 15 Genuine Hiring Companies')

    legend_items = [
        html.Div([
            html.Div(style={
                'width': '10px', 'height': '10px', 'borderRadius': '2px',
                'background': ISIC_COLOR.get(cat, TEAL),
                'marginRight': '7px', 'flexShrink': '0',
            }),
            html.Span(cat.split(' (ISIC')[0],
                      style={'fontSize': '11px', 'color': TEXT_MED}),
        ], style={'display': 'flex', 'alignItems': 'center', 'marginBottom': '6px'})
        for cat in ISIC_COLOR
    ]

    isic_ref = [
        ('8610', 'Hospital activities'),
        ('8620', 'Medical and dental practice activities'),
        ('8690', 'Other human health activities'),
        ('8710', 'Residential nursing care facilities'),
        ('8720', 'Residential care — mental health & rehabilitation'),
        ('7820', 'Temporary employment agency activities'),
    ]

    return html.Div([
        row(
            col(
                card([
                    card_title('Distribution by ISIC Rev. 4 Category',
                               'UN International Standard Industrial Classification'),
                    graph(fig_donut, 300),
                ]),
                flex=1, min_w=280,
            ),
            col(
                html.Div([
                    card([
                        card_title('Category Legend'),
                        *legend_items,
                    ], mb=16),
                    card([
                        html.Div('ISIC Rev. 4 Code Reference',
                                 style={'fontSize': '12px', 'fontWeight': '600',
                                        'color': TEXT_DARK, 'marginBottom': '10px'}),
                        *[html.Div([
                            html.Span(code, style={
                                'fontFamily': 'monospace', 'fontWeight': '700',
                                'color': TEAL, 'marginRight': '8px', 'fontSize': '12px',
                                'minWidth': '36px', 'display': 'inline-block',
                            }),
                            html.Span(name, style={'fontSize': '11px', 'color': TEXT_MED}),
                        ], style={'marginBottom': '5px', 'display': 'flex'})
                          for code, name in isic_ref],
                    ]),
                ]),
                flex=1, min_w=240,
            ),
        ),
        card([
            card_title('Top 15 Genuine Hiring Companies',
                       'Bars coloured by ISIC category · Excludes aggregator portals'),
            graph(fig_emp, 460),
        ]),
        note(
            'Excluded from this analysis: meinestadt.de (job aggregator, 1,435 postings) '
            'and EASYFITNESS Franchise GmbH (fitness sector, 868 postings). '
            'Both are flagged in the full dataset with Employer_Flag = "Aggregator/Non-HC".'
        ),
    ])


def tab_geography():
    fig_map = build_map()

    state_sorted = sorted(state_data.keys(),
                          key=lambda s: state_data[s][0], reverse=False)
    fig_bar = hbar(
        state_sorted,
        [state_data[s][0] for s in state_sorted],
        TEAL,
        'Job Volume by Federal State',
    )

    # State table rows
    state_rows = []
    for i, s in enumerate(sorted(state_data, key=lambda x: state_data[x][0], reverse=True)):
        cnt, _, _, top3 = state_data[s]
        bg = CARD if i % 2 == 0 else TEAL_LIGHT
        state_rows.append(html.Div([
            html.Span(s,       style={'flex': '1.4', 'fontWeight': '500'}),
            html.Span(f'{cnt:,}', style={'flex': '0.5', 'color': TEAL, 'fontWeight': '700'}),
            html.Span(top3[0], style={'flex': '2', 'color': TEXT_MED}),
            html.Span(top3[1], style={'flex': '2', 'color': TEXT_MED}),
            html.Span(top3[2], style={'flex': '2', 'color': TEXT_MED}),
        ], style={
            'display': 'flex', 'gap': '12px',
            'padding': '9px 14px', 'background': bg,
            'fontSize': '11px', 'color': TEXT_DARK,
            'borderBottom': f'1px solid {BORDER}',
        }))

    return html.Div([
        note(
            f'Geographic data covers {34.8}% of postings (n = 10,099 of 29,045). '
            '64.9% of StepStone postings carry no state-level location tag. '
            'Results are indicative, not exhaustive, for any given state. '
            'Hover over states to see volume and top 3 ISCO-4 roles.'
        ),
        row(
            col(
                card([
                    card_title('Germany — Healthcare Jobs by State',
                               'Hover for state details and top roles'),
                    graph(fig_map, 480),
                ]),
                flex=2, min_w=380,
            ),
            col(
                card([
                    card_title('State Rankings', 'By total job postings (state-tagged only)'),
                    graph(fig_bar, 480),
                ]),
                flex=1, min_w=260,
            ),
        ),
        card([
            card_title('State-level Detail — Top ISCO-4 Roles',
                       'Ranked by total job postings (state-tagged subset)'),
            # Header
            html.Div([
                html.Span('State',   style={'flex': '1.4', 'fontWeight': '600'}),
                html.Span('Jobs',    style={'flex': '0.5', 'fontWeight': '600'}),
                html.Span('Top Role', style={'flex': '2', 'fontWeight': '600'}),
                html.Span('2nd Role', style={'flex': '2', 'fontWeight': '600'}),
                html.Span('3rd Role', style={'flex': '2', 'fontWeight': '600'}),
            ], style={
                'display': 'flex', 'gap': '12px', 'padding': '9px 14px',
                'background': TEAL_LIGHT, 'borderRadius': '6px 6px 0 0',
                'fontSize': '11px', 'fontWeight': '600', 'color': TEXT_DARK,
            }),
            html.Div(state_rows, style={
                'borderRadius': '0 0 8px 8px',
                'border': f'1px solid {BORDER}',
                'overflow': 'hidden',
            }),
        ]),
    ])


def tab_glossary():
    isco3_entries = [
        (221, 'Medical Doctors',
         'Diagnose, treat and prevent illness, disease and injury using procedures of modern medicine. '
         'Includes Generalist Medical Practitioners (2211) and Specialist Medical Practitioners (2212). '
         'Requires university-level medical degree plus postgraduate clinical training.'),
        (222, 'Nursing and Midwifery Professionals',
         'Provide treatment, support and care for people in need of nursing care. Plan and manage patient care, '
         'supervise other health care workers. Requires higher education qualification in nursing or midwifery.'),
        (226, 'Other Health Professionals',
         'Physiotherapists (2264), Pharmacists (2262), Dentists (2261), Dieticians & Nutritionists (2265), '
         'Audiologists & Speech Therapists (2266), Optometrists (2267), Health Professionals NEC (2269).'),
        (321, 'Medical and Pharmaceutical Technicians',
         'Medical imaging & therapeutic equipment technicians (3211), pathology laboratory technicians (3212), '
         'pharmaceutical technicians (3213), medical and dental prosthetic technicians (3214).'),
        (322, 'Nursing and Midwifery Associate Professionals',
         'Provide basic nursing and midwifery care. Implement care plans established by professionals. '
         'Includes nursing associate professionals (3221) and midwifery associate professionals (3222).'),
        (325, 'Other Health Associate Professionals',
         'Dental assistants (3251), medical records technicians (3252), community health workers (3253), '
         'physiotherapy technicians (3255), medical assistants (3256), ambulance workers (3258), '
         'health associate professionals NEC (3259).'),
        (531, 'Child Care Workers and Teachers Aides',
         'Provide care, supervision and support for children. Assist teachers in classroom settings. '
         'Includes child care workers (5311) and teachers aides (5312).'),
        (532, 'Personal Care Workers in Health Services',
         'Provide routine personal care in health and residential settings. Includes health care assistants (5321), '
         'home-based personal care workers (5322), and personal care workers NEC (5329).'),
    ]

    isic_entries = [
        ('8610', 'Hospitals & Acute Care',
         'Inpatient hospital activities: general hospitals, university hospitals, '
         'acute specialist care centres, rehabilitation hospitals.'),
        ('8620', 'Medical & Dental Practice',
         'Activities of general and specialist medical practitioners, dental practices, '
         'outpatient clinics, physiotherapy practices, and other ambulatory health care.'),
        ('8690', 'Other Health Services & Industry',
         'Home nursing, occupational therapy, medical laboratory services, '
         'ambulance services, health education, and medical equipment suppliers.'),
        ('8710', 'Residential & Long-term Care',
         'Residential nursing care facilities providing nursing, supervisory and other care. '
         'Includes nursing homes, elderly residential care, and convalescent homes.'),
        ('8720', 'Mental Health & Rehabilitation',
         'Residential care for mental health, substance abuse and developmental disabilities. '
         'Includes psychiatric residential care and drug rehabilitation centres.'),
        ('7820', 'Staffing & Recruitment',
         'Temporary employment agency activities, healthcare staffing agencies, '
         'locum agencies, and personnel placement services for the health sector.'),
    ]

    def gloss_row(code, name, desc, accent=TEAL):
        return html.Div([
            html.Div([
                html.Span(str(code), style={
                    'background': accent, 'color': 'white',
                    'padding': '2px 8px', 'borderRadius': '4px',
                    'fontSize': '11px', 'fontWeight': '700',
                    'fontFamily': 'monospace', 'marginRight': '10px',
                }),
                html.Span(name, style={
                    'fontWeight': '600', 'fontSize': '13px', 'color': TEXT_DARK,
                }),
            ], style={'marginBottom': '5px'}),
            html.Div(desc, style={
                'fontSize': '11px', 'color': TEXT_MED,
                'lineHeight': '1.6', 'paddingLeft': '2px',
            }),
        ], style={
            'padding': '14px 16px',
            'borderBottom': f'1px solid {BORDER}',
        })

    method_items = [
        ('Data Source',
         'Job postings scraped from StepStone Germany (stepstone.de). '
         'Collection period: 31 January – 10 March 2026. Total records: 29,045.'),
        ('Occupational Classification',
         'All job titles classified to ISCO-08 at unit group level (4-digit) using WHO '
         'healthcare worker classification guidelines. ISCO-2 groups 22 (Health Professionals), '
         '32 (Health Associate Professionals) and 53 (Personal Care Workers) define the core healthcare workforce.'),
        ('Employer Classification',
         'Employers classified using ISIC Rev. 4 codes based on company name, sector context '
         'and job content. meinestadt.de (aggregator, 1,435 postings) and EASYFITNESS Franchise GmbH '
         '(fitness sector, 868 postings) are flagged and excluded from employer analyses.'),
        ('Geographic Coverage',
         '35.1% of postings (n = 10,099) carry an explicit federal state tag. '
         'The remaining 64.9% do not specify a location on StepStone. '
         'Geographic analysis is based on the tagged subset and is indicative, not exhaustive.'),
        ('Visa & International Hiring',
         'Systematic check of Requirements, Description and Benefits fields found negligible '
         'mention of visa sponsorship or overseas hiring (< 0.1% of postings). '
         'This is itself a signal: German healthcare employers are not yet prominently '
         'advertising international hiring on StepStone.'),
    ]

    return html.Div([
        card([
            card_title(
                'ISCO-08 — Healthcare Role Categories (ISCO-3 Level)',
                'International Standard Classification of Occupations, 2008 — ILO',
            ),
            html.Div(
                [gloss_row(c, n, d, TEAL) for c, n, d in isco3_entries],
                style={'borderRadius': '8px', 'overflow': 'hidden',
                       'border': f'1px solid {BORDER}'},
            ),
        ]),
        card([
            card_title(
                'ISIC Rev. 4 — Employer Categories',
                'International Standard Industrial Classification, Rev. 4 — UN Statistics Division',
            ),
            html.Div(
                [gloss_row(c, n, d, GOLD) for c, n, d in isic_entries],
                style={'borderRadius': '8px', 'overflow': 'hidden',
                       'border': f'1px solid {BORDER}'},
            ),
        ]),
        card([
            card_title('Data Methodology & Notes'),
            *[html.Div([
                html.Div(t, style={'fontWeight': '600', 'fontSize': '12px',
                                   'color': TEXT_DARK, 'marginBottom': '4px'}),
                html.Div(b, style={'fontSize': '11px', 'color': TEXT_MED,
                                   'lineHeight': '1.7', 'marginBottom': '16px'}),
            ]) for t, b in method_items],
        ]),
    ])

# ─────────────────────────────────────────────────────────────
# APP LAYOUT
# ─────────────────────────────────────────────────────────────
app = dash.Dash(
    __name__,
    title='GATI Healthcare Dashboard',
    suppress_callback_exceptions=True,
    external_stylesheets=[
        ('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700'
         '&family=DM+Sans:wght@300;400;500;600&display=swap'),
    ],
)
server = app.server

TAB_STYLE = {
    'fontFamily': FONT, 'fontSize': '13px', 'fontWeight': '500',
    'color': TEXT_MED, 'backgroundColor': CARD,
    'borderTop': 'none', 'borderLeft': 'none', 'borderRight': 'none',
    'borderBottom': '2px solid transparent',
    'padding': '12px 22px',
}
TAB_SELECTED = {
    **TAB_STYLE,
    'color': TEAL, 'fontWeight': '600',
    'borderBottom': f'2px solid {TEAL}',
    'backgroundColor': CARD,
}

app.layout = html.Div([
    # HEADER
    html.Div([
        html.Div([
            html.Div([
                html.Div([
                    html.Div('GATI', style={
                        'fontSize': '24px', 'fontWeight': '700',
                        'color': 'white', 'fontFamily': FONT,
                        'letterSpacing': '-0.5px', 'lineHeight': '1',
                    }),
                    html.Div('Global Access to Talent from India', style={
                        'fontSize': '9px', 'color': 'rgba(255,255,255,0.7)',
                        'letterSpacing': '0.06em', 'marginTop': '2px',
                        'textTransform': 'uppercase',
                    }),
                ], style={
                    'borderRight': '1px solid rgba(255,255,255,0.2)',
                    'paddingRight': '18px', 'marginRight': '18px',
                }),
                html.Div([
                    html.Div('German Healthcare Labour Market Analysis', style={
                        'fontSize': '15px', 'fontWeight': '600',
                        'color': 'white', 'fontFamily': FONT,
                    }),
                    html.Div('StepStone Germany  ·  29,045 Job Postings  ·  Jan – Mar 2026',
                             style={'fontSize': '11px',
                                    'color': 'rgba(255,255,255,0.6)',
                                    'marginTop': '2px'}),
                ]),
            ], style={'display': 'flex', 'alignItems': 'center'}),
            html.Div([
                html.Span('ISCO-08', style={
                    'fontSize': '10px', 'fontWeight': '700',
                    'background': 'rgba(255,255,255,0.15)',
                    'color': 'white', 'padding': '4px 9px',
                    'borderRadius': '4px', 'marginRight': '6px',
                }),
                html.Span('ISIC Rev. 4', style={
                    'fontSize': '10px', 'fontWeight': '700',
                    'background': f'{GOLD}40',
                    'color': GOLD, 'padding': '4px 9px',
                    'borderRadius': '4px',
                }),
            ], style={'display': 'flex', 'alignItems': 'center'}),
        ], style={
            'maxWidth': '1280px', 'margin': '0 auto', 'padding': '0 32px',
            'display': 'flex', 'justifyContent': 'space-between',
            'alignItems': 'center', 'height': '60px',
        }),
    ], style={
        'background': TEAL_DARK,
        'borderBottom': f'3px solid {GOLD}',
        'position': 'sticky', 'top': '0', 'zIndex': '200',
    }),

    # TABS + CONTENT
    html.Div([
        dcc.Tabs(
            id='main-tabs',
            value='overview',
            children=[
                dcc.Tab(label='Overview',             value='overview',   style=TAB_STYLE, selected_style=TAB_SELECTED),
                dcc.Tab(label='Job Categories',       value='categories', style=TAB_STYLE, selected_style=TAB_SELECTED),
                dcc.Tab(label='Employer Analysis',    value='employers',  style=TAB_STYLE, selected_style=TAB_SELECTED),
                dcc.Tab(label='Geography',            value='geography',  style=TAB_STYLE, selected_style=TAB_SELECTED),
                dcc.Tab(label='Glossary & Methodology', value='glossary', style=TAB_STYLE, selected_style=TAB_SELECTED),
            ],
            style={
                'borderBottom': f'1px solid {BORDER}',
                'backgroundColor': CARD,
            },
            colors={'border': BORDER, 'primary': TEAL, 'background': CARD},
        ),
        html.Div(
            id='tab-content',
            style={
                'maxWidth': '1280px', 'margin': '0 auto',
                'padding': '28px 32px 60px',
            },
        ),
    ], style={'background': BG, 'minHeight': 'calc(100vh - 63px)'}),

], style={'fontFamily': FONT, 'color': TEXT_DARK})

# ─────────────────────────────────────────────────────────────
# CALLBACK
# ─────────────────────────────────────────────────────────────
@app.callback(
    Output('tab-content', 'children'),
    Input('main-tabs', 'value'),
)
def render_tab(tab):
    try:
        builders = {
            'overview':   tab_overview,
            'categories': tab_job_categories,
            'employers':  tab_employers,
            'geography':  tab_geography,
            'glossary':   tab_glossary,
        }
        return builders.get(tab, tab_overview)()
    except Exception as e:
        return html.Div([
            html.Div('Error loading this tab', style={
                'color': '#cc0000', 'fontWeight': '600', 'marginBottom': '8px',
            }),
            html.Pre(str(e), style={
                'fontSize': '11px', 'color': TEXT_MED,
                'background': '#fff5f5', 'padding': '12px',
                'borderRadius': '6px', 'overflowX': 'auto',
            }),
        ], style={'padding': '40px'})


if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=8050)
