import dash
from dash import dcc, html, Input, Output, dash_table
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import requests
import json

# ─────────────────────────────────────────────────────────────
# BRAND & THEME
# ─────────────────────────────────────────────────────────────
TEAL       = '#1A7B7A'
TEAL_DARK  = '#0F5B5A'
TEAL_LIGHT = '#E5F2F2'
GOLD       = '#D4940A'
GOLD_LIGHT = '#FBF0D8'
BG         = '#F2F6F6'
CARD       = '#FFFFFF'
TEXT_DARK  = '#0F2E2E'
TEXT_MED   = '#3D6060'
TEXT_LIGHT = '#7A9C9C'
BORDER     = '#D4E5E5'

CHART_COLORS = [TEAL, GOLD, '#2D9B9A', '#E8A820', '#0F5B5A',
                '#B8D9D9', '#7FB5B5', '#F5C842', '#5AAEAE', '#A07808']

ISIC_COLORS = {
    'Residential & Long-term Care (ISIC 8710)': '#1A7B7A',
    'Medical & Dental Practice (ISIC 8620)':    '#D4940A',
    'Other Health Services & Industry (ISIC 8690)': '#2D9B9A',
    'Hospitals & Acute Care (ISIC 8610)':       '#E8A820',
    'Staffing & Recruitment (ISIC 7820)':       '#0F5B5A',
    'Mental Health & Rehabilitation (ISIC 8720)':'#B8D9D9',
}

# ─────────────────────────────────────────────────────────────
# ALL PRE-AGGREGATED DATA
# ─────────────────────────────────────────────────────────────

TOTAL_JOBS        = 29_045
HEALTHCARE_JOBS   = 15_724
NON_HC_JOBS       = 13_321
UNIQUE_EMPLOYERS  = 10_657
STATES_COVERED    = 16
DATE_RANGE        = "31 Jan – 10 Mar 2026"
PCT_STATE_TAGGED  = 34.8

job_categories_raw = [
    ('Non-Healthcare',                                    10890),
    ('Nursing & Midwifery Professionals (ISCO 222)',       4207),
    ('Other Health Associates (ISCO 325)',                 3049),
    ('Other Healthcare (ISCO 22x/32x/53x)',               2580),
    ('Other Health Professionals (ISCO 226)',              2312),
    ('Personal Care Workers (ISCO 532)',                   2196),
    ('Medical Doctors (ISCO 221)',                         1663),
    ('Nursing & Midwifery Associates (ISCO 322)',           909),
    ('Medical & Pharma Technicians (ISCO 321)',             870),
    ('Child Care & Teachers Aides (ISCO 531)',              369),
]

top20_isco4_raw = [
    ('Nursing Professionals',                                    2221, 4178),
    ('Social Work & Counselling Professionals',                  2635, 1896),
    ('Specialist Medical Practitioners',                         2212, 1444),
    ('Medical Assistants',                                       3256, 1272),
    ('Health Care Assistants',                                   5321, 1193),
    ('Physiotherapists',                                         2264, 1067),
    ('Health Service Managers',                                  1342, 1067),
    ('Home-based Personal Care Workers',                         5322,  950),
    ('Nursing Associate Professionals',                          3221,  896),
    ('Dental Assistants and Therapists',                         3251,  775),
    ('Sports, Recreation & Cultural Centre Managers',            1431,  717),
    ('Early Childhood Educators',                                2342,  538),
    ('Health Professionals NEC',                                 2269,  464),
    ('Specialised Shop Salespersons',                            5223,  455),
    ('Health Associate Professionals NEC',                       3259,  449),
    ('Medical and Dental Prosthetic Technicians',                3214,  435),
    ('Cleaners & Helpers in Offices/Hotels',                     9112,  400),
    ('General Office Clerks',                                    4110,  393),
    ('Audiologists and Speech Therapists',                       2266,  321),
    ('Social Work Associate Professionals',                      3412,  311),
]

top20_titles_raw = [
    ('Physiotherapist',          918),
    ('Nursing Assistant',        732),
    ('Registered Nurse',         615),
    ('Medical Assistant',        590),
    ('Occupational Therapist',   454),
    ('Dental Assistant',         437),
    ('Geriatric Nurse',          310),
    ('Nursing Specialist',       217),
    ('Qualified Nurse',          200),
    ('Nursing Service Manager',  158),
    ('Nursing Professional',     153),
    ('Social Pedagogue',         124),
    ('Housekeeping Assistant',   122),
    ('Educator',                 116),
    ('Dental Technician',        112),
    ('Hairdresser',              110),
    ('Social Worker',            107),
    ('Cleaner',                  104),
    ('Early Childhood Educator',  98),
    ('Pedagogical Specialist',    98),
]

isic_raw = [
    ('Residential & Long-term Care (ISIC 8710)',     9383),
    ('Medical & Dental Practice (ISIC 8620)',         6216),
    ('Other Health Services & Industry (ISIC 8690)', 5131),
    ('Hospitals & Acute Care (ISIC 8610)',            3617),
    ('Staffing & Recruitment (ISIC 7820)',            2446),
    ('Mental Health & Rehabilitation (ISIC 8720)',    2252),
]

