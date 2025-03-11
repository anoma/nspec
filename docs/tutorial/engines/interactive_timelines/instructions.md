# Engine Timeline Visualizer

This is an interactive HTML application that visualizes message passing between different engines in a timeline format. The app takes a JSON configuration file as input and displays a visual timeline of message interactions.

## Screenshot

![Engine Timeline Visualizer Screenshot](resources/screenshot.png)
*Engine Timeline Visualizer showing message passing between engines*

## Features

- Visualize messages being passed between engines
- Interactive timeline with click-to-send functionality
- Support for custom JavaScript handlers in messages
- Support for engine state tracking
- Animation of message transmission
- Time-based scrolling timeline

## How to Use

1. Start a local web server in this directory (for example, using Python):
   ```
   python -m http.server
   ```

2. Open the application in a browser with a JSON configuration provided as a URL parameter:
   ```
   http://localhost:8000/?json=/sample-ping-pong.json
   ```

   Alternatively, you can directly include the JSON in the URL parameter:
   ```
   http://localhost:8000/?json={...JSON content...}
   ```

## JSON Configuration Format

The JSON configuration should have the following structure:

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

### Important Fields:

- `engines`: Array of engine configurations
  - `name`: Name of the engine
  - `initialState`: Initial state of the engine (can be any JSON value, or `null`)
  - `messageHandlers`: Object mapping message types to handler configurations
  - `initialMessages`: Array of messages that the engine will send on startup

- `messageHandlers`: An object where each key is a message type the engine handles:
  - `stateEffect`: JavaScript code as a string that updates the engine state (should return the new state)
  - `guard`: JavaScript condition as a string that determines if the message should be processed
  - `generateMessages`: Array of message objects to be generated in response

- Message objects have the following structure:
  - `to`: Target engine name
  - `type`: Type of message
  - `payload`: Data to send (can be a JS function string that returns a value)

### Message Processing Flow:

When an engine receives a message, the following steps occur:

1. The original state of the receiving engine is captured
2. The state effect is applied if the guard condition is met
3. The guard condition for message generation is evaluated using the original state
4. If the guard returns true, new messages are generated based on the updated state

This allows handlers to evaluate conditions based on the state before any modifications, while generating messages that include values from the updated state.

### Special Features:

- Use `"to": "from"` to send a message back to the sender
- Include JavaScript code in the payload as a string: `"payload": "return state;"`
- The JavaScript in `stateEffect` and `guard` now has access to:
  - `state`: The current state of the receiving engine
  - `payload`: The data sent with the message
  - `from`: The name of the sending engine
  - `messageType`: The type of message that triggered the handler

## Sample Configurations

Three example JSON files are included:

1. `sample-ping-pong.json`: Simple ping-pong message passing between two engines
2. `sample-broadcast.json`: Demonstrates broadcast messaging and state propagation
3. `sample-ticker.json`: Shows read and increment operations with two ticker engines

## Interaction Guide

- Each engine is represented as a box at the top of the screen
- Vertical lines extend down from each engine
- Dotted lines represent potential messages that can be sent
- Click on a dotted line to animate the message being sent
- When the animation completes, the message is processed and may generate new potential messages
- Hover over message lines to see details about the message
- The timeline scrolls up as messages are sent
- Hovering near an engine line will cause potential messages to spread out