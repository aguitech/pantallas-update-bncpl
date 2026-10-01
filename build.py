#!/usr/bin/env python3
"""
build.py — Genera TODAS las HTMLs de pantallas a partir de un spec dict.
Cine Financiero / BanCoppel / Afore Coppel
"""
import json
import os
import sys
from pathlib import Path

BASE = Path(__file__).parent.resolve()

CSS_LINK = '<link rel="stylesheet" href="assets/styles.css">'
FONTS = '<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;800;900&display=swap" rel="stylesheet">'

# ============== TEMPLATES ==============

def header_html(label, section_eyebrow=None):
    """Header común: logos BanCoppel / Afore Coppel + label de la estación."""
    return f"""
  <header class="app-header">
    <div class="brand">
      <div class="brand-logo">
        <span class="dots"><span class="dot"></span><span class="dot"></span><span class="dot"></span></span>
        BanCoppel.
      </div>
      <div class="brand-divider"></div>
      <div class="brand-logo">
        <span class="dots"><span class="dot"></span><span class="dot"></span><span class="dot"></span></span>
        Afore Coppel.
      </div>
    </div>
    <div class="section-tag">
      <span class="clapper">🎬</span> {label}
    </div>
  </header>"""

FOOTER_HTML = """
  <footer class="app-footer">
    <span class="pill"><span class="ico">🛡️</span> Tu información está protegida. Consulta el Aviso de privacidad.</span>
    <span class="pill"><span class="ico">💡</span> TIP DEL DIRECTOR — Tú eres el protagonista.</span>
  </footer>"""


def page(title, body_inner, header_label="FORO · 3"):
    """Envoltura común a todas las pantallas."""
    return f"""<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{title}</title>
  {CSS_LINK}
  {FONTS}
</head>
<body>
{header_html(header_label)}
  <main>
    <div class="screen">
      <div class="screen-inner">
{body_inner}
      </div>
    </div>
  </main>
{FOOTER_HTML}
</body>
</html>
"""


def stepper(steps, active_idx):
    """Renderiza un stepper tipo 1-2-3-4 con el paso active_idx activo."""
    out = ['<div class="stepper">']
    for i, s in enumerate(steps):
        if i > 0:
            out.append('<div class="line' + (' active' if i <= active_idx else '') + '"></div>')
        cls = 'active' if i == active_idx else ('done' if i < active_idx else '')
        out.append(f'<div class="step {cls}">{s}</div>')
    out.append('</div>')
    return '\n'.join(out)


def camera_frame(with_check=True):
    """Vista de cámara/enfoque con persona."""
    check = '<div class="check">✓</div>' if with_check else ''
    return f"""
<div class="camera-frame">
  <div class="hair"></div>
  <div class="face"></div>
  <div class="eyes"><span></span><span></span></div>
  <div class="smile"></div>
  <div class="corner tl"></div>
  <div class="corner tr"></div>
  <div class="corner bl"></div>
  <div class="corner br"></div>
  {check}
</div>"""


def countdown(active_idx=2):
    """Cuenta regresiva 3·2·1 con active_idx resaltado (1-based: 3→idx 2)."""
    circles = []
    for i, n in enumerate(['3', '2', '1']):
        cls = 'active' if (i + 1) == active_idx else ''
        circles.append(f'<div class="circle {cls}">{n}</div>')
    return '<div class="countdown" id="countdown">' + ''.join(circles) + '</div>'


def director_row(tag_label, bubble_text):
    """Avatar del Director IA + burbuja de diálogo."""
    return f"""
<div class="director-row">
  <div class="director-avatar">👨‍💼</div>
  <div>
    <span class="director-tag">{tag_label}</span>
    <div class="director-bubble">{bubble_text}</div>
  </div>
</div>"""


def opciones_abc(options, selected=None):
    """Lista de opciones A/B/C para preguntas. options = [('A', 'texto'), ...]"""
    out = ['<div class="opciones">']
    for letra, texto in options:
        sel = ' selected' if selected == letra else ''
        out.append(f"""
<div class="opcion{sel}" data-opcion="{letra}">
  <div class="letra">{letra}</div>
  <div class="texto">{texto}</div>
</div>""")
    out.append('</div>')
    return '\n'.join(out)


# ============== SPEC DE PANTALLAS ==============

# Estructura:
# output_dir/
#   ├── index.html         (especial)
#   ├── 0.01-bienvenida.html
#   ├── ...
# Pantallas tienen: filename, header_label, eyebrow, title, subtitle, body_html, prev, next

# Para no saturar, defino cada pantalla en bloques concisos:

PANTALLAS = []

def add(filename, header_label, eyebrow, title, subtitle, body, prev=None, next_=None):
    PANTALLAS.append({
        'filename': filename,
        'header_label': header_label,
        'eyebrow': eyebrow,
        'title': title,
        'subtitle': subtitle,
        'body': body,
        'prev': prev,
        'next': next_,
    })


# =============== ESTACIÓN 0 · PRERREGISTRO ===============
E0 = 'PRERREGISTRO'

add('0.01-bienvenida.html', E0, '0.01 · Bienvenida',
    'Crea tu película',
    'Antes de comenzar tu experiencia, necesitamos conocerte un poco. Tus respuestas nos ayudarán a crear una experiencia hecha para ti.',
    director_row('DIRECTOR IA',
                 'Hola, soy tu Director IA. Estoy aquí para acompañarte a crear tu propia película financiera.')
    + '<div class="instr">🛡 Tu información está segura. La usaremos solo para personalizar tu experiencia y tu película financiera.</div>'
    + '<a class="btn btn-yellow btn-block" href="0.02-consentimiento.html">COMENZAR MI PRE-REGISTRO ›</a>',
    next_='0.02-consentimiento.html')

add('0.02-consentimiento.html', E0, '0.02 · Consentimiento',
    'Aviso de privacidad',
    'Consulta el Aviso de privacidad y los términos de participación.',
    stepper(['1', '2', '3', '4'], 0)
    + '<div style="font-weight:700; color:var(--c-azul-900); margin:8px 0;">Prerregistro</div>'
    + '<label class="checkbox-row"><input type="checkbox"> <span>Acepto los términos para participar en la experiencia.</span></label>'
    + '<label class="checkbox-row"><input type="checkbox"> <span>Autorizo uso promocional de mi imagen (opcional).</span></label>'
    + '<a class="btn btn-yellow btn-block" href="0.03-datos.html">ACEPTAR Y CONTINUAR</a>',
    prev='0.01-bienvenida.html', next_='0.03-datos.html')

add('0.03-datos.html', E0, '0.03 · Datos',
    'Queremos conocerte',
    'Cuéntanos lo esencial para personalizar tu experiencia.',
    stepper(['1', '2', '3', '4'], 1)
    + '<div style="font-weight:700; color:var(--c-azul-900); margin:8px 0;">Datos</div>'
    + '<div class="field"><label>Nombre</label><input value="Arturo"></div>'
    + '<div class="field"><label>Correo</label><input placeholder="Tu correo electrónico"></div>'
    + '<div class="field"><label>Edad</label><input placeholder="Tu edad"></div>'
    + '<a class="btn btn-yellow btn-block" href="0.04-meta.html">CONTINUAR</a>',
    prev='0.02-consentimiento.html', next_='0.04-meta.html')

