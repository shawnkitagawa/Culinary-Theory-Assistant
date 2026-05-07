import culinary_logo from "../../public/culinary_logo.svg"



export function Footer() {


    return (
        <footer className="border-t border-neutral-200 bg-white px-6 py-12">
            <div className="mx-auto max-w-6xl">
                <div className="grid grid-cols-3 gap-8 mb-10">
                    <div>
                        <div className="flex items-center gap-2.5 mb-3">
                            <img src={culinary_logo} alt="" className="h-8 w-8 object-contain rounded-lg" />
                            <span className="text-[15px] font-medium text-neutral-900">Culinary RAG AI</span>
                        </div>
                        <p className="text-sm text-neutral-500 leading-relaxed">
                            AI-powered culinary answers backed by real sources.
                        </p>
                    </div>

                    <div>
                        <p className="text-xs font-medium text-neutral-400 uppercase tracking-widest mb-3">Product</p>
                        <div className="flex flex-col gap-1.5">
                            <a href="#" className="text-sm text-neutral-500 hover:text-neutral-900 transition-colors">Search recipes</a>
                            <a href="#" className="text-sm text-neutral-500 hover:text-neutral-900 transition-colors">Explore sources</a>
                            <a href="#" className="text-sm text-neutral-500 hover:text-neutral-900 transition-colors">Ask a question</a>
                        </div>
                    </div>

                    <div>
                        <p className="text-xs font-medium text-neutral-400 uppercase tracking-widest mb-3">More</p>
                        <div className="flex flex-col gap-1.5">
                            <a href="#" className="text-sm text-neutral-500 hover:text-neutral-900 transition-colors">About</a>
                            <a href="#" className="text-sm text-neutral-500 hover:text-neutral-900 transition-colors">Privacy</a>
                            <a href="#" className="text-sm text-neutral-500 hover:text-neutral-900 transition-colors">Contact</a>
                        </div>
                    </div>
                </div>

                <div className="border-t border-neutral-200 pt-5 flex items-center justify-between">
                    <p className="text-xs text-neutral-400">
                        © 2026 Culinary RAG AI. Built by Shawn Kitagawa.
                    </p>
                    <div className="flex gap-3">
                        <a href="#" className="text-neutral-400 hover:text-neutral-700 transition-colors">
                            {/* GitHub icon */}
                        </a>
                        <a href="#" className="text-neutral-400 hover:text-neutral-700 transition-colors">
                            {/* Twitter/X icon */}
                        </a>
                    </div>
                </div>
            </div>
        </footer>
    );
}