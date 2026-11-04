import os
from django.core.files import File
from django.conf import settings
from django.core.management.base import BaseCommand
from django.utils.text import slugify
from motapp.models import Marca, Categoria, Moto, InfoEmpresa

class Command(BaseCommand):
    help = 'Puebla la base de datos y vincula automáticamente las imágenes disponibles'

    def handle(self, *args, **kwargs):
        self.stdout.write('Iniciando sincronización automática del catálogo...')

        # 1. Categoría y Empresa por defecto
        cat_general, _ = Categoria.objects.get_or_create(
            nombre='General', 
            defaults={'descripcion': 'Categoría general de motocicletas'}
        )
        if not InfoEmpresa.objects.exists():
            InfoEmpresa.objects.create(nombre="Financiera Motos Colombia Crediservi")

        # Directorio físico de imágenes filtrando solo archivos de imagen reales
        dir_motos = os.path.join(settings.MEDIA_ROOT, 'motos')
        if os.path.exists(dir_motos):
            archivos_disponibles = [
                f for f in os.listdir(dir_motos) 
                if os.path.isfile(os.path.join(dir_motos, f)) and f.lower().endswith(('.png', '.jpg', '.jpeg', '.webp'))
            ]
        else:
            archivos_disponibles = []
        # 2. Catálogo completo con nombres flexibles
        # 3. Catálogo completo sincronizado con todas las variantes de color
        catalogo_completo = [
            ('BAJAJ BOXER', [
                ('Bajaj Boxer CT100 KS', 5899000, ['boxerct100negra.png', 'boxerct100roja.png', 'boxerct100azul.png', 'boxerct100gris.png', 'boxerct100amarillo.png', 'Boxer CT100 KS.png']),
                ('Bajaj Boxer CT100 ES Boxer Racing', 6399000, ['Boxer CT100 ES Boxer Racingnegrorojo.png', 'Boxer CT100 ES Boxer Racingnegrogris.png']),
                ('Bajaj Boxer CT100 KS Racing', 5999000, ['Boxer CT100 KS Boxer Raciningnegra-rojo.png', 'CT100-KS-Boxer-Racining-gris.png']),
                ('Bajaj Boxer CT100 ES', 6199000, ['Boxer-CT100-ESnegro.png', 'Boxer-CT100-ESroja.png', 'Boxer-CT100-ESazul.png', 'boxerct100morado.png']),
                ('Bajaj Boxer CT125 Sport', 6899000, ['Boxer CT125 Sportgris.png', 'Boxer CT125 Sportnegro.png', 'Boxer CT125 Sportrojo.png', 'Boxer CT125 Sportazul.png']),
                ('Bajaj Boxer 150X', 7499000, ['boxer 150xnegro.png', 'Boxer 150Xamarillo.png', 'Boxer 150Xazul.png']),
            ]),
            ('BAJAJ PULSAR', [
                ('Bajaj Pulsar N125 Carburada', 7599000, ['Pulsar N125 Carburadamorda.png', 'Pulsar N125 Carburadaverde.png', 'Pulsar N125 Carburadaroja.png']),
                ('Bajaj Pulsar N125 FI', 8099000, ['Pulsar N125 FIgris.png', 'Pulsar N125 FImorado.png', 'Pulsar N125 FIverde.png', 'Pulsar N125 FIrojo.png']),
                ('Bajaj Pulsar N160 Pro', 10999000, ['Pulsar N160 Pronegro.png', 'Pulsar N160 Proazulpetroleo.png', 'Pulsar N160 Progris.png', 'Pulsar N160 Pronegrocristal.png']),
                ('Bajaj Pulsar NS 125', 8799000, ['Pulsar NS 125negra.png', 'Pulsar NS 125rojo.png', 'Pulsar NS 125azul.png']),
                ('Bajaj Pulsar NS 160 Fi ABS', 11199000, ['Pulsar NS 160 Fi ABSrojomerlot.png', 'Pulsar NS 160 Fi ABSGris Onix.png', 'Pulsar NS 160 Fi ABSnegrozafiro.png', 'Pulsar NS 160 Fi ABSnegrocristal.png']),
                ('Bajaj Pulsar NS200 FI ABS DC', 15799000, ['Pulsar NS200 FI ABS DCMercury Bluet.png', 'Pulsar NS200 FI ABS DCRojo Merlot.png', 'Pulsar NS200 FI ABS DCGris Onix.png', 'Pulsar NS200 FI ABS DCNegro Zafiro.png', 'Pulsar NS200 FI ABS DCNegro Cristal.png']),
                ('Bajaj Pulsar NS200 FI ABS SC', 13199000, ['Pulsar NS200 FI ABS SCMercury Bluet.png', 'Pulsar NS200 FI ABS SCRojo Merlot.png', 'Pulsar NS200 FI ABS SCGris Onix.png', 'Pulsar NS200 FI ABS SCNegro Zafiro.png']),
                ('Bajaj Pulsar NS400Z', 18299000, ['Pulsar NS400ZBlanco metalizado.png', 'Pulsar NS400ZRojo Rancing.png', 'Pulsar NS400ZGris Mercurio.png', 'Pulsar NS400ZNegro Cristal.png']),
                ('Bajaj Pulsar P150', 8999000, ['Pulsar P150Azul.png', 'Pulsar P150Grisclaro.png', 'Pulsar P150grisoscuro.png']),
                ('Bajaj Pulsar RS 200 FI ABS', 15999000, ['Pulsar RS 200 FI ABSBlanco metalizado.png', 'Pulsar RS 200 FI ABSRojo.png', 'Pulsar RS 200 FI ABSNegro.png']),
            ]),
            ('BAJAJ DISCOVER', [
                ('Bajaj Discover 125 SPORT', 6999000, ['Discover 125 SPORTNaranja.png', 'Discover 125 SPORTAzul mercurio.png', 'Discover 125 SPORTazul.png', 'Discover 125 SPORTamarilo.png']),
            ]),
            ('BAJAJ DOMINAR', [
                ('Bajaj Dominar 250', 15799900, ['Dominar 250negromate.png', 'Dominar 250negro.png']),
                ('Bajaj Dominar 400 Touring', 19399000, ['Dominar 400 TouringAzul.png', 'Dominar 400 Touringnegro.png']),
                ('Bajaj Dominar 400 Volcano', 20399000, ['Dominar 400 VolcanoNEGRO.png']),
            ]),
            ('AKT', [
                ('AKT NKD 125 FP', 5890000, ['NKD 125 FPnegro.png']),
                ('AKT NKD 125', 4890000, ['NKD 125gris.png', 'NKD 125negro.png', 'NKD 125negrobrillante.png', 'NKD 125blanco.png', 'NKD 125grisbase.png']),
                ('AKT NKD 125 Classic', 5490000, ['NKD 125 Classicnegro.png']),
                ('AKT CHR 125', 5490000, ['CHR 125negro.png', 'CHR 125roja.png', 'CHR 125azul.png']),
                ('AKT CR4 150', 6999000, ['CR4 150gris.png', 'CR4 150negro.png']),
                ('AKT 250 R', 11590000, ['AKT 250 Rgris.png', 'AKT 250 Rnegroverde.png']),
                ('AKT CR4 125', 6590000, ['CR4 125gris.png', 'CR4 125negro.png']),
                ('AKT CR4 200 Pro', 8590000, ['CR4 200 Pronegromate.png', 'CR4 200 Progris.png', 'CR4 200 Pronegrobrillante.png']),
                ('AKT TTR 125', 7390000, ['TTR 125 NEGRA.png', 'TTR 125 BLANCA.png']),
                ('AKT TTR 200', 9190000, ['TTR 200 NEGRA.png', 'TTR 200 BLANCA.png']),
                ('AKT XRS 180', 13990000, ['XRS 180negro.png', 'XRS 180gris.png', 'XRS 180Blanco.png']),
            ]),
            ('AUTECO TVS Y APACHE', [
                ('AUTECO TVS RAIDER 125', 7299000, ['RAIDER 125NEGRA NEBULOSA.png', 'RAIDER 125VERDE SLATE.png']),
                ('AUTECO TVS APACHE 160 CARBURADA ABS', 9299000, ['APACHE 160 CARBURADA ABSNEGRO NEBULOSA - VERDE.png', 'APACHE 160 CARBURADA ABSGRISHUMO.png']),
                ('AUTECO TVS APACHE RTR 310', 27799000, ['APACHE RTR 310AMARILLO FURIA - NEGRA.png', 'APACHE RTR 310NEGRO ROJO.png']),
            ]),
            ('YAMAHA', [
                ('YAMAHA XTZ150', 14500000, ['XTZ150negra.png', 'XTZ150azul.png', 'XTZ150blanco.png', 'XTZ150Cafe.png']),
                ('YAMAHA XTZ250', 25900000, ['XT250negra.png', 'XTZ250blanco.png', 'XTZ250Rojo.png']),
                ('YAMAHA FZ VERSIÓN 3.0', 11800000, ['FZ VERSIÓN 3.0negra.png', 'FZ VERSIÓN 3.0azul.png', 'FZ VERSIÓN 3.0gris.png']),
                ('YAMAHA FZ25 ABS', 15300000, ['FZ25 ABSnegra.png', 'FZ25 ABSazul.png', 'FZ25 ABSverde.png']),
                ('YAMAHA MT15', 15500000, ['MT15negra.png', 'MT15Azul.png', 'MT15gris.png', 'MT15naranja.png']),
                ('YAMAHA MT03', 31900000, ['Mt03_2025_negra.png', 'MT03azul.png', 'MT03gris.png']),
                ('YAMAHA MT09', 63000000, ['MT09negra.png', 'MT09azul.png', 'MT09gris.png']),
            ]),
            ('HONDA', [
                ('HONDA CB 100 2027', 5700000, ['CB 100 2027negra.png', 'CB 100 2027azul.png', 'CB 100 2027roja.png']),
                ('HONDA CB 125F DLX 2027', 6499000, ['CB 125F DLX 2027rojo.png', 'CB 125F DLX 2027gris.png']),
                ('HONDA CB 190R 2.0 2027', 12499000, ['CB 190R 2.0 2027rojo.png', 'CB 190R 2.0 2027negro.png']),
                ('HONDA CB 300F 2027', 16800000, ['Nueva-CB-300F-rojo_3.webp', 'Nueva-CB-300F-azul-mate_3.webp', 'gris-mate-CB300F_3 (1).webp']),
                ('HONDA XR 150L 2.0 2027', 10190000, ['xr150l-r.png roja nuevo.png', 'xr150l-n-700x700.png negra nuevo.png', 'xr150l-b-700x700.png nuevo.png']),
                ('HONDA XR 190L 2.0 2027', 13500000, ['xr190l-r.png roja nueva.png', 'xr190l-beige-700x700.png nueva.png', 'xr190l-b-700x700.png blanco nueva.png']),
            ]),
            ('SUZUKI', [
                ('SUZUKI GN 160', 10130000, ['GN 160negra.png', 'GN 160gris.png', 'GN 160roja.png']),
                ('SUZUKI BURGMAN 15 AUTOMATICA', 15150000, ['BURGMAN-15-PLATEADA.png', 'BURGMAN-15-NEGRA.png', 'BURGMAN-15-BLANCA.png']),
                ('SUZUKI DR 160X ENDURO', 12599000, ['dr160azul.png', 'DR-160-NEGRA.png', 'DR-160-BLANCA.png', 'DR-160-ROJA.png']),
                ('SUZUKI GIXXER FI 150 ABS', 10990000, ['GIXXER FI 150 ABSazul.png', 'GIXXER FI 150 ABSroja.png', 'GIXXER FI 150 ABSnegra.png']),
                ('SUZUKI GIXXER 250', 14590000, ['GIXXER 250azul.png', 'GIXXER 250negro.png', 'GIXXER 250blanco.png']),
            ])
        ]
        for marca_nombre, motos in catalogo_completo:
            marca_obj, _ = Marca.objects.get_or_create(nombre=marca_nombre)

            for nombre_moto, precio_moto, posibles_nombres in motos:
                moto = Moto(
                    nombre=nombre_moto,
                    slug=slugify(nombre_moto),
                    marca=marca_obj,
                    categoria=cat_general,
                    cilindraje=150,
                    precio=precio_moto,
                    descripcion="Financiación directa disponible."
                )

                # Buscar cuál de los nombres posibles existe realmente en la carpeta
                archivo_encontrado = None
                for nombre_archivo in posibles_nombres:
                    if nombre_archivo in archivos_disponibles:
                        archivo_encontrado = nombre_archivo
                        break

                if archivo_encontrado:
                    ruta_imagen = os.path.join(dir_motos, archivo_encontrado)
                    with open(ruta_imagen, 'rb') as f:
                        moto.imagen_principal.save(archivo_encontrado, File(f), save=False)
                else:
                    # Si no encuentra coincidencia exacta, toma la primera imagen disponible en la carpeta para que no quede vacía
                    if archivos_disponibles:
                        archivo_comodin = archivos_disponibles[0]
                        ruta_imagen = os.path.join(dir_motos, archivo_comodin)
                        with open(ruta_imagen, 'rb') as f:
                            moto.imagen_principal.save(archivo_comodin, File(f), save=False)

                moto.save()

        self.stdout.write(self.style.SUCCESS('¡Catálogo poblado y sincronizado con éxito!'))