# 0.04 a 0.07 preguntas 1-4 con avatar del director al lado
def pregunta_meta(num, label, pregunta_txt, placeholder, prev_file, next_file):
    return {
        'body': stepper(['1', '2', '3', '4'], 2)
        + '<div style="font-weight:700; color:var(--c-azul-900); margin:8px 0;">Crea tu película</div>'
        + f'<div class="director-row"><div class="director-avatar">👨‍💼</div>'
        + f'<div><span class="director-tag">DIRECTOR IA</span>'
        + f'<div class="director-bubble">{label}<br><br><strong>{pregunta_txt}</strong></div></div></div>'
        + f'<div class="field"><input placeholder="{placeholder}"></div>'
        + f'<a class="btn btn-yellow btn-block" href="{next_file}">CONTINUAR</a>'
    }

add('0.04-meta.html', E0, '0.04 · Meta',
    'Crea tu película',
    'Es momento de construir tu película financiera. Para ello, responde las siguientes preguntas.',
    pregunta_meta(
        'Es momento de construir tu película financiera. Para ello, responde las siguientes preguntas.',
        '1/5 ¿Qué deseo te gustaría lograr?',
        '¿Qué deseo te gustaría lograr?',
        'Viajar',
        '0.03-datos.html',
        '0.05-lugar.html'
    )['body'],
    prev='0.03-datos.html', next_='0.05-lugar.html')

add('0.05-lugar.html', E0, '0.05 · Lugar',
    'Crea tu película',
    'Imagina el escenario donde te gustaría vivir esta historia.',
    stepper(['1', '2', '3', '4'], 2)
    + '<div style="font-weight:700; color:var(--c-azul-900); margin:8px 0;">Crea tu película</div>'
    + '<div class="director-row"><div class="director-avatar">👨‍💼</div>'
    + '<div><span class="director-tag">DIRECTOR IA</span>'
    + '<div class="director-bubble">Imagina el escenario donde te gustaría vivir esta historia.<br><br><strong>2/5 ¿En dónde sucede tu película?</strong></div></div></div>'
    + '<div class="field"><input placeholder="En las playas de Tailandia"></div>'
    + '<a class="btn btn-yellow btn-block" href="0.06-acompanantes.html">CONTINUAR</a>',
    prev='0.04-meta.html', next_='0.06-acompanantes.html')

add('0.06-acompanantes.html', E0, '0.06 · Acompañantes',
    'Crea tu película',
    'Piensa en las personas que harían especial esta experiencia.',
    stepper(['1', '2', '3', '4'], 2)
    + '<div style="font-weight:700; color:var(--c-azul-900); margin:8px 0;">Crea tu película</div>'
    + '<div class="director-row"><div class="director-avatar">👨‍💼</div>'
    + '<div><span class="director-tag">DIRECTOR IA</span>'
    + '<div class="director-bubble">Piensa en las personas que harían especial esta experiencia.<br><br><strong>3/5 ¿Con quién quieres compartir tu historia?</strong></div></div></div>'
    + '<div class="field"><input placeholder="Con mi familia"></div>'
    + '<a class="btn btn-yellow btn-block" href="0.07-final-feliz.html">CONTINUAR</a>',
    prev='0.05-lugar.html', next_='0.07-final-feliz.html')

add('0.07-final-feliz.html', E0, '0.07 · Final feliz',
    'Crea tu película',
    'Ahora visualiza ese momento en el que tu sueño ya se hizo realidad.',
    stepper(['1', '2', '3', '4'], 2)
    + '<div style="font-weight:700; color:var(--c-azul-900); margin:8px 0;">Crea tu película</div>'
    + '<div class="director-row"><div class="director-avatar">👨‍💼</div>'
    + '<div><span class="director-tag">DIRECTOR IA</span>'
    + '<div class="director-bubble">Ahora visualiza ese momento en el que tu sueño ya se hizo realidad.<br><br><strong>4/5 ¿Cuál sería tu final feliz?</strong></div></div></div>'
    + '<div class="field"><input placeholder="Con mi familia"></div>'
    + '<a class="btn btn-yellow btn-block" href="0.08-herramientas.html">CONTINUAR</a>',
    prev='0.06-acompanantes.html', next_='0.08-herramientas.html')

add('0.08-herramientas.html', E0, '0.08 · Herramientas',
    'Crea tu película',
    '5/5 Elige tus 3 herramientas financieras',
    stepper(['1', '2', '3', '4'], 2)
    + '<div style="font-weight:700; color:var(--c-azul-900); margin:8px 0;">3 DE 3 SELECCIONADAS</div>'
    + '<div class="opciones">'
    + '<div class="opcion selected"><div class="letra">✓</div><div class="texto"><strong>Plan financiero</strong><br>Diseña un plan con tus ingresos y gastos.</div></div>'
    + '<div class="opcion"><div class="letra">✓</div><div class="texto"><strong>Ahorro</strong><br>Reserva una parte de tus ingresos cada mes.</div></div>'
    + '<div class="opcion selected"><div class="letra">✓</div><div class="texto"><strong>Fondo para imprevistos</strong><br>Ten listo un colchón para emergencias.</div></div>'
    + '</div>'
    + '<a class="btn btn-yellow btn-block" href="0.09-revision.html">CONTINUAR</a>',
    prev='0.07-final-feliz.html', next_='0.09-revision.html')

add('0.09-revision.html', E0, '0.09 · Revisión',
    '¡Listo! ¡Tenemos el guión de tu película!',
    'Arturo, este es el resumen de tu historia.',
    stepper(['1', '2', '3', '4'], 3)
    + '<div class="instr" style="margin: 14px 0;">'
    + '<strong>Tu historia:</strong> Arturo quiere viajar con su familia a las playas de Tailandia.<br><br>'
    + '<strong>Mis herramientas son:</strong><br>'
    + '• Plan financiero<br>'
    + '• Ahorro<br>'
    + '• Fondo para imprevistos<br><br>'
    + '<strong>Correo y edad:</strong> datos capturados'
    + '</div>'
    + '<a class="btn btn-yellow btn-block" href="0.10-pase.html">CREAR MI PASE</a>',
    prev='0.08-herramientas.html', next_='0.10-pase.html')

add('0.10-pase.html', E0, '0.10 · Pase de Rodaje',
    '¡Tenemos historia!',
    'Guarda este código para continuar tu experiencia.',
    stepper(['1', '2', '3', '4'], 3)
    + '<div class="qr-placeholder"></div>'
    + '<div style="text-align:center; font-size:18px; font-weight:800; color:var(--c-azul-900); margin-top:14px;">ARTURO</div>'
    + '<div style="text-align:center; font-size:13px; color:var(--c-texto-s); margin-bottom:14px;">Folio: CF-2026-4587</div>'
    + '<div class="instr">Muestra este QR en cualquier estación para retomar tu experiencia.</div>'
    + '<a class="btn btn-yellow btn-block" href="0.11-ir-casting.html">CONTINUAR A CASTING</a>',
    prev='0.09-revision.html', next_='0.11-ir-casting.html')

add('0.11-ir-casting.html', E0, '0.11 · Ir a Casting',
    '¡Tu prerregistro está listo!',
    'Tu Director IA te espera en el casting.',
    '<div style="font-size:80px; text-align:center; margin:20px 0;">✅</div>'
    + '<div class="instr">Acércate a la estación de Casting y muestra tu Pase de Rodaje al staff.</div>'
    + '<a class="btn btn-yellow btn-block" href="1.01-escaneo.html">IR A CASTING</a>',
    prev='0.10-pase.html', next_='1.01-escaneo.html')


