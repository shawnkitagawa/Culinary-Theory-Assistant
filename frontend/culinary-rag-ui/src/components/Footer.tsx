import culinary_logo from "../../public/culinary_logo.svg"



export function Footer() {


    return (
        <footer className="border-t border-neutral-200 bg-white px-6 py-10">
            <div className="mx-auto flex max-w-6xl flex-col items-center text-center">
                <img
                    src={culinary_logo}
                    alt="Culinary RAG AI Logo"
                    className="h-12 w-12 object-contain"
                />

                <h3 className="mt-4 text-lg font-semibold tracking-tight text-neutral-950">
                    Culinary RAG AI
                </h3>

                <p className="mt-2 max-w-md text-sm leading-6 text-neutral-600">
                    AI-powered culinary answers backed by real sources.
                </p>

                <p className="mt-6 text-xs text-neutral-400">
                    © 2026 Culinary RAG AI. Built by Shawn Kitagawa.
                </p>
            </div>
        </footer>
    );
}