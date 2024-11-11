# Sistema de Administración de Datos para CEDICA

**Estado del Proyecto**: En Desarrollo 🚧

Este es un proyecto en desarrollo de una aplicación web para CEDICA, una organización que requiere un sistema de gestión integral para sus operaciones. El sistema permitirá la administración eficiente de datos críticos, tales como pagos, recibos, clientes, empleados, y caballos, entre otros.

---

## Sobre el Proyecto

La aplicación está diseñada para proporcionar una plataforma centralizada que facilite la administración de información sensible y los procesos de negocio de CEDICA. Al utilizar herramientas y tecnologías avanzadas, este sistema busca ser seguro, robusto, y escalable.

### Funcionalidades Actuales

- **Gestión de Usuarios**: Sistema de acceso seguro para usuarios autorizados.
- **Autenticación y Seguridad**: Bcrypt se utiliza para la encriptación de datos confidenciales, garantizando la seguridad de la información sensible de los usuarios.
- **Estructura de Base de Datos Compleja**: PostgreSQL se ha elegido como sistema de gestión de bases de datos (DBMS) debido a su rendimiento y soporte para estructuras de datos avanzadas.
- **Sistema de Almacenamiento de Archivos**: MinIO se utiliza para el almacenamiento seguro de archivos complementarios relacionados con los datos de los usuarios y operaciones.

### Tecnologías y Herramientas Utilizadas

- **Lenguaje de Programación**: Python
- **Framework Web**: Flask
- **ORM**: SQLAlchemy, para simplificar las operaciones con la base de datos
- **DBMS**: PostgreSQL
- **Almacenamiento de Archivos**: MinIO (Compatible con AWS S3)
- **Encriptación**: Bcrypt, para la seguridad de datos sensibles

## Estructura del Proyecto

El sistema se estructura en diversos módulos, cada uno diseñado para una funcionalidad específica dentro de la administración de CEDICA. Actualmente, la aplicación está centrada en la funcionalidad para usuarios autenticados y no incluye una página de inicio pública.

## Acceso al Proyecto en Línea

La aplicación está actualmente desplegada en un servidor público y accesible para visualización y pruebas en tiempo real. *https://admin-grupo03.proyecto2024.linti.unlp.edu.ar/*

Para acceder a la página de prueba, utiliza las siguientes credenciales de prueba:
-   Usuario: juan@gmail.com
-   Contraseña: 123a

> **Nota**: Aunque accesible, la aplicación sigue en desarrollo, y algunas funcionalidades podrían estar incompletas o presentar errores. Además, ten en cuenta que la base de datos contiene datos ficticios que pueden modificarse a través del enlace proporcionado, pero se reinicia periódicamente para mantener su estado de prueba.