# =============== ESTACIÓN 1 · CASTING ===============
E1 = 'CASTING'

add('1.01-escaneo.html', E1, '1.01 · Escaneo',
    'Bienvenido a tu Casting',
    'Aquí expondrás el guión de tu película y tomaremos la foto para tu póster.',
    director_row('CASTING', 'Acerca tu QR a la cámara para continuar.')
    + '<div class="qr-placeholder" style="margin: 20px auto;"></div>'
    + '<div style="text-align:center; color:var(--c-azul-700); font-weight:600; font-size:14px;">Muestra aquí el QR de tu pase</div>'
    + '<a class="btn btn-yellow btn-block" href="1.02-guion.html">CONTINUAR</a>',
    prev='0.11-ir-casting.html', next_='1.02-guion.html')

add('1.02-guion.html', E1, '1.02 · Guión',
    '¿Estás listo?',
    'Antes de grabar una película se debe presentar un casting. Por ello en la siguiente pantalla aparecerá tu historia y deberás leerla en voz alta.',
    '<div style="text-align:center; font-size:60px; margin:20px 0;">🎬</div>'
    + '<div style="height:3px; width:60px; background:var(--c-amarillo); margin:0 auto 18px;"></div>'
    + '<a class="btn btn-yellow btn-block" href="1.03-narracion.html">VER MI GUIÓN</a>',
    prev='1.01-escaneo.html', next_='1.03-narracion.html')

add('1.03-narracion.html', E1, '1.03 · Narración',
    'Lee en voz alta el guión de tu película',
    'Esta lectura no se graba. Tómate tu tiempo.',
    '<div style="font-style:italic; font-size:17px; color:var(--c-azul-900); border-left:4px solid var(--c-amarillo); padding:14px 22px; margin:20px 0; background:var(--c-azul-100); border-radius:6px;">'
    + '"Soy Arturo. Mi película es un viaje con mi familia, sucede en Tailandia. Y mi final feliz es disfrutar juntos del viaje."'
    + '</div>'
    + '<div class="instr">Esta lectura no se graba.</div>'
    + '<a class="btn btn-yellow btn-block" href="1.04-hero-shot.html">CONTINUAR A MI FOTO</a>',
    prev='1.02-guion.html', next_='1.04-hero-shot.html')

add('1.04-hero-shot.html', E1, '1.04 · Hero Shot',
    'Toma tu foto para el póster de tu película',
    'Mira a la cámara y mantén tu rostro dentro del encuadre.',
    camera_frame(with_check=True)
    + '<div style="text-align:center; margin-top:18px;">'
    + '<a class="btn btn-yellow btn-block" href="1.05-cuenta.html">CAPTURAR</a>'
    + '</div>',
    prev='1.03-narracion.html', next_='1.05-cuenta.html')

add('1.05-cuenta.html', E1, '1.05 · 3, 2, 1',
    'Mira a la cámara ¿Estás listo?',
    'El conteo 3, 2, 1 termina con la captura automática.',
    '<div style="position:relative;">'
    + camera_frame(with_check=False)
    + '<div style="position:absolute; top:50%; left:50%; transform:translate(-50%, -50%); background:rgba(10,26,74,0.85); color:#fff; width:100px; height:100px; border-radius:50%; display:flex; align-items:center; justify-content:center; font-size:54px; font-weight:800;">3</div>'
    + '</div>'
    + '<div style="text-align:center; margin-top:18px;">'
    + '<a class="btn btn-yellow btn-block" href="1.06-confirmar.html">CONTINUAR</a>'
    + '</div>',
    prev='1.04-hero-shot.html', next_='1.06-confirmar.html')

add('1.06-confirmar.html', E1, '1.06 · Confirmar foto',
    '¡Ya tenemos tu foto!',
    'Esta será la imagen que aparecerá en el póster de tu película.',
    camera_frame(with_check=True)
    + '<div style="text-align:center; margin-top:18px;">'
    + '<a class="btn btn-yellow btn-block" href="1.07-caracterizacion.html">CONFIRMAR FOTO</a>'
    + '</div>',
    prev='1.05-cuenta.html', next_='1.07-caracterizacion.html')

add('1.07-caracterizacion.html', E1, '1.07 · Ir a Caracterización',
    '¡Tu casting está completo!',
    'Pasa a la siguiente estación para caracterizarte.',
    '<div style="text-align:center; font-size:60px; margin:20px 0;">🎬</div>'
    + '<div style="height:3px; width:60px; background:var(--c-amarillo); margin:0 auto 18px;"></div>'
    + '<div class="instr">Nuestro equipo te ayudará a elegir un accesorio y te acompañará al foro de grabación.</div>'
    + '<a class="btn btn-yellow btn-block" href="3.01-bienvenida.html">FINALIZAR CASTING</a>',
    prev='1.06-confirmar.html', next_='3.01-bienvenida.html')


# =============== ESTACIÓN 3 · FORO / PREPARACIÓN ===============
E3 = 'FORO · 3'

add('3.01-bienvenida.html', E3, '3.01 · Bienvenida',
    'Vas a grabar 3 ESCENAS',
    'Colócate sobre la marca frente al croma y mira a esta pantalla. En unos segundos comenzaremos con la escena 1 de 3.',
    director_row('DIRECTOR IA', 'Colócate sobre la marca frente al croma y mira a esta pantalla. En unos segundos comenzaremos con la escena 1 de 3.')
    + '<a class="btn btn-yellow btn-block" href="3.02-reconocimiento.html">CONTINUAR</a>',
    prev='1.07-caracterizacion.html', next_='3.02-reconocimiento.html')

add('3.02-reconocimiento.html', E3, '3.02 · Reconocimiento',
    'Tu reconocimiento fue exitoso',
    'Alinea tu posición: rostro al centro, mirada a la cámara, pies sobre la marca.',
    '<div style="display:grid; grid-template-columns:1fr 1fr; gap:24px; align-items:center;">'
    + '<div>'
    + '<div class="eyebrow">3.02 · Reconocimiento</div>'
    + '<h1 class="title">Tu reconocimiento fue exitoso</h1>'
    + '<ul style="padding-left:18px; color:var(--c-texto); font-size:14px; line-height:1.8;">'
    + '<li>Alinea tu posición</li>'
    + '<li>Rostro al centro de la pantalla</li>'
    + '<li>Mira hacia la cámara</li>'
    + '<li>Pies sobre la marca del suelo</li>'
    + '</ul>'
    + '<a class="btn btn-yellow" href="3.03-escaneo.html" style="margin-top:14px;">CONTINUAR</a>'
    + '</div>'
    + '<div>' + camera_frame(with_check=True) + '</div>'
    + '</div>',
    prev='3.01-bienvenida.html', next_='3.03-escaneo.html')

