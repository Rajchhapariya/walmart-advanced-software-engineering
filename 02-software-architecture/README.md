# 02. Software Architecture: Decoupled Pipeline Data Processor

UML 2.5 architecture and technical specification for an enterprise data processing engine capable of dynamic reconfiguration and multi-database persistence without conditional branching antipatterns.

## Architectural Patterns
- **Strategy Pattern (Mode Hierarchy):** Encapsulates operating mode logic (`DumpMode`, `PassthroughMode`, `ValidateMode`) behind a common interface. Removes `switch` / `if-else` branching from the execution loop.
- **Bridge Pattern (DatabaseConnector Subsystem):** Decouples storage operations (`insert`, `validate`) from database vendor drivers (`PostgresConnector`, `RedisConnector`, `ElasticConnector`).
- **Factory Pattern (ModeFactory):** Centralizes runtime instantiation and dependency injection during `configure(modeId, dbId)` calls.

## Artifacts
- `Data_Processor_Pipeline_UML_Diagram.svg`: Scalable vector diagram.
- `Data_Processor_Pipeline_UML_Diagram.png`: High-resolution render.
- `Data_Processor_Pipeline_UML_Diagram.pdf`: Standalone vector sheet.
- `Data_Processor_Pipeline_Architecture_Report.pdf`: 3-page architectural specification document.
