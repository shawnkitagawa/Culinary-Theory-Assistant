import { useState, useRef, useEffect } from "react";

const SAMPLE_CHATS = [
    { id: 1, title: "Maillard reaction in beef" },
    { id: 2, title: "Emulsification for sauces" },
    { id: 3, title: "Proper knife grip techniques" },
    { id: 4, title: "Salt in pasta water ratios" },
    { id: 5, title: "Resting meat after cooking" },
];

const SUGGESTIONS = [
    "How does the Maillard reaction work?",
    "Why do emulsions break?",
    "Best way to caramelize onions?",
    "When should I salt pasta water?",
];

const INITIAL_MESSAGES = [
    {
        role: "user",
        content: "Why does searing meat create a crust?",
    },
    {
        role: "assistant",
        content:
            "The crust forms through the Maillard reaction — a chemical process between amino acids and reducing sugars that occurs above 140°C (285°F). At this temperature, hundreds of new flavour compounds are created, producing the characteristic brown colour and complex, savoury aroma we associate with a well-seared steak.\n\nThe key is surface dryness: moisture causes steaming rather than searing. Pat the meat dry before it hits the pan, and ensure the pan is extremely hot before adding fat.",
        source:
            "On Food and Cooking — Harold McGee, p. 778: Maillard browning begins around 140°C and accelerates with higher heat. Surface moisture suppresses crust formation by keeping surface temperature at 100°C until evaporation is complete.",
    },
];

// ── Icons ──
const PlusIcon = () => (
    <svg width="14" height="14" viewBox="0 0 14 14" fill="none">
        <path d="M7 1v12M1 7h12" stroke="#fff" strokeWidth="1.8" strokeLinecap="round" />
    </svg>
);

const SearchIcon = () => (
    <svg width="13" height="13" viewBox="0 0 13 13" fill="none">
        <circle cx="5.5" cy="5.5" r="4" stroke="#8a7f74" strokeWidth="1.5" />
        <path d="M9 9l2.5 2.5" stroke="#8a7f74" strokeWidth="1.5" strokeLinecap="round" />
    </svg>
);

const LogoIcon = () => (
    <svg width="18" height="18" viewBox="0 0 18 18" fill="none">
        <circle cx="9" cy="9" r="8" stroke="#c4460a" strokeWidth="1.5" />
        <path d="M5 11c1-2 3-4 4-4s3 2 4 4" stroke="#c4460a" strokeWidth="1.5" strokeLinecap="round" />
        <circle cx="9" cy="6" r="1" fill="#c4460a" />
    </svg>
);

const AssistantIcon = () => (
    <svg width="10" height="10" viewBox="0 0 10 10" fill="none">
        <circle cx="5" cy="5" r="4" stroke="#fff" strokeWidth="1.2" />
        <path d="M3 6c.5-1 1.5-2 2-2s1.5 1 2 2" stroke="#fff" strokeWidth="1.2" strokeLinecap="round" />
    </svg>
);

const SourceIcon = () => (
    <svg width="12" height="12" viewBox="0 0 12 12" fill="none">
        <rect x="1" y="1" width="10" height="10" rx="2" stroke="#c4460a" strokeWidth="1.2" />
        <path d="M3.5 4h5M3.5 6h5M3.5 8h3" stroke="#c4460a" strokeWidth="1.2" strokeLinecap="round" />
    </svg>
);

const SendIcon = () => (
    <svg width="16" height="16" viewBox="0 0 16 16" fill="none">
        <path d="M2 8h12M9 3l5 5-5 5" stroke="#fff" strokeWidth="1.8" strokeLinecap="round" strokeLinejoin="round" />
    </svg>
);

// ── Sub-components ──

function TypingIndicator() {
    return (
        <div className="flex flex-col gap-2.5">
            <div className="flex items-center gap-1.5">
                <div className="flex h-5 w-5 items-center justify-center rounded-full bg-gradient-to-br from-[#c4460a] to-[#e8874a]">
                    <AssistantIcon />
                </div>
                <span className="text-[11px] font-medium uppercase tracking-widest text-[#8a7f74]">
                    Assistant
                </span>
            </div>
            <div className="flex w-fit items-center gap-1.5 rounded-tl rounded-tr-2xl rounded-br-2xl rounded-bl-2xl border border-[#e4ddd2] bg-white px-4 py-3.5 shadow-sm">
                <span className="h-2 w-2 animate-bounce rounded-full bg-[#8a7f74] [animation-delay:-0.3s]" />
                <span className="h-2 w-2 animate-bounce rounded-full bg-[#8a7f74] [animation-delay:-0.15s]" />
                <span className="h-2 w-2 animate-bounce rounded-full bg-[#8a7f74]" />
            </div>
        </div>
    );
}