add('3.03-escaneo.html', E3, '3.03 · Escaneo / Falla',
    'Escanea tu Pase de Rodaje',
    'Acerca el QR a la cámara para continuar.',
    '<div style="display:grid; grid-template-columns:1fr 1fr; gap:24px; align-items:center;">'
    + '<div>'
    + '<div class="eyebrow">3.03 · Escaneo</div>'
    + '<h1 class="title">Escanea tu Pase de Rodaje</h1>'
    + '<p class="subtitle">Acerca el QR a la cámara para continuar.</p>'
    + '<a class="btn btn-yellow" href="3.04-instrucciones.html">CONTINUAR</a>'
    + '</div>'
    + '<div style="text-align:center;">'
    + '<div class="qr-placeholder"></div>'
    + '<div style="font-weight:700; color:var(--c-azul-700); margin-top:10px;">ACERCA TU CÓDIGO AQUÍ</div>'
    + '</div>'
    + '</div>',
    prev='3.02-reconocimiento.html', next_='3.04-instrucciones.html')

add('3.04-instrucciones.html', E3, '3.04 · Instrucciones',
    'Así grabarás cada escena',
    'Sigue estos 3 pasos para cada escena. Una sola toma por escena, sin repetir.',
    director_row('DIRECTOR IA', 'Lee la frase. Actúa la emoción indicada. Espera el conteo y grábalo.')
    + '<div style="margin:16px 0; padding:14px; background:var(--c-amarillo-1); border-radius:10px; color:var(--c-azul-900); font-weight:700;">'
    + '📌 Una sola toma por escena, sin repetir.'
    + '</div>'
    + '<a class="btn btn-yellow btn-block" href="3.05-cuenta-1.html">CONTINUAR</a>',
    prev='3.03-escaneo.html', next_='3.05-cuenta-1.html')

add('3.05-cuenta-1.html', E3, '3.05 · Cuenta 1',
    'En posición… ¡vamos a comenzar!',
    'Prepárate para la escena 1.',
    countdown(active_idx=3)
    + '<div class="look-cam">MIRA DIRECTAMENTE A LA CÁMARA</div>'
    + '<a class="btn btn-yellow btn-block" href="3.06-posicionamiento.html">CONTINUAR</a>',
    prev='3.04-instrucciones.html', next_='3.06-posicionamiento.html')

add('3.06-posicionamiento.html', E3, '3.06 · Posicionamiento',
    'Prepárate para tu primera escena',
    'Grabarás 3 escenas de tu película en las que usarás las herramientas financieras que elegiste al inicio.',
    '<div style="display:grid; grid-template-columns:1fr 1fr; gap:24px; align-items:center;">'
    + '<div>'
    + '<div class="eyebrow">3.06 · Posicionamiento</div>'
    + '<h1 class="title">Prepárate para tu primera escena</h1>'
    + '<p class="subtitle">Grabarás 3 escenas de tu película en las que usarás las herramientas financieras que elegiste al inicio. Sigue las instrucciones y trata de memorizarlas ya que las necesitarás después.</p>'
    + '<a class="btn btn-yellow" href="3.07-cuenta-2.html">CONTINUAR</a>'
    + '</div>'
    + '<div>' + camera_frame(with_check=True) + '</div>'
    + '</div>',
    prev='3.05-cuenta-1.html', next_='3.07-cuenta-2.html')

add('3.07-cuenta-2.html', E3, '3.07 · Cuenta 2',
    'En posición… ¡vamos a comenzar!',
    'Cuenta regresiva antes de la primera grabación.',
    countdown(active_idx=2)
    + '<div class="look-cam">MIRA DIRECTAMENTE A LA CÁMARA</div>'
    + '<a class="btn btn-yellow btn-block" href="3.08-guion-1.html">INICIAR GRABACIÓN</a>',
    prev='3.06-posicionamiento.html', next_='3.08-guion-1.html')

add('3.08-guion-1.html', E3, '3.08 · Guion 1',
    'ESCENA 1 DE 3',
    'Lee esta frase con la emoción indicada.',
    '<span class="escena-tag">ESCENA 1 DE 3</span> <span class="emocion-tag">RISA DE VILLANO</span>'
    + '<blockquote class="quote">"Planea tus gastos mes a mes, y olvídate del estrés"</blockquote>'
    + '<div class="instr">Lee esta frase con la emoción indicada.</div>'
    + '<a class="btn btn-yellow btn-block" href="3.09-cuenta-3.html">CONTINUAR</a>',
    prev='3.07-cuenta-2.html', next_='3.09-cuenta-3.html')

add('3.09-cuenta-3.html', E3, '3.09 · Cuenta 3',
    'En posición… ¡vamos a comenzar!',
    'Cuenta regresiva antes de la grabación.',
    countdown(active_idx=1)
    + '<div class="look-cam">MIRA DIRECTAMENTE A LA CÁMARA</div>'
    + '<a class="btn btn-yellow btn-block" href="3.10-grabacion-1.html">INICIAR GRABACIÓN</a>',
    prev='3.08-guion-1.html', next_='3.10-grabacion-1.html')


# =============== ESTACIÓN 3 · GRABACIÓN ===============
add('3.10-grabacion-1.html', E3, '3.10 · Grabación 1',
    'ESCENA 1 DE 3 · GRABANDO',
    'Mantén tu mirada a cámara y continúa.',
    '<div style="display:flex; gap:12px; align-items:center;">'
    + '<span class="escena-tag">ESCENA 1 DE 3</span>'
    + '<span class="rec-hud"><span class="dot"></span> GRABANDO</span>'
    + '<span class="timer" id="timer">00:00:00</span>'
    + '</div>'
    + '<blockquote class="quote">"Planea tus gastos mes a mes, y olvídate del estrés"</blockquote>'
    + '<div class="instr">Mantén tu mirada a cámara y continúa.</div>'
    + '<a class="btn btn-yellow btn-block" href="3.11-clip-1.html">DETENER Y GUARDAR</a>'
    + '<script>'
    + '(function(){var t=document.getElementById("timer"),s=0;setInterval(function(){s++;var h=String(Math.floor(s/3600)).padStart(2,"0"),m=String(Math.floor((s%3600)/60)).padStart(2,"0"),ss=String(s%60).padStart(2,"0");t.textContent=h+":"+m+":"+ss;},1000);})();'
    + '</script>',
    prev='3.09-cuenta-3.html', next_='3.11-clip-1.html')

add('3.11-clip-1.html', E3, '3.11 · Clip 1 guardado',
    '¡CORTE! · ESCENA 1 GUARDADA',
    'Prepárate para tu siguiente escena.',
    director_row('ESCENA 1 DE 3', '¡CORTE! Tu escena 1 ha sido guardada. Continuamos con la escena 2.')
    + '<div class="corte" style="margin-top:8px;"><span class="badge">¡CORTE!</span> ESCENA 1 GUARDADA</div>'
    + '<div class="instr" style="margin-top:14px;">Continuamos con la escena 2.</div>'
    + '<a class="btn btn-yellow btn-block" href="3.12-guion-2.html">SIGUIENTE ESCENA</a>',
    prev='3.10-grabacion-1.html', next_='3.12-guion-2.html')

add('3.12-guion-2.html', E3, '3.12 · Guion 2',
    'ESCENA 2 DE 3',
    'Lee esta frase con la emoción indicada.',
    '<span class="escena-tag">ESCENA 2 DE 3</span> <span class="emocion-tag">MISTERIOSO</span>'
    + '<blockquote class="quote">"Ahorro dinero poco a poco y alcanzarás tus deseos pronto."</blockquote>'
    + '<div class="instr">Lee esta frase con la emoción indicada.</div>'
    + '<a class="btn btn-yellow btn-block" href="3.13-cuenta-4.html">CONTINUAR</a>',
    prev='3.11-clip-1.html', next_='3.13-cuenta-4.html')

