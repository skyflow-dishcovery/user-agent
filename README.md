Here's an updated and well-organized `README.md` file including the **Intent Agent** and all work done so far:

---

# ✨ Dishcovery x SkyFlow — Multimodal, Context-Aware AI Agents

> A real-world, Prosus-ready AI system combining **food ordering (Dishcovery)** and **travel booking (SkyFlow)** powered by **Groq + LLaMA3**, voice/text input, user memory, and contextual agents.

---

## ✅ FEATURES IMPLEMENTED SO FAR

---

### 🔐 1. User Authentication System

**Tech:** FastAPI · PostgreSQL (Supabase) · JWT

* Secure signup and login routes.
* Passwords hashed before storing.
* JWT-based session handling.
* User ID passed in all agent calls for personalization.

---

### 🧠 2. Input Agent (Text + Voice)

**Goal:** Normalize input to English and pass to next agent.

* **Voice Input:**

  * Converts voice file to text using **Groq Whisper API**.
* **Text Input:**

  * Translates non-English text to English via **LLaMA3 (Groq)**.
* Returns `{ user_id, translated_text }`.

📍 **Endpoints:**

```
POST /agent/voice
POST /agent/text
```

---

### 🧠 3. Intent Agent (With User History)

**Goal:** Determine whether input is related to Dishcovery (food) or SkyFlow (travel) and regenerate a clear version of the user’s message.

**Key Features:**

* Loads past conversation history from DB.
* Uses **Groq LLaMA3** to classify the **intent**:

  * "dishcovery" or "skyflow"
* Refines user query using the history for clarity.
* Updates history with this refined input for future context.

📍 **Endpoint:**

```
POST /agent/intent
```

🔑 Fields:

* `user_id` (from JWT)
* `text` (user query)

---

### 🌍 4. Response Agent (With Location Awareness)

**Goal:** Final response generation using location + refined input + intent.

**Features:**

* Converts `latitude` & `longitude` into city + country using **GeoPy**.
* Generates a context-aware response via **LLaMA3**.
* Personalized reply for food or travel depending on intent.

📍 **Endpoint:**

```
POST /agent/response
```

🔑 Fields:

* `user_id`
* `intent` (from Intent Agent)
* `user_input` (refined)
* `latitude`, `longitude`

---

### 🧾 5. User History & Personalization

**Status:** ✅ Implemented

* User message history fetched from PostgreSQL.
* Appended automatically after each Intent Agent step.
* Enables better continuity, fallbacks, personalization.

---

## 🧩 SYSTEM ARCHITECTURE

```text
[User Input]
   ↓ voice/text
[Input Agent] 
   ↓ translated English
[Intent Agent]
   ↓ {intent, refined_input}
[Response Agent]
   ↓ + location
[Final Output to Restaurant / Travel agent according to user's intent]
```

---

## 🧪 HOW TO TEST

1. Clone the repo & install dependencies:

```bash
pip install -r requirements.txt
```

2. Add your `.env`:

```env
GROQ_API_KEY=your_key
```

3. Run the server:

```bash
uvicorn app.main:app --reload
```

4. Use POSTMAN to test endpoints.

---

## 🔄 FLOW SUMMARY

```
1. User logs in → gets JWT
2. Sends input via voice or text → translated to English
3. Intent Agent uses history to detect topic + refine input
4. Response Agent generates answer using user’s location
5. History is updated for next query
6. Generated response is sent to restaurant / travel agent respectively.
```

---
