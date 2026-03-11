JAZZMIN_SETTINGS = {
    # Título de la página (aparece en la pestaña del navegador)
    "site_title": "SafeLab Panel",
    
    # Título en la barra de inicio de sesión
    "site_header": "SafeLab Admin",
    
    # Título en la pantalla de inicio de sesión
    "site_brand": "SafeLab Labs",
    
    
    # Logo para el formulario de inicio de sesión en modo claro
    "login_logo_dark": None,
    
    
    # Texto de bienvenida
    "welcome_sign": "Welcome to SafeLab Admin Panel",
    
    # Copyright
    "copyright": "SafeLab © 2024",
    
    # Buscador
    "search_model": ["auth.User", "clients.Client"],
    
    # Apps y modelos para mostrar en el menú
    "topmenu_links": [
        # Enlaces que aparecen en la parte superior
        {"name": "Start", "url": "admin:index", "permissions": ["auth.view_user"]},
        {"name": "Website", "url": "/", "new_window": True},
        {"model": "auth.User"},
        {"app": "clients"},
    ],
    
    # Menú de usuario (parte superior derecha)
    "usermenu_links": [
        {"name": "Soporte", "url": "https://github.com/farridav/django-jazzmin/issues", "new_window": True},
        {"model": "auth.user"}
    ],
    
    # Iconos para modelos/apps
    "icons": {
        "auth": "fas fa-users-cog",
        "auth.user": "fas fa-user",
        "auth.Group": "fas fa-users",
        "admin.LogEntry": "fas fa-file",
        
        # Tus apps
        "inventory.Campus": "fas fa-globe",
        "inventory.Component": "fas fa-cogs",
        "inventory.Equipment": "fas fa-tools",
        "inventory.Glassware": "fas fa-tools",
        "inventory.Laboratory": "fas fa-flag",
        "inventory.Reagent": "fas fa-tasks",


        "orders.Order": "fas fa-shopping-cart",
        "orders.Product": "fas fa-shopping-cart",
        "orders.Supplier": "fas fa-shopping-cart",

        "reports.Report": "fas fa-user-tie",
    },
    
    # Iconos por defecto
    "default_icon_parents": "fas fa-chevron-circle-right",
    "default_icon_children": "fas fa-circle",
    
    # Permisos
    "permissions": {
        "custom_link": ["auth.view_user"],
    },
}