add('3.13-cuenta-4.html', E3, '3.13 · Cuenta 4',
    'En posición… ¡vamos a comenzar!',
    'Cuenta regresiva antes de la grabación 2.',
    countdown(active_idx=2)
    + '<div class="look-cam">MIRA DIRECTAMENTE A LA CÁMARA</div>'
    + '<a class="btn btn-yellow btn-block" href="3.14-grabacion-2.html">INICIAR GRABACIÓN</a>',
    prev='3.12-guion-2.html', next_='3.14-grabacion-2.html')

add('3.14-grabacion-2.html', E3, '3.14 · Grabación 2',
    'ESCENA 2 DE 3 · GRABANDO',
    'Mantén tu mirada a cámara y continúa.',
    '<div style="display:flex; gap:12px; align-items:center;">'
    + '<span class="escena-tag">ESCENA 2 DE 3</span>'
    + '<span class="rec-hud"><span class="dot"></span> GRABANDO</span>'
    + '<span class="timer" id="timer">00:00:00</span>'
    + '</div>'
    + '<blockquote class="quote">"Ahorro dinero poco a poco y alcanzarás tus deseos pronto."</blockquote>'
    + '<div class="instr">Mantén tu mirada a cámara y continúa.</div>'
    + '<a class="btn btn-yellow btn-block" href="3.15-clip-2.html">DETENER Y GUARDAR</a>'
    + '<script>'
    + '(function(){var t=document.getElementById("timer"),s=0;setInterval(function(){s++;var h=String(Math.floor(s/3600)).padStart(2,"0"),m=String(Math.floor((s%3600)/60)).padStart(2,"0"),ss=String(s%60).padStart(2,"0");t.textContent=h+":"+m+":"+ss;},1000);})();'
    + '</script>',
    prev='3.13-cuenta-4.html', next_='3.15-clip-2.html')

add('3.15-clip-2.html', E3, '3.15 · Clip 2 guardado',
    '¡CORTE! · ESCENA 2 GUARDADA',
    'Continuamos con la escena 3.',
    director_row('ESCENA 2 DE 3', '¡CORTE! Tu escena 2 ha sido guardada. Continuamos con la escena 3.')
    + '<div class="corte" style="margin-top:8px;"><span class="badge">¡CORTE!</span> ESCENA 2 GUARDADA</div>'
    + '<div class="instr" style="margin-top:14px;">Continuamos con la escena 3.</div>'
    + '<a class="btn btn-yellow btn-block" href="3.16-guion-3.html">SIGUIENTE ESCENA</a>',
    prev='3.14-grabacion-2.html', next_='3.16-guion-3.html')

add('3.16-guion-3.html', E3, '3.16 · Guion 3',
    'ESCENA 3 DE 3',
    'Lee esta frase con la emoción indicada.',
    '<span class="escena-tag">ESCENA 3 DE 3</span> <span class="emocion-tag">PROFESIONAL</span>'
    + '<blockquote class="quote">"Para un imprevisto tengo un ahorro listo."</blockquote>'
    + '<div class="instr">Lee esta frase con la emoción indicada.</div>'
    + '<a class="btn btn-yellow btn-block" href="3.17-cuenta-5.html">CONTINUAR</a>',
    prev='3.15-clip-2.html', next_='3.17-cuenta-5.html')

add('3.17-cuenta-5.html', E3, '3.17 · Cuenta 5',
    'En posición… ¡vamos a comenzar!',
    'Última cuenta regresiva.',
    countdown(active_idx=1)
    + '<div class="look-cam">MIRA DIRECTAMENTE A LA CÁMARA</div>'
    + '<a class="btn btn-yellow btn-block" href="3.18-grabacion-3.html">INICIAR GRABACIÓN</a>',
    prev='3.16-guion-3.html', next_='3.18-grabacion-3.html')

add('3.18-grabacion-3.html', E3, '3.18 · Grabación 3',
    'ESCENA 3 DE 3 · GRABANDO',
    'Mantén tu mirada a cámara y continúa.',
    '<div style="display:flex; gap:12px; align-items:center;">'
    + '<span class="escena-tag">ESCENA 3 DE 3</span>'
    + '<span class="rec-hud"><span class="dot"></span> GRABANDO</span>'
    + '<span class="timer" id="timer">00:00:00</span>'
    + '</div>'
    + '<blockquote class="quote">"Para un imprevisto tengo un ahorro listo."</blockquote>'
    + '<div class="instr">Mantén tu mirada a cámara y continúa.</div>'
    + '<a class="btn btn-yellow btn-block" href="3.19-clip-3.html">DETENER Y GUARDAR</a>'
    + '<script>'
    + '(function(){var t=document.getElementById("timer"),s=0;setInterval(function(){s++;var h=String(Math.floor(s/3600)).padStart(2,"0"),m=String(Math.floor((s%3600)/60)).padStart(2,"0"),ss=String(s%60).padStart(2,"0");t.textContent=h+":"+m+":"+ss;},1000);})();'
    + '</script>',
    prev='3.17-cuenta-5.html', next_='3.19-clip-3.html')

add('3.19-clip-3.html', E3, '3.19 · Clip 3 guardado',
    '¡CORTE! · ESCENA 3 GUARDADA',
    '¡Has terminado tus ensayos! Tus tres herramientas continúan contigo.',
    director_row('DIRECTOR IA', '¡Has terminado tus ensayos! Tus tres herramientas continúan contigo.')
    + '<div class="corte" style="margin-top:8px;"><span class="badge">¡CORTE!</span> ESCENA 3 GUARDADA</div>'
    + '<div class="instr" style="margin-top:14px;">¡Has terminado! Pasa a Decisiones para poner en práctica lo aprendido.</div>'
    + '<a class="btn btn-yellow btn-block" href="3.20-ir-decisiones.html">IR A DECISIONES</a>',
    prev='3.18-grabacion-3.html', next_='3.20-ir-decisiones.html')

add('3.20-ir-decisiones.html', E3, '3.20 · Ir a Decisiones',
    'Recuerda las escenas que grabaste',
    'Pasa a Decisiones para poner en práctica lo aprendido.',
    director_row('DIRECTOR IA', 'Recuerda las escenas que grabaste y pasa a la siguiente estación para ponerlas a prueba.')
    + '<div class="instr" style="margin-top:14px;">Pasa a Decisiones para poner en práctica lo aprendido.</div>'
    + '<a class="btn btn-yellow btn-block" href="4.01-escaneo.html">IR A DECISIONES</a>',
    prev='3.19-clip-3.html', next_='4.01-escaneo.html')


# =============== ESTACIÓN 4 · DECISIONES ===============
E4 = 'DECISIONES · 4'

add('4.01-escaneo.html', E4, '4.01 · Escaneo',
    'Escanea tu Pase de Rodaje',
    'Acerca el QR a la cámara para continuar.',
    '<div style="display:grid; grid-template-columns:1fr 1fr; gap:24px; align-items:center;">'
    + '<div>'
    + '<div class="eyebrow">4.01 · Escaneo</div>'
    + '<h1 class="title">Escanea tu<br>Pase de Rodaje</h1>'
    + '<p class="subtitle">Acerca el QR a la cámara para continuar.</p>'
    + '</div>'
    + '<div style="text-align:center;">'
    + '<div class="qr-placeholder"></div>'
    + '<div style="font-weight:700; color:var(--c-azul-700); margin-top:10px;">ACERCA TU CÓDIGO AQUÍ</div>'
    + '</div>'
    + '</div>'
    + '<div style="margin-top:18px;">'
    + '<a class="btn btn-yellow btn-block" href="4.02-rumbo.html">CONTINUAR</a>'
    + '</div>',
    prev='3.20-ir-decisiones.html', next_='4.02-rumbo.html')

