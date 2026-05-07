
import culinary_video from "../../public/culinary_video.mp4"

export function HeroSection() {
    return (
        <div className="relative min-h-screen overflow-hidden bg-black">
            {/* Background video */}
            <video
                className="absolute inset-0 h-full w-full object-cover"
                src={culinary_video}
                autoPlay
                muted
                playsInline
                loop
            />

            {/* Overlays */}
            <div className="absolute inset-0 bg-black/35" />
            <div className="absolute inset-0 bg-gradient-to-t from-black/80 via-black/35 to-black/10" />
            <div className="absolute inset-0 bg-[radial-gradient(ellipse_at_50%_90%,rgba(180,100,20,0.12),transparent_65%)]" />

            <div className="relative z-10 flex min-h-screen flex-col items-center justify-end px-6 pb-20 text-center sm:px-10 lg:pb-28">

                {/* Badge */}
                <div className="mb-6 flex items-center gap-1.5 rounded-full border border-white/20 bg-white/8 px-4 py-1.5 backdrop-blur-sm">
                    <span className="h-1.5 w-1.5 rounded-full bg-amber-400" />
                    <span className="text-[10px] font-medium uppercase tracking-[0.32em] text-white/70">
                        Culinary RAG System
                    </span>
                </div>

                <h1 className="max-w-4xl text-4xl font-semibold tracking-tight text-white sm:text-5xl lg:text-[3.5rem] lg:leading-[1.06]">
                    AI answers, grounded
                    <br />
                    in real technique
                </h1>

                <p className="mt-5 max-w-md text-[15px] leading-relaxed text-white/70">
                    Ask culinary questions and get clear, document-backed answers powered by AI retrieval.
                </p>

                <div className="mt-8 flex flex-col gap-3 sm:flex-row">
                    <button className="rounded-full bg-white px-6 py-3 text-sm font-medium text-black transition hover:bg-white/90 active:scale-[0.97]">
                        See Culinary AI 1.0
                    </button>
                    <button className="rounded-full border border-white/20 bg-white/10 px-6 py-3 text-sm font-medium text-white/90 backdrop-blur-sm transition hover:bg-white/15 active:scale-[0.97]">
                        Ask a question →
                    </button>
                </div>

            </div>
        </div>
    );
}