top15_employers_raw = [
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
    'Berlin':                  {'count': 1925, 'lat': 52.52, 'lon': 13.40,
        'top3': ['Nursing Professionals (2221)', 'Social Work & Counselling Professionals (2635)', 'Specialist Medical Practitioners (2212)']},
    'North Rhine-Westphalia':  {'count': 1755, 'lat': 51.43, 'lon': 7.66,
        'top3': ['Nursing Professionals (2221)', 'Nursing Associate Professionals (3221)', 'Medical Assistants (3256)']},
    'Bavaria':                 {'count': 1696, 'lat': 48.79, 'lon': 11.50,
        'top3': ['Nursing Professionals (2221)', 'Medical Assistants (3256)', 'Specialist Medical Practitioners (2212)']},
    'Hamburg':                 {'count':  955, 'lat': 53.55, 'lon': 10.00,
        'top3': ['Nursing Professionals (2221)', 'Social Work & Counselling Professionals (2635)', 'Medical Assistants (3256)']},
    'Baden-Württemberg':       {'count':  705, 'lat': 48.66, 'lon': 9.35,
        'top3': ['Nursing Professionals (2221)', 'Medical Assistants (3256)', 'Specialist Medical Practitioners (2212)']},
    'Lower Saxony':            {'count':  580, 'lat': 52.64, 'lon': 9.84,
        'top3': ['Nursing Professionals (2221)', 'Medical Assistants (3256)', 'Specialist Medical Practitioners (2212)']},
    'Saxony':                  {'count':  541, 'lat': 51.11, 'lon': 13.20,
        'top3': ['Nursing Professionals (2221)', 'Specialist Medical Practitioners (2212)', 'Physiotherapists (2264)']},
    'Hesse':                   {'count':  382, 'lat': 50.65, 'lon': 9.16,
        'top3': ['Nursing Professionals (2221)', 'Specialist Medical Practitioners (2212)', 'Social Work & Counselling Professionals (2635)']},
    'Bremen':                  {'count':  256, 'lat': 53.08, 'lon': 8.81,
        'top3': ['Nursing Professionals (2221)', 'Social Work & Counselling Professionals (2635)', 'Health Service Managers (1342)']},
    'Brandenburg':             {'count':  251, 'lat': 52.41, 'lon': 13.52,
        'top3': ['Nursing Professionals (2221)', 'Specialist Medical Practitioners (2212)', 'Social Work & Counselling Professionals (2635)']},
    'Rhineland-Palatinate':    {'count':  221, 'lat': 50.12, 'lon': 7.31,
        'top3': ['Nursing Professionals (2221)', 'Specialist Medical Practitioners (2212)', 'Nursing Associate Professionals (3221)']},
    'Schleswig-Holstein':      {'count':  218, 'lat': 54.22, 'lon': 9.68,
        'top3': ['Nursing Professionals (2221)', 'Nursing Associate Professionals (3221)', 'Medical Assistants (3256)']},
    'Thuringia':               {'count':  216, 'lat': 50.88, 'lon': 11.03,
        'top3': ['Specialist Medical Practitioners (2212)', 'Nursing Professionals (2221)', 'Health Care Assistants (5321)']},
    'Saxony-Anhalt':           {'count':  198, 'lat': 51.88, 'lon': 11.70,
        'top3': ['Specialist Medical Practitioners (2212)', 'Nursing Professionals (2221)', 'Social Work & Counselling Professionals (2635)']},
    'Mecklenburg-Vorpommern':  {'count':  115, 'lat': 53.61, 'lon': 12.43,
        'top3': ['Nursing Professionals (2221)', 'Nursing Associate Professionals (3221)', 'Specialist Medical Practitioners (2212)']},
    'Saarland':                {'count':   85, 'lat': 49.40, 'lon': 7.02,
        'top3': ['Nursing Professionals (2221)', 'Social Work & Counselling Professionals (2635)', 'Early Childhood Educators (2342)']},
}

# ─────────────────────────────────────────────────────────────
# BUILD DATAFRAMES
# ─────────────────────────────────────────────────────────────
df_jobs   = pd.DataFrame(job_categories_raw, columns=['category', 'count'])
df_isco4  = pd.DataFrame(top20_isco4_raw, columns=['label', 'code', 'count'])
df_isco4['display'] = df_isco4['label'] + ' (' + df_isco4['code'].astype(str) + ')'
df_titles = pd.DataFrame(top20_titles_raw, columns=['title', 'count'])
df_isic   = pd.DataFrame(isic_raw, columns=['category', 'count'])
df_emp    = pd.DataFrame(top15_employers_raw, columns=['employer', 'count', 'category'])
df_state  = pd.DataFrame([
    {'state': k, 'count': v['count'], 'lat': v['lat'], 'lon': v['lon'],
     'top1': v['top3'][0], 'top2': v['top3'][1], 'top3': v['top3'][2]}
    for k, v in state_data.items()
]).sort_values('count', ascending=False)

# ─────────────────────────────────────────────────────────────
# FETCH GERMANY GEOJSON (for choropleth; fallback to bubble map)
# ─────────────────────────────────────────────────────────────
GEOJSON_URL = 'https://raw.githubusercontent.com/isellsoap/deutschlandGeoJSON/main/2_bundeslaender/4_niedrig.geo.json'
STATE_NAME_MAP = {
    'Baden-Württemberg': 'Baden-Württemberg',
    'Bavaria': 'Bayern', 'Berlin': 'Berlin',
    'Brandenburg': 'Brandenburg', 'Bremen': 'Bremen',
    'Hamburg': 'Hamburg', 'Hesse': 'Hessen',
    'Lower Saxony': 'Niedersachsen',
    'Mecklenburg-Vorpommern': 'Mecklenburg-Vorpommern',
    'North Rhine-Westphalia': 'Nordrhein-Westfalen',
    'Rhineland-Palatinate': 'Rheinland-Pfalz',
    'Saarland': 'Saarland', 'Saxony': 'Sachsen',
    'Saxony-Anhalt': 'Sachsen-Anhalt',
    'Schleswig-Holstein': 'Schleswig-Holstein',
    'Thuringia': 'Thüringen',
}

germany_geojson = None
try:
    r = requests.get(GEOJSON_URL, timeout=8)
    if r.status_code == 200:
        germany_geojson = r.json()
