// Constants
const ANIMATION_DURATION = 1500; // ms
const FADE_OUT_HEIGHT = 100; // px

// Global state
let engines = {};
let messages = [];
let pendingMessages = [];
let animatingMessages = [];
let timelineOffset = 0;

// DOM elements
const enginesContainer = document.getElementById('engines-container');
const timelineContainer = document.getElementById('timeline-container');

// Utility function for evaluating code/function strings
function evaluateFunctionString(codeString, context = {}, defaultReturn = null) {
    if (!codeString || typeof codeString !== 'string') return defaultReturn;

    try {
        // Create parameter list from context object keys
        const params = Object.keys(context);
        const values = params.map(key => context[key]);

        // Handle code block
        const fn = new Function(...params, `
            try {
                ${codeString}
            } catch (e) {
                console.error("Error in code evaluation:", e);
                return ${params[0] || 'null'};
            }
        `);

        return fn(...values);
    } catch (e) {
        console.error(`Error executing function string:`, e);
        return defaultReturn;
    }
}

// Utility function for DOM operations with debouncing
function debounce(fn, delay = 50) {
    clearTimeout(window._resizeTimeout);
    window._resizeTimeout = setTimeout(fn, delay);
}

// Get JSON from URL parameters
function getJsonFromUrl() {
    const urlParams = new URLSearchParams(window.location.search);
    const jsonParam = urlParams.get('json');

    if (!jsonParam) {
        // If no JSON parameter provided, show available JSON files
        showJsonFileSelector();
        return null;
    }

    try {
        // Try to parse the JSON directly from the URL parameter
        return JSON.parse(jsonParam);
    } catch (e) {
        // If it fails, it might be a URL to a JSON file
        fetch(jsonParam)
            .then(response => {
                if (!response.ok) {
                    throw new Error('Network response was not ok');
                }
                return response.json();
            })
            .then(data => {
                initializeApp(data);
            })
            .catch(error => {
                showError(`Error fetching JSON: ${error.message}`);
            });
        return null;
    }
}

// Show selector for available JSON files
function showJsonFileSelector() {
    // Create a container for the file selector
    const selectorContainer = document.createElement('div');
    selectorContainer.className = 'file-selector-container';

    const title = document.createElement('h2');
    title.textContent = 'Select a engine-timeline example';
    selectorContainer.appendChild(title);

    const fileList = document.createElement('div');
    fileList.className = 'file-list';
    selectorContainer.appendChild(fileList);

    document.body.appendChild(selectorContainer);

    // First, try directory listing method
    tryDirectoryListing(fileList).then(success => {
        // If directory listing fails or returns no files, fall back to known samples
        if (!success) {
            showKnownSampleFiles(fileList);
        }
    });
}
// Try to get JSON files via directory listing
async function tryDirectoryListing(fileList) {
    // Add loading indicator
    const loadingIndicator = document.createElement('div');
    loadingIndicator.className = 'loading-indicator';
    loadingIndicator.textContent = 'Loading available files...';
    fileList.appendChild(loadingIndicator);

    try {
        // Get current directory path based on page location
        const currentPath = window.location.pathname;
        const directoryPath = currentPath.substring(0, currentPath.lastIndexOf('/') + 1);

        const response = await fetch(directoryPath);
        const html = await response.text();

        // Parse HTML to get file links
        const parser = new DOMParser();
        const doc = parser.parseFromString(html, 'text/html');
        const links = Array.from(doc.querySelectorAll('a'));

        // Filter for JSON files and exclude directories
        const jsonFiles = links
            .map(link => {
                const href = link.getAttribute('href');
                return href && decodeURIComponent(href); // Handle URL-encoded filenames
            })
            .filter(href => href &&
                !href.endsWith('/') && // Exclude directories
                href.toLowerCase().endsWith('.json')
            );

        // Remove loading indicator
        loadingIndicator.remove();

        if (jsonFiles.length === 0) {
            return false; // No files found, will fall back to known samples
        }

        // Create file buttons with decoded filenames
        jsonFiles.forEach(file => {
            addFileButton(fileList, file);
        });

        return true;
    } catch (error) {
        console.error('Error fetching file list:', error);
        loadingIndicator.remove();
        return false;
    }
}

