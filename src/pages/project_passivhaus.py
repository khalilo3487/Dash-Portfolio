import dash
from dash import html, dcc
import dash_bootstrap_components as dbc

# Register the page so it becomes accessible at /passivhaus
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
                "Im Rahmen der Planung wurden umfangreiche Simulationen und Analysen durchgeführt, um die strengen "
                "energetischen Anforderungen zu erfüllen. Die Ergebnisse belegen, dass das Konzept sowohl "
                "ökologisch als auch ökonomisch überzeugt und einen signifikanten Beitrag zur Reduzierung des Energieverbrauchs leistet.",
                className="mb-4"
            ),
            # If you have an image in your assets folder, reference it here.
            html.Img(src="/assets/passivhaus_example.jpg", className="img-fluid mb-4", alt="Passivhaus Konzept A+"),
            dcc.Link("Zurück zur Projektübersicht", href="/", className="btn btn-secondary mt-3")
        ])
    ], className="my-card", style={"margin": "20px"})
], fluid=True)

