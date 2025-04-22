import dash
import dash_bootstrap_components as dbc
from dash import dcc, html, Input, Output, State
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np
import base64
import io
import logging

logging.basicConfig(level=logging.INFO)

# ---------------------------------------------------------------------
# Data Generation Functions
# ---------------------------------------------------------------------
def generate_energy_efficiency_data():
    dates = pd.date_range(start='2023-01-01', end='2023-12-31', freq='M')
    energy_consumption = [150, 145, 140, 130, 120, 110, 105, 100, 95, 90, 85, 80]
    baseline = [150] * 12
    return pd.DataFrame({
        'Datum': dates,
        'Energieverbrauch (kWh)': energy_consumption,
        'Baseline (kWh)': baseline
    })

def generate_co2_reduction_data():
    categories = ['Ausgangswert', 'Optimierung 1', 'Optimierung 2', 'Finales Design']
    emissions = [100, 75, 60, 42]
    return pd.DataFrame({
        'Designphase': categories,
        'CO2-Emissionen (%)': emissions
    })

def generate_process_simulation_data():
    temperature = np.linspace(20, 100, 20)
    efficiency = 45 + 30 * (1 - np.exp(-(temperature - 20) / 30))
    return pd.DataFrame({
        'Temperatur (°C)': temperature,
        'Wirkungsgrad (%)': efficiency
    })

def generate_sankey_data():
    return {
        'source': [0, 0, 1, 1, 2, 2, 3, 4, 4, 5, 6],
        'target': [1, 2, 3, 4, 5, 6, 7, 7, 8, 9, 9],
        'value': [50, 50, 30, 20, 20, 30, 30, 15, 5, 15, 30],
        'label': [
            "Primärenergie", "Elektrische Energie", "Wärmeenergie", "Umwandlungsverluste",
            "Prozesswärme", "Maschinenbetrieb", "Licht & Elektronik", "Nutzenergie",
            "Verluste", "Produktionsnutzen", "Komfortnutzen"
        ]
    }

# ---------------------------------------------------------------------
# Prepare Example Data
# ---------------------------------------------------------------------
energy_df = generate_energy_efficiency_data()
co2_df = generate_co2_reduction_data()
process_df = generate_process_simulation_data()
sankey_example = generate_sankey_data()

# ---------------------------------------------------------------------
# File Upload Parsing
# ---------------------------------------------------------------------
def parse_contents(contents, filename):
    content_type, content_string = contents.split(',')
    decoded = base64.b64decode(content_string)
    file_ext = filename.lower()
    try:
        if file_ext.endswith('.csv'):
            df = pd.read_csv(io.StringIO(decoded.decode('utf-8')))
            fig = px.bar(df, title="Uploaded CSV Data", template="plotly_white")
        elif file_ext.endswith(('.xls', '.xlsx')):
            df = pd.read_excel(io.BytesIO(decoded))
            fig = px.bar(df, title="Uploaded Excel Data", template="plotly_white")
        else:
            return html.Div(["Unsupported file format. Please upload a CSV or Excel file."])
    except Exception as e:
        return html.Div([f"Error processing file: {e}"])
    
    fig.update_layout(
        paper_bgcolor="rgba(128,128,128,0.2)",
        plot_bgcolor="rgba(128,128,128,0.2)",
        font_color="#000"
    )
    
    return html.Div([
        html.H5(filename),
        dcc.Graph(figure=fig)
    ])

# ---------------------------------------------------------------------
# Dash App Setup
# ---------------------------------------------------------------------

external_stylesheets = [
    dbc.themes.CYBORG,
    "https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0-beta3/css/all.min.css"
]

app = dash.Dash(__name__, use_pages=True, external_stylesheets=external_stylesheets, suppress_callback_exceptions=True)
server = app.server

# ---------------------------------------------------------------------
# Layout
# ---------------------------------------------------------------------
app.layout = html.Div([
    dcc.Location(id="url", refresh=False),
    # Background video and overlay
    html.Video(
        src="/assets/background.mp4",
        autoPlay=True,
        loop=True,
        muted=True,
        className="video-background"
    ),
    html.Div(className="video-overlay"),
    dbc.Container([
        dbc.NavbarSimple(
            brand="Portfolio: B.Eng Khalil Ayed",
            brand_href="/",
            color="primary",
            dark=True,
            className="mb-3 navbar",
            style={"borderRadius": "8px", "overflow": "hidden"}
        ),
        html.Div(id="main-content"),
        html.Footer("© 2025 • Khalil Ayed", className="mt-4")
    ], fluid=True, className="dash-container")
])

