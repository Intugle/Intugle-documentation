---
title: Speech-to-Text (Voice Input)
sidebar_position: 8
---

# Speech-to-Text (Voice Input)

Intugle transcribes live speech on the server using the voice model configured for your workspace. The chat mic in Intugle and in deployed ChatApps uses this capability, and your own client (a mobile app, a desktop app or a custom web page) can use it too.

Your client opens a Socket.IO connection, streams raw microphone audio, and receives the text as the user speaks. It then sends that text to Intugle like any typed question (for example through [MCP](./mcp/overview.md) or [A2A](./a2a/overview.md)). Voice provider keys stay on the server; your client never needs one.

## Prerequisites

1. **A voice model is configured for the workspace.** In the Agent Configurator, open **Orchestration Agent → Other → Chat Speech-to-Text** and choose a primary voice model (and optionally a fallback). The same editor sets **After recording** (review first or send automatically), the maximum recording length, and key terms that improve recognition of your domain words.
2. **For a ChatApp: the deployment has voice input turned on.** In the deploy wizard, open **Serving Options → Chat Config** and turn on **Enable Chat Speech-to-Text**. A deployment keeps the voice settings it was deployed with; after changing the voice model, redeploy the ChatApp to use the new one.
3. **A signed-in user.** The connection uses the user's Intugle access token: the same `Authorization: Bearer` token your client sends to the Intugle REST API. ChatApp MCP and A2A API keys are **not** accepted.

## How It Works

```
Your client                                      Intugle (/speech)
─────────────                                    ─────────────────
connect (token, subscription, ChatApp) ───────▶
                                       ◀──────── speech:capabilities  (show or hide the mic)
speech:start {session_ref}             ───────▶
speech:audio <PCM16 frame> × n         ───────▶
                                       ◀──────── speech:partial  (text so far, repeatedly)
speech:stop {session_ref}              ───────▶
                                       ◀──────── speech:final    (finished text)
```

One recording at a time per connection. Keep the connection open while the chat screen is visible and start a new session for each recording.

## Connecting

| Setting | Value |
|---|---|
| Client library | Any **Socket.IO v4** client: `socket.io-client` (JavaScript / React Native), Socket.IO-Client-Swift, socket.io-client-java, or `python-socketio` |
| URL | `https://<your-intugle-host>/speech` (for example `https://app.intugle.ai/speech`) |
| Path | `/api/ws/socket.io` |
| Transports | `["websocket"]` |

Send these values in the connection's `auth` object:

| Field | Required | Description |
|---|---|---|
| `token` | Yes | `"Bearer <access token>"` of the signed-in user |
| `subscription_id` | Yes | The workspace (subscription) ID |
| `deployed_app_id` | For ChatApps | The ChatApp's **current** deployment ID. Needs `subscription_id`. |

Get `deployed_app_id` from the `current_deployed_app_id` field of:

```http
GET /api/v1/conversation_ai/chatapp/apps?subscription_id=<subscription_id>
Authorization: Bearer <access token>
```

With `deployed_app_id`, the connection uses the voice settings saved in that ChatApp deployment, and voice input works only if the deployment turned it on. Without it, the connection uses the workspace's current voice settings, like the chat inside Intugle; users with app-only access must always connect with a `deployed_app_id`.

The connection is refused if the token is missing or invalid, or if `deployed_app_id` is sent without `subscription_id`. Pass `auth` as a function (where your client supports it) so that each reconnect sends a fresh token.

## Checking Availability

About 200 ms after connecting, the server sends `speech:capabilities`. Emit `speech:capabilities` (no payload) to ask again at any time, for example when your app returns to the foreground.

```json
{
  "enabled": true,
  "reason": null,
  "auto_send": false,
  "max_session_seconds": 120,
  "model_name": "scribe_v3_live"
}
```

| Field | Description |
|---|---|
| `enabled` | Show the mic only when `true` |
| `reason` | Why voice input is off (see below); `null` when enabled |
| `auto_send` | `true`: send the final text as soon as recording stops. `false`: put it in the input box for the user to review. Your client applies this. |
| `max_session_seconds` | Longest recording allowed; the server stops the session after this |
| `model_name` | The primary voice model (for display only) |

