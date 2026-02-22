class HAcoBotCard extends HTMLElement {
    constructor() {
        super();
        this.attachShadow({ mode: 'open' });
        this._hass = null;
        this._initialized = false;
        this._messages = [];
    }

    setConfig(config) {
        this._config = config;
    }

    set hass(hass) {
        this._hass = hass;
        // Nur einmal rendern, um Eingabefokus zu behalten
        if (!this._initialized) {
            this._initialized = true;
            this._firstRender();
        }
    }

    getCardSize() {
        return 5; 
    }

    _handleKeyDown(e) {
        if (e.key === 'Enter') {
            this._sendMessage();
        }
    }

    async _sendMessage() {
        const input = this.shadowRoot.getElementById('input');
        const text = input.value.trim();
        if (!text) return;

        // User Nachricht
        this._appendMessage('user', text);
        input.value = ''; 
        
        // Lade-Animation
        const loadingId = this._appendMessage('bot', '...', true);

        try {
            const response = await this._hass.callWS({
                type: 'call_service',
                domain: 'hacobot',
                service: 'process_prompt',
                service_data: {
                    prompt: text
                },
                return_response: true
            });

            // Lade-Animation weg
            const loadingEl = this.shadowRoot.getElementById(loadingId);
            if (loadingEl) loadingEl.remove();

            // ANTWORT EXTRAHIEREN (Die "Zwiebel" schälen)
            const replyText = this._extractReply(response);
            
            this._appendMessage('bot', replyText);

        } catch (err) {
            const loadingEl = this.shadowRoot.getElementById(loadingId);
            if (loadingEl) loadingEl.remove();
            
            let errMsg = err.message || JSON.stringify(err);
            this._appendMessage('bot', `Fehler: ${errMsg}`);
        }
    }

    // Rekursive Funktion zum Finden des echten Textes
    _extractReply(data) {
        if (data === null || data === undefined) return "Keine Antwort.";
        
        // 1. JSON String parsen
        if (typeof data === 'string') {
            try {
                // Prüfen ob es JSON ist (startet mit { oder [)
                if (data.trim().startsWith('{') || data.trim().startsWith('[')) {
                    const parsed = JSON.parse(data);
                    return this._extractReply(parsed); // Rekursion mit Objekt
                }
                // Kein JSON, also ist es der Text selbst
                return this._cleanString(data);
            } catch (e) {
                return this._cleanString(data);
            }
        }

        // 2. Objekte durchsuchen
        if (typeof data === 'object') {
            // Home Assistant schachtelt oft: { response: { response: "Text" } }
            if ('response' in data) {
                return this._extractReply(data.response);
            }
            if ('result' in data) {
                return this._extractReply(data.result);
            }
            // Fallback: Wenn wir am Ende eines Objekts sind und keine bekannten Keys finden,
            // zeigen wir das Objekt formatiert an (besser als [object Object])
            return JSON.stringify(data, null, 2);
        }

        return String(data);
    }

    _cleanString(str) {
        // Bereinigt Strings von Artefakten
        if (!str) return "";
        // Manchmal sind Strings doppelt encodet mit Anführungszeichen
        if (str.startsWith('"') && str.endsWith('"') && str.length > 1) {
            try {
                 // JSON parse entfernt Quotes und escaped Zeilenumbrüche (\n -> newline)
                return JSON.parse(str); 
            } catch (e) {
                return str.slice(1, -1);
            }
        }
        return str;
    }

    _appendMessage(sender, text, isLoading = false) {
        const history = this.shadowRoot.getElementById('history');
        if (!history) return;

        const msgDiv = document.createElement('div');
        msgDiv.className = `message ${sender}`;
        if (isLoading) msgDiv.id = `loading-${Date.now()}`;
        
        // Hier wenden wir die Markdown-Formatierung an
        msgDiv.innerHTML = `<div class="bubble">${this._formatText(text)}</div>`;
        
        history.appendChild(msgDiv);
        history.scrollTop = history.scrollHeight;
        return msgDiv.id;
    }

    _formatText(text) {
        if (!text) return "";
        let formatted = String(text);

        // Markdown: Fett (**text**)
        formatted = formatted.replace(/\*\*(.*?)\*\*/g, '<b>$1</b>');
        
        // Markdown: Code (`text`)
        formatted = formatted.replace(/`(.*?)`/g, '<code>$1</code>');
        
        // Markdown: Listen (- Punkt)
        // Ersetzt Zeilen die mit "- " beginnen durch einen Bullet Point und Zeilenumbruch
        formatted = formatted.replace(/(^|\n)- (.*)/g, '<br>• $2');
        
        // Zeilenumbrüche erhalten
        formatted = formatted.replace(/\n/g, '<br>');
        
        // Aufeinanderfolgende <br> am Anfang bereinigen (durch Listen-Replace entstanden)
        if (formatted.startsWith('<br>')) formatted = formatted.substring(4);

        return formatted;
    }

    _firstRender() {
        this.shadowRoot.innerHTML = `
            <style>
                :host {
                    display: block;
                    height: 500px; /* Fixe Höhe für Scrollen */
                }
                ha-card {
                    height: 100%;
                    display: flex;
                    flex-direction: column;
                    background: var(--ha-card-background, var(--card-background-color, white));
                    border: var(--ha-card-border, 1px solid var(--divider-color));
                    border-radius: var(--ha-card-border-radius, 12px);
                    box-shadow: var(--ha-card-box-shadow, 0 2px 2px 0 rgba(0,0,0,0.14));
                    overflow: hidden;
                }
                .header {
                    padding: 16px;
                    font-size: 18px;
                    font-weight: 500;
                    color: var(--primary-text-color);
                    background: var(--secondary-background-color);
                    border-bottom: 1px solid var(--divider-color);
                    display: flex;
                    align-items: center;
                    gap: 10px;
                    flex-shrink: 0;
                }
                .history {
                    flex: 1;
                    overflow-y: auto;
                    min-height: 0;
                    padding: 16px;
                    display: flex;
                    flex-direction: column;
                    gap: 8px;
                }
                .message {
                    display: flex;
                    margin-bottom: 4px;
                    animation: fadeIn 0.2s ease-out;
                    flex-shrink: 0;
                }
                @keyframes fadeIn {
                    from { opacity: 0; transform: translateY(5px); }
                    to { opacity: 1; transform: translateY(0); }
                }
                .message.user {
                    justify-content: flex-end;
                }
                .message.bot {
                    justify-content: flex-start;
                }
                .bubble {
                    padding: 8px 14px;
                    border-radius: 12px;
                    max-width: 85%;
                    word-wrap: break-word;
                    font-size: 14px;
                    line-height: 1.5;
                }
                .user .bubble {
                    background: var(--primary-color);
                    color: var(--text-primary-color);
                    border-bottom-right-radius: 2px;
                }
                .bot .bubble {
                    background: var(--secondary-background-color);
                    color: var(--primary-text-color);
                    border-bottom-left-radius: 2px;
                    border: 1px solid var(--divider-color);
                }
                .input-area {
                    padding: 10px;
                    background: var(--card-background-color);
                    border-top: 1px solid var(--divider-color);
                    display: flex;
                    gap: 8px;
                    align-items: center;
                    flex-shrink: 0;
                }
                input {
                    flex: 1;
                    padding: 12px;
                    border-radius: 20px;
                    border: 1px solid var(--divider-color);
                    background: var(--secondary-background-color);
                    color: var(--primary-text-color);
                    outline: none;
                    transition: border-color 0.2s;
                }
                input:focus {
                    border-color: var(--primary-color);
                }
                button {
                    background: var(--primary-color);
                    color: var(--text-primary-color);
                    border: none;
                    border-radius: 50%;
                    width: 42px;
                    height: 42px;
                    cursor: pointer;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    transition: filter 0.2s;
                }
                button:hover {
                    filter: brightness(1.1);
                }
                
                /* Markdown Style */
                .bubble b { font-weight: 700; }
                .bubble ul { margin: 5px 0; padding-left: 20px; }
                .bubble li { margin-bottom: 2px; }
                .bubble code { 
                    background: rgba(0,0,0,0.15); 
                    padding: 2px 4px; 
                    border-radius: 4px; 
                    font-family: monospace; 
                    font-size: 90%;
                }
                .bubble pre {
                    white-space: pre-wrap;
                    background: rgba(0,0,0,0.1);
                    padding: 5px;
                    border-radius: 5px;
                }
            </style>
            
            <ha-card>
                <div class="header">
                    <ha-icon icon="mdi:robot"></ha-icon>
                    HAcoBot
                </div>
                <div class="history" id="history">
                    <div class="message bot">
                        <div class="bubble">Hallo! Ich bin HAcoBot. Wie kann ich helfen?</div>
                    </div>
                </div>
                <div class="input-area">
                    <input type="text" id="input" placeholder="Nachricht eingeben..." autocomplete="off">
                    <button id="send">
                        <ha-icon icon="mdi:send"></ha-icon>
                    </button>
                </div>
            </ha-card>
        `;

        const inputEl = this.shadowRoot.getElementById('input');
        const sendBtn = this.shadowRoot.getElementById('send');
        
        inputEl.addEventListener('keydown', this._handleKeyDown.bind(this));
        sendBtn.addEventListener('click', () => this._sendMessage());
    }
}

customElements.define('hacobot-card', HAcoBotCard);

window.customCards = window.customCards || [];
window.customCards.push({
    type: "hacobot-card",
    name: "HAcoBot Chat",
    preview: true,
    description: "Chatte direkt mit deinem Smart Home Admin."
});
