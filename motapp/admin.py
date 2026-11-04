from django.contrib import admin
from .models import Moto, Marca, Categoria, InfoEmpresa

@admin.register(Moto)
class MotoAdmin(admin.ModelAdmin):
    # Campos que se mostrarán en la tabla de lista
    list_display = ('nombre', 'marca', 'precio', 'cilindraje', 'stock', 'destacado', 'anio')
    
    # Define cuáles de estos campos actúan como enlace para abrir la vista de edición
    list_display_links = ('nombre',)
    
    # Agrega filtros laterales para facilitar la búsqueda
    list_filter = ('marca', 'destacado', 'anio')
    
    # Agrega una barra de búsqueda en la parte superior
    search_fields = ('nombre', 'marca__nombre')

# Registra los demás modelos si lo requieres
admin.site.register(Marca)
admin.site.register(Categoria)
admin.site.register(InfoEmpresa)