// Helper function to check if we're in an iframe
function isInIframe() {
    try {
        return window.self !== window.top;
    } catch (e) {
        // If we can't access window.top, we're likely in a cross-origin iframe
        return true;
    }
}
// Sample titles mapped to display names
const sampleTitles = {
    'sample-ticker.json': 'Ticker: Two engines of the same type',
    'sample-ping-pong.json': 'Ping Pong: Two engines of different types',
    'sample-broadcast.json': 'Broadcast: Several engines of the same type'
};

// Show known sample files if directory listing fails
function showKnownSampleFiles(fileList) {
    // Known sample files in this project
    const knownSamples = Object.keys(sampleTitles);

    // const heading = document.createElement('div');
    // heading.className = 'sample-heading';
    // heading.textContent = 'Sample Network Configurations:';
    // fileList.appendChild(heading);

    // Create buttons for sample files using the titles dictionary
    knownSamples.forEach(file => {
        addFileButton(fileList, file);
    });

    // Only show URL input if not in an iframe
    if (!isInIframe()) {
        // Add custom JSON input option
        const customSection = document.createElement('div');
        customSection.className = 'custom-json-section';

        const customHeading = document.createElement('div');
        customHeading.className = 'sample-heading';
        customHeading.textContent = 'Or provide JSON URL:';
        customSection.appendChild(customHeading);

        const customInput = document.createElement('input');
        customInput.type = 'text';
        customInput.className = 'custom-json-input';
        customInput.placeholder = 'Enter URL to JSON file';
        customSection.appendChild(customInput);

        const loadButton = document.createElement('button');
        loadButton.className = 'file-button';
        loadButton.textContent = 'Load JSON';

        // Helper function to load the JSON
        const loadJson = () => {
            const url = customInput.value.trim();
            if (url) {
                window.location.search = `?json=${encodeURIComponent(url)}`;
            }
        };

        // Add click event
        loadButton.addEventListener('click', loadJson);

        // Add enter key event
        customInput.addEventListener('keypress', (e) => {
            if (e.key === 'Enter') {
                loadJson();
            }
        });

        customSection.appendChild(loadButton);
        fileList.appendChild(customSection);
    }
}

// Helper function to add a file button
function addFileButton(container, file) {
    const fileButton = document.createElement('button');
    fileButton.className = 'file-button';
    fileButton.textContent = sampleTitles[file] || file;

    fileButton.addEventListener('click', () => {
        // Load the selected JSON file
        window.location.search = `?json=${encodeURIComponent(file)}`;
    });

    container.appendChild(fileButton);
}

// Show error message
function showError(message) {
    const errorDiv = document.createElement('div');
    errorDiv.className = 'error-message';
    errorDiv.textContent = message;
    document.body.appendChild(errorDiv);
}

// Initialize the application
function initializeApp(data) {
    if (!data || !data.engines || !Array.isArray(data.engines)) {
        showError('Invalid JSON structure: missing or invalid engines');
        return;
    }

    // Set up engines
    data.engines.forEach(engine => {
        if (!engine.name) {
            console.warn('Engine without name found, skipping');
            return;
        }

        engines[engine.name] = {
            name: engine.name,
            state: engine.initialState ?? null,
            messageHandlers: Array.isArray(engine.messageHandlers) ? engine.messageHandlers : [],
            initialMessages: Array.isArray(engine.initialMessages) ? engine.initialMessages : []
        };

        createEngineBox(engine.name);
    });

    // Handle initial messages from each engine
    Object.values(engines).forEach(engine => {
        engine.initialMessages.forEach(msg => {
            if (msg.to && msg.type) {
                // Process payload if it's a function string
                const msgPayload = typeof msg.payload === 'string'
                    ? evaluateFunctionString(msg.payload, { state: engine.state }, null)
                    : msg.payload;

                queueMessage(engine.name, msg.to, msg.type, msgPayload);
            }
        });
    });

    // Add back button for selection menu
    const backButton = document.createElement('button');
    backButton.id = 'back-to-selection';
    backButton.innerHTML = '&larr;';
    backButton.addEventListener('click', () => {
        window.location.search = ''; // Clear the query string to return to selection menu
    });
    document.body.appendChild(backButton);

    // Set up timeline visuals
    setupTimeline();

    // Start handling initial messages
    updatePendingMessages();
}

