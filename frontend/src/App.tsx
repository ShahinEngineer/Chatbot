import { useState, useRef } from "react";
import "./App.css";
import type { MESSAGE } from "./types";

function App() {
  const [messages, setMessages] = useState<MESSAGE[]>([]);
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);
  const eventSourceRef = useRef<EventSource | null>(null);
  const sessionId = "test_session";
  const apiUrl = import.meta.env.VITE_API_URL;

  console.log("API URL:", apiUrl);

  const handleSend = async () => {
    const userInput = input.trim();
    if (!userInput) return;

    setMessages((prev) => [...prev, { text: userInput, sender: "user" }]);
    setInput("");
    setLoading(true);

    // Start empty bot message placeholder
    setMessages((prev) => [...prev, { text: "", sender: "bot" }]);

    try {
      await fetch(`${apiUrl}/chat`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ message: userInput, session_id: sessionId }),
      });

      if (eventSourceRef.current) {
        eventSourceRef.current.close();
      }

      const es = new EventSource(`${apiUrl}/chat/sse?session_id=${sessionId}`);
      eventSourceRef.current = es;

      es.onmessage = (event) => {
        const chunk = event.data;

        // Append streamed data to the last bot message
        setMessages((prev) => {
          const updated = [...prev];
          const lastIndex = updated.length - 1;
          updated[lastIndex] = {
            ...updated[lastIndex],
            text: updated[lastIndex].text + chunk,
          };
          return updated;
        });
      };

      es.onerror = (err) => {
        console.error("SSE error:", err);
        es.close();
        setLoading(false);
      };

      es.onopen = () => {
        setLoading(false);
      };
    } catch (err) {
      setMessages((prev) => [
        ...prev,
        { text: `Error contacting server.${(err as Error).message}`, sender: "bot" },
      ]);
      setLoading(false);
    }
  };

  return (
    <div className="chat-container">
      <div className="chat-box">
        {messages.map((msg, idx) => (
          <div
            key={idx}
            className={`chat-message ${msg.sender === "user" ? "user" : "bot"}`}
          >
            <span>{msg.text}</span>
          </div>
        ))}
      </div>

      <div className="chat-input">
        <textarea
          value={input}
          onChange={(e) => setInput(e.target.value)}
          placeholder="Type your message..."
          disabled={loading}
        />
        <button onClick={handleSend} disabled={loading}>
          {loading ? "..." : "Send"}
        </button>
      </div>
    </div>
  );
}

export default App;