except Exception:
    pass

# ─────────────────────────────────────────────────────────────
# CHART BUILDERS
# ─────────────────────────────────────────────────────────────
CHART_LAYOUT = dict(
    paper_bgcolor='rgba(0,0,0,0)',
    plot_bgcolor='rgba(0,0,0,0)',
    font=dict(family='Outfit, sans-serif', color=TEXT_DARK),
    margin=dict(l=0, r=0, t=30, b=0),
    legend=dict(bgcolor='rgba(0,0,0,0)', font=dict(size=11)),
)

def hbar(df, x_col, y_col, color=TEAL, title='', text_auto=True):
    df = df.sort_values(x_col, ascending=True)
    fig = go.Figure(go.Bar(
        x=df[x_col], y=df[y_col], orientation='h',
        marker_color=color,
        marker_line_width=0,
        text=df[x_col].apply(lambda v: f'{v:,}'),
        textposition='outside',
        textfont=dict(size=11, color=TEXT_DARK),
        hovertemplate='<b>%{y}</b><br>Jobs: %{x:,}<extra></extra>',
    ))
    fig.update_layout(
        **CHART_LAYOUT,
        title=dict(text=title, font=dict(size=13, color=TEXT_MED), x=0),
        xaxis=dict(showgrid=True, gridcolor=BORDER, zeroline=False,
                   showticklabels=False, title=''),
        yaxis=dict(showgrid=False, title='', tickfont=dict(size=11)),
        bargap=0.35,
    )
    return fig

def donut(labels, values, colors, title=''):
    fig = go.Figure(go.Pie(
        labels=labels, values=values,
        hole=0.55,
        marker=dict(colors=colors, line=dict(color=CARD, width=2)),
        textinfo='percent',
        textfont=dict(size=11),
        hovertemplate='<b>%{label}</b><br>%{value:,} jobs (%{percent})<extra></extra>',
        sort=False,
    ))
    fig.update_layout(
        **CHART_LAYOUT,
        title=dict(text=title, font=dict(size=13, color=TEXT_MED), x=0),
        showlegend=True,
        legend=dict(orientation='v', x=1.02, y=0.5,
                    font=dict(size=10), bgcolor='rgba(0,0,0,0)'),
        margin=dict(l=0, r=120, t=30, b=0),
    )
    return fig

def build_map():
    hover = df_state.apply(
        lambda r: (f"<b>{r['state']}</b><br>"
                   f"Total Jobs: {r['count']:,}<br>"
                   f"<br><i>Top Roles:</i><br>"
                   f"1. {r['top1']}<br>"
                   f"2. {r['top2']}<br>"
                   f"3. {r['top3']}"),
        axis=1
    )

    if germany_geojson:
        df_map = df_state.copy()
        df_map['german_name'] = df_map['state'].map(STATE_NAME_MAP)
        fig = px.choropleth(
            df_map,
            geojson=germany_geojson,
            locations='german_name',
            featureidkey='properties.name',
            color='count',
            color_continuous_scale=[[0, TEAL_LIGHT], [0.3, TEAL], [1, TEAL_DARK]],
            custom_data=['state', 'count', 'top1', 'top2', 'top3'],
        )
        fig.update_traces(
            hovertemplate=(
                '<b>%{customdata[0]}</b><br>'
                'Total Jobs: %{customdata[1]:,}<br><br>'
                '<i>Top Roles:</i><br>'
                '1. %{customdata[2]}<br>'
                '2. %{customdata[3]}<br>'
                '3. %{customdata[4]}<extra></extra>'
            ),
            marker_line_color='white',
            marker_line_width=1.5,
        )
        fig.update_geos(
            fitbounds='locations', visible=False,
            bgcolor='rgba(0,0,0,0)',
        )
        fig.update_coloraxes(
            colorbar=dict(
                title='Jobs', tickformat=',d',
                len=0.6, thickness=12,
                title_font=dict(size=11),
            )
        )
    else:
        # Bubble map fallback
        fig = go.Figure()
        fig.add_trace(go.Scattergeo(
            lat=df_state['lat'], lon=df_state['lon'],
            text=hover,
            hoverinfo='text',
            mode='markers+text',
            textposition='top center',
            textfont=dict(size=9, color=TEXT_DARK),
            marker=dict(
                size=df_state['count'] / df_state['count'].max() * 50 + 10,
                color=df_state['count'],
                colorscale=[[0, TEAL_LIGHT], [0.3, TEAL], [1, TEAL_DARK]],
                showscale=True,
                colorbar=dict(title='Jobs', tickformat=',d', len=0.6),
                line=dict(color='white', width=1),
                opacity=0.85,
            ),
            showlegend=False,
        ))
        fig.update_geos(
            scope='europe',
            center=dict(lat=51.2, lon=10.4),
            projection_scale=5.5,
            showland=True, landcolor='#F5F9F9',
            showocean=True, oceancolor='#EAF3F5',
            showcountries=True, countrycolor=BORDER,
            showcoastlines=True, coastlinecolor=BORDER,
            bgcolor='rgba(0,0,0,0)',
        )

    fig.update_layout(
        **CHART_LAYOUT,
        geo=dict(bgcolor='rgba(0,0,0,0)'),
        margin=dict(l=0, r=0, t=0, b=0),
        height=520,
    )
    return fig