// Create engine box in the UI
function createEngineBox(engineName) {
    const engineBox = document.createElement('div');
    engineBox.className = 'engine-box';
    engineBox.dataset.engine = engineName;

    const nameDiv = document.createElement('div');
    nameDiv.className = 'engine-name';
    nameDiv.textContent = engineName;

    const stateDiv = document.createElement('div');
    stateDiv.className = 'engine-state';
    stateDiv.textContent = 'State: ' + (engines[engineName].state !== null ? JSON.stringify(engines[engineName].state) : 'null');

    engineBox.appendChild(nameDiv);
    engineBox.appendChild(stateDiv);
    enginesContainer.appendChild(engineBox);
}

// Update state display for an engine
function updateEngineState(engineName) {
    const engineBox = document.querySelector(`.engine-box[data-engine="${engineName}"]`);
    if (engineBox) {
        const stateDiv = engineBox.querySelector('.engine-state');
        stateDiv.textContent = 'State: ' + (engines[engineName].state !== null ? JSON.stringify(engines[engineName].state) : 'null');
    }
}

// Set up timeline visualization
function setupTimeline() {
    // Create vertical lines for each engine
    Object.keys(engines).forEach(engineName => {
        const engineBox = document.querySelector(`.engine-box[data-engine="${engineName}"]`);
        const boxRect = engineBox.getBoundingClientRect();
        const containerRect = enginesContainer.getBoundingClientRect();

        const line = document.createElement('div');
        line.className = 'timeline-line';
        line.dataset.engine = engineName;

        const centerX = boxRect.left + boxRect.width / 2 - containerRect.left;
        line.style.left = `${centerX}px`;
        line.style.top = '0';
        line.style.height = '100%';

        timelineContainer.appendChild(line);
    });

    // Set up resize observer to reposition lines when window size changes
    const handleResize = () => {
        // Update the engine timeline lines
        Object.keys(engines).forEach(engineName => {
            const engineBox = document.querySelector(`.engine-box[data-engine="${engineName}"]`);
            const timelineLine = document.querySelector(`.timeline-line[data-engine="${engineName}"]`);
            const boxRect = engineBox.getBoundingClientRect();
            const containerRect = enginesContainer.getBoundingClientRect();

            const centerX = boxRect.left + boxRect.width / 2 - containerRect.left;
            timelineLine.style.left = `${centerX}px`;
        });

        // Reposition all message lines with animation
        document.querySelectorAll('.message-line').forEach(line => {
            line.style.transition = 'left 0.3s, width 0.3s, transform 0.3s';
        });

        // Reposition all message lines
        repositionAllLines();

        // Remove transitions after animation completes
        setTimeout(() => {
            document.querySelectorAll('.message-line').forEach(line => {
                line.style.transition = '';
            });
        }, 300);
    };

    // Use the debounce utility for resize handling
    const resizeObserver = new ResizeObserver(() => debounce(handleResize, 50));
    resizeObserver.observe(document.body);

    // Use same handler for window resize event
    window.addEventListener('resize', () => debounce(handleResize, 50));

    // Setup animation frame for timeline scrolling
    requestAnimationFrame(animateTimeline);
}

// Queue a message for processing
function queueMessage(from, to, type, payload = null) {
    const message = {
        from,
        to,
        type,
        payload,
        id: Date.now() + '-' + Math.random().toString(36).slice(2, 11)
    };

    pendingMessages.push(message);
    return message;
}

// Process a message by running its handler
function processMessage(message) {
    const { from, to, type, payload } = message;

    const engine = engines[to];
    if (!engine) {
        console.warn(`Engine '${to}' not found`);
        return;
    }

    // Store original state to check guards against
    const originalState = engine.state !== null ? JSON.parse(JSON.stringify(engine.state)) : null;

    // Handle direct message (apply state effect)
    handleMessageForEngine(from, to, type, payload);

    // New message generation phase (using the original state for guards)
    generateNewMessages(from, to, type, payload, originalState);
}

