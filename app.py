import os
import urllib.parse
from datetime import datetime
from flask import Flask, redirect, request

app = Flask(__name__)

# --- CONFIGURACIÓN DE TUS DATOS ---
TELEFONO = "51960881208"
MENSAJE_TEXTO = "Buen día, deseo solicitar activar mi cuenta  de MyLOFT.\nMi correo institucional es: "

# Codificar el mensaje para la URL de WhatsApp
MENSAJE_REWRITE = urllib.parse.quote(MENSAJE_TEXTO)
WHATSAPP_URL = f"https://wa.me/{TELEFONO}?text={MENSAJE_REWRITE}"
LOG_FILE = "registro_visitas.txt"


def generar_qr(url_servidor):
    """Genera el código QR apuntando a tu servidor."""
    import qrcode

    qr = qrcode.QRCode(version=1, box_size=10, border=5)
    qr.add_data(url_servidor)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    img.save("codigo_qr_whatsapp.png")
    print(
        "¡QR Generado con éxito! Revisa el archivo 'codigo_qr_whatsapp.png'."
    )


# --- RUTA DEL CONTADOR Y REDIRECCIÓN ---
@app.route("/")
def escanear_qr():
    # 1. Obtener fecha y hora actual
    ahora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # 2. Registrar la visita en el archivo de texto
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(f"[{ahora}] - Nuevo escaneo registrado desde el QR.\n")

    # 3. Redirigir inmediatamente al usuario a su WhatsApp
    return redirect(WHATSAPP_URL)


# --- RUTA PARA QUE TÚ VEAS LAS ESTADÍSTICAS ---
@app.route("/metricas")
def ver_metricas():
    if not os.path.exists(LOG_FILE):
        return "<h3>Aún no hay visitas registradas.</h3>"

    with open(LOG_FILE, "r", encoding="utf-8") as f:
        lineas = f.readlines()

    total_visitas = len(lineas)

    # Mostrar un reporte web sencillo
    html = f"<h2>Estadísticas de tu QR de WhatsApp</h2>"
    html += f"<p><strong>Total de escaneos/visitas:</strong> {total_visitas}</p>"
    html += "<h3>Historial de accesos:</h3><ul>"
    for linea in reversed(lineas):  # Mostrar las más recientes primero
        html += f"<li>{linea.strip()}</li>"
    html += "</ul>"

    return html


if __name__ == "__main__":
    # Generar un QR local temporal de prueba
    generar_qr("http://localhost:5000")
    app.run(debug=True, port=5000)