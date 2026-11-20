# Copilot instructions

## Project context

This repository is a Python/MicroPython application for configuring Wi-Fi and other settings on an IoT device.
It starts an access point, serves an HTML settings form, saves submitted settings as JSON, and then attempts to connect to the configured Wi-Fi network.

Keep device compatibility in mind: code may run on MicroPython hardware, not just standard CPython.
Check the target runtime and available libraries before introducing dependencies or language features.

## Python standards

- Follow PEP 8 and PEP 257. Use clear names, consistent formatting, and docstrings for public classes and methods.
- Add type annotations to public interfaces where the target runtime supports them. Avoid annotations or standard-library features that the project’s MicroPython version cannot parse or provide.
- Prefer small, readable methods and explicit control flow. Avoid unnecessary abstractions, global mutable state, and duplicated logic.
- Preserve existing module names and import conventions unless a change explicitly includes updating all affected imports.
- Do not log, print, or expose Wi-Fi passwords or other secrets.

## Design principles

Use object-oriented design where it clarifies responsibilities, and apply SOLID pragmatically:

- **Single Responsibility:** Keep networking, HTTP request handling, HTML rendering, and settings persistence in distinct components.
- **Open/Closed:** Prefer extending behavior through focused collaborators or small interfaces rather than adding unrelated branches to existing classes.
- **Liskov Substitution:** Any replacement implementation of a collaborator must honor its documented contract.
- **Interface Segregation:** Keep collaborator interfaces small and specific to the client’s needs.
- **Dependency Inversion:** Pass external dependencies, such as storage or network adapters, into the classes that use them. Keep hardware and application startup wiring in the composition/root module.

Do not introduce interfaces, inheritance, or design patterns solely to satisfy a checklist. Choose the simplest design that keeps responsibilities clear and components testable.

## Patterns and comments

When a design pattern is genuinely used, add a brief comment or docstring at the relevant class or composition point naming the pattern and explaining its purpose.
For example, identify dependency injection when collaborators are supplied to a class, or an adapter when a wrapper isolates hardware-specific APIs.

Write comments to explain intent, constraints, or non-obvious decisions—not to restate each line of code. Keep comments accurate as the implementation changes.

## Project structure

Preserve and build on the repository’s existing separation of concerns:

- `access_point.py` and `wifi.py`: Wi-Fi hardware operations.
- `web_server.py`: HTTP server and request flow.
- `services/file_reader_service.py`: reading HTML assets.
- `services/json_settings_service.py`: settings JSON persistence.
- `html/` and `json_data/`: templates and data files.
- `setup.py`: application startup and dependency wiring.

Keep HTML rendering and request parsing out of persistence services, and keep hardware-specific operations out of the web server. If a change requires new responsibilities, place them in focused modules and update imports and startup wiring consistently.

## Reliability and security

- Handle expected I/O, socket, JSON, and network errors explicitly. Do not silently swallow exceptions or report success after a failure.
- Validate and safely parse incoming HTTP data. Do not assume requests are complete, well-formed, or free of URL-encoded characters.
- Close sockets and files reliably, using context managers for files and `try`/`finally` where needed for resources the runtime does not support as context managers.
- Avoid hard-coded credentials. Do not include real secrets in code, tests, logs, or committed data.
- Keep behavior compatible with constrained device memory and the target runtime; avoid unnecessary buffering, dependencies, and concurrency.

## Testing and verification

- Add focused tests for new or changed behavior where the runtime and project setup permit.
- Keep hardware-dependent behavior isolated so it can be tested with substitutes or mocks on a development machine.
- Run the smallest relevant test or validation command available. If hardware or MicroPython-specific behavior cannot be validated locally, state that limitation rather than implying it was tested.