add('4.02-rumbo.html', E4, '4.02 · El rumbo de tu película',
    'AHORA TÚ DECIDES EL RUMBO DE TU PELÍCULA',
    'Enfrentarás 3 situaciones. Usa lo que aprendiste durante el rodaje y elige cómo actuar.',
    '<div style="display:flex; justify-content:center; gap:32px; margin:30px 0;">'
    + '<div style="text-align:center;"><div style="font-size:54px;">🎬</div><div style="font-weight:800; color:var(--c-azul-900); font-size:24px;">1</div></div>'
    + '<div style="text-align:center;"><div style="font-size:54px;">🪑</div><div style="font-weight:800; color:var(--c-azul-900); font-size:24px;">2</div></div>'
    + '<div style="text-align:center;"><div style="font-size:54px;">🍿</div><div style="font-weight:800; color:var(--c-azul-900); font-size:24px;">3</div></div>'
    + '</div>'
    + '<div style="text-align:center; color:var(--c-azul-700); font-weight:800; letter-spacing:1px; margin-bottom:20px;">3 ESCENAS · 3 DECISIONES</div>'
    + '<a class="btn btn-yellow btn-block" href="4.03-pregunta-1.html">COMENZAR ›</a>',
    prev='4.01-escaneo.html', next_='4.03-pregunta-1.html')

add('4.03-pregunta-1.html', E4, '4.03 · Pregunta 1',
    'DECISIÓN 1 DE 3',
    'Quieres convertir tu sueño en meta. ¿Cuál es el secreto para hacer un presupuesto exitoso?',
    '<span class="decision-badge">DECISIÓN 1 DE 3</span>'
    + '<p style="font-weight:700; color:var(--c-azul-900); margin-bottom:14px;">Quieres convertir tu sueño en meta. ¿Cuál es el secreto para hacer un presupuesto exitoso?</p>'
    + opciones_abc([
        ('A', 'Registrar detalladamente cada gasto que hiciste durante el mes.'),
        ('B', 'Recortar al máximo los gastos para ahorrar más.'),
        ('C', 'Diseñar un plan con mis ingresos y gastos y apegarse a él.'),
    ])
    + '<a class="btn btn-disabled btn-block" href="4.04-confirmar-1.html">ELIGE LA RESPUESTA CORRECTA</a>',
    prev='4.02-rumbo.html', next_='4.04-confirmar-1.html')

add('4.04-confirmar-1.html', E4, '4.04 · Confirmar decisión 1',
    'DECISIÓN 1 DE 3',
    '¿Confirmas tu respuesta?',
    '<span class="decision-badge">DECISIÓN 1 DE 3</span>'
    + '<p style="font-weight:700; color:var(--c-azul-900); margin-bottom:14px;">¿Cuál es el secreto para hacer un presupuesto exitoso?</p>'
    + opciones_abc([
        ('A', 'Registrar detalladamente cada gasto que hiciste durante el mes.'),
        ('B', 'Recortar al máximo los gastos para ahorrar más.'),
        ('C', 'Diseñar un plan con mis ingresos y gastos y apegarse a él.'),
    ], selected='C')
    + '<a class="btn btn-yellow btn-block" href="4.05-consecuencia-1.html">CONFIRMAR MI DECISIÓN</a>',
    prev='4.03-pregunta-1.html', next_='4.05-consecuencia-1.html')

add('4.05-consecuencia-1.html', E4, '4.05 · Consecuencia 1',
    '¡Toma buena!',
    'Planeas, tomas el control y te olvidas del estrés.',
    '<span class="decision-badge" style="background:var(--c-verde); color:#fff;">C · ¡TOMA BUENA!</span>'
    + '<p style="font-weight:700; color:var(--c-azul-900); margin-bottom:14px;">Planeas, tomas el control y te olvidas del estrés.</p>'
    + '<div class="feedback-box bad"><strong>A — Incorrecto</strong>Registrar gastos es mirar al pasado. El presupuesto es planear antes de usar tu dinero.</div>'
    + '<div class="feedback-box bad"><strong>B — Incorrecto</strong>Un plan muy estricto es difícil de mantener. La clave es el equilibrio, no la prohibición.</div>'
    + '<div class="feedback-box ok"><strong>C — ¡Correcto!</strong>Diseñar un plan con tus ingresos y gastos es la base del presupuesto exitoso.</div>'
    + '<a class="btn btn-yellow btn-block" href="4.06-pregunta-2.html">SIGUIENTE DECISIÓN</a>',
    prev='4.04-confirmar-1.html', next_='4.06-pregunta-2.html')

add('4.06-pregunta-2.html', E4, '4.06 · Pregunta 2',
    'DECISIÓN 2 DE 3',
    'Tienes una meta clara por cumplir. ¿Cómo organizas tu dinero cuando lo recibes?',
    '<span class="decision-badge">DECISIÓN 2 DE 3</span>'
    + '<p style="font-weight:700; color:var(--c-azul-900); margin-bottom:14px;">Tienes una meta clara por cumplir. ¿Cómo organizas tu dinero cuando lo recibes?</p>'
    + opciones_abc([
        ('A', 'Primero separo lo que quiero ahorrar, lo demás lo gasto.'),
        ('B', 'Primero gasto y lo que sobre se ahorra.'),
        ('C', 'Celebro invitando a todos a comer.'),
    ])
    + '<a class="btn btn-disabled btn-block" href="4.07-confirmar-2.html">ELIGE UNA RESPUESTA</a>',
    prev='4.05-consecuencia-1.html', next_='4.07-confirmar-2.html')

add('4.07-confirmar-2.html', E4, '4.07 · Confirmar decisión 2',
    'DECISIÓN 2 DE 3',
    '¿Confirmas tu respuesta?',
    '<span class="decision-badge">DECISIÓN 2 DE 3</span>'
    + '<p style="font-weight:700; color:var(--c-azul-900); margin-bottom:14px;">¿Cómo organizas tu dinero cuando lo recibes?</p>'
    + opciones_abc([
        ('A', 'Primero separo lo que quiero ahorrar, lo demás lo gasto.'),
        ('B', 'Primero gasto y lo que sobre se ahorra.'),
        ('C', 'Celebro invitando a todos a comer.'),
    ], selected='A')
    + '<a class="btn btn-yellow btn-block" href="4.08-consecuencia-2.html">CONFIRMAR MI DECISIÓN</a>',
    prev='4.06-pregunta-2.html', next_='4.08-consecuencia-2.html')

