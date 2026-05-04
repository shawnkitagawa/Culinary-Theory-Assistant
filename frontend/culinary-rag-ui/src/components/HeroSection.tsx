
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
            <div className="absolute inset-0 bg-gradient-to-t from-black/75 via-black/35 to-transparent" />
            <div className="absolute inset-0 bg-gradient-to-b from-black/10 via-transparent to-amber-50/10" />

            <div className="relative z-10 flex min-h-screen flex-col items-center justify-end px-6 pb-20 text-center sm:px-10 lg:pb-24">
                <p className="text-[10px] font-medium uppercase tracking-[0.35em] text-white/70">
                    CULINARY RAG SYSTEM
                </p>

                <h1 className="mt-4 max-w-4xl text-4xl font-semibold tracking-tight text-white sm:text-5xl lg:text-6xl lg:leading-[1.05]">
                    AI answers, grounded
                    <br />
                    in real technique
                </h1>

                <p className="mt-6 max-w-xl text-sm leading-6 text-white/75 sm:text-base">
                    Ask culinary questions and get clear, document-backed answers powered by AI retrieval.
                </p>

                <div className="mt-8 flex flex-col gap-3 sm:flex-row">
                    <button className="rounded-full bg-white px-6 py-3 text-sm font-medium text-black transition hover:bg-white/90">
                        See Culinary AI 1.0
                    </button>

                </div>
            </div>
        </div>

    )
}