// Handle a message for a specific engine
function handleMessageForEngine(from, to, type, payload) {
    const engine = engines[to];
    if (!engine) {
        console.warn(`Engine '${to}' not found`);
        return;
    }

    if (engine.messageHandlers.length === 0) {
        console.warn(`No message handlers in engine '${to}'`);
        return;
    }

    // Try to find a handler with matching guard condition
    const handler = engine.messageHandlers.find(h => {
        if (!h.guard) return false;

        return !!evaluateFunctionString(
            h.guard,
            {
                state: engine.state,
                payload,
                from,
                messageType: type
            },
            false
        );
    });

    if (!handler) return;

    // Process state effect
    if (handler.stateEffect) {
        const result = evaluateFunctionString(
            handler.stateEffect,
            {
                state: engine.state,
                payload,
                from
            },
            undefined
        );

        // Update engine state if returned
        if (result !== undefined) {
            engine.state = result;
            updateEngineState(to);
        }
    }
}

// Generate new messages after message handling
function generateNewMessages(triggerFrom, triggerTo, messageType, triggerPayload, originalState) {
    const engine = engines[triggerTo];

    // Skip if no engine or no handlers
    if (!engine || !engine.messageHandlers) return;

    // Check all message handlers in this engine
    engine.messageHandlers.forEach(handler => {
        // Skip if no generation messages
        if (!handler.generateMessages || !Array.isArray(handler.generateMessages)) return;

        // Check guard condition for generating messages
        const shouldGenerateMessages = handler.guard ?
            !!evaluateFunctionString(
                handler.guard,
                {
                    state: originalState,
                    payload: triggerPayload,
                    from: triggerFrom,
                    messageType
                },
                false
            ) : false;

        // Process generated messages if guard condition allows
        if (shouldGenerateMessages) {
            handler.generateMessages.forEach(message => {
                if (message.to && message.type) {
                    // Handle special "from" case
                    const messageTo = message.to === "from" ? triggerFrom : message.to;

                    // Handle payload as function
                    const messagePayload = typeof message.payload === 'string'
                        ? evaluateFunctionString(message.payload, { state: engine.state }, null)
                        : message.payload;

                    queueMessage(triggerTo, messageTo, message.type, messagePayload);
                }
            });
        }
    });
}

// Update and display pending messages
function updatePendingMessages() {
    if (pendingMessages.length === 0) return;

    // Keep track of existing message IDs to avoid duplicating
    const existingMessageIds = new Set();
    document.querySelectorAll('.dotted-line').forEach(line => {
        existingMessageIds.add(line.dataset.messageId);
    });

    // Filter out any duplicate messages that already exist as dotted lines
    const newPendingMessages = pendingMessages.filter(message =>
        !existingMessageIds.has(message.id));

    if (newPendingMessages.length === 0) return;

    // Determine appropriate base Y position
    const baseY = Math.max(
        // Find lowest dotted line position if any exist
        document.querySelectorAll('.dotted-line').length > 0 ?
            Math.max(...Array.from(document.querySelectorAll('.dotted-line'))
                .map(line => parseInt(line.dataset.baseY || '0'))) + 50 : 0,
        // Or use standard position if no existing lines
        timelineContainer.clientHeight - 50
    );

    // Create all message lines at the same base Y level
    newPendingMessages.forEach((message, index) => {
        const existingCount = document.querySelectorAll(`.dotted-line[data-from="${message.from}"]`).length;
        createMessageLine(message, baseY, true, {
            groupIndex: existingCount + index
        });
    });

    // Register mouse movement handlers for spreading out messages
    registerMessageSpreadHandlers();

    // Force a reposition to ensure all lines are correctly placed
    repositionAllLines();

    // Clear the pending messages array now that we've processed them
    pendingMessages = [];
}

