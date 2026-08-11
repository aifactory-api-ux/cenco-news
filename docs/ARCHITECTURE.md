# CENCO NEWS - Arquitectura del Sistema

## Visión General

CENCO NEWS es una plataforma de inteligencia de noticias destinada a automatizar el ciclo de monitoreo, análisis, priorización y distribución de noticias relevantes para la toma de decisiones. El sistema garantiza una operación eficiente, robusta y trazable, cubriendo múltiples países e idiomas con un estricto control editorial.

## Componentes Principales

### Backend
- **API REST con FastAPI:** Servicio principal que ofrece puntos finales para la gestión de usuarios, fuentes de noticias, artículos, reportes, aprobaciones y más.
- **Base de Datos PostgreSQL:** Almacena toda la información estructurada del sistema con esquema relacional y migraciones gestionadas.
- **Redis:** Para almacenamiento en caché, sesiones y tasas de limitación.
- **Qdrant:** Motor de búsqueda vectorial para permitir búsquedas semánticas avanzadas en artículos.
- **RabbitMQ y Celery:** Gestión de colas y tareas asincrónicas distribuidas para recolección, procesamiento y análisis de datos.
- **Almacenamiento Compatible con S3:** Para guardar informes generados, documentos y archivos adjuntos.
- **Servicios de Reconocimiento y Síntesis de Voz:** Implementación de Speech-to-Text y Text-to-Speech para interfaces de voz.

### Frontend
- **React con TypeScript:** Interfaz de usuario para el Portal Principal, la Vista de Aprobación Editorial y el Panel de Administración.
- **TailwindCSS:** Estilos basados en tokens específicos para mantener consistencia visual.
- **React-Router-Dom, React-Query y Zustand:** Manejo avanzado de rutas, estados y datos.

### Infraestructura
- **Kubernetes:** Orquestación y despliegue de contenedores en entorno cloud gestionado.
- **Terraform:** Definición de Infraestructura como Código para provisión reproducible.
- **Prometheus, Grafana y Loki:** Observabilidad, monitoreo y gestión de logs.

## Interacción y Flujos

1. El sistema ingiere múltiples fuentes de noticias por RSS, APIs, web scraping, PDF, OCR y audio.
2. Se procesan y normalizan los datos, luego se almacenan en PostgreSQL y Qdrant.
3. Algoritmos de scoring evalúan relevancia, urgencia e impacto.
4. Noticias y resúmenes se exponen en la interfaz para usuarios y editores.
5. Flujo editorial con calificación, feedback y aprobación humana.
6. Generación y distribución de reportes en formatos HTML, PDF, Word y CSV.
7. Monitorización continua y alertas.

## Diagrama de Arquitectura

![Diagrama Arquitectura](https://www.figma.com/file/ojtZBW5iuH8gwBPm7WgksF?node-id=2-401)

## Diseño de Esquema de Base de Datos

- Tablas principales: users, sources, news_articles, reports, approvals, audit_logs.
- Uso de UUID para claves primarias.
- Relaciones con claves foráneas con políticas ON DELETE CASCADE y ON UPDATE CASCADE.
- Índices en columnas clave para optimización de consultas frecuentes.

## Configuración y Variables de Entorno

- Variables para conexión a DB, Redis, RabbitMQ, S3.
- Configuración de JWT para autenticación y autorización.

## Observabilidad

- Configuración de tracing con OpenTelemetry.
- Logs estructurados con structlog.
- Métricas expuestas vía Prometheus.
- Dashboards en Grafana para monitoreo de salud y uso.

## Consideraciones de Seguridad y Compliance

- Cumplimiento estricto del manejo de datos personales (PII).
- Auditoría completa de los flujos de aprobación y cambios.

---

Archivo generado para cumplir con el ítem FOUNDATION compartido del proyecto CENCO NEWS, reflejando el diseño técnico y los requisitos acordados.