# ─────────────────────────────────────────────────────────────
# SHARED UI HELPERS
# ─────────────────────────────────────────────────────────────
def kpi_card(label, value, subtitle='', accent_color=TEAL):
    return html.Div([
        html.Div(style={'width': '4px', 'background': accent_color,
                        'borderRadius': '4px', 'marginRight': '14px',
                        'minHeight': '54px'}),
        html.Div([
            html.Div(value, style={'fontSize': '28px', 'fontWeight': '700',
                                   'color': TEXT_DARK, 'lineHeight': '1.1',
                                   'fontFamily': 'Outfit, sans-serif'}),
            html.Div(label, style={'fontSize': '12px', 'color': TEXT_MED,
                                   'marginTop': '3px', 'fontWeight': '500',
                                   'textTransform': 'uppercase',
                                   'letterSpacing': '0.05em'}),
            html.Div(subtitle, style={'fontSize': '11px', 'color': TEXT_LIGHT,
                                      'marginTop': '2px'}) if subtitle else None,
        ])
    ], style={
        'background': CARD, 'borderRadius': '10px',
        'padding': '18px 20px', 'display': 'flex', 'alignItems': 'center',
        'boxShadow': '0 1px 4px rgba(0,0,0,0.06)',
        'border': f'1px solid {BORDER}',
        'flex': '1',
    })

def section_card(title, children, subtitle=None):
    return html.Div([
        html.Div([
            html.Div(title, style={'fontSize': '14px', 'fontWeight': '600',
                                   'color': TEXT_DARK,
                                   'fontFamily': 'Outfit, sans-serif'}),
            html.Div(subtitle, style={'fontSize': '11px', 'color': TEXT_LIGHT,
                                      'marginTop': '2px'}) if subtitle else None,
        ], style={'marginBottom': '16px', 'paddingBottom': '12px',
                  'borderBottom': f'1px solid {BORDER}'}),
        *children,
    ], style={
        'background': CARD, 'borderRadius': '12px',
        'padding': '22px 24px',
        'boxShadow': '0 1px 4px rgba(0,0,0,0.06)',
        'border': f'1px solid {BORDER}',
        'marginBottom': '20px',
    })

def note_box(text):
    return html.Div(text, style={
        'background': GOLD_LIGHT, 'borderLeft': f'3px solid {GOLD}',
        'padding': '10px 14px', 'borderRadius': '0 6px 6px 0',
        'fontSize': '11px', 'color': '#7A5A00', 'marginTop': '12px',
    })

def glossary_row(code, name, description, color=TEAL):
    return html.Div([
        html.Div([
            html.Span(str(code), style={
                'background': color, 'color': 'white',
                'padding': '2px 8px', 'borderRadius': '4px',
                'fontSize': '11px', 'fontWeight': '700',
                'fontFamily': 'monospace', 'marginRight': '10px',
            }),
            html.Span(name, style={'fontWeight': '600', 'fontSize': '13px',
                                   'color': TEXT_DARK}),
        ], style={'marginBottom': '4px'}),
        html.Div(description, style={'fontSize': '12px', 'color': TEXT_MED,
                                     'lineHeight': '1.5', 'paddingLeft': '2px'}),
    ], style={
        'padding': '14px 16px',
        'borderBottom': f'1px solid {BORDER}',
        'background': CARD,
    })

# ─────────────────────────────────────────────────────────────
# TAB CONTENT BUILDERS
# ─────────────────────────────────────────────────────────────
def build_overview():
    hc_pct = round(HEALTHCARE_JOBS / TOTAL_JOBS * 100, 1)

    donut_fig = donut(
        ['Healthcare Roles', 'Non-Healthcare Roles'],
        [HEALTHCARE_JOBS, NON_HC_JOBS],
        [TEAL, '#D4E5E5'],
        title='Healthcare vs Non-Healthcare',
    )

    isic_fig = hbar(
        df_isic.sort_values('count', ascending=True),
        'count', 'category',
        color=[ISIC_COLORS.get(c, TEAL) for c in df_isic.sort_values('count', ascending=True)['category']],
        title='Jobs by Employer Category (ISIC Rev. 4)',
    )

    return html.Div([
        # KPI row
        html.Div([
            kpi_card('Total Job Postings', f'{TOTAL_JOBS:,}', f'Source: StepStone Germany', TEAL),
            kpi_card('Healthcare Roles', f'{HEALTHCARE_JOBS:,}', f'{hc_pct}% of total postings', GOLD),
            kpi_card('Unique Employers', f'{UNIQUE_EMPLOYERS:,}', 'Genuine employers only', TEAL_DARK),
            kpi_card('States Covered', f'{STATES_COVERED}', 'All 16 German federal states', GOLD),
        ], style={'display': 'flex', 'gap': '16px', 'marginBottom': '20px',
                  'flexWrap': 'wrap'}),

        # Data period banner
        html.Div([
            html.Span('Data Period: ', style={'fontWeight': '600', 'color': TEXT_DARK}),
            html.Span(f'{DATE_RANGE}  ', style={'color': TEXT_MED}),
            html.Span('  |  Source: ', style={'fontWeight': '600', 'color': TEXT_DARK}),
            html.Span('StepStone Germany  ', style={'color': TEXT_MED}),
            html.Span('  |  Classification: ', style={'fontWeight': '600', 'color': TEXT_DARK}),
            html.Span('ISCO-08 (ILO) · ISIC Rev. 4 (UN Statistics)', style={'color': TEXT_MED}),
        ], style={
            'background': TEAL_LIGHT, 'border': f'1px solid {BORDER}',
            'borderRadius': '8px', 'padding': '10px 16px',
            'fontSize': '12px', 'marginBottom': '20px',
        }),

        # Charts row
        html.Div([
            html.Div(
                section_card('Healthcare Role Breakdown', [
                    dcc.Graph(figure=donut_fig, config={'displayModeBar': False},
                              style={'height': '300px'})
                ]),
                style={'flex': '1', 'minWidth': '280px'}
            ),
            html.Div(
                section_card('Jobs by Employer Category',
                             [dcc.Graph(figure=isic_fig, config={'displayModeBar': False},
                                        style={'height': '300px'})],
                             subtitle='Classified using ISIC Rev. 4 (UN standard)'),
                style={'flex': '2', 'minWidth': '380px'}
            ),
        ], style={'display': 'flex', 'gap': '20px', 'flexWrap': 'wrap'}),

        note_box(
            '64.9% of job postings do not carry state-level location data on StepStone. '
            'Geographic analysis is based on the 35.1% of records with a state tag (n=10,099). '
            '2,303 postings from aggregator portals (meinestadt.de) and non-healthcare employers '
            '(EASYFITNESS) are flagged in the dataset and excluded from employer-level analyses.'
        ),
    ])


