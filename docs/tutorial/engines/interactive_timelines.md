---
icon: material/animation-play
search:
  exclude: false
tags:
  - tutorial
  - example
  - interactive
---
# Engine Timeline Visualizer

## Engine communication

This interactive tutorial helps you explore how we envision [[Anomian|engines]]
communicating through message passing. The visualization tool takes a JSON
configuration and renders an animated timeline of message interactions between
engines.

<div class="interactive-timeline-wrapper">
<iframe
class="interactive-timeline"
src="app.html"
width="100%"
height="500px">
</iframe>
</div>

## Getting Started

### how to use

1. **Start the visualization** by clicking dotted message lines.
2. **Hover over elements** to see detailed tooltips.
3. **Watch the timeline scroll** automatically as messages propagate.
4. **Observe engine states** update in real-time above each engine.

### Visual interface overview

- **Engine Nodes**: Coloured boxes at top representing system components.
- **Timeline**: Vertical lines showing message history and potential paths.
- **Message Types**:
  - **Dotted Lines**: Potential messages (click to send).
  - **Solid Lines**: Active message animations
  - **Faded Lines**: Historical messages

## Core Concepts

### message lifecycle

1. **Initiation**: Click potential message (dotted line).
2. **Transmission**: Animation shows message travelling between engines.
3. **Processing**: Receiving engine evaluates message against handlers.
4. **Response**: New potential messages generated based on updated state.

### Configuration Guide

??? example "JSON Schema Structure"
    ```json
    {
    "engines": [
        {
        "name": "EngineName",
        "initialState": any,
        "messageHandlers": [
            {
            "stateEffect": "return state + 1;",
            "guard": "return messageType === 'messageType1';",
            "generateMessages": [
                {
                "to": "TargetEngineName",
                "type": "responseMessageType",
                "payload": null
                }
            ]
            }
        ],
        "initialMessages": [
            {
            "to": "TargetEngineName",
            "type": "initialMessageType",
            "payload": null
            }
        ]
        }
    ]
    }
    ```

??? note "Field Reference"

    #### Engine configuration

    | Field | Type | Description |
    |-------|------|-------------|
    | `name` | string | Unique engine identifier |
    | `initialState` | any | Starting state value |
    | `messageHandlers` | array | Message processing rules |
    | `initialMessages` | array | Initial outgoing messages |

    #### Handler configuration

    | Field | Context Variables | Description |
    |-------|-------------------|-------------|
    | `stateEffect` | `state`, `payload` | JS code returning new state |
    | `guard` | `state`, `payload`, `messageType` | JS condition for handler activation |
    | `generateMessages` | `state`, `payload` | Messages to send if guard passes |

### Advanced Features

!!! tip "Special Message Handling"

    - **Loopback Messages**: Use `"to": "from"` to return messages to sender
    - **Dynamic Payloads**: Include JS code in payload strings:
      ```json
      "payload": "return {timestamp: Date.now(), value: state}"
      ```
    - **State Access**: Handlers can access:
      - `state`: Current engine state
      - `payload`: Received message data
      - `from`: Sender engine name
      - `messageType`: Type of received message