add('4.08-consecuencia-2.html', E4, '4.08 · Consecuencia 2',
    '¡Toma buena!',
    'Separar el ahorro desde el principio garantiza que logres avanzar hacia tu meta.',
    '<span class="decision-badge" style="background:var(--c-verde); color:#fff;">A · ¡TOMA BUENA!</span>'
    + '<p style="font-weight:700; color:var(--c-azul-900); margin-bottom:14px;">Separar el ahorro desde el principio garantiza que logres avanzar hacia tu meta.</p>'
    + '<div class="feedback-box bad"><strong>B — Incorrecto</strong>Si esperas a ver qué sobra, otros gastos pueden llevarse ese dinero.</div>'
    + '<div class="feedback-box bad"><strong>C — Incorrecto</strong>Es bueno celebrar, pero separar tu ahorro es clave para premios más grandes.</div>'
    + '<div class="feedback-box ok"><strong>A — ¡Correcto!</strong>Primero separar el ahorro garantiza que avances hacia tu meta.</div>'
    + '<a class="btn btn-yellow btn-block" href="4.09-pregunta-3.html">SIGUIENTE DECISIÓN</a>',
    prev='4.07-confirmar-2.html', next_='4.09-pregunta-3.html')

add('4.09-pregunta-3.html', E4, '4.09 · Pregunta 3',
    'DECISIÓN 3 DE 3',
    'Estás ahorrando para tu sueño y aparece un gasto urgente e inesperado. ¿Cómo lo pagas?',
    '<span class="decision-badge">DECISIÓN 3 DE 3</span>'
    + '<p style="font-weight:700; color:var(--c-azul-900); margin-bottom:14px;">Estás ahorrando para tu sueño y aparece un gasto urgente e inesperado. ¿Cómo lo pagas?</p>'
    + opciones_abc([
        ('A', 'Uso mi fondo separado para emergencias.'),
        ('B', 'Uso el dinero destinado para mi meta.'),
        ('C', 'Pido un crédito.'),
    ])
    + '<a class="btn btn-disabled btn-block" href="4.10-confirmar-3.html">ELIGE UNA RESPUESTA</a>',
    prev='4.08-consecuencia-2.html', next_='4.10-confirmar-3.html')

add('4.10-confirmar-3.html', E4, '4.10 · Confirmar decisión 3',
    'DECISIÓN 3 DE 3',
    '¿Confirmas tu respuesta?',
    '<span class="decision-badge">DECISIÓN 3 DE 3</span>'
    + '<p style="font-weight:700; color:var(--c-azul-900); margin-bottom:14px;">¿Cómo lo pagas?</p>'
    + opciones_abc([
        ('A', 'Uso mi fondo separado para emergencias.'),
        ('B', 'Uso el dinero destinado para mi meta.'),
        ('C', 'Pido un crédito.'),
    ], selected='C')
    + '<a class="btn btn-yellow btn-block" href="4.11-consecuencia-3.html">CONFIRMAR MI DECISIÓN</a>',
    prev='4.09-pregunta-3.html', next_='4.11-consecuencia-3.html')

add('4.11-consecuencia-3.html', E4, '4.11 · Consecuencia 3',
    '¡Corte!',
    'Resolverías la emergencia, pero retrasarías tu meta.',
    '<span class="decision-badge" style="background:var(--c-rojo); color:#fff;">C · ¡CORTE!</span>'
    + '<p style="font-weight:700; color:var(--c-azul-900); margin-bottom:14px;">Resolverías la emergencia, pero retrasarías tu meta.</p>'
    + '<div class="feedback-box ok"><strong>A — Correcto</strong>Tener un fondo para imprevistos te protege sin endeudarte ni sacarte de tus metas.</div>'
    + '<div class="feedback-box bad"><strong>C — ¡Cuidado!</strong>Endeudarte hace que la emergencia te salga más cara.</div>'
    + '<a class="btn btn-yellow btn-block" href="4.12-enviar-produccion.html">CONTINUAR</a>',
    prev='4.10-confirmar-3.html', next_='4.12-enviar-produccion.html')

add('4.12-enviar-produccion.html', E4, '4.12 · Enviar a producción',
    'TUS DECISIONES YA FORMAN PARTE DE TU PELÍCULA',
    'Tu historia ya tiene un rumbo.',
    stepper(['1', '2', '3'], 2)  # all done
    + '<div style="display:flex; gap:12px; justify-content:center; margin:18px 0;">'
    + '<span style="background:var(--c-verde); color:#fff; padding:6px 12px; border-radius:6px; font-weight:800; font-size:13px;">✓ DECISIÓN 1</span>'
    + '<span style="background:var(--c-verde); color:#fff; padding:6px 12px; border-radius:6px; font-weight:800; font-size:13px;">✓ DECISIÓN 2</span>'
    + '<span style="background:var(--c-verde); color:#fff; padding:6px 12px; border-radius:6px; font-weight:800; font-size:13px;">✓ DECISIÓN 3</span>'
    + '</div>'
    + '<div class="feedback-box ok" style="font-size:15px; text-align:center;"><strong>3 DE 3 DECISIONES REGISTRADAS</strong>Tu historia ya tiene un rumbo.</div>'
    + '<a class="btn btn-yellow btn-block" href="4.13-producir.html">ENVIAR A PRODUCCIÓN ›</a>',
    prev='4.11-consecuencia-3.html', next_='4.13-producir.html')

add('4.13-producir.html', E4, '4.13 · Producir mi película',
    'TU HISTORIA ESTÁ LISTA PARA CONVERTIRSE EN PELÍCULA',
    'Tus escenas y decisiones ya están registradas. Solo falta dar la orden final.',
    '<span class="decision-badge">PRODUCCIÓN</span>'
    + '<p style="font-weight:700; color:var(--c-azul-900); margin-bottom:14px;">Tus escenas y decisiones ya están registradas. Solo falta dar la orden final.</p>'
    + '<div style="display:flex; justify-content:center; gap:24px; margin:24px 0;">'
    + '<div style="text-align:center;"><div style="font-size:48px;">🎬</div><div style="font-weight:800; color:var(--c-verde); font-size:14px;">ESCENAS ✓</div></div>'
    + '<div style="text-align:center;"><div style="font-size:48px;">🪑</div><div style="font-weight:800; color:var(--c-verde); font-size:14px;">DECISIONES ✓</div></div>'
    + '<div style="text-align:center;"><div style="font-size:48px;">🎥</div><div style="font-weight:800; color:var(--c-verde); font-size:14px;">HISTORIA ✓</div></div>'
    + '</div>'
    + '<a class="btn btn-yellow btn-block" href="6.01-correo.html">PRODUCIR MI PELÍCULA ››</a>',
    prev='4.12-enviar-produccion.html', next_='6.01-correo.html')


# =============== ESTACIÓN 6 · CORREO / CONTENIDOS ===============
E6 = 'CORREO · 6'

add('6.01-correo.html', E6, '6.01 · Recibes tu correo',
    '¡Tu película está lista!',
    'Gracias por vivir Cine Financiero. Tu foto de Premier y tu videoclip ya están disponibles.',
    '<div style="font-size:80px; text-align:center; margin:20px 0;">🎬</div>'
    + '<div class="instr" style="text-align:center;">También encontrarás tu folio y la encuesta de la experiencia.</div>'
    + '<a class="btn btn-yellow btn-block" href="6.02-contenidos.html">VER MIS CONTENIDOS</a>',
    prev='4.13-producir.html', next_='6.02-contenidos.html')