def build_job_categories():
    # Healthcare only bar
    df_hc = df_jobs[df_jobs['category'] != 'Non-Healthcare'].sort_values('count', ascending=True)
    fig_hc = hbar(df_hc, 'count', 'category', color=TEAL,
                  title='Healthcare Job Categories (ISCO-3 based)')

    # Top 20 ISCO-4
    df_i4 = df_isco4.sort_values('count', ascending=True)
    fig_isco4 = hbar(df_i4, 'count', 'display', color=GOLD,
                     title='Top 20 ISCO-4 Unit Groups by Volume')

    # Top 20 titles
    df_t = df_titles.sort_values('count', ascending=True)
    fig_titles = hbar(df_t, 'count', 'title', color=TEAL_DARK,
                      title='Top 20 Job Titles by Volume')

    # Full breakdown incl non-HC
    df_all = df_jobs.sort_values('count', ascending=True)
    colors_all = [TEAL if 'Non-Healthcare' not in c else '#B8D9D9'
                  for c in df_all['category']]
    fig_all = hbar(df_all, 'count', 'category', color=colors_all,
                   title='All Job Categories (ISCO-3 based, incl. Non-Healthcare)')

    return html.Div([
        html.Div([
            html.Div(
                section_card('Healthcare Role Categories',
                             [dcc.Graph(figure=fig_hc, config={'displayModeBar': False},
                                        style={'height': '380px'})],
                             subtitle='Roles classified under ISCO-2 groups 22, 32, 53'),
                style={'flex': '1', 'minWidth': '340px'}
            ),
            html.Div(
                section_card('All Categories (incl. Non-Healthcare)',
                             [dcc.Graph(figure=fig_all, config={'displayModeBar': False},
                                        style={'height': '380px'})],
                             subtitle='Full distribution across all ISCO-3 categories'),
                style={'flex': '1', 'minWidth': '340px'}
            ),
        ], style={'display': 'flex', 'gap': '20px', 'flexWrap': 'wrap', 'marginBottom': '20px'}),

        html.Div([
            html.Div(
                section_card('Top 20 ISCO-4 Unit Groups',
                             [dcc.Graph(figure=fig_isco4, config={'displayModeBar': False},
                                        style={'height': '480px'})],
                             subtitle='Official ILO unit group classifications'),
                style={'flex': '1', 'minWidth': '340px'}
            ),
            html.Div(
                section_card('Top 20 Job Titles',
                             [dcc.Graph(figure=fig_titles, config={'displayModeBar': False},
                                        style={'height': '480px'})],
                             subtitle='Standardised job titles from StepStone listings'),
                style={'flex': '1', 'minWidth': '340px'}
            ),
        ], style={'display': 'flex', 'gap': '20px', 'flexWrap': 'wrap'}),
    ])


def build_employer():
    # ISIC donut
    fig_donut = donut(
        df_isic['category'].tolist(),
        df_isic['count'].tolist(),
        [ISIC_COLORS.get(c, TEAL) for c in df_isic['category']],
        title='Distribution by ISIC Rev. 4 Category',
    )

    # Employer bar — color by ISIC category
    df_emp_sorted = df_emp.sort_values('count', ascending=True)
    emp_colors = [ISIC_COLORS.get(c, TEAL) for c in df_emp_sorted['category']]
    fig_emp = go.Figure(go.Bar(
        x=df_emp_sorted['count'],
        y=df_emp_sorted['employer'],
        orientation='h',
        marker_color=emp_colors,
        marker_line_width=0,
        text=df_emp_sorted['count'].apply(lambda v: f'{v:,}'),
        textposition='outside',
        textfont=dict(size=11, color=TEXT_DARK),
        customdata=df_emp_sorted['category'],
        hovertemplate='<b>%{y}</b><br>Jobs: %{x:,}<br>Category: %{customdata}<extra></extra>',
    ))
    fig_emp.update_layout(
        **CHART_LAYOUT,
        title=dict(text='Top 15 Hiring Companies', font=dict(size=13, color=TEXT_MED), x=0),
        xaxis=dict(showgrid=True, gridcolor=BORDER, zeroline=False,
                   showticklabels=False, title=''),
        yaxis=dict(showgrid=False, title='', tickfont=dict(size=10)),
        bargap=0.35,
        height=460,
    )

    # Legend for employer bar
    legend_items = [
        html.Div([
            html.Div(style={'width': '10px', 'height': '10px', 'borderRadius': '2px',
                            'background': ISIC_COLORS.get(cat, TEAL),
                            'marginRight': '6px', 'flexShrink': '0'}),
            html.Span(cat.split(' (ISIC')[0], style={'fontSize': '11px', 'color': TEXT_MED}),
        ], style={'display': 'flex', 'alignItems': 'center', 'marginBottom': '5px'})
        for cat in ISIC_COLORS.keys()
    ]

    return html.Div([
        html.Div([
            html.Div(
                section_card('Employer Category Distribution',
                             [dcc.Graph(figure=fig_donut, config={'displayModeBar': False},
                                        style={'height': '320px'})],
                             subtitle='ISIC Rev. 4 — UN International Standard Industrial Classification'),
                style={'flex': '1', 'minWidth': '280px'}
            ),
            html.Div([
                section_card('ISIC Category Key', legend_items),
                html.Div([
                    html.Div('ISIC Rev. 4 Reference', style={
                        'fontSize': '12px', 'fontWeight': '600', 'color': TEXT_DARK,
                        'marginBottom': '8px'
                    }),
                    *[html.Div([
                        html.Span(code, style={'fontFamily': 'monospace', 'fontWeight': '700',
                                               'color': TEAL, 'marginRight': '8px', 'fontSize': '12px'}),
                        html.Span(name, style={'fontSize': '11px', 'color': TEXT_MED}),
                    ], style={'marginBottom': '4px', 'display': 'flex'})
                    for code, name in [
                        ('8610', 'Hospital activities'),
                        ('8620', 'Medical and dental practice activities'),
                        ('8690', 'Other human health activities'),
                        ('8710', 'Residential nursing care facilities'),
                        ('8720', 'Residential care activities for mental health, substance abuse'),
                        ('7820', 'Temporary employment agency activities'),
                    ]],
                ], style={
                    'background': CARD, 'borderRadius': '12px',
                    'padding': '18px 20px', 'border': f'1px solid {BORDER}',
                    'boxShadow': '0 1px 4px rgba(0,0,0,0.06)',
                }),
            ], style={'flex': '1', 'minWidth': '240px', 'display': 'flex',
                      'flexDirection': 'column', 'gap': '16px'}),
        ], style={'display': 'flex', 'gap': '20px', 'flexWrap': 'wrap', 'marginBottom': '20px'}),

        section_card('Top 15 Genuine Hiring Companies',
                     [dcc.Graph(figure=fig_emp, config={'displayModeBar': False},
                                style={'height': '460px'})],
                     subtitle='Bars coloured by ISIC employer category · Excludes aggregator portals'),
    ])