# ---------------------------------------------------------------------
# Callback to control page content (main page vs. detail pages)
# ---------------------------------------------------------------------
@app.callback(
    Output("main-content", "children"),
    Input("url", "pathname")
)
def render_main_content(pathname):
    # Always show the same tabs
    tabs_layout = dcc.Tabs(
        id="tabs",
        value='tab-profil',
        className="tabs-container",
        children=[
            dcc.Tab(label='Profil', value='tab-profil', className="tab", selected_className="tab-selected"),
            dcc.Tab(label='Lebenslauf', value='tab-lebenslauf', className="tab", selected_className="tab-selected"),
            dcc.Tab(label='Projekte', value='tab-projekte', className="tab", selected_className="tab-selected"),
            dcc.Tab(label='Kontakt', value='tab-kontakt', className="tab", selected_className="tab-selected"),
        ]
    )
    
    # Container for main-page tab content
    tabs_content = html.Div(id='tabs-content', className='tabs-content mt-3')
    
    # Home page: show only tabs and their content container
    if pathname in ["/", "/index"]:
        return html.Div([tabs_layout, tabs_content])
    
    # Detail page for Projekt A
    elif pathname == "/projekt-a":
        content = [
            html.H2("Projekt A – Detailseite"),
            # First image (Abbildung 1)
            html.Div([
                html.Img(
                    src="/assets/abbildung1.png",
                    style={"width": "45%", "display": "block", "margin": "auto"}
                ),
                html.H4("Abbildung 1"),
                html.P(
                    "In dieser Abbildung wird ein Überblick über die räumliche Anordnung der Lichtquellen gegeben. "
                    "Es werden verschiedene Winkel und Höhen berücksichtigt, um ein möglichst realistisches Beleuchtungsprofil zu erhalten."
                ),
                html.P(
                    "Besonderes Augenmerk liegt auf der Ermittlung der optimalen Positionierung, damit "
                    "sowohl eine gleichmäßige Ausleuchtung als auch Energieeffizienz gewährleistet werden kann."
                )
            ], className="mb-4"),
            # Second image (Abbildung 2)
            html.Div([
                html.Img(
                    src="/assets/abbildung2.png",
                    style={"width": "45%", "display": "block", "margin": "auto"}
                ),
                html.H4("Abbildung 2"),
                html.P(
                    "Hier wird die Szene zu verschiedenen Tageszeiten dargestellt. "
                    "Es kann beobachtet werden, wie sich die Lichtverhältnisse mit wechselndem Sonnenstand verändern."
                ),
                html.P(
                    "Dadurch lassen sich Schlüsse über das Zusammenspiel von natürlichem und künstlichem Licht ziehen, "
                    "um sowohl eine angenehme Atmosphäre als auch ein funktionales Beleuchtungskonzept zu realisieren."
                )
            ], className="mb-4"),
            # Third image (Abbildung 3)
            html.Div([
                html.Img(
                    src="/assets/abbildung3.png",
                    style={"width": "45%", "display": "block", "margin": "auto"}
                ),
                html.H4("Abbildung 3"),
                html.P(
                    "In dieser Grafik wird der zeitliche Verlauf des solaren Zenithwinkels sowie der Sonneneinstrahlung "
                    "über das Jahr veranschaulicht. Auf Grundlage der dargestellten Kurven können "
                    "mögliche Optimierungsmaßnahmen für passive Solartechniken im Gebäudedesign abgeleitet werden."
                ),
                html.P(
                    "Es wird deutlich, dass in den Sommermonaten höhere Einstrahlungswerte vorliegen, "
                    "während in den Wintermonaten ein deutlich flacherer Einfallswinkel auftritt. "
                    "Dies dient als wesentliche Grundlage für die Auslegung von Verschattungselementen "
                    "und die effiziente Planung der Gebäudehülle."
                )
            ], className="mb-4"),
            # Link back to "Projekte"
            dcc.Link("Zurück zu Projekten", href="/", className="btn btn-secondary mt-3")
        ]
        return html.Div([
            tabs_layout,
            dbc.Container([
                dbc.Card([dbc.CardBody(content)], className="my-card", style={"margin": "20px"})
            ], fluid=True)
        ])
    
    # Detail page for Projekt B
    elif pathname == "/projekt-b":
        df = pd.DataFrame({
            "Monat": ["Mai", "Juni", "Juli", "August"],
            "Wert": [120, 140, 135, 155]
        })
        fig = px.line(df, x="Monat", y="Wert", title="Projekt B - Entwicklungsverlauf")
        content = [
            html.H2("Projekt B – Detailseite"),
            html.P("Detaillierte Informationen, Diagramme und Analysen zu Projekt B."),
            dcc.Graph(figure=fig),
            dcc.Link("Zurück zu Projekten", href="/", className="btn btn-secondary mt-3")
        ]
        return html.Div([
            tabs_layout,
            dbc.Container([dbc.Card([dbc.CardBody(content)])], fluid=True)
        ])
    
    # Detail page for Projekt C
    elif pathname == "/projekt-c":
        df = pd.DataFrame({
            "Woche": ["W1", "W2", "W3", "W4"],
            "Wert": [80, 95, 90, 100]
        })
        fig = px.bar(df, x="Woche", y="Wert", title="Projekt C - Wochenverlauf")
        content = [
            html.H2("Projekt C – Detailseite"),
            html.P("Detaillierte Informationen, Diagramme und Analysen zu Projekt C."),
            dcc.Graph(figure=fig),
            dcc.Link("Zurück zu Projekten", href="/", className="btn btn-secondary mt-3")
        ]
        return html.Div([
            tabs_layout,
            dbc.Container([dbc.Card([dbc.CardBody(content)])], fluid=True)
        ])
    
    # Detail page for Projekt D
    elif pathname == "/projekt-d":
        df = pd.DataFrame({
            "Kategorie": ["A", "B", "C"],
            "Wert": [200, 150, 180]
        })
        fig = px.pie(df, names="Kategorie", values="Wert", title="Projekt D - Verteilung")
        content = [
            html.H2("Projekt D – Detailseite"),
            html.P("Detaillierte Informationen, Diagramme und Analysen zu Projekt D."),
            dcc.Graph(figure=fig),
            dcc.Link("Zurück zu Projekten", href="/", className="btn btn-secondary mt-3")
        ]
        return html.Div([
            tabs_layout,
            dbc.Container([dbc.Card([dbc.CardBody(content)])], fluid=True)
        ])
    
    # Detail page for Projekt E
    elif pathname == "/projekt-e":
        content = [
            html.H2("Projekt E – DEM-Simulation und Konstruktion einer Kugelmühle"),
            
            # Abbildung 1
            html.Div([
                html.Img(
                    src="/assets/abb1.png",
                    style={"width": "45%", "display": "block", "margin": "auto"}
                ),
                html.H4("Abbildung 1"),
                html.P(
                    "In dieser Abbildung wird das Partikelspektrum der Kugelmühle zu verschiedenen Zeitpunkten dargestellt. "
                    "Die Farbskala hebt unterschiedliche Größen- oder Geschwindigkeitsbereiche hervor, um den Mahlvorgang detailliert zu untersuchen."
                ),
                html.P(
                    "Es wurde darauf geachtet, verschiedene Parameter wie Partikelanzahl und Drehzahl zu variieren, "
                    "damit das Fließverhalten präzise erfasst und potenzielle Engstellen identifiziert werden können."
                )
            ], className="mb-4"),
            
            # Abbildung 2
            html.Div([
                html.Img(
                    src="/assets/abb2.png",
                    style={"width": "45%", "display": "block", "margin": "auto"}
                ),
                html.H4("Abbildung 2"),
                html.P(
                    "Hier wird eine dreidimensionale Visualisierung der Partikelbewegung im Inneren der Kugelmühle gezeigt. "
                    "Die unterschiedlichen Farben stehen beispielsweise für Temperatur- oder Geschwindigkeitsverteilungen, "
                    "um mögliche Hotspots oder Verklumpungen zu identifizieren."
                ),
                html.P(
                    "Auf Basis dieser Informationen kann eine gezielte Anpassung von Drehzahl und Mühlengeometrie erfolgen, "
                    "um sowohl Verschleiß als auch Energieverbrauch zu minimieren."
                )
            ], className="mb-4"),
            
            # Abbildung 3
            html.Div([
                html.Img(
                    src="/assets/abb3.png",
                    style={"width": "45%", "display": "block", "margin": "auto"}
                ),
                html.H4("Abbildung 3"),
                html.P(
                    "In dieser Explosionszeichnung wird der konstruktive Aufbau der Kugelmühle dargestellt. "
                    "Die Baugruppen wie Trommelgehäuse, Lagerung und Antriebseinheit wurden so ausgelegt, "
                    "dass eine gleichmäßige Partikelverteilung und ein effizienter Mahlprozess ermöglicht werden."
                ),
                html.P(
                    "Besonderer Wert wurde auf Modularität gelegt, damit Wartungsarbeiten vereinfacht und "
                    "Anpassungen an unterschiedliche Materialeigenschaften problemlos durchgeführt werden können."
                )
            ], className="mb-4"),
            
            # Abbildung 4
            html.Div([
                html.Img(
                    src="/assets/abb4.png",
                    style={"width": "45%", "display": "block", "margin": "auto"}
                ),
                html.H4("Abbildung 4"),
                html.P(
                    "In dieser Darstellung werden verschiedene Geschwindigkeitskomponenten (vx, vy, vz) "
                    "innerhalb der Kugelmühle visualisiert. Dadurch wird eine genauere Untersuchung der Partikeldynamik ermöglicht."
                ),
                html.P(
                    "Besonders im Bereich der Randzonen lassen sich potenzielle Scher- und Reibungskräfte ableiten, "
                    "was bei der Dimensionierung von Verschleißschutz und Antriebssystemen berücksichtigt werden kann."
                )
            ], className="mb-4"),
            
            # Abbildung 5
            html.Div([
                html.Img(
                    src="/assets/abb5.png",
                    style={"width": "45%", "display": "block", "margin": "auto"}
                ),
                html.H4("Abbildung 5"),
                html.P(
                    "Hier wird das zeitliche Kraftprofil an ausgewählten Partikeln und Kugeln gezeigt. "
                    "Die Peaks geben Hinweise auf Kollisionen und Energieeinträge, die für die Zerkleinerungseffizienz entscheidend sind."
                ),
                html.P(
                    "Auf dieser Grundlage können Prozessparameter wie Füllgrad oder Drehzahl optimiert werden, "
                    "um eine gleichmäßige Belastung der Partikel zu erreichen."
                )
            ], className="mb-4"),
            
            # Abbildung 6
            html.Div([
                html.Img(
                    src="/assets/abb6.png",
                    style={"width": "45%", "display": "block", "margin": "auto"}
                ),
                html.H4("Abbildung 6"),
                html.P(
                    "In diesem Diagramm wird die Partikelgrößenverteilung vor und nach dem Mahlprozess dargestellt. "
                    "Die Kumulativkurven ermöglichen eine detaillierte Bewertung der Zerkleinerungseffizienz bei unterschiedlichen Betriebsbedingungen."
                ),
                html.P(
                    "Es lassen sich Rückschlüsse darauf ziehen, welche Mahlparameter besonders effektiv sind, "
                    "um gewünschte Endkorngrößen zu erzielen und die Ausbeute zu maximieren."
                )
            ], className="mb-4"),
            
            # Abbildung 7
            html.Div([
                html.Img(
                    src="/assets/abb7.png",
                    style={"width": "45%", "display": "block", "margin": "auto"}
                ),
                html.H4("Abbildung 7"),
                html.P(
                    "Diese Trajektorien verdeutlichen die Bewegung einzelner Partikel im xy- und xz-Raum. "
                    "Anhand der Kurven können Bereiche mit hoher Rezirkulation oder intensiver Kollision identifiziert werden."
                ),
                html.P(
                    "Daraus lassen sich Empfehlungen für die Mühlengeometrie ableiten, um einen stabilen Prozessablauf zu gewährleisten "
                    "und das Risiko von Totzonen oder Materialstau zu reduzieren."
                )
            ], className="mb-4"),
            
            # Video Section 1 (video1.mp4)
            html.Div([
                html.H4("Video: DEM-Simulation der Partikelbewegung"),
                html.Video(
                    src="/assets/video1.mp4",
                    controls=True,
                    style={"width": "45%", "display": "block", "margin": "auto"}
                ),
                html.P(
                    "In diesem Video wird die dynamische Bewegung der Partikel innerhalb der Kugelmühle veranschaulicht. "
                    "Die dargestellten Trajektorien liefern wichtige Erkenntnisse über die Effektivität des Mahlprozesses."
                ),
                html.P(
                    "Anhand der Simulation können kritische Bereiche identifiziert werden, an denen Optimierungsmaßnahmen "
                    "zur Verbesserung der Energieeffizienz und Prozessstabilität abgeleitet werden."
                )
            ], className="mb-4"),
            
            # Video Section 2 (record2.mp4)
            html.Div([
                html.H4("Video: Paraview-Simulation"),
                html.Video(
                    src="/assets/record2.mp4",
                    controls=True,
                    style={"width": "50%", "display": "block", "margin": "auto"}
                ),
                html.P(
                    "In dieser Paraview-Simulation wird die Auswertung der Partikelverteilung und -bewegung mit erweiterter Visualisierung dargestellt. "
                    "Die farbcodierten Bereiche verdeutlichen, wie sich lokale Dichte und Geschwindigkeiten im Mahlraum entwickeln."
                ),
                html.P(
                    "Dadurch lassen sich detaillierte Einblicke in das Prozessgeschehen gewinnen, "
                    "die für eine gezielte Optimierung von Betriebsparametern und Mühlengeometrie genutzt werden können."
                )
            ], className="mb-4"),
            # Video Section 2 (record2.mp4)
            html.Div([
                html.H4("Video: LIGGGHTS-Simulation"),
                html.Video(
                    src="/assets/record3.mp4",
                    controls=True,
                    style={"width": "50%", "display": "block", "margin": "auto"}
                ),
                html.P(
                    "In dieser Simulation wird die Auswertung der Partikelverteilung und -bewegung mit erweiterter Visualisierung dargestellt. "
                    "Die farbcodierten Bereiche verdeutlichen, wie sich lokale Dichte und Geschwindigkeiten im Mahlraum entwickeln."
                ),
                html.P(
                    "Dadurch lassen sich detaillierte Einblicke in das Prozessgeschehen gewinnen, "
                    "die für eine gezielte Optimierung von Betriebsparametern und Mühlengeometrie genutzt werden können."
                )
            ], className="mb-4"),
            
            # PDF Section: Drawing (z1.pdf) with image preview
            html.Div([
                html.H4("Zeichnung (PDF: z1.pdf)"),
                html.Img(
                    src="/assets/z1_preview.png",
                    style={"width": "45%", "display": "block", "margin": "auto"}
                ),
                html.P(
                    "In diesem PDF-Dokument werden die technischen Zeichnungen der Kugelmühle dargestellt. "
                    "Die präzisen Konstruktionsdetails ermöglichen eine detaillierte Analyse der geometrischen Parameter, "
                    "die für den Produktionsprozess von Bedeutung sind."
                ),
                html.A(
                    "PDF herunterladen: z1.pdf",
                    href="/assets/z1.pdf",
                    download="z1.pdf",
                    className="btn btn-primary mt-2"
                )
            ], className="mb-4"),
            
            # PDF Section: Explosion (z2.pdf) with image preview
            html.Div([
                html.H4("Explosionszeichnung (PDF: z2.pdf)"),
                html.Img(
                    src="/assets/z2_preview.png",
                    style={"width": "45%", "display": "block", "margin": "auto"}
                ),
                html.P(
                    "Dieses PDF enthält die Explosionszeichnung der Kugelmühle, welche die einzelnen Komponenten "
                    "und deren Montage detailliert aufzeigt. Die Ansicht unterstützt das Verständnis des Aufbaus "
                    "und der Funktionsweise der Anlage."
                ),
                html.A(
                    "PDF herunterladen: z2.pdf",
                    href="/assets/z2.pdf",
                    download="z2.pdf",
                    className="btn btn-primary mt-2"
                )
            ], className="mb-4"),
            
            # 3D "Deck" style gallery (no scroll)
            html.Div([
                html.H4("3D Konstruktion"),
                html.Div(
                    children=[
                        html.Div([
                            html.Img(src=f"/assets/assembly{i}.jpg", className="deck-img")
                        ], className="deck-card")
                        for i in range(1, 6)  # e.g., assembly1.jpg to assembly5.jpg
                    ],
                    className="deck-container"
                )
            ], className="mb-4"),
            
            # Link back to "Projekte"
            dcc.Link("Zurück zu Projekten", href="/", className="btn btn-secondary mt-3")
        ]
        
        return html.Div([
            tabs_layout,
            dbc.Container([
                dbc.Card([
                    dbc.CardBody(content + [dcc.Link("Zurück zu Projekten", href="/", className="btn btn-secondary mt-3")])
                ], className="my-card", style={"margin": "20px"})
            ], fluid=True)
        ])