| `reason` | Meaning | What to do |
|---|---|---|
| `not_configured` | No voice model is set for the workspace, or this ChatApp was deployed without one | Hide the mic |
| `disabled_for_app` | The ChatApp was deployed with voice input off | Hide the mic |
| `app_updated` | `deployed_app_id` is not the ChatApp's current version | Fetch the current `current_deployed_app_id` and reconnect |
| `unavailable` | The user has no access to this workspace or ChatApp, or the server could not load the settings | Hide the mic |

## Recording a Session

### 1. Start

Generate a unique `session_ref` (1–64 characters; a UUID works) and emit:

```json
"speech:start"  { "session_ref": "6f1c2e0a-8f3b-4c1e-9d2a-1b7e5a9c4d10" }
```

Start capturing and sending audio straight away. Do not wait for a reply: the server holds up to 12 seconds of audio while it connects to the voice provider, so the user can start speaking immediately.

The server then sends `speech:ready` with details of the model in use. It is informational:

```json
{
  "session_ref": "6f1c2e0a-…",
  "model_id": 76,
  "model_name": "scribe_v3_live",
  "provider": "elevenlabs",
  "fallback_used": false,
  "sample_rate": 16000,
  "max_session_seconds": 120
}
```

If the primary model cannot start, the fallback model is tried automatically (`fallback_used: true`).

### 2. Stream Audio

Send each chunk of microphone audio as a `speech:audio` event whose payload is **binary**:

| Property | Value |
|---|---|
| Encoding | PCM, signed 16-bit, little-endian |
| Channels | 1 (mono) |
| Sample rate | 16,000 Hz |
| Frame size | Up to 64,000 bytes. 100 ms frames (3,200 bytes) work well. |
| Payload type | Binary: `ArrayBuffer` / `Uint8Array` (JavaScript), `Data` (Swift), `byte[]` (Java/Kotlin), `bytes` (Python) |

:::warning
Frames that are not binary (for example a base64 string) or that are larger than 64,000 bytes are **dropped without an error**, and you will receive no text. Decode base64 audio to bytes before sending it.
:::

Capturing audio in the required format:

- **Android:** `AudioRecord` with `16000` Hz, `AudioFormat.CHANNEL_IN_MONO`, `AudioFormat.ENCODING_PCM_16BIT`.
- **iOS:** `AVAudioEngine` usually delivers 48 kHz float samples; convert them with `AVAudioConverter` to 16 kHz, mono, 16-bit integer.
- **React Native:** a streaming microphone library that can record 16 kHz, mono, 16-bit PCM (for example `react-native-live-audio-stream`). Such libraries often emit base64 chunks; decode each one to bytes.
- **Browser:** capture with an `AudioWorklet`, downmix to mono, resample to 16 kHz and convert the float samples to Int16.

Ask for microphone permission first: `NSMicrophoneUsageDescription` on iOS, `RECORD_AUDIO` on Android.

### 3. Show Partial Text

While the user speaks, the server sends `speech:partial`:

```json
{ "session_ref": "6f1c2e0a-…", "text": "Show me revenue for the last" }
```

`text` is the **whole transcript so far**, so replace the text you displayed, don't append to it. If the user had already typed something before tapping the mic, show the transcript after their text.

### 4. Stop and Get the Final Text

When the user taps the mic again, stop capturing and emit:

```json
"speech:stop"  { "session_ref": "6f1c2e0a-…" }
```

The server replies with `speech:final`:

```json
{
  "session_ref": "6f1c2e0a-…",
  "text": "Show me revenue for the last quarter by region.",
  "language_code": "en",
  "reason": "stopped",
  "timings": { "first_partial_ms": 1240, "total_ms": 6380 }
}
```

| `reason` | Meaning |
|---|---|
| `stopped` | The user stopped recording |
| `max_duration` | The recording reached `max_session_seconds` and the server stopped it |
| `provider_error` | The voice provider failed during the recording. `text` holds what was transcribed before the failure, and a `speech:error` follows. Do **not** auto-send it. |