// Called when window resizes to reposition message lines
function repositionAllLines() {
    const timelineHeight = timelineContainer.clientHeight;

    // Reposition all dotted lines to the bottom
    const dottedLines = document.querySelectorAll('.dotted-line');
    if (dottedLines.length > 0) {
        // Set a common base Y for all dotted lines
        const commonBaseY = timelineHeight - 50;

        // Group by 'from' attribute
        const groups = {};
        dottedLines.forEach(line => {
            const from = line.dataset.from;
            if (!groups[from]) {
                groups[from] = [];
            }
            groups[from].push(line);
        });

        // Update all dotted lines to use the same base Y
        Object.keys(groups).forEach(from => {
            const lines = groups[from];

            // Update group indices for each line
            lines.sort((a, b) => parseInt(a.dataset.groupIndex || 0) - parseInt(b.dataset.groupIndex || 0));

            lines.forEach((line, i) => {
                line.dataset.groupIndex = i;
                line.dataset.baseY = commonBaseY;

                // Update line position directly if no active animation
                if (!window._lineSpreadState ||
                    !window._lineSpreadState[line.dataset.messageId] ||
                    Math.abs(window._lineSpreadState[line.dataset.messageId].currentY -
                             window._lineSpreadState[line.dataset.messageId].targetY) < 0.5) {
                    updateLinePosition(line, commonBaseY);
                }
            });
        });
    }

    // Reposition all solid lines
    document.querySelectorAll('.solid-line').forEach(line => {
        const from = line.dataset.from;
        const to = line.dataset.to;

        // Get positions of the engine lines
        const fromLine = document.querySelector(`.timeline-line[data-engine="${from}"]`);
        const toLine = document.querySelector(`.timeline-line[data-engine="${to}"]`);

        if (!fromLine || !toLine) return;

        const containerRect = timelineContainer.getBoundingClientRect();
        const fromRect = fromLine.getBoundingClientRect();
        const toRect = toLine.getBoundingClientRect();

        const x1 = fromRect.left + fromRect.width / 2 - containerRect.left;
        const x2 = toRect.left + toRect.width / 2 - containerRect.left;
        const y1 = parseFloat(line.style.top);

        // Update line position
        line.style.left = `${x1}px`;
        line.style.width = `${Math.sqrt(Math.pow(x2 - x1, 2) + 400)}px`;
        line.style.transform = `rotate(${Math.atan2(20, x2 - x1) * 180 / Math.PI}deg)`;
    });
}

// Helper function to update a line's position and angle
function updateLinePosition(line, newY) {
    const from = line.dataset.from;
    const to = line.dataset.to;

    // Get positions of the engine lines
    const fromLine = document.querySelector(`.timeline-line[data-engine="${from}"]`);
    const toLine = document.querySelector(`.timeline-line[data-engine="${to}"]`);

    if (!fromLine || !toLine) return;

    const containerRect = timelineContainer.getBoundingClientRect();
    const fromRect = fromLine.getBoundingClientRect();
    const toRect = toLine.getBoundingClientRect();

    const x1 = fromRect.left + fromRect.width / 2 - containerRect.left;
    const x2 = toRect.left + toRect.width / 2 - containerRect.left;
    const y1 = newY - 20; // From is higher
    const y2 = newY;

    // Calculate line properties
    const distance = Math.sqrt(Math.pow(x2 - x1, 2) + Math.pow(y2 - y1, 2));
    const angle = Math.atan2(y2 - y1, x2 - x1) * 180 / Math.PI;

    // Update line position and angle
    line.style.left = `${x1}px`;
    line.style.top = `${y1}px`;
    line.style.width = `${distance}px`;
    line.style.transform = `rotate(${angle}deg)`;
}