# ---------------------------------------------------------------------
# Callback to render the content of each tab (only for the main page)
# ---------------------------------------------------------------------
@app.callback(Output('tabs-content', 'children'), Input('tabs', 'value'))
def render_content(tab):
    if tab == 'tab-profil':
        return dbc.Card(html.Div([
            html.H2("Profil"),
            html.P("Bachelor of Engineering in Verfahrenstechnik, Energietechnik und Umwelttechnik. "
                   "Meine Schwerpunkte liegen in der Optimierung energetischer Prozesse, nachhaltiger "
                   "Verfahrenstechnik und ressourcenschonenden Technologien."),
            html.Div([
                html.Div([
                    html.H4("Fachkenntnisse"),
                    html.Ul([
                        html.Li("Prozesssimulation und -optimierung"),
                        html.Li("Energieeffizienzanalyse"),
                        html.Li("Nachhaltigkeitsbewertung"),
                        html.Li("Regenerative Energiesysteme")
                    ])
                ], className="profile-section"),
                html.Div([
                    html.H4("Technische Fähigkeiten"),
                    html.Ul([
                        html.Li("Python (Pandas, NumPy, Plotly, Dash)"),
                        html.Li("MATLAB/Simulink"),
                        html.Li("Aspen Plus / HYSYS"),
                        html.Li("CFD-Modellierung")
                    ])
                ], className="profile-section")
            ], className="profile-grid"),
            html.H2("Über mich", className="mt-4"),
            html.P("Als junger Ingenieur im Bereich Verfahrenstechnik, Energietechnik und Umwelttechnik "
                   "bin ich begeistert von der Entwicklung nachhaltiger Lösungen für komplexe technische "
                   "Herausforderungen. Während meines Studiums habe ich praktische Erfahrungen in "
                   "verschiedenen Projekten gesammelt, die sich mit Energieeffizienz, erneuerbaren "
                   "Energien und Prozessoptimierung befassten."),
            html.P("Mein Ziel ist es, innovative Technologien zu entwickeln und anzuwenden, um die "
                   "Energiewende voranzutreiben und industrielle Prozesse umweltfreundlicher zu gestalten.")
        ]), className="my-card")
    
    elif tab == 'tab-lebenslauf':
        return dbc.Card(
            html.Div([
                dbc.Row([
                    dbc.Col(
                        dbc.Card([
                            dbc.CardImg(src="/assets/cv.jpg", top=True, style={"borderRadius": "8px"}),
                            dbc.CardBody([
                                html.H4("Khalil Ayed", className="card-title"),
                                html.P("Verfahrenstechnik B.Eng", className="card-text"),
                                html.P("SalzdahlumerStr 112"),
                                html.P("Tel: +49 1520 7467 431"),
                                html.P("E-Mail: khalil.ayed.pro@gmail.com")
                            ])
                        ], className="card-glass", style={"width": "100%", "marginBottom": "1rem"}),
                        width=3
                    ),
                    dbc.Col([
                        html.H2("Profilzusammenfassung"),
                        html.P("Absolvent der Verfahrenstechnik mit Fokus auf nachhaltige Technologien und Prozessoptimierung. "
                               "Erfahrung in interdisziplinärer Zusammenarbeit und Einhaltung internationaler Standards, "
                               "insbesondere in der Optimierung von Adsorptionsprozessen."),
                        html.H2("Ausbildung"),
                        html.Div([
                            html.Div(className="timeline-dot"),
                            html.Div([
                                html.H4(
                                    html.Button(
                                        "Bachelor of Engineering, Verfahrens-, Energie- und Umwelttechnik", 
                                        id="btn-bachelor",
                                        n_clicks=0,
                                        style={"background": "none", "border": "none", "color": "inherit", "fontSize": "inherit", "cursor": "pointer", "padding": 0}
                                    )
                                ),
                                html.P("Hochschule Hannover, 09/2019 – 01/2025")
                            ], className="timeline-content")
                        ], className="timeline-item"),
                        html.H2("Berufserfahrung", className="mt-4"),
                        html.Div([
                            html.Div(className="timeline-dot"),
                            html.Div([
                                html.H4("Praktikum, Thyna Petroleum Services, Tunesien"),
                                html.P("06/2024 – 09/2024"),
                                html.P("Unterstützung technischer Prozesse und Optimierung von Systemen. Einblicke in die Energiewirtschaft und Zusammenarbeit mit internationalen Teams.")
                            ], className="timeline-content")
                        ], className="timeline-item"),
                        html.Div([
                            html.Div(className="timeline-dot"),
                            html.Div([
                                html.H4("Bachelorarbeit, Hochschule Hannover"),
                                html.P("06/2024 – 12/2024"),
                                html.P("Thema: Mechanochemische Aktivierung von Katalysatoren in der Kugelmühle zur CO2-Methanisierung. Note: 1,3. Intensive Zusammenarbeit mit interdisziplinären Teams.")
                            ], className="timeline-content")
                        ], className="timeline-item"),
                        html.Div([
                            html.Div(className="timeline-dot"),
                            html.Div([
                                html.H4("Projektmitarbeit, Hochschule Hannover"),
                                html.P("01/2023 – 05/2023"),
                                html.P("Mitarbeit bei der Planung und Optimierung energieeffizienter Gebäudekonzepte. Erstellung von Simulationen und Analysen zur Steigerung der Energieeffizienz.")
                            ], className="timeline-content")
                        ], className="timeline-item"),
                        html.H2("Zusatzqualifikationen", className="mt-4"),
                        html.Div([
                            html.Div([
                                html.H4("Fähigkeiten"),
                                html.Ul([
                                    html.Li("Wissenschaftliches Arbeiten, Teamarbeit und interkulturelle Kommunikation"),
                                    html.Li("Projektmanagement und Prozessoptimierung"),
                                    html.Li("Software: CAD, R&I-Fließbilder, SPS, Python, Matlab, Java")
                                ])
                            ], className="qual-section"),
                            html.Div([
                                html.H4("Sprachkenntnisse"),
                                html.Ul([
                                    html.Li("Deutsch (C1)"),
                                    html.Li("Englisch (B2)"),
                                    html.Li("Französisch (C1)"),
                                    html.Li("Arabisch (Muttersprache)")
                                ])
                            ], className="qual-section")
                        ], className="profile-grid")
                    ], width=9)
                ]),
                dbc.Modal(
                    [
                        dbc.ModalHeader("Bachelor Urkunde"),
                        dbc.ModalBody(html.Img(src="/assets/ba.jpg", style={"width": "100%"})),
                        dbc.ModalFooter([
                            html.A(
                                "Download Urkunde",
                                href="/assets/ba.pdf",
                                download="Bachelor_Urkunde.pdf",
                                className="btn btn-primary",
                                style={"marginRight": "1rem"}
                            ),
                            dbc.Button("Schließen", id="modal-close", n_clicks=0, className="ml-auto")
                        ])
                    ],
                    id="bachelor-modal",
                    centered=True,
                    is_open=False,
                    size="lg"
                )
            ]),
            className="my-card"
        )
    
    elif tab == 'tab-projekte':
        return dbc.Card(html.Div([
            html.H2("Projektübersicht"),
            html.Div(id='project-content', className="mt-3"),
            html.H3("Unsere Projekte in der Übersicht", className="mt-5"),
            html.Div(
                [
                    # Each project card is wrapped in a dcc.Link so that the whole card is clickable.
                    dcc.Link(
                        dbc.Card(
                            [
                                dbc.CardImg(src="/assets/sample1.jpg", top=True),
                                dbc.CardBody([
                                    html.H4("Projekt A", className="card-title"),
                                    html.P("Kurze Beschreibung von Projekt A.", className="card-text")
                                ]),
                            ],
                            className="card-glass",
                            style={"width": "18rem", "margin": "10px"}
                        ),
                        href="/projekt-a",
                        style={"textDecoration": "none", "color": "inherit"}
                    ),
                    dcc.Link(
                        dbc.Card(
                            [
                                dbc.CardImg(src="/assets/sample2.jpg", top=True),
                                dbc.CardBody([
                                    html.H4("Projekt B", className="card-title"),
                                    html.P("Kurze Beschreibung von Projekt B.", className="card-text")
                                ]),
                            ],
                            className="card-glass",
                            style={"width": "18rem", "margin": "10px"}
                        ),
                        href="/projekt-b",
                        style={"textDecoration": "none", "color": "inherit"}
                    ),
                    dcc.Link(
                        dbc.Card(
                            [
                                dbc.CardImg(src="/assets/sample3.jpg", top=True),
                                dbc.CardBody([
                                    html.H4("Projekt C", className="card-title"),
                                    html.P("Kurze Beschreibung von Projekt C.", className="card-text")
                                ]),
                            ],
                            className="card-glass",
                            style={"width": "18rem", "margin": "10px"}
                        ),
                        href="/projekt-c",
                        style={"textDecoration": "none", "color": "inherit"}
                    ),
                    dcc.Link(
                        dbc.Card(
                            [
                                dbc.CardImg(src="/assets/sample4.jpg", top=True),
                                dbc.CardBody([
                                    html.H4("Projekt D", className="card-title"),
                                    html.P("Kurze Beschreibung von Projekt D.", className="card-text")
                                ]),
                            ],
                            className="card-glass",
                            style={"width": "18rem", "margin": "10px"}
                        ),
                        href="/projekt-d",
                        style={"textDecoration": "none", "color": "inherit"}
                    ),
                    dcc.Link(
                        dbc.Card(
                            [
                                dbc.CardImg(src="/assets/sample5.jpg", top=True),
                                dbc.CardBody([
                                    html.H4("Projekt E", className="card-title"),
                                    html.P("Kurze Beschreibung von Projekt E.", className="card-text")
                                ]),
                            ],
                            className="card-glass",
                            style={"width": "18rem", "margin": "10px"}
                        ),
                        href="/projekt-e",
                        style={"textDecoration": "none", "color": "inherit"}
                    ),
                    dcc.Link(
                        dbc.Card(
                            [
                                dbc.CardImg(src="/assets/sample6.jpg", top=True),
                                dbc.CardBody([
                                    html.H4("Projekt F", className="card-title"),
                                    html.P("Kurze Beschreibung von Projekt F.", className="card-text")
                                ]),
                            ],
                            className="card-glass",
                            style={"width": "18rem", "margin": "10px"}
                        ),
                        href="/projekt-f",
                        style={"textDecoration": "none", "color": "inherit"}
                    ),
                    dcc.Link(
                        dbc.Card(
                            [
                                dbc.CardImg(src="/assets/sample7.jpg", top=True),
                                dbc.CardBody([
                                    html.H4("Projekt G", className="card-title"),
                                    html.P("Kurze Beschreibung von Projekt G.", className="card-text")
                                ]),
                            ],
                            className="card-glass",
                            style={"width": "18rem", "margin": "10px"}
                        ),
                        href="/projekt-g",
                        style={"textDecoration": "none", "color": "inherit"}
                    ),
                    dcc.Link(
                        dbc.Card(
                            [
                                dbc.CardImg(src="/assets/sample8.jpg", top=True),
                                dbc.CardBody([
                                    html.H4("Projekt H", className="card-title"),
                                    html.P("Kurze Beschreibung von Projekt H.", className="card-text")
                                ]),
                            ],
                            className="card-glass",
                            style={"width": "18rem", "margin": "10px"}
                        ),
                        href="/projekt-h",
                        style={"textDecoration": "none", "color": "inherit"}
                    )
                ],
                style={
                    "display": "flex",
                    "justifyContent": "center",
                    "alignItems": "center",
                    "gap": "1rem",
                    "flexWrap": "wrap"
                }
            )
        ]), className="my-card")
    
    elif tab == 'tab-kontakt':
        return dbc.Card(html.Div([
            html.H2("Kontakt"),
            html.P("Interesse an einer Zusammenarbeit oder weitere Fragen? "
                   "Kontaktieren Sie mich gerne über folgende Wege:"),
            html.Div([
                html.Div([
                    html.H4("Kontaktdaten"),
                    html.P([html.I(className="fas fa-envelope contact-icon"), " khalil.ayed.pro@gmail.com"]),
                    html.P([html.I(className="fas fa-phone contact-icon"), " +49 1520 7467 431"]),
                    html.P([html.I(className="fas fa-map-marker-alt contact-icon"), " Wolfenbüttel, Deutschland"])
                ], className="contact-section"),
                html.Div([
                    html.H4("Social Media & Plattformen"),
                    html.Div([
                        html.A(
                            html.I(className="fab fa-github fa-2x"),
                            href="https://github.com/dein-username",
                            style={"margin": "10px", "color": "#fff"}
                        ),
                        html.A(
                            html.I(className="fab fa-linkedin fa-2x"),
                            href="https://linkedin.com/in/dein-name",
                            style={"margin": "10px", "color": "#fff"}
                        ),
                        html.A(
                            html.I(className="fab fa-xing fa-2x"),
                            href="https://xing.com/profile/dein-name",
                            style={"margin": "10px", "color": "#fff"}
                        ),
                        html.A(
                            html.I(className="fab fa-researchgate fa-2x"),
                            href="https://researchgate.net/profile/dein-name",
                            style={"margin": "10px", "color": "#fff"}
                        )
                    ], className="social-icons")
                ], className="contact-section")
            ], className="contact-grid"),
            html.Div([
                html.H4("Kontaktformular"),
                dcc.Input(id="contact-name", type="text", placeholder="Name", className="contact-input"),
                dcc.Input(id="contact-email", type="email", placeholder="E-Mail", className="contact-input"),
                dcc.Textarea(id="contact-message", placeholder="Ihre Nachricht", className="contact-textarea"),
                html.Button("Nachricht senden", id="contact-submit", className="contact-submit-button"),
                html.Div(id="contact-output")
            ], className="contact-form", style={"marginTop": "2rem"})
        ]), className="my-card")

    return dbc.Card(html.Div([html.H3("Inhalt wird geladen...")]), className="my-card")