The language is detected automatically; `language_code` reports what was detected. Then, if `auto_send` is `true` and `reason` is not `provider_error`, send the text as the user's message; otherwise leave it in the input box for the user to edit.

### Cancel

To abandon a recording without a final transcript (the user dismissed it, or your app went to the background), stop capturing and emit:

```json
"speech:cancel"  { "session_ref": "6f1c2e0a-…" }
```

`speech:stop` and `speech:cancel` with a `session_ref` other than the running session's are ignored.

## Errors

The server sends `speech:error`:

```json
{
  "session_ref": "6f1c2e0a-…",
  "code": "provider_unavailable",
  "message": "Voice input is not available right now",
  "retryable": true
}
```

| `code` | `retryable` | Meaning |
|---|---|---|
| `provider_unavailable` | Yes | No voice model could start a session (primary and fallback both failed) |
| `provider_error` | Yes | The voice provider failed during the recording |
| `busy` | Yes | A session is already running on this connection; stop or cancel it first |
| `not_configured` | No | No voice model is configured (see Checking Availability) |
| `disabled_for_app` | No | The ChatApp was deployed with voice input off |
| `app_updated` | No | The ChatApp has a newer deployment; reconnect with the current `deployed_app_id` |
| `forbidden` | No | The user cannot use voice input in this workspace or ChatApp |
| `bad_request` | No | The `speech:start` payload is invalid (for example a missing `session_ref`) |

For retryable errors, let the user tap the mic again. For the others, hide or disable the mic.

## App Lifecycle

- **Going to the background:** stop capturing and emit `speech:cancel`. If you don't, the server only notices when the connection drops, which can take more than a minute for a suspended app, and then cancels the session without a final transcript.
- **Returning to the foreground:** reconnect if needed; capabilities are sent again after connecting.
- **Token refresh:** reconnect with the new token (automatic when `auth` is a function).
- **Long recordings through your own proxy or load balancer:** a recording can last up to 300 seconds, so allow WebSocket connections to stay idle at least that long.

## Examples

### JavaScript / React Native

Uses `socket.io-client` v4 and, for React Native, `react-native-live-audio-stream`, the `buffer` package to decode base64 audio, and `uuid` (with `react-native-get-random-values` imported first) for session references.

```ts
import { io } from "socket.io-client";
import LiveAudioStream from "react-native-live-audio-stream";
import { Buffer } from "buffer";
import "react-native-get-random-values";
import { v4 as uuidv4 } from "uuid";

const socket = io("https://app.intugle.ai/speech", {
  path: "/api/ws/socket.io",
  transports: ["websocket"],
  auth: (cb) =>
    cb({
      token: `Bearer ${getAccessToken()}`,
      subscription_id: subscriptionId,
      deployed_app_id: currentDeployedAppId,
    }),
});

let capabilities = null;
let sessionRef = null;
let typedBefore = "";

const join = (base, text) => (!text ? base : !base || /\s$/.test(base) ? base + text : `${base} ${text}`);

socket.on("speech:capabilities", (c) => {
  capabilities = c;
  setMicVisible(c.enabled);
});

socket.on("speech:partial", ({ session_ref, text }) => {
  if (session_ref === sessionRef) setInput(join(typedBefore, text));
});

socket.on("speech:final", ({ session_ref, text, reason }) => {
  if (session_ref !== sessionRef) return;
  sessionRef = null;
  const message = join(typedBefore, text);
  if (capabilities?.auto_send && reason !== "provider_error" && message.trim()) {
    sendChatMessage(message); // your normal chat call
  } else {
    setInput(message);
  }
});

socket.on("speech:error", ({ code, message, retryable }) => {
  sessionRef = null;
  LiveAudioStream.stop();
  showToast(retryable ? `${message} Tap the mic to try again.` : message);
});

LiveAudioStream.init({ sampleRate: 16000, channels: 1, bitsPerSample: 16, audioSource: 6, bufferSize: 3200 });
LiveAudioStream.on("data", (base64) => {
  if (sessionRef) socket.emit("speech:audio", Buffer.from(base64, "base64"));
});

export function startRecording() {
  typedBefore = getInput();
  sessionRef = uuidv4();
  socket.emit("speech:start", { session_ref: sessionRef });
  LiveAudioStream.start();
}

export function stopRecording() {
  LiveAudioStream.stop();
  socket.emit("speech:stop", { session_ref: sessionRef });
}

export function cancelRecording() {
  LiveAudioStream.stop();
  if (sessionRef) socket.emit("speech:cancel", { session_ref: sessionRef });
  sessionRef = null;
}
```

