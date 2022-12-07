# Core

The core module contains the **Agent**, **STT**, **TTS**, as well as dataclasses related to the **Agent**. The Agent is responsible for the overall control flow of the application. It is the main entry point for the user and the main interface to the other modules. It also takes care of the proactivity of the application.

## Agent

```mermaid
graph LR;

start_agent --> greet_user;
greet_user --> check_for_proactivity;
check_for_proactivity --> trigger_proactivity;
trigger_proactivity --> get_user_input;
check_for_proactivity --> get_user_input;
get_user_input --> calculate_best_match;
calculate_best_match --> trigger_use_case;
trigger_use_case --> check_for_proactivity;
```

<!-- prettier-ignore -->
::: aswe.core.agent
    options:
        heading_level: 3

## User Interaction

<!-- prettier-ignore -->
::: aswe.core.user_interaction
    options:
        heading_level: 3

## Dataclasses

<!-- prettier-ignore -->
::: aswe.core.objects
    options:
        heading_level: 3