function Message({ message }) {
    if (message.role === "user") {
        return (
            <div className="flex justify-end">
                <div className="max-w-[480px] rounded-tl-[18px] rounded-tr-[18px] rounded-bl-[18px] rounded-br-[4px] bg-[#1c1815] px-4 py-3 text-sm leading-relaxed text-white">
                    {message.content}
                </div>
            </div>
        );
    }

    return (
        <div className="flex flex-col gap-2.5">
            <div className="flex items-center gap-1.5">
                <div className="flex h-5 w-5 items-center justify-center rounded-full bg-gradient-to-br from-[#c4460a] to-[#e8874a]">
                    <AssistantIcon />
                </div>
                <span className="text-[11px] font-medium uppercase tracking-widest text-[#8a7f74]">
                    Assistant
                </span>
            </div>

            <div className="max-w-[520px] rounded-tl rounded-tr-[18px] rounded-br-[18px] rounded-bl-[18px] border border-[#e4ddd2] bg-white px-4 py-3.5 text-sm leading-7 text-[#1c1815] shadow-sm">
                {message.content.split("\n\n").map((para, i) => (
                    <p key={i} className={i > 0 ? "mt-3" : ""}>
                        {para}
                    </p>
                ))}
            </div>

            {message.source && (
                <div className="max-w-[520px] rounded-2xl border border-[#f5cbb5] bg-[#fdf0ea] px-4 py-3.5 text-sm leading-relaxed text-[#7a2e06]">
                    <div className="mb-2 flex items-center gap-1.5 text-[11px] font-semibold uppercase tracking-widest text-[#c4460a]">
                        <SourceIcon />
                        Retrieved source insight
                    </div>
                    <p>{message.source}</p>
                </div>
            )}
        </div>
    );
}

// ── Main Component ──