### Python (testing with a WAV file)

Useful for checking a workspace's setup without a microphone. Needs `python-socketio[asyncio_client]` and a 16 kHz, mono, 16-bit WAV file.

```python
import asyncio
import uuid
import wave

import socketio

HOST = "https://app.intugle.ai"
TOKEN = "<access token>"
SUBSCRIPTION_ID = 123
DEPLOYED_APP_ID = 456  # or None for the workspace's own settings

async def main(wav_path: str) -> None:
    sio = socketio.AsyncClient()
    ready = asyncio.Event()
    done = asyncio.Event()

    capabilities = {}

    @sio.on("speech:capabilities", namespace="/speech")
    async def on_capabilities(data):
        print("capabilities:", data)
        capabilities.update(data)
        ready.set()

    @sio.on("speech:partial", namespace="/speech")
    async def on_partial(data):
        print("partial:", data["text"])

    @sio.on("speech:final", namespace="/speech")
    async def on_final(data):
        print("final:", data["text"], f"({data['reason']})")
        done.set()

    @sio.on("speech:error", namespace="/speech")
    async def on_error(data):
        print("error:", data)
        done.set()

    auth = {"token": f"Bearer {TOKEN}", "subscription_id": SUBSCRIPTION_ID}
    if DEPLOYED_APP_ID is not None:
        auth["deployed_app_id"] = DEPLOYED_APP_ID

    await sio.connect(
        HOST,
        namespaces=["/speech"],
        socketio_path="/api/ws/socket.io",
        transports=["websocket"],
        auth=auth,
    )
    await asyncio.wait_for(ready.wait(), timeout=10)
    if not capabilities.get("enabled"):
        print("Voice input is off:", capabilities.get("reason"))
        await sio.disconnect()
        return

    ref = str(uuid.uuid4())
    await sio.emit("speech:start", {"session_ref": ref}, namespace="/speech")

    with wave.open(wav_path, "rb") as wav:
        assert wav.getframerate() == 16000 and wav.getnchannels() == 1 and wav.getsampwidth() == 2
        while frames := wav.readframes(1600):  # 100 ms
            await sio.emit("speech:audio", frames, namespace="/speech")
            await asyncio.sleep(0.1)  # send in real time

    await sio.emit("speech:stop", {"session_ref": ref}, namespace="/speech")
    await asyncio.wait_for(done.wait(), timeout=30)
    await sio.disconnect()

asyncio.run(main("question.wav"))
```

## Reference

| Direction | Event | Payload |
|---|---|---|
| Client → server | `speech:capabilities` | none |
| Client → server | `speech:start` | `{session_ref}` |
| Client → server | `speech:audio` | binary PCM16 mono 16 kHz frame, ≤ 64,000 bytes |
| Client → server | `speech:stop` | `{session_ref}` |
| Client → server | `speech:cancel` | `{session_ref}` |
| Server → client | `speech:capabilities` | `{enabled, reason, auto_send, max_session_seconds, model_name}` |
| Server → client | `speech:ready` | `{session_ref, model_id, model_name, provider, fallback_used, sample_rate, max_session_seconds}` |
| Server → client | `speech:partial` | `{session_ref, text}` |
| Server → client | `speech:final` | `{session_ref, text, language_code, reason, timings: {first_partial_ms, total_ms}}` |
| Server → client | `speech:error` | `{session_ref, code, message, retryable}` |

| Limit | Value |
|---|---|
| Sessions per connection | 1 at a time |
| Longest recording | `max_session_seconds` from capabilities (at most 300 s) |
| Audio buffered before the provider is ready | 12 s |
| Largest audio frame | 64,000 bytes |

No audio is stored, and transcripts are not logged.