# ---------------------------------------------------------------------
# Additional Callbacks
# ---------------------------------------------------------------------
@app.callback(
    Output('project-content', 'children'),
    Input('project-dropdown', 'value')
)
def update_project_content(selected_project):
    if selected_project == 'energy':
        return html.Div([
            html.H3("Energieeffizienzoptimierung"),
            html.P("Entwicklung und Umsetzung eines Energieeffizienzkonzepts ..."),
            dcc.Graph(
                figure=px.line(
                    energy_df,
                    x='Datum',
                    y=['Energieverbrauch (kWh)', 'Baseline (kWh)'],
                    title="Energieverbrauchsreduktion über Zeit",
                    labels={'value': 'Verbrauch (kWh)', 'variable': 'Messgröße'},
                    template="plotly_white"
                )
            )
        ])
    elif selected_project == 'co2':
        return html.Div([
            html.H3("CO2-Emissionsreduktion"),
            dcc.Graph(
                figure=px.bar(
                    co2_df,
                    x='Designphase',
                    y='CO2-Emissionen (%)',
                    title="CO2-Emissionsreduktion in Designphasen",
                    template="plotly_white",
                    color='CO2-Emissionen (%)',
                    color_continuous_scale=px.colors.sequential.Viridis_r
                )
            )
        ])
    elif selected_project == 'process':
        return html.Div([
            html.H3("Prozesssimulation"),
            dcc.Graph(
                figure=px.scatter(
                    process_df,
                    x='Temperatur (°C)',
                    y='Wirkungsgrad (%)',
                    title="Temperaturabhängigkeit des Prozesswirkungsgrads",
                    template="plotly_white",
                    trendline="lowess"
                )
            )
        ])
    elif selected_project == 'sankey':
        fig_sankey = go.Figure(data=[go.Sankey(
            node=dict(
                pad=15,
                thickness=20,
                line=dict(color="black", width=0.5),
                label=sankey_example['label'],
                color="rgba(31, 119, 180, 0.8)"
            ),
            link=dict(
                source=sankey_example['source'],
                target=sankey_example['target'],
                value=sankey_example['value'],
                color="rgba(31, 119, 180, 0.3)"
            )
        )])
        fig_sankey.update_layout(
            title_text="Energieflussdiagramm des Produktionsprozesses",
            font_size=12
        )
        return html.Div([
            html.H3("Energieflussanalyse"),
            dcc.Graph(figure=fig_sankey)
        ])
    return html.Div([html.H3("Inhalt wird geladen...")])