def build_geography():
    fig_map = build_map()
    fig_bar = hbar(
        df_state.sort_values('count', ascending=True),
        'count', 'state', color=TEAL,
        title='Job Volume by Federal State',
    )

    hover_note = (
        'Hover over each state marker to see total job volume and the top 3 ISCO-4 roles for that state. '
        if not germany_geojson else
        'Hover over each state to see total job volume and the top 3 ISCO-4 roles for that state. '
    )

    return html.Div([
        note_box(
            f'Geographic analysis is based on {PCT_STATE_TAGGED}% of records that carry a '
            f'state-level tag (n=10,099 of 29,045). '
            'The remaining 64.9% of postings do not specify a state on StepStone.'
        ),
        html.Div(style={'height': '16px'}),
        html.Div([
            html.Div(
                section_card('Germany — Healthcare Jobs by State',
                             [
                                 html.Div(hover_note, style={
                                     'fontSize': '11px', 'color': TEXT_MED,
                                     'marginBottom': '10px'
                                 }),
                                 dcc.Graph(figure=fig_map, config={'displayModeBar': False},
                                           style={'height': '520px'}),
                             ]),
                style={'flex': '2', 'minWidth': '380px'}
            ),
            html.Div(
                section_card('State Rankings',
                             [dcc.Graph(figure=fig_bar, config={'displayModeBar': False},
                                        style={'height': '520px'})],
                             subtitle='By total job postings (state-tagged only)'),
                style={'flex': '1', 'minWidth': '280px'}
            ),
        ], style={'display': 'flex', 'gap': '20px', 'flexWrap': 'wrap', 'marginBottom': '20px'}),

        # State detail table
        section_card('State-level Detail — Top ISCO-4 Roles',
                     [html.Div([
                         html.Div([
                             html.Div(['State', 'Total Jobs', 'Top Role', '2nd Role', '3rd Role'],
                                      style={'display': 'grid',
                                             'gridTemplateColumns': '180px 80px 1fr 1fr 1fr',
                                             'gap': '0 12px',
                                             'padding': '10px 14px',
                                             'background': TEAL_LIGHT,
                                             'borderRadius': '6px 6px 0 0',
                                             'fontSize': '11px', 'fontWeight': '600',
                                             'color': TEXT_DARK}),
                         ]),
                         *[html.Div(
                             html.Div([
                                 state,
                                 f"{state_data[state]['count']:,}",
                                 state_data[state]['top3'][0],
                                 state_data[state]['top3'][1],
                                 state_data[state]['top3'][2],
                             ], style={
                                 'display': 'grid',
                                 'gridTemplateColumns': '180px 80px 1fr 1fr 1fr',
                                 'gap': '0 12px',
                                 'padding': '9px 14px',
                                 'background': CARD if i % 2 == 0 else TEAL_LIGHT,
                                 'fontSize': '11px', 'color': TEXT_MED,
                                 'borderBottom': f'1px solid {BORDER}',
                             }),
                         ) for i, state in enumerate(
                             sorted(state_data.keys(),
                                    key=lambda s: state_data[s]['count'], reverse=True)
                         )],
                     ])],
                     subtitle='Ranked by total job postings'),
    ])


