import dash
from dash import html, dcc
import dash_bootstrap_components as dbc

# Register this page so it is available at /passivhaus
dash.register_page(__name__, path="/passivhaus", name="Passivhaus Konzept A+")

layout = dbc.Container([
    dbc.Card([
        dbc.CardBody([
            html.H1("Passivhaus Konzept – A+ Erreicht", className="text-center mb-4"),
            html.Hr(),
            html.P(
                "Dieses Projekt dokumentiert die Entwicklung eines innovativen Passivhauskonzepts, "
                "das den A+ Standard erreicht. Durch den Einsatz von hochwertiger Dämmung, einer extrem luftdichten "
                "Gebäudehülle und effizienten Wärmerückgewinnungssystemen wird der Heizwärmebedarf drastisch reduziert – "
                "sodass konventionelle Heizsysteme weitestgehend überflüssig werden.",
                className="lead"
            ),
            html.P(
                "Die umfangreichen Analysen und Simulationen belegen, dass dieses Konzept sowohl ökologisch als auch "
                "ökonomisch überzeugt und einen signifikanten Beitrag zur Senkung des Energieverbrauchs leistet.",
                className="mb-4"
            ),
            # Make sure to include the corresponding image in your assets folder.
            html.Img(src="/assets/passivhaus_example.jpg", className="img-fluid mb-4", alt="Passivhaus Konzept A+"),
            # Link to return to the project overview
            dcc.Link("Zurück zur Projektübersicht", href="/?tab=tab-projekte", className="btn btn-secondary mt-3")
        ])
    ], className="my-card", style={"margin": "20px"})
], fluid=True)