@app.callback(
    Output('output-image-upload', 'children'),
    Input('upload-image', 'contents'),
    State('upload-image', 'filename')
)
def update_output(contents, filename):
    if contents:
        return parse_contents(contents, filename)
    return ""

@app.callback(
    Output('contact-output', 'children'),
    Input('contact-submit', 'n_clicks'),
    State('contact-name', 'value'),
    State('contact-email', 'value'),
    State('contact-message', 'value')
)
def submit_contact(n_clicks, name, email, message):
    if n_clicks:
        return html.Div([
            html.P(f"Vielen Dank, {name}, für Ihre Nachricht. Wir melden uns in Kürze unter {email}.")
        ])
    return ""

@app.callback(
    [Output("publication-details", "children"),
     Output("publication-details", "style")],
    [Input("btn-thesis", "n_clicks"),
     Input("btn-project", "n_clicks"),
     Input("btn-conference", "n_clicks")]
)
def show_publication_details(n_thesis, n_project, n_conference):
    ctx = dash.callback_context
    if not ctx.triggered:
        return "", {"display": "none"}
    button_id = ctx.triggered[0]['prop_id'].split('.')[0]
    if button_id == "btn-thesis":
        details = "Detaillierte Informationen zur Bachelorarbeit: [Weitere Informationen und Ergebnisse ...]"
    elif button_id == "btn-project":
        details = "Detaillierte Informationen zum Forschungsprojekt: [Weitere Projektdetails ...]"
    elif button_id == "btn-conference":
        details = "Detaillierte Informationen zum Konferenzbeitrag: [Ergebnisse und Analysen ...]"
    else:
        details = ""
    return html.Div([html.P(details)]), {"display": "block"}

@app.callback(
    Output("bachelor-modal", "is_open"),
    [Input("btn-bachelor", "n_clicks"), Input("modal-close", "n_clicks")],
    [State("bachelor-modal", "is_open")]
)
def toggle_bachelor_modal(n1, n2, is_open):
    if n1 or n2:
        return not is_open
    return is_open

# ---------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------
if __name__ == "__main__":
    app.run_server(debug=True, host="192.168.0.13")
