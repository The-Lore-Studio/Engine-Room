# 🏛️ Chromium Engine: Architecture & Subsystems Map

Chromium is one of the most sophisticated open-source software projects in existence. To navigate it, you must understand it along **two axes at once**:
1. **The Runtime Axis (Process Model)**: How the engine splits itself into sandboxed operating system processes at runtime.
2. **The Code Layering Axis (Dependency Stack)**: How the source code is organized into a strictly one-directional dependency stack.

---

## 1. The Runtime Axis: Multi-Process Architecture

At runtime, Chromium splits its work across separate operating system processes to ensure stability, performance, and security.

```mermaid
graph TD
    subgraph Browser Process [Browser Process - Host]
        UI[UI Thread]
        IO[IO Thread]
    end

    subgraph GPU Process [GPU Process - Sandboxed]
        Viz[Viz Display Compositor]
        ANGLE[ANGLE Graphics Abstraction]
    end

    subgraph Network Service [Network Service - Sandboxed]
        NetStack[Net Stack & Cache]
    end

    subgraph Device Service [Device Service - Sandboxed]
        Gamepad[Gamepad Provider & Fetchers]
    end

    subgraph Renderer Process [Renderer Process - Sandboxed]
        Blink[Blink Engine / DOM / Layout]
        V8[V8 Javascript Engine]
    end

    Browser Process -->|Mojo IPC| Renderer Process
    Browser Process -->|Mojo IPC| GPU Process
    Browser Process -->|Mojo IPC| Network Service
    Browser Process -->|Mojo IPC| Device Service
    Renderer Process -->|Direct Shared Memory| Device Service
    GPU Process -->|Rasterization / Display| UI
```

*   **Browser Process**: The central coordinator. It runs the UI, handles user input (keyboard/mouse), and coordinates other processes. It is privileged and has full OS access.
*   **Renderer Process**: Renders web content (HTML/CSS/JS). It is strictly sandboxed. If a webpage crashes or is compromised, it cannot access the user's filesystem or hardware directly.
*   **Utility / Helper Services**: Dedicated sandboxed processes (like the **Network Service** or **Device Service**) isolate complex, vulnerable stacks (like network protocols or hardware drivers) so they don't threaten the main browser process.

---

## 2. The Code Layering Axis: Dependency Stack

The second axis is the **code dependency stack**, which defines which directories are allowed to depend on one another. The rule is strictly **one-directional** (nothing lower in the stack may depend on anything higher).

```text
  +-------------------------------------------------------------+
  | //chrome     - The actual product (UI, settings, branding)  |
  +-------------------------------------------------------------+
         |
         v (embeds)
  +-------------------------------------------------------------+
  | //components - Reusable browser features (Sync, Autofill)   |
  +-------------------------------------------------------------+
         |
         v
  +-------------------------------------------------------------+
  | //content    - The multi-process engine (Brave, Edge, etc.)  |
  +-------------------------------------------------------------+
         |
         +---------------------------------------+
         |                                       |
         v                                       v
  +-----------------------+              +----------------------+
  | //third_party/blink   |              | //services           |
  | (DOM, parsing, style) |              | (Device, Audio, etc.)|
  +-----------------------+              +----------------------+
         |                                       |
         +-------------------+-------------------+
                             |
                             v
                      +--------------+
                      | //mojo       |
                      | (IPC system) |
                      +--------------+
                             |
                             v
                      +--------------+
                      | //base       |
                      | (Primitives) |
                      +--------------+
```

### The Stack Layers:
1.  **`base/`**: Core utilities, threading primitives, memory helpers, and files used by absolutely everything.
2.  **`mojo/`**: The inter-process communication (IPC) messaging framework used for message passing.
3.  **`//services`**: Out-of-process utility microservices (Gamepad, Audio, Geolocation, etc.).
4.  **`//content`**: The core multi-process web engine. It embeds Blink and V8 but does *not* contain browser features like bookmarks, extensions, or sync. (This is what Brave, Edge, and Electron embed).
5.  **`//components`**: Reusable components shared between Chrome and other products (like Chrome on Android or iOS).
6.  **`//chrome`**: The top-level product layer. Contains the main UI, product definitions, and features.

---

## 3. The Major Subsystems (Glossary)

Chromium's code is grouped into 11 major subsystems spanning across the process and dependency axes:

1.  **Engine & Web Platform**: *`//third_party/blink` (HTML/CSS parsing, DOM, style, layout)* and *V8 (JavaScript and WebAssembly engine)*.
2.  **Graphics**: *Compositor (`cc`)*, *Viz (GPU-side display compositor)*, *Skia (2D rasterization library)*, and *ANGLE (cross-platform GL/Vulkan/Metal abstraction)*.
3.  **Networking**: *`//net`* and the Network Service (manages HTTP, sockets, TLS, cache, cookies, and QUIC/HTTP3).
4.  **Storage**: *`//storage`*, Quota management, IndexedDB, Cache Storage, and Service Worker disk storage.
5.  **Process Model & Security**: The sandbox implementations, Site Isolation (rendering different sites in different OS processes), and the Browser/Renderer process split.
6.  **Platform Services**: *`//services/device` (Gamepad, sensors, geolocation APIs)*, Audio services, and others.
7.  **Media**: *`//media`* (audio/video pipeline, codecs, WebRTC, and Encrypted Media Extensions).
8.  **Browser Features**: *`//components`* (Chrome Sync, Autofill, Safe Browsing, metrics, and `//extensions`).
9.  **UI**: *`//ui`* (Views toolkit, Aura window manager, event handling) and *`//chrome/browser/ui`* (the actual browser shell/chrome).
10. **DevTools**: The TypeScript frontend and the backend instrumentation protocol reaching into Blink, V8, and the network stack.
11. **Foundation**: *`base/`* and *Mojo*, used by everything in the repository.