def build_glossary():
    isco3_entries = [
        (221, 'Medical Doctors',
         'Diagnose, treat and prevent illness, disease and injury. Includes generalist (2211) and specialist (2212) practitioners. Requires university-level medical degree plus postgraduate training.'),
        (222, 'Nursing and Midwifery Professionals',
         'Provide treatment, support and care services. Plan and manage patient care, supervise health care workers. Requires higher education qualification in nursing or midwifery.'),
        (226, 'Other Health Professionals',
         'Includes physiotherapists (2264), pharmacists (2262), dentists (2261), dieticians (2265), audiologists (2266), optometrists (2267) and health professionals NEC (2269).'),
        (321, 'Medical and Pharmaceutical Technicians',
         'Includes medical imaging technicians (3211), pathology laboratory technicians (3212), pharmaceutical technicians (3213), medical and dental prosthetic technicians (3214).'),
        (322, 'Nursing and Midwifery Associate Professionals',
         'Provide basic nursing and midwifery care. Implement care plans established by professionals. Includes nursing associate professionals (3221) and midwifery associate professionals (3222).'),
        (325, 'Other Health Associate Professionals',
         'Includes dental assistants (3251), medical records technicians (3252), community health workers (3253), physiotherapy technicians (3255), medical assistants (3256), ambulance workers (3258).'),
        (531, 'Child Care Workers and Teachers Aides',
         'Provide care, supervision and support for children. Assist teachers in classroom environments. Includes child care workers (5311) and teachers aides (5312).'),
        (532, 'Personal Care Workers in Health Services',
         'Provide routine personal care in health and residential settings. Includes health care assistants (5321), home-based personal care workers (5322), and personal care workers NEC (5329).'),
    ]

    isic_entries = [
        ('8610', 'Hospitals & Acute Care',
         'Inpatient hospital activities. General hospitals, university hospitals, acute specialist care centres, rehabilitation hospitals.'),
        ('8620', 'Medical & Dental Practice',
         'Activities of general and specialist medical practitioners, dental practices, outpatient clinics, physiotherapy practices, and other ambulatory health care not elsewhere classified.'),
        ('8690', 'Other Health Services & Industry',
         'Other human health activities including home nursing, occupational therapy, medical laboratory services, ambulance services, health education, and medical equipment suppliers.'),
        ('8710', 'Residential & Long-term Care',
         'Residential nursing care facilities providing nursing, supervisory and other types of care. Includes nursing homes, elderly residential care, and convalescent homes.'),
        ('8720', 'Mental Health & Rehabilitation',
         'Residential care activities for mental health, substance abuse and developmental disabilities. Includes psychiatric residential care, drug rehabilitation centres.'),
        ('7820', 'Staffing & Recruitment',
         'Temporary employment agency activities. Includes healthcare staffing agencies, locum agencies, and personnel placement services for the health sector.'),
    ]

    return html.Div([
        section_card('ISCO-08 Classification — Healthcare Role Categories (ISCO-3 Level)',
                     [html.Div([glossary_row(code, name, desc, TEAL)
                                for code, name, desc in isco3_entries],
                               style={'borderRadius': '8px', 'overflow': 'hidden',
                                      'border': f'1px solid {BORDER}'})],
                     subtitle='International Standard Classification of Occupations, 2008 revision — International Labour Organization (ILO)'),

        html.Div(style={'height': '20px'}),

        section_card('ISIC Rev. 4 — Employer Categories',
                     [html.Div([glossary_row(code, name, desc, GOLD)
                                for code, name, desc in isic_entries],
                               style={'borderRadius': '8px', 'overflow': 'hidden',
                                      'border': f'1px solid {BORDER}'})],
                     subtitle='International Standard Industrial Classification of All Economic Activities, Revision 4 — UN Statistics Division'),

        html.Div(style={'height': '20px'}),

        section_card('Data Methodology & Notes', [
            *[html.Div([
                html.Div(title, style={'fontWeight': '600', 'color': TEXT_DARK,
                                       'fontSize': '12px', 'marginBottom': '4px'}),
                html.Div(body, style={'fontSize': '11px', 'color': TEXT_MED,
                                      'lineHeight': '1.6', 'marginBottom': '14px'}),
            ]) for title, body in [
                ('Data Source',
                 'Job postings scraped from StepStone Germany (stepstone.de). Collection period: '
                 '31 January – 10 March 2026. Total records: 29,045.'),
                ('Occupational Classification',
                 'All job titles are classified to ISCO-08 at the unit group level (4-digit) '
                 'using WHO healthcare worker classification guidelines as a reference framework. '
                 'ISCO-2 groups 22 (Health Professionals), 32 (Health Associate Professionals) '
                 'and 53 (Personal Care Workers) are treated as the core healthcare workforce.'),
                ('Employer Classification',
                 'Employers are classified using ISIC Rev. 4 codes based on company name, '
                 'sector context and job content. Classification is applied at the posting level. '
                 'meinestadt.de (job aggregator portal, 1,435 postings) and EASYFITNESS Franchise '
                 'GmbH (fitness sector, 868 postings) are flagged as non-genuine employers and '
                 'excluded from employer-level analyses.'),
                ('Geographic Coverage',
                 '35.1% of postings (n=10,099) carry an explicit German federal state tag. '
                 'The remaining 64.9% do not specify a location on StepStone. All geographic '
                 'analysis is based on the tagged subset. Results should be interpreted as '
                 'indicative, not exhaustive, for any given state.'),
                ('Visa & International Hiring',
                 'A systematic check of Requirements, Description and Benefits fields found '
                 'negligible mention of visa sponsorship or overseas hiring (< 0.1% of postings). '
                 'This is itself a market signal: German healthcare employers are not yet '
                 'prominently advertising international hiring on StepStone. This analysis '
                 'should be complemented by direct employer outreach.'),
            ]]
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
        'https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700&family=DM+Sans:wght@300;400;500;600&display=swap'
    ],
)
server = app.server

NAV_TABS = [
    ('overview',    'Overview'),
    ('categories',  'Job Categories'),
    ('employers',   'Employer Analysis'),
    ('geography',   'Geography'),
    ('glossary',    'Glossary & Methodology'),
]

app.layout = html.Div([
    # ── HEADER ──────────────────────────────────────────────
    html.Div([
        html.Div([
            html.Div([
                # Logo block
                html.Div([
                    html.Div('GATI', style={
                        'fontSize': '26px', 'fontWeight': '700', 'color': 'white',
                        'fontFamily': 'Outfit, sans-serif', 'letterSpacing': '-0.5px',
                        'lineHeight': '1',
                    }),
                    html.Div('Global Access to Talent from India', style={
                        'fontSize': '9px', 'color': 'rgba(255,255,255,0.75)',
                        'letterSpacing': '0.05em', 'marginTop': '2px',
                        'textTransform': 'uppercase',
                    }),
                ], style={
                    'borderRight': '1px solid rgba(255,255,255,0.25)',
                    'paddingRight': '20px', 'marginRight': '20px',
                }),
                html.Div([
                    html.Div('German Healthcare Labour Market Analysis',
                             style={'fontSize': '16px', 'fontWeight': '600',
                                    'color': 'white', 'fontFamily': 'Outfit, sans-serif'}),
                    html.Div('StepStone Germany  ·  29,045 Job Postings  ·  Jan–Mar 2026',
                             style={'fontSize': '11px', 'color': 'rgba(255,255,255,0.65)',
                                    'marginTop': '2px'}),
                ]),
            ], style={'display': 'flex', 'alignItems': 'center'}),

            html.Div([
                html.Div('ISCO-08', style={
                    'fontSize': '10px', 'fontWeight': '700',
                    'background': 'rgba(255,255,255,0.15)',
                    'color': 'white', 'padding': '4px 8px',
                    'borderRadius': '4px', 'marginRight': '6px',
                }),
                html.Div('ISIC Rev. 4', style={
                    'fontSize': '10px', 'fontWeight': '700',
                    'background': f'{GOLD}33',
                    'color': GOLD, 'padding': '4px 8px',
                    'borderRadius': '4px',
                }),
            ], style={'display': 'flex', 'alignItems': 'center'}),
        ], style={
            'maxWidth': '1280px', 'margin': '0 auto',
            'padding': '0 32px',
            'display': 'flex', 'justifyContent': 'space-between',
            'alignItems': 'center', 'height': '64px',
        }),
    ], style={'background': TEAL_DARK, 'borderBottom': f'3px solid {GOLD}'}),

    # ── NAVIGATION ──────────────────────────────────────────
    html.Div([
        html.Div([
            html.Div(id='nav-tabs', children=[
                html.Button(
                    label,
                    id=f'tab-btn-{tab_id}',
                    n_clicks=0,
                    style={
                        'background': 'none', 'border': 'none',
                        'padding': '14px 20px', 'cursor': 'pointer',
                        'fontSize': '13px', 'fontWeight': '500',
                        'color': TEXT_MED,
                        'fontFamily': 'Outfit, sans-serif',
                        'borderBottom': '2px solid transparent',
                        'transition': 'color 0.15s, border-color 0.15s',
                        'whiteSpace': 'nowrap',
                    },
                )
                for tab_id, label in NAV_TABS
            ], style={'display': 'flex', 'alignItems': 'center'}),
        ], style={
            'maxWidth': '1280px', 'margin': '0 auto', 'padding': '0 32px',
        }),
    ], style={
        'background': CARD, 'borderBottom': f'1px solid {BORDER}',
        'position': 'sticky', 'top': '0', 'zIndex': '100',
        'boxShadow': '0 1px 4px rgba(0,0,0,0.05)',
        'overflowX': 'auto',
    }),

    # ── CONTENT ─────────────────────────────────────────────
    html.Div(
        id='page-content',
        style={
            'maxWidth': '1280px', 'margin': '0 auto',
            'padding': '28px 32px 48px',
        }
    ),

    dcc.Store(id='active-tab', data='overview'),

], style={
    'fontFamily': 'DM Sans, sans-serif',
    'background': BG,
    'minHeight': '100vh',
    'color': TEXT_DARK,
})

# ─────────────────────────────────────────────────────────────
# CALLBACKS
# ─────────────────────────────────────────────────────────────
@app.callback(
    Output('active-tab', 'data'),
    [Input(f'tab-btn-{tab_id}', 'n_clicks') for tab_id, _ in NAV_TABS],
    prevent_initial_call=True,
)
def update_active_tab(*args):
    from dash import ctx
    if not ctx.triggered_id:
        return 'overview'
    return ctx.triggered_id.replace('tab-btn-', '')


@app.callback(
    Output('page-content', 'children'),
    Input('active-tab', 'data'),
)
def render_content(tab):
    builders = {
        'overview':   build_overview,
        'categories': build_job_categories,
        'employers':  build_employer,
        'geography':  build_geography,
        'glossary':   build_glossary,
    }
    return builders.get(tab, build_overview)()


@app.callback(
    [Output(f'tab-btn-{tab_id}', 'style') for tab_id, _ in NAV_TABS],
    Input('active-tab', 'data'),
)
def update_tab_styles(active):
    styles = []
    for tab_id, _ in NAV_TABS:
        if tab_id == active:
            styles.append({
                'background': 'none', 'border': 'none',
                'padding': '14px 20px', 'cursor': 'pointer',
                'fontSize': '13px', 'fontWeight': '600',
                'color': TEAL, 'fontFamily': 'Outfit, sans-serif',
                'borderBottom': f'2px solid {TEAL}',
                'transition': 'color 0.15s, border-color 0.15s',
                'whiteSpace': 'nowrap',
            })
        else:
            styles.append({
                'background': 'none', 'border': 'none',
                'padding': '14px 20px', 'cursor': 'pointer',
                'fontSize': '13px', 'fontWeight': '500',
                'color': TEXT_MED, 'fontFamily': 'Outfit, sans-serif',
                'borderBottom': '2px solid transparent',
                'transition': 'color 0.15s, border-color 0.15s',
                'whiteSpace': 'nowrap',
            })
    return styles


if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=8050)