add('6.02-contenidos.html', E6, '6.02 · Abres tus contenidos',
    'Tu historia, para compartir',
    'Descarga tu video, tu foto y tu cartel.',
    '<h2 style="font-size:20px; font-weight:800; color:var(--c-azul-900); margin:18px 0 8px;">Tu historia, para compartir</h2>'
    + '<div style="background:var(--c-azul-900); border-radius:12px; aspect-ratio:16/9; display:flex; align-items:center; justify-content:center; margin-bottom:14px;">'
    + '<div style="width:64px; height:64px; background:var(--c-amarillo); border-radius:50%; display:flex; align-items:center; justify-content:center; font-size:30px; color:var(--c-azul-900);">▶</div>'
    + '</div>'
    + '<a class="btn btn-yellow btn-block" href="6.02-contenidos.html">VER / DESCARGAR VIDEO</a>'
    + '<h2 style="font-size:20px; font-weight:800; color:var(--c-azul-900); margin:24px 0 8px;">Tu foto de Premier</h2>'
    + '<div style="background:linear-gradient(135deg, #e8edf5, #d0d8e8); height:160px; border-radius:10px; display:flex; align-items:center; justify-content:center; font-size:54px;">📸</div>'
    + '<div style="text-align:right; margin:6px 0 18px;"><a href="6.02-contenidos.html" style="color:var(--c-azul-700); font-weight:700;">DESCARGAR FOTO ›</a></div>'
    + '<a href="6.02-contenidos.html" style="color:var(--c-azul-700); font-weight:700; display:block; margin-bottom:18px;">Descargar mi cartel</a>'
    + '<a class="btn btn-yellow btn-block" href="6.03-folio.html">RECIBIR MI GIVEAWAY</a>'
    + '<div style="text-align:center; margin-top:14px;"><a href="7.01-invitacion.html" style="color:var(--c-azul-700); font-weight:700;">Responder la encuesta ›</a></div>',
    prev='6.01-correo.html', next_='6.03-folio.html')

add('6.03-folio.html', E6, '6.03 · Muestras tu folio',
    'Tu obsequio te espera',
    'Muestra este folio al staff para recibir tu giveaway.',
    '<div style="text-align:center; margin:30px 0;">'
    + '<div style="font-size:60px;">🎁</div>'
    + '<div style="background:var(--c-azul-100); border:2px dashed var(--c-azul-500); padding:20px 30px; border-radius:12px; display:inline-block; font-size:24px; font-weight:800; color:var(--c-azul-900); margin-top:14px;">'
    + 'CF-2026-4587'
    + '</div>'
    + '<div style="font-weight:800; color:var(--c-azul-700); margin-top:14px; letter-spacing:1.5px;">PENDIENTE DE ENTREGA</div>'
    + '</div>'
    + '<div class="instr" style="text-align:center;">La encuesta es voluntaria. Tu obsequio es independiente.</div>'
    + '<a class="btn btn-yellow btn-block" href="7.01-invitacion.html">CONTINUAR</a>',
    prev='6.02-contenidos.html', next_='7.01-invitacion.html')


# =============== ESTACIÓN 7 · ENCUESTA ===============
E7 = 'ENCUESTA'

add('7.01-invitacion.html', E7, '7.01 · Invitación',
    '¡Cuéntanos qué te pareció!',
    'Tu opinión es muy valiosa para nosotros.',
    '<h1 class="title" style="text-align:center;">¡Cuéntanos qué te pareció!</h1>'
    + '<div style="height:3px; width:60px; background:var(--c-amarillo); margin:0 auto 18px;"></div>'
    + '<p class="subtitle" style="text-align:center;">¿Te gustó grabar tu película financiera? Tu opinión es muy valiosa para nosotros.</p>'
    + '<a class="btn btn-yellow btn-block" href="7.02-encuesta.html">RESPONDER ENCUESTA</a>'
    + '<div style="text-align:center; margin-top:14px;"><a href="index.html" style="color:var(--c-azul-700); font-weight:700;">AHORA NO</a></div>',
    prev='6.03-folio.html', next_='7.02-encuesta.html')

add('7.02-encuesta.html', E7, '7.02 · Encuesta',
    'Cuéntanos qué te pareció',
    '¿Cómo calificas la experiencia?',
    '<p style="font-weight:700; color:var(--c-azul-900); margin-bottom:8px;">¿Cómo calificas la experiencia?</p>'
    + '<div class="stars">'
    + '<span>★</span><span>★</span><span>★</span><span>★</span><span>★</span>'
    + '</div>'
    + '<p style="font-weight:700; color:var(--c-azul-900); margin:18px 0 8px;">¿Qué parte te gustó más?</p>'
    + '<div class="opciones">'
    + '<div class="opcion"><div class="letra">1</div><div class="texto">Casting</div></div>'
    + '<div class="opcion"><div class="letra">2</div><div class="texto">Rodaje</div></div>'
    + '<div class="opcion"><div class="letra">3</div><div class="texto">Decisiones</div></div>'
    + '<div class="opcion"><div class="letra">4</div><div class="texto">Premiere</div></div>'
    + '</div>'
    + '<a class="btn btn-yellow btn-block" href="index.html">ENVIAR RESPUESTAS</a>',
    prev='7.01-invitacion.html', next_='index.html')


# ============== BUILD ==============

def build():
    for p in PANTALLAS:
        nav = ''
        if p['prev']:
            nav += f'<a class="btn btn-blue" style="margin-right:8px;" href="{p["prev"]}">‹ Anterior</a>'
        if p['next']:
            nav += f'<a class="btn btn-yellow" href="{p["next"]}">Siguiente ›</a>'
        nav_html = f'<div style="margin-top:24px; display:flex; justify-content:space-between; gap:8px;">{nav}</div>' if nav else ''

        body_inner = f'''
        <div class="eyebrow">{p["eyebrow"]}</div>
        <h1 class="title">{p["title"]}</h1>
        <h2 class="subtitle">{p["subtitle"]}</h2>
        {p["body"]}
        {nav_html}
'''
        html = page(p['title'], body_inner, header_label=p['header_label'])
        out = HTML / p['filename']
        out.write_text(html)
        print(f"  ✓ {p['filename']}")


def build_index():
    # Agrupar por estación
    estaciones = {}
    for p in PANTALLAS:
        key = p['header_label']
        estaciones.setdefault(key, []).append(p)

    cards = []
    for label, plist in estaciones.items():
        cards.append(f'<h2 style="margin-top:32px; color:var(--c-azul-900); font-size:18px; letter-spacing:2px; font-weight:800;">{label}</h2>')
        for p in plist:
            cards.append(f'''
<a class="flow-card" href="{p["filename"]}">
  <span class="station-label">{p["header_label"]}</span>
  <div class="num">{p["eyebrow"].split("·")[0].strip()}</div>
  <h3>{p["title"]}</h3>
  <p>{p["subtitle"][:80]}{"…" if len(p["subtitle"]) > 80 else ""}</p>
</a>''')
        cards.append('</div><div class="flow-grid">')

    body_inner = f'''
    <div class="eyebrow">Cine Financiero</div>
    <h1 class="title">Flujo de pantallas · Cine Financiero</h1>
    <h2 class="subtitle">Réplicas HTML de las {len(PANTALLAS)} pantallas del recorrido del visitante por estación.</h2>
    <div class="flow-grid">
{''.join(cards)}
    </div>
'''
    html = page('Inicio · Cine Financiero', body_inner, header_label='🎬 RECORRIDO')
    out = HTML / 'index.html'
    out.write_text(html)
    print(f"  ✓ index.html ({len(PANTALLAS)} pantallas)")


HTML = BASE

if __name__ == '__main__':
    build_index()
    build()
    print(f"\n✅ {len(PANTALLAS) + 1} HTMLs generadas en {HTML}")