export default function Demo() {
    const [messages, setMessages] = useState(INITIAL_MESSAGES);
    const [currentChatId, setCurrentChatId] = useState(1);
    const [chats, setChats] = useState(SAMPLE_CHATS);
    const [input, setInput] = useState("");
    const [isLoading, setIsLoading] = useState(false);
    const messagesEndRef = useRef(null);

    useEffect(() => {
        messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
    }, [messages, isLoading]);

    const handleSend = async () => {
        const text = input.trim();
        if (!text || isLoading) return;
        setInput("");
        setIsLoading(true);
        setMessages((prev) => [...prev, { role: "user", content: text }]);

        // Replace with your real API call
        await new Promise((r) => setTimeout(r, 1800));
        setMessages((prev) => [
            ...prev,
            {
                role: "assistant",
                content:
                    "That's a great technique question. Based on retrieved culinary sources, the answer involves both chemistry and physical principles — ensuring that temperature, timing, and ingredient ratios all work in harmony for the best result.",
                source:
                    "Source material retrieved from culinary reference library. Cross-referenced against technique database for accuracy.",
            },
        ]);
        setIsLoading(false);
    };

    const handleKeyDown = (e) => {
        if (e.key === "Enter" && !e.shiftKey) {
            e.preventDefault();
            handleSend();
        }
    };

    const handleNewChat = () => {
        const id = Date.now();
        setChats((prev) => [{ id, title: "New conversation" }, ...prev]);
        setCurrentChatId(id);
        setMessages([]);
    };

    return (
        <div className="flex h-dvh overflow-hidden bg-[#faf7f2] text-[#1c1815]">

            {/* ── Sidebar ── */}
            <aside className="hidden w-64 flex-shrink-0 flex-col border-r border-[#e4ddd2] bg-white p-3 md:flex">

                <div className="mb-5 flex items-center gap-2 px-2 font-serif text-[13px] font-semibold tracking-wide text-[#c4460a]">
                    <LogoIcon />
                    Mise en Place
                </div>

                <button
                    onClick={handleNewChat}
                    className="flex w-full items-center gap-2 rounded-xl bg-[#c4460a] px-3.5 py-2.5 text-left text-[13px] font-medium text-white transition-colors hover:bg-[#a83908]"
                >
                    <PlusIcon />
                    New conversation
                </button>

                <button className="mt-2 flex w-full items-center gap-2 rounded-xl border border-[#e4ddd2] px-3.5 py-2.5 text-left text-[13px] text-[#8a7f74] transition-colors hover:bg-[#f2ede4]">
                    <SearchIcon />
                    Search conversations
                </button>

                <p className="mt-5 mb-2 px-2.5 text-[10px] font-medium uppercase tracking-widest text-[#8a7f74]">
                    Recent
                </p>

                <div className="flex-1 overflow-y-auto">
                    {chats.map((chat) => (
                        <button
                            key={chat.id}
                            onClick={() => setCurrentChatId(chat.id)}
                            className={`mb-0.5 w-full overflow-hidden text-ellipsis whitespace-nowrap rounded-lg px-2.5 py-2 text-left text-[13px] transition-colors ${chat.id === currentChatId
                                ? "bg-[#fdf0ea] font-medium text-[#c4460a]"
                                : "text-[#4a4037] hover:bg-[#f2ede4]"
                                }`}
                        >
                            {chat.title}
                        </button>
                    ))}
                </div>

                <div className="mt-2 border-t border-[#e4ddd2] pt-3">
                    <button className="flex w-full items-center gap-2.5 rounded-xl p-2.5 transition-colors hover:bg-[#f2ede4]">
                        <div className="flex h-8 w-8 flex-shrink-0 items-center justify-center rounded-full bg-gradient-to-br from-[#c4460a] to-[#e8874a] text-xs font-semibold text-white">
                            SK
                        </div>
                        <div className="text-left">
                            <div className="text-[13px] font-medium text-[#1c1815]">Shawn Kitagawa</div>
                            <div className="text-[11px] text-[#8a7f74]">Home chef</div>
                        </div>
                    </button>
                </div>
            </aside>

            {/* ── Main ── */}
            <main className="flex flex-1 flex-col overflow-hidden">

                <header className="flex flex-shrink-0 items-center justify-between border-b border-[#e4ddd2] bg-white px-7 py-3.5">
                    <div>
                        <div className="font-serif text-[15px] font-semibold text-[#1c1815]">
                            Culinary Technique Assistant
                        </div>
                        <div className="mt-0.5 text-[12px] text-[#8a7f74]">
                            Source-grounded cooking explanations
                        </div>
                    </div>
                    <button className="flex items-center gap-1.5 rounded-full border border-green-300 bg-green-50 px-3.5 py-1.5 text-[12px] font-medium text-green-700 transition-colors hover:bg-green-100">
                        <span className="h-2 w-2 animate-pulse rounded-full bg-green-600" />
                        Guardrails active
                    </button>
                </header>

                <div className="flex-1 overflow-y-auto px-7 py-8 [scrollbar-width:thin]">
                    <div className="mx-auto flex max-w-2xl flex-col gap-6">

                        {/* Welcome card */}
                        <div className="rounded-[20px] border border-[#e4ddd2] bg-white p-7 shadow-sm">
                            <div className="flex items-center gap-1.5 text-[10px] font-semibold uppercase tracking-[0.12em] text-[#c4460a]">
                                <span className="inline-block h-px w-4 bg-[#c4460a]" />
                                Culinary RAG Assistant
                            </div>
                            <h2 className="mt-3.5 font-serif text-[22px] font-semibold leading-snug text-[#1c1815]">
                                Ask a cooking technique question.
                            </h2>
                            <p className="mt-2.5 text-[13.5px] leading-7 text-[#8a7f74]">
                                This assistant explains culinary techniques using retrieved source material,
                                critique checks, and guardrails for safer, more grounded answers.
                            </p>
                            <div className="mt-4 flex flex-wrap gap-2">
                                {SUGGESTIONS.map((s) => (
                                    <button
                                        key={s}
                                        onClick={() => setInput(s)}
                                        className="rounded-full border border-[#e4ddd2] bg-[#f2ede4] px-3.5 py-1.5 text-[12px] text-[#4a4037] transition-all hover:border-[#f5cbb5] hover:bg-[#fdf0ea] hover:text-[#c4460a]"
                                    >
                                        {s}
                                    </button>
                                ))}
                            </div>
                        </div>

                        {messages.map((msg, i) => (
                            <Message key={i} message={msg} />
                        ))}

                        {isLoading && <TypingIndicator />}

                        <div ref={messagesEndRef} />
                    </div>
                </div>

                <div className="flex-shrink-0 border-t border-[#e4ddd2] bg-white px-7 pb-5 pt-4">
                    <div className="mx-auto max-w-2xl">
                        <div className="flex items-end gap-3 rounded-2xl border border-[#e4ddd2] bg-[#faf7f2] px-3.5 py-3 transition-colors focus-within:border-[#c4460a]">
                            <textarea
                                rows={2}
                                value={input}
                                onChange={(e) => setInput(e.target.value)}
                                onKeyDown={handleKeyDown}
                                placeholder="Ask about a cooking technique..."
                                className="max-h-32 flex-1 resize-none bg-transparent px-1 py-1 text-sm leading-relaxed text-[#1c1815] outline-none placeholder:text-[#8a7f74]"
                            />
                            <button
                                onClick={handleSend}
                                disabled={isLoading}
                                className="flex h-9 w-9 flex-shrink-0 items-center justify-center rounded-[10px] bg-[#c4460a] transition-all hover:scale-105 hover:bg-[#a83908] disabled:cursor-not-allowed disabled:opacity-40 disabled:hover:scale-100"
                            >
                                <SendIcon />
                            </button>
                        </div>
                        <p className="mt-2.5 text-center text-[11px] text-[#8a7f74]">
                            Answers grounded in retrieved culinary sources · Always verify with trusted references
                        </p>
                    </div>
                </div>
            </main>
        </div>
    );
}