from django.shortcuts import render
from .models import Moto, Marca, Categoria, InfoEmpresa

def index_view(request):
    # Empresa y categorías
    empresa = InfoEmpresa.objects.first()
    categorias = Categoria.objects.all()
    marcas = Marca.objects.all()
    
    catalogo_agrupado = []
    for marca in marcas:
        motos_marca = Moto.objects.filter(marca=marca)
        if motos_marca.exists():
            catalogo_agrupado.append({
                'marca_nombre': marca.nombre,
                'motos': motos_marca
            })
            
    context = {
        'empresa': empresa,
        'categorias': categorias,
        'marcas': marcas,
        'catalogo_agrupado': catalogo_agrupado,
    }
    return render(request, 'motapp/index.html', context)

def financiacion_view(request):
    return render(request, 'motapp/financiacion.html')

def contrato_view(request):
    return render(request, 'motapp/contrato.html')

def ayuda_view(request):
    return render(request, 'motapp/ayuda.html')

from django.shortcuts import render

def contrato_dinamico_view(request):
    # Estos datos pueden venir por parámetros GET desde el modal o formulario
    nombre = request.GET.get('nombre', 'Nombre del Cliente')
    cedula = request.GET.get('cedula', 'Cédula')
    moto = request.GET.get('moto', 'Modelo de Moto')
    color = request.GET.get('color', 'Color')
    precio = float(request.GET.get('precio', 7299000))
    cuota_inicial = float(request.GET.get('cuota_inicial', 1000000))
    
    monto_financiado = precio - cuota_inicial

    context = {
        'nombre': nombre,
        'cedula': cedula,
        'moto': moto,
        'color': color,
        'precio': precio,
        'cuota_inicial': cuota_inicial,
        'monto_financiado': monto_financiado,
    }
    return render(request, 'motapp/contrato_dinamico.html', context)