// Register mouse movement handlers for spreading out grouped message lines
function registerMessageSpreadHandlers() {
    // Clear previous listeners
    if (window._spreadHandlerAdded) {
        timelineContainer.removeEventListener('mousemove', window._spreadHandlerFunction);
    }

    // Track the current spread state if not initialized
    window._lineSpreadState = window._lineSpreadState || {};

    // Helper function to group elements by a data attribute (moved inside to avoid recreation)
    function groupLinesByAttribute(elements, attribute) {
        const groups = {};
        elements.forEach(element => {
            const key = element.dataset[attribute];
            if (!groups[key]) {
                groups[key] = [];
            }
            groups[key].push(element);
        });
        return groups;
    }

    // Set up animation for smooth transitions
    if (!window._spreadAnimationRunning) {
        window._spreadAnimationRunning = true;

        function animateSpread() {
            // Group dotted lines by sender engine
            const lineGroups = groupLinesByAttribute(document.querySelectorAll('.dotted-line'), 'from');

            // For each group, animate towards the target position
            Object.keys(lineGroups).forEach(groupKey => {
                const linesInGroup = lineGroups[groupKey];

                // Sort lines by their creation order
                linesInGroup.sort((a, b) => parseInt(a.dataset.groupIndex || 0) - parseInt(b.dataset.groupIndex || 0));

                // Only animate if there are multiple lines in this group
                if (linesInGroup.length > 1) {
                    linesInGroup.forEach(line => {
                        const baseY = parseInt(line.dataset.baseY || 0);

                        // Get or initialize the current Y position
                        if (!window._lineSpreadState[line.dataset.messageId]) {
                            window._lineSpreadState[line.dataset.messageId] = {
                                currentY: baseY,
                                targetY: baseY
                            };
                        }

                        const state = window._lineSpreadState[line.dataset.messageId];

                        // Smoothly animate to the target position
                        if (Math.abs(state.currentY - state.targetY) > 0.5) {
                            state.currentY += (state.targetY - state.currentY) * 0.2;
                            updateLinePosition(line, state.currentY);
                        }
                    });
                }
            });

            requestAnimationFrame(animateSpread);
        }

        animateSpread();
    }

    // Handler for mouse movement to spread messages
    const spreadHandler = e => {
        // Get mouse position relative to timeline container
        const timelineRect = timelineContainer.getBoundingClientRect();
        const mouseX = e.clientX - timelineRect.left;
        const mouseY = e.clientY - timelineRect.top;

        // Group dotted lines by sender
        const lineGroups = groupLinesByAttribute(document.querySelectorAll('.dotted-line'), 'from');

        // Process each group
        Object.keys(lineGroups).forEach(groupKey => {
            const linesInGroup = lineGroups[groupKey];

            // Only process groups with multiple lines
            if (linesInGroup.length > 1) {
                // Get sender engine position
                const senderLine = document.querySelector(`.timeline-line[data-engine="${groupKey}"]`);
                if (!senderLine) return;

                const senderX = parseFloat(senderLine.style.left);
                const distanceToMouse = Math.abs(mouseX - senderX);

                // Sort lines by creation order
                linesInGroup.sort((a, b) => parseInt(a.dataset.groupIndex || 0) - parseInt(b.dataset.groupIndex || 0));

                // Check if mouse is near the sender line and in lower part
                const nearLine = distanceToMouse < 80;
                const inLowerPart = mouseY > (timelineRect.height - 150);

                // Set target positions for each line
                linesInGroup.forEach((line, index) => {
                    const baseY = parseInt(line.dataset.baseY || 0);
                    let targetY = baseY;

                    if (nearLine && inLowerPart) {
                        // Calculate spread factor based on distance
                        const spreadFactor = Math.max(0, 1 - distanceToMouse / 80);

                        // Move later lines upward but keep first in place
                        if (index > 0) {
                            targetY = baseY - (index * 15 * spreadFactor);
                        }
                    }

                    // Update target position in state
                    if (window._lineSpreadState[line.dataset.messageId]) {
                        window._lineSpreadState[line.dataset.messageId].targetY = targetY;
                    }
                });
            }
        });
    };

    // Save handler reference and add listener
    window._spreadHandlerFunction = spreadHandler;
    window._spreadHandlerAdded = true;
    timelineContainer.addEventListener('mousemove', spreadHandler);
}


// Create a message line in the timeline
function createMessageLine(message, yPosition, isDotted = false, groupInfo = null) {
    const { from, to, id, type, payload } = message;

    // Get positions of the engine lines
    const fromLine = document.querySelector(`.timeline-line[data-engine="${from}"]`);
    const toLine = document.querySelector(`.timeline-line[data-engine="${to}"]`);

    if (!fromLine || !toLine) {
        console.warn(`Could not find timeline lines for engines: ${from} -> ${to}`);
        return;
    }

    const fromRect = fromLine.getBoundingClientRect();
    const toRect = toLine.getBoundingClientRect();
    const containerRect = timelineContainer.getBoundingClientRect();

    const x1 = fromRect.left + fromRect.width / 2 - containerRect.left;
    const x2 = toRect.left + toRect.width / 2 - containerRect.left;
    const y1 = yPosition - 20; // From is higher (earlier in time)

    // Calculate line properties
    const distance = Math.sqrt(Math.pow(x2 - x1, 2) + Math.pow(20, 2));
    const angle = Math.atan2(20, x2 - x1) * 180 / Math.PI;

    // Create the line
    const line = document.createElement('div');
    line.className = `message-line ${isDotted ? 'dotted-line' : 'solid-line'}`;
    line.dataset.messageId = id;
    line.dataset.from = from;
    line.dataset.to = to;

    // Store grouping information for dotted lines
    if (isDotted && groupInfo) {
        line.dataset.groupIndex = groupInfo.groupIndex;
        line.dataset.baseY = yPosition;
    }

    line.style.left = `${x1}px`;
    line.style.top = `${y1}px`;
    line.style.width = `${distance}px`;
    line.style.transform = `rotate(${angle}deg)`;

    // Add tooltip content for hover
    line.title = `${from} → ${to}: "${type}"${payload !== null ? ' | Payload: ' + JSON.stringify(payload) : ''}`;

    // Create custom tooltip only on mouseenter (better performance)
    line.addEventListener('mouseenter', e => {
        const info = document.createElement('div');
        info.className = 'message-info';
        info.textContent = line.title;
        info.style.left = (e.clientX + 10) + 'px';
        info.style.top = (e.clientY - 20) + 'px';
        info.dataset.forMessage = id;
        document.body.appendChild(info);

        const moveHandler = e => {
            info.style.left = (e.clientX + 10) + 'px';
            info.style.top = (e.clientY - 20) + 'px';
        };

        const leaveHandler = () => {
            info.remove();
            line.removeEventListener('mousemove', moveHandler);
            line.removeEventListener('mouseleave', leaveHandler);
        };

        line.addEventListener('mousemove', moveHandler);
        line.addEventListener('mouseleave', leaveHandler);
    });

    if (isDotted) {
        // Create filling animation div
        const filling = document.createElement('div');
        filling.className = 'filling-animation';
        line.appendChild(filling);

        // Add click event for dotted lines
        line.addEventListener('click', () => {
            // Prevent clicking if already animating
            if (animatingMessages.find(m => m.id === id)) return;

            // Start animation
            filling.style.transition = `width ${ANIMATION_DURATION}ms linear`;
            filling.style.width = '100%';

            // Add to animating messages
            animatingMessages.push({
                ...message,
                element: line,
                filling,
                startTime: Date.now(),
                completed: false
            });
        });
    }

    timelineContainer.appendChild(line);

    // Add to messages array if it's a solid line
    if (!isDotted) {
        messages.push({
            ...message,
            element: line,
            y: y1
        });
    }
}

// Update message lines position for scrolling effect
function updateMessageLines() {
    // Only start scrolling when we need to make room for new messages
    const timelineHeight = timelineContainer.clientHeight;
    const bottomMessage = findBottomMessage();
    const needScrolling = bottomMessage && (bottomMessage.y > timelineHeight - 150);

    if (needScrolling) {
        // Update positions of existing message lines
        messages.forEach(message => {
            if (!message.element) return;
            message.y -= timelineOffset;
            message.element.style.top = `${message.y}px`;

            // Remove if scrolled out of view
            if (message.y < -FADE_OUT_HEIGHT) {
                message.element.remove();
                message.element = null;
            }
        });

        // Clean up removed messages
        messages = messages.filter(message => message.element !== null);
    }
}

// Find the message that appears lowest in the timeline
function findBottomMessage() {
    if (messages.length === 0) return null;

    return messages.reduce((lowest, current) => {
        if (!lowest || current.y > lowest.y) {
            return current;
        }
        return lowest;
    }, null);
}

// Timeline animation loop
function animateTimeline() {
    // Check for completed animations
    const now = Date.now();
    animatingMessages.forEach(message => {
        if (message.completed) return;

        const elapsed = now - message.startTime;
        if (elapsed >= ANIMATION_DURATION) {
            message.completed = true;

            // Convert dotted line to solid
            message.element.classList.remove('dotted-line');
            message.element.classList.add('solid-line');
            message.filling.remove();

            // Clean up any stuck message info tooltips
            const info = document.querySelector(`.message-info[data-for-message="${message.id}"]`);
            if (info) {
                info.remove();
            }

            // Process the message
            processMessage(message);

            // Add this as a solid message line
            messages.push({
                ...message,
                y: parseFloat(message.element.style.top)
            });

            // Generate new pending messages
            updatePendingMessages();
        }
    });

    // Remove completed animations
    animatingMessages = animatingMessages.filter(m => !m.completed);

    // Scroll timeline if we have active messages
    if (messages.length > 0) {
        timelineOffset = 1; // Consistent speed
        updateMessageLines();
    }

    requestAnimationFrame(animateTimeline);
}

// Initialize on page load
document.addEventListener('DOMContentLoaded', () => {
    // Try to get JSON from URL parameter
    const jsonData = getJsonFromUrl();
    if (jsonData) {
        initializeApp(jsonData);
    }
});